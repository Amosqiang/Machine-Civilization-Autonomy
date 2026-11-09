# Contributing to MCAB

MCAB is an open research benchmark for measuring how far AI–robotics–industrial systems can continue operating, repairing, expanding, and reproducing as human support is progressively removed.

We welcome contributions from AI researchers, roboticists, industrial engineers, semiconductor specialists, energy researchers, economists, systems researchers, historians of technology, and practitioners with domain expertise.

## High-value contributions

1. **Evidence** — add strong public evidence for a subsystem or metric.
2. **Domain review** — identify missing dependencies, unrealistic assumptions, or incorrect scoring logic.
3. **Ontology improvements** — propose changes to the 10×10 subsystem structure with justification.
4. **Dependency mapping** — add or correct upstream/downstream industrial dependencies.
5. **Engineering** — improve data validation, scoring, simulations, dashboards, tests, and reproducibility.
6. **Annual baselines** — help build MCAB-2026 and future yearly snapshots.
7. **Translations and documentation** — make the benchmark accessible to a wider research community.

## Evidence standard

Prefer, in order:

- peer-reviewed papers and official technical reports;
- primary company or government technical documentation;
- standards bodies and high-quality datasets;
- well-documented experiments or reproducible demonstrations;
- secondary reporting only when primary sources are unavailable.

Every empirical claim should record a source, date, scope, and confidence. Do not convert speculation into a benchmark score.

## Scoring discipline

- Distinguish automated operation from autonomous maintenance, recovery, expansion, and replication.
- Distinguish digital copying from physical industrial reproduction.
- Do not use a simple average to hide critical-path dependencies.
- Preserve uncertainty explicitly.
- If evidence is insufficient, mark the field unknown rather than guessing.

## How to contribute

For small corrections, open an issue or pull request.

For substantial changes:

1. explain the subsystem or metric affected;
2. provide the strongest evidence available;
3. state the proposed change;
4. describe downstream effects on dependencies or scoring;
5. separate observed facts from inference;
6. include tests if code or schema behavior changes.

## Suggested starting points

Existing tasks provide concrete entry points: [baseline evidence #1](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/1), [engineering #2](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/2), and domain reviews #4–#13. The [issue alignment snapshot](docs/GITHUB_ISSUE_ALIGNMENT.md) maps each domain to its current research inputs and remaining review work. Link contributions to the relevant issue and identify whether they add literature evidence, calibrated scores, engineering functionality, or expert review.

- Review one of the 100 subsystems as a domain expert.
- Add evidence for one subsystem in the 2026 baseline.
- Improve dependency edges between energy, materials, manufacturing, semiconductors, robotics, and compute.
- Reproduce one score from public evidence.
- Build visualizations for bottlenecks and human-dependence paths.

## Research norm

The goal is not to argue that machine civilization is inevitable or impossible. The goal is to measure dependencies, closure, uncertainty, and change over time as rigorously as possible.

Read [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md), [docs/CONTINUITY.md](docs/CONTINUITY.md), and [docs/EDITION_PLAYBOOK.md](docs/EDITION_PLAYBOOK.md) before large structural or scoring changes. Prefer forward corrections and new edition rows over rewriting history. Update [CHANGELOG.md](CHANGELOG.md) when an edition or ontology materially moves. Use the Annual baseline / Interim update issue templates for cadence work.
