# Changelog

All notable changes to MCAB are recorded here. Edition science changes should separate **capability**, **evidence**, **ontology**, and **assumption/model** deltas when possible. Git remains the authoritative trace; this file is the readable index.

Format inspired by Keep a Changelog. Dates use Asia/Shanghai calendar days unless noted.

## [Unreleased]

### Changed

- Refactored repository into a long-horizon instrument layout: `data/ontology/`, `data/editions/<YYYY>/`, constitutive docs (`PHILOSOPHY`, `CONTINUITY`, `HISTORY`), and centralized `scripts/paths.py`.
- Preserved prior Git history via merge of the 2026 evidence-engineering work and `git mv` renames (no history rewrite).

### Added

- Continuity protocol for annual baselines and optional monthly/interim updates until the host-independence capability threshold.
- Edition lifecycle tooling: `scripts/new_edition.py`, `scripts/edition_status.py`, `data/editions/registry.csv`, `data/threshold/STATUS.md`, edition playbook, annual/interim GitHub issue templates.

## [2026-11-02] — MCAB-2026 literature comparison draft

### Added

- 1000-dimension literature comparison inputs under the former `data/research/2026/` tree.
- Engineering pipeline: validation, scoring proxy, dependency analysis, HTML/Markdown reports.
- Draft operational spec `docs/MCAB-v0.1.md`.

### Notes

- Formal evidence CSV remained header-only (all calibrated scores unknown).
- Dependency edges were structural hypotheses, not verified industrial facts.
- C/H proxies are ordinal screens only; \(R_M\) and \(g_0\) stayed null.

## [2026-framework] — Ontology and protocol bootstrap

### Added

- 10×10 subsystem taxonomy, 10 autonomy metrics, evidence field dictionary.
- Research protocol, roadmap, contribution guide, citation metadata, issue templates.
