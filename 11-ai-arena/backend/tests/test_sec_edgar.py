from datetime import datetime, timezone
import unittest

from backend.adapters.sec_edgar import (
    SECAdapterError, issuer_candidates_from_submissions, parse_companyfacts,
)
from backend.research_gateway import LicenseStatus, freeze_evidence_pack, resolve_issuer

UTC = timezone.utc
ACCEPTED = "2026-01-02T10:30:00.000Z"
ACCESSION = "0000320193-26-000001"


def fixture():
    submissions = {
        "cik": 320193,
        "name": "Example Systems Inc.",
        "tickers": ["EXM", "EXM"],
        "exchanges": ["NASDAQ", "NYSE"],
        "filings": {"recent": {
            "accessionNumber": [ACCESSION],
            "acceptanceDateTime": [ACCEPTED],
            "form": ["10-Q"],
            "filingDate": ["2026-01-02"],
        }},
    }
    companyfacts = {
        "cik": 320193,
        "facts": {"us-gaap": {"Revenue": {
            "label": "Revenue",
            "description": "Revenue from contracts with customers",
            "units": {"USD": [
                {"accn": ACCESSION, "fy": 2026, "fp": "Q1", "form": "10-Q",
                 "filed": "2026-01-02", "end": "2025-12-31", "val": 123456},
                {"accn": "0000320193-26-000999", "fy": 2026, "fp": "Q2", "form": "10-Q",
                 "filed": "2026-04-02", "end": "2026-03-31", "val": 140000},
                {"accn": ACCESSION, "fy": 2026, "fp": "Q1", "form": "8-K",
                 "filed": "2026-01-02", "end": "2025-12-31", "val": 999},
                {"accn": ACCESSION, "fy": 2026, "fp": "Q1", "form": "10-Q",
                 "filed": "2026-01-02", "end": "bad-date", "val": 999},
            ]},
        }},
    }}
    return submissions, companyfacts


class SECIssuerTests(unittest.TestCase):
    def test_cik_and_exchange_candidates_preserve_share_class_ambiguity(self):
        submissions, _ = fixture()
        candidates = issuer_candidates_from_submissions(submissions)
        self.assertEqual(len(candidates), 2)
        self.assertEqual(candidates[0].cik, "0000320193")
        self.assertEqual(resolve_issuer("NASDAQ:EXM", candidates).status, "resolved")
        self.assertEqual(resolve_issuer("EXM", candidates).status, "ambiguous")

    def test_missing_ticker_uses_cik_only_as_an_explicit_fallback(self):
        submissions, _ = fixture()
        submissions["tickers"] = []
        submissions["exchanges"] = []
        candidates = issuer_candidates_from_submissions(submissions)
        self.assertEqual(candidates[0].ticker, "0000320193")
        self.assertEqual(candidates[0].exchange, "SEC")


class SECCompanyFactsTests(unittest.TestCase):
    def test_acceptance_timestamp_anchors_evidence_not_period_end_or_filing_date(self):
        submissions, companyfacts = fixture()
        retrieved = datetime(2026, 1, 2, 12, tzinfo=UTC)
        result = parse_companyfacts(submissions, companyfacts, retrieved_at=retrieved,
                                    license_status=LicenseStatus.APPROVED)
        self.assertEqual(len(result.records), 1)
        record = result.records[0]
        accepted = datetime(2026, 1, 2, 10, 30, tzinfo=UTC)
        self.assertEqual(record.published_at, accepted)
        self.assertEqual(record.available_at, accepted)
        self.assertEqual(record.source_version, ACCESSION)
        self.assertEqual(record.payload["period_end"], "2025-12-31")
        self.assertEqual(record.payload["filing_date"], "2026-01-02")
        self.assertIn("320193/000032019326000001", record.source_url)
        self.assertEqual(result.skipped_unmatched_accessions, 1)
        self.assertEqual(result.skipped_form_mismatches, 1)
        self.assertEqual(result.skipped_invalid_values, 1)

    def test_point_in_time_snapshot_excludes_before_acceptance_and_includes_after(self):
        submissions, companyfacts = fixture()
        retrieved = datetime(2026, 1, 2, 12, tzinfo=UTC)
        result = parse_companyfacts(submissions, companyfacts, retrieved_at=retrieved,
                                    license_status=LicenseStatus.APPROVED)
        before = freeze_evidence_pack("cik:0000320193", datetime(2026, 1, 2, 10, 29, tzinfo=UTC),
                                      result.records, created_at=retrieved)
        after = freeze_evidence_pack("cik:0000320193", datetime(2026, 1, 2, 10, 31, tzinfo=UTC),
                                     result.records, created_at=retrieved)
        self.assertEqual(len(before.records), 0)
        self.assertEqual(len(after.records), 1)
        self.assertTrue(after.verify())

    def test_license_review_is_required_by_default(self):
        submissions, companyfacts = fixture()
        retrieved = datetime(2026, 1, 2, 12, tzinfo=UTC)
        result = parse_companyfacts(submissions, companyfacts, retrieved_at=retrieved)
        self.assertEqual(result.records[0].license_status, LicenseStatus.REVIEW_REQUIRED)
        with self.assertRaises(ValueError):
            freeze_evidence_pack("cik:0000320193", datetime(2026, 1, 2, 11, tzinfo=UTC),
                                 result.records, created_at=retrieved)

    def test_mismatched_cik_and_missing_acceptance_time_fail_closed(self):
        submissions, companyfacts = fixture()
        companyfacts["cik"] = 999
        with self.assertRaises(SECAdapterError):
            parse_companyfacts(submissions, companyfacts,
                               retrieved_at=datetime(2026, 1, 2, 12, tzinfo=UTC))
        submissions, companyfacts = fixture()
        submissions["filings"]["recent"]["acceptanceDateTime"] = []
        result = parse_companyfacts(submissions, companyfacts,
                                    retrieved_at=datetime(2026, 1, 2, 12, tzinfo=UTC),
                                    license_status=LicenseStatus.APPROVED)
        self.assertEqual(len(result.records), 0)
        self.assertEqual(result.skipped_unmatched_accessions, 4)

    def test_retrieval_before_acceptance_is_rejected(self):
        submissions, companyfacts = fixture()
        with self.assertRaises(SECAdapterError):
            parse_companyfacts(submissions, companyfacts,
                               retrieved_at=datetime(2026, 1, 2, 10, tzinfo=UTC),
                               license_status=LicenseStatus.APPROVED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
