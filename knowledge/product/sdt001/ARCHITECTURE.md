# SDT-001 Architecture — Student Digital Twin Foundation

Companion to `COMPLETION_REPORT.md`. Introduces the canonical learner model
without redesigning CS-DOC-001 or CIP-001 → CIP-003.

## Long-term principle

Kwalitec now has two canonical models:

1. **Curriculum Intelligence** — WHAT is to be learned
2. **Student Digital Twin** — WHO is learning and their evolving educational state

Every future adaptive capability (Adaptive Mission Engine, Revision Planner,
Intelligent Tutor, Educational Analytics) must consume the Student Digital Twin
rather than constructing independent learner models.

```
Observations (facts)
        │
        ▼
StudentReasoningService
        │
        ▼
Educational Reasoning Engine (SDT-002)  ← sole educational inference authority
        │   RuleRegistry: mastery · confidence · momentum · consistency
        │                 readiness · gaps · prerequisites · recommendations
        │   Curriculum evidence via CurriculumRetrievalService (CIP-003)
        ▼
StudentDigitalTwin aggregate  ← sole source of truth for learner state
```

## Educational philosophy

| Kind | Nature | Examples |
|---|---|---|
| Facts | Immutable observations, append-only | Question answered, quiz completed, chapter completed |
| Inferences | Reproducible conclusions from facts | Mastery, knowledge gap, confidence, recommendation |

No LLM. No AI inference. Reasoning is deterministic.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/student_digital_twin/` |
| Application | `app/application/student_digital_twin/` |
| Persistence | `app/models/student_digital_twin.py` |
| Founder diagnostics | `app/presentation/student_digital_twin/` |

Aggregate root: `StudentDigitalTwin`.

Owns: Student, Observations, Learning State, Mastery, Knowledge Gaps,
Confidence, Goals, Recommendations, Predictions, Timeline, Reasoning history.

Nothing outside this bounded context may directly manipulate learner state.

## Curriculum access rule

Curriculum information may ONLY be accessed through:

`CurriculumRetrievalService`

Never:

- VectorStore directly
- Knowledge Graph directly
- Embeddings directly

Knowledge gaps always cite retrieval evidence. Gaps without retrieval hits are
not created.

## Relationship to other systems

| System | Relationship |
|---|---|
| CIP-001 → CIP-003 | Twin consumes structured curriculum evidence via retrieval |
| CS-DOC-001 | Unchanged Founder publishing workflow |
| Adaptive Mission Engine (future) | Must read Twin state; must not invent parallel learner models |
| AI Tutor (future) | Must read Twin + retrieve via CurriculumRetrievalService |
| Existing `app/domain/student_twin` / `app/domain/twin` | Legacy coexistence; SDT-001 is the CIP-aligned foundation |

## Founder diagnostics

Founder-only JSON endpoints under `/founder/twin`:

- `GET/POST /founder/twin/`
- `GET /founder/twin/<id>`
- `GET /founder/twin/<id>/history`
- `GET /founder/twin/<id>/mastery`
- `GET /founder/twin/<id>/gaps`
- `GET /founder/twin/<id>/recommendations`
- `GET /founder/twin/<id>/predictions`
- `GET /founder/twin/<id>/reasoning`

Not part of the student-facing experience.

## Persistence

Alembic `202607270008` adds:

| Table | Purpose |
|---|---|
| `student_digital_twins` | Twin root |
| `student_observations` | Append-only facts |
| `mastery_records` | Current mastery inferences |
| `knowledge_gaps` | Evidence-backed gaps |
| `learning_state_snapshots` | Append-only multi-dimension state |
| `recommendations` | Current Twin recommendations |
| `predictions` | Prediction scaffolds |
| `reasoning_history` | Append-only reasoning audit |

## What SDT-001 does not do

- Tutoring
- Adaptive mission generation
- Full exam prediction algorithms (scaffold only)
- Student-facing UX
- Replacement of CIP or Curriculum Studio
