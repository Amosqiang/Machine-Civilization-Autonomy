#!/usr/bin/env python3
"""Validate inputs and rebuild analysis/reports without overwriting manual data."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from paths import DEFAULT_YEAR, dependencies_json, dimensions_csv, evidence_csv, scores_json

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-research", action="store_true", help="rebuild only CSV engineering analysis, not the separate literature report")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help="edition year under data/editions/<year>/")
    args = parser.parse_args()
    year = args.year
    evidence = evidence_csv(year).relative_to(ROOT).as_posix()
    scores = scores_json(year).relative_to(ROOT).as_posix()
    commands = []
    if not dimensions_csv().exists():
        commands.append(("generate_dimensions.py",))
    commands.extend([
        ("validate_data.py", "--require-dimensions", "--evidence", evidence),
        ("score_evidence.py", "--year", str(year), "--evidence", evidence, "--output", scores),
        ("analyze_dependencies.py", "--scores", scores, "--output", dependencies_json(year).relative_to(ROOT).as_posix()),
        ("build_engineering_report.py", "--year", str(year)),
    ])
    if not args.skip_research:
        if year != DEFAULT_YEAR:
            print(f"Pipeline stopped: literature rebuild currently supports {DEFAULT_YEAR} only", file=sys.stderr)
            return 1
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
