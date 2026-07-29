# Premium Scorecard — Student Home

**Programme:** DX-005A  
**Status:** Design review (architecture target)  
**Release Candidate:** `RC-2026.07.29-01`  
**Checklist:** DX-001 `PREMIUM_DESIGN_CHECKLIST.md` + DX-005A review dimensions  
**Screen:** Student Home (target design)  
**Reviewer:** DX-005A design authority  
**Date:** 2026-07-29  

---

## Mandatory checks (DX-001)

| Check | Result |
|---|---|
| One Primary action | **PASS** |
| KPI policy respected (no vanity metrics) | **PASS** |
| Cards only for justified grouping | **PASS** (lists; optional single L0 group) |
| Empty state = Reason + Next Action | **PASS** |
| Lucide only; Inter only | **PASS** (spec) |
| Semantic colour only; Gold not UI chrome | **PASS** |
| No implementation leakage in primary UI | **PASS** |
| Motion ≤250ms and purposeful | **PASS** (none required) |

**Mandatory checks: PASS**

---

## DX-005A dimension scores (target design)

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | **Mission Clarity** | **10** | L0 answers what / why now / after; Mission Model binds fields |
| 2 | **Decision Clarity** | **10** | One question; one Decision → one Action; queue cannot outshout Primary |
| 3 | **Learning Continuity** | **10** | Continuity spec: subject, lesson, mission, question, assessment, timer |
| 4 | **Information Density** | **9** | Dense lists where useful; zero KPI clutter; L2 capped at 5; why stack collapsed |
| 5 | **Professional Tone** | **10** | Operational labels; no greeting, cheer, Sensei theatre, gamification |
| 6 | **Minimalism** | **10** | Every section justified; forbid list enforced; Zero Legacy |
| 7 | **Navigation Clarity** | **10** | Boundaries: Home / Choose Exam / Session / Assessment / History |
| 8 | **Session Continuity** | **10** | One-click resume; no re-commit; failure modes honest |
| 9 | **Overall Premium Feel** | **10** | Mastery First; calm; Linear/Stripe restraint applied to learning OS |

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

**SHIP (design)** — redesign required before ship only if implementation regresses any DX-005A dimension below 9.

---

## Comparison: legacy Student Home (reference)

| Dimension | Legacy (DX-002/003) | Target |
|---|---:|---:|
| Mission Clarity | ~4 | 10 |
| Decision Clarity | ~3 | 10 |
| Learning Continuity | ~6 (resume exists; buried) | 10 |
| Information Density | ~2 | 9 |
| Professional Tone | ~4 | 10 |
| Minimalism | ~2 | 10 |
| Navigation Clarity | ~4 | 10 |
| Session Continuity | ~6 | 10 |
| Premium Feel | **~3–4/10** | **10/10** |

Legacy failed DX-001 gate and DX-003 decision density. Target clears gate.

---

## Anything below 9?

None on the target architecture. Implementation must re-score against this card in DX-005 UI execution; any dimension ≤8 forces redesign before Alpha claim on Student Home.
