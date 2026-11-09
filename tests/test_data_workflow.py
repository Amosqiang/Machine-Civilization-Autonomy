"""Exercise the public CSV workflow in isolated copies of the repository data."""

from __future__ import annotations

import csv
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class DataWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mcab-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ("data", "scripts"):
            shutil.copytree(ROOT / directory, self.root / directory)
        self.output = self.root / "data/ontology/dimensions.csv"
        self.output.unlink(missing_ok=True)

    def run_script(self, name, *arguments, success=True):
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts" / name), *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def read_csv(self, relative_path):
        with (self.root / relative_path).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            return reader.fieldnames, list(reader)

    def write_csv(self, relative_path, fields, rows):
        with (self.root / relative_path).open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def generate(self):
        self.run_script("generate_dimensions.py", "--force")

    def test_generation_is_complete_and_explicit_regeneration_is_deterministic(self):
        self.run_script("generate_dimensions.py")
        first = self.output.read_bytes()
        _, rows = self.read_csv("data/ontology/dimensions.csv")
        _, taxonomy = self.read_csv("data/ontology/taxonomy.csv")
        _, metrics = self.read_csv("data/ontology/metrics.csv")
        self.assertEqual(len(rows), 1000)
        self.assertEqual(
            {row["dimension_id"] for row in rows},
            {f"{subsystem['subsystem_id']}-{metric['metric_id']}"
             for subsystem in taxonomy for metric in metrics},
        )
        self.assertTrue(all(row["score_0_5"] == "" for row in rows))
        self.run_script("validate_data.py", "--require-dimensions")
        self.generate()
        self.assertEqual(self.output.read_bytes(), first)

    def test_default_generation_preserves_existing_scores_and_empty_files(self):
        self.generate()
        fields, rows = self.read_csv("data/ontology/dimensions.csv")
        rows[0]["score_0_5"] = "3"
        rows[0]["notes"] = "Human-entered evidence must survive."
        self.write_csv("data/ontology/dimensions.csv", fields, rows)
        for existing in (self.output.read_bytes(), b""):
            with self.subTest(existing_size=len(existing)):
                self.output.write_bytes(existing)
                self.run_script("generate_dimensions.py", success=False)
                self.assertEqual(self.output.read_bytes(), existing)

    def test_failed_atomic_replacement_preserves_original_and_cleans_temporary_file(self):
        self.generate()
        fields, rows = self.read_csv("data/ontology/dimensions.csv")
        rows[0]["notes"] = "Preserve this human-entered note if publication fails."
        self.write_csv("data/ontology/dimensions.csv", fields, rows)
        original = self.output.read_bytes()
        module_path = self.root / "scripts/generate_dimensions.py"
        spec = importlib.util.spec_from_file_location("mcab_generator_under_test", module_path)
        generator = importlib.util.module_from_spec(spec)
        # Import the copied sibling validator without leaving path/module changes.
        with mock.patch.object(sys, "path", [str(module_path.parent), *sys.path]):
            with mock.patch.dict(sys.modules):
                sys.modules.pop("validate_data", None)
                spec.loader.exec_module(generator)
        with mock.patch.object(generator, "OUTPUT", self.output):
            with mock.patch.object(generator.os, "replace", side_effect=OSError("simulated publication failure")) as replace:
                with self.assertRaises(OSError):
                    generator.write_rows(rows, force=True)
                replace.assert_called_once()
        self.assertEqual(self.output.read_bytes(), original)
        self.assertFalse(list(self.output.parent.glob(".dimensions-*.tmp")))

    def test_default_generation_preserves_dangling_symlink(self):
        target = self.root / "data/ontology/missing-target.csv"
        try:
            self.output.symlink_to(target)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"Symbolic links unavailable: {error}")
        self.run_script("generate_dimensions.py", success=False)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual(self.output.readlink(), target)
        self.assertFalse(target.exists())

    def test_invalid_inputs_cannot_overwrite_output_even_with_force(self):
        self.generate()
        original = self.output.read_bytes()
        cases = (
            ("data/ontology/taxonomy.csv", "missing", lambda rows: rows.pop()),
            ("data/ontology/taxonomy.csv", "duplicate", lambda rows: rows[1].update(subsystem_id=rows[0]["subsystem_id"])),
            ("data/ontology/taxonomy.csv", "domain mismatch", lambda rows: rows[0].update(domain_id="2")),
            ("data/ontology/metrics.csv", "duplicate", lambda rows: rows[1].update(metric_id=rows[0]["metric_id"])),
        )
        for path, problem, mutate in cases:
            with self.subTest(path=path, problem=problem):
                source = (self.root / path).read_bytes()
                fields, rows = self.read_csv(path)
                mutate(rows)
                self.write_csv(path, fields, rows)
                self.run_script("generate_dimensions.py", "--force", success=False)
                self.assertEqual(self.output.read_bytes(), original)
                self.assertFalse(list(self.output.parent.glob(".dimensions-*.tmp")))
                (self.root / path).write_bytes(source)

    def test_missing_dimensions_are_optional_unless_required(self):
        self.run_script("validate_data.py")
        self.run_script("validate_data.py", "--require-dimensions", success=False)
        self.assertFalse(self.output.exists())

    def test_invalid_dimensions_are_rejected_without_modification(self):
        self.generate()
        fields, baseline = self.read_csv("data/ontology/dimensions.csv")
        cases = (
            ("duplicate ID", lambda rows: rows[1].update(dimension_id=rows[0]["dimension_id"])),
            ("mismatched domain", lambda rows: rows[0].update(domain_id="2")),
            ("score without evidence", lambda rows: rows[0].update(score_0_5="0")),
            ("nonfinite confidence", lambda rows: rows[0].update(confidence_0_1="NaN")),
            ("out-of-range confidence", lambda rows: rows[0].update(confidence_0_1="1.1")),
            ("impossible date", lambda rows: rows[0].update(evidence_date="2026-02-30")),
            ("invalid score", lambda rows: rows[0].update(score_0_5="2.5")),
        )
        for problem, mutate in cases:
            with self.subTest(problem=problem):
                rows = [row.copy() for row in baseline]
                mutate(rows)
                self.write_csv("data/ontology/dimensions.csv", fields, rows)
                original = self.output.read_bytes()
                self.run_script("validate_data.py", success=False)
                self.assertEqual(self.output.read_bytes(), original)

    def test_supported_zero_score_is_distinct_from_unknown(self):
        self.generate()
        fields, rows = self.read_csv("data/ontology/dimensions.csv")
        rows[0].update(
            score_0_5="0", confidence_0_1="0.8", evidence_date="2026-10-01",
            evidence_type="E2", source="https://example.org/experiment",
        )
        self.write_csv("data/ontology/dimensions.csv", fields, rows)
        self.run_script("validate_data.py", "--require-dimensions")
        rows[0]["evidence_type"] = "E0"
        self.write_csv("data/ontology/dimensions.csv", fields, rows)
        self.run_script("validate_data.py", success=False)
        rows[0]["notes"] = "Analyst inference from the documented system boundary."
        self.write_csv("data/ontology/dimensions.csv", fields, rows)
        self.run_script("validate_data.py")

    def test_duplicate_evidence_schema_fields_are_rejected(self):
        fields, rows = self.read_csv("data/ontology/evidence_schema.csv")
        rows[1]["field"] = rows[0]["field"]
        self.write_csv("data/ontology/evidence_schema.csv", fields, rows)
        self.run_script("validate_data.py", success=False)

    def make_evidence(self):
        _, schema = self.read_csv("data/ontology/evidence_schema.csv")
        fields = [row["field"] for row in schema]
        row = dict.fromkeys(fields, "")
        row.update(
            record_id="example-2026-001", year="2026", as_of_date="2026-10-31",
            domain_id="1", subsystem_id="1.1", metric_id="M1",
            human_removal_scenario="HR0", score_0_5="1", evidence_level="E2",
            confidence="Low", observed_capability="Synthetic fixture; no empirical claim.",
            remaining_human_role="Fixture operator", failure_mode="Fixture limitation",
            single_point_of_failure="Unknown", source_title="Synthetic fixture",
            source_url="https://example.org/fixture", source_type="Paper",
            source_date="2026-09-01",
        )
        return fields, row

    def test_valid_evidence_supports_all_five_human_removal_scenarios(self):
        fields, row = self.make_evidence()
        records = []
        for scenario in ("HR100", "HR50", "HR10", "HR1", "HR0"):
            records.append(dict(row, record_id=f"example-{scenario}", human_removal_scenario=scenario))
        self.write_csv("data/editions/2026/_fixture_evidence.csv", fields, records)
        self.run_script("validate_data.py", "--evidence", "data/editions/2026/_fixture_evidence.csv")

    def test_invalid_evidence_is_rejected(self):
        fields, row = self.make_evidence()
        cases = (
            ("scenario", {"human_removal_scenario": "HR25"}),
            ("unknown subsystem", {"subsystem_id": "11.1"}),
            ("mismatched domain", {"domain_id": "2"}),
            ("unknown metric", {"metric_id": "M11"}),
            ("source after cutoff", {"source_date": "2026-11-01"}),
            ("missing source", {"source_url": ""}),
            ("E0 without rationale", {"evidence_level": "E0", "notes": ""}),
        )
        for problem, changes in cases:
            with self.subTest(problem=problem):
                self.write_csv("data/editions/2026/_fixture_evidence.csv", fields, [dict(row, **changes)])
                self.run_script("validate_data.py", "--evidence", "data/editions/2026/_fixture_evidence.csv", success=False)
        self.write_csv("data/editions/2026/_fixture_evidence.csv", fields, [row, row.copy()])
        self.run_script("validate_data.py", "--evidence", "data/editions/2026/_fixture_evidence.csv", success=False)


if __name__ == "__main__":
    unittest.main()
