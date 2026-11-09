"""Validate method-loop queue generation and cycle logging."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MethodLoopTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="mcab-method-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "data"):
            shutil.copytree(ROOT / directory, self.root / directory)

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

    def test_queue_rebuild_is_complete_and_preserves_locks(self):
        queue_path = self.root / "data/method/target_queue.csv"
        if queue_path.exists():
            queue_path.unlink()
        self.run_script("build_target_queue.py")
        with queue_path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 1000)
        self.assertEqual([int(row["priority"]) for row in rows[:3]], [1, 2, 3])
        # Prefer closure-heavy metrics among the head of the queue.
        head_metrics = {row["metric_id"] for row in rows[:20]}
        self.assertTrue(head_metrics & {"M10", "M5", "M4", "M9", "M8"})
        # Lock one target and ensure rebuild preserves it.
        rows[0]["status"] = "locked_deep_dive"
        rows[0]["lock_reason"] = "umbilical cord deep dive"
        rows[0]["notes"] = "keep"
        with queue_path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        self.run_script("build_target_queue.py")
        with queue_path.open(encoding="utf-8-sig", newline="") as stream:
            rebuilt = {row["dimension_id"]: row for row in csv.DictReader(stream)}
        locked = rebuilt[rows[0]["dimension_id"]]
        self.assertEqual(locked["status"], "locked_deep_dive")
        self.assertEqual(locked["lock_reason"], "umbilical cord deep dive")
        self.run_script("validate_method.py")

    def test_cycle_log_is_append_only(self):
        log_path = self.root / "data/method/cycle_log.csv"
        if log_path.exists():
            log_path.unlink()
        self.run_script("build_target_queue.py")
        self.run_script(
            "log_method_cycle.py",
            "--cycle", "2026-C99",
            "--summary", "test cycle",
            "--attempted", "3",
            "--verified", "1",
            "--ingested", "1",
            "--learning", "tighten queries",
        )
        self.run_script(
            "log_method_cycle.py",
            "--cycle", "2026-C99",
            "--summary", "duplicate",
            success=False,
        )
        with log_path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["cycle_id"], "2026-C99")


if __name__ == "__main__":
    unittest.main()
