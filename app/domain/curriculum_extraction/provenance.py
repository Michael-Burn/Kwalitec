"""Source provenance for extracted Curriculum Knowledge Graph nodes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_extraction.canonical_document import (
    DocumentKind,
    StructuralLocator,
)
from app.domain.curriculum_extraction.confidence import ExtractionConfidence


class ExtractionMethod(StrEnum):
    """How an educational object was obtained from a Canonical Document."""

    HEURISTIC = "heuristic"
    STRUCTURED_FIELD = "structured_field"
    ADAPTER_IMPORT = "adapter_import"


@dataclass(frozen=True)
class ExtractionProvenance:
    """Permanent recoverability of an extracted node's origin.

    Attached as a sidecar to CKG nodes — does not alter educational entity
    shapes from EI-001.
    """

    stable_id: str
    locator: StructuralLocator
    document_kind: DocumentKind
    confidence: ExtractionConfidence
    extraction_method: ExtractionMethod
    notes: str = ""

    @classmethod
    def create(
        cls,
        stable_id: str,
        locator: StructuralLocator,
        *,
        document_kind: DocumentKind | str,
        confidence: int | ExtractionConfidence,
        extraction_method: ExtractionMethod | str = ExtractionMethod.HEURISTIC,
        notes: str = "",
    ) -> ExtractionProvenance:
        """Construct provenance after validating identifiers."""
        sid = (stable_id or "").strip()
        if not sid:
            raise ValueError("stable_id must be non-empty")
        kind = (
            document_kind
            if isinstance(document_kind, DocumentKind)
            else DocumentKind(document_kind)
        )
        conf = (
            confidence
            if isinstance(confidence, ExtractionConfidence)
            else ExtractionConfidence.of(confidence)
        )
        method = (
            extraction_method
            if isinstance(extraction_method, ExtractionMethod)
            else ExtractionMethod(extraction_method)
        )
        return cls(
            stable_id=sid,
            locator=locator,
            document_kind=kind,
            confidence=conf,
            extraction_method=method,
            notes=(notes or "").strip(),
        )
