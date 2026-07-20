"""ProgressReport — deterministic progress evaluation projection.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Progress Report
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DigitalTwinId, EvidenceId
from domain.mission_generation.ids import MissionSpecificationId
from domain.progress_evaluation.confidence_trend import ConfidenceTrend
from domain.progress_evaluation.enums import StabilityBand
from domain.progress_evaluation.ids import ProgressReportId
from domain.progress_evaluation.intervention_signal import InterventionSignal
from domain.progress_evaluation.learning_velocity import LearningVelocity
from domain.progress_evaluation.mastery_trend import MasteryTrend
from domain.progress_evaluation.progress_metric import ProgressMetric
from domain.progress_evaluation.revision_effectiveness import RevisionEffectiveness
from domain.study_planning.ids import StudyPlanId


@dataclass(frozen=True, slots=True)
class ProgressReport(EducationalValueObject):
    """Fully explainable progress evaluation from Educational OS inputs.

    Contains mastery and confidence trends, learning velocity, knowledge
    stability, revision effectiveness, confidence level, intervention signal,
    and an educational explanation. Pure educational projection — no
    persistence, AI, or visualization.
    """

    report_id: ProgressReportId
    student_id: str
    twin_id: DigitalTwinId
    mastery_trend: MasteryTrend
    learning_velocity: LearningVelocity
    knowledge_stability: StabilityBand
    revision_effectiveness: RevisionEffectiveness
    confidence_level: ConfidenceLevel
    confidence_trend: ConfidenceTrend
    intervention_signal: InterventionSignal
    metrics: tuple[ProgressMetric, ...]
    educational_explanation: str
    evidence_ids: tuple[EvidenceId, ...]
    mission_ids: tuple[MissionSpecificationId, ...]
    plan_ids: tuple[StudyPlanId, ...]

    def _validate(self) -> None:
        if not isinstance(self.report_id, ProgressReportId):
            raise EducationalInvariantViolation(
                "report_id must be a ProgressReportId",
                invariant="ProgressReport.report_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin_id must be a DigitalTwinId",
                invariant="ProgressReport.twin_id.type",
            )
        if not isinstance(self.mastery_trend, MasteryTrend):
            raise EducationalInvariantViolation(
                "mastery_trend must be a MasteryTrend",
                invariant="ProgressReport.mastery_trend.type",
            )
        if not isinstance(self.learning_velocity, LearningVelocity):
            raise EducationalInvariantViolation(
                "learning_velocity must be a LearningVelocity",
                invariant="ProgressReport.learning_velocity.type",
            )
        if not isinstance(self.knowledge_stability, StabilityBand):
            raise EducationalInvariantViolation(
                "knowledge_stability must be a StabilityBand",
                invariant="ProgressReport.knowledge_stability.type",
            )
        if not isinstance(self.revision_effectiveness, RevisionEffectiveness):
            raise EducationalInvariantViolation(
                "revision_effectiveness must be a RevisionEffectiveness",
                invariant="ProgressReport.revision_effectiveness.type",
            )
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "confidence_level must be a ConfidenceLevel",
                invariant="ProgressReport.confidence_level.type",
            )
        if not isinstance(self.confidence_trend, ConfidenceTrend):
            raise EducationalInvariantViolation(
                "confidence_trend must be a ConfidenceTrend",
                invariant="ProgressReport.confidence_trend.type",
            )
        if not isinstance(self.intervention_signal, InterventionSignal):
            raise EducationalInvariantViolation(
                "intervention_signal must be an InterventionSignal",
                invariant="ProgressReport.intervention_signal.type",
            )
        if not isinstance(self.metrics, tuple) or not self.metrics:
            raise EducationalInvariantViolation(
                "metrics must be a non-empty tuple",
                invariant="ProgressReport.metrics.min_one",
            )
        for metric in self.metrics:
            if not isinstance(metric, ProgressMetric):
                raise EducationalInvariantViolation(
                    "metrics must contain ProgressMetric values",
                    invariant="ProgressReport.metrics.item_type",
                )
        object.__setattr__(
            self,
            "educational_explanation",
            require_non_empty_text(
                self.educational_explanation, "educational_explanation"
            ),
        )
        if len(self.educational_explanation) < 24:
            raise EducationalInvariantViolation(
                "educational explanation must be educationally substantive",
                invariant="ProgressReport.educational_explanation.substantive",
            )
        for name, values, item_type in (
            ("evidence_ids", self.evidence_ids, EvidenceId),
            ("mission_ids", self.mission_ids, MissionSpecificationId),
            ("plan_ids", self.plan_ids, StudyPlanId),
        ):
            if not isinstance(values, tuple):
                raise EducationalInvariantViolation(
                    f"{name} must be a tuple",
                    invariant=f"ProgressReport.{name}.type",
                )
            for value in values:
                if not isinstance(value, item_type):
                    raise EducationalInvariantViolation(
                        f"{name} must contain {item_type.__name__} values",
                        invariant=f"ProgressReport.{name}.item_type",
                    )

    @property
    def intervention_required(self) -> bool:
        return self.intervention_signal.required
