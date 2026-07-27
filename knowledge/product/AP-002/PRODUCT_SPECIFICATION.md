# AP-002 — Assessment Engine Product Specification

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design complete — implementation deferred  
**Nature:** Design only (no production code)  
**Depends on:** AP-001 Assessment Pipeline, SDT-001 → SDT-003, AME-001, TUTOR-001, CIP-003  
**Governing law:** `knowledge/engineering/ARCHITECTURE_INVARIANTS.md`

---

## 1. Purpose

Design an independent **Assessment Engine** for Kwalitec that collects educational evidence about the learner in order to improve learning — not to grade, rank, or intimidate.

The Assessment Engine turns curriculum-aligned questions and prompts into structured **observations**. Those observations reduce uncertainty inside the Student Digital Twin through the existing Assessment Pipeline → Educational Reasoning path.

> Assessments are instruments of understanding. They are not examinations.

---

## 2. Educational objectives

| Objective | Outcome |
|---|---|
| Evidence collection | Every assessment run produces lawful observations the Twin can consume. |
| Uncertainty reduction | Assessment targets Twin unknowns (gaps, unstable mastery, thin evidence). |
| Mastery support | Evidence strengthens or weakens mastery confidence; it never invents mastery from completion alone. |
| Learning improvement | Feedback after assessment helps the learner understand *what to do next*, not how they “scored”. |
| Psychological safety | Assessment experiences feel supportive, curious, and non-punitive. |
| Authority integrity | Assessment observes; Reasoning infers; Twin stores learner belief; Mission schedules; Tutor explains. |

---

## 3. Scope

This design covers:

1. Educational model distinguishing Assessment from Quiz, Practice, Mission, Revision, and Exam.
2. Assessment lifecycle (intent → selection → delivery → response → observation → feedback).
3. Question taxonomy and metadata contracts.
4. Scoring-as-evidence model (no marks culture).
5. Evidence vocabulary: Observation → Evidence → Signal → Inference → Decision.
6. Integration contracts with Digital Twin, Mission Engine, and Intelligent Tutor.
7. UX principles for anxiety-safe assessment experiences.
8. Phased, independently releasable implementation milestones (AP-002A…F).

In-scope for *future implementation guidance* (not this milestone):

- Assessment domain bounded context (alongside AP-001 pipeline)
- Question bank / delivery runtime
- Richer observation payloads for Twin reasoning
- Adaptive assessment triggering from missions
- Founder analytics over assessment evidence

---

## 4. Out of scope

| Explicitly out of scope | Rationale |
|---|---|
| Implementation of engine code | This milestone is design-only |
| Production routes, templates, services, models, migrations, APIs | Constraint of AP-002-DESIGN |
| Redesign of Educational Intelligence authorities | Architecture invariants hold |
| Replacement of AP-001 Assessment Pipeline | Pipeline remains the observation ingress; Engine produces richer inputs into it |
| LLM-based auto-scoring or auto-reasoning | No LLM in educational reasoning; scoring stays deterministic |
| High-stakes exam simulation as product core | Exams are out of educational philosophy for V1 Assessment Engine |
| Marks, percentages, leaderboards, pass/fail theatre | Contradicts evidence-over-grading philosophy |
| Tutor becoming a second grading engine | Tutor explains; never grades |
| Direct Twin inference mutation by Assessment | Twin updates only via `StudentReasoningService` |
| Curriculum Studio / CIP redesign | Curriculum truth remains CIP + Retrieval |

---

## 5. Primary users

| User | Need |
|---|---|
| **Student** | Low-anxiety checks that clarify understanding and suggest next learning action |
| **Adaptive Mission Engine** | Ability to trigger assessment activity types that yield Twin-usable evidence |
| **Educational Reasoning / Twin** | Higher-quality observations than completion-only signals |
| **Intelligent Tutor** | Interpretable assessment feedback to explain without inventing grades |
| **Founder / Operator** | Diagnostics and analytics on evidence density, not student ranking |

---

## 6. Success metrics

Success is measured by **learning-system usefulness**, not exam scores.

| Metric | Intent |
|---|---|
| Observation yield | % of assessment runs that emit valid Twin observations via AP-001 |
| Uncertainty reduction | Drop in Twin “thin evidence” / unknown concepts after assessment cycles |
| Evidence integrity | Zero assessment paths that write mastery/gaps without Reasoning |
| Mission usefulness | Missions that include assessment steps produce usable Twin updates |
| Anxiety safety (qualitative) | Blind/pilot feedback: students feel supported, not tested |
| Explainability | Every student-facing assessment outcome cites evidence + next action |
| Determinism | Same inputs → same observation schema and feedback structure |

Non-metrics (do not use as success):

- Average “score”
- Time-to-100%
- Competitive ranking
- Volume of questions answered without Twin benefit

---

## 7. Acceptance criteria (design milestone)

This design pack is accepted when:

1. All required documents exist under `knowledge/product/AP-002/`.
2. Assessment is defined as evidence collection, not examination.
3. Observation / Evidence / Signal / Inference / Decision are cleanly separated.
4. Assessment Engine authority is consistent with `ARCHITECTURE_INVARIANTS.md` §7 (Assessment produces observations).
5. Twin, Mission, and Tutor integrations preserve existing authority boundaries.
6. Implementation is decomposed into independently releasable milestones.
7. Design review records risks, open questions, and recommendations.
8. No production application code, migrations, routes, templates, services, models, or APIs were modified.
9. Completion report and mandated commit are produced.

---

## 8. Relationship to AP-001

| Concern | AP-001 Assessment Pipeline | AP-002 Assessment Engine |
|---|---|---|
| Role | Evidence ingress + learning feedback from activities | Educational design & delivery of assessment instruments |
| Owns | Events, results metadata, feedback, mission links | Question model, assessment sessions, evidence semantics, triggering policy |
| Reasoning | Never | Never |
| Twin writes | Via `StudentReasoningService` only | Via AP-001 / Observation path only |
| Status | Implemented | Design |

AP-002 does not obsolete AP-001. The Engine produces assessment activity; the Pipeline remains the lawful path that turns activity into immutable events, Twin observations, and deterministic learning feedback.

---

## 9. Product thesis (one line)

> **Assess to understand the learner; never assess to judge the learner.**
