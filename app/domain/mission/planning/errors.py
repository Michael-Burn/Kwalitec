"""Explicit Mission planning errors (AP-002D5).

Never silently repair malformed plans or invent missing learner state.
"""

from __future__ import annotations


class PlanningError(Exception):
    """Base domain error for Mission planning failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class UnknownTwinVersion(PlanningError):  # noqa: N818
    """Twin version is unknown, unsupported, or inconsistent with decisions."""


class InvalidDecisionVersion(PlanningError):  # noqa: N818
    """Referenced Twin decision version is invalid or unsupported."""


class UnsupportedPlanningContract(PlanningError):  # noqa: N818
    """Planning contract / version is not supported."""


class BrokenLearningObjectiveReference(PlanningError):  # noqa: N818
    """Learning objective reference is missing or broken."""


class BrokenConceptReference(PlanningError):  # noqa: N818
    """Concept reference required for a mission candidate is blank or broken."""


class MissingProvenance(PlanningError):  # noqa: N818
    """Required provenance identifiers are missing or blank."""


class IncompleteProvenance(PlanningError):  # noqa: N818
    """Provenance chain required for Mission explainability is incomplete."""


class DuplicateMissionRequest(PlanningError):  # noqa: N818
    """Identical mission planning request was already processed."""


class InvalidPlanningSchema(PlanningError):  # noqa: N818
    """Planning payload / schema fails structural validation."""


class PlanningRejected(PlanningError):  # noqa: N818
    """Planning batch refused before apply (validation failed)."""


class MissingLearnerState(PlanningError):  # noqa: N818
    """Required Twin belief fields are absent — never inferred."""
