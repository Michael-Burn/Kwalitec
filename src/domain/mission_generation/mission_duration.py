"""MissionDuration — estimated sitting time for a generated mission.

Architecture Source
    LEARNING_EPISODE_TYPES.md (duration bands)
Concept
    Mission Duration
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.enums import MissionDurationBand


@dataclass(frozen=True, slots=True)
class MissionDuration(EducationalValueObject):
    """Immutable estimated duration for a MissionSpecification.

    Duration constrains the sitting; it is never the educational purpose.
    """

    planned_minutes: int
    band: MissionDurationBand

    def _validate(self) -> None:
        if not isinstance(self.planned_minutes, int) or isinstance(
            self.planned_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "planned_minutes must be an integer",
                invariant="MissionDuration.planned_minutes.type",
            )
        if self.planned_minutes <= 0:
            raise EducationalInvariantViolation(
                "planned_minutes must be positive",
                invariant="MissionDuration.planned_minutes.positive",
            )
        if not isinstance(self.band, MissionDurationBand):
            raise EducationalInvariantViolation(
                "band must be a MissionDurationBand",
                invariant="MissionDuration.band.type",
            )

    @classmethod
    def of(cls, planned_minutes: int) -> MissionDuration:
        """Construct duration with band derived deterministically from minutes."""
        return cls(planned_minutes=planned_minutes, band=cls.band_for(planned_minutes))

    @staticmethod
    def band_for(planned_minutes: int) -> MissionDurationBand:
        """Map planned minutes to illustrative duration bands."""
        if planned_minutes <= 15:
            return MissionDurationBand.SHORT
        if planned_minutes <= 35:
            return MissionDurationBand.MEDIUM
        return MissionDurationBand.LONG

    def is_short(self) -> bool:
        return self.band is MissionDurationBand.SHORT

    def is_medium(self) -> bool:
        return self.band is MissionDurationBand.MEDIUM

    def is_long(self) -> bool:
        return self.band is MissionDurationBand.LONG
