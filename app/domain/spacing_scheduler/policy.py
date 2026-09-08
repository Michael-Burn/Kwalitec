"""Configurable spacing interval policy.

Interval rules live here so learner evidence can later retune defaults
without rebuilding the scheduler. Policy never consults mastery or weakness.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.spacing_scheduler.types import ExposureKind


@dataclass(frozen=True, slots=True)
class SpacingIntervalPolicy:
    """Deterministic interval ladder and adjustment rules.

    Defaults follow a simple widening ladder after on-time completions and
    a one-step retreat after late or missed reviews. All values are days.
    """

    initial_interval_days: int = 1
    interval_ladder_days: tuple[int, ...] = (1, 3, 7, 14, 30)
    min_interval_days: int = 1
    max_interval_days: int = 60

    def __post_init__(self) -> None:
        if self.initial_interval_days < 1:
            raise ValueError("initial_interval_days must be >= 1")
        if self.min_interval_days < 1:
            raise ValueError("min_interval_days must be >= 1")
        if self.max_interval_days < self.min_interval_days:
            raise ValueError("max_interval_days must be >= min_interval_days")
        if not self.interval_ladder_days:
            raise ValueError("interval_ladder_days must be non-empty")
        if any(d < 1 for d in self.interval_ladder_days):
            raise ValueError("interval_ladder_days entries must be >= 1")

    def interval_after(
        self,
        *,
        prior_interval_days: int | None,
        exposure_kind: ExposureKind,
    ) -> int:
        """Return the next interval for the given exposure kind."""
        if exposure_kind is ExposureKind.INITIAL_COMPLETION:
            return self._clamp(self.initial_interval_days)

        prior = prior_interval_days or self.initial_interval_days
        if exposure_kind is ExposureKind.ON_TIME_REVIEW:
            return self._clamp(self._next_ladder_step(prior))
        if exposure_kind in {
            ExposureKind.LATE_REVIEW,
            ExposureKind.MISSED_REVIEW,
        }:
            return self._clamp(self._previous_ladder_step(prior))
        raise ValueError(f"unsupported exposure_kind: {exposure_kind}")

    def _next_ladder_step(self, current: int) -> int:
        for step in self.interval_ladder_days:
            if step > current:
                return step
        return max(self.interval_ladder_days)

    def _previous_ladder_step(self, current: int) -> int:
        previous = self.min_interval_days
        for step in self.interval_ladder_days:
            if step < current:
                previous = step
            else:
                break
        return previous

    def _clamp(self, days: int) -> int:
        return max(self.min_interval_days, min(self.max_interval_days, days))
