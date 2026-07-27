"""Integration tests for Curriculum Studio foundation + presentation upload."""

from __future__ import annotations

from io import BytesIO

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.presentation.curriculum_studio.factory import set_studio_service
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)
from tests.presentation.curriculum_studio.helpers import login_founder


def test_end_to_end_foundation_lifecycle_persists(ctx):
    service = CurriculumStudioFoundationService()
    authority = PublishedCurriculumAuthority()

    service.create_subject("INT1", title="Integration Subject", actor_id="founder")
    version = service.create_version("INT1", "2026.1", actor_id="founder")
    structure = {
        "entries": [
            {
                "entry_id": "s1",
                "entry_type": "section",
                "text": "Section A",
                "number": "1",
            },
            {
                "entry_id": "t1",
                "entry_type": "topic",
                "text": "Topic A",
                "number": "1.1",
                "parent_ref": "s1",
            },
            {
                "entry_id": "o1",
                "entry_type": "objective",
                "text": "Objective A",
                "number": "1",
                "parent_ref": "t1",
            },
        ]
    }
    service.upload_document(
        version.version_id,
        kind="cmp",
        reference="ref://cmp/int1",
        structure=structure,
        actor_id="founder",
    )
    service.upload_document(
        version.version_id,
        kind="syllabus",
        reference="ref://syllabus/int1",
        structure=structure,
        actor_id="founder",
    )
    processing = service.process_curriculum(version.version_id, actor_id="founder")
    assert processing.processing_state
    parsed = service.review_parsed_curriculum(version.version_id)
    assert parsed.topics
    service.validate_curriculum(version.version_id, actor_id="founder")
    service.founder_review(version.version_id, actor_id="founder")
    published = service.publish_curriculum(version.version_id, actor_id="founder")

    # Simulate "new request" by reading through authority only.
    active = authority.get_active("INT1")
    assert active is not None
    assert active.package_id == published.package_id
    assert "structure" in active.package
    assert authority.get_active("MISSING") is None

    events = service.list_audit_events(subject_code="INT1")
    assert len(events) >= 6


def test_studio_document_upload_route_records_sources(client, ctx, app, tmp_path):
    pdf = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
    app.config["DOCUMENT_STORAGE_ROOT"] = str(tmp_path / "docs")
    login_founder(client, app)
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-up1", subject_code="CS1")
    studio.create_subject("CS1", title="Core Statistics")
    studio.versions.assign_version("ws-up1", "2026.1", version_id="ver-up1")
    set_studio_service(studio, app=app)

    response = client.post(
        "/console/studio/workspaces/ws-up1/documents",
        data={
            "kind": "cmp",
            "file": (BytesIO(pdf), "cmp.pdf"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.get_json()["ok"] is True
    other = pdf + b" \n%%EOF\n"
    response = client.post(
        "/console/studio/workspaces/ws-up1/documents",
        data={
            "kind": "syllabus",
            "file": (BytesIO(other), "syllabus.pdf"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    facts = studio.registry.get_workspace("ws-up1").facts
    assert facts.cmp_uploaded is True
    assert facts.official_syllabus_uploaded is True


def test_workspace_page_includes_document_upload_cards(client, ctx, app):
    login_founder(client, app)
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-form1")
    set_studio_service(studio, app=app)
    response = client.get("/console/studio/workspaces/ws-form1")
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Official CMP" in text
    assert "Official Syllabus" in text
    assert "CMP reference" not in text
    assert "data-document-upload" in text
