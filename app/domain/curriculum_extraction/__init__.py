"""Curriculum Extraction (EI-002) — educational knowledge acquisition domain.

Consumes Canonical Structured Documents (never PDF bytes) and produces
draft Curriculum Knowledge Graph candidates with provenance and confidence.

Pure domain only: no Flask, SQLAlchemy, PDF I/O, Twin, or UI.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BlockKind",
    "CanonicalBlock",
    "CanonicalDocument",
    "CanonicalPage",
    "ConfidenceBand",
    "DocumentKind",
    "ExtractionConfidence",
    "ExtractionMethod",
    "ExtractionProvenance",
    "IssueSeverity",
    "PublicationState",
    "StructuralLocator",
    "ValidationIssue",
    "ValidationReport",
    "ValidationStatus",
    "confidence_band",
]

_EXPORT_MODULES = {
    "BlockKind": "app.domain.curriculum_extraction.canonical_document",
    "CanonicalBlock": "app.domain.curriculum_extraction.canonical_document",
    "CanonicalDocument": "app.domain.curriculum_extraction.canonical_document",
    "CanonicalPage": "app.domain.curriculum_extraction.canonical_document",
    "DocumentKind": "app.domain.curriculum_extraction.canonical_document",
    "StructuralLocator": "app.domain.curriculum_extraction.canonical_document",
    "ConfidenceBand": "app.domain.curriculum_extraction.confidence",
    "ExtractionConfidence": "app.domain.curriculum_extraction.confidence",
    "confidence_band": "app.domain.curriculum_extraction.confidence",
    "ExtractionMethod": "app.domain.curriculum_extraction.provenance",
    "ExtractionProvenance": "app.domain.curriculum_extraction.provenance",
    "IssueSeverity": "app.domain.curriculum_extraction.validation",
    "ValidationIssue": "app.domain.curriculum_extraction.validation",
    "ValidationReport": "app.domain.curriculum_extraction.validation",
    "PublicationState": "app.domain.curriculum_extraction.publication_state",
    "ValidationStatus": "app.domain.curriculum_extraction.publication_state",
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
