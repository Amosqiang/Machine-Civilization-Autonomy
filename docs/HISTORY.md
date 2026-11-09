# MCAB Repository History — 结构演进记录

This file records **structural eras** of the repository so future maintainers can navigate refactors without losing the meaning of old paths. Commit-level detail lives in Git; this is the map legend.

## Era 0 — Framework bootstrap (2025–2026)

Initial commits on `main` established:

- public README and research framing;
- `data/taxonomy.csv`, `data/metrics.csv`;
- `scripts/generate_dimensions.py`;
- research protocol, roadmap, evidence schema;
- contribution guide, citation metadata, issue templates.

Flat `data/` layout; dimensions generated but scoring pipeline incomplete.

## Era 1 — 2026 evidence engineering

Branch `codex/mcab-2026-evidence-engineering` (merged into the long-horizon refactor base) added:

- protected dimension generation and validators;
- formal `evidence_2026.csv` template + conservative `mcab-proxy-v0.1` scoring;
- dependency schema/analysis;
- 2026 literature comparison JSON + reports;
- CI workflow and unittest suite;
- draft `docs/MCAB-v0.1.md` and development notes.

Paths remained flat (`data/evidence_2026.csv`, `data/analysis/2026/`, `data/research/2026/`).

## Era 2 — Long-horizon instrument layout (this refactor)

Goal: keep all prior commits, reorganize for multi-year/multi-month continuity until the host-independence threshold.

Canonical layout:

- `data/ontology/` — shared schemas and worksheets;
- `data/editions/<YYYY>/` — per-year evidence, research, analysis;
- `docs/PHILOSOPHY.md`, `docs/CONTINUITY.md` — constitutive rules;
- `scripts/paths.py` — single path registry;
- `CHANGELOG.md` — human-facing edition notes.

No force-push rewrite of Era 0/1 history. File moves use Git renames so blame and prior PRs remain recoverable.

## Era 3 — Method loop for frontier acquisition

Added a closed-loop research method for multi-domain, latest-tech evidence:

- `docs/METHOD_LOOP.md`
- `data/method/` (`source_playbooks.csv`, `target_queue.csv`, `cycle_log.csv`)
- `scripts/build_target_queue.py`, `log_method_cycle.py`, `validate_method.py`

Bootstrap cycle `2026-C00` records method establishment; subsequent cycles acquire evidence against the ranked queue.
