# Implementation Roadmap — Adaptive Assessment Experience

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design — sequencing for small engineering milestones  
**Effective:** 2026-07-28  

---

## Purpose

Break Adaptive Assessment delivery into **small, independently releasable engineering milestones** that surface the certified Educational Intelligence Platform without architecture redesign or educational-reasoning reinvention.

This roadmap is product sequencing. Detailed service design remains subordinate to AP-001 / AP-002 / architecture law at implementation time.

---

## Roadmap principles

1. **Experience before cleverness** — ship framed checks and honest feedback before exotic adaptivity.  
2. **Observation yield before volume** — prove Twin-usable evidence path.  
3. **Mission-native** — assessment appears inside the daily loop, not as a side quiz app.  
4. **Explainability from day one** — why / next / uncertain on every release.  
5. **Additive flags** — progressive enablement; safe defaults.  
6. **No second brain** — reuse Reasoning, Twin, Mission, Tutor authorities.

---

## Dependency posture

| Dependency | Role |
|---|---|
| AP-001 Assessment Pipeline | Lawful observation ingress + learning feedback persistence |
| AP-002 Assessment Engine (design → implement) | Instruments, sessions, richer items (as engineered) |
| Adaptive Mission Engine | Scheduling whether/when a check is today’s work |
| Student Digital Twin + Reasoning | Belief updates; intents for selection |
| Tutor | Optional explanation of results |
| EQ / Explainability standards | Copy and claim honesty |

ILE-001 may proceed in thin slices even while AP-002 implementation milestones land — but must not bypass AP-001 for Twin writes.

---

## Milestone slices (indicative)

### ILE-001.A — Experience foundations (docs → thin UI contract)

**Intent:** Lock student language, session type labels, entry frame, and non-goals in product surfaces.

**Deliver:** Copy bank; empty/disabled states; feature flag scaffolding; no new educational math.

**Exit:** Design pack adopted; student-facing terms match `SESSION_TYPES.md` / principles.

---

### ILE-001.B — Framed Quick Check in Mission

**Intent:** First learner-complete path: Mission step → Quick Check → immediate feedback → observations via existing pipeline.

**Deliver:** Entry frame (why/effort); short item delivery; pause/resume basics; summary with next action; anxiety-safe chrome.

**Exit:** Students can complete a Quick Check without feeling examined; observation yield measurable.

**Non-goals:** Deep adaptive selection; readiness batteries; confidence calibration UX depth.

---

### ILE-001.C — Intent framing + eligibility visibility

**Intent:** Show *why this check now* from Twin/Mission context; respect density and time gates in UX.

**Deliver:** Intent → session type mapping in product behaviour; suppress/replace copy when gates fail; Mission alternative when check deferred.

**Exit:** Blind/dogfood: “I understand why this appeared.”

---

### ILE-001.D — Feedback & Tutor bridge

**Intent:** Immediate after-summary quality; optional “Explain this result.”

**Deliver:** Feedback model implementation for Quick Check; Tutor entry point without re-scoring; incomplete-session honesty.

**Exit:** Students can answer what/why/next/uncertain after a check.

---

### ILE-001.E — Additional session types (thin)

**Intent:** Introduce Revision Check and Recovery Check as distinct frames (reuse delivery runtime).

**Deliver:** Journey-specific framing + selection policy hooks; long-gap welcome path; revision-due path.

**Exit:** Correct session type appears for the matching journey without exam chrome.

---

### ILE-001.F — Confidence Check (assessment-time)

**Intent:** Optional confidence prompts + calibration narrative.

**Deliver:** Confidence Check type; sparse prompts; over/under/aligned narratives; never-overstate rules enforced in copy.

**Exit:** Calibration comprehensible; prompts skippable.

**Note:** Broader product-wide uncertainty UX remains ILE-005.

---

### ILE-001.G — Deep Check & Readiness Check

**Intent:** Longer confirmation and bounded pre-exam focus experiences.

**Deliver:** Time-budget enforcement; non-guarantee readiness language; confirmation vs exploration mix per policy.

**Exit:** Pre-exam check guides focus without pass prediction; Deep Check used only when budget/gates allow.

---

### ILE-001.H — Conflict, partial evidence, and recovery polish

**Intent:** Harden failure modes: interrupted, incomplete, conflicting evidence messaging + Mission bridges.

**Deliver:** UX for conflict honesty; partial evidence states; resume reliability; density after partial runs.

**Exit:** Failure/recovery checklist passes qualitative review.

---

### ILE-001.I — Perception validation

**Intent:** Measure learner trust and anxiety safety before strong effectiveness claims.

**Deliver:** Blind review / Stage-aligned perception pack for Adaptive Assessment; copy fixes.

**Exit:** Evidence for SUCCESS_MEASURES leading indicators; no vanity “questions answered” success story.

---

## Suggested sequencing

```
ILE-001.A Foundations
    → ILE-001.B Quick Check in Mission
    → ILE-001.C Intent + eligibility
    → ILE-001.D Feedback + Tutor bridge
    → ILE-001.E Revision + Recovery types
    → ILE-001.F Confidence Check
    → ILE-001.G Deep + Readiness
    → ILE-001.H Failure polish
    → ILE-001.I Perception validation
```

Parallel as capacity allows: AP-002 item/runtime milestones underneath B–G; ILE-002 Mission Experience polish alongside B–C; ILE-003 Explain patterns reused in D.

---

## Explicit non-milestones (out of ILE-001)

- Redesign of Educational Reasoning rules  
- LLM-authored item selection authority  
- High-stakes mock exam product  
- Social / competitive assessment  
- Architecture changes to Twin SoT  
- Declaring Version 1 production-ready solely from this programme  

---

## Engineering constraints (reminder)

- Documentation in this pack does not authorise production shortcuts.  
- Schema changes via Alembic when implementation needs them.  
- Curriculum V1/V2 both remain loadable.  
- Services must not depend on `flask.request`; routes stay thin.  
- No LLM in selection, scoring, or mastery inference.

---

## Handoff checklist (per slice)

1. Experience principles still hold  
2. Authorities unchanged  
3. Student copy reviewed for exam-anxiety leakage  
4. Success measures for the slice defined (learner outcomes / trust)  
5. Feature flag + safe rollback  
6. Completion report if programme process requires  

---

**End of IMPLEMENTATION_ROADMAP**
