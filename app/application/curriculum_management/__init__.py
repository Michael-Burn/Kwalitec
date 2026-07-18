"""Version 2 Curriculum Management — application layer.

Bounded context for curriculum asset and publication management.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.curriculum_management.subject_service.SubjectService``.
"""

from __future__ import annotations

from typing import Any

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management.approval_service import ApprovalService
from app.application.curriculum_management.asset_service import AssetService
from app.application.curriculum_management.blueprint_assignment_service import (
    BlueprintAssignmentService,
)
from app.application.curriculum_management.preview_service import PreviewService
from app.application.curriculum_management.publication_service import (
    PublicationService,
)
from app.application.curriculum_management.release_service import ReleaseService
from app.application.curriculum_management.subject_service import SubjectService
from app.application.curriculum_management.validation_service import (
    ValidationService,
)
from app.application.curriculum_management.version_service import VersionService

__all__ = [
    "ApprovalError",
    "ApprovalPolicy",
    "ApprovalService",
    "ApprovalSnapshot",
    "AssetError",
    "AssetNotFound",
    "AssetService",
    "BlueprintAssignmentError",
    "BlueprintAssignmentService",
    "CurriculumCatalogue",
    "CurriculumManagementError",
    "CurriculumManagementFacade",
    "PolicyViolation",
    "PreviewError",
    "PreviewService",
    "PreviewSnapshot",
    "PublicationError",
    "PublicationPolicy",
    "PublicationService",
    "PublicationSnapshot",
    "ReleaseError",
    "ReleaseService",
    "ReleaseSnapshot",
    "SubjectAlreadyExists",
    "SubjectNotFound",
    "SubjectService",
    "SubjectSnapshot",
    "SubjectSummary",
    "ValidationFailed",
    "ValidationPolicy",
    "ValidationService",
    "ValidationSnapshot",
    "VersionAlreadyExists",
    "VersionNotFound",
    "VersionPolicy",
    "VersionService",
    "VersionSnapshot",
]


class CurriculumManagementFacade:
    """Convenience wiring of all Curriculum Management services.

    Not required by callers — services may be constructed independently
    against a shared ``CurriculumCatalogue``.
    """

    def __init__(self, catalogue: CurriculumCatalogue | None = None) -> None:
        self.catalogue = catalogue or CurriculumCatalogue()
        self.subjects = SubjectService(self.catalogue)
        self.versions = VersionService(self.catalogue)
        self.assets = AssetService(self.catalogue)
        self.assignments = BlueprintAssignmentService(self.catalogue)
        self.validation = ValidationService(self.catalogue)
        self.approvals = ApprovalService(self.catalogue)
        self.previews = PreviewService(self.catalogue)
        self.publications = PublicationService(self.catalogue)
        self.releases = ReleaseService(self.catalogue)


_EXPORT_MODULES = {
    "ApprovalError": "app.application.curriculum_management.exceptions",
    "ApprovalPolicy": (
        "app.application.curriculum_management.policies.approval_policy"
    ),
    "ApprovalService": "app.application.curriculum_management.approval_service",
    "ApprovalSnapshot": (
        "app.application.curriculum_management.dto.approval_snapshot"
    ),
    "AssetError": "app.application.curriculum_management.exceptions",
    "AssetNotFound": "app.application.curriculum_management.exceptions",
    "AssetService": "app.application.curriculum_management.asset_service",
    "BlueprintAssignmentError": (
        "app.application.curriculum_management.exceptions"
    ),
    "BlueprintAssignmentService": (
        "app.application.curriculum_management.blueprint_assignment_service"
    ),
    "CurriculumCatalogue": "app.application.curriculum_management._catalogue",
    "CurriculumManagementError": (
        "app.application.curriculum_management.exceptions"
    ),
    "CurriculumManagementFacade": (
        "app.application.curriculum_management"
    ),
    "PolicyViolation": "app.application.curriculum_management.exceptions",
    "PreviewError": "app.application.curriculum_management.exceptions",
    "PreviewService": "app.application.curriculum_management.preview_service",
    "PreviewSnapshot": (
        "app.application.curriculum_management.dto.preview_snapshot"
    ),
    "PublicationError": "app.application.curriculum_management.exceptions",
    "PublicationPolicy": (
        "app.application.curriculum_management.policies.publication_policy"
    ),
    "PublicationService": (
        "app.application.curriculum_management.publication_service"
    ),
    "PublicationSnapshot": (
        "app.application.curriculum_management.dto.publication_snapshot"
    ),
    "ReleaseError": "app.application.curriculum_management.exceptions",
    "ReleaseService": "app.application.curriculum_management.release_service",
    "ReleaseSnapshot": (
        "app.application.curriculum_management.dto.release_snapshot"
    ),
    "SubjectAlreadyExists": "app.application.curriculum_management.exceptions",
    "SubjectNotFound": "app.application.curriculum_management.exceptions",
    "SubjectService": "app.application.curriculum_management.subject_service",
    "SubjectSnapshot": (
        "app.application.curriculum_management.dto.subject_snapshot"
    ),
    "SubjectSummary": (
        "app.application.curriculum_management.dto.subject_summary"
    ),
    "ValidationFailed": "app.application.curriculum_management.exceptions",
    "ValidationPolicy": (
        "app.application.curriculum_management.policies.validation_policy"
    ),
    "ValidationService": (
        "app.application.curriculum_management.validation_service"
    ),
    "ValidationSnapshot": (
        "app.application.curriculum_management.dto.validation_snapshot"
    ),
    "VersionAlreadyExists": "app.application.curriculum_management.exceptions",
    "VersionNotFound": "app.application.curriculum_management.exceptions",
    "VersionPolicy": (
        "app.application.curriculum_management.policies.version_policy"
    ),
    "VersionService": "app.application.curriculum_management.version_service",
    "VersionSnapshot": (
        "app.application.curriculum_management.dto.version_snapshot"
    ),
}


def __getattr__(name: str) -> Any:
    if name == "CurriculumManagementFacade":
        return CurriculumManagementFacade
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if module_name == "app.application.curriculum_management":
        return globals()[name]
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
