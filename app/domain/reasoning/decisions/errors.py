"""Explicit decision / Twin-update errors (AP-002D3).

Never silently repair malformed decisions or invent missing educational data.
"""

from __future__ import annotations


class DecisionError(Exception):
    """Base domain error for educational decision failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class UnknownDecisionCategory(DecisionError):  # noqa: N818
    """Decision category is not in the AP-002D3 catalogue."""


class UnsupportedDecisionVersion(DecisionError):  # noqa: N818
    """Decision version is not supported for Twin updates."""


class DuplicateDecision(DecisionError):  # noqa: N818
    """Decision identifier collides within a set or was already applied."""


class BrokenDecisionProvenance(DecisionError):  # noqa: N818
    """Required provenance identifiers are missing or blank."""


class MissingDecisionTraceability(DecisionError):  # noqa: N818
    """Traceability chain required for Twin explainability is incomplete."""


class UnknownConceptReference(DecisionError):  # noqa: N818
    """Concept reference required for a mastery decision is blank or unknown."""


class InvalidLearningObjectiveReference(DecisionError):  # noqa: N818
    """Learning objective reference is missing or invalid."""


class InvalidDecisionSchema(DecisionError):  # noqa: N818
    """Decision payload / schema fails structural validation."""


class TwinUpdateRejected(DecisionError):  # noqa: N818
    """Twin refused a decision set (validation failed before apply)."""
