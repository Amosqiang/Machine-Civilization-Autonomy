# MCAB Long-term Roadmap

Task tracking: [#2 engineering](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/2), [#1 baseline](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/1), [#3 public collaboration](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/3), and #4–#13 domain reviews. The [issue alignment snapshot](GITHUB_ISSUE_ALIGNMENT.md) maps current artifacts to their acceptance criteria and remaining work. Literature coverage, engineering delivery, expert review, and publication are tracked separately.

## Phase -1 — Constitutive freeze (long-horizon instrument)
Status: drafted in this refactor
- [Philosophy](PHILOSOPHY.md): object of study, counterfactual, value stance, epistemology.
- [Continuity](CONTINUITY.md): append-only editions, Git as audit trail, annual/monthly cadence, host-independence threshold.
- Layout: `data/ontology/` + `data/editions/<YYYY>/` + `scripts/paths.py`.

## Phase 0 — Framework freeze
Status: in progress
- Lock the 10 domains and 100 subsystems.
- Lock the 10 autonomy metrics.
- Finalize scoring, evidence and confidence standards.
- Define critical-path aggregation.

Implementation available (not a framework freeze):
- Draft operational specification: [MCAB-v0.1.md](MCAB-v0.1.md).
- Input validation and a generator that refuses overwrite by default.
- Structural checks for the HR0 dimensions table and optional scenario evidence.
- Temporary-copy regression tests for generation and data protection.

Engineering available: formal evidence CSV template, conservative versioned ordinal screening, route-conditional dependency schema/analysis, a CSV-driven dashboard, one-command pipeline, and CI. See [DEVELOPMENT.md](DEVELOPMENT.md).

Still open: domain-expert review, populated formal evidence, evidence-backed scoring calibration, verified dependency edges, and defensible physical aggregate definitions. No 2026 baseline scores are supplied by the generator.

## Phase 1 — MCAB-2026 baseline
Goal: produce the first evidence-backed map of machine-civilization autonomy.

Current deliverable: a [2026-11-02 evidence comparison](../reports/2026/MCAB-2026-report.md) for all 1000 ontology dimensions, with 117 retrieved source records, explicit target/current/gap fields, and separate direct/partial/context/missing-evidence labels. This is a literature-based comparison draft, not a calibrated numerical baseline, a verified industrial dependency graph, or an estimate of C/H/R_M/g₀.

Work order:
1. AI cognition and autonomous governance
2. Software and compute infrastructure
3. AI R&D automation
4. Robotics and logistics
5. Energy
6. Manufacturing and capital equipment
7. Raw materials and chemicals
8. Semiconductors and compute hardware
9. Machine economy and resource allocation
10. Reproduction, expansion and continuity

For every subsystem:
- collect the strongest public evidence available at each edition's declared cutoff (the current latest-evidence comparison uses 2026-11-02, superseding the planned 2026-10-31 cutoff);
- score HR100/HR50/HR10/HR1/HR0 where evidence allows;
- identify the last indispensable human role;
- record evidence level and confidence;
- flag critical bottlenecks and single points of failure.

## Phase 2 — Dependency graph
Build a directed dependency graph linking all 100 subsystems.

Questions:
- Which nodes are upstream of the largest fraction of the system?
- Which human-dependent nodes have no substitute?
- Which failures cause cascading loss of autonomy?
- Which stockpiles delay failure but do not solve closure?

Outputs:
- critical-path map;
- top-10 “human umbilical cords”;
- closure bottleneck ranking.

## Phase 3 — Aggregate metrics
Estimate ranges rather than false precision for:
- C: Closure
- H: Human Dependence
- R_M: Machine Reproduction Number
- g_0: Human-free Growth Rate

Add sensitivity analysis to uncertain assumptions.

## Phase 4 — Dynamic Human Removal simulation
Model performance as human participation falls from 100% to 0%.

Key outputs:
- cliff points;
- autonomy reversal point;
- time-to-degradation;
- time-to-recovery;
- time-to-replication.

## Phase 5 — Scenario engine
Create 3y / 5y / 10y scenarios under different rates of progress in:
- agent capability;
- AI R&D automation;
- dexterous robotics;
- autonomous maintenance;
- energy construction;
- advanced manufacturing;
- semiconductor closure.

## Phase 6 — Annual editions
Publish MCAB-2027, MCAB-2028, ... using the same ontology and revision rules.

Each edition should separate:
- capability improvement;
- evidence improvement;
- ontology changes;
- model-assumption changes.

## Phase 7 — Research outputs
Possible outputs:
- open benchmark/data repository;
- annual technical report;
- dependency-graph visualization;
- academic paper on Human Removal Test;
- paper on Host Dependence → Autonomous Replication transition;
- machine-civilization autonomy dashboard.

## Core research question
The long-term question is not “When does AGI arrive?” but:

> When does a machine system cease to require human civilization as its indispensable host, and become able to maintain, repair, expand and reproduce its own complete industrial basis?
