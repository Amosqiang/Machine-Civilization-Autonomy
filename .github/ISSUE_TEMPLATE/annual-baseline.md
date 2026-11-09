---
name: Annual baseline
about: Open or complete a yearly MCAB edition (MCAB-YYYY)
title: "Baseline: MCAB-"
labels: []
assignees: []
---

## Edition
- Year:
- Opened with: `python3 scripts/new_edition.py --year YYYY --from-year YYYY-1`
- Planned evidence cutoff (`as_of`):

## Scope
- [ ] Formal evidence rows for priority critical-path subsystems
- [ ] Domain reviews linked
- [ ] Dependency edges verified or explicitly left as hypotheses
- [ ] Pipeline rebuild (`run_pipeline.py --year YYYY`)
- [ ] CHANGELOG entry (capability / evidence / ontology / assumption)
- [ ] Threshold status reviewed (`data/threshold/STATUS.md`)

## Critical-path focus
List the umbilical cords this edition prioritizes.

## Explicit unknowns
What will remain unknown rather than guessed?

## Notes
Link related evidence issues and domain reviews. Do not treat literature demos as calibrated HR0 scores.
