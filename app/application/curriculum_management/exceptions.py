"""Application-layer exceptions for Curriculum Management.

Framework-independent. Raised when subject, version, validation,
approval, or publication rules are violated.
"""

from __future__ import annotations


class CurriculumManagementError(Exception):
    """Base exception for Curriculum Management failures."""


class SubjectNotFound(CurriculumManagementError):  # noqa: N818
    """No subject exists for the requested identity."""


class SubjectAlreadyExists(CurriculumManagementError):  # noqa: N818
    """A subject with the same identity or code already exists."""


class VersionNotFound(CurriculumManagementError):  # noqa: N818
    """No subject version exists for the requested identity."""


class VersionAlreadyExists(CurriculumManagementError):  # noqa: N818
    """A version with the same identity or label already exists."""


class AssetNotFound(CurriculumManagementError):  # noqa: N818
    """No curriculum asset exists for the requested identity."""


class AssetError(CurriculumManagementError):  # noqa: N818
    """Curriculum asset operation failed."""


class ValidationFailed(CurriculumManagementError):  # noqa: N818
    """Validation did not pass or cannot advance publication."""


class ApprovalError(CurriculumManagementError):  # noqa: N818
    """Approval operation failed."""


class PublicationError(CurriculumManagementError):  # noqa: N818
    """Publication lifecycle transition failed."""


class PreviewError(CurriculumManagementError):  # noqa: N818
    """Preview could not be produced."""


class ReleaseError(CurriculumManagementError):  # noqa: N818
    """Release notes or release operation failed."""


class BlueprintAssignmentError(CurriculumManagementError):  # noqa: N818
    """Blueprint assignment operation failed."""


class PolicyViolation(CurriculumManagementError):  # noqa: N818
    """A curriculum management policy rejected the operation."""
