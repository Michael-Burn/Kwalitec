# AME-001 — Adaptive Mission Engine

## Summary

AME-001 delivers Kwalitec’s Adaptive Mission Engine: a deterministic subsystem
that transforms educational decisions from the Student Digital Twin,
Educational Reasoning Engine, and Learning Graph into one actionable daily
mission per learner. The engine never performs educational reasoning itself —
it consumes Twin recommendations / gaps, traverses Learning Graph recovery
structure, optionally enriches curriculum evidence via
`CurriculumRetrievalService`, then prioritises, constructs, and validates a
daily plan. Student dashboard UX is unchanged; Founder diagnostics are exposed
under `/founder/missions/*`. No LLM dependency was introduced. CS-DOC-001,
CIP-001 → CIP-003, and SDT-001 → SDT-003 remain intact.

## Files Created

- `app/domain/adaptive_mission/__init__.py`
- `app/domain/adaptive_mission/adaptive_mission.py`
- `app/domain/adaptive_mission/mission.py`
- `app/domain/adaptive_mission/mission_step.py`
- `app/domain/adaptive_mission/mission_priority.py`
- `app/domain/adaptive_mission/mission_objective.py`
- `app/domain/adaptive_mission/mission_plan.py`
- `app/domain/adaptive_mission/mission_schedule.py`
- `app/domain/adaptive_mission/mission_reason.py`
- `app/domain/adaptive_mission/mission_outcome.py`
- `app/domain/adaptive_mission/mission_progress.py`
- `app/domain/adaptive_mission/mission_completion.py`
- `app/domain/adaptive_mission/prioritisation.py`
- `app/domain/adaptive_mission/construction.py`
- `app/domain/adaptive_mission/validation.py`
- `app/application/adaptive_mission/__init__.py`
- `app/application/adaptive_mission/adaptive_mission_service.py`
- `app/application/adaptive_mission/persistence.py`
- `app/models/adaptive_mission.py`
- `app/presentation/adaptive_mission/__init__.py`
- `app/presentation/adaptive_mission/routes.py`
- `migrations/versions/202607270011_ame001_adaptive_mission.py`
- `tests/application/adaptive_mission/__init__.py`
- `tests/application/adaptive_mission/test_adaptive_mission.py`
- `knowledge/product/ame001/ARCHITECTURE.md`
- `knowledge/product/ame001/COMPLETION_REPORT.md`

## Files Modified

- `app/models/__init__.py` (register Adaptive Mission ORM models)
- `app/__init__.py` (model import + `/founder/missions` blueprint)
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Tests Executed

```
python3 -m pytest tests/application/adaptive_mission/ \
  tests/application/learning_graph/ \
  tests/application/educational_reasoning/ \
  tests/application/student_digital_twin/ -q
# 44 passed

python3 -m ruff check app/domain/adaptive_mission \
  app/application/adaptive_mission \
  app/presentation/adaptive_mission \
  app/models/adaptive_mission.py \
  tests/application/adaptive_mission
# All checks passed
```

## Migration Impact

Alembic revision `202607270011` (revises `202607270010`) adds:

| Table | Purpose |
|---|---|
| `adaptive_missions` | Mission root (active/superseded/completed/rejected) |
| `mission_steps` | Abstract activity steps |
| `mission_progress` | Progress snapshot |
| `mission_history` | Append-only lifecycle audit |
| `mission_feedback` | Optional feedback |
| `mission_completion` | Immutable completion |

Does not alter SDT-001 / SDT-002 / SDT-003 tables. Does not duplicate Twin
inference rows.

## Architecture Compliance

- Layering preserved: domain → application → presentation; no HTTP in services.
- Mission Engine consumes Twin / Reasoning / Graph / Retrieval — does not
  duplicate educational logic.
- Curriculum evidence exclusively via `CurriculumRetrievalService`.
- Curriculum V1/V2 traversal/import paths untouched (N/A for this milestone).
- Student dashboard / Mission card UX not redesigned; `as_mission_card()`
  projection provided for future cutover without changing student surfaces.
- No LLM introduced.
- One active adaptive mission per learner enforced via supersede-on-activate.

## Technical Debt

- Student dashboard still served by legacy / Twin-gated `PlanningService`
  surfaces; wiring `as_mission_card()` into the Mission card is a deliberate
  follow-up cutover, not part of AME-001.
- Evidence enrichment is best-effort when no workspace retrieval corpus exists;
  gap-driven missions still require Twin evidence ids from prior reasoning.
- Mission Engine v2 (`app/application/mission_engine_v2`) remains a separate
  journey-orchestration path; eventual consolidation is out of scope.

## Known Limitations

- No calendar scheduling (by design — abstract time budgets only).
- No student-facing Adaptive Mission UX beyond the existing simple Mission card.
- Activities remain abstract (review / practice / recovery / reflection).
- Does not replace legacy `Mission` / `MissionTask` ORM persistence.
