# DX-005B Executive Summary

**Programme:** DX-005B — Choose Exam Redesign (Discovery First)  
**Status:** Complete (design architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None in this programme — documentation only  

---

## Verdict

Choose Exam is redesigned from an empty canvas as the **student discovery surface**. It answers one question: **Which exam do I want to begin?** Exactly one Primary action: **Begin Learning**. Ready curricula own L0. Coming Soon stays visually secondary. After commitment, Home owns continuation. Premium target **≥9/10 on all dimensions** — design scorecard **PASS**.

This is not a dashboard refresh of the Study Plan wizard. Zero Legacy Rule: the current Choose Exam step and multi-section review theatre are treated as if they do not exist.

---

## Design target

**Discovery First** — calm commitment, not catalogue maximisation. Find a Ready curriculum and begin with almost no uncertainty:

```
Arrive → Recognise Ready offerings → Select → Confirm → Begin Learning → Home
```

Discovery reduces uncertainty. It does not maximise choice.

---

## Structure

| Layer | Content |
|---|---|
| **L0** | Published curricula Ready to begin — selection + Primary **Begin Learning** |
| **L1** | Search & filters — Exam family, Status, Alphabetical |
| **L2** | Brief description, estimated study scope, last updated |
| **L3** | Shell navigation only — minimal |

---

## Explicit removals

Marketing copy, feature lists, readiness percentages, progress rings, recommendation essays, tutorial paragraphs, multiple CTAs, decorative badges, Coming Soon domination of the viewport, review sections for defaults the student never chose, “today’s mission” theatre on discovery.

---

## Pillar relationship (Student Operating System)

| Surface | Question | Owns |
|---|---|---|
| **Home** (DX-005A) | What should I study next? | Continuation |
| **Choose Exam** (DX-005B) | Which exam do I want to begin? | Discovery |
| **Study Session** (DX-005C) | What do I practice now? | Execution |
| **Assessment** | How am I evaluated? | Evaluation |
| **History** | What have I practiced? | Reflection |

Responsibilities must never overlap. Choose Exam owns discovery only. Home receives the learner after commitment.

---

## Authorities applied

| Authority | Role |
|---|---|
| **DX-001** | Type 24/18/16/14; spacing; one Primary; no vanity KPIs; premium gate |
| **DX-002** | Catalogue / Wizard type; one question; student nav tree |
| **DX-003** | Decision → Action → Feedback; Ready / Coming Soon; empty states; terminology |
| **DX-005A** | Home vs Choose Exam boundary; empty-state handoff; post-commit return to Home |
| **Brand Guidelines** | Inter; palette; gold not UI chrome; premium minimal tone |

---

## Impact (when implemented)

| Metric | Legacy Choose Exam / wizard | Target | Δ |
|---|---|---|---|
| Independent decisions on discovery entry | 2–4 (select + Next + later confirm clutter) | **1** (which exam) | ~60–75% |
| Primary-weight CTAs across flow | Next + Begin Learning + dual confirm | **1** (Begin Learning) | ~70% |
| Coming Soon visual weight | Peer cards / repeated essays | Secondary band | Density restored |
| Review surprise defaults | Position / style / target shown as if chosen | Applied defaults one line or omitted | ~35%+ |
| Post-commit destination | Calibration or Home (split) | **Home** with Mission ready | Continuity restored |
| Premium Feel (Choose Exam) | ~7/10 (DX-002) | ≥9/10 | Gate cleared |

---

## Non-goals

- No UI / CSS / route code in DX-005B  
- No Student Home implementation (DX-005A plan remains separate)  
- No Study Session redesign (DX-005C)  
- No Founder Subjects catalogue changes (DX-004B)  
- No curriculum engine / V1–V2 changes  
- No publication pipeline changes  

---

## Exit

All DX-005B exit criteria met at architecture level. UI execution must follow `IMPLEMENTATION_PLAN.md` and re-validate the scorecard live before claiming Choose Exam complete in product.

**Next:** DX-005C — Study Session Redesign (design), and/or Choose Exam UI execution per `IMPLEMENTATION_PLAN.md`.
