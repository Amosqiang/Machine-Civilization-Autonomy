# MCAB Continuity Protocol — 长期连续性协议

This repository is designed to run for years — annually/editions may update monthly, baselines annually — until the host-independence capability threshold is reached. Continuity means: **structure may be refactored; history must remain reconstructible.**

## 1. Immutable commitments

1. **Never rewrite published history.** Do not force-push over shared main history to erase editions, evidence, or mistaken scores. Correct forward with new commits, errata, or superseding edition tags.
2. **Git is the audit trail.** Every ontology change, evidence row, score revision, and report rebuild should be reviewable as commits/PRs.
3. **Editions are append-only snapshots.** MCAB-2026 remains readable after MCAB-2027 exists. Later editions may disagree with earlier ones; they must not silently overwrite them.
4. **Ontology identity is sticky.** Changing `subsystem_id` / `metric_id` requires an explicit migration note and edition bump; do not silently renumber history.
5. **Unknown stays unknown.** Pipeline tools must not invent scores to “complete” a release.

## 2. Repository layout

| Path | Role |
| --- | --- |
| `data/ontology/` | Living ontology + HR0 worksheet templates (`taxonomy`, `metrics`, `evidence_schema`, `dimensions`, `dependencies`). |
| `data/editions/<YYYY>/` | Year edition: formal `evidence.csv`, `research/`, generated `analysis/`. |
| `reports/<YYYY>/` | Human-readable reports for that edition. |
| `docs/` | Philosophy, protocol, specs, roadmap, continuity. |
| `scripts/` | Stdlib-only tooling; paths centralized in `scripts/paths.py`. |
| `CHANGELOG.md` | Human summary of material changes across editions. |
| `docs/HISTORY.md` | Lineage of structural eras and preserved branches. |

Legacy flat paths under `data/*.csv` are retired by this restructure. File history remains in Git via `git mv` and prior commits.

## 3. Cadence

### Annual baseline (required)

Each year `Y` publishes `MCAB-Y` with:

1. declared evidence cutoff (`as_of_date`);
2. formal evidence CSV under `data/editions/Y/evidence.csv`;
3. regenerated analysis + reports;
4. changelog entry separating capability / evidence / ontology / assumption deltas vs prior year;
5. explicit statement of what remains unknown.

### Monthly or interim updates (optional)

Use when strong public evidence moves a bottleneck, without waiting for year-end:

- prefer additive evidence rows and dated report regenerations;
- keep the same baseline year until the annual cutover;
- label interim products clearly (e.g. `as_of` in report headers);
- do not pretend an interim scrape is a calibrated annual baseline.

## 4. Edition lifecycle

1. **Open** — create `data/editions/<YYYY>/` from the prior edition template (header-compatible evidence schema).
2. **Fill** — add evidence; domain reviews; dependency verification.
3. **Freeze cutoff** — set `as_of`; reject later-dated backfill into that freeze.
4. **Build** — `python3 scripts/run_pipeline.py` (or year-scoped flags when added).
5. **Release** — tag `mcab-<YYYY>` (or `mcab-<YYYY>-rN` for corrected releases); update `CHANGELOG.md`.
6. **Supersede, don’t delete** — later corrections ship as `rN+1` or next edition.

## 5. Threshold — “那一天”

The program’s stopping criterion is **capability**, not demographic absence of humans:

> Under a declared system boundary and HR0 conditions, the machine industrial basis can operate, diagnose, repair, secure critical inputs and energy, recover from disruption, expand capacity, and reproduce an equivalent successor system — with critical-path closure supporting C → 1, H → 0, \(R_M\) > 1, \(g_0\) > 0 at stated confidence.

Until that threshold is evidenced — possibly across many annual editions — MCAB continues. Reaching the threshold ends the “host dependence measurement” primary arc; archival and monitoring editions may still continue.

## 6. Refactors

Full structural refactors are allowed when they improve continuity, provided:

1. they happen on branches merged through normal review;
2. they use `git mv` / additive history rather than deleting the past;
3. `docs/HISTORY.md` records why the layout changed;
4. scripts resolve paths through `scripts/paths.py`;
5. CI and tests pass on the new layout before merge.

## 7. Contribution rule of thumb

If a change would make last year’s claims unreproducible from Git, it is the wrong change. Fix forward; annotate; keep the cord of evidence intact.
