#!/usr/bin/env python3
"""Build a prioritized frontier-evidence target queue from research gaps."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

from paths import (
    DEFAULT_YEAR,
    dependencies_csv,
    dimensions_csv,
    evidence_csv,
    research_dir,
    source_playbooks_csv,
    target_queue_csv,
    taxonomy_csv,
)
from validate_data import ValidationError, load_inputs, read_table

QUEUE_FIELDS = (
    "target_id", "priority", "year", "dimension_id", "domain_id", "domain",
    "subsystem_id", "subsystem", "metric_id", "metric", "criticality",
    "evidence_relation", "assessment_status", "formal_evidence_rows",
    "dependency_degree", "score", "search_focus", "playbook_hint",
    "status", "lock_reason", "notes",
)
METRIC_WEIGHT = {
    "M10": 50, "M5": 45, "M4": 40, "M9": 35, "M8": 30,
    "M6": 25, "M7": 20, "M3": 15, "M2": 10, "M1": 5,
}
RELATION_WEIGHT = {
    "no_direct_evidence": 40,
    "context_only": 28,
    "partial_metric": 14,
    "direct_metric": 0,
}
STATUS_WEIGHT = {
    "not_established_in_review": 12,
    "unknown": 10,
    "partial_related_evidence": 6,
    "demonstrated_limited": 2,
}


def load_research_records(year: int) -> list[dict]:
    root = research_dir(year)
    if not root.is_dir():
        raise ValidationError(f"missing research dir: {root}")
    records: list[dict] = []
    for path in sorted(root.glob("domains_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        chunk = payload.get("records")
        if not isinstance(chunk, list):
            raise ValidationError(f"{path}: expected records list")
        records.extend(chunk)
    if len(records) != 1000:
        raise ValidationError(f"expected 1000 research records, found {len(records)}")
    return records


def load_preserved_overrides(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    rows = read_table(path, QUEUE_FIELDS)
    preserved = {}
    for row in rows:
        if row["status"] in {"locked_deep_dive", "in_progress", "deferred"} or row["lock_reason"].strip():
            preserved[row["dimension_id"]] = {
                "status": row["status"],
                "lock_reason": row["lock_reason"],
                "notes": row["notes"],
            }
    return preserved


def formal_counts(year: int) -> dict[str, int]:
    path = evidence_csv(year)
    counts: dict[str, int] = {}
    if not path.exists():
        return counts
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        for row in reader:
            key = f"{row['subsystem_id']}-{row['metric_id']}"
            counts[key] = counts.get(key, 0) + 1
    return counts


def dependency_degrees() -> dict[str, int]:
    path = dependencies_csv()
    if not path.exists():
        return {}
    rows = read_table(
        path,
        (
            "dependency_id", "consumer_subsystem_id", "upstream_subsystem_id",
            "dependency_type", "critical", "verification_status", "evidence_refs",
            "substitutes", "notes",
        ),
    )
    degree: dict[str, int] = {}
    for row in rows:
        for key in (row["consumer_subsystem_id"], row["upstream_subsystem_id"]):
            degree[key] = degree.get(key, 0) + 1
    return degree


def playbook_hints() -> dict[str, str]:
    if not source_playbooks_csv().exists():
        return {}
    rows = read_table(
        source_playbooks_csv(),
        (
            "domain_id", "domain", "primary_venues", "secondary_venues",
            "avoid_as_sole_evidence", "example_queries", "notes",
        ),
    )
    return {row["domain_id"]: row["example_queries"] for row in rows}


def score_row(criticality: str, metric_id: str, relation: str, status: str, formal: int, degree: int) -> int:
    score = METRIC_WEIGHT.get(metric_id, 0)
    score += RELATION_WEIGHT.get(relation, 0)
    score += STATUS_WEIGHT.get(status, 0)
    score += 25 if criticality == "critical" else 8
    if formal == 0:
        score += 15
    score += min(degree, 8) * 2
    return score


def build_queue(year: int) -> list[dict[str, str]]:
    taxonomy, metrics = load_inputs()
    tax = {row["subsystem_id"]: row for row in taxonomy}
    metric_map = {row["metric_id"]: row for row in metrics}
    records = load_research_records(year)
    formal = formal_counts(year)
    degree = dependency_degrees()
    hints = playbook_hints()
    overrides = load_preserved_overrides(target_queue_csv())
    # optional dimension labels
    dim_labels = {}
    if dimensions_csv().exists():
        for row in read_table(
            dimensions_csv(),
            (
                "dimension_id", "domain_id", "domain", "subsystem_id", "subsystem",
                "metric_id", "metric", "test_question", "criticality", "score_0_5",
                "confidence_0_1", "evidence_date", "evidence_type", "source", "notes",
            ),
        ):
            dim_labels[row["dimension_id"]] = row

    built: list[dict[str, str]] = []
    for record in records:
        dimension_id = record["dimension_id"]
        subsystem_id, metric_id = dimension_id.rsplit("-", 1)
        subsystem = tax[subsystem_id]
        metric = metric_map[metric_id]
        relation = record.get("evidence_relation", "")
        assessment = record.get("assessment_status", "")
        formal_n = formal.get(dimension_id, 0)
        dep = degree.get(subsystem_id, 0)
        total = score_row(subsystem["criticality"], metric_id, relation, assessment, formal_n, dep)
        focus = record.get("validation_needed") or record.get("gap") or ""
        row = {
            "target_id": f"{year}-{dimension_id}",
            "priority": "",  # filled after sort
            "year": str(year),
            "dimension_id": dimension_id,
            "domain_id": subsystem["domain_id"],
            "domain": subsystem["domain"],
            "subsystem_id": subsystem_id,
            "subsystem": subsystem["subsystem"],
            "metric_id": metric_id,
            "metric": metric["metric"],
            "criticality": subsystem["criticality"],
            "evidence_relation": relation,
            "assessment_status": assessment,
            "formal_evidence_rows": str(formal_n),
            "dependency_degree": str(dep),
            "score": str(total),
            "search_focus": " ".join(focus.split()),
            "playbook_hint": hints.get(subsystem["domain_id"], ""),
            "status": "queued",
            "lock_reason": "",
            "notes": "",
        }
        if dimension_id in overrides:
            row.update(overrides[dimension_id])
        if dimension_id in dim_labels and not row["notes"]:
            # keep notes empty; label map reserved for future worksheet sync
            pass
        built.append(row)

    built.sort(key=lambda row: (-int(row["score"]), row["dimension_id"]))
    for index, row in enumerate(built, 1):
        row["priority"] = str(index)
    return built


def write_queue(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=QUEUE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument("--limit", type=int, default=0, help="if >0, print only top N to stdout summary")
    args = parser.parse_args(argv)
    try:
        rows = build_queue(args.year)
        write_queue(rows, target_queue_csv())
    except (OSError, ValidationError, KeyError, json.JSONDecodeError) as error:
        print(f"build_target_queue failed: {error}", file=sys.stderr)
        return 1
    limit = args.limit or 20
    print(f"Wrote {len(rows)} targets -> {target_queue_csv()}")
    print(f"Top {limit}:")
    for row in rows[:limit]:
        print(
            f"  P{row['priority']:>4} score={row['score']:>3} {row['dimension_id']:<8} "
            f"{row['criticality']:<8} {row['evidence_relation']:<22} {row['subsystem']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
