# DX-005A Executive Summary

**Programme:** DX-005A — Student Home Redesign (Mastery First)  
**Status:** Complete (design architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None in this programme — documentation only  

---

## Verdict

Student Home is redesigned from an empty canvas as the **Student Operating System entry point**. It answers one question: **What should I study next?** Exactly one Primary action. Mission owns L0. Hierarchy L0 Current Mission → L1 Learning Queue → L2 Recent Progress → L3 shell navigation. Premium target **≥9/10 on all dimensions** — design scorecard **PASS**.

This is not a CSS refresh of `student/home.html`. Zero Legacy Rule: the current Student Home is treated as if it does not exist.

---

## Design target

**Mastery First** — calm, purposeful, professional. Continue learning with almost no thought:

```
Arrive → Recognise current mission → Click Primary → Study → Return Home
```

Encouragement comes from **clarity**, not celebration.

---

## Structure

| Layer | Content |
|---|---|
| **L0** | Current Mission — subject, objective, one Primary |
| **L1** | Learning Queue — attention-only rows |
| **L2** | Recent Progress — ≤5, quiet orientation |
| **L3** | Shell nav only — no Quick Actions |

---

## Explicit removals

Welcome / greeting theatre, Study Sensei narrator stack, multi-why MES layers, trust badges, readiness / countdown KPI cards, Journey story panel, Guidance / Coach duplicate panel, educational experience panel on Home, “This week” feedback stats, upcoming milestones, Quick Actions, welcome modal, congratulations / day-complete cheer, progress rings, streaks, badges, gamification, feature promotion, multiple Primaries.

Full register: `CONTENT_REMOVAL_REGISTER.md`.

---

## Pillar relationship (Student Operating System)

| Surface | Question | Owns |
|---|---|---|
| **Home** (DX-005A) | What should I study next? | Continuation |
| **Choose Exam** (DX-005B) | What can I begin studying? | Discovery |
| **Study Session** | What do I practice now? | Execution |
| **Assessment** | How am I evaluated? | Evaluation |
| **History** | What have I practiced? | Reflection |

Responsibilities must never overlap. Home owns continuation only.

---

## Authorities applied

| Authority | Role |
|---|---|
| **DX-001** | Type 24/18/16/14; spacing; one Primary; no vanity KPIs; premium gate |
| **DX-002** | Home type; one question; student nav tree; B-004 density |
| **DX-003** | Decision → Action → Feedback; reading flow; terminology; empty states |
| **DX-004** | Operating-system discipline (continuation vs catalogue vs execution) adapted to student |
| **Brand Guidelines** | Inter; palette; gold not UI chrome; premium minimal tone |

---

## Impact (when implemented)

| Metric | Legacy Student Home | Target | Δ |
|---|---|---|---|
| Independent decisions | 4–7 | 1 | ~75–85% |
| Explanation / why layers above CTA | 6–10 | ≤2 (objective + why-now) | ~70–80% |
| Primary-weight buttons | 2–5 | 1 | ~80% |
| Secondary panels (readiness/journey/coach) | 3+ | 0 | −100% |
| Resume path | Scan + re-commit risk | One click | Continuity restored |
| Premium Feel | ~3–4/10 | ≥9/10 | Gate cleared |

---

## Non-goals

- No UI / CSS / route code in DX-005A  
- No Choose Exam redesign (DX-005B)  
- No Session / Assessment surface redesign  
- No curriculum engine / V1–V2 changes  
- No Founder Console changes  

---

## Exit

All DX-005A exit criteria met at architecture level. UI execution must follow `IMPLEMENTATION_PLAN.md` and re-validate the scorecard live before claiming Student Home complete in product.

**Next:** DX-005B — Choose Exam Experience Redesign (after Home design gate; UI may sequence separately).
