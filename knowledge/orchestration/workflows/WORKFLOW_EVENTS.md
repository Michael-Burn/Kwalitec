# Workflow Events

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS001 — Educational Workflow Model  
**Classification:** Educational stimuli that initiate or continue workflows  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **educational events** that may initiate or continue educational workflows.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`EDUCATIONAL_WORKFLOW_MODEL.md`](EDUCATIONAL_WORKFLOW_MODEL.md)
3. [`WORKFLOW_OBJECTIVES.md`](WORKFLOW_OBJECTIVES.md)
4. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md)
5. Programme VI trigger / completion corpora (recovery, revision, exam, reflection, session) where they define educational meaning of the underlying situation

> **Events initiate workflows.  
> Events do not themselves make educational decisions.**

---

## 1. Purpose

Without a clear event vocabulary, orchestration either fires randomly or silently invents “reasons” for recommendations.

This document classifies **what may lawfully start or continue a workflow**, and what an event is forbidden from implying.

---

## 2. Event Principles

1. **Stimulus, not decision.** An event reports that something educationally relevant occurred or is present. It does not choose today’s objective, recovery strategy, revision emphasis, or exam approach.
2. **Classification before participation.** The workflow must classify the event before inviting Programme VI authorities.
3. **Evidence honesty.** Occurrence of an event is not Educational Evidence of understanding unless Evidence Model writers have lawfully recorded such evidence.
4. **Deterministic classification.** The same observable situation maps to the same event class (or explicit multi-class warrant set with conflict rules).
5. **Continuation is first-class.** Some events continue an open workflow; they do not always open a new one.
6. **Absence is speakable.** “No workflow warranted” is a lawful outcome of classification.
7. **No timer-as-tutor.** Pure clock ticks without educational meaning do not invent coaching; calendar proximity may *signal* Exam Coach warrant only when Programme VI examination meaning already authorises that reading.

---

## 3. Event Catalogue

Each event has an ID for audit/developer use. Student-facing speech must not dump these IDs.

### WE-01 — Student login / return

| Aspect | Meaning |
|--------|---------|
| **Definition** | The learner becomes present for tutoring — session start, mid-journey return, or re-entry after interruption |
| **May initiate** | Day-level orchestration toward Daily Coach when an Active-class Canonical Study Plan exists; otherwise honest refusal / plan-needed path |
| **Must not imply** | Educational need equals the next chapter; login equals understanding; login equals readiness |
| **Typical primary authority** | Daily Coach (under plan); Master Planner if no lawful plan |

### WE-02 — Study session completion

| Aspect | Meaning |
|--------|---------|
| **Definition** | A Learning Session sitting ends (completed, abandoned, or capacity-exhausted) under today’s Daily Coach objective |
| **May initiate / continue** | Reflection / loop-closure workflow; subsequent Daily Coach input update; Learning Coach progression read when longitudinal warrant exists |
| **Must not imply** | Completion equals mastery; abandonment equals moral failure; session end alone rewrites the plan |
| **Typical primary authority** | Reflection meaning (Programme VI WS2 MS003) feeding Daily Coach; Learning Coach when progression question is primary |

### WE-03 — New educational evidence

| Aspect | Meaning |
|--------|---------|
| **Definition** | Lawful Educational Evidence has been recorded (assessment / quiz / mock / scored mission-assessment under Evidence Model) |
| **May initiate / continue** | Learning Coach progression / obstacle / intervention warrant evaluation; Twin estimate update *by permitted writers only*; Daily Coach context refresh |
| **Must not imply** | Workflow may reinterpret or invent evidence; coverage ticks alone are evidence of understanding |
| **Typical primary authority** | Learning Coach for educational response meaning; Twin/Evidence authorities for mutation; Daily Coach consumes, does not author evidence |

### WE-04 — Disruption detection

| Aspect | Meaning |
|--------|---------|
| **Definition** | Observed break or degradation of educational continuity or progress sufficient to raise recovery warrant evaluation (per Recovery Coach meaning) |
| **May initiate** | Recovery-oriented workflow; possible deferral of ordinary day / revision / exam emphases |
| **Must not imply** | Every quiet day is catastrophe; disruption equals punishment catch-up; recovery workflow may rewrite the Canonical Study Plan |
| **Typical primary authority** | Recovery Coach; escalate to Master Planner / Scheduling when structural change is required |

### WE-05 — Revision completion

| Aspect | Meaning |
|--------|---------|
| **Definition** | A consolidating revision emphasis or revision window reaches a completion judgement under Revision Completion meaning |
| **May initiate / continue** | Return to ordinary Daily Coach rhythm; Learning Coach progression read; Exam Coach warrant evaluation when assessment proximity and prior preparation lawfully apply |
| **Must not imply** | Revision volume equals mastery or exam certainty; completion invents new syllabus exposure |
| **Typical primary authority** | Revision Completion → Daily Coach / Exam Coach as Programme VI completion transitions specify |

### WE-06 — Examination proximity

| Aspect | Meaning |
|--------|---------|
| **Definition** | The learner’s authorised examination sitting is near enough that assessment-facing preparation becomes a candidate primary educational question (per Exam Coach / plan examination windows) |
| **May initiate** | Exam Coach warrant evaluation; possible rebalancing of day emphasis *within* plan envelopes |
| **Must not imply** | Calendar proximity equals readiness; exam phase label equals mastery; unlearned material is “exam ready” |
| **Typical primary authority** | Exam Coach when warrant holds; otherwise Learning / Revision / Recovery as Programme VI priority requires |

### WE-07 — Reflection completed

| Aspect | Meaning |
|--------|---------|
| **Definition** | Post-session Educational Reflection has produced authorised coaching notes / attainment reading for subsequent days |
| **May continue** | Daily Coach input refresh for later days; Learning Coach longitudinal inputs when applicable |
| **Must not imply** | Reflection may rewrite Canonical Study Plan; reflection mints Estimated Mastery |
| **Typical primary authority** | Daily Coach as consumer; Learning Coach when progression meaning is primary |

### WE-08 — Plan lifecycle / structural signal

| Aspect | Meaning |
|--------|---------|
| **Definition** | Canonical Study Plan lifecycle change or explicit reschedule / replan need signal (e.g. Adapted / Recovered transition meaning, or Daily Coach escalation that envelopes no longer fit) |
| **May initiate** | Master Planner / Scheduling pathway workflow |
| **Must not imply** | Workflow Engine itself mutates the plan; coaches may silently redesign envelopes |
| **Typical primary authority** | Master Planner / Scheduling (MS006–MS007 pathways) |

### WE-09 — Learning progression / obstacle signal

| Aspect | Meaning |
|--------|---------|
| **Definition** | Learning Coach meaning indicates progression concern or obstacle diagnosis warrant (without yet selecting an intervention as a workflow invention) |
| **May initiate / continue** | Learning obstacle → intervention workflow stages under Learning Coach authority |
| **Must not imply** | Workflow selects interventions independently; obstacle label rewrites Daily Coach day authority by fiat |
| **Typical primary authority** | Learning Coach; Daily Coach remains day decider unless lawful handoff says otherwise |

### WE-10 — Explicit student educational request

| Aspect | Meaning |
|--------|---------|
| **Definition** | The learner states an educational focus or asks for guidance (within product surfaces that lawfully accept such input) |
| **May initiate** | Classification into the coach/planner question that matches the request — or honest refusal if the request would violate plan / mode / evidence honesty |
| **Must not imply** | Student request overrides Learning Mode topic authority, plan protections, or Evidence Model |
| **Typical primary authority** | Depends on classified request; often Daily Coach under plan |

---

## 4. Initiate vs Continue

| Pattern | Meaning |
|---------|---------|
| **Initiate** | No open workflow for this educational concern — open a new workflow instance at Stage 0 / warrant |
| **Continue** | An open workflow awaits the next lawful stimulus (e.g. session complete → reflection → coaching notes) |
| **Supersede** | A higher-priority warrant (e.g. meaningful disruption) pauses or ends a lower-priority open workflow with explicit explanation |
| **No-op** | Event observed; no orchestration warranted — record classification, do nothing educationally inventive |

Supersede must preserve continuity of educational history and must not delete learner-owned records.

---

## 5. Simultaneous Events and Conflict

When multiple event classes apply at once, classify **all** warrants, then apply:

1. **Authority preservation** over convenience.
2. **Disruption (WE-04)** and **structural signal (WE-08)** outrank ordinary day cosmetics when Recovery / Master Planner meaning says they are primary.
3. **Evidence (WE-03)** updates inputs before day recommendation speech, but does not by itself invent a recommendation.
4. **Examination proximity (WE-06)** does not outrank unfinished first learning, unresolved disruption, or mandatory consolidation when Exam Coach warrant rules say otherwise.
5. Produce **one primary workflow** (or one primary + documented read-only inputs). Never emit conflicting primary actions.

Detailed stage behaviour lives in `WORKFLOW_STAGES.md`. Boundary hard stops live in `WORKFLOW_BOUNDARIES.md`.

---

## 6. What Is Not an Educational Workflow Event

| Non-event | Why |
|-----------|-----|
| Raw UI click without educational meaning | Product telemetry, not tutoring stimulus |
| A/B experiment assignment alone | Analytics / experiment framework |
| Background job heartbeat | Infrastructure |
| Marketing notification open | Growth surface, not Programme VII educational law |
| Twin estimate drift without Evidence Model warrant | Unlawful stimulus for educational decision |

---

## 7. Binding Rule

No Educational Workflow Engine behaviour may treat an event as an educational recommendation, mastery claim, plan mutation, or coach-authority override. Events open or continue flow; Programme VI authorities decide educational meaning within that flow.
