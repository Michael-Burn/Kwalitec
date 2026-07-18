"""Version 2 Curriculum Ingestion — application layer.

Deterministic pipeline: classify → extract → normalise → validate → preview.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.curriculum_ingestion.ingestion_engine.CurriculumIngestionEngine``.
"""

from __future__ import annotations

from typing import Any

from app.application.curriculum_ingestion.document_classifier import (
    DocumentClassifier,
)
from app.application.curriculum_ingestion.extraction_service import (
    ExtractionService,
)
from app.application.curriculum_ingestion.ingestion_engine import (
    CurriculumIngestionEngine,
)
from app.application.curriculum_ingestion.mapping_service import MappingService
from app.application.curriculum_ingestion.normalization_service import (
    NormalizationService,
)
from app.application.curriculum_ingestion.preview_service import PreviewService
from app.application.curriculum_ingestion.validation_service import (
    ValidationService,
)

__all__ = [
    "ClassificationError",
    "CurriculumIngestionEngine",
    "CurriculumIngestionError",
    "CurriculumPackagePreview",
    "DocumentClassifier",
    "DocumentEntryPayload",
    "DocumentNotFound",
    "DocumentPayload",
    "DocumentSourceRef",
    "ExtractionError",
    "ExtractionPolicy",
    "ExtractionService",
    "ExtractionSnapshot",
    "IllegalState",
    "IngestionRequest",
    "IngestionSnapshot",
    "JobNotFound",
    "MappingError",
    "MappingService",
    "NormalizationError",
    "NormalizationPolicy",
    "NormalizationService",
    "NormalizationSnapshot",
    "PolicyViolation",
    "PreviewError",
    "PreviewService",
    "ValidationFailed",
    "ValidationPolicy",
    "ValidationService",
    "ValidationSnapshot",
]

_EXPORT_MODULES = {
    "ClassificationError": "app.application.curriculum_ingestion.exceptions",
    "CurriculumIngestionEngine": (
        "app.application.curriculum_ingestion.ingestion_engine"
    ),
    "CurriculumIngestionError": (
        "app.application.curriculum_ingestion.exceptions"
    ),
    "CurriculumPackagePreview": (
        "app.application.curriculum_ingestion.dto.ingestion_snapshot"
    ),
    "DocumentClassifier": (
        "app.application.curriculum_ingestion.document_classifier"
    ),
    "DocumentEntryPayload": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "DocumentNotFound": "app.application.curriculum_ingestion.exceptions",
    "DocumentPayload": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "DocumentSourceRef": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "ExtractionError": "app.application.curriculum_ingestion.exceptions",
    "ExtractionPolicy": (
        "app.application.curriculum_ingestion.policies.extraction_policy"
    ),
    "ExtractionService": (
        "app.application.curriculum_ingestion.extraction_service"
    ),
    "ExtractionSnapshot": (
        "app.application.curriculum_ingestion.dto.extraction_snapshot"
    ),
    "IllegalState": "app.application.curriculum_ingestion.exceptions",
    "IngestionRequest": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "IngestionSnapshot": (
        "app.application.curriculum_ingestion.dto.ingestion_snapshot"
    ),
    "JobNotFound": "app.application.curriculum_ingestion.exceptions",
    "MappingError": "app.application.curriculum_ingestion.exceptions",
    "MappingService": "app.application.curriculum_ingestion.mapping_service",
    "NormalizationError": "app.application.curriculum_ingestion.exceptions",
    "NormalizationPolicy": (
        "app.application.curriculum_ingestion.policies.normalization_policy"
    ),
    "NormalizationService": (
        "app.application.curriculum_ingestion.normalization_service"
    ),
    "NormalizationSnapshot": (
        "app.application.curriculum_ingestion.dto.normalization_snapshot"
    ),
    "PolicyViolation": "app.application.curriculum_ingestion.exceptions",
    "PreviewError": "app.application.curriculum_ingestion.exceptions",
    "PreviewService": "app.application.curriculum_ingestion.preview_service",
    "ValidationFailed": "app.application.curriculum_ingestion.exceptions",
    "ValidationPolicy": (
        "app.application.curriculum_ingestion.policies.validation_policy"
    ),
    "ValidationService": (
        "app.application.curriculum_ingestion.validation_service"
    ),
    "ValidationSnapshot": (
        "app.application.curriculum_ingestion.dto.validation_snapshot"
    ),
}


def __getattr__(name: str) -> Any:
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
