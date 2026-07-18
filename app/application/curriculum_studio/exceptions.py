"""Application-layer exceptions for Curriculum Studio.

Framework-independent. Raised when workflow, publication, preview,
validation, version, or diff rules are violated.
"""

from __future__ import annotations


class CurriculumStudioError(Exception):
    """Base exception for Curriculum Studio failures."""


class WorkspaceNotFound(CurriculumStudioError):  # noqa: N818
    """No workspace exists for the requested identity."""


class WorkspaceAlreadyExists(CurriculumStudioError):  # noqa: N818
    """A workspace with the same identity already exists."""


class WorkflowError(CurriculumStudioError):  # noqa: N818
    """Workflow stage transition failed."""


class WorkflowGateBlocked(CurriculumStudioError):  # noqa: N818
    """Advancing the workflow is blocked by unmet readiness gates."""


class ValidationError(CurriculumStudioError):  # noqa: N818
    """Validation summary could not be produced or failed readiness."""


class PreviewError(CurriculumStudioError):  # noqa: N818
    """Preview summary could not be produced or approved."""


class PublicationError(CurriculumStudioError):  # noqa: N818
    """Publication readiness or lifecycle operation failed."""


class VersionError(CurriculumStudioError):  # noqa: N818
    """Version lifecycle operation failed."""


class VersionNotFound(CurriculumStudioError):  # noqa: N818
    """No version record exists for the requested identity."""


class DiffError(CurriculumStudioError):  # noqa: N818
    """Curriculum diff could not be produced."""


class PortUnavailable(CurriculumStudioError):  # noqa: N818
    """An injected Studio port is unavailable."""


class SubjectNotFound(CurriculumStudioError):  # noqa: N818
    """No subject exists for the requested identity."""


class SubjectAlreadyExists(CurriculumStudioError):  # noqa: N818
    """A subject with the same identity already exists."""


class DashboardError(CurriculumStudioError):  # noqa: N818
    """Dashboard projection could not be produced."""


class PolicyViolation(CurriculumStudioError):  # noqa: N818
    """A Curriculum Studio policy rejected the operation."""
