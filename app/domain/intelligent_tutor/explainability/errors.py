"""Explicit Tutor explanation errors (AP-002D6).

Never silently repair malformed explanations or invent missing provenance.
"""

from __future__ import annotations


class ExplanationError(Exception):
    """Base domain error for Tutor explanation failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class UnknownTwinVersion(ExplanationError):  # noqa: N818
    """Twin version is unknown, unsupported, or inconsistent with inputs."""


class TwinVersionMismatch(ExplanationError):  # noqa: N818
    """Twin version does not match decision / mission provenance."""


class InvalidDecisionVersion(ExplanationError):  # noqa: N818
    """Referenced Twin decision version is invalid or unsupported."""


class MissionVersionMismatch(ExplanationError):  # noqa: N818
    """Study mission plan version does not match expected planning contract."""


class UnsupportedExplanationContract(ExplanationError):  # noqa: N818
    """Explanation contract / version is not supported."""


class BrokenConceptReference(ExplanationError):  # noqa: N818
    """Concept reference required for an explanation is blank or broken."""


class BrokenLearningObjectiveReference(ExplanationError):  # noqa: N818
    """Learning objective reference is missing or broken."""


class MissingProvenance(ExplanationError):  # noqa: N818
    """Required provenance identifiers are missing or blank."""


class IncompleteProvenance(ExplanationError):  # noqa: N818
    """Provenance chain required for Tutor explainability is incomplete."""


class UnknownExplanationSchema(ExplanationError):  # noqa: N818
    """Explanation section / schema kind is unknown."""


class InvalidExplanationSchema(ExplanationError):  # noqa: N818
    """Explanation payload / schema fails structural validation."""


class ExplanationRejected(ExplanationError):  # noqa: N818
    """Explanation batch refused before emit (validation failed)."""


class DuplicateExplanationRequest(ExplanationError):  # noqa: N818
    """Identical explanation request was already processed."""


class MissingExplanationInput(ExplanationError):  # noqa: N818
    """Required validated Twin / decision / mission input is absent."""
