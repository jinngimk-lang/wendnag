"""Point-in-time evidence and audit contracts for AI Arena.

This module is deliberately provider-agnostic and uses only the Python standard
library. It does not fetch market data, resolve real tickers, call an LLM, or
place orders. Production adapters must create EvidenceRecord instances only
from licensed, source-attributed data and preserve the source's as-known-at-time
availability timestamp.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
import math
from types import MappingProxyType
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse


class GatewayError(ValueError):
    """Base class for invalid evidence, issuer, or research contracts."""


class EvidenceValidationError(GatewayError):
    pass


class IssuerResolutionError(GatewayError):
    pass


class ResearchContractError(GatewayError):
    pass


class SourceType(str, Enum):
    FILING = "filing"
    FINANCIAL_METRIC = "financial_metric"
    PRICE_BAR = "price_bar"
    NEWS = "news"
    MACRO = "macro"
    SENTIMENT = "sentiment"


class LicenseStatus(str, Enum):
    APPROVED = "approved"
    REVIEW_REQUIRED = "review_required"
    RESTRICTED = "restricted"


class Stance(str, Enum):
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"


FACTION_IDS = frozenset({"value", "growth", "trend", "quant", "sentiment", "macro"})
GENESIS_HASH = "GENESIS"


def as_utc(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise GatewayError(f"{field_name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _freeze_json(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise GatewayError("JSON payload numbers must be finite")
        return value
    if isinstance(value, Mapping):
        if not all(isinstance(k, str) for k in value):
            raise GatewayError("JSON object keys must be strings")
        return MappingProxyType({k: _freeze_json(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(v) for v in value)
    raise GatewayError(f"Unsupported JSON payload value: {type(value).__name__}")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _thaw_json(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest_json(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _nonempty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GatewayError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class Issuer:
    issuer_id: str
    legal_name: str
    ticker: str
    exchange: str
    currency: str = "USD"
    share_class: str = ""
    cik: str | None = None
    aliases: tuple[str, ...] = ()
    active: bool = True

    def __post_init__(self) -> None:
        for field_name in ("issuer_id", "legal_name", "ticker", "exchange", "currency"):
            object.__setattr__(self, field_name, _nonempty(getattr(self, field_name), field_name))
        object.__setattr__(self, "ticker", self.ticker.upper())
        object.__setattr__(self, "exchange", self.exchange.upper())
        object.__setattr__(self, "currency", self.currency.upper())
        object.__setattr__(self, "aliases", tuple(_nonempty(x, "alias") for x in self.aliases))
        if self.cik is not None:
            digits = "".join(ch for ch in str(self.cik) if ch.isdigit())
            if not digits:
                raise GatewayError("CIK must contain digits")
            object.__setattr__(self, "cik", digits.zfill(10))


@dataclass(frozen=True, slots=True)
class IssuerResolution:
    status: str
    query: str
    issuer: Issuer | None
    candidates: tuple[Issuer, ...]


def resolve_issuer(query: str, issuers: Iterable[Issuer]) -> IssuerResolution:
    """Resolve exact identifiers only; ambiguous tickers are never guessed."""
    raw = _nonempty(query, "query")
    q = " ".join(raw.upper().split())
    exchange = ticker = None
    if ":" in q:
        exchange, ticker = (part.strip() for part in q.split(":", 1))
        if not exchange or not ticker:
            return IssuerResolution("not_found", raw, None, ())
    matches: list[Issuer] = []
    for issuer in issuers:
        keys = {issuer.issuer_id.upper(), issuer.legal_name.upper(), issuer.ticker.upper()}
        keys.update(alias.upper() for alias in issuer.aliases)
        if issuer.cik:
            keys.add(issuer.cik.upper())
        match = (issuer.exchange == exchange and issuer.ticker == ticker) if exchange else q in keys
        if match and issuer not in matches:
            matches.append(issuer)
    matches.sort(key=lambda x: (x.exchange, x.ticker, x.issuer_id))
    if len(matches) == 1:
        return IssuerResolution("resolved", raw, matches[0], tuple(matches))
    if matches:
        return IssuerResolution("ambiguous", raw, None, tuple(matches))
    return IssuerResolution("not_found", raw, None, ())


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    issuer_id: str
    source_type: SourceType
    title: str
    source_url: str
    published_at: datetime
    available_at: datetime
    retrieved_at: datetime
    provider: str
    license_id: str
    license_status: LicenseStatus
    payload: Mapping[str, Any]
    content_hash: str
    source_version: str = ""

    @classmethod
    def create(
        cls,
        *,
        evidence_id: str,
        issuer_id: str,
        source_type: SourceType,
        title: str,
        source_url: str,
        published_at: datetime,
        available_at: datetime,
        retrieved_at: datetime,
        provider: str,
        license_id: str,
        license_status: LicenseStatus,
        payload: Mapping[str, Any],
        source_version: str = "",
    ) -> "EvidenceRecord":
        published = as_utc(published_at, "published_at")
        available = as_utc(available_at, "available_at")
        retrieved = as_utc(retrieved_at, "retrieved_at")
        if available < published:
            raise EvidenceValidationError("available_at cannot precede published_at")
        if retrieved < available:
            raise EvidenceValidationError("retrieved_at cannot precede available_at")
        frozen_payload = _freeze_json(payload)
        if not isinstance(frozen_payload, Mapping):
            raise EvidenceValidationError("payload must be a JSON object")
        record_fields = {
            "evidence_id": _nonempty(evidence_id, "evidence_id"),
            "issuer_id": _nonempty(issuer_id, "issuer_id"),
            "source_type": SourceType(source_type).value,
            "title": _nonempty(title, "title"),
            "source_url": _nonempty(source_url, "source_url"),
            "published_at": published.isoformat(),
            "available_at": available.isoformat(),
            "retrieved_at": retrieved.isoformat(),
            "provider": _nonempty(provider, "provider"),
            "license_id": _nonempty(license_id, "license_id"),
            "license_status": LicenseStatus(license_status).value,
            "payload": _thaw_json(frozen_payload),
            "source_version": source_version.strip(),
        }
        parsed_url = urlparse(record_fields["source_url"])
        if parsed_url.scheme not in {"https", "http"} or not parsed_url.netloc:
            raise EvidenceValidationError("source_url must be an absolute HTTP(S) URL")
        return cls(
            evidence_id=record_fields["evidence_id"], issuer_id=record_fields["issuer_id"],
            source_type=SourceType(record_fields["source_type"]), title=record_fields["title"],
            source_url=record_fields["source_url"], published_at=published, available_at=available,
            retrieved_at=retrieved, provider=record_fields["provider"], license_id=record_fields["license_id"],
            license_status=LicenseStatus(record_fields["license_status"]), payload=frozen_payload,
            content_hash=digest_json(record_fields), source_version=record_fields["source_version"],
        )

    def hash_payload(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id, "issuer_id": self.issuer_id,
            "source_type": self.source_type.value, "title": self.title, "source_url": self.source_url,
            "published_at": self.published_at.isoformat(), "available_at": self.available_at.isoformat(),
            "retrieved_at": self.retrieved_at.isoformat(), "provider": self.provider,
            "license_id": self.license_id, "license_status": self.license_status.value,
            "payload": _thaw_json(self.payload), "source_version": self.source_version,
        }

    def verify_hash(self) -> bool:
        return digest_json(self.hash_payload()) == self.content_hash

    def to_dict(self) -> dict[str, Any]:
        return {**self.hash_payload(), "content_hash": self.content_hash}


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot:
    snapshot_id: str
    issuer_id: str
    as_of: datetime
    created_at: datetime
    records: tuple[EvidenceRecord, ...]
    manifest_hash: str

    def manifest(self) -> dict[str, Any]:
        return {
            "issuer_id": self.issuer_id,
            "as_of": self.as_of.isoformat(),
            "evidence": [{"evidence_id": r.evidence_id, "content_hash": r.content_hash} for r in self.records],
        }

    def verify(self) -> bool:
        try:
            cutoff = as_utc(self.as_of, "as_of")
            created = as_utc(self.created_at, "created_at")
            if created < cutoff or len({r.evidence_id for r in self.records}) != len(self.records):
                return False
            if any(not r.verify_hash() or r.issuer_id != self.issuer_id or r.available_at > cutoff
                   or r.retrieved_at > created or r.license_status is not LicenseStatus.APPROVED
                   for r in self.records):
                return False
            manifest_hash = digest_json(self.manifest())
            expected_id = "snap_" + manifest_hash[:24]
            return self.manifest_hash == manifest_hash and self.snapshot_id == expected_id
        except (GatewayError, TypeError, ValueError):
            return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id, "issuer_id": self.issuer_id,
            "as_of": self.as_of.isoformat(), "created_at": self.created_at.isoformat(),
            "manifest_hash": self.manifest_hash, "records": [r.to_dict() for r in self.records],
        }


def freeze_evidence_pack(
    issuer_id: str,
    as_of: datetime,
    records: Iterable[EvidenceRecord],
    *,
    created_at: datetime,
) -> EvidenceSnapshot:
    """Freeze one shared evidence set, excluding anything not yet public at as_of."""
    issuer = _nonempty(issuer_id, "issuer_id")
    cutoff = as_utc(as_of, "as_of")
    created = as_utc(created_at, "created_at")
    if created < cutoff:
        raise EvidenceValidationError("created_at cannot precede the research as_of cutoff")
    accepted: list[EvidenceRecord] = []
    seen: dict[str, str] = {}
    for record in records:
        if not record.verify_hash():
            raise EvidenceValidationError(f"evidence hash mismatch: {record.evidence_id}")
        if record.issuer_id != issuer:
            raise EvidenceValidationError(f"foreign issuer evidence: {record.evidence_id}")
        if record.retrieved_at > created:
            raise EvidenceValidationError(f"evidence retrieved after snapshot creation: {record.evidence_id}")
        if record.license_status is not LicenseStatus.APPROVED:
            raise EvidenceValidationError(f"license is not approved: {record.evidence_id}")
        previous = seen.get(record.evidence_id)
        if previous is not None and previous != record.content_hash:
            raise EvidenceValidationError(f"conflicting duplicate evidence id: {record.evidence_id}")
        if previous is not None:
            continue
        seen[record.evidence_id] = record.content_hash
        if record.available_at <= cutoff:
            accepted.append(record)
    accepted.sort(key=lambda r: (r.available_at, r.source_type.value, r.evidence_id))
    manifest = {
        "issuer_id": issuer,
        "as_of": cutoff.isoformat(),
        "evidence": [{"evidence_id": r.evidence_id, "content_hash": r.content_hash} for r in accepted],
    }
    manifest_hash = digest_json(manifest)
    return EvidenceSnapshot(
        snapshot_id="snap_" + manifest_hash[:24], issuer_id=issuer, as_of=cutoff,
        created_at=created, records=tuple(accepted), manifest_hash=manifest_hash,
    )


@dataclass(frozen=True, slots=True)
class FactionResearch:
    faction_id: str
    stance: Stance
    confidence: float
    thesis: str
    evidence_refs: tuple[str, ...]
    counter_evidence_refs: tuple[str, ...]
    entry_triggers: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    target_weight: float
    max_weight: float
    uncertainties: tuple[str, ...]
    missing_data: tuple[str, ...]
    model_version: str
    prompt_version: str

    def __post_init__(self) -> None:
        if self.faction_id not in FACTION_IDS:
            raise ResearchContractError(f"unknown faction_id: {self.faction_id}")
        object.__setattr__(self, "stance", Stance(self.stance))
        if not 0 <= self.confidence <= 1:
            raise ResearchContractError("confidence must be between 0 and 1")
        if not 0 <= self.target_weight <= self.max_weight <= 1:
            raise ResearchContractError("weights must satisfy 0 <= target_weight <= max_weight <= 1")
        for name in ("thesis", "model_version", "prompt_version"):
            _nonempty(getattr(self, name), name)
        for name in ("evidence_refs", "counter_evidence_refs", "entry_triggers", "invalidation_conditions", "uncertainties", "missing_data"):
            values = tuple(getattr(self, name))
            if any(not isinstance(x, str) or not x.strip() for x in values):
                raise ResearchContractError(f"{name} must contain non-empty strings")
            if name in {"evidence_refs", "counter_evidence_refs"} and len(values) != len(set(values)):
                raise ResearchContractError(f"{name} must not contain duplicates")
            object.__setattr__(self, name, values)

    def validate_against(self, snapshot: EvidenceSnapshot) -> None:
        if not snapshot.verify():
            raise ResearchContractError("evidence snapshot failed integrity verification")
        allowed = {r.evidence_id for r in snapshot.records}
        unknown = (set(self.evidence_refs) | set(self.counter_evidence_refs)) - allowed
        if unknown:
            raise ResearchContractError(f"research references evidence outside the shared snapshot: {sorted(unknown)}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "faction_id": self.faction_id, "stance": self.stance.value, "confidence": self.confidence,
            "thesis": self.thesis, "evidence_refs": list(self.evidence_refs),
            "counter_evidence_refs": list(self.counter_evidence_refs),
            "entry_triggers": list(self.entry_triggers), "invalidation_conditions": list(self.invalidation_conditions),
            "target_weight": self.target_weight, "max_weight": self.max_weight,
            "uncertainties": list(self.uncertainties), "missing_data": list(self.missing_data),
            "model_version": self.model_version, "prompt_version": self.prompt_version,
        }


@dataclass(frozen=True, slots=True)
class LedgerEvent:
    sequence: int
    event_type: str
    actor: str
    occurred_at: datetime
    snapshot_id: str
    payload: Mapping[str, Any]
    payload_hash: str
    previous_hash: str
    event_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence, "event_type": self.event_type, "actor": self.actor,
            "occurred_at": self.occurred_at.isoformat(), "snapshot_id": self.snapshot_id,
            "payload": _thaw_json(self.payload), "payload_hash": self.payload_hash,
            "previous_hash": self.previous_hash, "event_hash": self.event_hash,
        }


class AppendOnlyLedger:
    """In-memory hash-chained ledger; persistence and signatures are later adapters."""

    def __init__(self) -> None:
        self._events: list[LedgerEvent] = []

    @property
    def events(self) -> tuple[LedgerEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        *,
        event_type: str,
        actor: str,
        occurred_at: datetime,
        snapshot_id: str,
        payload: Mapping[str, Any],
    ) -> LedgerEvent:
        timestamp = as_utc(occurred_at, "occurred_at")
        if self._events and timestamp < self._events[-1].occurred_at:
            raise GatewayError("ledger timestamps must be monotonic")
        frozen_payload = _freeze_json(payload)
        if not isinstance(frozen_payload, Mapping):
            raise GatewayError("ledger payload must be a JSON object")
        payload_hash = digest_json(_thaw_json(frozen_payload))
        sequence = len(self._events) + 1
        previous_hash = self._events[-1].event_hash if self._events else GENESIS_HASH
        body = {
            "sequence": sequence, "event_type": _nonempty(event_type, "event_type"),
            "actor": _nonempty(actor, "actor"), "occurred_at": timestamp.isoformat(),
            "snapshot_id": _nonempty(snapshot_id, "snapshot_id"),
            "payload_hash": payload_hash, "previous_hash": previous_hash,
        }
        event = LedgerEvent(
            sequence=sequence, event_type=body["event_type"], actor=body["actor"],
            occurred_at=timestamp, snapshot_id=body["snapshot_id"], payload=frozen_payload,
            payload_hash=payload_hash, previous_hash=previous_hash, event_hash=digest_json(body),
        )
        self._events.append(event)
        return event

    def verify(self) -> bool:
        previous_hash = GENESIS_HASH
        previous_time: datetime | None = None
        for expected_sequence, event in enumerate(self._events, start=1):
            if event.sequence != expected_sequence or event.previous_hash != previous_hash:
                return False
            if previous_time is not None and event.occurred_at < previous_time:
                return False
            payload_hash = digest_json(_thaw_json(event.payload))
            if payload_hash != event.payload_hash:
                return False
            body = {
                "sequence": event.sequence, "event_type": event.event_type, "actor": event.actor,
                "occurred_at": event.occurred_at.isoformat(), "snapshot_id": event.snapshot_id,
                "payload_hash": event.payload_hash, "previous_hash": event.previous_hash,
            }
            if digest_json(body) != event.event_hash:
                return False
            previous_hash, previous_time = event.event_hash, event.occurred_at
        return True
