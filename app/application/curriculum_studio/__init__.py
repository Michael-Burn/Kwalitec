"""Version 2 Curriculum Studio — application layer.

Founder-facing operational foundation for curriculum readiness:
subjects, workspaces, workflow, validation, preview, publication checklist,
versioning, dashboard, and structural diffs.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.
Does not import or modify Curriculum Management, Curriculum Ingestion,
Education Platform, Student Twin, Adaptive Decision Engine, or Orchestrator.

Prefer explicit imports such as
``app.application.curriculum_studio.curriculum_studio_service.CurriculumStudioService``.
"""

from __future__ import annotations

from typing import Any

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)

__all__ = [
    "ActivityEntrySnapshot",
    "ChecklistItemSnapshot",
    "CurriculumIngestionPort",
    "CurriculumManagementPort",
    "CurriculumStudioError",
    "CurriculumStudioService",
    "DashboardError",
    "DashboardService",
    "DashboardSnapshot",
    "DiagnosticReport",
    "Diagnostics",
    "DiffEntrySnapshot",
    "DiffError",
    "DiffService",
    "DiffSnapshot",
    "EducationPlatformPort",
    "PORT_NAMES",
    "PolicyViolation",
    "PortUnavailable",
    "PreviewError",
    "PreviewNodeSnapshot",
    "PreviewService",
    "PreviewSnapshot",
    "PublicationChecklistService",
    "PublicationError",
    "PublicationService",
    "PublicationSnapshot",
    "STUDIO_VERSION",
    "StudioRegistry",
    "SubjectAlreadyExists",
    "SubjectNotFound",
    "SubjectService",
    "SubjectSnapshot",
    "ValidationError",
    "ValidationFindingSnapshot",
    "ValidationService",
    "ValidationSnapshot",
    "VersionError",
    "VersionHistoryService",
    "VersionNotFound",
    "VersionRecordSnapshot",
    "VersionService",
    "VersionSnapshot",
    "WorkflowError",
    "WorkflowGateBlocked",
    "WorkflowService",
    "WorkflowSnapshot",
    "WorkflowTransitionSnapshot",
    "WorkspaceAlreadyExists",
    "WorkspaceNotFound",
    "WorkspaceService",
    "WorkspaceSnapshot",
]

_EXPORT_MODULES = {
    "ActivityEntrySnapshot": (
        "app.application.curriculum_studio.dto.dashboard_snapshot"
    ),
    "ChecklistItemSnapshot": (
        "app.application.curriculum_studio.dto.publication_snapshot"
    ),
    "CurriculumIngestionPort": (
        "app.application.curriculum_studio.ports.curriculum_ingestion_port"
    ),
    "CurriculumManagementPort": (
        "app.application.curriculum_studio.ports.curriculum_management_port"
    ),
    "CurriculumStudioError": "app.application.curriculum_studio.exceptions",
    "CurriculumStudioService": (
        "app.application.curriculum_studio.curriculum_studio_service"
    ),
    "DashboardError": "app.application.curriculum_studio.exceptions",
    "DashboardService": "app.application.curriculum_studio.dashboard_service",
    "DashboardSnapshot": (
        "app.application.curriculum_studio.dto.dashboard_snapshot"
    ),
    "DiagnosticReport": "app.application.curriculum_studio.diagnostics",
    "Diagnostics": "app.application.curriculum_studio.diagnostics",
    "DiffEntrySnapshot": "app.application.curriculum_studio.diff_service",
    "DiffError": "app.application.curriculum_studio.exceptions",
    "DiffService": "app.application.curriculum_studio.diff_service",
    "DiffSnapshot": "app.application.curriculum_studio.diff_service",
    "EducationPlatformPort": (
        "app.application.curriculum_studio.ports.education_platform_port"
    ),
    "PORT_NAMES": "app.application.curriculum_studio.ports",
    "PolicyViolation": "app.application.curriculum_studio.exceptions",
    "PortUnavailable": "app.application.curriculum_studio.exceptions",
    "PreviewError": "app.application.curriculum_studio.exceptions",
    "PreviewNodeSnapshot": (
        "app.application.curriculum_studio.dto.preview_snapshot"
    ),
    "PreviewService": "app.application.curriculum_studio.preview_service",
    "PreviewSnapshot": (
        "app.application.curriculum_studio.dto.preview_snapshot"
    ),
    "PublicationChecklistService": (
        "app.application.curriculum_studio.publication_checklist_service"
    ),
    "PublicationError": "app.application.curriculum_studio.exceptions",
    "PublicationService": (
        "app.application.curriculum_studio.publication_service"
    ),
    "PublicationSnapshot": (
        "app.application.curriculum_studio.dto.publication_snapshot"
    ),
    "STUDIO_VERSION": "app.application.curriculum_studio.diagnostics",
    "StudioRegistry": "app.application.curriculum_studio._registry",
    "SubjectAlreadyExists": "app.application.curriculum_studio.exceptions",
    "SubjectNotFound": "app.application.curriculum_studio.exceptions",
    "SubjectService": "app.application.curriculum_studio.subject_service",
    "SubjectSnapshot": (
        "app.application.curriculum_studio.dto.subject_snapshot"
    ),
    "ValidationError": "app.application.curriculum_studio.exceptions",
    "ValidationFindingSnapshot": (
        "app.application.curriculum_studio.dto.validation_snapshot"
    ),
    "ValidationService": (
        "app.application.curriculum_studio.validation_service"
    ),
    "ValidationSnapshot": (
        "app.application.curriculum_studio.dto.validation_snapshot"
    ),
    "VersionError": "app.application.curriculum_studio.exceptions",
    "VersionHistoryService": (
        "app.application.curriculum_studio.version_history_service"
    ),
    "VersionNotFound": "app.application.curriculum_studio.exceptions",
    "VersionRecordSnapshot": (
        "app.application.curriculum_studio.dto.version_snapshot"
    ),
    "VersionService": (
        "app.application.curriculum_studio.version_history_service"
    ),
    "VersionSnapshot": (
        "app.application.curriculum_studio.dto.version_snapshot"
    ),
    "WorkflowError": "app.application.curriculum_studio.exceptions",
    "WorkflowGateBlocked": "app.application.curriculum_studio.exceptions",
    "WorkflowService": "app.application.curriculum_studio.workflow_service",
    "WorkflowSnapshot": (
        "app.application.curriculum_studio.dto.workflow_snapshot"
    ),
    "WorkflowTransitionSnapshot": (
        "app.application.curriculum_studio.dto.workflow_snapshot"
    ),
    "WorkspaceAlreadyExists": "app.application.curriculum_studio.exceptions",
    "WorkspaceNotFound": "app.application.curriculum_studio.exceptions",
    "WorkspaceService": "app.application.curriculum_studio.workspace_service",
    "WorkspaceSnapshot": (
        "app.application.curriculum_studio.dto.workspace_snapshot"
    ),
}


def __getattr__(name: str) -> Any:
    if name == "CurriculumStudioService":
        return CurriculumStudioService
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
