# SDT-001 — Student Digital Twin Foundation

## Summary

SDT-001 establishes the canonical Student Digital Twin: the sole source of truth
for learner educational state. Observations are append-only facts;
`StudentReasoningService` deterministically derives mastery, multi-dimensional
learning state, confidence, evidence-backed knowledge gaps, recommendations, and
prediction scaffolds. Curriculum evidence is retrieved exclusively through
`CurriculumRetrievalService`. CS-DOC-001 and CIP-001 → CIP-003 remain intact.
No LLM dependency was introduced.

## Files Created

- `app/domain/student_digital_twin/__init__.py`
- `app/domain/student_digital_twin/student.py`
- `app/domain/student_digital_twin/observation.py`
- `app/domain/student_digital_twin/learning_state.py`
- `app/domain/student_digital_twin/mastery.py`
- `app/domain/student_digital_twin/knowledge_gap.py`
- `app/domain/student_digital_twin/confidence.py`
- `app/domain/student_digital_twin/goal.py`
- `app/domain/student_digital_twin/recommendation.py`
- `app/domain/student_digital_twin/prediction.py`
- `app/domain/student_digital_twin/timeline.py`
- `app/domain/student_digital_twin/reasoning.py`
- `app/domain/student_digital_twin/student_digital_twin.py`
- `app/application/student_digital_twin/__init__.py`
- `app/application/student_digital_twin/persistence.py`
- `app/application/student_digital_twin/student_digital_twin_service.py`
- `app/application/student_digital_twin/observation_service.py`
- `app/application/student_digital_twin/mastery_service.py`
- `app/application/student_digital_twin/learning_state_service.py`
- `app/application/student_digital_twin/knowledge_gap_service.py`
- `app/application/student_digital_twin/recommendation_service.py`
- `app/application/student_digital_twin/prediction_service.py`
- `app/application/student_digital_twin/student_reasoning_service.py`
- `app/models/student_digital_twin.py`
- `app/presentation/student_digital_twin/__init__.py`
- `app/presentation/student_digital_twin/routes.py`
- `app/presentation/student_digital_twin/serializers.py`
- `migrations/versions/202607270008_sdt001_student_digital_twin.py`
- `tests/application/student_digital_twin/__init__.py`
- `tests/application/student_digital_twin/test_student_digital_twin.py`
- `knowledge/product/sdt001/ARCHITECTURE.md`
- `knowledge/product/sdt001/COMPLETION_REPORT.md`

## Files Modified

- `app/domain/curriculum_retrieval/profile.py` (additive `STUDENT_DIGITAL_TWIN` profile)
- `app/models/__init__.py`
- `app/__init__.py` (model registration + Twin diagnostics blueprint)
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Tests Executed

```
python3 -m pytest tests/application/student_digital_twin/ \
  tests/application/curriculum_retrieval/test_evidence_retrieval.py \
  tests/application/curriculum_intelligence/test_pipeline.py \
  tests/application/curriculum_intelligence/test_validation_provenance.py -q
# 50 passed

python3 -m ruff check app/domain/student_digital_twin \
  app/application/student_digital_twin \
  app/models/student_digital_twin.py \
  app/presentation/student_digital_twin \
  app/domain/curriculum_retrieval/profile.py \
  tests/application/student_digital_twin \
  migrations/versions/202607270008_sdt001_student_digital_twin.py
# All checks passed
```

### Test coverage

- Twin creation (idempotent scope)
- Observation recording + immutability
- Mastery and learning-state updates
- Knowledge-gap generation requires retrieval evidence
- Recommendation generation + prediction scaffolding
- Deterministic reasoning (same inputs → same inferences)
- Persistence round-trip
- CurriculumRetrievalService integration contract
- Founder diagnostic endpoints
- CIP-001 / CIP-002 / CIP-003 regression suites

## Migration Impact

Requires `flask db upgrade` to revision `202607270008`.

Additive tables only:

| Table | Purpose |
|---|---|
| `student_digital_twins` | Twin root |
| `student_observations` | Append-only facts |
| `mastery_records` | Current mastery |
| `knowledge_gaps` | Evidence-backed gaps |
| `learning_state_snapshots` | Append-only state history |
| `recommendations` | Twin recommendations |
| `predictions` | Prediction scaffolds |
| `reasoning_history` | Append-only reasoning audit |

No changes to CIP, CS-DOC, or student experience schema.

## Architecture Compliance

- Clean Architecture / DDD bounded context under `student_digital_twin`
- HTTP in presentation; reasoning in application; contracts in domain
- Curriculum V1/V2 JSON engine untouched
- CS-DOC-001 / CIP-001 / CIP-002 / CIP-003 invariants preserved
- Curriculum access only via `CurriculumRetrievalService`
- No LLM / no AI inference in reasoning path

## Technical Debt

- Legacy Twin packages (`app/domain/student_twin`, `app/domain/twin`,
  `TwinSnapshot`) coexist; a future milestone should formally migrate consumers
  onto SDT-001.
- Prediction algorithms are scaffolds (`sdt001.scaffold_v1`) only.
- Founder observation POST that triggers live reasoning depends on indexed CIP
  evidence in the workspace; diagnostics tests stub retrieval for isolation.

## Known Limitations

- No tutoring, adaptive missions, or student-facing Twin UX
- Goals are modelled but not yet driven by a goal-setting workflow
- Knowledge gaps are only created when retrieval returns evidence
- Existing Student Experience runtime still uses prior Twin adapters

## Success Criteria

| Criterion | Status |
|---|---|
| StudentDigitalTwin as canonical learner aggregate | ✓ |
| Observations immutable and append-only | ✓ |
| StudentReasoningService deterministically updates Twin | ✓ |
| Mastery evidence-backed | ✓ |
| Knowledge gaps evidence-backed via retrieval | ✓ |
| Curriculum only via CurriculumRetrievalService | ✓ |
| Founder diagnostics expose Twin state | ✓ |
| Existing curriculum infrastructure unchanged | ✓ |
| No LLM dependency | ✓ |
