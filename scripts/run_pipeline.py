#!/usr/bin/env python3
"""Validate inputs and rebuild analysis/reports without overwriting manual data."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-research", action="store_true", help="rebuild only CSV engineering analysis, not the separate literature report")
    args = parser.parse_args()
    commands = []
    if not (ROOT / "data/dimensions.csv").exists():
        commands.append(("generate_dimensions.py",))
    commands.extend([
        ("validate_data.py", "--require-dimensions", "--evidence", "data/evidence_2026.csv"),
        ("score_evidence.py",),
        ("analyze_dependencies.py", "--scores", "data/analysis/2026/scores.json"),
        ("build_engineering_report.py",),
    ])
    if not args.skip_research:
        commands.append(("build_2026_report.py",))
    try:
        for name, *arguments in commands:
            subprocess.run([sys.executable, str(ROOT / "scripts" / name), *arguments], cwd=ROOT, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Pipeline stopped: {error}", file=sys.stderr)
        return 1
    print("Pipeline complete. Manual CSV inputs were preserved; unknowns were not assigned scores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
