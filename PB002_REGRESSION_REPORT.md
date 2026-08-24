# PB-002 — Regression Report

**Programme:** PB-002 Educational Trust Closure  
**Date:** 2026-08-01  
**Method:** Focused pytest against published CS1 educational package inventory + F6/F7/F8 unit tests  
**Base tip:** `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` (pre-merge working tree)  

---

## Commands

```bash
python3 -m pytest \
  tests/domain/session_experience/test_terminology.py \
  tests/domain/session_experience/test_pb002_reflection_packages.py \
  tests/application/educational_packages/test_pb002_f7_withhold.py \
  tests/application/educational_packages/test_pb002_package_selection.py \
  tests/application/educational_packages/test_ea006_publication.py -q
# Result: 56 passed

python3 -m ruff check <PB-002 paths>
# Result: All checks passed
```

---

## Published inventory — Reflection (F6)

| Package ID | topic_code | campaign_day | ReflectionProjection.create | Notes |
|------------|------------|--------------|-------------------------------|-------|
| CS1-EP001-PKG-1.1-PURPOSE-FUNCTION | 1.1 | CA-D1 | PASS | |
| CS1-EP001-PKG-1.2-EDA-SUMMARIES | 1.2 | CA-D2 | PASS | previously tripped on *exploratory* |
| CS1-EP001-PKG-1.2-EDA-ASSOCIATION | 1.2 | CA-D3 | PASS | |
| CS1-CS1002-PKG-1.2-PCA | 1.2 | CB-D1 | PASS | |
| CS1-CS1002-PKG-2.1-DISCRETE | 2.1 | CB-D2 | PASS | |
| CS1-CS1002-PKG-2.1-CONTINUOUS | 2.1 | CB-D3 | PASS | |
| CS1-EA005-PKG-4.2-GLM-STRUCTURE | 4.2 | — | PASS | *Explain* / *exponential* safe |
| CS1-EP001-PKG-REV-PURPOSE-EDA | CA-R1 | CA-R1 | PASS | |
| CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS | CB-R1 | CB-R1 | PASS | |

**Reflection completion rate on published inventory (projection gate):** **9/9 = 100%**

Standalone gamification tokens (`xp`, `score`, `badge`) still rejected.

---

## Published inventory — CMP substance (no LO shell)

| Topic / package | Substance source | LO-shell marker absent | CMP / package body |
|-----------------|------------------|------------------------|--------------------|
| 4.2 | `educational_package` | PASS | PASS |
| 1.1 (EA-006 suite) | `educational_package` | PASS | PASS |
| 4.1 (control) | `None` (withheld) | N/A — no session substance | PASS withhold |

---

## Revision reachability (F8)

| Chain | Sequence | Result |
|-------|----------|--------|
| Alpha | 1.1 → 1.2.1 → 1.2.2 → **CA-R1** | PASS |
| Beta (post-Alpha) | → 2.1.1 → 2.1.2 → **CB-R1** | PASS |
| Suppress TOPIC_COMPLETED | Same-leaf / revision successors | PASS |
| Allow advance after CA-R1 | No same-leaf suppress | PASS |

Natural reach without Baseline seed of `CA-R1`/`CB-R1`: **PASS** (selection layer).

---

## Affected PB-001 Phase 2 scenarios (mapped)

| Scenario | Prior | PB-002 evidence |
|----------|-------|-----------------|
| Day-1 Reflection 500 (9/10 personas) | FAIL | F6 projection PASS on all published packs |
| Topic 4.1 fallback Reading | FAIL | Substance `None` + withhold copy |
| CA-R1 / CB-R1 seed unreachable | FAIL | Chain selection reaches revision days |
| Published 1.1/1.2/2.1/4.2 CMP Reading | PASS (F1/F2) | Still PASS (EA-006 suite) |

---

## Pre-existing failures (not PB-002 regressions)

| Test | Result on tip without PB-002 | Notes |
|------|------------------------------|-------|
| `test_finish_returns_home` | FAIL | Redirect to summary, not `/student` |
| `test_daily_mission_from_derived_template_and_completion_advances` | FAIL | Synthetic `1.1` overlaid by live CS1 package title |

---

## Verdict

Published-inventory Reflection and F7/F8 selection/withhold regressions **PASS**. Silent LO-shell degrade for CS1 unpublished topics **cleared** at substance planning. LIVE full adversarial cohort re-run deferred to post-deploy tip verification.
