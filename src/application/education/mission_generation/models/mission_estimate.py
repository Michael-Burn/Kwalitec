"""MissionEstimate — deterministic duration and workload estimate."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionDurationBand
from application.education.mission_generation.errors import MissionInvariantViolation

_BAND_THRESHOLDS: tuple[tuple[int, MissionDurationBand], ...] = (
    (15, MissionDurationBand.SHORT),
    (35, MissionDurationBand.MEDIUM),
)


@dataclass(frozen=True, slots=True)
class MissionEstimate:
    """Immutable duration estimate for a mission.

    ``duration_band`` is always derived from ``duration_minutes`` so the
    two can never disagree. Estimates are instructional planning figures —
    never mastery scores.
    """

    duration_minutes: int
    workload_units: float = 1.0

    def __post_init__(self) -> None:
        if isinstance(self.duration_minutes, bool) or not isinstance(
            self.duration_minutes, int
        ):
            raise MissionInvariantViolation(
                "duration_minutes must be an integer",
                invariant="MissionEstimate.duration_minutes.type",
            )
        if self.duration_minutes < 1:
            raise MissionInvariantViolation(
                "duration_minutes must be >= 1",
                invariant="MissionEstimate.duration_minutes.positive",
            )
        if isinstance(self.workload_units, bool) or not isinstance(
            self.workload_units, int | float
        ):
            raise MissionInvariantViolation(
                "workload_units must be a real number",
                invariant="MissionEstimate.workload_units.type",
            )
        units = float(self.workload_units)
        if units <= 0.0:
            raise MissionInvariantViolation(
                "workload_units must be > 0",
                invariant="MissionEstimate.workload_units.positive",
            )
        object.__setattr__(self, "workload_units", round(units, 4))

    @property
    def duration_band(self) -> MissionDurationBand:
        for threshold, band in _BAND_THRESHOLDS:
            if self.duration_minutes <= threshold:
                return band
        return MissionDurationBand.LONG

    def exceeds(self, minutes: int) -> bool:
        return self.duration_minutes > minutes
