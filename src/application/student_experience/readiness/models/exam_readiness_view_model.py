"""ExamReadinessViewModel — top-level Exam Readiness Experience surface."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)
from application.student_experience.readiness.ids import ReadinessId
from application.student_experience.readiness.models.action_plan_card import (
    ActionPlanCard,
)
from application.student_experience.readiness.models.confidence_card import (
    ConfidenceCard,
)
from application.student_experience.readiness.models.evidence_quality_card import (
    EvidenceQualityCard,
)
from application.student_experience.readiness.models.readiness_card import (
    ReadinessCard,
)
from application.student_experience.readiness.models.readiness_trend_card import (
    ReadinessTrendCard,
)
from application.student_experience.readiness.models.risk_card import RiskCard
from application.student_experience.readiness.models.strength_card import StrengthCard
from application.student_experience.readiness.models.upcoming_milestone_card import (
    UpcomingMilestoneCard,
)


@dataclass(frozen=True, slots=True)
class ExamReadinessViewModel:
    """Immutable Exam Readiness Experience view model.

    Composes Education OS outputs into transparent readiness presentation.
    Never carries raw Education OS aggregates or internal architecture types.
    """

    readiness_id: ReadinessId
    student_id: str
    composed_at: datetime
    readiness: ReadinessCard
    trend: ReadinessTrendCard
    confidence: ConfidenceCard
    strengths: StrengthCard
    risks: RiskCard
    action_plan: ActionPlanCard
    upcoming_milestones: UpcomingMilestoneCard
    evidence_quality: EvidenceQualityCard

    def __post_init__(self) -> None:
        if not isinstance(self.readiness_id, ReadinessId):
            raise ReadinessInvariantViolation(
                "readiness_id must be a ReadinessId",
                invariant="ExamReadinessViewModel.readiness_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ReadinessInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ExamReadinessViewModel.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise ReadinessInvariantViolation(
                "composed_at must be a datetime",
                invariant="ExamReadinessViewModel.composed_at.type",
            )
        expected = {
            "readiness": ReadinessCard,
            "trend": ReadinessTrendCard,
            "confidence": ConfidenceCard,
            "strengths": StrengthCard,
            "risks": RiskCard,
            "action_plan": ActionPlanCard,
            "upcoming_milestones": UpcomingMilestoneCard,
            "evidence_quality": EvidenceQualityCard,
        }
        for name, expected_type in expected.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise ReadinessInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"ExamReadinessViewModel.{name}.type",
                )
