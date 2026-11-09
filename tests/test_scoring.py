"""Check conservative manual-evidence aggregation and unknown propagation."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "score_evidence.py"
SPEC = importlib.util.spec_from_file_location("score_evidence", SCRIPT)
scoring = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(SCRIPT.parent))
try:
    SPEC.loader.exec_module(scoring)
finally:
    sys.path.pop(0)


class EvidenceScoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mcab-scoring-test-")
        self.addCleanup(self.temp.cleanup)
        self.evidence = Path(self.temp.name) / "evidence.csv"
        self.taxonomy, self.metrics = scoring.load_inputs(ROOT / "data" / "ontology")
        self.serial = 0

    def row(self, subsystem="1.1", metric="M1", scenario="HR0", score="3"):
        self.serial += 1
        record = dict.fromkeys(scoring.EVIDENCE_FIELDS, "")
        record.update(record_id=f"test-{self.serial}", year="2026", as_of_date="2026-11-02", domain_id=subsystem.split(".")[0], subsystem_id=subsystem, metric_id=metric, human_removal_scenario=scenario, score_0_5=score, evidence_level="E4", confidence="Medium", observed_capability="A narrowly scoped observed test.", remaining_human_role="Human maintenance remains required.", source_title="Test source", source_url="https://example.org/test", source_type="Paper", source_date="2026-10-01")
        return record

    def write(self, rows):
        with self.evidence.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=scoring.EVIDENCE_FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_header_only_evidence_produces_all_unknown_not_zero(self):
        self.write([])
        result = scoring.build_scores(self.evidence)
        self.assertEqual(result["formula_version"], "mcab-proxy-v0.1")
        self.assertEqual(len(result["dimensions"]), 1000)
        self.assertEqual(result["proxies"], dict(C_proxy=None, H_proxy=None, R_M=None, g_0=None))
        self.assertEqual(result["evidence_selection"], {})
        for scenario in scoring.SCENARIOS:
            summary = result["scenarios"][scenario]
            self.assertEqual(summary["scored_dimensions"], 0)
            self.assertEqual(summary["unknown_dimensions"], 1000)
            self.assertIsNone(summary["observed_min"])
            self.assertFalse(summary["complete"])
            self.assertFalse(summary["critical_complete"])
            self.assertIsNone(result["subsystems"]["1.1"][scenario])
            self.assertIsNone(result["domains"]["1"][scenario])
        self.assertTrue(all(value is None for scores in result["dimensions"].values() for value in scores.values()))

    def test_one_observation_does_not_produce_complete_subsystem_domain_or_closure(self):
        self.write([self.row(score="4")])
        result = scoring.build_scores(self.evidence)
        self.assertEqual(result["dimensions"]["1.1-M1"]["HR0"], 4)
        self.assertEqual(result["scenarios"]["HR0"]["observed_min"], 4)
        self.assertEqual(result["scenarios"]["HR0"]["scored_dimensions"], 1)
        self.assertEqual(result["scenarios"]["HR0"]["scored_subsystems"], 0)
        self.assertIsNone(result["domains"]["1"]["HR0"])
        self.assertIsNone(result["proxies"]["C_proxy"])

    def test_zero_is_a_real_score_and_unscored_evidence_does_not_become_zero(self):
        scored, unscored = self.row(score="0"), self.row(score="")
        self.write([scored, unscored])
        result = scoring.build_scores(self.evidence)
        self.assertEqual(result["dimensions"]["1.1-M1"]["HR0"], 0)
        self.assertEqual(result["scenarios"]["HR0"]["scored_records"], 1)
        detail = result["evidence_selection"]["1.1-M1"]["HR0"]
        self.assertEqual(detail["unscored_record_ids"], [unscored["record_id"]])
        self.assertFalse(detail["conflict"])

    def test_reported_spof_assertions_preserve_yes_no_unknown_without_inference(self):
        rows = []
        for assessment in ("Yes", "No", "Unknown", ""):
            record = self.row(score="")
            record["single_point_of_failure"] = assessment
            record["notes"] = "Source assertion only; not independently verified."
            rows.append(record)
        self.write(rows)
        result = scoring.build_scores(self.evidence)
        assertions = result["reported_spof_assessments"]
        self.assertEqual([entry["assessment"] for entry in assertions], ["Yes", "No", "Unknown"])
        self.assertEqual(assertions[0]["record_id"], rows[0]["record_id"])
        self.assertEqual(assertions[0]["dimension_id"], "1.1-M1")
        self.assertEqual(assertions[0]["scenario"], "HR0")
        self.assertEqual(assertions[0]["source_url"], rows[0]["source_url"])
        self.assertEqual(assertions[0]["notes"], rows[0]["notes"])
        self.assertTrue(all("rank" not in entry for entry in assertions))
        self.assertIsNone(result["dimensions"]["1.1-M1"]["HR0"])
        self.assertEqual(result["scenarios"]["HR0"]["scored_dimensions"], 0)

    def test_complete_scenarios_use_minima_flag_conflicts_and_compute_versioned_proxies(self):
        critical = next(row["subsystem_id"] for row in self.taxonomy if row["criticality"] == "critical")
        noncritical = next(row["subsystem_id"] for row in self.taxonomy if row["criticality"] != "critical")
        rows = []
        for subsystem in self.taxonomy:
            for metric in self.metrics:
                rows.append(self.row(subsystem["subsystem_id"], metric["metric_id"], "HR100", "5"))
                value = "2" if subsystem["subsystem_id"] == critical and metric["metric_id"] == "M1" else "4"
                if subsystem["subsystem_id"] == noncritical and metric["metric_id"] == "M1":
                    value = "0"
                rows.append(self.row(subsystem["subsystem_id"], metric["metric_id"], "HR0", value))
        rows.append(self.row(critical, "M1", "HR0", "3"))
        self.write(rows)
        result = scoring.build_scores(self.evidence)
        self.assertEqual(result["scenarios"]["HR0"]["observed_min"], 0)
        self.assertEqual(result["scenarios"]["HR0"]["critical_min"], 2)
        self.assertTrue(result["scenarios"]["HR0"]["complete"])
        self.assertEqual(result["scenarios"]["HR0"]["scored_subsystems"], 100)
        self.assertEqual(result["scenarios"]["HR0"]["scored_domains"], 10)
        self.assertEqual(result["subsystems"][critical]["HR0"], 2)
        self.assertEqual(result["domains"][noncritical.split(".")[0]]["HR0"], 0)
        self.assertEqual(result["proxies"]["C_proxy"], 0.4)
        self.assertAlmostEqual(result["proxies"]["H_proxy"], 0.6)
        self.assertEqual(result["conflicts"][0]["distinct_scores"], [2, 3])
        self.assertEqual(result["conflicts"][0]["selected_score"], 2)
        self.assertEqual(result["scenarios"]["HR0"]["conflict_dimensions"], 1)
        self.assertIsNone(result["proxies"]["R_M"])
        self.assertIsNone(result["proxies"]["g_0"])

    def test_critical_screening_can_be_complete_while_full_ontology_is_not(self):
        rows = [self.row(subsystem["subsystem_id"], metric["metric_id"], "HR0", "1") for subsystem in self.taxonomy if subsystem["criticality"] == "critical" for metric in self.metrics]
        self.write(rows)
        result = scoring.build_scores(self.evidence)
        self.assertTrue(result["scenarios"]["HR0"]["critical_complete"])
        self.assertFalse(result["scenarios"]["HR0"]["complete"])
        self.assertEqual(result["proxies"]["C_proxy"], 0.2)
        self.assertIsNone(result["proxies"]["H_proxy"])

    def test_zero_baseline_and_nonmonotonic_scenarios_leave_h_unknown(self):
        critical = [subsystem for subsystem in self.taxonomy if subsystem["criticality"] == "critical"]
        rows = [self.row(subsystem["subsystem_id"], metric["metric_id"], scenario, score) for subsystem in critical for metric in self.metrics for scenario, score in (("HR100", "0"), ("HR0", "2"))]
        self.write(rows)
        result = scoring.build_scores(self.evidence)
        self.assertIsNone(result["proxies"]["H_proxy"])
        self.assertIn("zero", result["proxy_explanations"]["H_proxy"])
        for row in rows:
            if row["human_removal_scenario"] == "HR100":
                row["score_0_5"] = "1"
        self.write(rows)
        result = scoring.build_scores(self.evidence)
        self.assertIsNone(result["proxies"]["H_proxy"])
        self.assertIn("monotonicity assumption failed", result["proxy_explanations"]["H_proxy"])
        self.assertTrue(result["diagnostics"])

    def test_other_years_and_evidence_after_cutoff_are_rejected(self):
        row = self.row()
        row.update(year="2025", as_of_date="2025-11-02", source_date="2025-10-01")
        self.write([row])
        with self.assertRaisesRegex(scoring.ValidationError, "differs from selected year"):
            scoring.build_scores(self.evidence)
        accepted = scoring.build_scores(self.evidence, year=2025, as_of="2025-11-02")
        self.assertEqual(accepted["input"]["year"], 2025)
        row.update(year="2026", as_of_date="2026-11-03", source_date="2026-10-01")
        self.write([row])
        with self.assertRaisesRegex(scoring.ValidationError, "after scoring cutoff"):
            scoring.build_scores(self.evidence)

    def test_invalid_csv_fails_before_existing_output_is_changed(self):
        self.evidence.write_text("bad,header\n", encoding="utf-8")
        output = Path(self.temp.name) / "scores.json"
        output.write_text("preserve existing analysis", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), "--evidence", str(self.evidence), "--output", str(output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected columns", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(output.read_text(), "preserve existing analysis")

    def test_curated_data_outputs_are_refused_in_an_isolated_checkout(self):
        isolated = Path(self.temp.name) / "checkout"
        (isolated / "scripts").mkdir(parents=True)
        ontology = isolated / "data" / "ontology"
        ontology.mkdir(parents=True)
        for filename in ("score_evidence.py", "validate_data.py", "paths.py"):
            shutil.copy2(ROOT / "scripts" / filename, isolated / "scripts" / filename)
        for filename in ("taxonomy.csv", "metrics.csv"):
            shutil.copy2(ROOT / "data" / "ontology" / filename, ontology / filename)
        self.write([])
        script = isolated / "scripts" / "score_evidence.py"
        for filename in ("taxonomy.csv", "metrics.csv"):
            output = ontology / filename
            original = output.read_bytes()
            result = subprocess.run([sys.executable, str(script), "--evidence", str(self.evidence), "--output", str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not overwrite curated data", result.stderr)
            self.assertEqual(output.read_bytes(), original)
        allowed = isolated / "data" / "editions" / "2026" / "analysis" / "scores.json"
        result = subprocess.run([sys.executable, str(script), "--evidence", str(self.evidence), "--output", str(allowed)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(allowed.is_file())

    def test_fingerprints_use_actual_custom_ontology_and_detect_criticality_change(self):
        data = Path(self.temp.name) / "custom-data"
        data.mkdir()
        for filename in ("taxonomy.csv", "metrics.csv"):
            shutil.copy2(ROOT / "data" / "ontology" / filename, data / filename)
        self.write([])
        first = scoring.build_scores(self.evidence, data_dir=data)
        self.assertEqual(first["input"]["taxonomy_sha256"], hashlib.sha256((data / "taxonomy.csv").read_bytes()).hexdigest())
        self.assertEqual(first["input"]["metrics_sha256"], hashlib.sha256((data / "metrics.csv").read_bytes()).hexdigest())
        with (data / "taxonomy.csv").open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        changed = next(row for row in rows if row["criticality"] == "high")
        changed["criticality"] = "critical"
        with (data / "taxonomy.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        second = scoring.build_scores(self.evidence, data_dir=data)
        self.assertNotEqual(first["input"]["taxonomy_sha256"], second["input"]["taxonomy_sha256"])
        self.assertEqual(first["input"]["metrics_sha256"], second["input"]["metrics_sha256"])
        self.assertEqual(second["totals"]["critical_dimensions"], first["totals"]["critical_dimensions"] + 10)

    def test_cli_writes_readable_json_and_refuses_to_overwrite_input(self):
        self.write([])
        output = Path(self.temp.name) / "analysis" / "scores.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "--evidence", str(self.evidence), "--output", str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(output.read_text())
        self.assertEqual(parsed["totals"]["dimensions"], 1000)
        self.assertEqual(len(parsed["input"]["evidence_sha256"]), 64)
        self.assertEqual(len(parsed["input"]["taxonomy_sha256"]), 64)
        self.assertEqual(len(parsed["input"]["metrics_sha256"]), 64)
        self.assertFalse(list(output.parent.glob(".scores-*.tmp")))
        original = self.evidence.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--evidence", str(self.evidence), "--output", str(self.evidence)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.evidence.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
