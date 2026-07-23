"""Learning environment — the setting of the underlying interaction.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Learning Environment
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.enums import LearningEnvironmentKind
from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class LearningEnvironment(EducationalValueObject):
    """Immutable description of where/how a student interaction took place.

    The environment describes the *setting* of an interaction — a mission
    run, a study session, a review queue, and so on. It does not describe
    curriculum position (see ``LearningContext``).
    """

    kind: LearningEnvironmentKind
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.kind, LearningEnvironmentKind):
            raise EducationalInvariantViolation(
                "kind must be a LearningEnvironmentKind",
                invariant="LearningEnvironment.kind.type",
            )
        if self.label is not None:
            object.__setattr__(
                self, "label", require_non_empty_text(self.label, "label")
            )

    @classmethod
    def of(
        cls, kind: LearningEnvironmentKind, *, label: str | None = None
    ) -> LearningEnvironment:
        return cls(kind=kind, label=label)

    def __str__(self) -> str:
        return self.kind.value
