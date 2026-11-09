# Host-independence threshold status

This file is the instrument's living answer to “has that day arrived?”  
It records **capability under declared HR0 conditions**, not demographic absence of humans.

| Field | Value |
| --- | --- |
| status | `not_met` |
| as_of | 2026-11-02 |
| edition | MCAB-2026 |
| C (Closure) | unknown |
| H (Human Dependence) | unknown |
| R_M (Machine Reproduction Number) | unknown |
| g_0 (Human-free Growth Rate) | unknown |
| confidence | Low — no calibrated formal evidence scores yet |

## Threshold definition (locked)

`status` may flip to `met` only when evidence supports, under a declared system boundary and HR0 conditions:

- operate, diagnose, repair;
- secure critical inputs and energy;
- recover from disruption;
- expand capacity;
- reproduce an equivalent successor system;

with critical-path closure consistent with **C → 1, H → 0, R_M > 1, g_0 > 0** at stated confidence.

## Current reading

As of the 2026-11-02 literature comparison:

- formal evidence rows: **0**;
- calibrated C/H/R_M/g_0: **not estimated**;
- host dependence remains the working hypothesis for the whole industrial chain.

Update this file only via reviewed PR when aggregate evidence materially changes. Never mark `met` from demos, vendor claims, or digital-only replication.
