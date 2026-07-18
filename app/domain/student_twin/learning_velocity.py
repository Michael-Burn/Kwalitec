"""Learning velocity — rate of educational progress from evidence timing."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class LearningVelocity:
    """Deterministic velocity metrics derived from evidence chronology.

    Positive velocity means mastery/knowledge has been rising with recent evidence.
    Does not optimise engagement or screen time.
    """

    events_per_day: float = 0.0
    mastery_delta: float = 0.0
    knowledge_delta: float = 0.0
    window_days: float = 0.0
    confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> LearningVelocity:
        """Return an empty velocity state."""
        return cls()

    @classmethod
    def create(
        cls,
        *,
        events_per_day: float = 0.0,
        mastery_delta: float = 0.0,
        knowledge_delta: float = 0.0,
        window_days: float = 0.0,
        confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> LearningVelocity:
        """Construct LearningVelocity with validated numeric fields."""
        epd = _non_negative(events_per_day, "events_per_day")
        wd = _non_negative(window_days, "window_days")
        md = _signed_unit(mastery_delta, "mastery_delta")
        kd = _signed_unit(knowledge_delta, "knowledge_delta")
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        return cls(
            events_per_day=epd,
            mastery_delta=md,
            knowledge_delta=kd,
            window_days=wd,
            confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
        )

    @property
    def is_active(self) -> bool:
        """True when recent evidence activity is non-zero."""
        return self.events_per_day > 0.0

    @property
    def is_improving(self) -> bool:
        """True when mastery delta is strictly positive."""
        return self.mastery_delta > 0.0


def _non_negative(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a non-negative number")
    numeric = float(value)
    if numeric < 0.0:
        raise ValueError(f"{field_name} must be a non-negative number")
    return numeric


def _signed_unit(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [-1, 1]")
    numeric = float(value)
    if numeric < -1.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [-1, 1]")
    return numeric
