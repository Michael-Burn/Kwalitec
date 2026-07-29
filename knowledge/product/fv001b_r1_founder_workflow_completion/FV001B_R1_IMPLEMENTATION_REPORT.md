# FV-001B-R1 — Implementation Report

**Programme:** FV-001B-R1 — Founder Workflow Completion  
**Date:** 2026-07-28  
**Predecessor:** FV-001B (NO-GO) · PX-002  
**Scope:** Workflow completion and consistency — not EI redesign

---

## Summary

FV-001B-R1 closes the Founder Studio publication path so a Curriculum Authority user can complete:

**Create Subject → Upload Official Documents → Review Extraction → Approve → Publish → Observe Ready**

using only the visible Founder Studio, without contradictory messaging and without weakening publication safety.

Root causes addressed:

| P0 | Root cause | Fix |
|---|---|---|
| P0-1 | Management preview returned metadata without hierarchy; UI always flashed success | Map `section_refs` / assignments / CIP extraction into preview topics; refuse empty preview |
| P0-2 | Hidden checklist gates (`blueprint_assigned`, `rollback_snapshot`) unwired; approve before PREVIEW_READY | Auto-prepare structure + default blueprints on validate; preview advances gate; rollback auto-created on publish |
| P0-3 | Studio Management publish did not materialise Foundation packages | Publication bridge → Foundation approve + publish → Subject Catalogue Ready |
| P0-4 | Slot labels vs file chooser confusion | Kind-bound confirmation copy on each Official CMP / Official Syllabus card |
| P0-5 | Knowledge Graph / Pipeline / Entity Details / Inference on authoring chrome | Founder vocabulary on primary workspace surfaces |

---

## Files Created

- `app/application/curriculum_studio/structure_preparation_service.py`
- `app/application/platform_integration/publication_bridge.py`
- `tests/application/curriculum_studio/test_workflow_completion_r1.py`
- `knowledge/product/fv001b_r1_founder_workflow_completion/FV001B_R1_IMPLEMENTATION_REPORT.md` (this file)
- `knowledge/product/fv001b_r1_founder_workflow_completion/WORKFLOW_COMPLETION_REPORT.md`
- `knowledge/product/fv001b_r1_founder_workflow_completion/READY_STATE_VALIDATION.md`
- `knowledge/product/fv001b_r1_founder_workflow_completion/TERMINOLOGY_REVIEW.md`
- `knowledge/product/fv001b_r1_founder_workflow_completion/REGRESSION_REPORT.md`

---

## Files Modified

### Application / domain

- `app/application/curriculum_studio/validation_service.py` — prepare structure + blueprints before Management validate
- `app/application/curriculum_studio/preview_service.py` — payload mapping, `build_for_review`, CIP hierarchy fallback
- `app/application/curriculum_studio/publication_service.py` — preview gate on approve; rollback; Foundation Ready bridge
- `app/domain/curriculum_studio/curriculum_workspace.py` — `with_structure`
- `app/domain/curriculum_intelligence/pipeline_stage.py` — Founder stage labels
- `app/application/platform_integration/subject_catalogue.py` — Ready when published package exists
- `app/application/platform_integration/flags.py` — development default for publish→Ready discovery

### Presentation

- `app/presentation/curriculum_studio/routes.py` — meaningful preview flash; Subjects Ready rows
- `app/presentation/curriculum_studio/view_models.py` — preview/next-step copy; topic wording
- `app/presentation/curriculum_studio/operator_guidance.py` — empty-preview recovery
- `app/templates/curriculum_studio/workspace.html` — Founder terminology
- `app/templates/curriculum_studio/hub.html` — Ready / Current Version / Published Date
- `app/templates/curriculum_studio/_document_upload_card.html` — slot binding confirmation
- `app/application/curriculum_studio/document_upload_service.py` — document labels on processing jobs
- `app/static/js/curriculum_studio/document_upload.js` — extraction wording
- `app/static/js/curriculum_studio/curriculum_intelligence.js` — filter Inference/embeddings from audit chrome

### Tests

- `tests/presentation/curriculum_studio/test_view_models.py`
- `tests/presentation/curriculum_studio/test_volume.py`
- `tests/presentation/curriculum_studio/test_messaging.py`

---

## Safety preserved

- Management validation, approval, and publication policies still run.
- Empty packages / missing documents still block.
- Empty preview cannot flash success.
- Publish still requires checklist readiness; rollback snapshot is created as part of readiness, not skipped.
- Foundation publish still requires structure + approval.

---

## Recommendation

Re-run **FV-001B** blind Founder Studio validation on a clean instance after these changes. Expect GO only if the walk reaches **Ready** with consistent messaging and without EI chrome on the default path.
