"""Episode duration — planned time constraint, not educational purpose.

Architecture Source
    LEARNING_EPISODE_TYPES.md
Concept
    Episode Duration
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.enums import DurationBand


@dataclass(frozen=True, slots=True)
class EpisodeDuration(EducationalValueObject):
    """Optional planned duration for a Learning Episode.

    Duration constrains an episode; it is never the educational purpose
    (Learning Episode Architecture §2).
    """

    planned_minutes: int | None = None
    band: DurationBand | None = None

    def _validate(self) -> None:
        if self.planned_minutes is None and self.band is None:
            raise EducationalInvariantViolation(
                "episode duration requires planned_minutes and/or band",
                invariant="EpisodeDuration.presence",
            )
        if self.planned_minutes is not None:
            if not isinstance(self.planned_minutes, int):
                raise EducationalInvariantViolation(
                    "planned_minutes must be an integer",
                    invariant="EpisodeDuration.planned_minutes.type",
                )
            if self.planned_minutes <= 0:
                raise EducationalInvariantViolation(
                    "planned_minutes must be positive",
                    invariant="EpisodeDuration.planned_minutes.positive",
                )
        if self.band is not None and not isinstance(self.band, DurationBand):
            raise EducationalInvariantViolation(
                "band must be a DurationBand",
                invariant="EpisodeDuration.band.type",
            )

    def is_short(self) -> bool:
        """True when band is SHORT or planned minutes are within short band."""
        if self.band is DurationBand.SHORT:
            return True
        if self.planned_minutes is not None:
            return self.planned_minutes <= 15
        return False
