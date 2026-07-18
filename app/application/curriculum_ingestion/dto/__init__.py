"""DTO package for Curriculum Ingestion."""

from __future__ import annotations

from typing import Any

__all__ = [
    "CurriculumPackagePreview",
    "DocumentEntryPayload",
    "DocumentPayload",
    "DocumentSourceRef",
    "ExtractedObjectiveSnapshot",
    "ExtractedSectionSnapshot",
    "ExtractedTopicSnapshot",
    "ExtractionSnapshot",
    "IngestionRequest",
    "IngestionSnapshot",
    "NormalizedObjectiveSnapshot",
    "NormalizedSectionSnapshot",
    "NormalizedTopicSnapshot",
    "NormalizationSnapshot",
    "ValidationIssueSnapshot",
    "ValidationSnapshot",
]

_EXPORT_MODULES = {
    "CurriculumPackagePreview": (
        "app.application.curriculum_ingestion.dto.ingestion_snapshot"
    ),
    "DocumentEntryPayload": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "DocumentPayload": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "DocumentSourceRef": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "ExtractedObjectiveSnapshot": (
        "app.application.curriculum_ingestion.dto.extraction_snapshot"
    ),
    "ExtractedSectionSnapshot": (
        "app.application.curriculum_ingestion.dto.extraction_snapshot"
    ),
    "ExtractedTopicSnapshot": (
        "app.application.curriculum_ingestion.dto.extraction_snapshot"
    ),
    "ExtractionSnapshot": (
        "app.application.curriculum_ingestion.dto.extraction_snapshot"
    ),
    "IngestionRequest": (
        "app.application.curriculum_ingestion.dto.ingestion_request"
    ),
    "IngestionSnapshot": (
        "app.application.curriculum_ingestion.dto.ingestion_snapshot"
    ),
    "NormalizedObjectiveSnapshot": (
        "app.application.curriculum_ingestion.dto.normalization_snapshot"
    ),
    "NormalizedSectionSnapshot": (
        "app.application.curriculum_ingestion.dto.normalization_snapshot"
    ),
    "NormalizedTopicSnapshot": (
        "app.application.curriculum_ingestion.dto.normalization_snapshot"
    ),
    "NormalizationSnapshot": (
        "app.application.curriculum_ingestion.dto.normalization_snapshot"
    ),
    "ValidationIssueSnapshot": (
        "app.application.curriculum_ingestion.dto.validation_snapshot"
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
