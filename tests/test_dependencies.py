"""Dependency graphs keep structural hypotheses separate from verified evidence."""

from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analyze_dependencies.py"
SPEC = importlib.util.spec_from_file_location("dependency_analysis", SCRIPT)
dependencies = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(SCRIPT.parent))
try:
    SPEC.loader.exec_module(dependencies)
finally:
    sys.path.pop(0)


def edge(identifier="DEP-TEST", consumer="1.1", upstream="1.2", **updates):
    row = dict.fromkeys(dependencies.FIELDS, "")
    row.update(
        dependency_id=identifier, consumer_subsystem_id=consumer,
        upstream_subsystem_id=upstream, dependency_type="component",
        critical="Unknown", verification_status="structural_hypothesis",
        notes="Synthetic route-conditional hypothesis for testing, not empirical evidence.",
    )
    row.update(updates)
    return row


class DependencyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="mcab-dependencies-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        ontology = self.root / "data" / "ontology"
        ontology.mkdir(parents=True)
        for name in ("taxonomy.csv", "metrics.csv"):
            shutil.copy2(ROOT / "data" / "ontology" / name, ontology / name)
        self.path = ontology / "dependencies.csv"

    def write(self, rows):
        with self.path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=dependencies.FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def load(self):
        return dependencies.load_dependencies(self.root, Path("data/ontology/dependencies.csv"))

    def copy_scripts(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        for name in ("analyze_dependencies.py", "validate_data.py", "paths.py"):
            shutil.copy2(ROOT / "scripts" / name, scripts / name)
        return scripts

    def test_seed_table_is_explicitly_structural_without_claimed_verified_links(self):
        rows = dependencies.load_dependencies(ROOT, Path("data/ontology/dependencies.csv"))
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["verification_status"] == "structural_hypothesis" for row in rows))
        self.assertTrue(all(row["critical"] == "Unknown" and row["evidence_refs"] == "" for row in rows))
        result = dependencies.analyze(rows)
        self.assertEqual(result["verified_graph"]["edge_count"], 0)
        self.assertEqual(result["weakest_nodes"], [])
        self.assertEqual(result["highest_human_dependence"], [])
        self.assertEqual(result["possible_bottlenecks"], [])
        self.assertEqual(result["evidence_reported_single_points_of_failure"], [])
        self.assertEqual(result["evidence_reported_spof_assessment"]["status"], "not_assessed")
        self.assertEqual(result["critical_path_assessment"]["status"], "not_assessed")
        self.assertIsNone(result["critical_path_minimum_score"])
        self.assertFalse(result["critical_path_assessment"]["all_complete"])
        self.assertTrue(all(node["single_point_of_failure"] == "Unknown" for node in result["structural_exposure"]["nodes"]))

    def test_invalid_references_self_links_enums_and_evidence_are_rejected(self):
        cases = (
            {"consumer_subsystem_id": "11.1"}, {"upstream_subsystem_id": "1.11"},
            {"upstream_subsystem_id": "1.1"}, {"dependency_type": "unrecognized"},
            {"critical": "Probably"}, {"verification_status": "unreviewed"},
            {"verification_status": "verified", "evidence_refs": ""},
            {"evidence_refs": "SOURCE-001"}, {"notes": ""},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                self.write([edge(**changes)])
                with self.assertRaises(dependencies.ValidationError):
                    self.load()

    def test_duplicate_pairs_and_ids_are_rejected(self):
        for rows in (
            [edge(), edge(identifier="DEP-OTHER", dependency_type="maintenance")],
            [edge(), edge(consumer="1.3", upstream="1.4")],
        ):
            with self.subTest(rows=rows):
                self.write(rows)
                with self.assertRaises(dependencies.ValidationError):
                    self.load()

    def test_empty_graph_remains_unknown_without_phantom_nodes_or_scores(self):
        self.write([])
        result = dependencies.analyze(self.load())
        self.assertEqual(result["structural_exposure"]["nodes"], [])
        self.assertEqual(result["verified_graph"]["strongly_connected_components"], [])
        self.assertEqual(result["weakest_nodes"], [])
        self.assertEqual(result["highest_human_dependence"], [])
        self.assertEqual(result["score_assessment"]["status"], "not_assessed")

    def test_cycles_are_valid_and_reachability_excludes_the_node_itself(self):
        self.write([edge("A"), edge("B", "1.2", "1.1"), edge("C", "1.3", "1.2")])
        result = dependencies.analyze(self.load())
        graph = result["structural_exposure"]
        self.assertEqual(graph["cyclic_components"], [["1.1", "1.2"]])
        nodes = {row["subsystem_id"]: row for row in graph["nodes"]}
        self.assertEqual(nodes["1.2"]["direct_consumer_count"], 2)
        self.assertEqual(nodes["1.2"]["transitive_consumer_count"], 2)
        self.assertEqual(nodes["1.1"]["transitive_consumer_count"], 2)
        self.assertEqual(nodes["1.3"]["transitive_consumer_count"], 0)

    def test_ordinal_rankings_require_scores_and_bottlenecks_require_verified_critical_edges(self):
        self.write([
            edge("HYPOTHESIS", "1.4", "1.1", critical="Yes"),
            edge("VERIFIED", "1.3", "1.2", verification_status="verified", critical="Yes", evidence_refs="synthetic-test-source"),
            edge("UNCERTAIN", "1.5", "1.1", verification_status="verified", evidence_refs="synthetic-test-source"),
        ])
        scores = {"subsystems": {
            "1.1": {"HR100": 5, "HR0": 3}, "1.2": {"HR100": 5, "HR0": 0},
            "1.3": {"HR100": None, "HR0": None}, "1.4": {"HR100": 0, "HR0": 0},
            "1.5": {"HR100": 2, "HR0": 3},
        }}
        result = dependencies.analyze(self.load(), scores)
        self.assertNotIn("1.3", [row["subsystem_id"] for row in result["weakest_nodes"]])
        self.assertEqual(result["weakest_nodes"][0]["score_0_5"], 0)
        self.assertEqual([row["subsystem_id"] for row in result["highest_human_dependence"]], ["1.2", "1.1"])
        self.assertEqual(result["highest_human_dependence"][0]["H_ordinal_proxy"], 1)
        self.assertEqual(result["human_dependence_assessment"]["excluded_monotonicity_violations"], ["1.5"])
        self.assertEqual([row["subsystem_id"] for row in result["possible_bottlenecks"]], ["1.2"])
        self.assertEqual(result["possible_bottlenecks"][0]["critical_dependency_ids"], ["VERIFIED"])
        self.assertIsNone(result["critical_path_minimum_score"])
        for graph in (result["structural_exposure"], result["verified_graph"]):
            self.assertTrue(all(row["single_point_of_failure"] == "Unknown" for row in graph["nodes"]))

    def test_critical_minimum_requires_every_endpoint_in_the_verified_critical_scope(self):
        self.write([
            edge("A", verification_status="verified", critical="Yes", evidence_refs="test-source"),
            edge("B", "1.2", "1.1", verification_status="verified", critical="Yes", evidence_refs="test-source"),
            edge("UNCERTAIN", "1.2", "1.3", verification_status="verified", evidence_refs="test-source"),
            edge("HYPOTHESIS", "1.4", "1.5", critical="Yes"),
        ])
        scores = {"subsystems": {"1.1": {"HR0": 2}, "1.2": {"HR0": None}}}
        result = dependencies.analyze(self.load(), scores)
        self.assertEqual(result["critical_path_assessment"]["scope_ids"], ["1.1", "1.2"])
        self.assertEqual(result["critical_path_assessment"]["missing_score_ids"], ["1.2"])
        self.assertFalse(result["critical_path_assessment"]["all_complete"])
        self.assertIsNone(result["critical_path_minimum_score"])
        scores["subsystems"]["1.2"]["HR0"] = 0
        result = dependencies.analyze(self.load(), scores)
        self.assertTrue(result["critical_path_assessment"]["all_complete"])
        self.assertEqual(result["critical_path_assessment"]["missing_score_ids"], [])
        self.assertEqual(result["critical_path_minimum_score"], 0)
        self.assertEqual(result["critical_path_assessment"]["status"], "declared_subgraph_minimum")
        self.assertEqual(result["verified_graph"]["cyclic_components"], [["1.1", "1.2"]])

    def test_invalid_or_divergent_score_contract_is_rejected(self):
        cases = (
            {"records": []}, {"subsystems": []},
            {"subsystems": {"1.1": {"HR0": float("nan")}}},
            {"subsystems": {"1.1": {"HR0": True}}},
            {"subsystems": {"1.1": {"HR0": 6}}},
            {"subsystems": {"1.1": {"HR2": 2}}},
            {"subsystems": {"11.1": {"HR0": 0}}},
        )
        for scores in cases:
            with self.subTest(scores=scores):
                with self.assertRaises(dependencies.DependencyError):
                    dependencies.analyze([], scores)

    def test_manual_spof_yes_assertion_preserves_scenario_and_source_without_graph_inference(self):
        claim = {
            "record_id": "manual-001", "dimension_id": "1.1-M4", "subsystem_id": "1.1",
            "scenario": "HR10", "assessment": "Yes", "evidence_level": "E3",
            "confidence": "Medium", "source_url": "https://example.org/manual-evidence",
            "as_of_date": "2026-10-31",
        }
        scores = {"subsystems": {}, "reported_spof_assessments": [claim]}
        result = dependencies.analyze([edge()], scores)
        self.assertEqual(result["evidence_reported_single_points_of_failure"], [claim])
        self.assertEqual(result["evidence_reported_spof_assessment"]["status"], "manual_source_claims_only")
        self.assertTrue(all(node["single_point_of_failure"] == "Unknown" for node in result["structural_exposure"]["nodes"]))
        self.assertEqual(result["weakest_nodes"], [])
        self.assertEqual(result["possible_bottlenecks"], [])
        for changes in ({"source_url": ""}, {"dimension_id": "2.1-M4"}, {"scenario": "HR25"}, {"as_of_date": "2026-02-30"}):
            with self.subTest(changes=changes):
                scores["reported_spof_assessments"] = [dict(claim, **changes)]
                with self.assertRaises(dependencies.DependencyError):
                    dependencies.analyze([], scores)
        scores["reported_spof_assessments"] = [dict(claim, assessment="No")]
        result = dependencies.analyze([], scores)
        self.assertEqual(result["evidence_reported_single_points_of_failure"], [])
        self.assertEqual(result["evidence_reported_spof_assessment"]["reported_assessment_count"], 1)
        self.assertEqual(result["evidence_reported_spof_assessment"]["status"], "not_assessed")
        inference = dict(claim, evidence_level="E0", confidence="Low", source_url="", notes="Manual inference with no empirical verification.")
        scores["reported_spof_assessments"] = [inference]
        result = dependencies.analyze([], scores)
        self.assertEqual(result["evidence_reported_single_points_of_failure"], [inference])
        scores["reported_spof_assessments"] = [dict(inference, notes="")]
        with self.assertRaises(dependencies.DependencyError):
            dependencies.analyze([], scores)

    def test_cli_generates_json_with_input_hashes_without_inventing_null_scores(self):
        self.write([edge()])
        scripts = self.copy_scripts()
        scores_path = self.root / "scores.json"
        scores_path.write_text(json.dumps({"subsystems": {"1.1": {"HR0": None, "HR100": None}}}), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(scripts / "analyze_dependencies.py"), "--scores", "scores.json"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads((self.root / "data/editions/2026/analysis/dependencies.json").read_text())
        self.assertEqual(len(output["dependency_csv_sha256"]), 64)
        self.assertEqual(len(output["scores_sha256"]), 64)
        self.assertEqual(len(output["taxonomy_sha256"]), 64)
        self.assertEqual(len(output["metrics_sha256"]), 64)
        self.assertEqual(output["weakest_nodes"], [])
        self.assertEqual(output["possible_bottlenecks"], [])

    def test_output_cannot_replace_dependency_or_score_inputs(self):
        self.write([edge()])
        scripts = self.copy_scripts()
        scores = self.root / "scores.json"
        scores.write_text(json.dumps({"subsystems": {}}), encoding="utf-8")
        curated = self.root / "data/ontology/curated-research.json"
        curated.write_text('{"curated":true}\n', encoding="utf-8")
        for output in (self.path, scores, curated):
            with self.subTest(output=output):
                original = output.read_bytes()
                result = subprocess.run(
                    [sys.executable, str(scripts / "analyze_dependencies.py"), "--scores", "scores.json", "--output", str(output)],
                    cwd=self.root, capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(output.read_bytes(), original)

    def test_atomic_write_failure_preserves_old_analysis_and_removes_temporary_file(self):
        output = self.root / "old-analysis.json"
        output.write_bytes(b'{"previous_analysis":true}\n')
        original = output.read_bytes()
        with mock.patch.object(dependencies.os, "replace", side_effect=OSError("simulated failure")):
            with self.assertRaises(OSError):
                dependencies.write_json_atomic(output, {"new_analysis": True})
        self.assertEqual(output.read_bytes(), original)
        self.assertFalse(list(self.root.glob(".dependencies-*.tmp")))


if __name__ == "__main__":
    unittest.main()
