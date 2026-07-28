"""Document Import — validate and normalise Canonical Structured Documents."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_extraction.exceptions import DocumentImportError
from app.domain.curriculum_extraction.canonical_document import (
    CanonicalDocument,
    DocumentKind,
)


@dataclass(frozen=True)
class ImportedDocuments:
    """Normalised CMP + Syllabus pair ready for structural parsing."""

    cmp: CanonicalDocument
    syllabus: CanonicalDocument
    diagnostics: tuple[str, ...] = ()


class DocumentImportService:
    """Validate Canonical Documents. Never accepts PDF bytes."""

    STAGE_ID = "document_import"

    def import_documents(
        self,
        *,
        cmp_document: CanonicalDocument,
        syllabus_document: CanonicalDocument,
        subject_code: str,
    ) -> ImportedDocuments:
        """Validate document kinds, non-emptiness, and subject metadata."""
        diagnostics: list[str] = []
        self._require_kind(cmp_document, DocumentKind.CMP, "cmp_document")
        self._require_kind(
            syllabus_document, DocumentKind.SYLLABUS, "syllabus_document"
        )
        self._require_content(cmp_document, "CMP")
        self._require_content(syllabus_document, "Syllabus")

        code = subject_code.strip().upper()
        for doc, label in (
            (cmp_document, "CMP"),
            (syllabus_document, "Syllabus"),
        ):
            meta_code = doc.metadata_value("subject_code")
            if meta_code and meta_code.strip().upper() != code:
                raise DocumentImportError(
                    f"{label} subject_code metadata {meta_code!r} does not "
                    f"match request subject_code {code!r}"
                )
            if not meta_code:
                diagnostics.append(
                    f"{label} missing subject_code metadata; using request code"
                )

        return ImportedDocuments(
            cmp=cmp_document,
            syllabus=syllabus_document,
            diagnostics=tuple(diagnostics),
        )

    def _require_kind(
        self,
        document: CanonicalDocument,
        expected: DocumentKind,
        field_name: str,
    ) -> None:
        if document.document_kind is not expected:
            raise DocumentImportError(
                f"{field_name} must be document_kind={expected.value}, "
                f"got {document.document_kind.value}"
            )

    def _require_content(self, document: CanonicalDocument, label: str) -> None:
        if not document.pages:
            raise DocumentImportError(f"{label} document has no pages")
        if document.block_count < 1:
            raise DocumentImportError(f"{label} document has no content blocks")
