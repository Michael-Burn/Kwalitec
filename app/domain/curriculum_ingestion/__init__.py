"""Version 2 Curriculum Ingestion domain package.

Bounded context for deterministic curriculum document ingestion:
classification, extraction, normalisation, and validation only.

No teaching. No activity / session / mission generation.
No Flask / SQLAlchemy / persistence.

Prefer explicit imports such as
``app.domain.curriculum_ingestion.ingestion_job.IngestionJob``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CurriculumDocument",
    "DocumentEntry",
    "DocumentEntryType",
    "DocumentKind",
    "ExtractedObjective",
    "ExtractedSection",
    "ExtractedTopic",
    "ExtractionResult",
    "IngestionIssue",
    "IngestionIssueCode",
    "IngestionIssueSeverity",
    "IngestionJob",
    "IngestionReport",
    "IngestionState",
    "IngestionTransitionEvent",
    "NormalizationResult",
    "NormalizedObjective",
    "NormalizedSection",
    "NormalizedTopic",
    "has_reached",
    "is_failure_state",
    "is_terminal_ingestion_state",
    "next_ingestion_state",
    "pipeline_index",
    "resolve_document_kind",
    "resolve_entry_type",
    "resolve_ingestion_state",
]

_EXPORT_MODULES = {
    "CurriculumDocument": "app.domain.curriculum_ingestion.curriculum_document",
    "DocumentEntry": "app.domain.curriculum_ingestion.curriculum_document",
    "DocumentEntryType": "app.domain.curriculum_ingestion.curriculum_document",
    "DocumentKind": "app.domain.curriculum_ingestion.curriculum_document",
    "ExtractedObjective": "app.domain.curriculum_ingestion.extracted_objective",
    "ExtractedSection": "app.domain.curriculum_ingestion.extracted_section",
    "ExtractedTopic": "app.domain.curriculum_ingestion.extracted_topic",
    "ExtractionResult": "app.domain.curriculum_ingestion.extraction_result",
    "IngestionIssue": "app.domain.curriculum_ingestion.ingestion_report",
    "IngestionIssueCode": "app.domain.curriculum_ingestion.ingestion_report",
    "IngestionIssueSeverity": "app.domain.curriculum_ingestion.ingestion_report",
    "IngestionJob": "app.domain.curriculum_ingestion.ingestion_job",
    "IngestionReport": "app.domain.curriculum_ingestion.ingestion_report",
    "IngestionState": "app.domain.curriculum_ingestion.ingestion_state",
    "IngestionTransitionEvent": "app.domain.curriculum_ingestion.ingestion_state",
    "NormalizationResult": "app.domain.curriculum_ingestion.normalization_result",
    "NormalizedObjective": "app.domain.curriculum_ingestion.normalization_result",
    "NormalizedSection": "app.domain.curriculum_ingestion.normalization_result",
    "NormalizedTopic": "app.domain.curriculum_ingestion.normalization_result",
    "has_reached": "app.domain.curriculum_ingestion.ingestion_state",
    "is_failure_state": "app.domain.curriculum_ingestion.ingestion_state",
    "is_terminal_ingestion_state": (
        "app.domain.curriculum_ingestion.ingestion_state"
    ),
    "next_ingestion_state": "app.domain.curriculum_ingestion.ingestion_state",
    "pipeline_index": "app.domain.curriculum_ingestion.ingestion_state",
    "resolve_document_kind": "app.domain.curriculum_ingestion.curriculum_document",
    "resolve_entry_type": "app.domain.curriculum_ingestion.curriculum_document",
    "resolve_ingestion_state": "app.domain.curriculum_ingestion.ingestion_state",
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
