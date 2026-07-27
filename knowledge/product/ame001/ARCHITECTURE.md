# AME-001 Architecture — Adaptive Mission Engine

Companion to `COMPLETION_REPORT.md`. Introduces the Adaptive Mission Engine
without redesigning CS-DOC-001, CIP-001 → CIP-003, SDT-001, SDT-002, or SDT-003.

## Long-term principle

Kwalitec now converts educational intelligence into learner action:

1. **Curriculum Intelligence** — WHAT should be learned
2. **Student Digital Twin** — WHO is learning
3. **Learning Graph** — HOW knowledge is interconnected
4. **Educational Reasoning** — WHY educational state changes
5. **Adaptive Mission Engine** — WHAT to do today

The Mission Engine must **never** perform educational reasoning itself. It
consumes decisions already produced by the Educational Reasoning Engine and
structures already maintained by the Learning Graph.

```
Student Digital Twin
        │
        ▼
Educational Reasoning decisions (recommendations / gaps / readiness)
        │
        ▼
Learning Graph (prerequisite / recovery paths)
        │
        ▼
Curriculum Retrieval (evidence enrichment)
        │
        ▼
Mission Prioritisation  →  Construction  →  Validation
        │
        ▼
Daily Adaptive Mission (one learner · one day · one mission)
```

No LLM. No timetable. Output is today's optimal learning plan.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/adaptive_mission/` |
| Application | `app/application/adaptive_mission/` |
| Persistence | `app/models/adaptive_mission.py` |
| Founder diagnostics | `app/presentation/adaptive_mission/` (`/founder/missions/*`) |

Aggregate root: `AdaptiveMission`. One **active** mission exists per learner.

Owns: Objectives, Tasks/Steps, Priorities, Time Allocation, Educational Reasons,
Expected Outcomes, Progress.

## Mission generation pipeline

Every stage is deterministic:

1. Load Student Digital Twin
2. Consume Twin recommendations / knowledge gaps / learning state
   (produced earlier by Educational Reasoning — never recomputed here)
3. Load Learning Graph for recovery / prerequisite structure
4. Optionally enrich evidence via `CurriculumRetrievalService`
5. Prioritise candidates (no randomness)
6. Construct mission (abstract activities only)
7. Validate educational consistency
8. Activate (superseding any prior active mission)

## Prioritisation strategy

Candidates are ranked from Twin decisions using:

- knowledge gap severity
- recommendation priority
- exam readiness (lower readiness → higher urgency)
- momentum
- confidence
- Learning Graph recovery-path length
- recent study history (deterministic window)

Every priority score carries an educational explanation. Never prioritise
randomly.

## Validation pipeline

Before publication, verify:

- educational consistency with Twin decisions
- prerequisite validity via Learning Graph recovery paths
- curriculum alignment (Twin concepts / graph nodes)
- duplicate active-mission avoidance
- evidence availability for gap-driven missions

Reject missions that fail validation (`status=rejected`).

## Mission structure

Each mission contains:

- Mission Goal
- Educational Objective
- Estimated Duration
- Concepts Covered
- Activities (abstract: review, practice, recovery, reflection, …)
- Evidence References
- Expected Learning Outcome
- Reason
- Priority
- Success Criteria
- Reflection Prompt

`AdaptiveMission.as_mission_card()` projects a simple card-compatible DTO so
the student Mission card can remain unchanged while the engine deepens.

## Relationships

| System | Relationship |
|---|---|
| Student Digital Twin | Source of learner state + educational decisions |
| Educational Reasoning | Produces decisions consumed by prioritisation |
| Learning Graph | Supplies prerequisite / recovery structure |
| Curriculum Retrieval | Evidence enrichment only (never VectorStore direct) |
| Legacy `Mission` / Mission Engine v2 | Preserved; AME-001 does not redesign them |

## Founder diagnostics

| Endpoint | Purpose |
|---|---|
| `GET /founder/missions/` | List missions for a twin |
| `GET/POST /founder/missions/generate` | Generate today's mission |
| `GET /founder/missions/history` | Append-only history |
| `GET/POST /founder/missions/validate` | Validation dry-run / check |
| `GET /founder/missions/diagnostics` | Prioritisation + graph diagnostics |

Not student-facing.

## Persistence

Alembic `202607270011` adds:

| Table | Purpose |
|---|---|
| `adaptive_missions` | Mission root |
| `mission_steps` | Abstract activity steps |
| `mission_progress` | Progress snapshot |
| `mission_history` | Append-only lifecycle audit |
| `mission_feedback` | Optional feedback |
| `mission_completion` | Immutable completion |

Does not store duplicated Twin mastery / gap / recommendation rows.

## What AME-001 does not do

- Educational reasoning / mastery inference
- Calendar scheduling / timetables
- Dashboard redesign
- Replacement of legacy `Mission` / Mission Engine v2
- LLM / probabilistic ranking
- Direct VectorStore access
