import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from score_opportunities import score, analyze

BASE = {"id":"T01", "title":"sample", "stage":"hypothesis", "hard_gate":"unknown",
        "business_value":"5", "buyer_urgency":"5", "product_fit":"5", "data_access":"5", "poc_feasibility":"5"}

class TestScore(unittest.TestCase):
    def test_upper_bound_and_unknown_gate(self):
        self.assertEqual(score(BASE), (100, "VERIFY_GATES"))

    def test_fail_overrides_high_score(self):
        self.assertEqual(score({**BASE, "hard_gate":"fail"}), (100, "REJECT"))

    def test_pass_meets_threshold(self):
        self.assertEqual(score({**BASE, "hard_gate":"pass"}), (100, "PRIORITY_INTERVIEW"))

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            score({**BASE, "data_access":"7"})

    def test_csv_sorted(self):
        path = Path(__file__).resolve().parents[1] / "data" / "opportunities.csv"
        rows = analyze(path)
        self.assertTrue(len(rows) >= 5)
        self.assertEqual(len(rows), len({r['id'] for r in rows}))
        self.assertTrue(all(r['decision'] == "VERIFY_GATES" for r in rows))

if __name__ == "__main__":
    unittest.main()
