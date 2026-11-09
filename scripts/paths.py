#!/usr/bin/env python3
"""Canonical filesystem layout for the long-horizon MCAB instrument."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ONTOLOGY = DATA / "ontology"
EDITIONS = DATA / "editions"
REPORTS = ROOT / "reports"
DEFAULT_YEAR = 2026


def ontology_dir() -> Path:
    return ONTOLOGY


def taxonomy_csv() -> Path:
    return ONTOLOGY / "taxonomy.csv"


def metrics_csv() -> Path:
    return ONTOLOGY / "metrics.csv"


def evidence_schema_csv() -> Path:
    return ONTOLOGY / "evidence_schema.csv"


def dimensions_csv() -> Path:
    return ONTOLOGY / "dimensions.csv"


def dependencies_csv() -> Path:
    return ONTOLOGY / "dependencies.csv"


def edition_dir(year: int = DEFAULT_YEAR) -> Path:
    return EDITIONS / str(year)


def evidence_csv(year: int = DEFAULT_YEAR) -> Path:
    return edition_dir(year) / "evidence.csv"


def research_dir(year: int = DEFAULT_YEAR) -> Path:
    return edition_dir(year) / "research"


def analysis_dir(year: int = DEFAULT_YEAR) -> Path:
    return edition_dir(year) / "analysis"


def scores_json(year: int = DEFAULT_YEAR) -> Path:
    return analysis_dir(year) / "scores.json"


def dependencies_json(year: int = DEFAULT_YEAR) -> Path:
    return analysis_dir(year) / "dependencies.json"


def reports_dir(year: int = DEFAULT_YEAR) -> Path:
    return REPORTS / str(year)


def editions_registry_csv() -> Path:
    return EDITIONS / "registry.csv"


def threshold_status_md() -> Path:
    return DATA / "threshold" / "STATUS.md"


def edition_manifest(year: int = DEFAULT_YEAR) -> Path:
    return edition_dir(year) / "MANIFEST.md"


def _parts_under(path: Path, root: Path) -> tuple[str, ...] | None:
    """Return relative parts for path under root, trying resolve then abspath."""
    import os

    candidates = (
        (path.resolve(), root.resolve()),
        (Path(os.path.abspath(path)), Path(os.path.abspath(root))),
    )
    for candidate, base in candidates:
        try:
            return candidate.relative_to(base).parts
        except ValueError:
            continue
    return None


def is_analysis_output(path: Path) -> bool:
    """True when path is under an edition analysis directory (writable by tools)."""
    parts = _parts_under(path, EDITIONS)
    return parts is not None and len(parts) >= 2 and parts[1] == "analysis"


def is_curated_data(path: Path) -> bool:
    """True for ontology or non-analysis edition inputs that tools must not overwrite."""
    if _parts_under(path, DATA) is None:
        return False
    return not is_analysis_output(path)
