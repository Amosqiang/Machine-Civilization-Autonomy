#!/usr/bin/env python3
"""Append one method-loop cycle record without rewriting prior cycles."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
import sys

from paths import cycle_log_csv, target_queue_csv
from validate_data import ValidationError, read_table

CYCLE_FIELDS = (
    "cycle_id", "year", "opened_on", "closed_on", "batch_size",
    "targets_attempted", "targets_verified", "targets_ingested",
    "queue_top_snapshot", "failures", "learning", "summary", "status",
)


def load_cycles(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_table(path, CYCLE_FIELDS)


def write_cycles(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CYCLE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def top_snapshot(limit: int) -> str:
    path = target_queue_csv()
    if not path.exists():
        return ""
    rows = read_table(
        path,
        (
            "target_id", "priority", "year", "dimension_id", "domain_id", "domain",
            "subsystem_id", "subsystem", "metric_id", "metric", "criticality",
            "evidence_relation", "assessment_status", "formal_evidence_rows",
            "dependency_degree", "score", "search_focus", "playbook_hint",
            "status", "lock_reason", "notes",
        ),
    )
    rows = sorted(rows, key=lambda row: int(row["priority"]))[:limit]
    return ",".join(row["dimension_id"] for row in rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True, help="cycle id, e.g. 2026-C01")
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--attempted", type=int, default=0)
    parser.add_argument("--verified", type=int, default=0)
    parser.add_argument("--ingested", type=int, default=0)
    parser.add_argument("--failures", default="", help="short failure notes")
    parser.add_argument("--learning", default="", help="what changes next cycle")
    parser.add_argument("--summary", required=True, help="one-line cycle summary")
    parser.add_argument("--status", default="closed", choices=("open", "closed"))
    parser.add_argument("--open-only", action="store_true", help="create an open cycle row without closing stats")
    args = parser.parse_args(argv)
    try:
        rows = load_cycles(cycle_log_csv())
        if any(row["cycle_id"] == args.cycle for row in rows):
            raise ValidationError(f"cycle_id already exists: {args.cycle}")
        today = date.today().isoformat()
        row = {
            "cycle_id": args.cycle,
            "year": str(args.year),
            "opened_on": today,
            "closed_on": "" if args.open_only or args.status == "open" else today,
            "batch_size": str(args.batch_size),
            "targets_attempted": str(args.attempted),
            "targets_verified": str(args.verified),
            "targets_ingested": str(args.ingested),
            "queue_top_snapshot": top_snapshot(args.batch_size),
            "failures": args.failures,
            "learning": args.learning,
            "summary": args.summary,
            "status": "open" if args.open_only else args.status,
        }
        rows.append(row)
        write_cycles(cycle_log_csv(), rows)
    except (OSError, ValidationError) as error:
        print(f"log_method_cycle failed: {error}", file=sys.stderr)
        return 1
    print(f"Logged {args.cycle} -> {cycle_log_csv()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
