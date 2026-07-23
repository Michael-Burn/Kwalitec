"""HomeInputs — caller-supplied Education OS artefacts for home composition."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.revision_planner.exam_target import ExamTarget
from application.education.revision_planner.execution_history import ExecutionHistory
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.home.errors import HomeInvariantViolation
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)


@dataclass(frozen=True, slots=True)
class HomeInputs:
    """Immutable bundle of Education OS outputs for Student Home composition.

    All educational artefacts are optional so the home surface degrades
    gracefully. ``student_id`` and ``as_of`` are always required for
    deterministic composition. ``as_of`` is caller-supplied — never wall clock.
    """

    student_id: str
    as_of: datetime
    evaluation: EducationalEvaluation | None = None
    assessment: MasteryAssessment | None = None
    recommendation_set: RecommendationSet | None = None
    mission_plan: MissionPlan | None = None
    schedule: StudySchedule | None = None
    current_execution: MissionExecution | None = None
    execution_history: ExecutionHistory | None = None
    exam_target: ExamTarget | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise HomeInvariantViolation(
                "student_id must be a non-empty string",
                invariant="HomeInputs.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.as_of, datetime):
            raise HomeInvariantViolation(
                "as_of must be a datetime",
                invariant="HomeInputs.as_of.type",
            )
        if self.evaluation is not None and not isinstance(
            self.evaluation, EducationalEvaluation
        ):
            raise HomeInvariantViolation(
                "evaluation must be an EducationalEvaluation when provided",
                invariant="HomeInputs.evaluation.type",
            )
        if self.assessment is not None and not isinstance(
            self.assessment, MasteryAssessment
        ):
            raise HomeInvariantViolation(
                "assessment must be a MasteryAssessment when provided",
                invariant="HomeInputs.assessment.type",
            )
        if self.recommendation_set is not None and not isinstance(
            self.recommendation_set, RecommendationSet
        ):
            raise HomeInvariantViolation(
                "recommendation_set must be a RecommendationSet when provided",
                invariant="HomeInputs.recommendation_set.type",
            )
        if self.mission_plan is not None and not isinstance(
            self.mission_plan, MissionPlan
        ):
            raise HomeInvariantViolation(
                "mission_plan must be a MissionPlan when provided",
                invariant="HomeInputs.mission_plan.type",
            )
        if self.schedule is not None and not isinstance(self.schedule, StudySchedule):
            raise HomeInvariantViolation(
                "schedule must be a StudySchedule when provided",
                invariant="HomeInputs.schedule.type",
            )
        if self.current_execution is not None and not isinstance(
            self.current_execution, MissionExecution
        ):
            raise HomeInvariantViolation(
                "current_execution must be a MissionExecution when provided",
                invariant="HomeInputs.current_execution.type",
            )
        if self.execution_history is not None and not isinstance(
            self.execution_history, ExecutionHistory
        ):
            raise HomeInvariantViolation(
                "execution_history must be an ExecutionHistory when provided",
                invariant="HomeInputs.execution_history.type",
            )
        if self.exam_target is not None and not isinstance(
            self.exam_target, ExamTarget
        ):
            raise HomeInvariantViolation(
                "exam_target must be an ExamTarget when provided",
                invariant="HomeInputs.exam_target.type",
            )
        if self.exam_target is None and self.schedule is not None:
            object.__setattr__(self, "exam_target", self.schedule.exam_target)
