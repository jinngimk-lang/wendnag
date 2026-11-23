"""Deterministic research triage; never a substitute for customer validation."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

WEIGHTS = {"business_value": 30, "buyer_urgency": 20, "product_fit": 20,
           "data_access": 15, "poc_feasibility": 15}
MANDATORY = ("id", "title", "stage", "hard_gate", *WEIGHTS)


def score(row: dict[str, str]) -> tuple[int, str]:
    """Return integer weighted score and non-misleading research status."""
    missing = [key for key in MANDATORY if key not in row]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    values = {}
    for key in WEIGHTS:
        try:
            value = int(row[key])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{row['id']}: {key} must be an integer 1..5") from exc
        if not 1 <= value <= 5:
            raise ValueError(f"{row['id']}: {key} outside 1..5")
        values[key] = value
    total = round(sum(values[k] * w / 5 for k, w in WEIGHTS.items()))
    gate = row["hard_gate"].strip().lower()
    if gate not in ("pass", "unknown", "fail"):
        raise ValueError(f"{row['id']}: invalid hard_gate")
    if gate == "fail":
        state = "REJECT"
    elif gate == "unknown":
        state = "VERIFY_GATES"
    elif total >= 80:
        state = "PRIORITY_INTERVIEW"
    elif total >= 65:
        state = "FURTHER_DILIGENCE"
    else:
        state = "DEFER"
    return total, state


def analyze(path: Path) -> list[dict[str, str | int]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("empty CSV")
        output = []
        seen = set()
        for row in reader:
            if row.get("id") in seen:
                raise ValueError(f"duplicate id: {row['id']}")
            seen.add(row.get("id"))
            total, state = score(row)
            output.append({"id": row["id"], "title": row["title"],
                           "score": total, "decision": state,
                           "stage": row["stage"]})
    return sorted(output, key=lambda item: (-int(item["score"]), str(item["id"])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    print("id,score,decision,stage,title")
    for item in analyze(args.csv_path):
        print(",".join(str(item[key]) for key in ("id", "score", "decision", "stage", "title")))
