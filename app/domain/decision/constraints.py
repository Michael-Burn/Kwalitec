"""Framework-free Constraints for Decision Engine feasibility bounding.

Constraints bound ambition; they do not invent educational need or erase
high-weight curriculum risk.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IntensityPosture(StrEnum):
    """Sustainable intensity posture for the current session window."""

    AMPLE = "ample"
    MODERATE = "moderate"
    LIMITED = "limited"
    PROTECT = "protect"


class ConstraintClass(StrEnum):
    """Constraint classes acknowledged on Decisions when demotions apply."""

    SESSION_TIME = "session_time"
    INTENSITY = "intensity"
    BEHAVIOUR_SUSTAINABILITY = "behaviour_sustainability"
    GOAL_CAPACITY = "goal_capacity"


@dataclass(frozen=True)
class Constraints:
    """Session feasibility envelope for one Decision evaluation.

    Attributes:
        available_minutes: Minutes available now (None = unspecified).
        intensity: Sustainable intensity posture.
        burnout_risk: True when Behaviour / capacity flags sustainability risk.
        max_intensity_minutes: Soft ceiling for intensive work this session.
        note_tags: Structural feasibility tags.
    """

    available_minutes: int | None = None
    intensity: IntensityPosture = IntensityPosture.AMPLE
    burnout_risk: bool = False
    max_intensity_minutes: int | None = None
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        available_minutes: int | None = None,
        intensity: IntensityPosture | str = IntensityPosture.AMPLE,
        burnout_risk: bool = False,
        max_intensity_minutes: int | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> Constraints:
        """Construct Constraints.

        Raises:
            ValueError: If minute fields are negative.
        """
        if available_minutes is not None and available_minutes < 0:
            raise ValueError("available_minutes must be non-negative")
        if max_intensity_minutes is not None and max_intensity_minutes < 0:
            raise ValueError("max_intensity_minutes must be non-negative")
        inten = (
            intensity
            if isinstance(intensity, IntensityPosture)
            else IntensityPosture(intensity)
        )
        return cls(
            available_minutes=available_minutes,
            intensity=inten,
            burnout_risk=burnout_risk,
            max_intensity_minutes=max_intensity_minutes,
            note_tags=tuple(note_tags or ()),
        )

    @property
    def scarce_time(self) -> bool:
        """True when available minutes are structurally scarce (< 25)."""
        return self.available_minutes is not None and self.available_minutes < 25

    @property
    def protect_intensity(self) -> bool:
        """True when sustainability risk or protect posture applies."""
        return self.burnout_risk or self.intensity == IntensityPosture.PROTECT
