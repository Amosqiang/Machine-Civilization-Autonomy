"""Exercise annual edition scaffolding and status reporting."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EditionToolingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="mcab-edition-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "data"):
            shutil.copytree(ROOT / directory, self.root / directory)
        # Drop generated analysis noise for clearer scaffolding assertions.
        analysis = self.root / "data/editions/2026/analysis"
        for path in analysis.glob("*.json"):
            path.unlink()

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

    def test_status_reports_2026_and_threshold_not_met(self):
        result = self.run_script("edition_status.py", "--require-threshold-not-met")
        self.assertIn("2026", result.stdout)
        self.assertIn("status=not_met", result.stdout)

    def test_new_edition_is_append_only_and_refuses_clobber(self):
        self.run_script("new_edition.py", "--year", "2027", "--from-year", "2026", "--as-of", "2027-10-31")
        edition = self.root / "data/editions/2027"
        self.assertTrue((edition / "evidence.csv").is_file())
        self.assertTrue((edition / "MANIFEST.md").is_file())
        self.assertTrue((edition / "research").is_dir())
        self.assertTrue((edition / "analysis").is_dir())
        self.assertTrue((self.root / "reports/2027").is_dir())
        with (edition / "evidence.csv").open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(rows, [])
        # Prior edition evidence untouched.
        prior = (self.root / "data/editions/2026/evidence.csv").read_bytes()
        self.assertTrue(prior.startswith(b"\xef\xbb\xbf") or prior.startswith(b"record_id"))
        with (self.root / "data/editions/registry.csv").open(encoding="utf-8-sig", newline="") as stream:
            years = [row["year"] for row in csv.DictReader(stream)]
        self.assertEqual(years, ["2026", "2027"])
        self.run_script("new_edition.py", "--year", "2027", "--from-year", "2026", success=False)
        self.run_script("edition_status.py")


if __name__ == "__main__":
    unittest.main()
