# TUTOR-001 Architecture — Evidence-Backed Intelligent Tutor

Companion to `COMPLETION_REPORT.md`. Introduces the Intelligent Tutor without
redesigning CS-DOC-001, CIP-001 → CIP-003, SDT-001 → SDT-003, AME-001, or
AP-001.

## Long-term principle

Kwalitec now speaks educational intelligence to the learner:

1. **Curriculum Intelligence** — WHAT should be learned
2. **Student Digital Twin** — WHO is learning
3. **Learning Graph** — HOW knowledge is interconnected
4. **Educational Reasoning** — WHY educational state changes
5. **Adaptive Mission Engine** — WHAT to do today
6. **Assessment Pipeline** — evidence from activity back into the Twin
7. **Intelligent Tutor** — explains those decisions in understandable guidance

The Tutor must **never** become another reasoning engine. It explains
decisions already produced by Educational Reasoning, Twin state, Learning
Graph structure, Adaptive Missions, and Assessment Feedback.

```
Student Question
        │
        ▼
Student Digital Twin
        │
        ▼
Educational Reasoning decisions (already on Twin)
        │
        ▼
Learning Graph (prerequisites / recovery)
        │
        ▼
Curriculum Retrieval (TUTOR profile)
        │
        ▼
Evidence Assembly
        │
        ▼
Explanation Builder (ResponseBlueprint)
        │
        ▼
TutorGenerationPort (deterministic V1 / future LLM)
        │
        ▼
Tutor Response
```

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/intelligent_tutor/` |
| Application | `app/application/intelligent_tutor/` |
| Persistence | `app/models/intelligent_tutor.py` |
| Founder diagnostics | `app/presentation/intelligent_tutor/` (`/founder/tutor/*`) |
| Student surface | Home Coach panel + `POST /student/tutor/explain-mission` |

## Tutor pipeline

Every interaction walks the full stack — no bypass:

1. Classify / accept student question
2. Load Student Digital Twin
3. Consume Educational Reasoning outputs already on the Twin
4. Load Learning Graph relations (recovery / prerequisites)
5. Retrieve curriculum evidence via `CurriculumRetrievalService` (`RetrievalProfile.TUTOR`)
6. Assemble structured evidence (curriculum, student, graph, reasoning, mission, assessment)
7. Build `ResponseBlueprint` (explanation, next action, recovery, reflection, hints)
8. Generate prose through `TutorGenerationPort`
9. Persist conversation turn (session / messages / explanations)

## Evidence assembly

Every response packages:

- Curriculum evidence (CIP-003 retrieval excerpts)
- Student-specific evidence (mastery / confidence / learning state)
- Learning Graph relationships (recovery path, prerequisites, related concepts)
- Educational Reasoning outputs (recommendations, gaps, reasoning run id)
- Supporting observations via Twin state and Assessment feedback summaries

Evidence is structured **before** response generation.

## Response builder

Constructs:

- Educational explanation
- Supporting evidence ids / summaries
- Suggested next action
- Related concepts
- Recovery guidance
- Reflection prompt
- Learning hints + coaching lines

Every recommendation references assembled evidence.

## Conversation memory

Lightweight session memory remembers:

- current conversation turns
- referenced concepts
- active mission id
- short learner-state summary

Does **not** store long-term educational state. The Student Digital Twin remains
the system of record.

## LLM abstraction

`TutorGenerationPort` isolates prose generation.

Version 1 ships `DeterministicTutorGeneration` — a replaceable placeholder that
renders the blueprint deterministically. Future LLM adapters must:

- accept the same `TutorGenerationRequest`
- explain assembled evidence only
- never invent Twin / Reasoning / Graph decisions
- be swappable without changing Tutor domain or orchestration

## Relationships

| System | Relationship |
|---|---|
| Student Digital Twin | Source of learner state; Tutor never mutates Twin inferences |
| Educational Reasoning | Decisions explained by Tutor; never reimplemented |
| Learning Graph | Prerequisite / recovery structure for explanations |
| Curriculum Retrieval | Evidence enrichment via `RetrievalProfile.TUTOR` |
| Adaptive Mission Engine | Active mission explained; Tutor does not generate missions |
| Assessment Pipeline | Recent feedback summarised into Tutor context |

## Founder diagnostics

| Endpoint | Purpose |
|---|---|
| `GET /founder/tutor/sessions` | List Tutor sessions for a twin |
| `GET/POST /founder/tutor/context` | Build Tutor context |
| `GET/POST /founder/tutor/evidence` | Assemble structured evidence |
| `GET /founder/tutor/explanations` | List persisted explanations |
| `GET /founder/tutor/diagnostics` | Twin-scoped Tutor diagnostics |
| `GET/POST /founder/tutor/ask` | Run full Tutor pipeline (diagnostic) |

## Student experience

Home Coach panel surfaces a Tutor preview from Twin / Adaptive Mission decisions
and offers **Explain today's mission** (`POST /student/tutor/explain-mission`).
No dashboard redesign — the Tutor extends today's mission naturally.

## Persistence

Alembic `202607270013` adds:

| Table | Purpose |
|---|---|
| `tutor_sessions` | Conversation session + lightweight memory JSON |
| `tutor_messages` | Student and Tutor messages |
| `tutor_explanations` | Structured explanations |
| `tutor_feedback` | Optional feedback on responses |

Does not duplicate Twin mastery / gap / recommendation rows.

## Future LLM integration strategy

1. Keep `TutorGenerationPort` as the sole generation dependency
2. Add an infrastructure adapter (e.g. `LlmTutorGeneration`) implementing the port
3. Inject via `IntelligentTutorService(generation=...)` or app factory wiring
4. Constrain prompts to the assembled `ResponseBlueprint` + evidence summaries
5. Preserve deterministic tests via the placeholder backend in CI

## What TUTOR-001 does not do

- Educational reasoning / mastery inference
- Mission generation / prioritisation
- Dashboard redesign
- Direct VectorStore access
- Live LLM integration
- Duplication of Twin learner state
