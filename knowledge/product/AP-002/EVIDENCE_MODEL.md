# AP-002 — Evidence Model

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Purpose

Separate layers of educational information so Assessment cannot accidentally become Reasoning.

| Layer | Owner | Nature |
|---|---|---|
| Observation | Twin / AP-001 path | Immutable fact |
| Evidence | Assessment + Pipeline packaging | Structured support for claims |
| Signal | Derived soft indicators | Advisory strength only unless promoted |
| Inference | Educational Reasoning | Reproducible conclusion |
| Decision | Reasoning outputs on Twin | Actionable educational choice |

> Assessment produces observations. Educational Reasoning remains responsible for inference.

---

## 2. Definitions

### 2.1 Observation

An **Observation** is an immutable educational fact about what happened.

Examples:

- Learner answered item X at time T
- Selected option B tagged misconception M
- Used two hints
- Submitted reflection R

Observations never say “therefore mastery is high”.

Canonical kinds today (`ObservationKind`) include `question_answered`, `quiz_completed`, `study_session_completed`, `revision_completed`, `chapter_completed`, `formula_reviewed`. Assessment Engine sessions must map into these (or carefully extended kinds in a future Twin milestone — not silently).

### 2.2 Evidence

**Evidence** is packaged observational material that can lawfully support an educational claim.

Examples:

- Assessment Result linking event ↔ observation
- Declared evidence dimensions (correctness, misconception, …)
- Curriculum retrieval excerpts cited for the objective under assessment
- Session PerformanceSummary (evidence-only)

Evidence is stronger when dense, consistent, curriculum-grounded, and low-scaffolded.

### 2.3 Signal

A **Signal** is a lightweight indicator that *may* inform advice but does not alone author Estimated Knowledge / Mastery.

Examples:

- Self-reported confidence
- Response time outliers
- Single completion event
- Elapsed study minutes

Signals may appear in Tutor coaching tone and mission soft prioritisation inputs **only** where existing policy allows — they must not bypass EIP-002.

### 2.4 Inference

An **Inference** is a deterministic conclusion produced by `StudentReasoningService` / Educational Reasoning Engine.

Examples:

- Updated mastery record for concept C
- Knowledge gap G with retrieval citation
- Confidence / readiness dimension change
- Recommendation R

Only Reasoning creates inferences.

### 2.5 Decision

A **Decision** is an actionable educational output already reasoned — e.g. “recover prerequisite P”, “verify mastery on topic T”, “today’s mission priority”.

Mission Engine **consumes** decisions; Tutor **explains** decisions; Assessment **does not invent** decisions.

---

## 3. Clear separation diagram

```
Raw response (Engine)
        │
        ▼
Observation  ←──── Assessment / AP-001 (facts only)
        │
        ▼
Evidence packaging  ←──── metadata, summaries, retrieval refs
        │
        ├──► Signal (soft) ──► advice / tone (non-authoritative alone)
        │
        ▼
Inference  ←──── StudentReasoningService only
        │
        ▼
Decision  ←──── Twin recommendations / gaps / readiness outputs
        │
        ▼
Mission schedules · Tutor explains · Graph relates
```

---

## 4. Ownership matrix

| Artefact | May create | Must not create |
|---|---|---|
| Assessment Engine | Responses, instrument sessions, evidence dimensions | Inferences, Twin mastery rows, mission priorities |
| Assessment Pipeline (AP-001) | Events, Observations (via ObservationService), LearningFeedback | Educational policy reinterpretation |
| Educational Reasoning | Inferences, Decisions on Twin | Fabricated observations |
| Mission Engine | Missions from Decisions | New inferences |
| Tutor | Explanations, encouragement | Grades, inferences, Twin writes |
| Learning Graph | Relationship structure / projections | Independent learner SoT |

---

## 5. Provenance requirements

Every Observation from Assessment Engine must carry:

- `provenance` including engine session + item version
- `evidence_reference` suitable for Founder audit
- curriculum entity ids (opaque)
- assessment intent

Reasoning history should record `triggered_by` consistent with AP-001 (`assessment_pipeline:…`) and preferably engine session id in metadata for end-to-end traceability (MS-004 Digital Twin Traceability).

---

## 6. Integrity rules

1. No inference without observation and/or retrieved curriculum evidence.
2. Soft signals cannot alone create high Estimated Mastery language.
3. Evidence packaging cannot rewrite Observation facts.
4. Tutor prose is not evidence.
5. Founder analytics may aggregate evidence; they do not become Twin SoT.

---

## 7. Cold start honesty

When evidence is thin:

- Twin remains honest about uncertainty
- Assessment prioritises diagnostic intent
- UX avoids “you are behind” framing
- Missions may include short probes rather than fake certainty
