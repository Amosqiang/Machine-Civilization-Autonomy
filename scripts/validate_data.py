#!/usr/bin/env python3
"""Validate MCAB ontology, dimensions and optional scenario evidence (stdlib only)."""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_FIELDS = (
    "domain_id", "domain", "subsystem_id", "subsystem", "definition", "criticality"
)
METRIC_FIELDS = ("metric_id", "metric", "definition")
DIMENSION_FIELDS = (
    "dimension_id", "domain_id", "domain", "subsystem_id", "subsystem", "metric_id",
    "metric", "test_question", "criticality", "score_0_5", "confidence_0_1",
    "evidence_date", "evidence_type", "source", "notes",
)
EVIDENCE_FIELDS = (
    "record_id", "year", "as_of_date", "domain_id", "subsystem_id", "metric_id",
    "human_removal_scenario", "score_0_5", "evidence_level", "confidence",
    "observed_capability", "remaining_human_role", "failure_mode",
    "upstream_dependencies", "substitutes", "recovery_time", "stockpile_duration",
    "single_point_of_failure", "source_title", "source_url", "source_type",
    "source_date", "notes",
)
EVIDENCE_LEVELS = {f"E{i}" for i in range(6)}
SCENARIOS = {"HR100", "HR50", "HR10", "HR1", "HR0"}
SOURCE_TYPES = {"Paper", "benchmark", "field-data", "company-doc", "government", "other"}


class ValidationError(ValueError):
    """Invalid or unreadable MCAB CSV data."""


def read_table(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            header = reader.fieldnames
            if header is None or len(header) != len(set(header)) or set(header) != set(fields):
                raise ValidationError(f"{path}: expected columns {', '.join(fields)}")
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValidationError(f"{path}: line {reader.line_num}: wrong number of columns")
                rows.append(row)
            return rows
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ValidationError(f"{path}: {exc}") from exc


def require_values(row: dict[str, str], fields, label: str, errors: list[str]) -> None:
    for field in fields:
        if not row[field].strip():
            errors.append(f"{label}: {field} is required")


def check_date(value: str, label: str, errors: list[str]) -> date | None:
    if not value:
        return None
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: expected a real YYYY-MM-DD date")
        return None


def check_score(value: str, label: str, errors: list[str]) -> None:
    if value and value not in {"0", "1", "2", "3", "4", "5"}:
        errors.append(f"{label}: score_0_5 must be blank or an integer from 0 to 5")


def load_inputs(data_dir: Path | None = None) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return validated ontology/metrics, raising before any output is written.

    ``data_dir`` is the ontology directory (``data/ontology`` by default).
    """
    if data_dir is None:
        from paths import ontology_dir

        data_dir = ontology_dir()
    taxonomy = read_table(data_dir / "taxonomy.csv", TAXONOMY_FIELDS)
    metrics = read_table(data_dir / "metrics.csv", METRIC_FIELDS)
    errors: list[str] = []
    expected_subsystems = {f"{d}.{s}" for d in range(1, 11) for s in range(1, 11)}
    if len(taxonomy) != 100 or {r["subsystem_id"] for r in taxonomy} != expected_subsystems:
        errors.append("taxonomy.csv: expected each of the 100 subsystem IDs 1.1 through 10.10 exactly once")
    domains: dict[str, str] = {}
    for number, row in enumerate(taxonomy, 2):
        label = f"taxonomy.csv row {number}"
        require_values(row, TAXONOMY_FIELDS, label, errors)
        if row["domain_id"] not in {str(i) for i in range(1, 11)}:
            errors.append(f"{label}: domain_id must be 1 through 10")
        if row["subsystem_id"].split(".")[0] != row["domain_id"]:
            errors.append(f"{label}: subsystem_id does not belong to domain_id")
        previous = domains.setdefault(row["domain_id"], row["domain"])
        if previous != row["domain"]:
            errors.append(f"{label}: inconsistent domain name")
        if row["criticality"] not in {"high", "critical"}:
            errors.append(f"{label}: criticality must be high or critical for v0.1")
    if len(set(domains.values())) != 10:
        errors.append("taxonomy.csv: expected 10 distinct domain names")
    if len(metrics) != 10 or {r["metric_id"] for r in metrics} != {f"M{i}" for i in range(1, 11)}:
        errors.append("metrics.csv: expected M1 through M10 exactly once")
    for number, row in enumerate(metrics, 2):
        require_values(row, METRIC_FIELDS, f"metrics.csv row {number}", errors)
    if errors:
        raise ValidationError("\n".join(errors))
    return taxonomy, metrics


def validate_dimensions(path: Path, taxonomy, metrics) -> int:
    rows = read_table(path, DIMENSION_FIELDS)
    subsystems = {r["subsystem_id"]: r for r in taxonomy}
    metric_map = {r["metric_id"]: r for r in metrics}
    expected_ids = {f"{s}-{m}" for s in subsystems for m in metric_map}
    errors: list[str] = []
    if len(rows) != 1000 or {r["dimension_id"] for r in rows} != expected_ids:
        errors.append(f"{path}: expected all 1000 unique subsystem-metric dimension IDs")
    for number, row in enumerate(rows, 2):
        label = f"{path.name} row {number}"
        subsystem = subsystems.get(row["subsystem_id"])
        metric = metric_map.get(row["metric_id"])
        if subsystem is None or metric is None:
            errors.append(f"{label}: unknown subsystem_id or metric_id")
            continue
        if row["dimension_id"] != f"{row['subsystem_id']}-{row['metric_id']}":
            errors.append(f"{label}: dimension_id does not match subsystem_id and metric_id")
        for field in ("domain_id", "domain", "subsystem", "criticality"):
            if row[field] != subsystem[field]:
                errors.append(f"{label}: {field} disagrees with taxonomy.csv")
        if row["metric"] != metric["metric"]:
            errors.append(f"{label}: metric disagrees with metrics.csv")
        require_values(row, ("test_question",), label, errors)
        check_score(row["score_0_5"], label, errors)
        if row["confidence_0_1"]:
            try:
                confidence = float(row["confidence_0_1"])
                if not math.isfinite(confidence) or not 0 <= confidence <= 1:
                    raise ValueError
            except ValueError:
                errors.append(f"{label}: confidence_0_1 must be finite and between 0 and 1")
        check_date(row["evidence_date"], f"{label} evidence_date", errors)
        if row["evidence_type"] and row["evidence_type"] not in EVIDENCE_LEVELS:
            errors.append(f"{label}: evidence_type must be E0 through E5")
        if row["score_0_5"]:
            require_values(row, ("confidence_0_1", "evidence_date", "evidence_type", "source"), label, errors)
            if row["evidence_type"] == "E0":
                require_values(row, ("notes",), label, errors)
    if errors:
        raise ValidationError("\n".join(errors))
    return len(rows)


def validate_evidence(path: Path, taxonomy, metrics) -> int:
    rows = read_table(path, EVIDENCE_FIELDS)
    subsystems = {r["subsystem_id"]: r for r in taxonomy}
    metric_ids = {r["metric_id"] for r in metrics}
    errors: list[str] = []
    seen: set[str] = set()
    for number, row in enumerate(rows, 2):
        label = f"{path.name} row {number}"
        require_values(row, (
            "record_id", "year", "as_of_date", "domain_id", "subsystem_id", "metric_id",
            "human_removal_scenario", "evidence_level", "confidence", "observed_capability",
        ), label, errors)
        if row["record_id"] in seen:
            errors.append(f"{label}: duplicate record_id {row['record_id']}")
        seen.add(row["record_id"])
        subsystem = subsystems.get(row["subsystem_id"])
        if subsystem is None or subsystem["domain_id"] != row["domain_id"]:
            errors.append(f"{label}: unknown or mismatched subsystem/domain")
        if row["metric_id"] not in metric_ids:
            errors.append(f"{label}: unknown metric_id")
        for field, allowed in (
            ("human_removal_scenario", SCENARIOS), ("evidence_level", EVIDENCE_LEVELS),
            ("confidence", {"Low", "Medium", "High"}),
        ):
            if row[field] not in allowed:
                errors.append(f"{label}: invalid {field}: {row[field]!r}")
        if row["single_point_of_failure"] not in {"", "Yes", "No", "Unknown"}:
            errors.append(f"{label}: single_point_of_failure must be Yes, No, Unknown or blank")
        if row["source_type"] and row["source_type"] not in SOURCE_TYPES:
            errors.append(f"{label}: invalid source_type")
        check_score(row["score_0_5"], label, errors)
        as_of = check_date(row["as_of_date"], f"{label} as_of_date", errors)
        source_date = check_date(row["source_date"], f"{label} source_date", errors)
        if not re.fullmatch(r"[1-9]\d{3}", row["year"]):
            errors.append(f"{label}: year must be a four-digit baseline year")
        elif as_of and as_of.year > int(row["year"]):
            errors.append(f"{label}: as_of_date is after the baseline year")
        if source_date and as_of and source_date > as_of:
            errors.append(f"{label}: source_date is after as_of_date")
        if row["evidence_level"] == "E0":
            require_values(row, ("notes",), label, errors)
        else:
            require_values(row, ("source_title", "source_url", "source_type", "source_date"), label, errors)
    if errors:
        raise ValidationError("\n".join(errors))
    return len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, help="also validate a scenario evidence CSV")
    parser.add_argument("--require-dimensions", action="store_true", help="fail if dimensions.csv is missing")
    args = parser.parse_args(argv)
    try:
        from paths import dimensions_csv, evidence_schema_csv, ontology_dir

        taxonomy, metrics = load_inputs(ontology_dir())
        schema = read_table(evidence_schema_csv(), ("field", "description"))
        if len(schema) != len(EVIDENCE_FIELDS) or {r["field"] for r in schema} != set(EVIDENCE_FIELDS):
            raise ValidationError("evidence_schema.csv: expected each of the 23 evidence fields exactly once")
        if any(not row["description"].strip() for row in schema):
            raise ValidationError("evidence_schema.csv: field descriptions must not be blank")
        dimensions = dimensions_csv()
        summaries = ["10 domains / 100 subsystems / 10 metrics; evidence schema valid"]
        if dimensions.exists():
            summaries.append(f"{validate_dimensions(dimensions, taxonomy, metrics)} dimensions valid")
        elif args.require_dimensions:
            raise ValidationError(f"{dimensions}: missing; run scripts/generate_dimensions.py first")
        else:
            summaries.append("dimensions.csv absent (not checked; use --require-dimensions to require it)")
        if args.evidence is not None:
            summaries.append(f"{validate_evidence(args.evidence, taxonomy, metrics)} evidence records valid")
    except ValidationError as exc:
        print(f"Validation failed:\n{exc}", file=sys.stderr)
        return 1
    for summary in summaries:
        print(f"OK: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
