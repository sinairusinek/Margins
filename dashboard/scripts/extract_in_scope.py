"""Extract Margins in-scope (008-Year <= 1800) subset of mbimarc-bhb.tsv.

Reads ../../mbimarc-bhb.tsv, emits:
  dashboard/_data/bhb_pre1800.json      slim record list
  dashboard/_data/bhb_pre1800_summary.json   precomputed aggregates
  dashboard/_data/bhb_pre1800_places.geojson minimal places layer

Headline numbers also written to STDOUT so CI can diff them against the
methods document (bibliographic_units_and_marc.md, section 9).
"""

from __future__ import annotations

import csv
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TSV = ROOT / "mbimarc-bhb.tsv"
OUT_DATA = ROOT / "dashboard" / "_data"
OUT_DATA.mkdir(parents=True, exist_ok=True)

# Column positions follow mbimarc-bhb.tsv header order (1-indexed in methods doc).
COLS = {
    "id": 0, "url": 1, "title_a": 2, "title_b": 3, "uniform_130": 4,
    "varying_246": 5, "uniform_730": 6, "author_100": 7, "added_700": 8,
    "relator_700": 9, "uncontrolled_720": 10, "corporate_110": 11,
    "added_corp_710": 12, "edition_250": 13, "date_260c_heb": 14,
    "date_260c_greg": 15, "chronogram_912": 16, "publisher_260b": 17,
    "publisher_922": 18, "place_260a": 19, "manufacturer_260f": 20,
    "printer_923": 21, "haskama_915": 22, "physical_300": 23,
    "series_490": 24, "note_500": 25, "originals_535": 26,
    "location_921": 27, "location_951": 28, "contents": 29,
    "language_546": 30, "genre_690": 31, "type_901": 32,
    "fixed_008": 33, "year": 34, "reproduction_533": 35, "005": 36,
    "yael": 37, "language_041": 38, "leader": 39, "mbi_900": 40,
    "uniform_240": 41, "added_740": 42,
}

# Regex grammar from methods doc section 7 (Bowers / Gaskell signals in 500).
SIGNAL_PATTERNS = {
    "state": r"בחלק.*עותק",
    "variant_copies": r"יש טפסים",
    "issue": r"שער חדש|שער אחר|שער מתוקן",
    "cancel": r"דף מבוטל|הוחלף.*דף|דף.*הוחלף",
    "impression": r"נדפס שנית|נדפס מחדש",
    "replacement": r"הוחלף",
    "variant_text": r"נוסח אחר",
    "forged": r"מזוייף|מזויף",
    "omission": r"הושמט|נשמט",
}
SIGNAL_RE = {k: re.compile(v) for k, v in SIGNAL_PATTERNS.items()}


def normalize_place(raw: str) -> str:
    """Normalize 951 'Heb|Lat' bilingual place strings to a canonical order."""
    if not raw or "|" not in raw:
        return raw
    parts = raw.split("|", 1)
    return "|".join(sorted(parts))


def parse_year(s: str) -> int | None:
    if s and len(s) >= 4 and s[:4].isdigit():
        return int(s[:4])
    return None


def main() -> None:
    if not TSV.exists():
        sys.exit(f"missing {TSV}")

    records: list[dict] = []
    decade_hist: Counter[int] = Counter()
    place_hist: Counter[str] = Counter()
    work_hist: Counter[str] = Counter()
    author_hist: Counter[str] = Counter()
    type_hist: Counter[str] = Counter()
    genre_hist: Counter[str] = Counter()
    language_hist: Counter[str] = Counter()
    signal_hist: Counter[str] = Counter()
    haskama_by_century: Counter[int] = Counter()
    chronogram_by_century: Counter[int] = Counter()
    haskama_by_decade: Counter[int] = Counter()
    chronogram_by_decade: Counter[int] = Counter()
    records_by_century: Counter[int] = Counter()
    haskama_by_decade_place: dict[tuple[int, str], int] = defaultdict(int)
    chronogram_by_decade_place: dict[tuple[int, str], int] = defaultdict(int)
    place_by_century: dict[tuple[str, int], int] = defaultdict(int)
    decade_by_place: dict[tuple[int, str], int] = defaultdict(int)

    with TSV.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        header = next(reader)
        for row in reader:
            if len(row) < len(COLS):
                row = row + [""] * (len(COLS) - len(row))
            year = parse_year(row[COLS["year"]])
            if year is None or year > 1800:
                continue

            place_raw = row[COLS["location_951"]]
            place_norm = normalize_place(place_raw)
            note = row[COLS["note_500"]] or ""
            signals = [name for name, regex in SIGNAL_RE.items() if regex.search(note)]

            rec = {
                "id": row[COLS["id"]],
                "url": row[COLS["url"]],
                "year": year,
                "decade": (year // 10) * 10,
                "century": (year - 1) // 100 + 1,
                "title_a": row[COLS["title_a"]],
                "title_b": row[COLS["title_b"]],
                "uniform_130": row[COLS["uniform_130"]],
                "author_100": row[COLS["author_100"]],
                "place": place_norm,
                "place_raw": place_raw,
                "publisher_260b": row[COLS["publisher_260b"]],
                "printer_923": row[COLS["printer_923"]],
                "edition_250": row[COLS["edition_250"]],
                "haskama_915": row[COLS["haskama_915"]],
                "chronogram_912": row[COLS["chronogram_912"]],
                "language_041": row[COLS["language_041"]],
                "type_901": row[COLS["type_901"]],
                "genre_690": row[COLS["genre_690"]],
                "note_500": note,
                "signals": signals,
            }
            records.append(rec)

            decade_hist[rec["decade"]] += 1
            records_by_century[rec["century"]] += 1
            if place_norm:
                place_hist[place_norm] += 1
                place_by_century[(place_norm, rec["century"])] += 1
                decade_by_place[(rec["decade"], place_norm)] += 1
            if rec["uniform_130"]:
                work_hist[rec["uniform_130"]] += 1
            if rec["author_100"]:
                author_hist[rec["author_100"]] += 1
            if rec["type_901"]:
                type_hist[rec["type_901"]] += 1
            if rec["genre_690"]:
                genre_hist[rec["genre_690"]] += 1
            if rec["language_041"]:
                # First token of the language string (first language code).
                lang = rec["language_041"].split("|")[0].strip()
                if lang:
                    language_hist[lang] += 1
            for s in signals:
                signal_hist[s] += 1
            if rec["haskama_915"]:
                haskama_by_century[rec["century"]] += 1
                haskama_by_decade[rec["decade"]] += 1
                if place_norm:
                    haskama_by_decade_place[(rec["decade"], place_norm)] += 1
            if rec["chronogram_912"]:
                chronogram_by_century[rec["century"]] += 1
                chronogram_by_decade[rec["decade"]] += 1
                if place_norm:
                    chronogram_by_decade_place[(rec["decade"], place_norm)] += 1

    # Records list, gzipped JSON (size).
    out_records = OUT_DATA / "bhb_pre1800.json.gz"
    with gzip.open(out_records, "wt", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False)

    top_places_set = {p for p, _ in place_hist.most_common(12)}
    summary = {
        "total_in_scope": len(records),
        "year_min": min(r["year"] for r in records),
        "year_max": max(r["year"] for r in records),
        "by_century": dict(sorted(records_by_century.items())),
        "by_decade": dict(sorted(decade_hist.items())),
        "distinct_places_normalized": len(place_hist),
        "distinct_works_clustered": len(work_hist),
        "records_clustered": sum(1 for r in records if r["uniform_130"]),
        "records_unclustered": sum(1 for r in records if not r["uniform_130"]),
        "distinct_authors_100": len(author_hist),
        "haskama_total": sum(haskama_by_century.values()),
        "haskama_by_century": dict(sorted(haskama_by_century.items())),
        "haskama_by_decade": dict(sorted(haskama_by_decade.items())),
        "chronogram_total": sum(chronogram_by_century.values()),
        "chronogram_by_century": dict(sorted(chronogram_by_century.items())),
        "chronogram_by_decade": dict(sorted(chronogram_by_decade.items())),
        "signals_by_kind": dict(signal_hist),
        "records_any_signal": sum(1 for r in records if r["signals"]),
        "top_places": place_hist.most_common(20),
        "top_works": work_hist.most_common(20),
        "top_authors": author_hist.most_common(20),
        "top_types": type_hist.most_common(15),
        "top_genres": genre_hist.most_common(15),
        "top_languages": language_hist.most_common(15),
        "haskama_decade_place": [
            {"decade": d, "place": p, "n": n}
            for (d, p), n in haskama_by_decade_place.items()
        ],
        "chronogram_decade_place": [
            {"decade": d, "place": p, "n": n}
            for (d, p), n in chronogram_by_decade_place.items()
        ],
        "decade_place_top12": [
            {"decade": d, "place": p, "n": n}
            for (d, p), n in decade_by_place.items()
            if p in top_places_set
        ],
    }
    (OUT_DATA / "bhb_pre1800_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"wrote {out_records} ({out_records.stat().st_size/1e6:.1f} MB)")
    print(f"wrote {OUT_DATA / 'bhb_pre1800_summary.json'}")
    print()
    print("=== HEADLINE NUMBERS (sanity check against methods §9) ===")
    print(f"total_in_scope: {summary['total_in_scope']}")
    print(f"by_century: {summary['by_century']}")
    print(f"distinct_places_normalized: {summary['distinct_places_normalized']}")
    print(f"distinct_works_clustered: {summary['distinct_works_clustered']}")
    print(f"records_clustered: {summary['records_clustered']}")
    print(f"distinct_authors_100: {summary['distinct_authors_100']}")
    print(f"haskama_total: {summary['haskama_total']}")
    print(f"chronogram_total: {summary['chronogram_total']}")
    print(f"records_any_signal: {summary['records_any_signal']}")
    print(f"top 3 places: {summary['top_places'][:3]}")


if __name__ == "__main__":
    main()
