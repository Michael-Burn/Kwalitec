"""ReadinessTrendCard — historical readiness direction projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import ReadinessDirection
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ReadinessTrendCard:
    """Immutable readiness trend card — projects existing stability signals.

    Never forecasts future readiness using AI or invented scores.
    """

    direction: ReadinessDirection
    direction_message: str
    summary: str
    has_trend_data: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.direction, ReadinessDirection):
            raise ReadinessInvariantViolation(
                "direction must be a ReadinessDirection",
                invariant="ReadinessTrendCard.direction.type",
            )
        for name in ("direction_message", "summary"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReadinessTrendCard.{name}.required",
                )
            object.__setattr__(self, name, value)
