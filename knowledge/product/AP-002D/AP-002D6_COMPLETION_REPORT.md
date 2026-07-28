# AP-002D6 — Completion Report

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D6 — Tutor Explainability Integration  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit message:** `feat(ap-002d6): integrate tutor explainability with educational provenance`  
**Commit:** `0bf8185`

---

### Summary

Integrated the Tutor with the Educational Intelligence Platform as an **explanation-only** service. `TutorExplanationService` consumes validated `EducationalDecisionSet` + Twin belief (+ optional `StudyMissionPlan` / Learning Graph structure), builds deterministic provenance-backed explanation sections via `ExplanationBuilder`, validates fail-closed, and emits factual explanation events. The Tutor never reasons, never plans missions, never estimates mastery independently, and never fabricates missing educational context. Assessment, Evidence Packaging, StudentReasoningService, Twin semantics, Mission Engine, and Learning Graph were not modified.

### Explanation objects

| Object | Role |
|---|---|
| `TutorExplanation` | Immutable learner-facing explanation artefact |
| `ExplanationSection` | Base provenance-backed narration unit |
| `DecisionExplanation` | Narrates a validated EducationalDecision |
| `EvidenceExplanation` | Narrates evidence bundle / observation ids (not raw responses) |
| `MissionExplanation` | Narrates why a StudyMissionPlan was selected |
| `ConceptExplanation` | Narrates concepts that influenced the explanation |
| `LearningObjectiveExplanation` | Narrates involved learning objectives |
| `ExplanationContext` | Twin / decision / mission / correlation / version context |
| `ExplanationReference` | Decision → observation → evidence identity chain |
| `ExplanationVersion` | Contract version `AP-002D6.explanation.v1` |
| `ExplanationResult` | Context + explanation + factual events |

### Traceability model

Every learner-facing section records:

- decision id / decision version / twin version
- evidence bundle id / educational observation ids
- reasoning request id / assessment session id / correlation id
- explanation version + optional mission plan id / mission id
- learning objective / concept when applicable

Unavailable paths state uncertainty explicitly — never invent missing provenance.

### Validation

Rejects explicitly (never invents missing context):

- Missing / incomplete provenance
- Unsupported explanation contracts (`AP-002D6.explanation.v1` only)
- Invalid decision versions
- Twin version mismatch (context / mission / Twin)
- Mission planning version mismatch
- Broken concept / learning-objective references
- Unknown explanation section schema
- Duplicate explanation requests (strict raise or idempotent skip)

### Versioning

- Explanation contract: `AP-002D6.explanation.v1`
- Accepts Twin decisions at `AP-002D3.decision.v1`
- Accepts mission plans at `AP-002D5.planning.v1`
- Append-only in-process ledger supports audit / replay

### Events

Factual only (no orchestration / Reasoning callbacks):

- `TutorExplanationRequested`
- `TutorExplanationGenerated`
- `TutorExplanationUnavailable`

### Tests

- Domain: version, section catalogue, reference requirements, events, immutability
- Application: generation, traceability, determinism, replay, missing provenance, soft-decision uncertainty, empty decision set, version compatibility, twin/mission mismatch, DTO mapping, IntelligentTutorService wiring, Mission→Tutor pipeline, no exam-outcome prediction, StudentReasoningService untouched regression
- Architecture purity: required structure; forbidden Assessment / ReasoningService / Twin-write / Mission CandidateBuilder authority

### Deferred work for AP-002D7

- Wire Tutor explanation after D5 mission planning inside broader pipeline orchestration (without modifying Reasoning / Mission authority)
- Materialise Tutor explanations into student-visible Home / Coach / Mission surfaces + feature flags
- Durable DB-backed explanation audit tables if founder diagnostics require SQL persistence beyond existing Tutor rows
- MES / student-language polish of section bodies without adding educational reasoning
- Adaptive assessment intent triggering remains **AP-002E**

---

### Files Created

**Domain**

- `app/domain/intelligent_tutor/explainability/__init__.py`
- `app/domain/intelligent_tutor/explainability/context.py`
- `app/domain/intelligent_tutor/explainability/errors.py`
- `app/domain/intelligent_tutor/explainability/events.py`
- `app/domain/intelligent_tutor/explainability/explanation.py`
- `app/domain/intelligent_tutor/explainability/reference.py`
- `app/domain/intelligent_tutor/explainability/result.py`
- `app/domain/intelligent_tutor/explainability/section.py`
- `app/domain/intelligent_tutor/explainability/version.py`

**Application**

- `app/application/intelligent_tutor/explainability/__init__.py`
- `app/application/intelligent_tutor/explainability/errors.py`
- `app/application/intelligent_tutor/explainability/explanation_builder.py`
- `app/application/intelligent_tutor/explainability/persistence.py`
- `app/application/intelligent_tutor/explainability/tutor_explanation_service.py`
- `app/application/intelligent_tutor/explainability/validator.py`
- `app/application/intelligent_tutor/explainability/versions.py`
- `app/application/intelligent_tutor/dto/__init__.py`
- `app/application/intelligent_tutor/dto/explanation_dto.py`
- `app/application/intelligent_tutor/mappers/__init__.py`
- `app/application/intelligent_tutor/mappers/explanation_mapper.py`

**Tests**

- `tests/domain/intelligent_tutor/test_explainability.py`
- `tests/application/intelligent_tutor/conftest_explainability.py`
- `tests/application/intelligent_tutor/test_tutor_explainability.py`
- `tests/application/intelligent_tutor/test_explainability_architecture_purity.py`

**Docs**

- `knowledge/product/AP-002D/AP-002D6_COMPLETION_REPORT.md` (this file)

### Files Modified

- `app/application/intelligent_tutor/intelligent_tutor_service.py` — `explain_from_decisions` + explanation service wiring
- `app/application/intelligent_tutor/__init__.py` — export explainability API
- `app/domain/intelligent_tutor/__init__.py` — export explanation domain objects

### Tests Executed

```bash
.venv/bin/python -m pytest tests/domain/intelligent_tutor/test_explainability.py \
  tests/application/intelligent_tutor/test_tutor_explainability.py \
  tests/application/intelligent_tutor/test_explainability_architecture_purity.py -q
.venv/bin/python -m pytest -q
.venv/bin/ruff check app/domain/intelligent_tutor/explainability \
  app/application/intelligent_tutor/explainability \
  app/application/intelligent_tutor/dto app/application/intelligent_tutor/mappers \
  app/application/intelligent_tutor/intelligent_tutor_service.py \
  app/application/intelligent_tutor/__init__.py \
  app/domain/intelligent_tutor/__init__.py \
  tests/domain/intelligent_tutor \
  tests/application/intelligent_tutor/test_tutor_explainability.py \
  tests/application/intelligent_tutor/test_explainability_architecture_purity.py \
  tests/application/intelligent_tutor/conftest_explainability.py
# Alembic head: 202607270013 (unchanged)
```

Outcomes: explainability suites passed (46); full suite **44377 passed**, 7 skipped; milestone paths ruff clean; single Alembic head unchanged.

Note: repository-wide `ruff check .` may still report pre-existing errors outside this milestone’s paths (same posture as AP-002D1–D5).

### Migration Impact

None.

### Architecture Compliance

Layering preserved: Twin owns learner belief; Mission Engine owns scheduling/planning; Tutor owns explanation only. Explanation services do not call Reasoning, Assessment, Mission CandidateBuilder, or write Twin inferences. Curriculum V1/V2 traversal unaffected (N/A). Architecture purity tests forbid Assessment/ReasoningService/Twin-write authority creep in explainability packages. `StudentReasoningService` remains unmodified (explicit STOP boundary).

### Technical Debt

- Explanation ledger is in-process (append-only) rather than Alembic-backed tables — sufficient for deterministic replay/tests; durable SQL audit deferred.
- Section prose is deterministic structured English; student-language MES cutover deferred to AP-002D7 surface work.

### Known Limitations

- Does not auto-invoke Tutor explanation after D5 mission planning (explicit constraint — deferred wiring).
- Does not change student-visible Tutor / Home / Mission UI templates.
- Adaptive assessment triggering remains AP-002E.

### Student Impact Assessment

**N/A for this explanation-service milestone** as a student-facing surface change (no UI). When Tutor explanations are cut over onto Home/Coach/Mission surfaces, assess student value explicitly. Educational benefit intended: every Tutor statement can be traced to validated Twin decisions and evidence identifiers without a second educational brain.

### Estimated KSI contribution

ΔKSI ≈ 0 for student-visible surfaces until cutover. Enables future K8 integrity claims once Tutor narration is the sole explanation consumer of Twin / Mission provenance.

### Evidence collected

- Explainability tests under `tests/application/intelligent_tutor/` and `tests/domain/intelligent_tutor/`
- Full regression: 44377 passed
- Architecture purity tests in the Tutor explainability package

### Lessons learned for student value

Keeping “what do you know?” and “what next?” off the Tutor forces every narration to cite a Twin decision and evidence identifiers — students can always ask “why?” and land on reasoned provenance, not invented confidence.

### Explainability Review

N/A — no student-facing intelligence surface changes in this milestone (explanation is service-level only). Checklist execution belongs to the cutover programme that surfaces these artefacts to students.

### Recommendation Quality Review

N/A — recommendations are not generated or re-ranked on the D6 path; Tutor narrates validated decisions and planned missions only.

### Version 1 readiness residual

N/A — no Version 1 production-ready declaration claimed.
