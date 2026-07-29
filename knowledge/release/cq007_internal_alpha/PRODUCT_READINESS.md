# CQ-007 — Product Readiness

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Release Candidate:** `RC-2026.07.29-01`  
**Date:** 2026-07-29  
**Verdict:** **Ready for Internal Alpha** (GO WITH CONDITIONS from FV-001B / FV-001C)

---

## Scope

Product assessment of Founder workflow, student workflow, navigation, terminology, and learnability from blind validation evidence. This programme does not re-run UX.

---

## Founder workflow

| Criterion | Met? | Evidence |
|---|---|---|
| Create subject | Yes | FV-001B Final |
| Upload Official CMP + Syllabus | Yes | Documents Ready |
| Validate | Yes | Passed |
| Preview Ready | Yes | 23 topics |
| Approve | Yes | Success flash |
| Publish | Yes | Status Published |
| Observe Ready / Version / Date | Yes | Subjects catalogue |
| Complete without assistance | Yes | Full path on RC |

**Verdict inheritance:** FV-001B Final → **GO WITH CONDITIONS**.

Conditions are usability chrome (stale NEXT STEP, stage strip lag, findings trust friction, topic count mismatch) — not publication blockers.

---

## Student workflow

| Criterion | Met? | Evidence |
|---|---|---|
| Login | Yes | FV-001C |
| Onboarding comprehensible | Yes | Alpha onboarding |
| Choose Exam loads | Yes | No 500 |
| Discover Ready CS1V | Yes | Ready + version + date |
| Select / start enrolment wizard | Yes | Advances past Choose Exam |
| Exam date + availability steps | Yes | Wizard continues |
| Post-plan Student Home / Today's Focus | Partial | Gate understood; clean E2E Home shot not primary package |

**Verdict inheritance:** FV-001C → **GO WITH CONDITIONS**.

Discovery and enrol **start** are validated. Full enrol → Home confidence is lower and tracked as a quality/evidence condition, not a discovery P0.

---

## Navigation

| Surface | Assessment | Evidence |
|---|---|---|
| Console → Subjects / Studio | Reachable; Console Home is operations-first (Minor) | FV-001B UX-05 |
| Studio workspace chrome | Status + Subjects Ready authoritative; strip/NEXT STEP lag (Major) | FV-001B UX-01/03 |
| Student dual-role landing | RC admin lands Console; student surfaces reachable (Minor) | FV-001C UX-S02 |
| Choose Exam density | Ready findable near top; Coming Soon noise (Major) | FV-001C UX-S01 |

Navigation does **not** block Alpha publication or discovery.

---

## Terminology

| Check | Status | Evidence |
|---|---|---|
| Student surfaces free of forbidden EI jargon | Pass | FV-001C terminology audit |
| “Inference” as syllabus chapter title (not product jargon) | Noted / acceptable | FV-001B non-finding |
| Ready / Coming Soon language | Clear | FV-001C onboarding + Choose Exam |
| Approve vs Publish flash verbs | Cleared on RC | Prior PI-002 amplify defect; FV-001B cleared |

---

## Learnability

| Persona | Assessment |
|---|---|
| Founder | Can complete publish path without assistance on RC. Guidance chrome can mislead mid-flow (NEXT STEP / findings) but Status + Subjects Ready remain learnable anchors. |
| Student | Can find Ready CS1V and begin wizard without assistance. Catalogue density and dual-role landing add friction, not blockers. |

Learnability is **sufficient for invite-only Internal Alpha**, not yet polished for unguided external users.

---

## Product readiness summary

| Area | Ready for Alpha? | Blocks Alpha? |
|---|---|---|
| Founder workflow | Yes | No |
| Student workflow | Yes (Home path evidence P2) | No |
| Navigation | Yes (chrome P1) | No |
| Terminology | Yes | No |
| Learnability | Yes for invite-only Alpha | No |

**Product conclusion:** Product is ready for Internal Alpha on **Release Candidate: RC-2026.07.29-01**, with usability conditions tracked during testing.
