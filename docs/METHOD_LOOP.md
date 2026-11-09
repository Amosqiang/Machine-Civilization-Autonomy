# MCAB Method Loop — 前沿多行业证据获取回环

MCAB spans ten industrial domains. Relevant evidence is often **frontier** (latest papers, field pilots, vendor tech reports) and sometimes requires **deep domain reading**, not a single Google query. This document fixes the **acquisition method**, not one-off searches.

Related: [PHILOSOPHY.md](PHILOSOPHY.md) · [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) · [EDITION_PLAYBOOK.md](EDITION_PLAYBOOK.md) · [CONTINUITY.md](CONTINUITY.md)

## 1. Why a loop

Scattered browsing fails because:

1. domains are heterogeneous (semiconductors ≠ energy ≠ machine economy);
2. the useful frontier moves monthly;
3. demos are abundant while **HR0 / physical-closure** evidence is scarce;
4. without feedback, teams re-search easy AI headlines and ignore umbilical cords.

The loop forces: **select scarce bottlenecks → search with domain playbooks → verify against HR protocol → ingest without inventing scores → re-rank from new gaps**.

## 2. The six stages

```text
┌──────────────┐
│ 1. SELECT    │  build prioritized target queue from gaps + criticality
└──────┬───────┘
       ▼
┌──────────────┐
│ 2. ACQUIRE   │  domain source playbooks; frontier + primary sources
└──────┬───────┘
       ▼
┌──────────────┐
│ 3. VERIFY    │  date, scope, HR relevance, physical vs digital, E-level
└──────┬───────┘
       ▼
┌──────────────┐
│ 4. INGEST    │  evidence.csv and/or research JSON; never invent scores
└──────┬───────┘
       ▼
┌──────────────┐
│ 5. MEASURE   │  pipeline + edition_status + queue regeneration
└──────┬───────┘
       ▼
┌──────────────┐
│ 6. LEARN     │  cycle_log: what moved, what failed, next batch size
└──────┬───────┘
       └──────────► back to SELECT
```

Each full pass is one **method cycle** (`cycle_id`, e.g. `2026-C01`). Monthly interim updates should still run inside this loop; annual baselines are a freeze of many cycles.

## 3. SELECT — target formation

### Inputs

- ontology criticality (`data/ontology/taxonomy.csv`);
- latest research relations (`data/editions/<Y>/research/`);
- formal evidence coverage (`evidence.csv`);
- dependency hypotheses (`dependencies.csv`);
- synthesis `next_steps` (advisory, not automatic scores).

### Ranking principles (v0)

Higher priority when:

1. subsystem `criticality = critical`;
2. metric is closure-heavy: **M10 > M5 > M4 > M9 > M8 > others**;
3. evidence relation is weak: **no_direct_evidence > context_only > partial_metric > direct_metric**;
4. no formal evidence row yet for that dimension×HR0;
5. upstream of many dependency edges (structural exposure).

Tool: `python3 scripts/build_target_queue.py`  
Output: `data/method/target_queue.csv` (regenerable; curated overrides via `status`/`lock_reason` columns preserved when present).

Default batch for one cycle: **top 20 unlocked targets** (override with `--limit`).

## 4. ACQUIRE — frontier search playbooks

Do **not** use one generic query for all domains. Use `data/method/source_playbooks.csv`:

| Domain family | Prefer | Distrust alone |
| --- | --- | --- |
| AI / software / R&D | eval suites, reproducible papers, infra docs | model cards, demo videos |
| Energy / materials / manufacturing / semis / robotics | peer-reviewed + plant/field reports, standards, regulator/technical docs | marketing pages |
| Machine economy | central-bank / clearing / standards docs | crypto hype threads |
| Reproduction / ISRU | NASA/ESA technical reports, full methods sections | concept art / press-only |

For each target, record in the cycle worksheet:

- query intent tied to `required_capability` / `validation_needed`;
- at least one **primary** candidate URL/DOI;
- publication or observation date;
- whether the claim is digital-only or touches physical metabolism.

## 5. VERIFY — before ingest

Checklist (fail → do not raise autonomy score):

1. Source date ≤ edition `as_of` (or mark interim).
2. System boundary / human role / stockpile disclosed or explicitly unknown.
3. Claim maps to the **metric** (M4 repair ≠ M1 run).
4. Digital self-copy ≠ industrial reproduction.
5. Evidence level honest (demo → ≤ E2; vendor claim alone → ≤ E1).
6. Conflicts retained, not cherry-picked.

## 6. INGEST — write without false precision

- Formal rows → `data/editions/<Y>/evidence.csv` (23-field schema).
- Literature contrast updates → research JSON + rebuild report.
- Leave `score_0_5` blank unless an analyst explicitly scores.
- Link research source ids in `notes` when helpful.

## 7. MEASURE & LEARN

```sh
python3 scripts/run_pipeline.py --year YYYY
python3 scripts/build_target_queue.py --year YYYY
python3 scripts/edition_status.py
python3 scripts/log_method_cycle.py --cycle 2026-C01 --summary "..."
```

`data/method/cycle_log.csv` must state:

- targets attempted / verified / ingested;
- dimensions whose relation or formal coverage improved;
- search failures (so the next cycle does not repeat blind spots);
- whether the batch should shrink/expand.

## 8. Cadence mapping

| Cadence | Loop usage |
| --- | --- |
| Monthly interim | 1–N cycles; update queue + evidence; no fake annual freeze |
| Annual baseline | freeze `as_of` after enough cycles; tag edition |
| Deep-dive spike | lock a critical umbilical cord in the queue (`status=locked_deep_dive`) |

## 9. Anti-patterns

- Chasing only LLM agent leaderboard news.
- Filling zeros for missing industry evidence.
- Treating partial software autonomy as semiconductor/energy closure.
- Regenerating the queue and wiping analyst locks.
- Declaring threshold progress without critical-path movement.

## 10. Success of the *method* (not of civilization autonomy)

The method is working when each cycle:

1. spends most effort on high-priority gaps;
2. increases **verified primary sources** or explicit unknowns;
3. changes the queue ordering for the next cycle;
4. leaves Git-reproducible artifacts (`target_queue`, `cycle_log`, evidence diffs).
