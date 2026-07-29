# Premium Scorecard — Choose Exam

**Programme:** DX-005B  
**Status:** Design review (architecture target)  
**Release Candidate:** `RC-2026.07.29-01`  
**Checklist:** DX-001 `PREMIUM_DESIGN_CHECKLIST.md` + DX-005B review dimensions  
**Screen:** Choose Exam (target design)  
**Reviewer:** DX-005B design authority  
**Date:** 2026-07-29  

---

## Mandatory checks (DX-001 + DX-005B)

| Check | Result |
|---|---|
| One Primary action (Begin Learning) | **PASS** |
| Discovery only (not Home / not report / not curriculum management) | **PASS** |
| KPI policy respected (no vanity metrics) | **PASS** |
| Honest Ready / Coming Soon separation | **PASS** |
| Empty state = Reason + Return later | **PASS** |
| Cards only for justified grouping | **PASS** (list selection; no marketing cards) |
| Lucide only; Inter only | **PASS** (spec) |
| Semantic colour only; Gold not UI chrome | **PASS** |
| No implementation leakage in primary UI | **PASS** |
| Motion ≤250ms and purposeful | **PASS** (search debounce / selection only) |
| Home receives learner after commitment | **PASS** (architecture) |

**Mandatory checks: PASS**

---

## DX-005B dimension scores (target design)

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | **Discovery Clarity** | **10** | One question; Ready band answers what can be begun |
| 2 | **Decision Clarity** | **10** | Single Decision → Begin Learning; filters are not Primaries |
| 3 | **Commitment Honesty** | **10** | Ready-only Begin; Soon / gated never false-start |
| 4 | **Information Density** | **9** | Dense Ready list; Soon secondary; L2 factual only |
| 5 | **Professional Tone** | **10** | No marketing, tutorials, recommendation essays, cheer |
| 6 | **Minimalism** | **10** | Explicit removals; one Primary; empty is two beats |
| 7 | **Navigation Clarity** | **10** | Discovery vs Home vs Session owned; nav label Choose Exam |
| 8 | **Handoff Continuity** | **10** | Confirm → Mission → Home continuation (DX-005A) |
| 9 | **Overall Premium Feel** | **10** | Discovery First; Linear/Stripe restraint on commitment |

**All dimensions ≥9/10.** Average **9.9**.

---

## Supporting DX-001 dimensions (reference)

| Dimension | Score |
|---|---:|
| Visual Hierarchy | 10 |
| Task Focus | 10 |
| Typography | 10 |
| Spacing | 9 |
| Consistency | 9 |

---

## Verdict

**SHIP (design)** — redesign required before ship only if implementation regresses any DX-005B dimension below 9.

---

## Comparison: legacy Choose Exam (reference)

| Dimension | Legacy (DX-002 ~7/10) | Target |
|---|---:|---:|
| Discovery Clarity | ~7 | 10 |
| Decision Clarity | ~6 (Next + later Begin; review clutter) | 10 |
| Commitment Honesty | ~7 (Ready/Soon exist; Soon density) | 10 |
| Information Density | ~6 | 9 |
| Professional Tone | ~7 | 10 |
| Minimalism | ~6 | 10 |
| Navigation Clarity | ~5 (Study Plan label mismatch) | 10 |
| Handoff Continuity | ~6 (Calibration / Home split) | 10 |
| Premium Feel | **~7/10** | **10/10** |

Legacy passed basic catalogue intent but failed Discovery First density, Primary singularity, and Home handoff clarity. Target clears gate.

---

## Anything below 9?

None on the target architecture. Implementation must re-score against this card in UI execution; any dimension ≤8 forces redesign before Alpha claim on Choose Exam.
