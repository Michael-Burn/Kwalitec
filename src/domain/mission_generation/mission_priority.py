"""MissionPriority — instructional ordering projected onto a mission.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Mission Priority
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import UrgencyLevel
from domain.mission_generation.enums import MissionPriorityBand

_BAND_ORDER: tuple[MissionPriorityBand, ...] = (
    MissionPriorityBand.NEGLIGIBLE,
    MissionPriorityBand.LOW,
    MissionPriorityBand.MEDIUM,
    MissionPriorityBand.HIGH,
    MissionPriorityBand.CRITICAL,
)


@dataclass(frozen=True, slots=True)
class MissionPriority(EducationalValueObject):
    """Immutable instructional-ordering projection for a mission.

    Priority answers how urgently this mission should govern the next sitting
    relative to competing educational work. It is not diagnosis severity.
    """

    band: MissionPriorityBand
    urgency: UrgencyLevel
    ratio: float | None = None
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, MissionPriorityBand):
            raise EducationalInvariantViolation(
                "band must be a MissionPriorityBand",
                invariant="MissionPriority.band.type",
            )
        if not isinstance(self.urgency, UrgencyLevel):
            raise EducationalInvariantViolation(
                "urgency must be an UrgencyLevel",
                invariant="MissionPriority.urgency.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="MissionPriority.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="MissionPriority.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "priority rationale must be non-empty when provided",
                    invariant="MissionPriority.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        band: MissionPriorityBand,
        urgency: UrgencyLevel,
        *,
        ratio: float | None = None,
        rationale: str | None = None,
    ) -> MissionPriority:
        return cls(band=band, urgency=urgency, ratio=ratio, rationale=rationale)

    def is_at_least(self, other: MissionPriorityBand) -> bool:
        if other not in _BAND_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known MissionPriorityBand",
                invariant="MissionPriority.is_at_least.band",
            )
        return _BAND_ORDER.index(self.band) >= _BAND_ORDER.index(other)

    def __str__(self) -> str:
        if self.ratio is None:
            return f"{self.band.value}/{self.urgency.value}"
        return f"{self.band.value}({self.ratio:.2f})/{self.urgency.value}"
