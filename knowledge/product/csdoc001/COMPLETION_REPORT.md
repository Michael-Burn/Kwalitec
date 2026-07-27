# CS-DOC-001 — Curriculum Document Upload (Phase 1)

## Summary

Phase 1 delivers a production-ready PDF upload path for Curriculum Studio:
Founders upload Official CMP and Official Syllabus PDFs via reusable cards;
the system stores bytes outside SQL, mints internal `ref://` URIs, links the
workspace checklist, and enqueues processing at stage `queued` for Phase 2+.

## Architecture changes

```
Founder UI (DocumentUploadCard)
  → Blueprint multipart/JSON routes
  → DocumentUploadService
       → DocumentStoragePort (LocalDocumentStorageAdapter)
       → StudioFoundationDocument metadata
       → mint opaque ref://…
       → WorkspaceService.upload_sources (checklist)
       → DocumentProcessingPort (QueuedDocumentProcessingAdapter)
```

Domain contracts preserved: `CurriculumAsset`, `StudioFoundationDocument.reference`,
`WorkspaceService.upload_sources`, Founder RBAC (`founder_required`).

## Sequence (upload)

1. Founder drops/selects PDF on a registry-driven card
2. `POST …/documents` (multipart: kind + file)
3. Validate PDF magic + EOF + size
4. SHA-256 checksum; reject active duplicates
5. Ensure Management + foundation version
6. Archive prior active doc of same kind (if any)
7. Store bytes via DocumentStoragePort
8. Persist metadata row + opaque reference
9. Link workspace sources → checklist facts
10. Enqueue processing → stage `queued`
11. Return Founder-safe metadata JSON (no refs / storage keys)

## Files created

- `app/domain/curriculum_documents/` (registry + processing stages)
- `app/application/curriculum_studio/ports/document_storage_port.py`
- `app/application/curriculum_studio/ports/document_processing_port.py`
- `app/application/curriculum_studio/document_upload_service.py`
- `app/application/curriculum_studio/document_upload_exceptions.py`
- `app/application/curriculum_studio/dto/document_metadata.py`
- `app/infrastructure/adapters/document_storage/`
- `app/templates/curriculum_studio/_document_upload_card.html`
- `app/static/js/document_upload.js`
- `migrations/versions/202607270004_curriculum_document_file_metadata.py`
- `tests/application/curriculum_studio/test_document_upload.py`
- `knowledge/product/csdoc001/COMPLETION_REPORT.md`

## Files modified

- `app/models/curriculum_studio_foundation.py`
- `app/presentation/curriculum_studio/routes.py`
- `app/presentation/curriculum_studio/factory.py`
- `app/presentation/curriculum_studio/forms.py`
- `app/presentation/curriculum_studio/views.py`
- `app/presentation/curriculum_studio/view_models.py`
- `app/templates/curriculum_studio/workspace.html`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/application/curriculum_studio/validation_guidance.py`
- `app/application/curriculum_studio_foundation/service.py` (kind registry)
- `app/application/curriculum_studio/ports/__init__.py`
- `app/config.py`, `.env.example`
- Presentation / certification tests updated for new API

## Database changes

Alembic `202607270004` adds to `studio_foundation_documents`:

`workspace_id`, `original_filename`, `content_type`, `byte_size`,
`checksum_sha256`, `storage_key`, `version_number`, `is_active`,
`processing_stage` (+ indexes). **No PDF bytes in SQL.**

## API changes

| Method | Path |
|--------|------|
| POST | `/console/studio/workspaces/<id>/documents` |
| POST | `/console/studio/workspaces/<id>/documents/<doc_id>/replace` |
| GET | `/console/studio/workspaces/<id>/documents/<doc_id>/download` |
| DELETE | `/console/studio/workspaces/<id>/documents/<doc_id>` |
| GET | `/console/studio/workspaces/<id>/documents/status` |

Legacy string-ref `POST …/upload` removed from presentation (service
`upload_sources` retained for domain/tests).

## UI before / after

**Before:** CMP/Syllabus text inputs with `ref://` placeholders and
“Upload Sources”.

**After:** Registry-driven upload cards (drag/drop, browse, progress,
replace/download/remove, version/timestamp/size/status), CTA badge
(Upload / Replace / Documents Uploaded), Processing Status stages.

## Tests executed

```
python3 -m pytest tests/application/curriculum_studio/test_document_upload.py \
  tests/application/curriculum_studio_foundation/test_integration.py -q
```

## Migration impact

Requires `flask db upgrade` to revision `202607270004` on existing DBs.
Fresh test DBs create columns via `create_all`.

## Architecture compliance

Layering preserved (blueprints thin; orchestration in services; ports for
storage/processing). Curriculum V1/V2 JSON engine untouched. Opaque refs
remain domain-only; Founder never sees them.

## Technical debt

- Studio registry remains in-memory; durable docs are foundation-backed.
- Auto-assign version on first upload may surprise Founders who prefer
  explicit version labels first.
- Processing stages after `queued` are stubs until Phase 2 workers.
- Local filesystem storage only (S3/Azure/GCS adapters not yet shipped).

## Known limitations

- No OCR / text extraction / embeddings / vector / KG yet
- Phase 1 UI shows publish-required kinds only (CMP + Syllabus)
- Archived versions retained on disk but no Founder version-history browser

## Recommended Phase 2

1. Worker consuming `queued` → extract text (OCR if needed) → `processing` → `ready`
2. Feed structured extraction into `CurriculumIngestionEngine`
3. Chunk + embed + vector store hooks for Student Digital Twin
4. Enable additional registry kinds in UI (core reading, past papers, …)
5. Cloud object-storage adapter behind `DocumentStoragePort`
6. Founder version-history drawer for archived document versions

## Student Impact Assessment

N/A for Phase 1 (Founder authoring infrastructure only; no student-facing
recommendation/runtime change). Enables future authoritative curriculum
sources for the Student Digital Twin.

## Estimated KSI contribution

ΔKSI ≈ 0 for Phase 1 (infra/authoring). Future extraction/indexing phases
target K1/K2/K8 once student-facing intelligence consumes uploaded sources.

## Evidence collected

- `tests/application/curriculum_studio/test_document_upload.py`
- Updated foundation presentation integration tests
- Updated PR-001A certification upload negative path

## Lessons learned for student value

Founders cannot operationalise curriculum quality while typing storage URIs.
Document-first upload is a prerequisite for trustworthy AI curriculum
pipelines — Phase 1 removes that friction without claiming AI readiness yet.

## Explainability Review

N/A — no student-facing intelligence changed.

## Recommendation Quality Review

N/A — no recommendation ranking/selection changed.
