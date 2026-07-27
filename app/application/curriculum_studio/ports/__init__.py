"""Curriculum Studio ports package."""

from __future__ import annotations

from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.ports.document_processing_port import (
    DocumentProcessingPort,
)
from app.application.curriculum_studio.ports.document_storage_port import (
    DocumentStoragePort,
)
from app.application.curriculum_studio.ports.education_platform_port import (
    EducationPlatformPort,
)

PORT_NAMES: tuple[str, ...] = (
    "curriculum_management",
    "curriculum_ingestion",
    "education_platform",
    "document_storage",
    "document_processing",
)

__all__ = [
    "PORT_NAMES",
    "CurriculumIngestionPort",
    "CurriculumManagementPort",
    "DocumentProcessingPort",
    "DocumentStoragePort",
    "EducationPlatformPort",
]
