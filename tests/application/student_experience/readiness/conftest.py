"""Shared factories for Exam Readiness Experience (XP-003) tests."""

from __future__ import annotations

from datetime import time, timedelta

import pytest

from application.education.revision_planner.enums import SessionStatus
from application.student_experience.home import StudentHomeService
from application.student_experience.home.ids import SnapshotId as HomeSnapshotId
from application.student_experience.progress import (
    JourneySnapshot,
    LearningJourneyService,
    TrajectoryLabel,
    TrendDirection,
)
from application.student_experience.progress.ids import JourneySnapshotId
from application.student_experience.readiness import (
    ExamReadinessService,
    ExamReadinessViewModel,
    ReadinessExportProvider,
    ReadinessInputs,
    ReadinessPublisher,
    ReadinessSnapshot,
)
from domain.education.knowledge_graph.enums import DependencyStrengthBand
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
)
from domain.education.mastery_estimation.ids import (
    CompetencyId as MasteryCompetencyId,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.student_experience.home.conftest import (
    AS_OF,
    COMPETENCY_BAYES,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    SUBJECT_PROBABILITY,
    TODAY,
    make_assessment,
    make_evaluation,
    make_exam_target,
    make_gap,
    make_mission,
    make_plan,
    make_recommendation,
    make_recommendation_set,
    make_schedule,
    make_session,
)
from tests.application.student_experience.home.conftest import (
    make_full_inputs as make_home_inputs,
)
from tests.application.student_experience.progress.conftest import (
    make_abandoned_execution,
    make_completed_execution,
)
from tests.application.student_experience.progress.conftest import (
    make_rich_inputs as make_journey_inputs,
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
def as_of():
    return AS_OF


@pytest.fixture
def service() -> ExamReadinessService:
    return ExamReadinessService()


def make_prerequisite_gap(
    *,
    competency_id: str = "algebra-core",
    related: str = "conditional-probability-core",
) -> KnowledgeGap:
    return KnowledgeGap(
        competency_id=MasteryCompetencyId(competency_id),
        kind=KnowledgeGapKind.WEAK_PREREQUISITE,
        severity=KnowledgeGapSeverity.MODERATE,
        mastery_score=MasteryScore(magnitude=0.20, evidence_count=3),
        related_competency_id=MasteryCompetencyId(related),
        dependency_strength=DependencyStrength(
            band=DependencyStrengthBand.IMPORTANT,
            weight=0.8,
        ),
    )


def make_home_snapshot():
    home_service = StudentHomeService()
    home = home_service.build_home(make_home_inputs(), home_id="home-for-readiness")
    return home_service.build_snapshot(home, snapshot_id=HomeSnapshotId("hsnap-r001"))


def make_journey_snapshot() -> JourneySnapshot:
    journey_service = LearningJourneyService()
    journey = journey_service.build_journey(
        make_journey_inputs(), journey_id="journey-for-readiness"
    )
    return journey_service.build_snapshot(
        journey, snapshot_id=JourneySnapshotId("jsnap-r001")
    )


def make_minimal_journey_snapshot(
    *,
    mastery_trend: TrendDirection = TrendDirection.IMPROVING,
    weekly_missions: int = 3,
) -> JourneySnapshot:
    return JourneySnapshot(
        snapshot_id=JourneySnapshotId("jsnap-min"),
        student_id=STUDENT_ID,
        captured_at=AS_OF,
        trajectory=TrajectoryLabel.BUILDING,
        trajectory_message="You're building a steady study rhythm.",
        timeline_event_count=4,
        milestone_count=2,
        current_streak_days=3,
        longest_streak_days=5,
        weekly_missions_completed=weekly_missions,
        monthly_missions_completed=8,
        mastery_trend=mastery_trend,
        consistency_message="Your study consistency is encouraging.",
        habits_message="You tend to study in the morning.",
    )


def make_full_inputs(**overrides) -> ReadinessInputs:
    plan = make_plan(
        (
            make_mission("mission-001"),
            make_mission("mission-002", rank=2),
        )
    )
    executions = (
        make_completed_execution(
            plan,
            execution_id="exec-001",
            mission_id="mission-001",
            finished_at=AS_OF - timedelta(days=2),
        ),
        make_completed_execution(
            make_plan((make_mission("mission-002", rank=2),), plan_id="plan-002"),
            execution_id="exec-002",
            mission_id="mission-002",
            finished_at=AS_OF - timedelta(days=1),
        ),
        make_abandoned_execution(
            make_plan((make_mission("mission-abd"),), plan_id="plan-abd"),
            mission_id="mission-abd",
            finished_at=AS_OF - timedelta(days=3),
        ),
    )
    schedule = make_schedule(
        sessions=(
            make_session(
                session_id="session-past",
                session_date=TODAY - timedelta(days=2),
                mission_ids=("mission-001",),
                status=SessionStatus.COMPLETED,
            ),
            make_session(
                session_id="session-overdue",
                session_date=TODAY - timedelta(days=1),
                mission_ids=("mission-overdue",),
                status=SessionStatus.PLANNED,
                start=time(10, 0),
                end=time(10, 30),
            ),
            make_session(
                session_id="session-today",
                session_date=TODAY,
                mission_ids=("mission-002",),
                status=SessionStatus.PLANNED,
            ),
        ),
        exam_target=make_exam_target(exam_date=TODAY + timedelta(days=10)),
    )
    recommendations = make_recommendation_set(
        (
            make_recommendation(
                recommendation_id="r1",
                category=RecommendationCategory.FOCUS_COMPETENCY,
                rank=1,
                competency=COMPETENCY_BAYES,
            ),
            make_recommendation(
                recommendation_id="r2",
                category=RecommendationCategory.CONSOLIDATE_KNOWLEDGE,
                rank=2,
                subject=SUBJECT_PROBABILITY,
                competency=COMPETENCY_BAYES,
            ),
            make_recommendation(
                recommendation_id="r3",
                category=RecommendationCategory.STUDY_PREREQUISITE,
                rank=3,
                subject=SUBJECT_ALGEBRA,
                competency="algebra-core",
            ),
        )
    )
    assessment = make_assessment(
        subjects=(
            (SUBJECT_PROBABILITY, 0.82),
            (SUBJECT_ALGEBRA, 0.40),
        ),
        gaps=(
            make_gap(competency_id="algebra-core", mastery=0.25),
            make_prerequisite_gap(
                competency_id="algebra-core",
                related=f"{SUBJECT_PROBABILITY}-core",
            ),
        ),
        overall_mastery=0.72,
    )
    base = dict(
        student_id=STUDENT_ID,
        as_of=AS_OF,
        evaluation=make_evaluation(),
        assessment=assessment,
        recommendation_set=recommendations,
        schedule=schedule,
        execution_history=executions,
        journey_snapshot=make_minimal_journey_snapshot(),
        home_snapshot=make_home_snapshot(),
        exam_target=make_exam_target(exam_date=TODAY + timedelta(days=10)),
    )
    base.update(overrides)
    return ReadinessInputs(**base)


def make_empty_inputs(**overrides) -> ReadinessInputs:
    base = dict(student_id=STUDENT_ID, as_of=AS_OF)
    base.update(overrides)
    return ReadinessInputs(**base)


class RecordingReadinessPublisher(ReadinessPublisher):
    def __init__(self) -> None:
        self.readiness_views: list[ExamReadinessViewModel] = []
        self.snapshots: list[ReadinessSnapshot] = []

    def publish_readiness(self, readiness: ExamReadinessViewModel) -> None:
        self.readiness_views.append(readiness)

    def publish_snapshot(self, snapshot: ReadinessSnapshot) -> None:
        self.snapshots.append(snapshot)


class FakeReadinessExportProvider(ReadinessExportProvider):
    def export_readiness(self, readiness: ExamReadinessViewModel) -> str:
        return f"export:{readiness.readiness_id.value}"

    def export_snapshot(self, snapshot: ReadinessSnapshot) -> str:
        return f"export:{snapshot.snapshot_id.value}"
