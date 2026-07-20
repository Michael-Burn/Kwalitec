"""Episode sequence — ordered educational stages within an episode.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md / LEARNING_EPISODE_SEQUENCE.md
Concept
    Episode Sequence / Episode Step Kind
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EpisodeStepKind(EducationalValueObject):
    """Extensible educational stage kind for an episode step.

    Pedagogies are not hard-coded as a closed catalogue. Well-known examples
    (explanation, worked example, guided practice, etc.) are convenience
    factories; any non-empty kind token is lawful.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_non_empty_text(self.value, "EpisodeStepKind"),
        )

    def __str__(self) -> str:
        return self.value

    @classmethod
    def explanation(cls) -> EpisodeStepKind:
        return cls("explanation")

    @classmethod
    def worked_example(cls) -> EpisodeStepKind:
        return cls("worked_example")

    @classmethod
    def guided_practice(cls) -> EpisodeStepKind:
        return cls("guided_practice")

    @classmethod
    def independent_practice(cls) -> EpisodeStepKind:
        return cls("independent_practice")

    @classmethod
    def reflection(cls) -> EpisodeStepKind:
        return cls("reflection")

    @classmethod
    def custom(cls, value: str) -> EpisodeStepKind:
        """Create an open-vocabulary step kind."""
        return cls(value)


@dataclass(frozen=True, slots=True)
class EpisodeStepId(EducationalValueObject):
    """Identity of an episode step within a Learning Episode."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EpisodeStepId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EpisodeSequence(EducationalValueObject):
    """Ordered educational stage plan for a Learning Episode.

    Sequence identity is the ordered tuple of step identities. Advancement must
    respect required ordering (Learning Episode Invariant sequencing).
    """

    step_ids: tuple[EpisodeStepId, ...]
    required_step_ids: tuple[EpisodeStepId, ...]

    def _validate(self) -> None:
        if not self.step_ids:
            raise EducationalInvariantViolation(
                "episode sequence must contain at least one step",
                invariant="EpisodeSequence.steps.min_one",
            )
        for step_id in self.step_ids:
            if not isinstance(step_id, EpisodeStepId):
                raise EducationalInvariantViolation(
                    "step_ids must contain EpisodeStepId values",
                    invariant="EpisodeSequence.step_ids.type",
                )
        if len(set(self.step_ids)) != len(self.step_ids):
            raise EducationalInvariantViolation(
                "episode sequence must not contain duplicate step identities",
                invariant="EpisodeSequence.step_ids.unique",
            )
        required = tuple(self.required_step_ids)
        for step_id in required:
            if not isinstance(step_id, EpisodeStepId):
                raise EducationalInvariantViolation(
                    "required_step_ids must contain EpisodeStepId values",
                    invariant="EpisodeSequence.required_step_ids.type",
                )
            if step_id not in self.step_ids:
                raise EducationalInvariantViolation(
                    "required step must belong to the sequence",
                    invariant="EpisodeSequence.required_step_ids.membership",
                )
        if len(set(required)) != len(required):
            raise EducationalInvariantViolation(
                "required_step_ids must be unique",
                invariant="EpisodeSequence.required_step_ids.unique",
            )
        if not required:
            raise EducationalInvariantViolation(
                "episode sequence must declare at least one required step",
                invariant="EpisodeSequence.required_step_ids.min_one",
            )
        object.__setattr__(self, "required_step_ids", required)

    def index_of(self, step_id: EpisodeStepId) -> int:
        """Return zero-based position of ``step_id`` in the sequence."""
        try:
            return self.step_ids.index(step_id)
        except ValueError as exc:
            raise EducationalInvariantViolation(
                "step is not part of this episode sequence",
                invariant="EpisodeSequence.step.not_found",
            ) from exc

    def is_required(self, step_id: EpisodeStepId) -> bool:
        """True when ``step_id`` is a required educational stage."""
        return step_id in self.required_step_ids

    def next_after(self, step_id: EpisodeStepId) -> EpisodeStepId | None:
        """Return the next step identity, or None at the end of the sequence."""
        index = self.index_of(step_id)
        nxt = index + 1
        if nxt >= len(self.step_ids):
            return None
        return self.step_ids[nxt]

    @property
    def length(self) -> int:
        return len(self.step_ids)
