"""Shared factories for Learning Journey Experience (XP-002) tests."""

from __future__ import annotations

from datetime import datetime, time, timedelta

import pytest

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecution,
)
from application.education.mission_generation import (
    MissionId,
    MissionPlan,
    MissionType,
)
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.home import (
    HomeSnapshot,
    StudentHomeService,
)
from application.student_experience.home.ids import SnapshotId as HomeSnapshotId
from application.student_experience.progress import (
    JourneyExportProvider,
    JourneyInputs,
    JourneyPublisher,
    JourneySnapshot,
    LearningJourneyService,
    LearningJourneyViewModel,
    MilestoneProvider,
    ProvidedMilestone,
    StudyStatistics,
)
from domain.education.mastery_estimation import AssessmentId
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.ids import (
    CompetencyId as MasteryCompetencyId,
)
from domain.education.mastery_estimation.ids import (
    SubjectId as MasterySubjectId,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)
from domain.education.recommendation_engine import (
    RecommendationSet,
    RecommendationSetId,
)
from tests.application.student_experience.home.conftest import (
    AS_OF,
    COMPETENCY_BAYES,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    SUBJECT_PROBABILITY,
    TODAY,
    make_evaluation,
    make_exam_target,
    make_mission,
    make_plan,
    make_recommendation,
    make_schedule,
    make_session,
)
from tests.application.student_experience.home.conftest import (
    make_full_inputs as make_home_inputs,
)

__all__ = [
    "AS_OF",
    "COMPETENCY_BAYES",
    "STUDENT_ID",
    "SUBJECT_ALGEBRA",
    "SUBJECT_PROBABILITY",
    "TODAY",
]


@pytest.fixture
def as_of() -> datetime:
    return AS_OF


@pytest.fixture
def service() -> LearningJourneyService:
    return LearningJourneyService()


def make_completed_execution(
    plan: MissionPlan,
    *,
    execution_id: str = "exec-001",
    mission_id: str = "mission-001",
    finished_at: datetime | None = None,
    started_at: datetime | None = None,
    elapsed_seconds: float = 1800.0,
    mission_type: MissionType | None = None,
) -> MissionExecution:
    if mission_type is not None:
        mission = make_mission(mission_id, mission_type=mission_type)
        plan = make_plan((mission,), plan_id=plan.plan_id.value)
    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId(execution_id),
        mission_plan=plan,
        mission_id=MissionId(mission_id),
    )
    started = started_at or (finished_at or AS_OF) - timedelta(minutes=30)
    finished = finished_at or AS_OF
    completed_steps = tuple(step.step_id for step in execution.mission.steps)
    return execution.with_updates(
        status=ExecutionStatus.COMPLETED,
        started_at=started,
        finished_at=finished,
        last_active_at=finished,
        elapsed_study_time_seconds=elapsed_seconds,
        completed_step_ids=completed_steps,
        current_step_id=None,
    )


def make_abandoned_execution(
    plan: MissionPlan,
    *,
    execution_id: str = "exec-abandoned",
    mission_id: str = "mission-abandoned",
    finished_at: datetime | None = None,
) -> MissionExecution:
    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId(execution_id),
        mission_plan=plan,
        mission_id=MissionId(mission_id),
    )
    finished = finished_at or AS_OF
    return execution.with_updates(
        status=ExecutionStatus.ABANDONED,
        started_at=finished - timedelta(minutes=10),
        finished_at=finished,
        last_active_at=finished,
        elapsed_study_time_seconds=300.0,
    )


def make_assessment_at(
    assessed_at: datetime,
    *,
    assessment_id: str = "assessment-001",
    overall_mastery: float = 0.72,
    confidence: float = 0.70,
    subjects: tuple[tuple[str, float], ...] = (
        (SUBJECT_PROBABILITY, 0.72),
        (SUBJECT_ALGEBRA, 0.45),
    ),
    competencies: tuple[tuple[str, str, float], ...] | None = None,
) -> MasteryAssessment:
    subject_assessments: list[SubjectAssessment] = []
    competency_by_subject: dict[str, list[CompetencyAssessment]] = {}
    if competencies is None:
        for subject_id, magnitude in subjects:
            competency_by_subject[subject_id] = [
                CompetencyAssessment(
                    competency_id=MasteryCompetencyId(f"{subject_id}-core"),
                    subject_id=MasterySubjectId(subject_id),
                    mastery=MasteryScore(magnitude=magnitude, evidence_count=4),
                    confidence=MasteryConfidence(
                        score=ConfidenceScore(magnitude=confidence),
                        evidence_count=4,
                        contradiction_ratio=0.0,
                        recency_factor=0.8,
                    ),
                    stability=LearningStability(
                        magnitude=0.9, evidence_count=4, variance=0.1
                    ),
                )
            ]
    else:
        for competency_id, subject_id, magnitude in competencies:
            competency_by_subject.setdefault(subject_id, []).append(
                CompetencyAssessment(
                    competency_id=MasteryCompetencyId(competency_id),
                    subject_id=MasterySubjectId(subject_id),
                    mastery=MasteryScore(magnitude=magnitude, evidence_count=4),
                    confidence=MasteryConfidence(
                        score=ConfidenceScore(magnitude=confidence),
                        evidence_count=4,
                        contradiction_ratio=0.0,
                        recency_factor=0.8,
                    ),
                    stability=LearningStability(
                        magnitude=0.9, evidence_count=4, variance=0.1
                    ),
                )
            )
        subjects = tuple(
            (
                subject_id,
                max(item.mastery.magnitude for item in comps),
            )
            for subject_id, comps in competency_by_subject.items()
        )
    for subject_id, magnitude in subjects:
        comps = tuple(competency_by_subject.get(subject_id, ()))
        subject_assessments.append(
            SubjectAssessment(
                subject_id=MasterySubjectId(subject_id),
                mastery=MasteryScore(magnitude=magnitude, evidence_count=4),
                confidence=MasteryConfidence(
                    score=ConfidenceScore(magnitude=confidence),
                    evidence_count=4,
                    contradiction_ratio=0.0,
                    recency_factor=0.8,
                ),
                stability=LearningStability(
                    magnitude=0.9, evidence_count=4, variance=0.1
                ),
                competency_assessments=comps,
            )
        )
    primary = subject_assessments[0]
    return MasteryAssessment(
        assessment_id=AssessmentId(assessment_id),
        student_id=STUDENT_ID,
        assessed_at=assessed_at,
        overall_mastery=MasteryScore(
            magnitude=overall_mastery, evidence_count=4
        ),
        overall_confidence=primary.confidence,
        overall_stability=primary.stability,
        subject_assessments=tuple(subject_assessments),
        knowledge_gaps=(),
        supporting_evidence=(),
        reasons=(),
    )


def make_recommendation_set_at(
    recommended_at: datetime,
    *,
    set_id: str = "recset-001",
    competency: str | None = COMPETENCY_BAYES,
) -> RecommendationSet:
    return RecommendationSet(
        RecommendationSetId(set_id),
        STUDENT_ID,
        recommended_at,
        recommendations=(
            make_recommendation(
                recommendation_id=f"r-{set_id}",
                competency=competency,
            ),
        ),
    )


def make_home_snapshot() -> HomeSnapshot:
    home_service = StudentHomeService()
    home = home_service.build_home(make_home_inputs(), home_id="home-for-journey")
    return home_service.build_snapshot(home, snapshot_id=HomeSnapshotId("hsnap-001"))


def make_study_statistics(
    *,
    completed: int = 6,
    abandoned: int = 1,
    sessions: int = 8,
    minutes: float = 240.0,
    avg_minutes: float = 30.0,
    study_days: int = 5,
) -> StudyStatistics:
    return StudyStatistics(
        total_study_minutes=minutes,
        total_sessions=sessions,
        completed_missions=completed,
        abandoned_missions=abandoned,
        average_session_minutes=avg_minutes,
        study_day_count=study_days,
    )


def make_rich_inputs(**overrides) -> JourneyInputs:
    plan = make_plan(
        (
            make_mission("mission-001"),
            make_mission(
                "mission-002",
                mission_type=MissionType.REVISION_SESSION,
                rank=2,
            ),
            make_mission(
                "mission-003",
                mission_type=MissionType.CHECKPOINT_PREPARATION,
                rank=3,
            ),
        )
    )
    day_1 = AS_OF - timedelta(days=5)
    day_2 = AS_OF - timedelta(days=3)
    day_3 = AS_OF - timedelta(days=1)
    executions = (
        make_completed_execution(
            plan,
            execution_id="exec-001",
            mission_id="mission-001",
            finished_at=day_1,
            started_at=day_1.replace(hour=9),
        ),
        make_completed_execution(
            make_plan(
                (
                    make_mission(
                        "mission-002",
                        mission_type=MissionType.REVISION_SESSION,
                    ),
                ),
                plan_id="plan-002",
            ),
            execution_id="exec-002",
            mission_id="mission-002",
            finished_at=day_2,
            started_at=day_2.replace(hour=18),
            mission_type=MissionType.REVISION_SESSION,
        ),
        make_completed_execution(
            make_plan(
                (
                    make_mission(
                        "mission-003",
                        mission_type=MissionType.CHECKPOINT_PREPARATION,
                    ),
                ),
                plan_id="plan-003",
            ),
            execution_id="exec-003",
            mission_id="mission-003",
            finished_at=day_3,
            started_at=day_3.replace(hour=10),
            mission_type=MissionType.CHECKPOINT_PREPARATION,
        ),
        make_abandoned_execution(
            make_plan((make_mission("mission-abandoned"),), plan_id="plan-abd"),
            finished_at=AS_OF - timedelta(days=4),
        ),
    )
    schedule = make_schedule(
        sessions=(
            make_session(
                session_id="session-past-1",
                session_date=TODAY - timedelta(days=5),
                mission_ids=("mission-001",),
                status=SessionStatus.COMPLETED,
                start=time(9, 0),
                end=time(9, 30),
            ),
            make_session(
                session_id="session-past-2",
                session_date=TODAY - timedelta(days=3),
                mission_ids=("mission-002",),
                status=SessionStatus.COMPLETED,
                start=time(18, 0),
                end=time(18, 30),
            ),
            make_session(
                session_id="session-today",
                session_date=TODAY,
                mission_ids=("mission-004",),
                status=SessionStatus.PLANNED,
                start=time(9, 0),
                end=time(9, 30),
            ),
        ),
        exam_target=make_exam_target(),
    )
    early = make_assessment_at(
        AS_OF - timedelta(days=20),
        assessment_id="assessment-early",
        overall_mastery=0.40,
        confidence=0.40,
        competencies=(
            ("bayes-theorem", SUBJECT_PROBABILITY, 0.40),
            ("algebra-core", SUBJECT_ALGEBRA, 0.30),
        ),
    )
    mid = make_assessment_at(
        AS_OF - timedelta(days=7),
        assessment_id="assessment-mid",
        overall_mastery=0.60,
        confidence=0.55,
        competencies=(
            ("bayes-theorem", SUBJECT_PROBABILITY, 0.65),
            ("algebra-core", SUBJECT_ALGEBRA, 0.40),
        ),
    )
    latest = make_assessment_at(
        AS_OF - timedelta(days=1),
        assessment_id="assessment-latest",
        overall_mastery=0.80,
        confidence=0.75,
        competencies=(
            ("bayes-theorem", SUBJECT_PROBABILITY, 0.90),
            ("algebra-core", SUBJECT_ALGEBRA, 0.50),
        ),
    )
    # Force a mastered competency for milestone projection.
    mastered = make_assessment_at(
        AS_OF,
        assessment_id="assessment-mastered",
        overall_mastery=0.90,
        confidence=0.85,
        competencies=(
            ("bayes-theorem", SUBJECT_PROBABILITY, 0.95),
            ("algebra-core", SUBJECT_ALGEBRA, 0.55),
        ),
        subjects=((SUBJECT_PROBABILITY, 0.95), (SUBJECT_ALGEBRA, 0.55)),
    )
    recommendations = (
        make_recommendation_set_at(
            AS_OF - timedelta(days=10),
            set_id="recset-early",
            competency="linear-equations",
        ),
        make_recommendation_set_at(
            AS_OF - timedelta(days=2),
            set_id="recset-late",
            competency=COMPETENCY_BAYES,
        ),
    )
    evaluations = (
        make_evaluation(),
    )
    base = dict(
        student_id=STUDENT_ID,
        as_of=AS_OF,
        evaluation_history=evaluations,
        execution_history=executions,
        schedule_history=(schedule,),
        assessment_history=(early, mid, latest, mastered),
        recommendation_history=recommendations,
        study_statistics=make_study_statistics(),
        home_snapshot=make_home_snapshot(),
    )
    base.update(overrides)
    return JourneyInputs(**base)


def make_empty_inputs(**overrides) -> JourneyInputs:
    base = dict(student_id=STUDENT_ID, as_of=AS_OF)
    base.update(overrides)
    return JourneyInputs(**base)


class RecordingJourneyPublisher(JourneyPublisher):
    def __init__(self) -> None:
        self.journeys: list[LearningJourneyViewModel] = []
        self.snapshots: list[JourneySnapshot] = []

    def publish_journey(self, journey: LearningJourneyViewModel) -> None:
        self.journeys.append(journey)

    def publish_snapshot(self, snapshot: JourneySnapshot) -> None:
        self.snapshots.append(snapshot)


class FakeMilestoneProvider(MilestoneProvider):
    def __init__(self, items: tuple[ProvidedMilestone, ...] = ()) -> None:
        self._items = items

    def list_milestones(
        self, student_id: str, *, limit: int = 10
    ) -> tuple[ProvidedMilestone, ...]:
        return self._items[:limit]


class FakeExportProvider(JourneyExportProvider):
    def export_journey(self, journey: LearningJourneyViewModel) -> str:
        return f"export:{journey.journey_id.value}"

    def export_snapshot(self, snapshot: JourneySnapshot) -> str:
        return f"export:{snapshot.snapshot_id.value}"
