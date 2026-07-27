"""Curriculum document domain — types, processing stages, registries.

Opaque storage references belong to application/infrastructure layers.
This package defines Founder-facing document kinds and processing contracts.
"""

from app.domain.curriculum_documents.document_type_registry import (
    DocumentTypeDefinition,
    DocumentTypeRegistry,
    default_document_type_registry,
)
from app.domain.curriculum_documents.processing_stage import (
    FOUNDER_STAGE_LABELS,
    DocumentProcessingStage,
)

__all__ = [
    "DocumentProcessingStage",
    "DocumentTypeDefinition",
    "DocumentTypeRegistry",
    "FOUNDER_STAGE_LABELS",
    "default_document_type_registry",
]
