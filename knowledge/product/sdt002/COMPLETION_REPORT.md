# SDT-002 — Educational Reasoning Engine

## Summary

SDT-002 delivers Kwalitec’s deterministic Educational Reasoning Engine: a
bounded context that transforms learner observations into explainable
educational decisions via a fixed pipeline (observation → curriculum evidence →
rules → inference → Twin update → immutable history). `StudentReasoningService`
now delegates educational logic to `RuleRegistry` /
`EducationalReasoningEngine`. CS-DOC-001, CIP-001 → CIP-003, and the SDT-001
Twin aggregate remain intact. No LLM dependency was introduced.

## Files Created

- `app/domain/educational_reasoning/__init__.py`
- `app/domain/educational_reasoning/reasoning_engine.py`
- `app/domain/educational_reasoning/reasoning_rule.py`
- `app/domain/educational_reasoning/reasoning_result.py`
- `app/domain/educational_reasoning/reasoning_context.py`
- `app/domain/educational_reasoning/rule_registry.py`
- `app/domain/educational_reasoning/decision.py`
- `app/domain/educational_reasoning/explanation.py`
- `app/domain/educational_reasoning/confidence_update.py`
- `app/domain/educational_reasoning/mastery_update.py`
- `app/domain/educational_reasoning/gap_analysis.py`
- `app/domain/educational_reasoning/recommendation_rule.py`
- `app/domain/educational_reasoning/momentum_rule.py`
- `app/domain/educational_reasoning/consistency_rule.py`
- `app/domain/educational_reasoning/readiness_rule.py`
- `app/application/educational_reasoning/__init__.py`
- `app/application/educational_reasoning/curriculum_evidence_service.py`
- `app/application/educational_reasoning/educational_reasoning_service.py`
- `app/application/educational_reasoning/persistence.py`
- `app/models/educational_reasoning.py`
- `app/presentation/educational_reasoning/__init__.py`
- `app/presentation/educational_reasoning/routes.py`
- `migrations/versions/202607270009_sdt002_educational_reasoning.py`
- `tests/application/educational_reasoning/__init__.py`
- `tests/application/educational_reasoning/test_educational_reasoning.py`
- `knowledge/product/sdt002/ARCHITECTURE.md`
- `knowledge/product/sdt002/COMPLETION_REPORT.md`

## Files Modified

- `app/application/student_digital_twin/student_reasoning_service.py` (delegates to engine)
- `app/application/student_digital_twin/mastery_service.py` (facade over MasteryUpdateRule)
- `app/application/student_digital_twin/learning_state_service.py` (composed from rules)
- `app/application/student_digital_twin/knowledge_gap_service.py` (gap + prerequisite rules)
- `app/application/student_digital_twin/recommendation_service.py` (RecommendationRule)
- `app/application/student_digital_twin/__init__.py` (docstring)
- `app/models/__init__.py` (register reasoning ORM models)
- `app/__init__.py` (model import + `/founder/reasoning` blueprint)
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Tests Executed

```
python3 -m pytest tests/application/educational_reasoning/ \
  tests/application/student_digital_twin/ \
  tests/application/curriculum_retrieval/ -q
# 33 passed

python3 -m ruff check app/domain/educational_reasoning \
  app/application/educational_reasoning \
  app/application/student_digital_twin \
  app/presentation/educational_reasoning \
  app/models/educational_reasoning.py \
  tests/application/educational_reasoning
# All checks passed
```

## Migration Impact

Alembic revision `202607270009` (revises `202607270008`) adds:

| Table | Purpose |
|---|---|
| `educational_reasoning_runs` | Immutable engine cycle |
| `educational_rule_executions` | Per-rule execution trace |
| `reasoning_explanations` | Explainability payloads |
| `decision_records` | Educational decision metadata |

Does not alter SDT-001 Twin inference tables or CIP / CS-DOC schemas.

## Architecture Compliance

- Layering preserved: domain rules → application orchestration → presentation diagnostics.
- Curriculum V1/V2 traversal unchanged (N/A — no Curriculum Engine edits).
- CIP-003 contract preserved: evidence only via `CurriculumRetrievalService`
  with `STUDENT_DIGITAL_TWIN` profile.
- SDT-001 aggregate and observation immutability preserved.
- No LLM / probabilistic AI in the educational path.

## Technical Debt

- Live CIP retrieval can raise when filtering by `subject_code` against studio
  document metadata; `CurriculumEvidenceService` soft-fails to empty evidence
  so diagnostics remain available. Root cause belongs to CIP retrieval, not
  Twin state.
- Prediction scaffolds remain in Twin `PredictionService` (framework only);
  not yet a first-class engine rule.

## Known Limitations

- Not student-facing.
- Does not generate Adaptive Missions, tutoring dialogue, or full exam
  prediction algorithms.
- Founder `/founder/reasoning/run` without an indexed CIP workspace yields
  mastery/confidence updates but empty gaps/recommendations (by design —
  evidence-backed only).
