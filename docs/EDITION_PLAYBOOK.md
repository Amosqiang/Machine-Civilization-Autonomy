# Edition Playbook — 年度 / 月度操作手册

Operational checklist for running MCAB until the host-independence threshold. Philosophy: [PHILOSOPHY.md](PHILOSOPHY.md). Rules: [CONTINUITY.md](CONTINUITY.md). Evidence acquisition method: [METHOD_LOOP.md](METHOD_LOOP.md).

## Before any change

1. Work on a branch; open a PR.
2. Do not rewrite published Git history.
3. Prefer additive evidence rows and forward corrections.
4. Keep `unknown` as blank — never invent zeros.

## Open a new annual edition

```sh
python3 scripts/new_edition.py --year 2027 --from-year 2026 --as-of 2027-10-31
python3 scripts/edition_status.py
```

This creates:

- `data/editions/2027/evidence.csv` (header-only)
- `research/`, `analysis/`, `reports/2027/`
- `MANIFEST.md`
- a new row in `data/editions/registry.csv`

Prior editions stay untouched.

## Monthly / interim update (same year)

Run inside the method loop (do not ad-hoc browse):

```sh
python3 scripts/build_target_queue.py --year YYYY
# acquire+verify top batch using data/method/source_playbooks.csv
python3 scripts/run_pipeline.py --year YYYY
python3 scripts/build_target_queue.py --year YYYY
python3 scripts/log_method_cycle.py --cycle YYYY-Cxx --summary "..."
```

1. Add or amend rows only in the current open edition’s `evidence.csv`.
2. Update the edition `as_of_date` in evidence rows and, if freezing an interim cut, in `registry.csv` + `MANIFEST.md`.
3. Note in `CHANGELOG.md` whether the delta is **capability**, **evidence**, **ontology**, or **assumption**.
4. Do not brand an interim scrape as a calibrated annual baseline.

## Freeze and release

1. Set final `as_of` and refuse later backfill into that freeze.
2. Run tests + pipeline; confirm curated inputs unchanged.
3. Update `CHANGELOG.md` and `data/threshold/STATUS.md` if aggregates moved.
4. Tag `mcab-YYYY` or `mcab-YYYY-rN`.
5. Set registry `status` to `frozen` then `released`.

## Threshold check

```sh
python3 scripts/edition_status.py
```

`data/threshold/STATUS.md` stays `not_met` until critical-path evidence supports C → 1, H → 0, R_M > 1, g_0 > 0 under declared HR0 conditions. Marking `met` requires a dedicated review PR — never automation alone.

## Issue templates

- Annual baseline work: use the **Annual baseline** template.
- Mid-year evidence movement: use the **Interim update** template.
- Single-source claims: continue using **Evidence submission**.
