---
name: Method cycle
about: Run one frontier multi-domain evidence acquisition loop
title: "Method cycle: "
labels: []
assignees: []
---

## Cycle
- cycle_id (e.g. 2026-C02):
- edition year:
- batch size (default 20):

## SELECT
Paste top targets from `python3 scripts/build_target_queue.py` (dimension_id list).

## ACQUIRE
For each target, note primary sources consulted (URL/DOI + date) using the domain playbook.

## VERIFY
Confirm HR relevance, metric fit, physical vs digital boundary, honest E-level.

## INGEST
- Evidence rows added/amended:
- Research JSON updates (if any):
- Scores left blank unless explicitly justified:

## MEASURE / LEARN
- Pipeline commands run:
- Queue changes after rebuild:
- Failures / blind spots:
- Next-cycle adjustment:

Log with:

```sh
python3 scripts/log_method_cycle.py --cycle 2026-CXX --summary "..." --attempted N --verified N --ingested N --learning "..."
```
