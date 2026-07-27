# PI-001A — Test Evidence

**Programme:** PI-001A — Founder Curriculum Studio Foundation  
**Date:** 2026-07-27  

---

## Commands

```bash
python3 -m ruff check \
  app/domain/curriculum_studio_foundation \
  app/application/curriculum_studio_foundation \
  app/models/curriculum_studio_foundation.py \
  app/presentation/curriculum_studio/forms.py \
  app/presentation/curriculum_studio/routes.py \
  app/presentation/curriculum_studio/view_models.py \
  tests/domain/curriculum_studio_foundation \
  tests/application/curriculum_studio_foundation

python3 -m pytest \
  tests/domain/curriculum_studio_foundation/ \
  tests/application/curriculum_studio_foundation/ \
  -v
```

## Results

| Check | Outcome |
|---|---|
| ruff | All checks passed |
| pytest foundation suite | **23 passed** |

Raw capture: `knowledge/product/pi001a/TEST_EVIDENCE_RAW.txt`

### Notable cases

| Test | Proves |
|---|---|
| `test_create_subject` | Create subject |
| `test_upload_documents_and_track_processing` | Upload + processing state |
| `test_review_validate_founder_review_publish` | Review → validate → approve → publish |
| `test_draft_never_appears_in_published_authority` | Students never consume drafts |
| `test_audit_trail_covers_lifecycle` | Every stage auditable |
| `test_subject_agnostic_second_subject` | `LAW1` onboarded without code changes |
| `test_end_to_end_foundation_lifecycle_persists` | Durable persistence end-to-end |
| `test_studio_upload_route_records_sources` | Founder upload HTTP path |
| `test_workspace_page_includes_upload_form` | Upload UI surface present |

Related presentation regressions also re-run green (navigation / workflow / rendering suites with upload CTA update).

## Alembic

```text
202607270001 (head)
```

Revision: `migrations/versions/202607270001_pi001a_curriculum_studio_foundation.py`
