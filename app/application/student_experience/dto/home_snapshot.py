"""Immutable HomeSnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.dto.recommendation_alternative_snapshot import (
    RecommendationAlternativeSnapshot,
)
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)


@dataclass(frozen=True)
class StartSessionActionSnapshot:
    """Read-only Start Session action."""

    label: str = "Start Session"
    enabled: bool = True
    can_start: bool = False
    mission_id: str | None = None
    session_id: str | None = None
    estimated_minutes: int | None = None
    topic_title: str = ""


@dataclass(frozen=True)
class HomeSnapshot:
    """Student Home projection DTO."""

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
    explanation: ExplanationSnapshot | None = None
    # EP-006.4: authored readiness MES for Home (drivers / review / next).
    readiness_explanation: ReadinessExplanationSnapshot | None = None
    start_session: StartSessionActionSnapshot | None = None
    has_recommendation: bool = False
    can_start_session: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    # EP-008.1 — Recommendation Trust.
    recommendation_alternatives: tuple[
        RecommendationAlternativeSnapshot, ...
    ] = field(default_factory=tuple)
    trust_state: str = ""
    # EP-008.3 — Recommendation Commitment (preference / intent only).
    commitment: RecommendationCommitmentSnapshot | None = None
