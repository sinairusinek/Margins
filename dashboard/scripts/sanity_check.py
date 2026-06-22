"""Verify dashboard headline numbers against the methods document.

If the methods doc and the extracted summary diverge, fail loudly. This is the
guardrail that prevents the dashboard and the prose from silently drifting
when the source TSV changes.

Headline numbers to lock in (from bibliographic_units_and_marc.md, section 9):
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "dashboard" / "data" / "bhb_pre1800_summary.json"

EXPECTED = {
    "total_in_scope": 10787,
    "by_century": {15: 126, 16: 1772, 17: 2216, 18: 6673},
    "distinct_places_normalized": 205,
    "distinct_works_clustered": 3572,
    "records_clustered": 4731,
    "records_unclustered": 6056,
    "distinct_authors_100": 1986,
    "haskama_total": 2259,
    "chronogram_total": 5351,
}


def main() -> int:
    if not SUMMARY.exists():
        sys.exit(f"missing {SUMMARY} — run extract_in_scope.py first")

    s = json.loads(SUMMARY.read_text(encoding="utf-8"))
    failures = []

    for key, expected in EXPECTED.items():
        actual = s.get(key)
        if key == "by_century":
            actual = {int(k): v for k, v in actual.items()}
        if actual != expected:
            failures.append(f"  {key}: expected {expected}, got {actual}")

    if failures:
        print("Sanity check FAILED — methods doc and summary have diverged:")
        for f in failures:
            print(f)
        return 1

    print(f"Sanity check OK. {len(EXPECTED)} headline numbers match methods §9.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
