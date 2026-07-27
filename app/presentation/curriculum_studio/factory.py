"""Factory for Curriculum Studio application service used by the Founder UI."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, current_app, g, has_app_context

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.application.curriculum_studio.document_upload_service import (
    DocumentUploadService,
)
from app.application.curriculum_studio.ports.document_metadata_port import (
    bind_document_metadata_port,
)
from app.infrastructure.adapters.curriculum_ingestion import (
    CurriculumIngestionAdapter,
)
from app.infrastructure.adapters.curriculum_intelligence import (
    CurriculumIntelligenceProcessingAdapter,
)
from app.infrastructure.adapters.curriculum_management import (
    CurriculumManagementAdapter,
)
from app.infrastructure.adapters.document_storage import (
    LocalDocumentStorageAdapter,
)
from app.infrastructure.adapters.document_storage.metadata import (
    SqlAlchemyDocumentMetadataAdapter,
)

_CONFIG_KEY = "CURRICULUM_STUDIO_SERVICE"
_UPLOAD_CONFIG_KEY = "CURRICULUM_DOCUMENT_UPLOAD_SERVICE"
_G_KEY = "curriculum_studio_service"
_G_UPLOAD_KEY = "curriculum_document_upload_service"


def build_studio_service() -> CurriculumStudioService:
    """Construct CurriculumStudioService with production Management/Ingestion ports."""
    return CurriculumStudioService.create(
        curriculum_management=CurriculumManagementAdapter(),
        curriculum_ingestion=CurriculumIngestionAdapter(),
    )


def build_document_upload_service(
    flask_app: Flask | None = None,
    *,
    studio: CurriculumStudioService | None = None,
) -> DocumentUploadService:
    """Construct DocumentUploadService with local storage + CIP processing."""
    app = flask_app
    if app is None:
        app = current_app._get_current_object()  # type: ignore[attr-defined]
    root = Path(
        app.config.get(
            "DOCUMENT_STORAGE_ROOT",
            Path(app.instance_path) / "curriculum_documents",
        )
    )
    max_bytes = int(app.config.get("DOCUMENT_MAX_BYTES", 25 * 1024 * 1024))
    auto_run = bool(app.config.get("CIP_AUTO_RUN", True))
    storage = LocalDocumentStorageAdapter(root)
    metadata = SqlAlchemyDocumentMetadataAdapter()
    bind_document_metadata_port(metadata)
    return DocumentUploadService(
        studio=studio or get_studio_service(),
        storage=storage,
        processing=CurriculumIntelligenceProcessingAdapter(
            storage,
            auto_run=auto_run,
        ),
        metadata=metadata,
        max_bytes=max_bytes,
    )


def init_curriculum_studio(flask_app: Flask) -> CurriculumStudioService:
    """Register the studio service on the Flask app."""
    service = build_studio_service()
    flask_app.config[_CONFIG_KEY] = service
    flask_app.config[_UPLOAD_CONFIG_KEY] = build_document_upload_service(
        flask_app, studio=service
    )
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
        g.pop(_G_UPLOAD_KEY, None)
    target.config[_CONFIG_KEY] = service
    target.config[_UPLOAD_CONFIG_KEY] = build_document_upload_service(
        target, studio=service
    )


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


def get_document_upload_service() -> DocumentUploadService:
    """Return the request/app DocumentUploadService instance."""
    if has_app_context() and _G_UPLOAD_KEY in g:
        return g.get(_G_UPLOAD_KEY)  # type: ignore[return-value]
    flask_app = current_app
    service = flask_app.config.get(_UPLOAD_CONFIG_KEY)
    if service is None:
        init_curriculum_studio(flask_app)
        service = flask_app.config.get(_UPLOAD_CONFIG_KEY)
    if service is None:
        service = build_document_upload_service(flask_app)
        flask_app.config[_UPLOAD_CONFIG_KEY] = service
    if has_app_context():
        setattr(g, _G_UPLOAD_KEY, service)
    return service
