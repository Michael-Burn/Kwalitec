"""ReadinessInputs — caller-supplied Education OS artefacts for readiness."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.revision_planner.exam_target import ExamTarget
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)


@dataclass(frozen=True, slots=True)
class ReadinessInputs:
    """Immutable bundle of Education OS outputs for Exam Readiness composition.

    All educational artefacts are optional so the readiness surface degrades
    gracefully. ``student_id`` and ``as_of`` are always required for
    deterministic composition. ``as_of`` is caller-supplied — never wall clock.

    ``journey_snapshot`` is the Learning Journey compact projection
    (``JourneySnapshot``) — never a raw Education OS aggregate.
    """

    student_id: str
    as_of: datetime
    evaluation: EducationalEvaluation | None = None
    assessment: MasteryAssessment | None = None
    recommendation_set: RecommendationSet | None = None
    schedule: StudySchedule | None = None
    execution_history: tuple[MissionExecution, ...] = ()
    journey_snapshot: JourneySnapshot | None = None
    home_snapshot: HomeSnapshot | None = None
    exam_target: ExamTarget | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ReadinessInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ReadinessInputs.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.as_of, datetime):
            raise ReadinessInvariantViolation(
                "as_of must be a datetime",
                invariant="ReadinessInputs.as_of.type",
            )
        if self.evaluation is not None and not isinstance(
            self.evaluation, EducationalEvaluation
        ):
            raise ReadinessInvariantViolation(
                "evaluation must be an EducationalEvaluation when provided",
                invariant="ReadinessInputs.evaluation.type",
            )
        if self.assessment is not None and not isinstance(
            self.assessment, MasteryAssessment
        ):
            raise ReadinessInvariantViolation(
                "assessment must be a MasteryAssessment when provided",
                invariant="ReadinessInputs.assessment.type",
            )
        if self.recommendation_set is not None and not isinstance(
            self.recommendation_set, RecommendationSet
        ):
            raise ReadinessInvariantViolation(
                "recommendation_set must be a RecommendationSet when provided",
                invariant="ReadinessInputs.recommendation_set.type",
            )
        if self.schedule is not None and not isinstance(self.schedule, StudySchedule):
            raise ReadinessInvariantViolation(
                "schedule must be a StudySchedule when provided",
                invariant="ReadinessInputs.schedule.type",
            )
        object.__setattr__(
            self,
            "execution_history",
            self._normalise_executions(self.execution_history),
        )
        if self.journey_snapshot is not None and not isinstance(
            self.journey_snapshot, JourneySnapshot
        ):
            raise ReadinessInvariantViolation(
                "journey_snapshot must be a JourneySnapshot when provided",
                invariant="ReadinessInputs.journey_snapshot.type",
            )
        if self.home_snapshot is not None and not isinstance(
            self.home_snapshot, HomeSnapshot
        ):
            raise ReadinessInvariantViolation(
                "home_snapshot must be a HomeSnapshot when provided",
                invariant="ReadinessInputs.home_snapshot.type",
            )
        if self.exam_target is not None and not isinstance(
            self.exam_target, ExamTarget
        ):
            raise ReadinessInvariantViolation(
                "exam_target must be an ExamTarget when provided",
                invariant="ReadinessInputs.exam_target.type",
            )
        if self.exam_target is None and self.schedule is not None:
            object.__setattr__(self, "exam_target", self.schedule.exam_target)

    @staticmethod
    def _normalise_executions(
        values: Sequence[MissionExecution] | tuple[MissionExecution, ...],
    ) -> tuple[MissionExecution, ...]:
        items = tuple(values or ())
        for item in items:
            if not isinstance(item, MissionExecution):
                raise ReadinessInvariantViolation(
                    "execution_history must contain MissionExecution values",
                    invariant="ReadinessInputs.execution_history.type",
                )
        return items
