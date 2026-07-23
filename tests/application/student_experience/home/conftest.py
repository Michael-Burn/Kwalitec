"""Shared factories for Student Home Experience tests."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta

import pytest

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecution,
)
from application.education.mission_generation import (
    Mission,
    MissionEstimate,
    MissionId,
    MissionObjective,
    MissionObjectiveCode,
    MissionOrdering,
    MissionPlan,
    MissionPlanId,
    MissionStep,
    MissionStepAction,
    MissionStepId,
    MissionType,
)
from application.education.orchestration import (
    EducationalDecision,
    EducationalEvaluation,
    EvaluationSummary,
)
from application.education.revision_planner import (
    ExamTarget,
    ExecutionHistory,
    ScheduleId,
)
from application.education.revision_planner.enums import DayKind, SessionStatus
from application.education.revision_planner.ids import DayId, SessionId
from application.education.revision_planner.models.study_day import StudyDay
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.education.revision_planner.models.study_session import StudySession
from application.student_experience.home import (
    AchievementProvider,
    HomeAchievement,
    HomeInputs,
    HomeNotification,
    HomePublisher,
    HomeSnapshot,
    HomeViewModel,
    NotificationProvider,
    StudentHomeService,
)
from domain.education.mastery_estimation import AssessmentId
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    LearningStabilityBand,
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
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
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
    CompetencyId,
    Recommendation,
    RecommendationCategory,
    RecommendationConfidence,
    RecommendationExplanation,
    RecommendationId,
    RecommendationImpact,
    RecommendationOrdering,
    RecommendationPriority,
    RecommendationReason,
    RecommendationReasonCode,
    RecommendationSet,
    RecommendationSetId,
    RecommendationTarget,
    SubjectId,
)

STUDENT_ID = "student-001"
SUBJECT_PROBABILITY = "conditional-probability"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_BAYES = "bayes-theorem"
COMPETENCY_LINEAR = "linear-equations"
AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)
TODAY = date(2026, 7, 23)


@pytest.fixture
def as_of() -> datetime:
    return AS_OF


@pytest.fixture
def service() -> StudentHomeService:
    return StudentHomeService()


def make_mission(
    mission_id: str = "mission-001",
    *,
    mission_type: MissionType = MissionType.PRACTICE_QUESTIONS,
    duration_minutes: int = 30,
    priority: float = 0.80,
    rank: int = 1,
    subject: str | None = SUBJECT_PROBABILITY,
    competency: str | None = COMPETENCY_BAYES,
    objective_code: MissionObjectiveCode = MissionObjectiveCode.COMPLETE_PRACTICE,
) -> Mission:
    return Mission(
        mission_id=MissionId(mission_id),
        mission_type=mission_type,
        objective=MissionObjective(
            code=objective_code,
            subject_id=subject,
            competency_id=competency,
        ),
        estimate=MissionEstimate(duration_minutes=duration_minutes),
        ordering=MissionOrdering(rank=rank, priority_magnitude=priority),
        steps=(
            MissionStep(
                step_id=MissionStepId(f"{mission_id}:s1"),
                action=MissionStepAction.PRACTICE,
                order=1,
                estimated_minutes=duration_minutes,
                subject_id=subject,
                competency_id=competency,
            ),
        ),
        subject_id=subject,
        competency_id=competency,
    )


def make_plan(
    missions: tuple[Mission, ...] | list[Mission] | None = None,
    *,
    plan_id: str = "plan-001",
    student_id: str = STUDENT_ID,
) -> MissionPlan:
    if missions is None:
        missions = (make_mission(),)
    return MissionPlan(
        plan_id=MissionPlanId(plan_id),
        student_id=student_id,
        source_recommendation_set_id="recset-001",
        generated_at=AS_OF,
        missions=tuple(missions),
    )


def make_session(
    *,
    session_id: str = "session-001",
    session_date: date = TODAY,
    mission_ids: tuple[str, ...] = ("mission-001",),
    status: SessionStatus = SessionStatus.PLANNED,
    duration: int = 30,
    start: time = time(9, 0),
    end: time = time(9, 30),
    sequence_index: int = 1,
) -> StudySession:
    return StudySession(
        session_id=SessionId(session_id),
        session_date=session_date,
        start_time=start,
        end_time=end,
        estimated_duration_minutes=duration,
        scheduled_mission_ids=tuple(MissionId(mid) for mid in mission_ids),
        status=status,
        sequence_index=sequence_index,
    )


def make_schedule(
    *,
    sessions: tuple[StudySession, ...] | None = None,
    exam_target: ExamTarget | None = None,
    plan_id: str = "plan-001",
) -> StudySchedule:
    if sessions is None:
        sessions = (make_session(),)
    # Contiguous sequence_index across active sessions (schedule invariant).
    normalised: list[StudySession] = []
    sequence = 1
    for session in sessions:
        normalised.append(
            StudySession(
                session_id=session.session_id,
                session_date=session.session_date,
                start_time=session.start_time,
                end_time=session.end_time,
                estimated_duration_minutes=session.estimated_duration_minutes,
                scheduled_mission_ids=session.scheduled_mission_ids,
                objectives=session.objectives,
                priority=session.priority,
                status=session.status,
                completion_metrics=session.completion_metrics,
                sequence_index=sequence,
            )
        )
        if session.status not in (SessionStatus.CANCELLED, SessionStatus.RESCHEDULED):
            sequence += 1
    sessions = tuple(normalised)
    days: list[StudyDay] = []
    by_date: dict[date, list[StudySession]] = {}
    for session in sessions:
        by_date.setdefault(session.session_date, []).append(session)
    for day_date, day_sessions in sorted(by_date.items()):
        days.append(
            StudyDay(
                day_id=DayId(f"day-{day_date.isoformat()}"),
                day_date=day_date,
                sessions=tuple(day_sessions),
                available_minutes=120,
                kind=DayKind.STUDY,
            )
        )
    start = min(session.session_date for session in sessions)
    end = max(session.session_date for session in sessions)
    return StudySchedule(
        schedule_id=ScheduleId("sched-001"),
        student_id=STUDENT_ID,
        source_plan_id=MissionPlanId(plan_id),
        generated_at=AS_OF,
        start_date=start,
        end_date=end,
        days=tuple(days),
        sessions=sessions,
        exam_target=exam_target,
    )


def make_exam_target(
    *,
    examination_id: str = "ifoacs1-2026",
    exam_date: date | None = None,
) -> ExamTarget:
    return ExamTarget(
        examination_id=examination_id,
        exam_date=exam_date or (TODAY + timedelta(days=45)),
        subject_id=SUBJECT_PROBABILITY,
    )


def make_execution(
    plan: MissionPlan,
    *,
    mission_id: str = "mission-001",
    status: ExecutionStatus = ExecutionStatus.PLANNED,
    elapsed_seconds: float = 0.0,
) -> MissionExecution:
    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId("exec-001"),
        mission_plan=plan,
        mission_id=MissionId(mission_id),
    )
    if status is ExecutionStatus.PLANNED and elapsed_seconds == 0.0:
        return execution
    return execution.with_updates(
        status=status,
        started_at=AS_OF,
        last_active_at=AS_OF,
        elapsed_study_time_seconds=elapsed_seconds,
    )


def make_history(
    *,
    completed: tuple[str, ...] = (),
    abandoned: tuple[str, ...] = (),
    in_progress: tuple[str, ...] = (),
) -> ExecutionHistory:
    return ExecutionHistory(
        completed_mission_ids=tuple(MissionId(mid) for mid in completed),
        abandoned_mission_ids=tuple(MissionId(mid) for mid in abandoned),
        in_progress_mission_ids=tuple(MissionId(mid) for mid in in_progress),
    )


def make_mastery_confidence(
    *,
    magnitude: float = 0.7,
    evidence_count: int = 4,
) -> MasteryConfidence:
    return MasteryConfidence(
        score=ConfidenceScore(magnitude=magnitude),
        evidence_count=evidence_count,
        contradiction_ratio=0.0,
        recency_factor=0.8,
    )


def make_stability(
    *,
    band: LearningStabilityBand = LearningStabilityBand.STABLE,
) -> LearningStability:
    if band is LearningStabilityBand.INSUFFICIENT_DATA:
        return LearningStability.insufficient_data()
    if band is LearningStabilityBand.VOLATILE:
        return LearningStability(magnitude=0.2, evidence_count=4, variance=0.8)
    if band is LearningStabilityBand.MODERATE:
        return LearningStability(magnitude=0.6, evidence_count=4, variance=0.4)
    return LearningStability(magnitude=0.9, evidence_count=4, variance=0.1)


def make_competency(
    *,
    competency_id: str = COMPETENCY_BAYES,
    subject_id: str = SUBJECT_PROBABILITY,
    mastery: float = 0.72,
    evidence_count: int = 4,
    gaps: tuple[KnowledgeGap, ...] = (),
) -> CompetencyAssessment:
    return CompetencyAssessment(
        competency_id=MasteryCompetencyId(competency_id),
        subject_id=MasterySubjectId(subject_id),
        mastery=MasteryScore(magnitude=mastery, evidence_count=evidence_count),
        confidence=make_mastery_confidence(),
        stability=make_stability(),
        gaps=gaps,
    )


def make_gap(
    *,
    competency_id: str = COMPETENCY_LINEAR,
    severity: KnowledgeGapSeverity = KnowledgeGapSeverity.MODERATE,
    mastery: float = 0.25,
) -> KnowledgeGap:
    return KnowledgeGap(
        competency_id=MasteryCompetencyId(competency_id),
        kind=KnowledgeGapKind.WEAK_EVIDENCE,
        severity=severity,
        mastery_score=MasteryScore(magnitude=mastery, evidence_count=3),
    )


def make_assessment(
    *,
    subjects: tuple[tuple[str, float], ...] = (
        (SUBJECT_PROBABILITY, 0.72),
        (SUBJECT_ALGEBRA, 0.45),
    ),
    gaps: tuple[KnowledgeGap, ...] | None = None,
    overall_mastery: float = 0.72,
) -> MasteryAssessment:
    subject_assessments: list[SubjectAssessment] = []
    for subject_id, magnitude in subjects:
        competency_id = f"{subject_id}-core"
        competency = make_competency(
            competency_id=competency_id,
            subject_id=subject_id,
            mastery=magnitude,
        )
        subject_assessments.append(
            SubjectAssessment(
                subject_id=MasterySubjectId(subject_id),
                mastery=MasteryScore(magnitude=magnitude, evidence_count=4),
                confidence=make_mastery_confidence(),
                stability=make_stability(),
                competency_assessments=(competency,),
            )
        )
    if gaps is None:
        weakest_subject = min(subjects, key=lambda item: item[1])[0]
        gaps = (
            make_gap(competency_id=f"{weakest_subject}-core", mastery=0.25),
        )
    primary = subject_assessments[0]
    return MasteryAssessment(
        assessment_id=AssessmentId("assessment-001"),
        student_id=STUDENT_ID,
        assessed_at=AS_OF,
        overall_mastery=MasteryScore(
            magnitude=overall_mastery, evidence_count=4
        ),
        overall_confidence=primary.confidence,
        overall_stability=primary.stability,
        subject_assessments=tuple(subject_assessments),
        knowledge_gaps=tuple(gaps),
        supporting_evidence=(),
        reasons=(),
    )


def make_recommendation(
    *,
    recommendation_id: str = "r1",
    category: RecommendationCategory = RecommendationCategory.FOCUS_COMPETENCY,
    rank: int = 1,
    subject: str = SUBJECT_PROBABILITY,
    competency: str | None = COMPETENCY_BAYES,
) -> Recommendation:
    priority = RecommendationPriority(0.85)
    target_kwargs: dict = {"subject_id": SubjectId(subject)}
    if competency is not None:
        target_kwargs["competency_id"] = CompetencyId(competency)
    return Recommendation(
        recommendation_id=RecommendationId(recommendation_id),
        category=category,
        target=RecommendationTarget(**target_kwargs),
        priority=priority,
        impact=RecommendationImpact(0.80),
        confidence=RecommendationConfidence(0.70),
        explanation=RecommendationExplanation.from_reasons(
            (
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=SubjectId(subject),
                    competency_id=(
                        CompetencyId(competency) if competency is not None else None
                    ),
                ),
            )
        ),
        ordering=RecommendationOrdering(rank=rank, priority=priority),
    )


def make_recommendation_set(
    recommendations: tuple[Recommendation, ...] | None = None,
) -> RecommendationSet:
    items = recommendations or (make_recommendation(),)
    return RecommendationSet(
        RecommendationSetId("recset-001"),
        STUDENT_ID,
        AS_OF,
        recommendations=items,
    )


def make_evaluation(
    *,
    mastery_magnitude: float = 0.72,
    knowledge_gap_count: int = 1,
    decisions: tuple[EducationalDecision, ...] | None = None,
) -> EducationalEvaluation:
    from application.education.orchestration import EvaluationSnapshot

    if decisions is None:
        decisions = (
            EducationalDecision(
                decision_id="d1",
                category="focus_competency",
                subject_id=SUBJECT_PROBABILITY,
                competency_id=COMPETENCY_BAYES,
                priority_band="high",
                impact_band="high",
                confidence_magnitude=0.7,
                reason_summary="direct_knowledge_gap",
                rank=1,
            ),
        )
    summary = EvaluationSummary(
        student_id=STUDENT_ID,
        assessment_id="assessment-001",
        recommendation_set_id="recset-001",
        mastery_magnitude=mastery_magnitude,
        mastery_band="secure",
        confidence_magnitude=0.7,
        stability_band="stable",
        knowledge_gap_count=knowledge_gap_count,
        recommendation_count=len(decisions),
        evidence_count=4,
        evaluated_at=AS_OF,
        top_decision_category=decisions[0].category if decisions else None,
    )
    snapshot = EvaluationSnapshot(
        student_id=STUDENT_ID,
        evaluated_at=AS_OF,
        stages_completed=("compose_result",),
        summary=summary,
        decisions=decisions,
    )
    return EducationalEvaluation.succeeded(
        student_id=STUDENT_ID,
        stages_completed=("compose_result",),
        summary=summary,
        snapshot=snapshot,
        decisions=decisions,
    )


def make_full_inputs(**overrides) -> HomeInputs:
    plan = overrides.pop("mission_plan", None) or make_plan()
    if "schedule" in overrides:
        schedule = overrides.pop("schedule")
    else:
        schedule = make_schedule(exam_target=make_exam_target())
    base = dict(
        student_id=STUDENT_ID,
        as_of=AS_OF,
        evaluation=make_evaluation(),
        assessment=make_assessment(),
        recommendation_set=make_recommendation_set(),
        mission_plan=plan,
        schedule=schedule,
        current_execution=None,
        execution_history=make_history(),
        exam_target=make_exam_target(),
    )
    base.update(overrides)
    return HomeInputs(**base)


class RecordingPublisher(HomePublisher):
    def __init__(self) -> None:
        self.homes: list[HomeViewModel] = []
        self.snapshots: list[HomeSnapshot] = []

    def publish_home(self, home: HomeViewModel) -> None:
        self.homes.append(home)

    def publish_snapshot(self, snapshot: HomeSnapshot) -> None:
        self.snapshots.append(snapshot)


class FakeAchievementProvider(AchievementProvider):
    def __init__(self, items: tuple[HomeAchievement, ...] = ()) -> None:
        self._items = items

    def list_achievements(
        self, student_id: str, *, limit: int = 3
    ) -> tuple[HomeAchievement, ...]:
        return self._items[:limit]


class FakeNotificationProvider(NotificationProvider):
    def __init__(self, items: tuple[HomeNotification, ...] = ()) -> None:
        self._items = items

    def list_notifications(
        self, student_id: str, *, limit: int = 5
    ) -> tuple[HomeNotification, ...]:
        return self._items[:limit]
