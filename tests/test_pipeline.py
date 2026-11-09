"""Verify the CSV-to-analysis-to-dashboard workflow without changing real data."""

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="mcab-pipeline-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "data"):
            shutil.copytree(ROOT / directory, self.root / directory)

    def run_script(self, script, *arguments, success=True):
        result = subprocess.run([sys.executable, str(self.root / "scripts" / script), *arguments], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_empty_evidence_preserves_manual_inputs_and_generates_unknowns(self):
        paths = (
            self.root / "data/ontology/taxonomy.csv",
            self.root / "data/ontology/metrics.csv",
            self.root / "data/ontology/dimensions.csv",
            self.root / "data/editions/2026/evidence.csv",
            self.root / "data/ontology/dependencies.csv",
        )
        before = {str(path): path.read_bytes() for path in paths}
        self.run_script("run_pipeline.py", "--skip-research")
        self.assertEqual(before, {str(path): path.read_bytes() for path in paths})
        scores = json.loads((self.root / "data/editions/2026/analysis/scores.json").read_text())
        self.assertEqual(len(scores["dimensions"]), 1000)
        self.assertTrue(all(value is None for values in scores["dimensions"].values() for value in values.values()))
        self.assertTrue(all(value is None for value in scores["proxies"].values()))
        dependencies = json.loads((self.root / "data/editions/2026/analysis/dependencies.json").read_text())
        self.assertEqual(dependencies["verified_edge_count"], 0)
        self.assertEqual(dependencies["possible_bottlenecks"], [])
        report = (self.root / "reports/2026/MCAB-2026-engineering.html").read_text()
        self.assertIn("未知", report)
        self.assertEqual(report.count('<section data-scenario="'), 5)

    def test_supplied_score_stays_local_and_stale_inputs_are_rejected(self):
        path = self.root / "data/editions/2026/evidence.csv"
        with path.open(encoding="utf-8-sig", newline="") as stream:
            fields = csv.DictReader(stream).fieldnames
        row = dict.fromkeys(fields, "")
        row.update(record_id="synthetic-test", year="2026", as_of_date="2026-11-02", domain_id="1", subsystem_id="1.1", metric_id="M1", human_removal_scenario="HR0", score_0_5="2", evidence_level="E0", confidence="Low", observed_capability="Synthetic fixture, not empirical evidence", notes="Test-only analyst inference")
        def write():
            with path.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
        write()
        self.run_script("run_pipeline.py", "--skip-research")
        scores = json.loads((self.root / "data/editions/2026/analysis/scores.json").read_text())
        self.assertEqual(scores["dimensions"]["1.1-M1"]["HR0"], 2)
        self.assertIsNone(scores["subsystems"]["1.1"]["HR0"])
        self.assertIsNone(scores["proxies"]["C_proxy"])
        report_path = self.root / "reports/2026/MCAB-2026-engineering.html"
        before = report_path.read_bytes()
        row["notes"] = "Changed source fixture after analysis"
        write()
        self.run_script("build_engineering_report.py", success=False)
        self.assertEqual(report_path.read_bytes(), before)

    def test_invalid_evidence_stops_before_overwriting_analysis(self):
        self.run_script("run_pipeline.py", "--skip-research")
        artifact = self.root / "data/editions/2026/analysis/scores.json"
        before = artifact.read_bytes()
        (self.root / "data/editions/2026/evidence.csv").write_text("broken,header\n")
        self.run_script("run_pipeline.py", "--skip-research", success=False)
        self.assertEqual(artifact.read_bytes(), before)

    def test_ontology_changes_and_curated_output_targets_are_rejected(self):
        self.run_script("run_pipeline.py", "--skip-research")
        path = self.root / "data/ontology/metrics.csv"
        before = path.read_bytes()
        self.run_script("build_engineering_report.py", "--output", str(path), success=False)
        self.assertEqual(path.read_bytes(), before)
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        rows[0]["definition"] += " (test revision)"
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        self.run_script("build_engineering_report.py", success=False)
        self.run_script("run_pipeline.py", "--skip-research")

    def test_other_year_cannot_be_presented_as_2026(self):
        self.run_script(
            "score_evidence.py",
            "--year", "2025",
            "--as-of", "2025-12-31",
            "--evidence", "data/editions/2026/evidence.csv",
            "--output", "data/editions/2026/analysis/scores.json",
        )
        self.run_script("analyze_dependencies.py", "--scores", "data/editions/2026/analysis/scores.json")
        self.run_script("build_engineering_report.py", success=False)

    def test_missing_dimensions_are_generated_and_research_rebuilds_without_cache(self):
        (self.root / "data/ontology/dimensions.csv").unlink()
        self.run_script("run_pipeline.py")
        with (self.root / "reports/2026/MCAB-2026-dimension-comparison.csv").open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len({row["dimension_id"] for row in rows}), 1000)
        self.assertFalse((self.root / ".research_cache").exists())


if __name__ == "__main__":
    unittest.main()
