"""Application exceptions for Curriculum Studio foundation (PI-001A)."""

from __future__ import annotations


class CurriculumStudioFoundationError(Exception):
    """Base exception for foundation lifecycle failures."""


class SubjectAlreadyExists(CurriculumStudioFoundationError):  # noqa: N818
    """Subject code is already registered."""


class SubjectNotFound(CurriculumStudioFoundationError):  # noqa: N818
    """Subject was not found."""


class VersionAlreadyExists(CurriculumStudioFoundationError):  # noqa: N818
    """Version label already exists for the subject."""


class VersionNotFound(CurriculumStudioFoundationError):  # noqa: N818
    """Curriculum version was not found."""


class IllegalStageTransition(CurriculumStudioFoundationError):  # noqa: N818
    """Requested lifecycle transition is not allowed."""


class ValidationBlocked(CurriculumStudioFoundationError):  # noqa: N818
    """Validation failed and blocks founder review / publish."""


class PublicationError(CurriculumStudioFoundationError):
    """Publish gate rejected the operation."""
