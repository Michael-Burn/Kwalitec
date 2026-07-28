"""Explicit interpretation errors (AP-002D2).

Never silently repair malformed evidence or invent missing educational data.
"""

from __future__ import annotations


class InterpretationError(Exception):
    """Base domain/application error for evidence interpretation failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.__class__.__name__


class UnknownObservationCategory(InterpretationError):  # noqa: N818
    """Observation category is not in the AP-002D Design Pack catalogue."""


class BrokenEvidenceReference(InterpretationError):  # noqa: N818
    """Evidence reference is missing, blank, or structurally invalid."""


class MissingLearningObjective(InterpretationError):  # noqa: N818
    """Learning objective reference required for interpretation is absent."""


class InvalidConceptMapping(InterpretationError):  # noqa: N818
    """Concept reference is blank when declared or otherwise invalid."""


class UnsupportedEvidenceSchema(InterpretationError):  # noqa: N818
    """Evidence packaging / schema version is not supported for interpretation."""


class DuplicateInterpretedObservation(InterpretationError):  # noqa: N818
    """Two interpreted observations share the same observation identifier."""
