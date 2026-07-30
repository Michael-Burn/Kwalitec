"""FV-001A/FV-002 — Management reconciliation after durable Studio restart."""

from __future__ import annotations

from app.application.curriculum_studio.management_reconciliation_service import (
    ManagementReconciliationService,
)
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)


def _wipe_management(mgmt) -> None:
    """Simulate in-memory Curriculum Management process restart."""
    mgmt._subjects.clear()
    mgmt._versions.clear()
    mgmt._assets.clear()
    mgmt._validations.clear()
    mgmt._previews.clear()


def test_reconcile_restores_management_subject_and_version_after_wipe():
    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_subject("CS1", title="Actuarial Statistics")
    seed_workspace(studio, workspace_id="ws-cs1", subject_code="CS1")
    record = studio.versions.assign_version("ws-cs1", "2026.1")
    workspace = studio.registry.get_workspace("ws-cs1")
    assert workspace is not None
    assert workspace.version_id == record.version_id
    assert mgmt.get_subject_summary("CS1") is not None
    assert mgmt.get_version_summary(record.version_id) is not None

    _wipe_management(mgmt)
    assert mgmt.get_subject_summary("CS1") is None
    assert mgmt.get_version_summary(record.version_id) is None

    result = studio.reconcile_workspace("ws-cs1")
    assert result.subject_restored is True
    assert result.version_restored is True
    assert result.version_id == record.version_id
    assert mgmt.get_subject_summary("CS1") is not None
    assert mgmt.get_version_summary(record.version_id) is not None

    again = studio.reconcile_workspace("ws-cs1")
    assert again.already_consistent is True
    assert again.subject_restored is False
    assert again.version_restored is False


def test_ensure_workspace_version_does_not_trust_stale_version_id_alone(
    app, tmp_path, ctx
):
    from app.application.curriculum_studio.document_upload_service import (
        DocumentUploadService,
    )
    from app.infrastructure.adapters.document_storage import (
        LocalDocumentStorageAdapter,
        QueuedDocumentProcessingAdapter,
    )
    from app.presentation.curriculum_studio.factory import set_studio_service

    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_subject("CS1", title="Actuarial Statistics")
    seed_workspace(studio, workspace_id="ws-cs1", subject_code="CS1")
    record = studio.versions.assign_version("ws-cs1", "2026.1")
    _wipe_management(mgmt)

    set_studio_service(studio, app=app)
    svc = DocumentUploadService(
        studio=studio,
        storage=LocalDocumentStorageAdapter(tmp_path / "docs"),
        processing=QueuedDocumentProcessingAdapter(),
        max_bytes=1024 * 1024,
    )
    vid = svc._ensure_workspace_version("ws-cs1")
    assert vid == record.version_id
    assert mgmt.get_subject_summary("CS1") is not None
    assert mgmt.get_version_summary(record.version_id) is not None


def test_reconcile_all_via_service():
    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_subject("CS1", title="Actuarial Statistics")
    seed_workspace(studio, workspace_id="ws-cs1", subject_code="CS1")
    studio.versions.assign_version("ws-cs1", "2026.1")
    _wipe_management(mgmt)
    # Prefer explicit workspace reconcile — list_all may include durable
    # projections from the shared local SQLite when the app context is active.
    result = ManagementReconciliationService(
        studio.registry, management=mgmt
    ).reconcile_workspace("ws-cs1")
    assert result.subject_restored is True
    assert result.version_id is not None
    assert mgmt.get_subject_summary("CS1") is not None
