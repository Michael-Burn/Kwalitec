"""Student Home — primary experience answering what to do next and why."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_experience.experience_session import StartSessionAction
from app.domain.student_experience.recommendation_explanation import (
    RecommendationExplanation,
)


@dataclass(frozen=True)
class StudentHome:
    """Domain projection for the Student Home surface.

    Assembles presentation fields from upstream educational facts.
    Owns no readiness, recommendation, or mission calculation.
    """

    student_id: str
    greeting: str = ""
    examination_label: str = ""
    exam_countdown_days: int | None = None
    exam_readiness: float | None = None
    exam_readiness_label: str = ""
    recommendation_title: str = ""
    recommendation_summary: str = ""
    estimated_study_minutes: int | None = None
    expected_readiness_improvement: float | None = None
    explanation: RecommendationExplanation | None = None
    start_session: StartSessionAction | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        greeting: str = "",
        examination_label: str = "",
        exam_countdown_days: int | None = None,
        exam_readiness: float | None = None,
        exam_readiness_label: str = "",
        recommendation_title: str = "",
        recommendation_summary: str = "",
        estimated_study_minutes: int | None = None,
        expected_readiness_improvement: float | None = None,
        explanation: RecommendationExplanation | None = None,
        start_session: StartSessionAction | None = None,
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
        display_name: str = "",
    ) -> StudentHome:
        """Build a Student Home projection."""
        sid = _require_non_empty(student_id, "student_id")
        if exam_countdown_days is not None and exam_countdown_days < 0:
            raise ValueError("exam_countdown_days must be non-negative")
        if estimated_study_minutes is not None and estimated_study_minutes < 0:
            raise ValueError("estimated_study_minutes must be non-negative")
        if exam_readiness is not None and not 0.0 <= exam_readiness <= 1.0:
            raise ValueError("exam_readiness must be between 0 and 1")
        name = (display_name or "").strip()
        resolved_greeting = (greeting or "").strip() or _default_greeting(name)
        readiness_label = (exam_readiness_label or "").strip()
        if not readiness_label and exam_readiness is not None:
            readiness_label = readiness_band_label(exam_readiness)
        return cls(
            student_id=sid,
            greeting=resolved_greeting,
            examination_label=(examination_label or "").strip(),
            exam_countdown_days=exam_countdown_days,
            exam_readiness=exam_readiness,
            exam_readiness_label=readiness_label,
            recommendation_title=(recommendation_title or "").strip(),
            recommendation_summary=(recommendation_summary or "").strip(),
            estimated_study_minutes=estimated_study_minutes,
            expected_readiness_improvement=expected_readiness_improvement,
            explanation=explanation,
            start_session=start_session,
            metadata=tuple(metadata or ()),
        )

    @property
    def has_recommendation(self) -> bool:
        """True when today's recommendation is present."""
        return bool(self.recommendation_title.strip())

    @property
    def can_start_session(self) -> bool:
        """True when Start Session is actionable."""
        return bool(self.start_session and self.start_session.can_start)


def readiness_band_label(score: float) -> str:
    """Map a readiness ratio to a student-facing band label."""
    if score < 0.35:
        return "Building"
    if score < 0.6:
        return "Developing"
    if score < 0.8:
        return "On Track"
    return "Exam Ready"


def _default_greeting(display_name: str) -> str:
    if display_name:
        return f"Welcome back, {display_name}."
    return "Welcome back."


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
