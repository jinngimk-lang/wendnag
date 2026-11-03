"""Parser adapter for SEC EDGAR submissions + companyfacts JSON payloads.

This adapter does not perform HTTP requests. A separate fetcher must obtain the
SEC responses in compliance with SEC access policy and pass them here. Facts
are anchored to the filing's acceptanceDateTime, never just the period end or
filingDate. License review is required by default; callers must not mark data
approved without completing their own terms review.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from hashlib import sha256
from typing import Any, Mapping

from backend.research_gateway import (
    EvidenceRecord, EvidenceValidationError, Issuer, LicenseStatus, SourceType,
    as_utc,
)


class SECAdapterError(ValueError):
    pass


def _normalize_cik(value: Any) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if not digits:
        raise SECAdapterError("SEC payload is missing a valid CIK")
    return digits.zfill(10)


def _parse_sec_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise SECAdapterError(f"SEC filing is missing {field_name}")
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise SECAdapterError(f"invalid SEC {field_name}: {value}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SECAdapterError(f"SEC {field_name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _parse_period(value: Any, field_name: str, *, required: bool = True) -> str | None:
    if value in (None, "") and not required:
        return None
    if not isinstance(value, str):
        raise SECAdapterError(f"invalid SEC {field_name}")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise SECAdapterError(f"invalid SEC {field_name}: {value}") from exc


def issuer_candidates_from_submissions(submissions: Mapping[str, Any]) -> tuple[Issuer, ...]:
    """Create canonical CIK-backed candidates; share-class ambiguity is retained."""
    cik = _normalize_cik(submissions.get("cik"))
    legal_name = submissions.get("name")
    if not isinstance(legal_name, str) or not legal_name.strip():
        raise SECAdapterError("SEC submissions payload is missing issuer name")
    tickers = submissions.get("tickers") or []
    exchanges = submissions.get("exchanges") or []
    if not isinstance(tickers, list) or not isinstance(exchanges, list):
        raise SECAdapterError("SEC tickers and exchanges must be arrays")
    candidates: list[Issuer] = []
    seen: set[tuple[str, str]] = set()
    for index, raw_ticker in enumerate(tickers):
        if not isinstance(raw_ticker, str) or not raw_ticker.strip():
            continue
        ticker = raw_ticker.strip().upper()
        raw_exchange = exchanges[index] if index < len(exchanges) else "UNKNOWN"
        exchange = raw_exchange.strip().upper() if isinstance(raw_exchange, str) and raw_exchange.strip() else "UNKNOWN"
        if (ticker, exchange) in seen:
            continue
        seen.add((ticker, exchange))
        candidates.append(Issuer(
            issuer_id=f"cik:{cik}", legal_name=legal_name.strip(), ticker=ticker,
            exchange=exchange, currency="UNKNOWN", cik=cik,
        ))
    if not candidates:
        candidates.append(Issuer(
            issuer_id=f"cik:{cik}", legal_name=legal_name.strip(), ticker=cik,
            exchange="SEC", currency="UNKNOWN", cik=cik,
        ))
    return tuple(candidates)


@dataclass(frozen=True, slots=True)
class SECParseResult:
    issuer_candidates: tuple[Issuer, ...]
    records: tuple[EvidenceRecord, ...]
    skipped_unmatched_accessions: int
    skipped_form_mismatches: int
    skipped_invalid_values: int


def parse_companyfacts(
    submissions: Mapping[str, Any],
    companyfacts: Mapping[str, Any],
    *,
    retrieved_at: datetime,
    license_status: LicenseStatus = LicenseStatus.REVIEW_REQUIRED,
    license_id: str = "sec-edgar-public-data-terms-review-required",
) -> SECParseResult:
    """Normalize SEC companyfacts observations using accession acceptance times."""
    cik = _normalize_cik(submissions.get("cik"))
    facts_cik = companyfacts.get("cik")
    if facts_cik is not None and _normalize_cik(facts_cik) != cik:
        raise SECAdapterError("SEC submissions and companyfacts CIK values do not match")
    retrieved = as_utc(retrieved_at, "retrieved_at")
    filings = submissions.get("filings", {}).get("recent", {})
    if not isinstance(filings, Mapping):
        raise SECAdapterError("SEC submissions payload is missing filings.recent")
    accession_numbers = filings.get("accessionNumber") or []
    accepted_times = filings.get("acceptanceDateTime") or []
    forms = filings.get("form") or []
    filing_dates = filings.get("filingDate") or []
    if not all(isinstance(x, list) for x in (accession_numbers, accepted_times, forms, filing_dates)):
        raise SECAdapterError("SEC recent filing columns must be arrays")

    filing_by_accession: dict[str, dict[str, Any]] = {}
    for index, accession in enumerate(accession_numbers):
        if not isinstance(accession, str) or not accession.strip():
            continue
        accepted_raw = accepted_times[index] if index < len(accepted_times) else None
        if not accepted_raw:
            continue  # no acceptance timestamp: do not guess from filingDate
        accepted_at = _parse_sec_datetime(accepted_raw, "acceptanceDateTime")
        if accepted_at > retrieved:
            raise SECAdapterError(f"retrieved_at predates filing availability: {accession}")
        form = forms[index].strip() if index < len(forms) and isinstance(forms[index], str) else "UNKNOWN"
        filing_date = filing_dates[index] if index < len(filing_dates) else None
        filing_by_accession[accession] = {
            "accepted_at": accepted_at,
            "form": form,
            "filing_date": _parse_period(filing_date, "filingDate") if filing_date else None,
        }

    facts = companyfacts.get("facts")
    if not isinstance(facts, Mapping):
        raise SECAdapterError("SEC companyfacts payload is missing facts object")
    cik_path = str(int(cik))
    records: list[EvidenceRecord] = []
    skipped_unmatched = skipped_form = skipped_values = 0
    for taxonomy, tags in facts.items():
        if not isinstance(tags, Mapping):
            continue
        for tag, spec in tags.items():
            if not isinstance(spec, Mapping) or not isinstance(spec.get("units"), Mapping):
                continue
            for unit, observations in spec["units"].items():
                if not isinstance(observations, list):
                    continue
                for observation in observations:
                    if not isinstance(observation, Mapping):
                        skipped_values += 1
                        continue
                    accession = observation.get("accn")
                    filing = filing_by_accession.get(accession) if isinstance(accession, str) else None
                    if filing is None:
                        skipped_unmatched += 1
                        continue
                    observation_form = observation.get("form")
                    if observation_form and filing["form"] != "UNKNOWN" and observation_form != filing["form"]:
                        skipped_form += 1
                        continue
                    value = observation.get("val")
                    if isinstance(value, bool) or not isinstance(value, (int, float)):
                        skipped_values += 1
                        continue
                    try:
                        period_end = _parse_period(observation.get("end"), "fact period end")
                        period_start = _parse_period(observation.get("start"), "fact period start", required=False)
                    except SECAdapterError:
                        skipped_values += 1
                        continue
                    accepted_at = filing["accepted_at"]
                    accession_clean = accession.replace("-", "")
                    key = "|".join((cik, accession, str(taxonomy), str(tag), str(unit), str(period_start), str(period_end), str(filing["form"])))
                    evidence_id = "sec_" + sha256(key.encode("utf-8")).hexdigest()[:24]
                    title = f"{taxonomy}.{tag} ({unit})"
                    source_url = f"https://www.sec.gov/Archives/edgar/data/{cik_path}/{accession_clean}/"
                    payload = {
                        "taxonomy": str(taxonomy), "tag": str(tag), "label": spec.get("label"),
                        "description": spec.get("description"), "unit": str(unit), "value": value,
                        "period_start": period_start, "period_end": period_end,
                        "form": filing["form"], "filing_date": filing["filing_date"],
                        "acceptance_datetime": accepted_at.isoformat(), "accession": accession,
                        "fiscal_year": observation.get("fy"), "fiscal_period": observation.get("fp"),
                        "frame": observation.get("frame"),
                    }
                    try:
                        records.append(EvidenceRecord.create(
                            evidence_id=evidence_id, issuer_id=f"cik:{cik}",
                            source_type=SourceType.FINANCIAL_METRIC, title=title, source_url=source_url,
                            published_at=accepted_at, available_at=accepted_at, retrieved_at=retrieved,
                            provider="sec-edgar-companyfacts", license_id=license_id,
                            license_status=license_status, payload=payload, source_version=accession,
                        ))
                    except EvidenceValidationError as exc:
                        raise SECAdapterError(str(exc)) from exc

    records.sort(key=lambda record: (record.available_at, record.evidence_id))
    return SECParseResult(
        issuer_candidates=issuer_candidates_from_submissions(submissions), records=tuple(records),
        skipped_unmatched_accessions=skipped_unmatched, skipped_form_mismatches=skipped_form,
        skipped_invalid_values=skipped_values,
    )
