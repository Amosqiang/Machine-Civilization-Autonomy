"""Contract and rendering checks for the research comparison report."""

from __future__ import annotations

import copy
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_2026_report.py"
SPEC = importlib.util.spec_from_file_location("build_2026_report", SCRIPT)
report = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(SCRIPT.parent))
try:
    SPEC.loader.exec_module(report)
finally:
    sys.path.pop(0)


class ReportContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mcab-report-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        cache = self.root / ".research_cache"
        cache.mkdir()
        (cache / "source.txt").write_text("The robot can perform\n  a limited demonstrated task. Human service remains necessary.", encoding="utf-8")
        self.expected = {}
        for metric in ("M1", "M2"):
            identifier = f"1.1-{metric}"
            self.expected[identifier] = dict(dimension_id=identifier, domain_id="1", domain="测试系统", subsystem_id="1.1", subsystem="测试子系统", metric_id=metric, metric="测试指标", test_question="是否具备该能力？", criticality="high")
        self.document = dict(
            as_of_date="2026-11-02", domain_ids=["1"],
            sources=[dict(source_id="D01-S01", title="A verified <source>", url="https://example.org/research", publisher="Research Institute", publication_date="2026-10-01", retrieved_at="2026-11-02", source_type="Paper", supporting_excerpt="The robot can perform a limited demonstrated task.", verification="full_text", cache_path=".research_cache/source.txt", limitations="仅有限任务，不证明闭环。")],
            records=[dict(dimension_id=identifier, required_capability="特定目标能力", current_capability="局部任务已演示", gap="仍依赖人类维护", assessment_status="partial_related_evidence", evidence_relation="partial_metric", source_ids=["D01-S01"], human_dependency="人工维修", validation_needed="库存耗尽后的长期无人测试", confidence="Medium") for identifier in self.expected],
            domain_summaries=[dict(domain_id="1", summary="局部能力进展。", strongest_progress="有限演示。", principal_gap="闭环未确立。")],
            search_log=[dict(query="robot autonomy test", retrieved_at="2026-11-02", note="定向检索，非穷尽。")],
        )
        self.path = self.root / "research.json"

    def validate(self, document=None):
        self.path.write_text(json.dumps(document or self.document, ensure_ascii=False), encoding="utf-8")
        return report.validate_research_files(self.root, [self.path], self.expected, verify_cache=True)

    def test_complete_explicit_grid_and_whitespace_normalized_excerpt(self):
        bundle = self.validate()
        self.assertEqual([r["dimension_id"] for r in bundle["records"]], list(self.expected))
        self.assertEqual(len(bundle["sources"]), 1)

    def test_production_grid_is_exact_and_rejects_invalid_ontology(self):
        source_root = SCRIPT.parents[1]
        self.assertEqual(len(report.load_expected_grid(source_root)), 1000)
        ontology = self.root / "data" / "ontology"
        ontology.mkdir(parents=True)
        for name in ("taxonomy.csv", "metrics.csv"):
            shutil.copy2(source_root / "data" / "ontology" / name, ontology / name)
        taxonomy = ontology / "taxonomy.csv"
        with taxonomy.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            rows = list(reader)
        rows[0]["subsystem_id"] = "11.1"
        with taxonomy.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(report.ReportError, "100 subsystem IDs"):
            report.load_expected_grid(self.root)

    def test_rebuild_without_private_source_cache(self):
        (self.root / ".research_cache/source.txt").unlink()
        self.path.write_text(json.dumps(self.document), encoding="utf-8")
        bundle = report.validate_research_files(self.root, [self.path], self.expected)
        self.assertFalse(bundle["cache_verified"])
        self.assertEqual(len(bundle["records"]), 2)
        with self.assertRaisesRegex(report.ReportError, "unreadable cache"):
            report.validate_research_files(self.root, [self.path], self.expected, verify_cache=True)

    def test_missing_dimension_rejected(self):
        self.document["records"].pop()
        with self.assertRaisesRegex(report.ReportError, "Missing 1 dimensions"):
            self.validate()

    def test_duplicate_dimension_rejected(self):
        self.document["records"].append(copy.deepcopy(self.document["records"][0]))
        with self.assertRaisesRegex(report.ReportError, "Duplicate dimension"):
            self.validate()

    def test_undeclared_source_rejected(self):
        self.document["records"][0]["source_ids"] = ["D01-S99"]
        with self.assertRaisesRegex(report.ReportError, "undeclared source_ids"):
            self.validate()

    def test_unverified_excerpt_rejected(self):
        self.document["sources"][0]["supporting_excerpt"] = "A statement not found in the source."
        with self.assertRaisesRegex(report.ReportError, "absent from cached"):
            self.validate()

    def test_cache_path_escape_rejected(self):
        self.document["sources"][0]["cache_path"] = ".research_cache/../../outside.txt"
        with self.assertRaisesRegex(report.ReportError, "escapes the research cache"):
            self.validate()

    def test_synthesis_requires_declared_sources_and_renders_as_analysis(self):
        bundle = self.validate()
        path = self.root / "synthesis.json"
        synthesis = dict(overall_assessment="分析：闭环尚未确立。", findings=[dict(title="关键观察", text="仅局部能力已有证据。", source_ids=["D01-S01"])], next_steps=["开展长期无人测试。"])
        path.write_text(json.dumps(synthesis), encoding="utf-8")
        report.attach_synthesis(bundle, path)
        self.assertIn("分析性综合", report.html_report(bundle))
        self.assertIn("关键观察", report.markdown_report(bundle))
        synthesis["findings"][0]["source_ids"] = ["D01-S99"]
        path.write_text(json.dumps(synthesis), encoding="utf-8")
        with self.assertRaisesRegex(report.ReportError, "declared source_ids"):
            report.attach_synthesis(bundle, path)

    def test_future_publication_rejected_and_unknown_date_permitted(self):
        self.document["sources"][0]["publication_date"] = "2026-11-03"
        with self.assertRaisesRegex(report.ReportError, "after as_of_date"):
            self.validate()
        self.document["sources"][0]["publication_date"] = ""
        self.assertEqual(len(self.validate()["records"]), 2)

    def test_blank_required_fields_and_unsupported_positive_claim_rejected(self):
        self.document["records"][0]["human_dependency"] = "  "
        with self.assertRaisesRegex(report.ReportError, "human_dependency"):
            self.validate()
        self.document["records"][0]["human_dependency"] = "人工维护"
        self.document["records"][0]["source_ids"] = []
        with self.assertRaisesRegex(report.ReportError, "requires a source"):
            self.validate()

    def test_ontology_identity_cannot_be_overwritten(self):
        self.document["records"][0]["subsystem_id"] = "2.1"
        with self.assertRaisesRegex(report.ReportError, "disagrees with the ontology"):
            self.validate()

    def test_outputs_escape_html_keep_full_fields_and_bom_csv(self):
        bundle = self.validate()
        output = self.root / "report"
        paths = report.write_reports(bundle, output)
        self.assertEqual(len(paths), 4)
        html_text = (output / "MCAB-2026-latest.html").read_text()
        self.assertIn("A verified &lt;source&gt;", html_text)
        self.assertIn('id="source-D01-S01"', html_text)
        self.assertIn('id="source-query"', html_text)
        self.assertIn('data-map-domain="1" data-map-metric="M1"', html_text)
        self.assertIn("证据覆盖≠自主性得分", html_text)
        self.assertIn('id="relation"', html_text)
        self.assertIn("库存耗尽后的长期无人测试", html_text)
        self.assertIn("@media print", html_text)
        csv_path = output / "MCAB-2026-dimension-comparison.csv"
        self.assertTrue(csv_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["source_urls"], "https://example.org/research")
        self.assertTrue(set(report.IDENTITY_FIELDS).issubset(rows[0]))
        appendix = (output / "MCAB-2026-dimensions.md").read_text()
        for identifier in self.expected:
            self.assertIn(identifier, appendix)
        self.assertFalse(list(output.glob(".mcab-*.tmp")))


if __name__ == "__main__":
    unittest.main()
