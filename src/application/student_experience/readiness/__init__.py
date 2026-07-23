"""Exam Readiness Experience — XP-003.

Application-layer composition of Education OS outputs into a transparent
readiness assessment.

Responsibilities
    Project existing educational reasoning into immutable view models.

Non-responsibilities
    Estimate mastery, generate recommendations, generate missions,
    schedule work, persist data, forecast exams with AI, or render charts.
"""

from __future__ import annotations

from application.student_experience.readiness.enums import (
    ActionPlanItemKind,
    AssessmentConfidenceCategory,
    ConsistencyBand,
    EvidenceQualityBand,
    EvidenceQuantityBand,
    ReadinessCategory,
    ReadinessDirection,
    ReadinessMilestoneKind,
    RiskKind,
    StrengthKind,
)
from application.student_experience.readiness.errors import (
    ReadinessExperienceError,
    ReadinessInvariantViolation,
)
from application.student_experience.readiness.exam_readiness_service import (
    ExamReadinessService,
)
from application.student_experience.readiness.ids import (
    ReadinessId,
    ReadinessSnapshotId,
)
from application.student_experience.readiness.models import (
    ActionPlanCard,
    ActionPlanItem,
    ConfidenceCard,
    EvidenceQualityCard,
    ExamReadinessViewModel,
    ReadinessCard,
    ReadinessMilestone,
    ReadinessSnapshot,
    ReadinessTrendCard,
    RiskCard,
    RiskItem,
    StrengthCard,
    StrengthItem,
    UpcomingMilestoneCard,
)
from application.student_experience.readiness.ports import (
    ReadinessExportProvider,
    ReadinessPublisher,
)
from application.student_experience.readiness.readiness_inputs import ReadinessInputs

__all__ = [
    # Service
    "ExamReadinessService",
    # Inputs
    "ReadinessInputs",
    # Identity
    "ReadinessId",
    "ReadinessSnapshotId",
    # View models
    "ExamReadinessViewModel",
    "ReadinessCard",
    "ReadinessTrendCard",
    "ConfidenceCard",
    "StrengthCard",
    "StrengthItem",
    "RiskCard",
    "RiskItem",
    "ActionPlanCard",
    "ActionPlanItem",
    "UpcomingMilestoneCard",
    "ReadinessMilestone",
    "EvidenceQualityCard",
    "ReadinessSnapshot",
    # Enums
    "ReadinessCategory",
    "ReadinessDirection",
    "AssessmentConfidenceCategory",
    "EvidenceQualityBand",
    "EvidenceQuantityBand",
    "ConsistencyBand",
    "StrengthKind",
    "RiskKind",
    "ActionPlanItemKind",
    "ReadinessMilestoneKind",
    # Errors
    "ReadinessExperienceError",
    "ReadinessInvariantViolation",
    # Ports
    "ReadinessPublisher",
    "ReadinessExportProvider",
]
