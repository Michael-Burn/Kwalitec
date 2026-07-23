"""JourneyInputs — caller-supplied Education OS histories for journey composition."""

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
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.progress.errors import JourneyInvariantViolation
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)


@dataclass(frozen=True, slots=True)
class StudyStatistics:
    """Caller-supplied study statistics for journey composition.

    Optional overlay. When omitted, the composer projects equivalent
    scalars from execution and schedule history. Never estimates mastery.
    """

    total_study_minutes: float = 0.0
    total_sessions: int = 0
    completed_missions: int = 0
    abandoned_missions: int = 0
    average_session_minutes: float = 0.0
    study_day_count: int = 0

    def __post_init__(self) -> None:
        for name in (
            "total_study_minutes",
            "average_session_minutes",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise JourneyInvariantViolation(
                    f"{name} must be a real number",
                    invariant=f"StudyStatistics.{name}.type",
                )
            if float(value) < 0.0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"StudyStatistics.{name}.range",
                )
            object.__setattr__(self, name, round(float(value), 2))
        for name in (
            "total_sessions",
            "completed_missions",
            "abandoned_missions",
            "study_day_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"StudyStatistics.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"StudyStatistics.{name}.range",
                )


@dataclass(frozen=True, slots=True)
class JourneyInputs:
    """Immutable bundle of Education OS histories for Learning Journey composition.

    All educational histories are optional so the journey surface degrades
    gracefully. ``student_id`` and ``as_of`` are always required for
    deterministic composition. ``as_of`` is caller-supplied — never wall clock.
    """

    student_id: str
    as_of: datetime
    evaluation_history: tuple[EducationalEvaluation, ...] = ()
    execution_history: tuple[MissionExecution, ...] = ()
    schedule_history: tuple[StudySchedule, ...] = ()
    assessment_history: tuple[MasteryAssessment, ...] = ()
    recommendation_history: tuple[RecommendationSet, ...] = ()
    study_statistics: StudyStatistics | None = None
    home_snapshot: HomeSnapshot | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise JourneyInvariantViolation(
                "student_id must be a non-empty string",
                invariant="JourneyInputs.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.as_of, datetime):
            raise JourneyInvariantViolation(
                "as_of must be a datetime",
                invariant="JourneyInputs.as_of.type",
            )
        object.__setattr__(
            self,
            "evaluation_history",
            self._normalise_sequence(
                self.evaluation_history,
                EducationalEvaluation,
                "evaluation_history",
            ),
        )
        object.__setattr__(
            self,
            "execution_history",
            self._normalise_sequence(
                self.execution_history,
                MissionExecution,
                "execution_history",
            ),
        )
        object.__setattr__(
            self,
            "schedule_history",
            self._normalise_sequence(
                self.schedule_history,
                StudySchedule,
                "schedule_history",
            ),
        )
        object.__setattr__(
            self,
            "assessment_history",
            self._normalise_assessments(self.assessment_history),
        )
        object.__setattr__(
            self,
            "recommendation_history",
            self._normalise_recommendations(self.recommendation_history),
        )
        if self.study_statistics is not None and not isinstance(
            self.study_statistics, StudyStatistics
        ):
            raise JourneyInvariantViolation(
                "study_statistics must be a StudyStatistics when provided",
                invariant="JourneyInputs.study_statistics.type",
            )
        if self.home_snapshot is not None and not isinstance(
            self.home_snapshot, HomeSnapshot
        ):
            raise JourneyInvariantViolation(
                "home_snapshot must be a HomeSnapshot when provided",
                invariant="JourneyInputs.home_snapshot.type",
            )

    @staticmethod
    def _normalise_sequence(
        values: Sequence[object] | tuple[object, ...],
        expected_type: type,
        field_name: str,
    ) -> tuple:
        items = tuple(values or ())
        for item in items:
            if not isinstance(item, expected_type):
                raise JourneyInvariantViolation(
                    f"{field_name} must contain {expected_type.__name__} values",
                    invariant=f"JourneyInputs.{field_name}.type",
                )
        return items

    @staticmethod
    def _normalise_assessments(
        values: Sequence[MasteryAssessment] | tuple[MasteryAssessment, ...],
    ) -> tuple[MasteryAssessment, ...]:
        items = tuple(values or ())
        for item in items:
            if not isinstance(item, MasteryAssessment):
                raise JourneyInvariantViolation(
                    "assessment_history must contain MasteryAssessment values",
                    invariant="JourneyInputs.assessment_history.type",
                )
        return items

    @staticmethod
    def _normalise_recommendations(
        values: Sequence[RecommendationSet] | tuple[RecommendationSet, ...],
    ) -> tuple[RecommendationSet, ...]:
        items = tuple(values or ())
        for item in items:
            if not isinstance(item, RecommendationSet):
                raise JourneyInvariantViolation(
                    "recommendation_history must contain RecommendationSet values",
                    invariant="JourneyInputs.recommendation_history.type",
                )
        return items
