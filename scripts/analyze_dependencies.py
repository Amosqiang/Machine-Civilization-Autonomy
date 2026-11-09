#!/usr/bin/env python3
"""Validate MCAB dependency edges and report graph structure without inventing scores.

Edges point from a consumer to its upstream supplier. Structural hypotheses and
contributor-declared verified edges are analyzed separately. A verified label is
not independently checked by this script: evidence references require review.
Optional scores use score_evidence.py's JSON contract: subsystems maps subsystem
IDs to HR100/HR50/HR10/HR1/HR0 scores, with null for incomplete assessments.
All relative CLI paths are resolved against the repository root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

from paths import DEFAULT_YEAR, dependencies_csv, dependencies_json, is_curated_data, metrics_csv, taxonomy_csv
from validate_data import ValidationError, load_inputs, read_table

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "dependency_id", "consumer_subsystem_id", "upstream_subsystem_id",
    "dependency_type", "critical", "verification_status", "evidence_refs",
    "substitutes", "notes",
)
DEPENDENCY_TYPES = {"energy", "material", "component", "software", "maintenance", "logistics"}
SCENARIOS = {"HR100", "HR50", "HR10", "HR1", "HR0"}


class DependencyError(ValidationError):
    """Invalid dependency table or score input."""


def node_key(identifier: str) -> tuple[int, int]:
    return tuple(int(part) for part in identifier.split("."))


def resolve_path(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def load_dependencies(root: Path, path: Path) -> list[dict[str, str]]:
    """Read the dependency CSV and validate references against the full ontology."""
    taxonomy, _ = load_inputs(root / "data" / "ontology")
    subsystem_ids = {row["subsystem_id"] for row in taxonomy}
    rows = read_table(resolve_path(root, path), FIELDS)
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for number, row in enumerate(rows, 2):
        label = f"dependencies row {number}"
        identifier = row["dependency_id"]
        if not identifier.strip() or identifier in seen_ids:
            errors.append(f"{label}: dependency_id must be nonempty and unique")
        seen_ids.add(identifier)
        consumer, upstream = row["consumer_subsystem_id"], row["upstream_subsystem_id"]
        if consumer not in subsystem_ids or upstream not in subsystem_ids:
            errors.append(f"{label}: unknown consumer or upstream subsystem ID")
        if consumer == upstream:
            errors.append(f"{label}: self-dependencies are not allowed")
        if (consumer, upstream) in seen_pairs:
            errors.append(f"{label}: duplicate consumer/upstream pair")
        seen_pairs.add((consumer, upstream))
        if row["dependency_type"] not in DEPENDENCY_TYPES:
            errors.append(f"{label}: unknown dependency_type")
        if row["critical"] not in {"Yes", "No", "Unknown"}:
            errors.append(f"{label}: critical must be Yes, No or Unknown")
        status = row["verification_status"]
        if status not in {"structural_hypothesis", "verified"}:
            errors.append(f"{label}: unknown verification_status")
        if status == "verified" and not row["evidence_refs"].strip():
            errors.append(f"{label}: verified dependencies require evidence_refs")
        if status == "structural_hypothesis" and row["evidence_refs"].strip():
            errors.append(f"{label}: structural hypotheses must leave evidence_refs blank")
        if not row["notes"].strip():
            errors.append(f"{label}: notes must state the dependency's scope and assumptions")
    if errors:
        raise DependencyError("\n".join(errors))
    return rows


def strongly_connected_components(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan's algorithm; an industrial feedback cycle is valid graph data."""
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    active: set[str] = set()
    components: list[list[str]] = []

    def visit(node: str) -> None:
        indices[node] = lowlinks[node] = len(indices)
        stack.append(node)
        active.add(node)
        for neighbor in sorted(graph[node], key=node_key):
            if neighbor not in indices:
                visit(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in active:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])
        if lowlinks[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                active.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(sorted(component, key=node_key))

    for node in sorted(graph, key=node_key):
        if node not in indices:
            visit(node)
    return sorted(components, key=lambda component: node_key(component[0]))


def describe_graph(rows: list[dict[str, str]], basis: str) -> dict:
    graph: dict[str, set[str]] = {}
    consumers: dict[str, set[str]] = {}
    for row in rows:
        consumer, upstream = row["consumer_subsystem_id"], row["upstream_subsystem_id"]
        for node in (consumer, upstream):
            graph.setdefault(node, set())
            consumers.setdefault(node, set())
        graph[consumer].add(upstream)
        consumers[upstream].add(consumer)
    nodes = []
    for node in sorted(graph, key=node_key):
        reached: set[str] = set()
        pending = list(consumers[node])
        while pending:
            member = pending.pop()
            if member not in reached:
                reached.add(member)
                pending.extend(consumers[member] - reached)
        reached.discard(node)
        nodes.append({
            "subsystem_id": node,
            "direct_upstream_count": len(graph[node]),
            "direct_consumer_count": len(consumers[node]),
            "transitive_consumer_count": len(reached),
            "single_point_of_failure": "Unknown",
        })
    components = strongly_connected_components(graph)
    return {
        "basis": basis,
        "edge_count": len(rows),
        "node_count": len(nodes),
        "edges": sorted(rows, key=lambda row: row["dependency_id"]),
        "nodes": nodes,
        "exposure_order": [node["subsystem_id"] for node in sorted(
            nodes,
            key=lambda node: (-node["transitive_consumer_count"], -node["direct_consumer_count"], node_key(node["subsystem_id"])),
        )],
        "strongly_connected_components": components,
        "cyclic_components": [component for component in components if len(component) > 1],
        "interpretation": "Counts describe the listed edges only; neither degree nor reachability proves indispensability, failure propagation or a single point of failure.",
    }


def subsystem_scores(scores: dict | None) -> dict[str, dict]:
    if scores is None:
        return {}
    if not isinstance(scores, dict) or not isinstance(scores.get("subsystems"), dict):
        raise DependencyError("scores must use the scoring JSON contract with a subsystems object")
    subsystems = scores["subsystems"]
    expected = {f"{domain}.{subsystem}" for domain in range(1, 11) for subsystem in range(1, 11)}
    for identifier, values in subsystems.items():
        if identifier not in expected or not isinstance(values, dict):
            raise DependencyError(f"scores: invalid subsystem {identifier!r}")
        for scenario, value in values.items():
            if scenario not in SCENARIOS:
                raise DependencyError(f"scores {identifier}: unknown scenario {scenario!r}")
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, (int, float))
                or not 0 <= value <= 5 or not math.isfinite(value)
            ):
                raise DependencyError(f"scores {identifier}/{scenario}: expected null or a finite score from 0 to 5")
    return subsystems


def reported_spof_assessments(scores: dict | None) -> list[dict]:
    """Validate manual source claims without treating them as graph inference."""
    if scores is None:
        return []
    claims = scores.get("reported_spof_assessments", [])
    if not isinstance(claims, list):
        raise DependencyError("reported_spof_assessments must be a list")
    fields = (
        "record_id", "dimension_id", "subsystem_id", "scenario", "assessment",
        "evidence_level", "confidence", "source_url", "as_of_date",
    )
    subsystem_ids = {f"{domain}.{subsystem}" for domain in range(1, 11) for subsystem in range(1, 11)}
    seen: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict) or any(not isinstance(claim.get(field), str) for field in fields):
            raise DependencyError("reported_spof_assessments: every claim requires string identity, scenario and provenance fields")
        identifier = claim["record_id"]
        if not identifier.strip() or identifier in seen:
            raise DependencyError("reported_spof_assessments: record_id must be nonempty and unique")
        seen.add(identifier)
        subsystem = claim["subsystem_id"]
        if subsystem not in subsystem_ids or claim["dimension_id"] not in {f"{subsystem}-M{metric}" for metric in range(1, 11)}:
            raise DependencyError(f"reported SPOF {identifier}: unknown or mismatched subsystem/dimension")
        if claim["scenario"] not in SCENARIOS or claim["assessment"] not in {"Yes", "No", "Unknown"}:
            raise DependencyError(f"reported SPOF {identifier}: invalid scenario or assessment")
        if claim["evidence_level"] not in {f"E{level}" for level in range(6)} or claim["confidence"] not in {"Low", "Medium", "High"}:
            raise DependencyError(f"reported SPOF {identifier}: invalid evidence level or confidence")
        try:
            parsed = date.fromisoformat(claim["as_of_date"])
            if parsed.isoformat() != claim["as_of_date"]:
                raise ValueError
        except ValueError as exc:
            raise DependencyError(f"reported SPOF {identifier}: as_of_date must be a real YYYY-MM-DD date") from exc
        if claim["assessment"] == "Yes" and not claim["source_url"].strip():
            if claim["evidence_level"] != "E0":
                raise DependencyError(f"reported SPOF {identifier}: E1-E5 Yes claims require source_url provenance")
            if not isinstance(claim.get("notes"), str) or not claim["notes"].strip():
                raise DependencyError(f"reported SPOF {identifier}: E0 Yes claims without a source URL require inference notes")
    return claims


def analyze(rows: list[dict[str, str]], scores: dict | None = None) -> dict:
    """Analyze validated rows; score rankings preserve missingness and provenance."""
    structural = [row for row in rows if row["verification_status"] == "structural_hypothesis"]
    verified = [row for row in rows if row["verification_status"] == "verified"]
    values = subsystem_scores(scores)
    manual_spof = reported_spof_assessments(scores)
    reported_yes_spof = [claim.copy() for claim in manual_spof if claim["assessment"] == "Yes"]
    weakest = [
        {"subsystem_id": identifier, "score_0_5": scenarios["HR0"]}
        for identifier, scenarios in values.items() if scenarios.get("HR0") is not None
    ]
    weakest.sort(key=lambda row: (row["score_0_5"], node_key(row["subsystem_id"])))
    dependence = []
    monotonicity_violations = []
    for identifier, scenarios in values.items():
        hr100, hr0 = scenarios.get("HR100"), scenarios.get("HR0")
        if hr100 is not None and hr100 > 0 and hr0 is not None:
            if hr0 > hr100:
                monotonicity_violations.append(identifier)
                continue
            dependence.append({
                "subsystem_id": identifier, "HR100": hr100, "HR0": hr0,
                "H_ordinal_proxy": 1 - hr0 / hr100,
            })
    dependence.sort(key=lambda row: (-row["H_ordinal_proxy"], node_key(row["subsystem_id"])))
    critical_upstreams: dict[str, list[str]] = {}
    critical_scope: set[str] = set()
    for row in verified:
        if row["critical"] == "Yes":
            critical_upstreams.setdefault(row["upstream_subsystem_id"], []).append(row["dependency_id"])
            critical_scope.update((row["consumer_subsystem_id"], row["upstream_subsystem_id"]))
    bottlenecks = [
        dict(row, critical_dependency_ids=sorted(critical_upstreams[row["subsystem_id"]]))
        for row in weakest if row["subsystem_id"] in critical_upstreams
    ]
    missing_critical_scores = sorted(
        (identifier for identifier in critical_scope if values.get(identifier, {}).get("HR0") is None),
        key=node_key,
    )
    critical_complete = bool(critical_scope) and not missing_critical_scores
    critical_minimum = (
        min(values[identifier]["HR0"] for identifier in critical_scope)
        if critical_complete else None
    )
    if not critical_scope:
        critical_reason = "No verified critical edges are declared, so no scoped minimum is assessed."
    elif missing_critical_scores:
        critical_reason = "Some endpoints of declared verified critical edges lack complete HR0 scores; the scoped minimum remains unknown."
    else:
        critical_reason = "This is only the minimum HR0 ordinal score among endpoints of the declared verified critical subgraph, not a global physical critical path or validated whole-industrial Closure."
    return {
        "schema_version": "0.1",
        "edge_direction": "consumer_to_upstream",
        "edge_count": len(rows),
        "structural_hypothesis_edge_count": len(structural),
        "verified_edge_count": len(verified),
        "assessment_status": (
            "verified_edges_available" if verified else
            "structural_hypotheses_only" if structural else "no_dependency_edges"
        ),
        "reasons": [
            "Graph exposure and ordinal-score rankings are separate; neither establishes causal human dependence.",
            "No verified dependencies are present; the graph cannot establish observed bottlenecks."
            if not verified else "Verified labels require source and system-boundary review before causal interpretation.",
        ],
        "structural_exposure": describe_graph(structural, "structural_hypotheses_only"),
        "verified_graph": describe_graph(verified, "contributor_declared_verified_edges_only"),
        "weakest_nodes": weakest,
        "highest_human_dependence": dependence,
        "possible_bottlenecks": bottlenecks,
        "evidence_reported_single_points_of_failure": reported_yes_spof,
        "evidence_reported_spof_assessment": {
            "status": "manual_source_claims_only" if reported_yes_spof else "not_assessed",
            "reported_assessment_count": len(manual_spof),
            "reason": "Explicit Yes assertions retain their original scenario and source provenance; they are manual source claims, not independently verified or inferred from graph degree. An empty list, No or Unknown assertions do not prove the absence of single points of failure.",
        },
        "critical_path_minimum_score": critical_minimum,
        "score_assessment": {
            "status": "assessed_subset" if weakest else "not_assessed",
            "reason": "Only complete HR0 subsystem scores supplied by the scoring artifact are ranked; null or absent scores remain unknown.",
            "scored_subsystems": len(weakest),
        },
        "human_dependence_assessment": {
            "status": "ordinal_proxy_only" if dependence else "not_assessed",
            "reason": "Requires paired complete HR100 > 0 and HR0 subsystem scores. H_ordinal_proxy = 1 - HR0/HR100 is an ordinal-score proxy, not measured performance loss or human dependence.",
            "excluded_monotonicity_violations": sorted(monotonicity_violations, key=node_key),
        },
        "critical_path_assessment": {
            "status": "declared_subgraph_minimum" if critical_complete else "not_assessed",
            "scope": "endpoints_of_declared_verified_critical_edges_only",
            "scope_ids": sorted(critical_scope, key=node_key),
            "all_complete": critical_complete,
            "missing_score_ids": missing_critical_scores,
            "reason": critical_reason,
        },
        "limitations": [
            "The seed graph is incomplete and route-conditional, not a census of industrial dependencies.",
            "Verification status is a contributor declaration; this script checks presence of evidence references, not their factual adequacy.",
            "Every single_point_of_failure remains Unknown: redundancy, substitution, capacity and recovery evidence have not been assessed.",
            "Manually reported single-point-of-failure assertions are carried separately with their original scope; they do not change graph-node assessments.",
            "Do not derive Closure, R_M or human-free growth from these graph counts or ordinal rankings.",
        ],
    }


def ensure_separate_output(output: Path, inputs: list[Path], curated_root: Path | None = None) -> None:
    """Protect curated data and input aliases from generated JSON publication."""
    if curated_root is not None and is_curated_data(output):
        raise DependencyError(
            "output under data/ must be inside data/editions/<year>/analysis/; curated data cannot be replaced"
        )
    for source in inputs:
        if output.resolve() == source.resolve() or (
            output.exists() and source.exists() and output.samefile(source)
        ):
            raise DependencyError(f"output must not overwrite an input file: {source}")


def write_json_atomic(output: Path, result: dict) -> None:
    """Replace only after the complete JSON has been serialized and flushed."""
    contents = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output.parent,
            prefix=".dependencies-", suffix=".tmp", delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dependencies", type=Path, default=None)
    parser.add_argument("--scores", type=Path, help="optional JSON produced by score_evidence.py")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help="edition year for default dependency analysis output")
    args = parser.parse_args(argv)
    try:
        dependency_path = args.dependencies if args.dependencies is not None else dependencies_csv()
        output = resolve_path(ROOT, args.output if args.output is not None else dependencies_json(args.year))
        inputs = [resolve_path(ROOT, dependency_path), taxonomy_csv(), metrics_csv()]
        if args.scores is not None:
            inputs.append(resolve_path(ROOT, args.scores))
        ensure_separate_output(output, inputs, ROOT / "data")
        rows = load_dependencies(ROOT, dependency_path)
        scores = None
        if args.scores is not None:
            scores = json.loads(resolve_path(ROOT, args.scores).read_text(encoding="utf-8"))
        result = analyze(rows, scores)
        result["dependency_csv_sha256"] = hashlib.sha256(resolve_path(ROOT, dependency_path).read_bytes()).hexdigest()
        result["taxonomy_sha256"] = hashlib.sha256(taxonomy_csv().read_bytes()).hexdigest()
        result["metrics_sha256"] = hashlib.sha256(metrics_csv().read_bytes()).hexdigest()
        result["scores_sha256"] = (
            hashlib.sha256(resolve_path(ROOT, args.scores).read_bytes()).hexdigest()
            if args.scores is not None else None
        )
        write_json_atomic(output, result)
    except (ValidationError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Dependency analysis failed: {exc}", file=sys.stderr)
        return 1
    print(f"Analyzed {len(rows)} edges ({result['verified_edge_count']} verified) -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
