# Go / No-Go Decision — Version 1 Private Beta

**Programme:** EP-004 — Workstream 7  
**Decision date:** 2026-07-24  
**Evidence pack:** [`VERSION_1_BETA_REPORT.md`](VERSION_1_BETA_REPORT.md)  
**Framework:** EP-003 [`GO_NO_GO_REPORT.md`](../ep003_educational_effectiveness/GO_NO_GO_REPORT.md)  
**Scale:** GO | GO WITH CONDITIONS | NO GO

---

## Verdict

# GO WITH CONDITIONS

---

## What this decision means

| Allowed | Not allowed |
|---|---|
| Continue **Stage 0** internal private beta | Public registration or marketing launch |
| Enable analytics **internal-only** per activation log | Enable Pilot / Private-beta flag on external-hosting env without checklist |
| Recruit **Stage 1** only after conditions below | Claim “Kwalitec measurably improves outcomes” from Week 0 |
| File weekly scorecards with honest N labels | Change M1–M9 or educational algorithms under EP-004 |
| Use feedback register for copy/onboarding priorities | Recommendation-effectiveness marketing |

---

## Conditions (must clear to advance)

| # | Condition | Owner | Clears Stage |
|---|---|---|---|
| C1 | Complete Privacy Review checklist signatures (`../private_beta/PRIVACY_REVIEW.md`) | Product + Security / ops | Stage 1 |
| C2 | Complete EP-002 go-live checklist **Pilot** row before flag ON for invitees | Ops | Stage 1 analytics |
| C3 | Stage 0 monitoring remains GREEN; no open P0 | Ops / Product | Stage 1 |
| C4 | External cohort path to ≥20 active students documented before Stage 2 | Product | Stage 2 |
| C5 | ≥4 weeks measurement for ≥20 active **before** any educational-effectiveness **GO** claim | Product + Educational governance | Educational GO (EP-003 G5/G7/G8) |
| C6 | Interview sample target (≥8 or 25% of active) before Q1–Q5 all-Yes educational GO | Product | Educational GO |
| C7 | Keep recommendations **no-claim**; Journey M5 labelled provisional until ADR-026 emit | Product | Ongoing |

Until C5–C6: educational effectiveness remains **PENDING EVIDENCE** / **NO-GO for effectiveness claims**, even while this EP-004 verdict allows staged beta continuation.

---

## Q1–Q5 (EP-003 worksheet at this decision)

| # | Question | Answer | Evidence |
|---|---|---|---|
| Q1 | Does the product help students? | **Insufficient** | External KPIs empty; Stage 0 only |
| Q2 | Is it understandable? | **Partial / Insufficient** | FB-001, FB-008 — naming + orientation; no interview sample |
| Q3 | Is it trusted? | **Insufficient** | Twin/trust themes watch; no interview ≥ target |
| Q4 | Is it stable? | **Yes** (Stage 0) | Ops GREEN; GA retained; no EP-004 P0/P1 |
| Q5 | Would we recommend it? | **Conditional Yes** for closed Stage 0–1 invite | Founder would continue invite path **with C1–C3**; not for public recommend |

All five **Yes** required for educational **GO**. Current: **not met** → effectiveness claim **NO-GO**; programme execution **GO WITH CONDITIONS**.

---

## Gate cross-check

| Gate | Status |
|---|---|
| Educational behaviour unchanged | Pass |
| Analytics healthy for current stage | Pass |
| Privacy compliant for expanded cohort | Open → Condition C1 |
| Operational readiness maintained | Pass |
| Platform Baseline preserved | Pass |

---

## Sign-off

| Role | Name | Date | Verdict |
|---|---|---|---|
| Product | | 2026-07-24 | **GO WITH CONDITIONS** (programme) |
| Educational governance | | 2026-07-24 | **NO-GO** on effectiveness claims until C5–C6 |
| Security / ops | | 2026-07-24 | **HOLD** Stage 1 until C1–C2 |
| Architecture | | 2026-07-24 | **Baseline preserved** — Pass |

Holds:

1. Privacy Review signatures before any external invite (C1).  
2. Analytics Pilot checklist before external flag ON (C2).  
3. No educational-effectiveness or exam-readiness marketing until C5–C6 + EP-003 Q1–Q5 Yes.

---

## Relationship to other decisions

| Document | Relationship |
|---|---|
| EP-003 `GO_NO_GO_REPORT.md` | Framework; was PENDING EVIDENCE — EP-004 fills Stage 0 evidence and records execution verdict |
| EP-001 `V1_EXIT_CRITERIA.md` | Broader product exit — commercial/public still closed |
| GA `CERTIFICATION_REPORT.md` | Operational GA ≠ educational GO |
| `VERSION_1_READINESS.md` | Update Beta + Educational validation rows from this decision |

---

## Re-review trigger

Re-open this decision when **any** of:

- Privacy Review signed and first Stage 1 WAL week filed, or  
- Stage 2 N≥20 and ≥4 weeks scorecards complete, or  
- P0 incident / privacy incident / educational honesty incident.
