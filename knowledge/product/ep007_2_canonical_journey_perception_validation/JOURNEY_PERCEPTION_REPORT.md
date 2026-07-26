# EP-007.2 — Journey Perception Report

**Programme:** EP-007.2 — Canonical Journey Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Status:** Complete (evidence-only)  
**Method:** [`PERCEPTION_METHODOLOGY.md`](PERCEPTION_METHODOLOGY.md)  
**Surfaces judged:** [`STUDENT_SURFACE_PACK.md`](STUDENT_SURFACE_PACK.md)  
**Tier B archive:** [`tier_b_reviews/`](tier_b_reviews/) (N=9)  
**Baseline perception:** EP-004 corpus + Meta Analysis V2 (dual homes Near Universal; 30-vs-90 Universal) + EP-005.2 Student Journey Review + EP-006.3/5 dual-home residuals  
**Does not:** Change runtime, UI, or educational reasoning  

---

## 1. Executive verdict

Post–EP-007.1 journey consolidation **measurably improves student perception of navigation clarity, duration honesty, and organisational cognitive load on the W-PROD sole-runtime path**. Pre-change Near-Universal dual-home friction and Universal duration mismatch are **cleared to cleared / minority residual** for production sole runtime.

Cold-start explainability and content-depth nights remain separate residuals. Dual-run (`SOLE_RUNTIME=OFF`) still exposes dual homes — out of W-PROD claim window.

| Dimension | Baseline (pre-consolidation) | Post–EP-007.1 Tier B | Meaningful change? |
|---|---|---|---|
| Entry-point discoverability | Dual homes Near Universal | **Pass** (single Home) | **Yes** |
| Session-start clarity | Competing start paths | **Pass** ≥80% | **Yes** |
| Navigation confidence | Split authority | **Pass** majority | **Yes** |
| Duration consistency | 30-vs-90 Universal | **Pass** majority (preferred path) | **Yes** |
| Continuity through today’s study | Fractured continue | **Pass** majority | **Yes** |
| Perceived cognitive load | Reconciliation tax | **Pass** majority | **Yes** |

**Unsupported claims:** “Dual-home cured in dual-run Alpha”; “KSI ≥ 80”; “educational effectiveness GO”; “planning topic quality improved”; “thin session content cured.”

---

## 2. Cohort and method

| Item | Detail |
|---|---|
| Tier B personas | SV-001, 002, 004, 009, 010, 015, 016, 018, 020 |
| N | **9** (≥8 methodology floor) |
| Focus | Workflow / adoption / cognitive load / decision support / recoverability |
| Judgement basis | Sole-runtime surface pack + duration / navigation captures + EP-007.1 Tier A tests |
| Baseline contrast | EP-004 SV corpus; EV-PERC-002 dual-home / duration; EP-005.2 REM-02/03 |

Reviews are archived under this programme so EP-004 and EP-006.x corpora remain intact.

---

## 3. Dimension findings

### 3.1 Entry-point discoverability

**Pass (9/9).** All reviewers report login / root lands on one Student Home; SV-010 confirmed legacy `/dashboard/` and `/missions/` redirect. Dual-home choice is absent on W-PROD sole runtime.

### 3.2 Session-start clarity

**Pass (≥80%).** Home primary CTA Start / Resume is affirmative across the cohort (SV-001, SV-002, SV-016 especially). Meets methodology ≥80% target.

### 3.3 Navigation confidence

**Pass (majority).** Recoverability (SV-010) and end of “ignore one home” workaround (SV-018) support confidence. SV-009 remains Conditional on full workflow substitution — not a navigation Fail.

### 3.4 Duration consistency

**Pass (majority / Universal theme cleared on preferred path).** Home and Session Overview agree at preferred minutes (capture: 30 = 30). SV-002’s prior “Home 30 / Session 90” weeknight tax is explicitly cleared. Resolver matches legacy mission path when preferred is set (Tier A + capture).

**Residual:** If preferred is unset, day-type fallback still applies — not observed as 30-vs-90 conflict in this pack when preferred is set (production typical).

### 3.5 Continuity through today’s study

**Pass (majority).** Login → Home → Session → Complete → Home described as one loop (SV-001, SV-010, SV-018). Resume without second-home choice affirmed.

### 3.6 Perceived cognitive load

**Pass (majority).** SV-016 primary hypothesis cleared; SV-002 weeknight reconciliation tax gone; SV-015 decision fatigue down. SV-009 Conditional Pass (lighter organisation, not tool absorption).

---

## 4. Baseline vs post-implementation

| Theme (Meta Analysis V2 / EP-005.2) | Baseline frequency | Tier B post–EP-007.1 |
|---|---|---|
| Dual homes / dual start paths | Near Universal | **Cleared** on W-PROD sole runtime |
| Same-day 30 vs 90 duration | Universal | **Cleared** when preferred set |
| Thin Home → Session Overview | Near Universal | **Improved** (no competing thin path); sparse content residual may remain |
| Dual-home trust tax after MES / readiness Pass | EP-006.3/5 residual | **Cleared** as journey residual on W-PROD |

Qualitative cohort shift (N=9 persona re-reviews), not an external RCT. Under EP-005.1 methodology: sufficient Tier B for category re-score with **Medium** confidence — not High, and not Stage 1 product-decision KPIs.

---

## 5. Unsupported claims log

| Claim | Status |
|---|---|
| Dual-home cured under `SOLE_RUNTIME=OFF` | **Unsupported** (Alpha/soak residual) |
| PlanningService topic selection improved | **Unsupported** (not measured; unchanged) |
| K1 ≥ 80 / mid-Excellent planning | **Unsupported** |
| KSI ≥ 80 / G1 PASS | **Unsupported** |
| Educational-effectiveness GO | **Unsupported** |
| External cohort confirms same lift | **Unsupported** (N_external = 0) |
| Cold-start MES / readiness cured by journey | **Unsupported** (separate residuals) |

---

## 6. Remediation remaining (if any)

| ID | Residual | Priority |
|---|---|---|
| JRN-PERC-01 | Dual-home when sole runtime OFF (soak / Alpha) | P2 (ops posture; not W-PROD) |
| JRN-PERC-02 | Sparse / thin session content nights | P2 (content, not routing) |
| JRN-PERC-03 | External Stage 1 N=0 — Medium confidence ceiling | P1 for G1 Strong claims |
| JRN-PERC-04 | `V1_REVIEW_PACKAGE` may lag sole-runtime chrome | P3 |
| JRN-PERC-05 | Welcome dismiss endpoint still legacy-named (works; redirects Home) | P3 |
| JRN-PERC-06 | Guided Unified Journey chrome optional OFF — not required for dual-home clearance | Info |

REM-02 / REM-03 student-perception clearance on **W-PROD**: **Met** for this pack.

---

## 7. Evidence IDs

| ID | Artefact |
|---|---|
| EV-JRN-TB-001 | `tier_b_reviews/` (N=9) |
| EV-JRN-TB-002 | This report |
| EV-JRN-TB-003 | `STUDENT_SURFACE_PACK.md` + `_capture/` |
| EV-JRN-TA-001 | `tests/presentation/test_canonical_journey.py` (EP-007.1) |
| EV-JRN-BASE-001 | EP-004 Meta Analysis V2 dual-home / duration |
| EV-JRN-BASE-002 | EP-005.2 STUDENT_JOURNEY_REVIEW / REM-02 / REM-03 |

---

**End of JOURNEY_PERCEPTION_REPORT**
