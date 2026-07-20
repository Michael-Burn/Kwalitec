"""View helpers for Curriculum Studio routes."""

from __future__ import annotations

from flask_login import current_user

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.application.curriculum_studio.exceptions import WorkspaceNotFound
from app.presentation.curriculum_studio.factory import get_studio_service
from app.presentation.curriculum_studio.view_models import (
    EMPTY_CHECKLIST_SUMMARY,
    EMPTY_PREVIEW_SUMMARY,
    EMPTY_VALIDATION_SUMMARY,
    StudioDashboardView,
    WorkspacePageView,
    dashboard_view,
    friendly_checklist_summary,
    friendly_preview_summary,
    friendly_validation_summary,
    workspace_page,
)


def service() -> CurriculumStudioService:
    return get_studio_service()


def actor_id() -> str:
    return str(getattr(current_user, "id", "founder"))


def load_dashboard() -> StudioDashboardView:
    return dashboard_view(service().founder_dashboard())


def load_workspace(workspace_id: str) -> WorkspacePageView:
    svc = service()
    try:
        ws = svc.get_workspace(workspace_id)
    except WorkspaceNotFound as exc:
        raise LookupError(workspace_id) from exc
    validation = EMPTY_VALIDATION_SUMMARY
    preview = EMPTY_PREVIEW_SUMMARY
    checklist = EMPTY_CHECKLIST_SUMMARY
    try:
        snap = svc.validation.summarise(workspace_id)
        validation = friendly_validation_summary(
            readiness=snap.readiness,
            passed=bool(snap.passed),
        )
    except Exception:
        pass
    try:
        snap = svc.preview.preview(workspace_id)
        preview = friendly_preview_summary(
            readiness=snap.readiness,
            node_count=int(snap.node_count),
        )
    except Exception:
        pass
    try:
        check = svc.checklist.checklist(workspace_id)
        ready = sum(1 for item in check.checklist_items if item.satisfied)
        checklist = friendly_checklist_summary(
            ready=ready,
            total=int(check.checklist_item_count),
        )
    except Exception:
        pass
    history: list[str] = []
    try:
        version_snap = svc.versions.history(ws.subject_code)
        for record in version_snap.records:
            history.append(f"{record.version_label} ({record.status})")
    except Exception:
        pass
    return workspace_page(
        ws,
        validation_summary=validation,
        preview_summary=preview,
        checklist_summary=checklist,
        version_history=tuple(history),
    )
