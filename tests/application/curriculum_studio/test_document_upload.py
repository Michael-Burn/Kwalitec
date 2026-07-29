"""Phase 1 curriculum document upload tests."""

from __future__ import annotations

import hashlib
from io import BytesIO

import pytest

from app.application.curriculum_studio.document_upload_exceptions import (
    DocumentValidationError,
    DuplicateDocumentError,
)
from app.application.curriculum_studio.document_upload_service import (
    DocumentUploadService,
)
from app.domain.curriculum_documents.processing_stage import DocumentProcessingStage
from app.infrastructure.adapters.document_storage import (
    LocalDocumentStorageAdapter,
    QueuedDocumentProcessingAdapter,
)
from app.models.curriculum_studio_foundation import StudioFoundationDocument
from app.presentation.curriculum_studio.factory import (
    get_document_upload_service,
    set_studio_service,
)
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)
from tests.presentation.curriculum_studio.helpers import login_founder

# Minimal structurally valid PDF (magic + EOF).
MINIMAL_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj<<>>endobj\n"
    b"trailer<<>>\n"
    b"%%EOF\n"
)


@pytest.fixture
def upload_env(app, tmp_path, ctx):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-doc1", subject_code="CS1")
    studio.create_subject("CS1", title="Core Statistics")
    set_studio_service(studio, app=app)
    storage = LocalDocumentStorageAdapter(tmp_path / "docs")
    svc = DocumentUploadService(
        studio=studio,
        storage=storage,
        processing=QueuedDocumentProcessingAdapter(),
        max_bytes=1024 * 1024,
    )
    return studio, svc, storage


def test_local_storage_put_get_roundtrip(tmp_path):
    store = LocalDocumentStorageAdapter(tmp_path / "store")
    result = store.put(storage_key="cs1/cmp/v1/a.pdf", data=MINIMAL_PDF)
    assert result.byte_size == len(MINIMAL_PDF)
    assert result.checksum_sha256 == hashlib.sha256(MINIMAL_PDF).hexdigest()
    assert store.exists("cs1/cmp/v1/a.pdf")
    assert store.get("cs1/cmp/v1/a.pdf") == MINIMAL_PDF


def test_upload_stores_metadata_and_links_workspace(upload_env, ctx):
    studio, svc, storage = upload_env
    view = svc.upload(
        "ws-doc1",
        kind="cmp",
        filename="Official CMP.pdf",
        data=MINIMAL_PDF,
        actor_id="founder-1",
    )
    assert view.kind == "cmp"
    assert view.filename == "Official_CMP.pdf"
    assert view.byte_size == len(MINIMAL_PDF)
    assert view.version_number == 1
    assert view.processing_stage == DocumentProcessingStage.QUEUED.value
    payload = view.to_dict()
    assert "reference" not in payload
    assert "storage_key" not in payload
    assert all("ref://" not in str(v) for v in payload.values())

    row = StudioFoundationDocument.query.get(view.document_id)
    assert row is not None
    assert row.reference.startswith("ref://cmp/")
    assert row.storage_key
    assert storage.exists(row.storage_key)
    assert row.is_active is True

    facts = studio.registry.get_workspace("ws-doc1").facts
    assert facts.cmp_uploaded is True


def test_upload_rejects_non_pdf(upload_env, ctx):
    _, svc, _ = upload_env
    with pytest.raises(DocumentValidationError) as exc:
        svc.upload(
            "ws-doc1",
            kind="cmp",
            filename="notes.txt",
            data=b"not a pdf %%EOF",
        )
    assert exc.value.code == "not_pdf"


def test_upload_rejects_corrupt_pdf(upload_env, ctx):
    _, svc, _ = upload_env
    with pytest.raises(DocumentValidationError) as exc:
        svc.upload(
            "ws-doc1",
            kind="syllabus",
            filename="broken.pdf",
            data=b"%PDF-1.4\nno eof marker here",
        )
    assert exc.value.code == "corrupt_pdf"


def test_duplicate_upload_rejected(upload_env, ctx):
    _, svc, _ = upload_env
    svc.upload("ws-doc1", kind="cmp", filename="a.pdf", data=MINIMAL_PDF)
    with pytest.raises(DuplicateDocumentError):
        svc.upload("ws-doc1", kind="cmp", filename="a.pdf", data=MINIMAL_PDF)


def test_replace_archives_previous_version(upload_env, ctx):
    _, svc, _ = upload_env
    first = svc.upload("ws-doc1", kind="cmp", filename="a.pdf", data=MINIMAL_PDF)
    second_pdf = MINIMAL_PDF + b"% comment\n%%EOF\n"
    second = svc.replace(
        "ws-doc1",
        first.document_id,
        filename="b.pdf",
        data=second_pdf,
        actor_id="founder-1",
    )
    assert second.version_number == 2
    prior = StudioFoundationDocument.query.get(first.document_id)
    assert prior.is_active is False
    active = StudioFoundationDocument.query.get(second.document_id)
    assert active.is_active is True


def test_remove_updates_checklist(upload_env, ctx):
    studio, svc, _ = upload_env
    view = svc.upload("ws-doc1", kind="cmp", filename="a.pdf", data=MINIMAL_PDF)
    svc.remove("ws-doc1", view.document_id)
    facts = studio.registry.get_workspace("ws-doc1").facts
    assert facts.cmp_uploaded is False


def test_status_cta_states(upload_env, ctx):
    _, svc, _ = upload_env
    status = svc.status("ws-doc1")
    assert status.cta_state == "upload"
    assert status.all_required_uploaded is False
    svc.upload("ws-doc1", kind="cmp", filename="a.pdf", data=MINIMAL_PDF)
    other = MINIMAL_PDF + b" \n%%EOF\n"
    svc.upload("ws-doc1", kind="syllabus", filename="b.pdf", data=other)
    status = svc.status("ws-doc1")
    assert status.all_required_uploaded is True
    assert status.cta_state == "uploaded"
    for doc in status.documents:
        assert "reference" not in doc.to_dict()
        assert "storage_key" not in doc.to_dict()


def test_http_upload_and_status(client, app, ctx, tmp_path):
    app.config["DOCUMENT_STORAGE_ROOT"] = str(tmp_path / "http-docs")
    login_founder(client, app)
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-http1", subject_code="CS1")
    studio.create_subject("CS1", title="Core Statistics")
    set_studio_service(studio, app=app)

    response = client.post(
        "/console/studio/workspaces/ws-http1/documents",
        data={
            "kind": "cmp",
            "file": (BytesIO(MINIMAL_PDF), "cmp.pdf"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["document"]["kind"] == "cmp"
    assert "ref://" not in str(payload)

    status = client.get("/console/studio/workspaces/ws-http1/documents/status")
    assert status.status_code == 200
    body = status.get_json()
    assert body["ok"] is True
    assert body["status"]["documents"][0]["filename"] == "cmp.pdf"


def test_workspace_page_shows_upload_cards(client, app, ctx):
    login_founder(client, app)
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-ui1", subject_code="CS1")
    set_studio_service(studio, app=app)
    response = client.get("/console/studio/workspaces/ws-ui1")
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Official CMP" in text
    assert "Official Syllabus" in text
    assert "CMP reference" not in text
    assert "ref://" not in text
    assert "Upload documents" in text
    assert "data-document-upload" in text
    assert "document_upload.js" in text


def test_factory_builds_upload_service(app, ctx):
    studio, _, _, _ = make_studio_with_ports()
    set_studio_service(studio, app=app)
    svc = get_document_upload_service()
    assert isinstance(svc, DocumentUploadService)
    slots = svc.upload_slots()
    assert {s["kind"] for s in slots} == {"cmp", "syllabus"}
