# Version 2 Educational Principles

**Document ID:** V2-001-PRINCIPLES  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Binding educational rules for Version 2 design  
**Nature:** Architecture / governance — not implementation  

**Parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)  
**Higher law:** [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)

These principles specialise Version 2 Learning Journey behaviour. They do not amend the Constitution. Where conflict appears, the Constitution wins until formally amended.

---

## 1. Principle Catalogue

### P1 — Topics may require multiple sessions

A curriculum topic is not sized to a single daily mission by default.

**Implications**

- Journey planning must allow N sessions per topic
- Effort estimation is first-class ([`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md))
- UI and engines must avoid “one box = one topic finished” assumptions

**Forbids**

- Treating the first session finish as Topic Complete by default

---

### P2 — A session is never assumed to complete a topic

Finishing a Learning Session completes the session only.

**Implications**

- Session completion updates session state, history, reflection flow, and journey progress inputs
- Topic Complete requires journey completion criteria + lawful confirmation ([`STATE_MACHINE.md`](STATE_MACHINE.md))

**Forbids**

- Auto-writing journey `COMPLETED` on `finish_session`
- Student copy that says “Topic mastered” after one session

---

### P3 — Recommendations continue journeys rather than replace them

The default educational move is to continue the active Learning Journey.

**Implications**

- JourneyRecommendation prefers next session on the same topic when the journey is `ACTIVE`
- Topic switching requires an explainable educational reason (prerequisite gap, exam-weight urgency under authorised mode, disclosed revision interrupt, student choice)

**Forbids**

- Silent replacement of Learning Mode focus by advisory rankings
- Thrashing across topics for engagement novelty

**Aligns with:** Constitution Article VI (Learning Mode authority); Explainability Standard Q3/Q4.

---

### P4 — Evidence accumulates across sessions

Understanding and behavioural truth emerge from accumulated JourneyEvidence, not from the latest event alone.

**Implications**

- Evidence remains append-only and journey-attributed
- Twin updates consume accumulated evidence under existing Evidence Authority
- Thin evidence ⇒ honest uncertainty, not invented confidence

**Forbids**

- Overwriting yesterday’s evidence with today’s convenience
- Whiplash recommendations from a single soft signal

**Aligns with:** [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md).

---

### P5 — Reflection occurs after every learning session

Every completed Learning Session enters a reflection-required posture before educational close.

**Implications**

- Reflection is part of the session lifecycle, not a separate optional product
- Reflection produces soft evidence and recommendation inputs
- Deferred capture, if allowed later, must be explicit and time-bounded

**Forbids**

- Closing a session as educationally complete with no reflection path
- System-fabricated reflection presented as the student’s

---

### P6 — Revision is part of the journey rather than a separate feature

Revision is a **session intent** (and later a disclosed mode) inside or returning to topic journeys — not a disconnected island that erases first-pass history.

**Implications**

- A journey may include learn → practice → revise sessions
- Revision Mode, when activated, must disclose itself and must not wipe Learning Mode history ([`EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md))
- Revision Engine (V2-007) schedules revision sessions that attach to journeys / topics

**Forbids**

- “Revision workspace” as the only conceptual home for review with no journey attribution
- Treating revision completion as first-pass Topic Complete by synonym

**Aligns with:** Constitution Revision Mode; Product Blueprint sustainable progress.

---

### P7 — Progress represents educational evidence rather than unsupported mastery

`JourneyProgress` answers how the journey is advancing using coverage posture, sessions, objectives addressed, and evidence density — not unsupported mastery badges.

**Implications**

- Progress language must distinguish Observed / Derived facts from Estimates (Explainability Standard)
- Estimated Knowledge / Mastery remain Twin-owned and evidence-gated
- Coverage completion remains Study Progress meaning under the Constitution

**Forbids**

- Narrating JourneyProgress as “Mastered”
- Letting Estimated Mastery thresholds auto-complete journeys (EPA-002 FINDING-001 class failure)

---

### P8 — Curriculum identity remains canonical

Journeys reference official Subject / Chapter / Topic / Objective identity. They never invent parallel syllabuses.

**Implications**

- Curriculum Graph (V2-002) and Curriculum Engine remain syllabus truth
- Remapping follows continuity rules when editions change

**Forbids**

- Free-text “topics” as journey anchors without curriculum ids

---

### P9 — Twin authority is not replaced by journey state

The Learning Journey is the educational **path** model. The Student Digital Twin remains the learner **state** model.

**Implications**

- Journeys write evidence, history, and progress inputs
- Twin interprets knowledge, memory, readiness, predictions
- Plans and recommendations remain consequences of intelligence + constraints

**Forbids**

- A second mastery store inside JourneyProgress
- AI coach mutating Twin beliefs while bypassing evidence

---

### P10 — Explainability is mandatory for journey decisions

Every material JourneyRecommendation and Topic Complete prompt must answer:

1. What do we objectively know?  
2. What do we estimate?  
3. Why this recommendation / completion ask?  
4. What should the student do next?

**Forbids**

- Opaque “do this next” without educational reason
- Presenting advice as observed fact

---

### P11 — Continuity survives planning change

Deleting or replacing a Study Plan must not destroy journey history, evidence, or rightful coverage.

**Implications**

- Journeys belong to learner + topic identity
- Planning objects remain disposable contexts

**Aligns with:** Educational Continuity Standard; Constitution II §1.8.

---

### P12 — Sustainable intensity over forced streaks

Pause, defer, and effort-aware recommendations are educational features.

**Implications**

- `PAUSED` / `DEFERRED` are lawful, non-shameful states
- Burnout and capacity signals inform recommendations

**Forbids**

- Punitive streak breaks as product identity
- Auto-inflating workload to maximise sessions

---

### P13 — Determinism in core journey logic

Same journey state, evidence stream, and configuration → same transition and core recommendation outputs.

**Forbids**

- Random topic picks in core Learning Mode path
- Hidden non-deterministic LLM ownership of journey state

---

### P14 — Version 1 behaviour remains intact until governed cutover

These principles bind Version 2 design. They do not silently change Version 1 runtime.

**Implications**

- Implementation milestones must declare activation boundaries
- Dual-run / coexistence may be required during migration

---

## 2. Principle → Entity Map

| Principle | Primary entities |
|-----------|------------------|
| P1, P2 | LearningJourney, LearningSession, JourneyState |
| P3, P10 | JourneyRecommendation |
| P4, P7 | JourneyEvidence, JourneyProgress |
| P5 | JourneyReflection, SessionState |
| P6 | LearningSession intent, Revision Engine (future) |
| P8 | Curriculum Model bindings |
| P9 | Twin boundary |
| P11 | JourneyHistory, Continuity |
| P12 | PAUSED / DEFERRED |
| P13 | Journey Engine / Mission Engine 2.0 |
| P14 | Migration Strategy |

---

## 3. Anti-Patterns (Version 2)

| Anti-pattern | Violates |
|--------------|----------|
| Mission-complete auto Topic Complete | P2, P7 |
| Recommendation swaps topic without disclosure | P3, P10 |
| Mastery threshold completes journey | P7, Constitution |
| Optional reflection with no pending state | P5 |
| Revision wipes first-pass journey | P6, P11 |
| JourneyProgress labelled “Mastery” | P7 |
| Plan delete cascades journey evidence away | P11 |
| Chatbot owns next topic | P9, P13 |

---

## 4. Closing

Version 2 educational quality is judged by adherence to these principles in every subsequent milestone. Features that violate them are not Version 2 — even if they ship under a Version 2 label.
