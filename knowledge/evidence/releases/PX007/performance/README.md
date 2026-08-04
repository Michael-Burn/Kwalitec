# PX-007 — Performance verification

**Date:** 2026-08-04  
**Scope:** Local asset hygiene + loading craft re-verify. Not a LIVE CWV claim.

## Local asset baseline (bytes)

| Asset | Bytes |
|-------|------:|
| `css/tokens.css` | 12,016 |
| `css/student/student.css` | 46,466 |
| `js/student.js` | 5,814 |

Unchanged from PX-006 Phase 4 baseline (no asset bloat this programme).

## Loading honesty

Skeletons on Home / Mission / Plan / nav-pending remain wired (PX-006). Optimistic nav retained.

## Core Web Vitals

**Not measured on LIVE this exit.** Residual **PX6-R2 / PX7-R5**.

## Regression

Soft CSS budget and skeleton contracts green in `pytest_aggregate.txt` (157 passed).
