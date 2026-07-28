"""Explicit Learning Graph projection errors (AP-002D4).

Never silently repair malformed projections or invent missing relationships.
"""

from __future__ import annotations


class ProjectionError(Exception):
    """Base domain error for Learning Graph projection failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class UnknownProjectionRelationshipType(ProjectionError):  # noqa: N818
    """Relationship type is not in the AP-002D4 catalogue."""


class UnsupportedProjectionVersion(ProjectionError):  # noqa: N818
    """Projection version is not supported."""


class DuplicateProjection(ProjectionError):  # noqa: N818
    """Projection identifier collides within a batch or was already applied."""


class BrokenProjectionProvenance(ProjectionError):  # noqa: N818
    """Required provenance identifiers are missing or blank."""


class IncompleteProjectionProvenance(ProjectionError):  # noqa: N818
    """Provenance chain required for Graph explainability is incomplete."""


class BrokenConceptReference(ProjectionError):  # noqa: N818
    """Concept reference required for a relationship is blank or broken."""


class MissingLearningObjective(ProjectionError):  # noqa: N818
    """Learning objective reference is missing or invalid."""


class InvalidDecisionVersion(ProjectionError):  # noqa: N818
    """Referenced Twin decision version is invalid or unsupported."""


class InvalidProjectionSchema(ProjectionError):  # noqa: N818
    """Projection payload / schema fails structural validation."""


class ProjectionRejected(ProjectionError):  # noqa: N818
    """Projection batch refused before apply (validation failed)."""
