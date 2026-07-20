"""Factory for Curriculum Studio application service used by the Founder UI."""

from __future__ import annotations

from flask import Flask, current_app, g, has_app_context

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.infrastructure.adapters.curriculum_ingestion import (
    CurriculumIngestionAdapter,
)
from app.infrastructure.adapters.curriculum_management import (
    CurriculumManagementAdapter,
)

_CONFIG_KEY = "CURRICULUM_STUDIO_SERVICE"
_G_KEY = "curriculum_studio_service"


def build_studio_service() -> CurriculumStudioService:
    """Construct CurriculumStudioService with production Management/Ingestion ports."""
    return CurriculumStudioService.create(
        curriculum_management=CurriculumManagementAdapter(),
        curriculum_ingestion=CurriculumIngestionAdapter(),
    )


def init_curriculum_studio(flask_app: Flask) -> CurriculumStudioService:
    """Register the studio service on the Flask app."""
    service = build_studio_service()
    flask_app.config[_CONFIG_KEY] = service
    return service


def set_studio_service(
    service: CurriculumStudioService, *, app: Flask | None = None
) -> None:
    """Replace the studio service (tests)."""
    target = app
    if target is None:
        if not has_app_context():
            raise RuntimeError("set_studio_service requires an app or app context")
        target = current_app._get_current_object()  # type: ignore[attr-defined]
        g.pop(_G_KEY, None)
    target.config[_CONFIG_KEY] = service


def get_studio_service() -> CurriculumStudioService:
    """Return the request/app CurriculumStudioService instance."""
    if has_app_context() and _G_KEY in g:
        return g.get(_G_KEY)  # type: ignore[return-value]
    flask_app = current_app
    service = flask_app.config.get(_CONFIG_KEY)
    if service is None:
        service = init_curriculum_studio(flask_app)
    if has_app_context():
        setattr(g, _G_KEY, service)
    return service
