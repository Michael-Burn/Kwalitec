"""Projection correctness tests for application read models (WEB-003)."""

from __future__ import annotations

from application.dto.evidence import EvidenceHistoryDTO, EvidenceRecordDTO
from application.dto.learner import LearnerStateDTO
from application.dto.learning import LearningSessionDTO
from application.dto.teaching_plan import TeachingPlanDTO, TeachingPlanStepDTO
from application.dto.trajectory import LearningTrajectoryDTO, TrajectoryPointDTO
from application.read_models import (
    DashboardProjectionBuilder,
    MissionProjectionBuilder,
    ProgressSummaryProjectionBuilder,
    RecommendationProjectionBuilder,
    TimelineProjectionBuilder,
    TodaysMissionProjectionBuilder,
)


def test_recommendation_builder_strips_and_projects() -> None:
    model = RecommendationProjectionBuilder.build(
        title="  Continue studying  ",
        subtitle="  Next step  ",
        primary_action="Start Session",
        reason_summary="Stay on plan",
        estimated_minutes=25,
        can_start=True,
        decision_id="dec-1",
        recommendation_id="rec-1",
    )
    assert model.title == "Continue studying"
    assert model.subtitle == "Next step"
    assert model.can_start is True
    assert model.estimated_minutes == 25


def test_mission_tasks_from_teaching_plan() -> None:
    plan = TeachingPlanDTO(
        plan_id="plan-001",
        episode_id="episode-001",
        student_id="student-ada",
        teaching_goal_statement="Repair confusion",
        teaching_strategy_id="strategy-1",
        primary_dimension="understanding",
        status="planned",
        learning_objective_ids=("lo-1",),
        concept_ids=("concept-1",),
        steps=(
            TeachingPlanStepDTO(
                step_id="step-001",
                kind="explanation",
                sequence_index=0,
                label="Explanation",
                required=True,
                status="pending",
            ),
            TeachingPlanStepDTO(
                step_id="step-002",
                kind="guided_practice",
                sequence_index=1,
                label="Practice",
                required=True,
                status="pending",
            ),
        ),
    )
    tasks = MissionProjectionBuilder.build_tasks(plan)
    assert len(tasks) == 2
    assert tasks[0].task_id == "step-001"
    assert tasks[0].headline == "Explanation"
    assert tasks[1].sequence_index == 1


def test_todays_mission_from_teaching_plan() -> None:
    plan = TeachingPlanDTO(
        plan_id="plan-001",
        episode_id="episode-001",
        student_id="student-ada",
        teaching_goal_statement="Repair confusion",
        teaching_strategy_id="strategy-1",
        primary_dimension="understanding",
        status="planned",
        learning_objective_ids=(),
        concept_ids=(),
        steps=(
            TeachingPlanStepDTO(
                step_id="step-001",
                kind="explanation",
                sequence_index=0,
                label="Explanation",
                required=True,
                status="pending",
            ),
        ),
    )
    mission = TodaysMissionProjectionBuilder.from_teaching_plan(
        plan,
        title="Today's Session",
        estimated_minutes=20,
        mission_id="mission-1",
    )
    assert mission.episode_id == "episode-001"
    assert mission.task_count == 1
    assert mission.can_open is True
    assert mission.summary == "1 task"
    assert mission.tasks[0].headline == "Explanation"


def test_todays_mission_from_learning_session() -> None:
    session = LearningSessionDTO(
        episode_id="episode-001",
        student_id="student-ada",
        status="active",
        first_active_step_id="step-001",
    )
    mission = TodaysMissionProjectionBuilder.from_learning_session(session)
    assert mission.episode_id == "episode-001"
    assert mission.status == "active"
    assert mission.can_open is True
    assert mission.task_count == 0
    assert mission.summary == "No tasks in this session"


def test_progress_summary_from_learner_state() -> None:
    state = LearnerStateDTO(
        twin_id="twin-001",
        student_id="student-ada",
        learner_state_id="ls-001",
        activity_status="engaged",
        twin_status="active",
        concept_count=4,
        evidence_count=7,
        intervention_count=1,
    )
    progress = ProgressSummaryProjectionBuilder.build(state)
    assert progress.student_id == "student-ada"
    assert progress.concept_count == 4
    assert progress.evidence_count == 7
    assert "activity:engaged" in progress.progress_cues
    assert "concepts:4" in progress.progress_cues


def test_timeline_from_trajectory() -> None:
    trajectory = LearningTrajectoryDTO(
        twin_id="twin-001",
        student_id="student-ada",
        points=(
            TrajectoryPointDTO(sequence=0, kind="created", label="Twin created"),
            TrajectoryPointDTO(sequence=1, kind="evidence", label="Evidence added"),
        ),
    )
    timeline = TimelineProjectionBuilder.from_trajectory(trajectory)
    assert timeline.event_count == 2
    assert timeline.events[1].kind == "evidence"
    assert timeline.twin_id == "twin-001"


def test_timeline_from_evidence_history() -> None:
    history = EvidenceHistoryDTO(
        student_id="student-ada",
        records=(
            EvidenceRecordDTO(
                evidence_id="ev-1",
                student_id="student-ada",
                status="recorded",
                strength_level="moderate",
                confidence_level="high",
                item_count=1,
                concept_ids=("c1",),
                learning_episode_ids=("ep-1",),
                occurred_at="2026-07-20T09:00:00+00:00",
            ),
        ),
    )
    timeline = TimelineProjectionBuilder.from_evidence_history(history)
    assert timeline.event_count == 1
    assert timeline.events[0].kind == "evidence"
    assert timeline.events[0].occurred_at == "2026-07-20T09:00:00+00:00"
    assert "moderate" in timeline.events[0].label


def test_dashboard_composes_sections_without_duplicating_logic() -> None:
    state = LearnerStateDTO(
        twin_id="twin-001",
        student_id="student-ada",
        learner_state_id="ls-001",
        activity_status="engaged",
        twin_status="active",
        concept_count=2,
        evidence_count=1,
        intervention_count=0,
    )
    trajectory = LearningTrajectoryDTO(
        twin_id="twin-001",
        student_id="student-ada",
        points=(TrajectoryPointDTO(sequence=0, kind="created", label="Twin created"),),
    )
    recommendation = RecommendationProjectionBuilder.build(
        title="Continue studying",
        can_start=True,
        primary_action="Start Session",
    )
    progress = ProgressSummaryProjectionBuilder.build(state)
    timeline = TimelineProjectionBuilder.from_trajectory(trajectory)
    dashboard = DashboardProjectionBuilder.build(
        student_id="student-ada",
        recommendation=recommendation,
        progress=progress,
        timeline=timeline,
        warnings=(),
        empty_states=("cold_start",),
        composed_at="2026-07-20T10:00:00+00:00",
    )
    assert dashboard.student_id == "student-ada"
    assert dashboard.recommendation is recommendation
    assert dashboard.progress is progress
    assert dashboard.timeline is timeline
    assert dashboard.todays_mission is None
    assert dashboard.empty_states == ("cold_start",)
    assert dashboard.composed_at == "2026-07-20T10:00:00+00:00"
