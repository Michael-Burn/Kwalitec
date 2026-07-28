"""Typed errors for the Curriculum Extraction pipeline."""

from __future__ import annotations


class CurriculumExtractionError(Exception):
    """Base error for extraction pipeline failures."""

    def __init__(self, message: str, *, stage: str | None = None) -> None:
        super().__init__(message)
        self.stage = stage
        self.message = message


class DocumentImportError(CurriculumExtractionError):
    """Raised when Canonical Document import fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, stage="document_import")


class StructuralParseError(CurriculumExtractionError):
    """Raised when structural parsing cannot proceed."""

    def __init__(self, message: str) -> None:
        super().__init__(message, stage="structural_parsing")


class SegmentationError(CurriculumExtractionError):
    """Raised when curriculum segmentation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, stage="curriculum_segmentation")


class PersistenceError(CurriculumExtractionError):
    """Raised when draft persistence is refused or fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, stage="draft_persist")
