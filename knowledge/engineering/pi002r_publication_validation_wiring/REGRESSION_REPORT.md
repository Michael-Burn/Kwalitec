# Regression Report

**Programme:** PI-002R

---

## Safety gates — still enforced

| Scenario | Expected | Test |
|---|---|---|
| Empty curriculum / no structure | ValidationError | `test_regression_empty_structure_fails_prepare` |
| Missing version | ValidationError | `test_regression_validation_requires_version` |
| Approval without validation | PublicationError | `test_regression_approval_requires_validation` |
| Publish without checklist | PublicationError | `test_regression_publish_requires_checklist` |
| Management ValidationPolicy failure | ValidationError; `validation_passed=False` | `test_regression_management_failure_blocks_validation` |
| Mutating actions require Management port | PortUnavailable | Existing `test_authority_boundaries` |

---

## Blueprint / package rules

Management `ValidationPolicy` unchanged:
- Empty package → blocking  
- Missing syllabus → blocking  
- Missing blueprint assignments → error/blocking  
- Missing CMP / learning-objectives → warnings  

Studio still assigns default blueprints via Structure Preparation before the gate so a coherent Founder path can pass **without inventing curriculum content**.

---

## What was intentionally changed (not regressions)

| Behaviour | Before | After |
|---|---|---|
| Reference-only `upload_sources` | Started stub Ingestion | Does not start Ingestion |
| Stub job in registry | Failed Studio validate | Ignored for publication gate |
| `_map_report` | Ignored `issues[]` | Maps `issues[]` |
| Preview success flash | Topics alone | Requires ready + validated |

---

## Commands run

```bash
python3 -m pytest \
  tests/application/curriculum_studio/test_pi002r_validation_wiring.py \
  tests/application/curriculum_studio/test_use_cases.py \
  tests/application/curriculum_studio/test_orchestration_matrix.py \
  tests/application/curriculum_studio/test_workflow_completion_r1.py \
  tests/application/curriculum_studio/test_services.py \
  tests/presentation/curriculum_studio/test_view_models.py \
  -q
```

**Result:** 372 passed

```bash
python3 -m ruff check app/application/curriculum_studio/validation_service.py \
  app/application/curriculum_studio/workspace_service.py \
  app/application/curriculum_studio/preview_service.py \
  app/application/curriculum_studio/document_upload_service.py \
  app/presentation/curriculum_studio/operator_guidance.py \
  app/presentation/curriculum_studio/routes.py \
  app/infrastructure/adapters/curriculum_management/adapter.py \
  tests/application/curriculum_studio/test_pi002r_validation_wiring.py
```

**Result:** clean
