"""View helpers for Curriculum Studio routes."""

from __future__ import annotations

from flask_login import current_user

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.founder.dashboard.dto.founder_workspace import FounderWorkspacePage
from app.founder.dashboard.services.founder_workspace_service import (
    FounderWorkspaceService,
)
from app.presentation.curriculum_studio.factory import (
    get_document_upload_service,
    get_studio_service,
)
from app.presentation.curriculum_studio.view_models import (
    StudioDashboardView,
    dashboard_view,
)


def service() -> CurriculumStudioService:
    return get_studio_service()


def document_upload_service():
    return get_document_upload_service()


def actor_id() -> str:
    return str(getattr(current_user, "id", "founder"))


def load_dashboard() -> StudioDashboardView:
    return dashboard_view(service().founder_dashboard())


def load_workspace(workspace_id: str) -> FounderWorkspacePage:
    """Load DX-004C Publication Workspace projection."""
    return FounderWorkspaceService(studio=service()).build_page(workspace_id)
