"""Stateless extraction policy for curriculum documents."""

from __future__ import annotations

from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntryType,
    DocumentKind,
)


class ExtractionPolicy:
    """Deterministic rules for what may be extracted from a document kind."""

    STRUCTURAL_KINDS = frozenset(
        {
            DocumentKind.SYLLABUS,
            DocumentKind.CMP,
            DocumentKind.LEARNING_OBJECTIVES,
        }
    )

    @staticmethod
    def allows_sections(kind: DocumentKind) -> bool:
        """True when sections may be extracted from ``kind``."""
        return kind in {
            DocumentKind.SYLLABUS,
            DocumentKind.CMP,
            DocumentKind.SUPPORTING_DOCUMENT,
        }

    @staticmethod
    def allows_topics(kind: DocumentKind) -> bool:
        """True when topics may be extracted from ``kind``."""
        return kind in {
            DocumentKind.SYLLABUS,
            DocumentKind.CMP,
            DocumentKind.SUPPORTING_DOCUMENT,
        }

    @staticmethod
    def allows_objectives(kind: DocumentKind) -> bool:
        """True when objectives may be extracted from ``kind``."""
        return kind in {
            DocumentKind.LEARNING_OBJECTIVES,
            DocumentKind.SYLLABUS,
            DocumentKind.CMP,
        }

    @staticmethod
    def allows_formulas(kind: DocumentKind) -> bool:
        """True when formula entries are meaningful for ``kind``."""
        return kind is DocumentKind.FORMULA_SHEET

    @staticmethod
    def requires_structural_entries(kind: DocumentKind) -> bool:
        """True when empty structural documents are invalid for ``kind``."""
        return kind in ExtractionPolicy.STRUCTURAL_KINDS

    @staticmethod
    def extractable_entry_types(kind: DocumentKind) -> frozenset[DocumentEntryType]:
        """Entry types the extractor will consider for ``kind``."""
        types: set[DocumentEntryType] = {DocumentEntryType.METADATA}
        if ExtractionPolicy.allows_sections(kind):
            types.add(DocumentEntryType.SECTION)
        if ExtractionPolicy.allows_topics(kind):
            types.add(DocumentEntryType.TOPIC)
            types.add(DocumentEntryType.PREREQUISITE)
        if ExtractionPolicy.allows_objectives(kind):
            types.add(DocumentEntryType.OBJECTIVE)
        if ExtractionPolicy.allows_formulas(kind):
            types.add(DocumentEntryType.FORMULA)
            types.add(DocumentEntryType.NOTE)
        if kind is DocumentKind.SUPPORTING_DOCUMENT:
            types.add(DocumentEntryType.NOTE)
        if kind is DocumentKind.UNKNOWN:
            types.update(DocumentEntryType)
        return frozenset(types)

    @staticmethod
    def assert_document_extractable(document: CurriculumDocument) -> None:
        """Raise ValueError when a document cannot be extracted."""
        if document.entry_count == 0:
            raise ValueError(
                f"document {document.document_id!r} has no extractable entries"
            )
