# Authority Domains

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS001 — Educational Authority Model  
**Classification:** Constitutional domain map — owned, consumed, and prohibited educational decisions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document catalogues **educational decision domains** owned by constitutional components.

Subordinate to:

1. [`EDUCATIONAL_AUTHORITY_MODEL.md`](EDUCATIONAL_AUTHORITY_MODEL.md)
2. [`AUTHORITY_PRINCIPLES.md`](AUTHORITY_PRINCIPLES.md) — especially AP-01, AP-03, AP-05
3. Programme VI meaning corpora for each domain owner
4. [`../workflows/`](../workflows/) — Workflow Engine domain (orchestration only)

> **For each domain: owned decisions · consumed decisions · prohibited decisions.**

Educational meaning remains in Programme VI. This document records **who may decide**, not how meaning is reasoned.

---

## 1. How to Read a Domain Entry

| Field | Meaning |
|-------|---------|
| **Owner** | Constitutional component accountable for the domain (AP-01) |
| **Primary question** | The educational question this owner alone may answer |
| **Owned decisions** | Decision classes this owner may make |
| **Consumed decisions** | Authorised outputs of other owners this domain may read as inputs (AP-05) |
| **Prohibited decisions** | Decision classes this owner must refuse (AP-08) |
| **Meaning corpus** | Programme VI (or VII WS1) documents that define *how* the owned decisions are reasoned |

Consumed ≠ owned. Prohibited lists are hard stops, not preferences.

---

## 2. Domain Index

| ID | Owner | Primary educational question |
|----|-------|------------------------------|
| **AD-01** | Master Planner | How should long-term preparation be designed and published? |
| **AD-02** | Daily Coach | What is most educationally valuable *today*? |
| **AD-03** | Learning Coach | Is genuine learning progressing — and what learning response is warranted? |
| **AD-04** | Recovery Coach | How should the student recover after meaningful disruption? |
| **AD-05** | Revision Coach | What previously learned material should be revised now, and why? |
| **AD-06** | Exam Coach | How should the learner prepare for and approach the examination? |
| **AD-07** | Workflow Engine | How should constitutional reasonings be sequenced without inventing meaning? |

Supporting non-coach authorities that constrain all domains (not repeated as full AD entries): Educational Constitution / EIP corpora, Educational Evidence Pipeline, Digital Twin estimate paths, Curriculum Engine, EIP-001 State Authority Matrix — see §10.

---

## 3. AD-01 — Master Planner

| | |
|--|--|
| **Owner** | Master Planner (Programme VI) |
| **Primary question** | How should this student’s long-term preparation be designed, decided, structured, scheduled, and published as the Canonical Study Plan? |
| **Meaning corpus** | [`../../educational/planning/`](../../educational/planning/), [`../../educational/student_profile/`](../../educational/student_profile/), [`../../educational/strategy/`](../../educational/strategy/), [`../../educational/planning_engine/`](../../educational/planning_engine/), [`../../educational/planning_blueprint/`](../../educational/planning_blueprint/), [`../../educational/scheduling/`](../../educational/scheduling/), [`../../educational/study_plan/`](../../educational/study_plan/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Student Educational Profile diagnosis (planning horizon) | Where the student is now for journey design |
| Educational Strategy selection | Overall approach before plan construction |
| Planning Decision Package production | Educational decisions prior to timetable |
| Planning Blueprint structure | Date-independent journey structure |
| Scheduling / rescheduling of educational allocation | Calendar packing under policy — not coach tips |
| Canonical Study Plan publication and structural amendment pathways | Authorised preparation contract |
| Long-term educational envelopes (including protected revision / exam-facing windows) | Plan-level intent coaches must respect |
| Escalation acceptance for structural change requested by coaches | Via published rescheduling / replanning pathways |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Curriculum Engine | Syllabus structure and lawful topic order |
| Educational Evidence / Learning Coach meanings | Inputs to diagnosis and re-consultation — not overwritten |
| Recovery / Revision / Exam completion transitions | Signals that may warrant structural review — not automatic plan rewrite by those coaches |
| Daily Coach lived divergence signals | Inputs to rescheduling policy — Master Planner / Scheduling still owns structural change |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| Today’s primary educational priority under an already published plan | Daily Coach |
| In-session phase transitions for a sitting | Learning Session (under Daily Coach warrant) |
| Whether genuine learning is progressing longitudinally | Learning Coach |
| Restorative recovery warrant after disruption | Recovery Coach |
| Revision warrant for previously learned material | Revision Coach |
| Examination-preparation warrant and exam priorities | Exam Coach |
| Workflow stage order | Workflow Engine |
| Redefinition of Educational Evidence or Twin estimates | EIP-002 / Twin / EIP-001 |
| Independent daily tips that bypass the published contract’s coaching layer | Daily Coach interprets the plan; Master Planner does not micromanage each day |

---

## 4. AD-02 — Daily Coach

| | |
|--|--|
| **Owner** | Daily Coach (Programme VI / Workstream 2) |
| **Primary question** | What is most educationally valuable for this student to do *today* under the Canonical Study Plan? |
| **Meaning corpus** | [`../../educational/daily_coach/`](../../educational/daily_coach/), [`../../educational/learning_session/`](../../educational/learning_session/), [`../../educational/reflection/`](../../educational/reflection/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Today’s educational priority / objective (DCO-01 class) | Day-horizon coaching under the plan |
| Conflict handling among day-level candidates | Within Daily Coach decision model |
| Day-level recovery / adaptation posture *when still within Daily Coach bounds* | Escalates when disruption requires Recovery Coach |
| Learning Session design for today’s objective | How one sitting serves the day objective |
| Local session adaptation within the objective | Delegated under Daily Coach warrant — not a new day job |
| Educational Reflection for today’s sitting | What the sitting taught; feeds later days — not plan rewrite |
| Escalation to rescheduling / replanning pathways when day divergence is structural | Escalates; does not absorb Master Planner |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Canonical Study Plan / Master Planner | Authorised contract and envelopes |
| Student Educational Profile | Current diagnosis input |
| Learning Coach progression / obstacle / intervention meanings | Emphasis and honesty constraints |
| Recovery Coach posture | Whether restorative primary question is live |
| Revision Coach warrant / priorities | Informs day emphasis when revision is lawful |
| Exam Coach warrant / priorities | Informs day emphasis when exam preparation is lawful |
| Educational Evidence and session history | Inputs — never redefined as coverage-as-mastery |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| Redesign or silent rewrite of Canonical Study Plan | Master Planner / Scheduling |
| Educational Strategy selection as substitute for consulting it | Master Planner |
| Calendar packing / inventing intensity envelopes | Master Planner / Scheduling |
| Longitudinal progression ownership, obstacle diagnosis ownership, learning intervention meaning | Learning Coach |
| Restorative coaching when meaningful disruption is primary | Recovery Coach |
| Revision meaning for consolidating previously learned material | Revision Coach (Daily may execute today’s priority when it *is* revision under plan) |
| Examination-preparation meaning | Exam Coach |
| Workflow orchestration law | Workflow Engine |
| Minting Estimated Knowledge / Mastery from day completion | Twin / Evidence / EIP-001 |
| Redefining Educational Evidence | Evidence Pipeline |

---

## 5. AD-03 — Learning Coach

| | |
|--|--|
| **Owner** | Learning Coach (Programme VI / Workstream 3) |
| **Primary question** | Is the student genuinely learning over time — and if not, why, and what learning response is warranted? |
| **Meaning corpus** | [`../../educational/learning_coach/`](../../educational/learning_coach/), [`../../educational/learning_obstacles/`](../../educational/learning_obstacles/), [`../../educational/learning_interventions/`](../../educational/learning_interventions/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Learning progression judgement and posture | Across sessions — not a single day’s completion |
| Accumulation reading of educational evidence for progression | Consumes Evidence Model; does not rewrite writers |
| Learning obstacle diagnosis | Why progression is stalled, inconsistent, decaying, thin, or falsely ready |
| Learning intervention selection (educational response) | After diagnosis — Learning Intervention Framework |
| Informing Profile evolution and Daily Coach emphasis | Advisory to other domains — not commandeering |
| Escalation to Master Planner when progression implies structural change | Escalates; does not rewrite the plan |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Educational Evidence Model / permitted observations | Observational truth |
| Knowledge & Mastery ladder | Claim discipline (coverage ≠ understanding ≠ mastery) |
| Student Educational Profile | Diagnosis context |
| Daily Coach objectives and Reflection outputs over time | Session-history inputs |
| Canonical Study Plan | Envelope and mode context |
| Recovery / Revision / Exam postures | Boundary honesty — do not treat disruption or exam theatre as progression |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| Today’s primary day priority under the plan | Daily Coach |
| Canonical Study Plan publication / structural amendment | Master Planner |
| Restorative recovery after meaningful disruption | Recovery Coach |
| Revision warrant as consolidating coaching | Revision Coach |
| Examination-preparation warrant | Exam Coach |
| Workflow stage sequencing | Workflow Engine |
| Authoring Educational Evidence or Twin estimates by coaching fiat | Evidence / Twin / EIP-001 |
| Treating mission completion alone as mastery | EIP-006 / Evidence |

---

## 6. AD-04 — Recovery Coach

| | |
|--|--|
| **Owner** | Recovery Coach (Programme VI / Workstream 4) |
| **Primary question** | How should this student recover educationally after meaningful disruption? |
| **Meaning corpus** | [`../../educational/recovery/`](../../educational/recovery/), [`../../educational/recovery_pathways/`](../../educational/recovery_pathways/), [`../../educational/recovery_completion/`](../../educational/recovery_completion/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Recovery warrant (meaningful disruption vs temporary fluctuation) | Triggers corpus |
| Recovery educational objectives | What restoration pursues |
| Recovery strategy / pathway selection | Restorative journey type |
| Recovery boundaries for what may change during recovery | Protects plan integrity |
| Recovery completion judgement and post-recovery transition meaning | Whether recovery has been achieved and what follows |
| Informing Daily Coach while recovery is primary | Coordinates; does not permanently absorb day ownership |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Canonical Study Plan posture (Active / Adapted / Recovered) | Plan integrity context |
| Rescheduling Policy | Lawful structural pathways when needed |
| Learning Coach evidence / obstacle meanings | Honesty about learning vs disruption |
| Daily Coach day context | Coordination input |
| Educational Evidence and continuity history | Disruption reading — Continuity preserved |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| Long-term Educational Strategy / plan redesign as if Master Planner | Master Planner — escalate via pathways |
| Ordinary day-priority ownership when disruption is not primary | Daily Coach |
| Learning obstacle / intervention meaning as a substitute for recovery | Learning Coach (distinct question) |
| Revision as fake recovery theatre | Revision Coach / Recovery boundaries forbid |
| Exam preparation as punitive catch-up | Exam Coach / Recovery boundaries |
| Punitive overload or history erasure | Constitution / Continuity / Recovery boundaries |
| Workflow orchestration law | Workflow Engine |
| Redefining Evidence or Mastery from missed days alone | Evidence / Twin |

---

## 7. AD-05 — Revision Coach

| | |
|--|--|
| **Owner** | Revision Coach (Programme VI / Workstream 5) |
| **Primary question** | What previously learned material should this student revise now, and why? |
| **Meaning corpus** | [`../../educational/revision/`](../../educational/revision/), [`../../educational/revision_strategies/`](../../educational/revision_strategies/), [`../../educational/revision_completion/`](../../educational/revision_completion/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Revision warrant (prior exposure mandatory) | Refuse if first learning is required |
| Revision objectives and qualitative priority emphasis | What to consolidate now |
| Revision strategy selection | Kind of revision appropriate now |
| Revision boundary posture | Protects plan, Daily, Learning, Recovery, mastery authorities |
| Revision completion judgement and transition meaning | Whether consolidation has strengthened enough |
| Informing Daily Coach emphasis | Coordinates; does not commandeer day authority |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Canonical Study Plan / protected revision windows | Plan intent |
| Learning Coach progression / evidence / obstacle / intervention meanings | Honest consumption — never override |
| Daily Coach day-priority authority | Coordination context |
| Recovery Coach posture | Defer when disruption is primary |
| Educational Evidence of prior exposure and consolidation needs | Inputs |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| First-pass learning of material without prior exposure | Learning Coach / Daily first learning |
| Today’s day-priority ownership by commandeering Daily Coach | Daily Coach |
| Restorative recovery after meaningful disruption | Recovery Coach |
| Master Planner strategy / scheduling / plan rewrite | Master Planner |
| Examination-preparation ownership | Exam Coach |
| Overriding Learning Coach progression / obstacle / intervention meaning | Learning Coach |
| Workflow orchestration law | Workflow Engine |
| Minting mastery from revision theatre | Evidence / Twin / EIP-006 |

---

## 8. AD-06 — Exam Coach

| | |
|--|--|
| **Owner** | Exam Coach (Programme VI / Workstream 6) |
| **Primary question** | How should this learner prepare for and approach the examination? |
| **Meaning corpus** | [`../../educational/exam/`](../../educational/exam/), [`../../educational/exam_strategies/`](../../educational/exam_strategies/), [`../../educational/exam_completion/`](../../educational/exam_completion/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Examination-preparation warrant | When exam-facing preparation is educationally warranted |
| Examination-preparation objectives and qualitative priorities | Assessment-facing goods |
| Examination strategy selection | Kind of preparation appropriate at this stage |
| Examination-preparation boundaries | Must not replace learning, revision, recovery, or planning |
| Examination-preparation completion judgement and transition meaning | Whether preparation has fulfilled its educational purpose |
| Informing Daily Coach emphasis when exam preparation is primary | Coordinates; does not permanently absorb day ownership |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| Canonical Study Plan / exam-facing windows | Plan intent |
| Learning Coach / Revision Coach / Recovery Coach meanings | Honesty — exam theatre must not hide missing learning, revision, or disruption |
| Daily Coach day context | Coordination |
| Accumulated Educational Evidence | Assessment-facing readiness inputs — not calendar-alone claims |
| Student Educational Profile | Learner context |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| First learning of unlearned syllabus material as “exam prep” | Learning / Daily |
| Revision ownership of consolidating coaching | Revision Coach |
| Recovery ownership after disruption | Recovery Coach |
| Plan redesign / strategy / scheduling | Master Planner |
| Day-priority ownership outside exam-primary coordination | Daily Coach |
| Readiness claims from calendar proximity alone | Evidence / Exam warrant rules |
| Workflow orchestration law | Workflow Engine |
| Redefining Evidence or Mastery from mock proximity alone | Evidence / Twin |

---

## 9. AD-07 — Workflow Engine

| | |
|--|--|
| **Owner** | Educational Workflow Engine (Programme VII / Workstream 1) |
| **Primary question** | How should educational reasonings be initiated, sequenced, handed off, and concluded across constitutional components without inventing meaning? |
| **Meaning corpus** | [`../workflows/`](../workflows/), [`../workflow_transitions/`](../workflow_transitions/), [`../workflow_completion/`](../workflow_completion/) |

### Owned decisions

| Decision class | Notes |
|----------------|-------|
| Recognition and classification of educational events for orchestration | Events do not decide educational meaning |
| Opening, continuing, superseding, and concluding workflows | Orchestration lifecycle |
| Selection of which Programme VI authority’s question is *primary* for a flow | Invitation — not answering the question |
| Stage sequencing and lawful transitions | WS1 / MS002 |
| Conflict prevention among simultaneous primary actions | Single primary decider per active flow |
| Orchestration completion (fulfilment of coordination responsibilities) | ≠ educational success |
| Orchestration explainability of flow | Why the flow started / who participated |

### Consumed decisions

| Source | Consumed as |
|--------|-------------|
| All Programme VI owned decisions | Artefacts to sequence and surface — never rewrite |
| This Authority Model (domains / principles / boundaries) | Ownership map the invitation must respect |
| EIP corpora | Bounds on what orchestration may claim |

### Prohibited decisions

| Must not decide | Rightful owner / reason |
|-----------------|-------------------------|
| Any Programme VI educational answer (today / progression / recovery / revision / exam / plan) | Respective Programme VI owners |
| Redefinition of coach or Master Planner meaning | Programme VI |
| Modification of Canonical Study Plan | Master Planner / Scheduling |
| Reinterpretation of Educational Evidence | Evidence Pipeline |
| Independent educational recommendations | Programme VI warrant required |
| EIP-001 mutation rights by orchestration label | State Authority Matrix |
| Educational Authority ownership map amendments by runtime fiat | This Model — amend documentation first |

**Special note:** The Workflow Engine owns *orchestration decisions*. This Educational Authority Model (Programme VII / Workstream 2) owns the *ownership catalogue*. Neither owns Programme VI educational meaning.

---

## 10. Supporting Authorities (Constraints, Not Coach Domains)

These authorities bound all AD-01–AD-07 owners. They are not substitute coaches.

| Authority | Owns | Domains must |
|-----------|------|--------------|
| **Educational Constitution / Logic Registry** | Educational truth and logic IDs | Obey; never invent contradicting meaning |
| **Educational Evidence Pipeline** | Observational evidence meaning and lawful creation pathways | Consume; never redefine |
| **Digital Twin (estimate paths)** | Evidence-driven Estimated Knowledge / Mastery under EIP | Consume; never author via coaching fiat |
| **Curriculum Engine** | Syllabus structure truth (V1/V2 traversable) | Traverse; never rewrite syllabus law in coaching |
| **EIP-001 State Authority Matrix** | Mutation rights for educational states | Separate decision ownership from write rights |
| **EIP-003 Explainability Standard** | How educational claims must be explained | Satisfy; authority explainability adds ownership layer |
| **EIP-005 Continuity Standard** | Preservation of rightful educational history | Never erase history to simplify ownership |

---

## 11. Cross-Domain Decision Quick Reference

| Educational decision | Single owner |
|----------------------|--------------|
| Publish / structurally amend Canonical Study Plan | Master Planner |
| Choose Educational Strategy | Master Planner |
| Pack / reschedule educational calendar allocation | Master Planner / Scheduling |
| Decide today’s primary educational priority | Daily Coach |
| Design / adapt one learning session under today’s objective | Daily Coach → Learning Session (delegated) |
| Interpret what today’s sitting meant educationally | Daily Coach → Reflection |
| Judge longitudinal learning progression | Learning Coach |
| Diagnose learning obstacles / select learning interventions | Learning Coach |
| Warrant and lead recovery after meaningful disruption | Recovery Coach |
| Warrant and prioritise consolidating revision | Revision Coach |
| Warrant and prioritise examination preparation | Exam Coach |
| Sequence / hand off / conclude among the above | Workflow Engine |
| Own the ownership map itself | This Educational Authority Model (WS2) |

---

## 12. Closing

If a proposed decision does not appear under exactly one domain’s **Owned decisions**, it is not yet constitutional.

> **Name the owner. Consume with respect. Refuse the prohibited. Amend the map before inventing ownership.**
