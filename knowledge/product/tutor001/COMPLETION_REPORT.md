# TUTOR-001 — Evidence-Backed Intelligent Tutor

## Summary

TUTOR-001 delivers Kwalitec’s Evidence-Backed Intelligent Tutor: a bounded
context that explains educational decisions already produced by the Student
Digital Twin, Educational Reasoning Engine, Learning Graph, Adaptive Mission
Engine, Assessment Pipeline, and Curriculum Retrieval. The Tutor never
performs educational reasoning itself. Every response assembles structured
evidence before generation. Prose is produced behind `TutorGenerationPort`
with a deterministic Version 1 placeholder (no LLM). Conversation state is
session-scoped and isolated from Twin learner state. Founder diagnostics live
under `/founder/tutor/*`. Student Home gains a light Tutor preview and
“Explain today's mission” action without redesigning the application.
CS-DOC-001, CIP-001 → CIP-003, SDT-001 → SDT-003, AME-001, and AP-001 remain
intact.

## Files Created

- `app/domain/intelligent_tutor/__init__.py`
- `app/domain/intelligent_tutor/tutor_session.py`
- `app/domain/intelligent_tutor/tutor_context.py`
- `app/domain/intelligent_tutor/tutor_question.py`
- `app/domain/intelligent_tutor/tutor_response.py`
- `app/domain/intelligent_tutor/explanation.py`
- `app/domain/intelligent_tutor/learning_hint.py`
- `app/domain/intelligent_tutor/coaching_message.py`
- `app/domain/intelligent_tutor/conversation_memory.py`
- `app/domain/intelligent_tutor/response_evidence.py`
- `app/domain/intelligent_tutor/response_builder.py`
- `app/application/intelligent_tutor/__init__.py`
- `app/application/intelligent_tutor/intelligent_tutor_service.py`
- `app/application/intelligent_tutor/persistence.py`
- `app/application/intelligent_tutor/ports/__init__.py`
- `app/application/intelligent_tutor/ports/tutor_generation_port.py`
- `app/application/intelligent_tutor/ports/deterministic_tutor_generation.py`
- `app/models/intelligent_tutor.py`
- `app/presentation/intelligent_tutor/__init__.py`
- `app/presentation/intelligent_tutor/routes.py`
- `migrations/versions/202607270013_tutor001_intelligent_tutor.py`
- `tests/application/intelligent_tutor/__init__.py`
- `tests/application/intelligent_tutor/test_intelligent_tutor.py`
- `knowledge/product/tutor001/ARCHITECTURE.md`
- `knowledge/product/tutor001/COMPLETION_REPORT.md`

## Files Modified

- `app/models/__init__.py` (register Tutor ORM models)
- `app/__init__.py` (model import + `/founder/tutor` blueprint)
- `app/presentation/student/forms.py` (`ExplainMissionTutorForm`)
- `app/presentation/student/routes.py` (`/student/tutor/explain-mission`)
- `app/presentation/student/view_models.py` (Tutor Home preview fields)
- `app/templates/student/home.html` (Tutor preview in Coach panel)
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Tests Executed

```
python3 -m pytest tests/application/intelligent_tutor/ \
  tests/application/adaptive_mission/ \
  tests/application/assessment_pipeline/ \
  tests/application/learning_graph/ \
  tests/application/educational_reasoning/ \
  tests/application/student_digital_twin/ -q
# 67 passed

python3 -m ruff check app/domain/intelligent_tutor \
  app/application/intelligent_tutor \
  app/presentation/intelligent_tutor \
  app/models/intelligent_tutor.py \
  tests/application/intelligent_tutor
# All checks passed
```

## Migration Impact

Alembic revision `202607270013` (revises `202607270012`) adds:

| Table | Purpose |
|---|---|
| `tutor_sessions` | Conversation session + lightweight memory JSON |
| `tutor_messages` | Student / Tutor messages |
| `tutor_explanations` | Structured explanations |
| `tutor_feedback` | Optional response feedback |

Does not alter SDT-001 / SDT-002 / SDT-003 / AME-001 / AP-001 tables. Does not
duplicate Twin inference rows.

## Architecture Compliance

- Layering preserved: domain → application → presentation; no HTTP in services.
- Tutor consumes Twin / Reasoning / Graph / Mission / Assessment / Retrieval —
  does not duplicate educational logic.
- Curriculum evidence exclusively via `CurriculumRetrievalService`
  (`RetrievalProfile.TUTOR`).
- Curriculum V1/V2 traversal/import paths untouched (N/A for this milestone).
- Student Home extended lightly (Coach Tutor preview + explain-mission action);
  no dashboard redesign.
- Future LLM integration abstracted behind `TutorGenerationPort`.
- Conversation memory isolated from Twin learner state.

## Technical Debt

- Student Home Twin lookup uses `list_twins_for_student(str(user.id))`; learners
  whose Twin `student_id` is not the Flask user id will not see the preview
  until identity wiring is unified.
- Deterministic placeholder generation is readable but not conversational;
  LLM adapter is intentionally deferred.
- Tutor does not yet stream multi-turn UI beyond session persistence + Founder
  diagnostics (Home uses flash for full explain-mission responses).

## Known Limitations

- No live LLM / external model integration.
- Tutor does not invent recommendations, missions, or mastery updates.
- Assessment feedback in Tutor context is a summary of recent AP-001 feedback
  rows, not a re-scoring path.
- Founder `/founder/tutor/*` endpoints are diagnostic only.
