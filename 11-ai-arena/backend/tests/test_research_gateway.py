from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from backend.research_gateway import (
    AppendOnlyLedger, EvidenceRecord, EvidenceValidationError, FactionResearch,
    GatewayError, Issuer, LicenseStatus, ResearchContractError, SourceType,
    Stance, freeze_evidence_pack, resolve_issuer,
)

UTC = timezone.utc
T0 = datetime(2026, 1, 2, 9, 30, tzinfo=UTC)


def issuer(issuer_id="issuer-acme", ticker="ACME", exchange="NASDAQ", name="Acme Robotics Inc."):
    return Issuer(issuer_id=issuer_id, legal_name=name, ticker=ticker, exchange=exchange,
                  currency="USD", cik="1234567", aliases=("ACME ROBOTICS",))


def evidence(evidence_id="ev-001", *, issuer_id="issuer-acme", available_offset=0,
             license_status=LicenseStatus.APPROVED, payload=None):
    published = T0 + timedelta(minutes=available_offset)
    available = published + timedelta(minutes=1)
    retrieved = available + timedelta(minutes=2)
    return EvidenceRecord.create(
        evidence_id=evidence_id, issuer_id=issuer_id, source_type=SourceType.FILING,
        title="Quarterly filing", source_url=f"https://example.test/{evidence_id}",
        published_at=published, available_at=available, retrieved_at=retrieved,
        provider="sec-fixture", license_id="public-source-terms-reviewed-v1",
        license_status=license_status, payload=payload or {"revenue": 120, "unit": "USD_m"},
        source_version="accession-fixture-001",
    )


class IssuerResolutionTests(unittest.TestCase):
    def test_exact_ticker_and_exchange_qualified_symbol(self):
        acme = issuer()
        self.assertEqual(resolve_issuer("ACME", [acme]).issuer, acme)
        self.assertEqual(resolve_issuer("NASDAQ:ACME", [acme]).issuer, acme)
        self.assertEqual(resolve_issuer("0001234567", [acme]).status, "resolved")

    def test_ambiguous_ticker_is_not_silently_resolved(self):
        candidates = [issuer(), issuer("issuer-acme-ca", "ACME", "TSXV", "Acme Robotics Canada")]
        result = resolve_issuer("ACME", candidates)
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNone(result.issuer)
        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(resolve_issuer("NASDAQ:ACME", candidates).issuer, candidates[0])

    def test_unknown_symbol_returns_not_found(self):
        self.assertEqual(resolve_issuer("NO-SUCH-ISSUER", [issuer()]).status, "not_found")


class EvidenceSnapshotTests(unittest.TestCase):
    def test_freeze_excludes_not_yet_available_records_and_is_order_independent(self):
        old = evidence("ev-old", available_offset=-60)
        future = evidence("ev-future", available_offset=60)
        cutoff = T0 + timedelta(minutes=10)
        created = T0 + timedelta(hours=2)
        first = freeze_evidence_pack("issuer-acme", cutoff, [old, future], created_at=created)
        second = freeze_evidence_pack("issuer-acme", cutoff, [future, old], created_at=created)
        self.assertEqual([x.evidence_id for x in first.records], ["ev-old"])
        self.assertEqual(first.snapshot_id, second.snapshot_id)
        self.assertTrue(first.verify())

    def test_foreign_issuer_and_unapproved_license_fail_closed(self):
        with self.assertRaises(EvidenceValidationError):
            freeze_evidence_pack("issuer-acme", T0 + timedelta(hours=1),
                                 [evidence(issuer_id="issuer-other")], created_at=T0 + timedelta(hours=2))
        restricted = evidence("ev-restricted", license_status=LicenseStatus.REVIEW_REQUIRED)
        with self.assertRaises(EvidenceValidationError):
            freeze_evidence_pack("issuer-acme", T0 + timedelta(hours=1),
                                 [restricted], created_at=T0 + timedelta(hours=2))

    def test_future_retrieval_and_naive_timestamps_are_rejected(self):
        with self.assertRaises(EvidenceValidationError):
            EvidenceRecord.create(
                evidence_id="bad", issuer_id="issuer-acme", source_type=SourceType.NEWS,
                title="Bad chronology", source_url="https://example.test/bad",
                published_at=T0, available_at=T0 + timedelta(minutes=2),
                retrieved_at=T0 + timedelta(minutes=1), provider="fixture", license_id="reviewed",
                license_status=LicenseStatus.APPROVED, payload={},
            )
        with self.assertRaises(GatewayError):
            EvidenceRecord.create(
                evidence_id="naive", issuer_id="issuer-acme", source_type=SourceType.NEWS,
                title="Naive timestamp", source_url="https://example.test/naive",
                published_at=datetime(2026, 1, 2), available_at=T0, retrieved_at=T0,
                provider="fixture", license_id="reviewed", license_status=LicenseStatus.APPROVED,
                payload={},
            )

    def test_conflicting_duplicate_ids_are_rejected(self):
        a = evidence("ev-dup", payload={"value": 1})
        b = evidence("ev-dup", payload={"value": 2})
        with self.assertRaises(EvidenceValidationError):
            freeze_evidence_pack("issuer-acme", T0 + timedelta(hours=1), [a, b],
                                 created_at=T0 + timedelta(hours=2))

    def test_nested_payload_is_deeply_immutable_and_snapshot_tampering_is_detected(self):
        nested = evidence("ev-nested", payload={"financials": {"revenue": [100, 120]}})
        with self.assertRaises(TypeError):
            nested.payload["financials"]["new"] = 1
        with self.assertRaises(AttributeError):
            nested.payload["financials"]["revenue"].append(140)
        snapshot = freeze_evidence_pack("issuer-acme", T0 + timedelta(hours=1),
                                        [nested], created_at=T0 + timedelta(hours=2))
        corrupted = replace(snapshot, manifest_hash="0" * 64)
        self.assertFalse(corrupted.verify())


class ResearchContractTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = freeze_evidence_pack("issuer-acme", T0 + timedelta(hours=1),
                                            [evidence()], created_at=T0 + timedelta(hours=2))

    def test_research_requires_evidence_from_the_shared_snapshot(self):
        report = FactionResearch(
            faction_id="value", stance=Stance.BULLISH, confidence=.72,
            thesis="Cash-flow quality is improving against a conservative valuation.",
            evidence_refs=("ev-001",), counter_evidence_refs=(),
            entry_triggers=("Margin trend remains positive",),
            invalidation_conditions=("Cash conversion deteriorates",),
            target_weight=.25, max_weight=.35, uncertainties=("One quarter is not a trend",),
            missing_data=("No peer-group valuation set",), model_version="rules-v0.1",
            prompt_version="research-contract-v0.1",
        )
        report.validate_against(self.snapshot)
        self.assertEqual(report.to_dict()["evidence_refs"], ["ev-001"])

    def test_unknown_evidence_and_weight_over_cap_are_rejected(self):
        report = FactionResearch(
            faction_id="growth", stance=Stance.NEUTRAL, confidence=.5, thesis="Wait for confirmation.",
            evidence_refs=("future-or-foreign-evidence",), counter_evidence_refs=(),
            entry_triggers=(), invalidation_conditions=(), target_weight=.4, max_weight=.4,
            uncertainties=(), missing_data=(), model_version="rules-v0.1", prompt_version="p-v0.1",
        )
        with self.assertRaises(ResearchContractError):
            report.validate_against(self.snapshot)
        with self.assertRaises(ResearchContractError):
            FactionResearch(
                faction_id="growth", stance=Stance.NEUTRAL, confidence=.5, thesis="Wait.",
                evidence_refs=(), counter_evidence_refs=(), entry_triggers=(), invalidation_conditions=(),
                target_weight=.5, max_weight=.4, uncertainties=(), missing_data=(),
                model_version="rules-v0.1", prompt_version="p-v0.1",
            )


class AppendOnlyLedgerTests(unittest.TestCase):
    def test_hash_chain_verifies_and_events_are_read_only(self):
        ledger = AppendOnlyLedger()
        first = ledger.append(event_type="snapshot_frozen", actor="gateway", occurred_at=T0,
                              snapshot_id="snap_demo", payload={"evidence_count": 1})
        second = ledger.append(event_type="research_completed", actor="value", occurred_at=T0 + timedelta(minutes=1),
                               snapshot_id="snap_demo", payload={"evidence_refs": ["ev-001"]})
        self.assertEqual(first.previous_hash, "GENESIS")
        self.assertEqual(second.previous_hash, first.event_hash)
        self.assertTrue(ledger.verify())
        with self.assertRaises(TypeError):
            first.payload["evidence_count"] = 9
        self.assertEqual(len(ledger.events), 2)

    def test_tampering_breaks_chain_and_time_cannot_move_backwards(self):
        ledger = AppendOnlyLedger()
        event = ledger.append(event_type="snapshot_frozen", actor="gateway", occurred_at=T0,
                              snapshot_id="snap_demo", payload={"evidence_count": 1})
        tampered = replace(event, event_hash="0" * 64)
        ledger._events[0] = tampered  # simulate storage corruption, not a supported mutation API
        self.assertFalse(ledger.verify())
        with self.assertRaises(GatewayError):
            AppendOnlyLedger().append(event_type="x", actor="y", occurred_at=datetime(2026, 1, 2),
                                      snapshot_id="snap", payload={})
        fresh = AppendOnlyLedger()
        fresh.append(event_type="one", actor="system", occurred_at=T0 + timedelta(minutes=2),
                     snapshot_id="snap", payload={})
        with self.assertRaises(GatewayError):
            fresh.append(event_type="two", actor="system", occurred_at=T0,
                         snapshot_id="snap", payload={})


if __name__ == "__main__":
    unittest.main(verbosity=2)
