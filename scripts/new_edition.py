#!/usr/bin/env python3
"""Open a new MCAB annual edition directory without touching prior editions."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
import sys

from paths import (
    DEFAULT_YEAR,
    ROOT,
    analysis_dir,
    edition_dir,
    edition_manifest,
    editions_registry_csv,
    evidence_csv,
    evidence_schema_csv,
    reports_dir,
    research_dir,
)
from validate_data import EVIDENCE_FIELDS, ValidationError, read_table

REGISTRY_FIELDS = ("year", "status", "as_of_date", "git_tag", "opened_on", "notes")


def load_registry(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows = read_table(path, REGISTRY_FIELDS)
    errors: list[str] = []
    seen: set[str] = set()
    for number, row in enumerate(rows, 2):
        label = f"{path.name} row {number}"
        year = row["year"].strip()
        if not year.isdigit() or len(year) != 4:
            errors.append(f"{label}: year must be YYYY")
        if year in seen:
            errors.append(f"{label}: duplicate year {year}")
        seen.add(year)
        if row["status"] not in {"planned", "open", "frozen", "released", "superseded"}:
            errors.append(f"{label}: invalid status {row['status']!r}")
        if row["as_of_date"]:
            try:
                date.fromisoformat(row["as_of_date"])
            except ValueError:
                errors.append(f"{label}: as_of_date must be YYYY-MM-DD or blank")
    if errors:
        raise ValidationError("\n".join(errors))
    return rows


def write_registry(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=REGISTRY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def evidence_header() -> list[str]:
    schema = read_table(evidence_schema_csv(), ("field", "description"))
    fields = [row["field"] for row in schema]
    if fields != list(EVIDENCE_FIELDS):
        raise ValidationError("evidence_schema.csv fields must match the validator contract exactly")
    return fields


def write_empty_evidence(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=evidence_header())
        writer.writeheader()


def write_manifest(year: int, *, from_year: int | None, as_of: str, opened_on: str) -> None:
    prior = f"Bootstrapped from MCAB-{from_year}." if from_year is not None else "Initial edition scaffold."
    text = f"""# MCAB-{year} Edition Manifest

| Field | Value |
| --- | --- |
| Edition | MCAB-{year} |
| Status | open |
| Evidence cutoff (`as_of`) | {as_of or '(unset — set before freeze)'} |
| Opened on | {opened_on} |
| Formal evidence | `evidence.csv` |
| Literature research | `research/` |
| Generated analysis | `analysis/` |
| Reports | `reports/{year}/` |

## Continuity notes

- {prior}
- Do not overwrite prior editions. Correct forward; supersede with tags `mcab-{year}` / `mcab-{year}-rN`.
- Formal scores stay blank until evidence rows exist. Unknown must not become zero.
"""
    edition_manifest(year).write_text(text, encoding="utf-8")


def open_edition(year: int, *, from_year: int | None, as_of: str, notes: str) -> Path:
    if year < 2000 or year > 2100:
        raise ValidationError("year looks implausible for an MCAB edition")
    target = edition_dir(year)
    if target.exists():
        raise ValidationError(f"{target} already exists; refuse to clobber an edition")
    registry_path = editions_registry_csv()
    rows = load_registry(registry_path)
    if any(row["year"] == str(year) for row in rows):
        raise ValidationError(f"registry already lists {year}")
    if from_year is not None:
        source = edition_dir(from_year)
        if not source.is_dir():
            raise ValidationError(f"source edition missing: {source}")
        if not evidence_csv(from_year).exists():
            raise ValidationError(f"source evidence missing: {evidence_csv(from_year)}")

    opened_on = date.today().isoformat()
    write_empty_evidence(evidence_csv(year))
    research_dir(year).mkdir(parents=True, exist_ok=True)
    (research_dir(year) / ".gitkeep").write_text("", encoding="utf-8")
    analysis_dir(year).mkdir(parents=True, exist_ok=True)
    (analysis_dir(year) / ".gitkeep").write_text("", encoding="utf-8")
    reports_dir(year).mkdir(parents=True, exist_ok=True)
    (reports_dir(year) / ".gitkeep").write_text("", encoding="utf-8")
    write_manifest(year, from_year=from_year, as_of=as_of, opened_on=opened_on)
    rows.append(
        {
            "year": str(year),
            "status": "open",
            "as_of_date": as_of,
            "git_tag": "",
            "opened_on": opened_on,
            "notes": notes or (f"Opened from {from_year}" if from_year else "Opened empty edition"),
        }
    )
    rows.sort(key=lambda row: row["year"])
    write_registry(registry_path, rows)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, required=True, help="new edition year, e.g. 2027")
    parser.add_argument("--from-year", type=int, default=None, help="prior edition to reference in the manifest")
    parser.add_argument("--as-of", default="", help="optional initial as_of cutoff YYYY-MM-DD")
    parser.add_argument("--notes", default="", help="registry note")
    args = parser.parse_args(argv)
    try:
        if args.as_of:
            date.fromisoformat(args.as_of)
        if args.from_year is None and args.year != DEFAULT_YEAR:
            # Prefer chaining from the latest registered year when present.
            existing = load_registry(editions_registry_csv())
            if existing:
                args.from_year = max(int(row["year"]) for row in existing)
        target = open_edition(args.year, from_year=args.from_year, as_of=args.as_of, notes=args.notes)
    except (OSError, ValidationError, ValueError) as error:
        print(f"new_edition failed: {error}", file=sys.stderr)
        return 1
    print(f"Opened edition {args.year} -> {target.relative_to(ROOT)}")
    print(f"Registry -> {editions_registry_csv().relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
