"""Application-layer exceptions for Curriculum Ingestion.

Framework-independent. Raised when classification, extraction,
normalisation, validation, or mapping rules are violated.
"""

from __future__ import annotations


class CurriculumIngestionError(Exception):
    """Base exception for Curriculum Ingestion failures."""


class DocumentNotFound(CurriculumIngestionError):  # noqa: N818
    """No document exists for the requested identity."""


class JobNotFound(CurriculumIngestionError):  # noqa: N818
    """No ingestion job exists for the requested identity."""


class ClassificationError(CurriculumIngestionError):  # noqa: N818
    """Document classification failed."""


class ExtractionError(CurriculumIngestionError):  # noqa: N818
    """Extraction could not produce structures."""


class NormalizationError(CurriculumIngestionError):  # noqa: N818
    """Normalisation could not produce canonical structures."""


class ValidationFailed(CurriculumIngestionError):  # noqa: N818
    """Validation did not pass or blocks completion."""


class MappingError(CurriculumIngestionError):  # noqa: N818
    """Mapping to a curriculum package preview failed."""


class PreviewError(CurriculumIngestionError):  # noqa: N818
    """Preview could not be produced."""


class PolicyViolation(CurriculumIngestionError):  # noqa: N818
    """An ingestion policy rejected the operation."""


class IllegalState(CurriculumIngestionError):  # noqa: N818
    """Operation is not lawful in the current ingestion state."""
