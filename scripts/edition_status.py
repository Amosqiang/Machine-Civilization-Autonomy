#!/usr/bin/env python3
"""Report edition registry state and host-independence threshold status."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from new_edition import REGISTRY_FIELDS, load_registry
from paths import EDITIONS, edition_dir, editions_registry_csv, evidence_csv, threshold_status_md
from validate_data import ValidationError


STATUS_RE = re.compile(r"^\| status \| `([^`]+)` \|", re.MULTILINE)
AS_OF_RE = re.compile(r"^\| as_of \| ([^|]+) \|", re.MULTILINE)


def read_threshold(path: Path) -> dict[str, str]:
    if not path.exists():
        raise ValidationError(f"missing threshold status file: {path}")
    text = path.read_text(encoding="utf-8")
    status_match = STATUS_RE.search(text)
    as_of_match = AS_OF_RE.search(text)
    if status_match is None:
        raise ValidationError(f"{path}: could not parse status field")
    status = status_match.group(1).strip()
    if status not in {"not_met", "met", "unknown"}:
        raise ValidationError(f"{path}: invalid status {status!r}")
    return {
        "status": status,
        "as_of": as_of_match.group(1).strip() if as_of_match else "",
        "path": str(path),
    }


def filesystem_years() -> list[int]:
    if not EDITIONS.is_dir():
        return []
    years = []
    for child in EDITIONS.iterdir():
        if child.is_dir() and child.name.isdigit() and len(child.name) == 4:
            years.append(int(child.name))
    return sorted(years)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-threshold-not-met", action="store_true", help="exit 1 if threshold is marked met (sanity for pre-threshold workflows)")
    args = parser.parse_args(argv)
    try:
        rows = load_registry(editions_registry_csv())
        threshold = read_threshold(threshold_status_md())
        disk_years = filesystem_years()
        registry_years = sorted(int(row["year"]) for row in rows)
    except (OSError, ValidationError) as error:
        print(f"edition_status failed: {error}", file=sys.stderr)
        return 1

    print("Editions (registry):")
    if not rows:
        print("  (none)")
    for row in rows:
        year = int(row["year"])
        evidence = evidence_csv(year)
        evidence_state = "missing"
        if evidence.exists():
            # header-only files still count as present scaffolds
            with evidence.open(encoding="utf-8-sig") as stream:
                line_count = sum(1 for _ in stream)
            evidence_state = "header-only" if line_count <= 1 else f"{line_count - 1} rows"
        on_disk = "yes" if edition_dir(year).is_dir() else "NO"
        print(
            f"  {year}  status={row['status']:<10} as_of={row['as_of_date'] or '-':<10} "
            f"tag={row['git_tag'] or '-':<16} disk={on_disk} evidence={evidence_state}"
        )

    orphan = [year for year in disk_years if year not in registry_years]
    missing = [year for year in registry_years if year not in disk_years]
    if orphan:
        print(f"Orphan edition directories (on disk, not in registry): {orphan}")
    if missing:
        print(f"Registry years missing on disk: {missing}")

    print("Threshold:")
    print(f"  status={threshold['status']}  as_of={threshold['as_of'] or '-'}  file={threshold['path']}")
    if args.require_threshold_not_met and threshold["status"] == "met":
        print("Threshold unexpectedly marked met.", file=sys.stderr)
        return 1
    if orphan or missing:
        return 1
    # Validate registry field contract stayed intact for CI callers.
    if rows and set(rows[0]) != set(REGISTRY_FIELDS):
        print("Registry field contract drift.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
