#!/usr/bin/env python3
"""Conservatively screen manually scored MCAB evidence; never infer missing scores."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

from validate_data import EVIDENCE_FIELDS, ValidationError, load_inputs, read_table, validate_evidence

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("HR100", "HR50", "HR10", "HR1", "HR0")
FORMULA_VERSION = "mcab-proxy-v0.1"
AS_OF = "2026-11-02"


def complete_min(values: list[int | None]) -> int | None:
    """Missing members prevent a complete aggregate, including an empty set."""
    if not values or any(value is None for value in values):
        return None
    return min(values)


def validate_scope(rows: list[dict], year: int, as_of: str) -> None:
    if not isinstance(year, int) or not 1000 <= year <= 9999:
        raise ValidationError("year must be a four-digit baseline year")
    try:
        cutoff = date.fromisoformat(as_of)
        if cutoff.isoformat() != as_of or cutoff.year > year:
            raise ValueError
    except (ValueError, TypeError) as error:
        raise ValidationError("as_of must be a real YYYY-MM-DD date no later than the selected baseline year") from error
    for row in rows:
        if row["year"] != str(year):
            raise ValidationError(f"{row['record_id']}: evidence baseline year {row['year']} differs from selected year {year}")
        for field in ("as_of_date", "source_date"):
            if row[field] and date.fromisoformat(row[field]) > cutoff:
                raise ValidationError(f"{row['record_id']}: {field} is after scoring cutoff {as_of}")


def aggregate_scores(taxonomy: list[dict], metrics: list[dict], rows: list[dict], evidence_label: str, *, year: int = 2026, as_of: str = AS_OF) -> dict:
    """Aggregate already validated rows using minima on the ordinal score scale."""
    validate_scope(rows, year, as_of)
    dimensions = {
        f"{subsystem['subsystem_id']}-{metric['metric_id']}": dict.fromkeys(SCENARIOS)
        for subsystem in taxonomy for metric in metrics
    }
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        identifier = f"{row['subsystem_id']}-{row['metric_id']}"
        grouped[identifier, row["human_removal_scenario"]].append(row)
    selection, conflicts = {}, []
    for (identifier, scenario), evidence in grouped.items():
        scored = [row for row in evidence if row["score_0_5"] != ""]
        distinct = sorted({int(row["score_0_5"]) for row in scored})
        selected = min(distinct) if distinct else None
        dimensions[identifier][scenario] = selected
        detail = {
            "record_ids": [row["record_id"] for row in evidence],
            "scored_record_ids": [row["record_id"] for row in scored],
            "unscored_record_ids": [row["record_id"] for row in evidence if row["score_0_5"] == ""],
            "distinct_scores": distinct,
            "conflict": len(distinct) > 1,
        }
        selection.setdefault(identifier, {})[scenario] = detail
        if detail["conflict"]:
            conflicts.append({"dimension_id": identifier, "scenario": scenario, "distinct_scores": distinct, "selected_score": selected, "record_ids": detail["scored_record_ids"]})

    subsystem_members = {
        subsystem["subsystem_id"]: [f"{subsystem['subsystem_id']}-{metric['metric_id']}" for metric in metrics]
        for subsystem in taxonomy
    }
    subsystems = {
        identifier: {scenario: complete_min([dimensions[dimension][scenario] for dimension in members]) for scenario in SCENARIOS}
        for identifier, members in subsystem_members.items()
    }
    domain_members: dict[str, list[str]] = defaultdict(list)
    for subsystem in taxonomy:
        domain_members[subsystem["domain_id"]].append(subsystem["subsystem_id"])
    domains = {
        identifier: {scenario: complete_min([subsystems[subsystem][scenario] for subsystem in members]) for scenario in SCENARIOS}
        for identifier, members in domain_members.items()
    }
    critical_dimensions = [
        f"{subsystem['subsystem_id']}-{metric['metric_id']}"
        for subsystem in taxonomy if subsystem["criticality"] == "critical" for metric in metrics
    ]
    scenarios = {}
    for scenario in SCENARIOS:
        observed = [value[scenario] for value in dimensions.values() if value[scenario] is not None]
        critical_known = sum(dimensions[identifier][scenario] is not None for identifier in critical_dimensions)
        scenarios[scenario] = {
            "total_dimensions": len(dimensions),
            "scored_dimensions": len(observed),
            "unknown_dimensions": len(dimensions) - len(observed),
            "total_subsystems": len(subsystems),
            "scored_subsystems": sum(scores[scenario] is not None for scores in subsystems.values()),
            "total_domains": len(domains),
            "scored_domains": sum(scores[scenario] is not None for scores in domains.values()),
            "scored_records": sum(row["human_removal_scenario"] == scenario and row["score_0_5"] != "" for row in rows),
            "observed_min": min(observed) if observed else None,
            "critical_total_dimensions": len(critical_dimensions),
            "critical_scored_dimensions": critical_known,
            "critical_complete": bool(critical_dimensions) and critical_known == len(critical_dimensions),
            "critical_min": complete_min([dimensions[identifier][scenario] for identifier in critical_dimensions]),
            "complete": len(observed) == len(dimensions),
            "conflict_dimensions": sum(conflict["scenario"] == scenario for conflict in conflicts),
        }

    hr0, hr100 = scenarios["HR0"], scenarios["HR100"]
    c_proxy = hr0["critical_min"] / 5 if hr0["critical_complete"] else None
    c_reason = (
        "HR0 critical_min / 5; all ontology-tagged critical dimensions have manual scores. This ordinal screening proxy is not measured physical industrial closure."
        if c_proxy is not None else
        f"Unknown: HR0 has scores for {hr0['critical_scored_dimensions']} of {hr0['critical_total_dimensions']} ontology-tagged critical dimensions; a nonempty complete critical set is required."
    )
    h_proxy = None
    diagnostics = []
    if not hr0["critical_complete"] or not hr100["critical_complete"]:
        h_reason = "Unknown: complete nonempty critical-dimension scores are required in both HR0 and HR100."
    elif hr100["critical_min"] == 0:
        h_reason = "Unknown: HR100 critical_min is zero; division by zero is undefined."
    elif hr0["critical_min"] > hr100["critical_min"]:
        h_reason = "Unknown: HR0 critical_min exceeds HR100 critical_min; the scenario monotonicity assumption failed. No clamping or physical dependence estimate is performed."
        diagnostics.append("HR0 critical_min exceeds HR100 critical_min; review the evidence scope and scenario comparability before interpreting an H proxy.")
    else:
        h_proxy = 1 - hr0["critical_min"] / hr100["critical_min"]
        h_reason = "1 - HR0 critical_min / HR100 critical_min. Ratios on this ordinal scale are screening conventions, not measured performance loss or physical human dependence."
    years = sorted({row["year"] for row in rows})
    return {
        "schema_version": "mcab-scores-v0.1",
        "formula_version": FORMULA_VERSION,
        "method": {
            "purpose": "Conservative ordinal screening of supplied manual evidence scores, not scientific estimates of C or H.",
            "dimension_aggregation": "Within each dimension and HR scenario, select the minimum supplied score; flag distinct-score conflicts; never average or assign missing scores.",
            "subsystem_aggregation": "Minimum of all 10 metric scores only when all 10 are known.",
            "domain_aggregation": "Minimum of all 10 complete subsystem scores only when all 100 dimension scores are known.",
            "system_aggregation": "Minimum of ontology-tagged critical dimensions only when every such dimension is known; criticality tags are not a verified dependency or critical-path graph.",
            "unknown_policy": "Unknown is null, never zero. observed_min ignores unknowns solely to summarize observed scores and must be read with its adjacent coverage counts.",
            "single_point_of_failure": "reported_spof_assessments preserves explicit source-record assertions, including No and Unknown; these are not computed or independently verified SPOFs and are not ranked.",
        },
        "limitations": [
            "The 0–5 scale is ordinal; normalization and ratios are explicitly versioned screening conventions, not calibrated physical measurements.",
            "Complete ontology coverage does not establish jointly necessary or sufficient industrial closure, comparable experimental boundaries, or independent corroboration.",
            "Different evidence systems, operating durations, and human roles are not automatically harmonized; a conservative minimum does not resolve their substantive differences.",
            "No scores are assigned from research JSON, source counts, search coverage, confidence labels, or absent evidence.",
            "R_M and g_0 require separate reproduction and longitudinal growth measurements and remain unestimated.",
        ],
        "input": {"evidence_path": evidence_label, "year": year, "as_of_date": as_of, "evidence_records": len(rows), "scored_records": sum(row["score_0_5"] != "" for row in rows), "unscored_records": sum(row["score_0_5"] == "" for row in rows), "baseline_years": years},
        "totals": {"dimensions": len(dimensions), "subsystems": len(subsystems), "domains": len(domains), "metrics_per_subsystem": len(metrics), "critical_dimensions": len(critical_dimensions)},
        "scenarios": scenarios,
        "proxies": {"C_proxy": c_proxy, "H_proxy": h_proxy, "R_M": None, "g_0": None},
        "proxy_explanations": {"C_proxy": c_reason, "H_proxy": h_reason, "R_M": "Not estimated: no machine-system reproduction measurement is provided by this scoring workflow.", "g_0": "Not estimated: no longitudinal human-free growth measurement is provided by this scoring workflow."},
        "diagnostics": diagnostics,
        "dimensions": dimensions,
        "subsystems": subsystems,
        "domains": domains,
        "evidence_selection": selection,
        "conflicts": conflicts,
        "reported_spof_assessments": [
            {
                "record_id": row["record_id"],
                "dimension_id": f"{row['subsystem_id']}-{row['metric_id']}",
                "subsystem_id": row["subsystem_id"],
                "scenario": row["human_removal_scenario"],
                "assessment": row["single_point_of_failure"],
                "evidence_level": row["evidence_level"],
                "confidence": row["confidence"],
                "source_url": row["source_url"],
                "as_of_date": row["as_of_date"],
                "notes": row["notes"],
            }
            for row in rows if row["single_point_of_failure"]
        ],
    }


def build_scores(evidence: Path, data_dir: Path = ROOT / "data", *, year: int = 2026, as_of: str = AS_OF) -> dict:
    input_paths = {"evidence_sha256": evidence, "taxonomy_sha256": data_dir / "taxonomy.csv", "metrics_sha256": data_dir / "metrics.csv"}
    snapshots = {key: path.read_bytes() for key, path in input_paths.items()}
    taxonomy, metrics = load_inputs(data_dir)
    validate_evidence(evidence, taxonomy, metrics)
    rows = read_table(evidence, EVIDENCE_FIELDS)
    try:
        label = evidence.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        label = str(evidence)
    result = aggregate_scores(taxonomy, metrics, rows, label, year=year, as_of=as_of)
    for key, path in input_paths.items():
        if path.read_bytes() != snapshots[key]:
            raise ValidationError(f"{path}: input changed while scoring; rerun with stable input files")
        result["input"][key] = hashlib.sha256(snapshots[key]).hexdigest()
    return result


def validate_output_path(output: Path, evidence: Path | None = None) -> None:
    if evidence is not None and evidence.resolve() == output.resolve():
        raise ValidationError("Evidence input and JSON output must be different files")
    data_root, analysis_root = ROOT / "data", ROOT / "data" / "analysis"
    lexical_output = Path(os.path.abspath(output))
    resolved_output = output.resolve()
    lexical_protected = lexical_output.is_relative_to(data_root) and not lexical_output.is_relative_to(analysis_root)
    resolved_protected = resolved_output.is_relative_to(data_root.resolve()) and not resolved_output.is_relative_to(analysis_root.resolve())
    if lexical_protected or resolved_protected:
        raise ValidationError("Scoring output must not overwrite curated data; use data/analysis/ or a custom output outside data/")


def write_scores(result: dict, output: Path) -> None:
    validate_output_path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, prefix=".scores-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "data" / "evidence_2026.csv", help="validated manual scenario evidence CSV; a header-only file yields all unknown scores")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "analysis" / "2026" / "scores.json", help="JSON analysis output")
    parser.add_argument("--year", type=int, default=2026, help="required baseline year for every evidence row; other years are rejected")
    parser.add_argument("--as-of", default=AS_OF, help="latest permitted evidence as_of_date and source_date (YYYY-MM-DD)")
    args = parser.parse_args(argv)
    try:
        validate_output_path(args.output, args.evidence)
        result = build_scores(args.evidence, year=args.year, as_of=args.as_of)
        write_scores(result, args.output)
    except (ValidationError, OSError, UnicodeError, ValueError) as error:
        print(f"Scoring failed: {error}", file=sys.stderr)
        return 1
    print(f"OK: {result['input']['evidence_records']} evidence records; {result['totals']['dimensions']} dimensions; {FORMULA_VERSION} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
