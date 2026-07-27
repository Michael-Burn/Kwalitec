# PR-001A — Test Evidence

**Programme:** PR-001A — Founder Operations Certification  
**Date:** 2026-07-27  

---

## Commands

```bash
python3 -m ruff check \
  app/domain/curriculum_studio/validation_summary.py \
  app/application/curriculum_studio/validation_guidance.py \
  app/application/curriculum_studio/validation_service.py \
  app/application/curriculum_studio/dto/validation_snapshot.py \
  app/application/curriculum_studio/_snapshots.py \
  app/presentation/curriculum_studio/ \
  tests/certification/test_pr001a_founder_operations.py

python3 -m pytest \
  tests/certification/test_pr001a_founder_operations.py \
  tests/presentation/curriculum_studio/test_messaging.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/presentation/workflows/test_workflow_founder_studio.py \
  -v --tb=short
```

## Outcome

**Ruff:** All checks passed.  
**Pytest:** 129 passed (`test_pr001a_founder_operations` + related messaging/workflow/product-language suites).  

Raw log: [`TEST_EVIDENCE_RAW.txt`](TEST_EVIDENCE_RAW.txt).

## Acceptance mapping

| Criterion | Evidence |
|---|---|
| Create subject | `TestFounderHappyPath.test_create_subject` |
| Upload CMP/syllabus | `test_full_service_publish_path` upload_sources |
| Resolve validation | `TestValidationExperience` |
| Review extracted curriculum | preview/approve in full path |
| Publish successfully | `test_full_service_publish_path` |
| Verify availability | dashboard published_count assertion |
| Without developer intervention | Operator docs + recovery flashes |
| Recovery scenarios | `TestOperationalErrorRecovery` |
| Documentation alone | `TestOperatorDocumentation` + guides under `knowledge/product/pr001a/` |
