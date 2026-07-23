"""MissionOrdering — deterministic rank within a plan."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionPriorityBand
from application.education.mission_generation.errors import MissionInvariantViolation

_BAND_THRESHOLDS: tuple[tuple[float, MissionPriorityBand], ...] = (
    (0.25, MissionPriorityBand.LOW),
    (0.50, MissionPriorityBand.MEDIUM),
    (0.75, MissionPriorityBand.HIGH),
)


@dataclass(frozen=True, slots=True)
class MissionOrdering:
    """Immutable rank position of a mission inside a plan.

    ``rank`` is 1-based; denser ranks are higher priority. The attached
    ``priority_magnitude`` mirrors the priority used to compute the rank.
    """

    rank: int
    priority_magnitude: float

    def __post_init__(self) -> None:
        if isinstance(self.rank, bool) or not isinstance(self.rank, int):
            raise MissionInvariantViolation(
                "rank must be an integer",
                invariant="MissionOrdering.rank.type",
            )
        if self.rank < 1:
            raise MissionInvariantViolation(
                "rank must be a positive 1-based integer",
                invariant="MissionOrdering.rank.positive",
            )
        if isinstance(self.priority_magnitude, bool) or not isinstance(
            self.priority_magnitude, int | float
        ):
            raise MissionInvariantViolation(
                "priority_magnitude must be a real number",
                invariant="MissionOrdering.priority_magnitude.type",
            )
        magnitude = float(self.priority_magnitude)
        if magnitude < 0.0 or magnitude > 1.0:
            raise MissionInvariantViolation(
                "priority_magnitude must be between 0.0 and 1.0 inclusive",
                invariant="MissionOrdering.priority_magnitude.range",
            )
        object.__setattr__(self, "priority_magnitude", round(magnitude, 4))

    @property
    def priority_band(self) -> MissionPriorityBand:
        for threshold, band in _BAND_THRESHOLDS:
            if self.priority_magnitude < threshold:
                return band
        return MissionPriorityBand.CRITICAL
