"""Readiness state — preparedness estimate from mastery, retention, confidence."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
)


@dataclass(frozen=True)
class ReadinessState:
    """Overall educational readiness with explicit confidence.

    Does not schedule sessions or generate missions — estimates only.
    """

    readiness_score: float = 0.0
    confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    supporting_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    limiting_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = "insufficient_evidence"

    @classmethod
    def empty(cls) -> ReadinessState:
        """Return an empty readiness state."""
        return cls()

    @classmethod
    def create(
        cls,
        readiness_score: float,
        *,
        confidence: ConfidenceBand | str | None = None,
        confidence_score: float | None = None,
        supporting_topic_ids: list[str] | tuple[str, ...] | None = None,
        limiting_topic_ids: list[str] | tuple[str, ...] | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        rationale: str = "evidence_derived",
    ) -> ReadinessState:
        """Construct a ReadinessState."""
        score = _unit_interval(readiness_score, "readiness_score")
        if confidence is not None:
            band = (
                confidence
                if isinstance(confidence, ConfidenceBand)
                else ConfidenceBand(str(confidence).strip().lower())
            )
        elif confidence_score is not None:
            band = confidence_band_from_score(confidence_score)
        else:
            band = ConfidenceBand.VERY_LOW
        reason = (rationale or "evidence_derived").strip() or "evidence_derived"
        return cls(
            readiness_score=score,
            confidence=band,
            supporting_topic_ids=tuple(supporting_topic_ids or ()),
            limiting_topic_ids=tuple(limiting_topic_ids or ()),
            evidence_ids=tuple(evidence_ids or ()),
            rationale=reason,
        )

    @property
    def is_ready(self) -> bool:
        """Heuristic: readiness >= 0.65 with at least medium confidence."""
        return self.readiness_score >= 0.65 and self.confidence in (
            ConfidenceBand.MEDIUM,
            ConfidenceBand.HIGH,
            ConfidenceBand.VERY_HIGH,
        )


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
