#!/usr/bin/env python3
"""Validate method-loop artifacts: playbooks, target queue, cycle log."""

from __future__ import annotations

import argparse
import sys

from build_target_queue import QUEUE_FIELDS
from log_method_cycle import CYCLE_FIELDS
from paths import cycle_log_csv, source_playbooks_csv, target_queue_csv
from validate_data import ValidationError, read_table

PLAYBOOK_FIELDS = (
    "domain_id", "domain", "primary_venues", "secondary_venues",
    "avoid_as_sole_evidence", "example_queries", "notes",
)


def validate_playbooks() -> str:
    rows = read_table(source_playbooks_csv(), PLAYBOOK_FIELDS)
    if len(rows) != 10:
        raise ValidationError("source_playbooks.csv: expected 10 domain rows")
    ids = {row["domain_id"] for row in rows}
    if ids != {str(i) for i in range(1, 11)}:
        raise ValidationError("source_playbooks.csv: domain_id must be 1..10 exactly once")
    for number, row in enumerate(rows, 2):
        for field in ("primary_venues", "example_queries"):
            if not row[field].strip():
                raise ValidationError(f"source_playbooks.csv row {number}: {field} required")
    return f"{len(rows)} domain playbooks valid"


def validate_queue() -> str:
    path = target_queue_csv()
    if not path.exists():
        raise ValidationError(f"missing {path}; run scripts/build_target_queue.py")
    rows = read_table(path, QUEUE_FIELDS)
    if len(rows) != 1000:
        raise ValidationError(f"{path}: expected 1000 targets, found {len(rows)}")
    priorities = [int(row["priority"]) for row in rows]
    if sorted(priorities) != list(range(1, 1001)):
        raise ValidationError(f"{path}: priority must be a permutation of 1..1000")
    ids = [row["dimension_id"] for row in rows]
    if len(set(ids)) != 1000:
        raise ValidationError(f"{path}: dimension_id must be unique")
    return f"{len(rows)} queue rows valid"


def validate_cycles() -> str:
    path = cycle_log_csv()
    if not path.exists():
        return "cycle_log.csv absent (ok until first cycle is logged)"
    rows = read_table(path, CYCLE_FIELDS)
    seen = set()
    for number, row in enumerate(rows, 2):
        if not row["cycle_id"].strip():
            raise ValidationError(f"cycle_log.csv row {number}: cycle_id required")
        if row["cycle_id"] in seen:
            raise ValidationError(f"cycle_log.csv row {number}: duplicate cycle_id")
        seen.add(row["cycle_id"])
        if row["status"] not in {"open", "closed"}:
            raise ValidationError(f"cycle_log.csv row {number}: invalid status")
        if not row["summary"].strip():
            raise ValidationError(f"cycle_log.csv row {number}: summary required")
    return f"{len(rows)} cycle log rows valid"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        messages = [validate_playbooks(), validate_queue(), validate_cycles()]
    except (OSError, ValidationError) as error:
        print(f"Method validation failed:\n{error}", file=sys.stderr)
        return 1
    for message in messages:
        print(f"OK: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
