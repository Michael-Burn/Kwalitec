"""Document classifier — deterministic kind resolution for abstract sources."""

from __future__ import annotations

from app.application.curriculum_ingestion.exceptions import ClassificationError
from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntryType,
    DocumentKind,
    resolve_document_kind,
)

_TITLE_HINTS: tuple[tuple[tuple[str, ...], DocumentKind], ...] = (
    (("cmp", "core maths pack", "core mathematics pack"), DocumentKind.CMP),
    (("syllabus", "specification", "spec"), DocumentKind.SYLLABUS),
    (
        ("learning objective", "learning objectives", "objectives"),
        DocumentKind.LEARNING_OBJECTIVES,
    ),
    (("formula", "formulae", "formula sheet"), DocumentKind.FORMULA_SHEET),
    (("supporting", "appendix", "notes"), DocumentKind.SUPPORTING_DOCUMENT),
)


class DocumentClassifier:
    """Classify abstract curriculum documents without AI reasoning.

    Priority:
    1. Explicit ``declared_kind`` (when not UNKNOWN)
    2. Title / metadata keyword hints
    3. Dominant entry-type fingerprint
    4. UNKNOWN
    """

    def classify(self, document: CurriculumDocument) -> DocumentKind:
        """Return the resolved DocumentKind for ``document``."""
        if document.declared_kind is not None and (
            document.declared_kind is not DocumentKind.UNKNOWN
        ):
            return document.declared_kind

        hinted = self._from_title(document.title)
        if hinted is not None:
            return hinted

        meta_kind = document.metadata_value("document_kind") or document.metadata_value(
            "kind"
        )
        if meta_kind:
            try:
                resolved = resolve_document_kind(meta_kind)
                if resolved is not DocumentKind.UNKNOWN:
                    return resolved
            except ValueError:
                pass

        fingerprint = self._from_entries(document)
        if fingerprint is not None:
            return fingerprint
        return DocumentKind.UNKNOWN

    def classify_many(
        self, documents: list[CurriculumDocument] | tuple[CurriculumDocument, ...]
    ) -> tuple[tuple[str, DocumentKind], ...]:
        """Classify each document; raise if the set is empty."""
        docs = tuple(documents)
        if not docs:
            raise ClassificationError("No documents to classify")
        return tuple((doc.document_id, self.classify(doc)) for doc in docs)

    def _from_title(self, title: str) -> DocumentKind | None:
        lowered = (title or "").strip().lower()
        for keywords, kind in _TITLE_HINTS:
            if any(token in lowered for token in keywords):
                return kind
        return None

    def _from_entries(self, document: CurriculumDocument) -> DocumentKind | None:
        if document.entry_count == 0:
            return None
        counts: dict[DocumentEntryType, int] = {}
        for entry in document.entries:
            counts[entry.entry_type] = counts.get(entry.entry_type, 0) + 1

        formulas = counts.get(DocumentEntryType.FORMULA, 0)
        objectives = counts.get(DocumentEntryType.OBJECTIVE, 0)
        topics = counts.get(DocumentEntryType.TOPIC, 0)
        sections = counts.get(DocumentEntryType.SECTION, 0)
        notes = counts.get(DocumentEntryType.NOTE, 0)

        if formulas > 0 and formulas >= topics and formulas >= objectives:
            return DocumentKind.FORMULA_SHEET
        if objectives > 0 and topics == 0 and sections == 0:
            return DocumentKind.LEARNING_OBJECTIVES
        if topics > 0 or sections > 0:
            # Prefer syllabus when structural; CMP if metadata says pack-like
            if "cmp" in document.title.lower() or document.metadata_value(
                "pack"
            ):
                return DocumentKind.CMP
            return DocumentKind.SYLLABUS
        if notes > 0:
            return DocumentKind.SUPPORTING_DOCUMENT
        return None
