"""Episode outcome — modest evaluation relative to the teaching goal.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / LEARNING_EPISODE_INVARIANTS.md (E5, E13)
Concept
    Episode Outcome
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.enums import EpisodeOutcomeKind


@dataclass(frozen=True, slots=True)
class EpisodeOutcomeId(EducationalValueObject):
    """Identity of an episode outcome judgement."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EpisodeOutcomeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EpisodeOutcome(EducationalEntity):
    """Educational outcome of a Learning Episode — never mastery.

    Completing an episode answers whether engagement closed; the outcome is a
    modest judgement against the single teaching goal (E5, E13).
    """

    outcome_id: EpisodeOutcomeId
    kind: EpisodeOutcomeKind
    summary: str

    @property
    def entity_id(self) -> EpisodeOutcomeId:
        return self.outcome_id

    def _validate(self) -> None:
        if not isinstance(self.outcome_id, EpisodeOutcomeId):
            raise EducationalInvariantViolation(
                "outcome_id must be an EpisodeOutcomeId",
                invariant="EpisodeOutcome.outcome_id.type",
            )
        if not isinstance(self.kind, EpisodeOutcomeKind):
            raise EducationalInvariantViolation(
                "kind must be an EpisodeOutcomeKind",
                invariant="EpisodeOutcome.kind.type",
            )
        object.__setattr__(
            self,
            "summary",
            require_non_empty_text(self.summary, "summary"),
        )
        lowered = self.summary.casefold()
        if "master" in lowered:
            raise EducationalInvariantViolation(
                "episode outcome must not declare mastery",
                invariant="EpisodeOutcome.no_mastery",
            )

    def is_terminal_success(self) -> bool:
        """True when the teaching goal was fully or partially advanced."""
        return self.kind in {
            EpisodeOutcomeKind.GOAL_ACHIEVED,
            EpisodeOutcomeKind.GOAL_PARTIALLY_ACHIEVED,
        }

    def is_interrupt_kind(self) -> bool:
        return self.kind is EpisodeOutcomeKind.INTERRUPTED

    def requires_further_action(self) -> bool:
        return self.kind in {
            EpisodeOutcomeKind.REQUIRES_REMEDIATION,
            EpisodeOutcomeKind.REQUIRES_FOLLOW_UP,
            EpisodeOutcomeKind.INTERRUPTED,
        }
