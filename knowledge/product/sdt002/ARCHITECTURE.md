# SDT-002 Architecture — Educational Reasoning Engine

Companion to `COMPLETION_REPORT.md`. Introduces the deterministic Educational
Reasoning Engine without redesigning CS-DOC-001, CIP-001 → CIP-003, or SDT-001.

## Long-term principle

Every educational inference that updates the Student Digital Twin must be
produced by the Educational Reasoning Engine. Future adaptive capabilities
(Adaptive Mission Engine, Revision Planner, Intelligent Tutor, Educational
Analytics) must **consume** engine decisions — they must not implement
educational logic independently.

```
Observation (fact)
        │
        ▼
Retrieve Supporting Curriculum Evidence   ← CurriculumRetrievalService (CIP-003)
        │
        ▼
Apply Educational Rules                   ← RuleRegistry + deterministic rules
        │
        ▼
Generate Educational Inference            ← ReasoningResult (decisions + explanations)
        │
        ▼
Update Student Digital Twin               ← StudentReasoningService applies result
        │
        ▼
Record Reasoning History                  ← educational_reasoning_* tables (immutable)
```

No component may skip a stage. No LLM. No probabilistic AI.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/educational_reasoning/` |
| Application | `app/application/educational_reasoning/` |
| Persistence | `app/models/educational_reasoning.py` |
| Founder diagnostics | `app/presentation/educational_reasoning/` (`/founder/reasoning/*`) |

The Student Digital Twin aggregate (SDT-001) remains the sole learner-state
source of truth. This context owns **how inferences are produced**, not the
learner state itself.

## Rule types

| Rule | Code | Role |
|---|---|---|
| Mastery Update | `mastery_update` | Evidence-weighted mastery from outcomes |
| Confidence Adjustment | `confidence_adjustment` | Confidence from outcome ratio |
| Learning Momentum | `learning_momentum` | Recent-outcome momentum |
| Consistency | `consistency` | Study-day consistency |
| Readiness Contribution | `readiness_contribution` | Retention + weighted exam readiness |
| Knowledge Gap Detection | `knowledge_gap_detection` | Gaps requiring curriculum evidence |
| Prerequisite Analysis | `prerequisite_analysis` | Enrich gaps with prerequisite entities |
| Recommendation | `recommendation` | Recommendations from gaps |

Rules receive structured inputs (`ReasoningContext`), return structured outputs
(`RuleExecution`), produce human-readable `Explanation`s, and are independently
testable. New rules register on `RuleRegistry` without modifying existing rules.

## Rule execution lifecycle

1. Application builds `ReasoningContext` (observations, prior mastery, twin scope).
2. `CurriculumEvidenceService` retrieves supporting evidence via
   `CurriculumRetrievalService` only.
3. `EducationalReasoningEngine.reason()` executes registry rules in order,
   merging each `RuleExecution` into the context.
4. Engine assembles `ReasoningResult` (mastery, confidence, learning state, gaps,
   recommendations, decisions, explanations).
5. `StudentReasoningService` applies the result to the Twin aggregate and
   scaffolds predictions (framework only).
6. `ReasoningPersistenceService` appends immutable run / execution / explanation /
   decision metadata.

## Explanation model

Every decision exposes:

- **Why** — `Explanation.summary` / `detail`
- **Observations** — `observation_ids`
- **Curriculum evidence** — `curriculum_evidence_ids`
- **Rule** — `rule_code`

Founder diagnostics surface these fields under `/founder/reasoning/*`.

## Relationship to Student Digital Twin (SDT-001)

| Concern | Owner |
|---|---|
| Learner state aggregate | SDT-001 `StudentDigitalTwin` |
| Observation facts | SDT-001 (append-only) |
| Educational inference math | SDT-002 rules / engine |
| Twin orchestration | `StudentReasoningService` (delegates to engine) |
| Twin inference tables | SDT-001 (`mastery_records`, `knowledge_gaps`, …) |
| Reasoning audit metadata | SDT-002 (`educational_reasoning_runs`, …) |

SDT-001 Twin tables are **not** duplicated. Engine tables store reasoning
metadata only.

## Relationship to Curriculum Retrieval (CIP-003)

Curriculum evidence is retrieved exclusively through
`CurriculumRetrievalService` with profile `STUDENT_DIGITAL_TWIN`. Rules never
query VectorStore, Knowledge Graph, or embeddings directly. Gaps without
retrieval hits are not created.

## Founder diagnostics

| Endpoint | Purpose |
|---|---|
| `POST /founder/reasoning/run` | Execute engine for a Twin |
| `GET /founder/reasoning/history` | Immutable run history |
| `GET /founder/reasoning/rules` | Registered rules |
| `GET /founder/reasoning/explanations` | Explanation audit |
| `GET /founder/reasoning/decision/<id>` | Single decision record |

Not student-facing.

## Persistence

Alembic `202607270009` adds:

| Table | Purpose |
|---|---|
| `educational_reasoning_runs` | One immutable engine cycle |
| `educational_rule_executions` | Per-rule execution trace |
| `reasoning_explanations` | Explainability payloads |
| `decision_records` | Educational decision metadata |

## What SDT-002 does not do

- Tutoring or Adaptive Mission generation
- Full exam prediction algorithms (scaffold remains SDT-001)
- Student-facing UX
- Replacement of CIP, Curriculum Studio, or Twin aggregate
- LLM / probabilistic inference
