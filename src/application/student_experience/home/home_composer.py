"""Home composition helpers — project Education OS outputs to view models.

Composition only. No mastery estimation, recommendation generation,
mission generation, scheduling, persistence, or AI.
"""

from __future__ import annotations

from datetime import date, timedelta

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.revision_planner.enums import DayKind, SessionStatus
from application.education.revision_planner.execution_history import ExecutionHistory
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.education.revision_planner.models.study_session import StudySession
from application.student_experience.home.enums import (
    FocusActionKind,
    InsightKind,
    MasteryTrendLabel,
    MilestoneKind,
    QuickActionKind,
    ReadinessTrend,
)
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.home.ids import HomeId, SnapshotId
from application.student_experience.home.models.achievement_card import (
    AchievementCard,
    AchievementItem,
)
from application.student_experience.home.models.exam_readiness_card import (
    ExamReadinessCard,
)
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.home.models.home_view_model import HomeViewModel
from application.student_experience.home.models.learning_insight_card import (
    LearningInsight,
    LearningInsightCard,
)
from application.student_experience.home.models.momentum_card import MomentumCard
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.home.models.progress_card import ProgressCard
from application.student_experience.home.models.progress_summary import ProgressSummary
from application.student_experience.home.models.quick_actions_card import (
    QuickAction,
    QuickActionsCard,
)
from application.student_experience.home.models.todays_focus_card import TodaysFocusCard
from application.student_experience.home.models.todays_study_session_card import (
    TodaysStudySessionCard,
)
from application.student_experience.home.models.upcoming_milestone_card import (
    UpcomingMilestoneCard,
)
from application.student_experience.home.ports.achievement_provider import (
    HomeAchievement,
)
from application.student_experience.home.presentation import (
    humanise_identifier,
    mastery_message_for,
    mastery_trend_from_band,
    mission_title,
    readiness_label_from_percent,
    readiness_message_for,
    readiness_trend_from_stability,
    study_objective_label,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)

_ACTIVE_EXECUTION = frozenset(
    {
        ExecutionStatus.STARTED,
        ExecutionStatus.RESUMED,
        ExecutionStatus.PAUSED,
    }
)

_REVISION_TYPES = frozenset(
    {
        MissionType.REVISION_SESSION,
        MissionType.REVISE_PREREQUISITE,
        MissionType.MAINTENANCE_REVIEW,
        MissionType.CONSOLIDATE_KNOWLEDGE,
    }
)


def compose_home(
    inputs: HomeInputs,
    *,
    home_id: HomeId,
    achievements: tuple[HomeAchievement, ...] = (),
) -> HomeViewModel:
    """Compose a full HomeViewModel from Education OS inputs."""
    focus = determine_primary_focus(inputs)
    return HomeViewModel(
        home_id=home_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        todays_focus=_focus_card(focus),
        todays_study_session=compose_todays_session(inputs),
        progress=compose_progress_card(inputs),
        momentum=compose_momentum_card(inputs),
        upcoming_milestone=compose_upcoming_milestone(inputs),
        exam_readiness=compose_exam_readiness(inputs),
        achievements=compose_achievement_card(achievements),
        learning_insights=compose_learning_insights(inputs),
        quick_actions=compose_quick_actions(inputs, focus=focus),
    )


def compose_snapshot(home: HomeViewModel, *, snapshot_id: SnapshotId) -> HomeSnapshot:
    """Project a HomeViewModel into a compact HomeSnapshot."""
    return HomeSnapshot(
        snapshot_id=snapshot_id,
        student_id=home.student_id,
        captured_at=home.composed_at,
        focus_headline=home.todays_focus.headline,
        focus_mission_title=home.todays_focus.mission_title,
        focus_action_label=home.todays_focus.primary_action_label,
        progress_message=home.progress.mastery_message,
        momentum_message=home.momentum.momentum_message,
        completed_missions=home.progress.completed_missions,
        current_streak_days=home.momentum.current_streak_days,
        hours_studied=home.progress.hours_studied,
        exam_available=home.exam_readiness.available,
        exam_days_remaining=home.exam_readiness.days_remaining,
        exam_readiness_label=home.exam_readiness.readiness_label,
        insight_count=len(home.learning_insights.insights),
        quick_action_count=len(home.quick_actions.actions),
        achievement_count=len(home.achievements.items),
    )


def summarise_progress(inputs: HomeInputs) -> ProgressSummary:
    """Compose a ProgressSummary from available Education OS outputs."""
    history = inputs.execution_history or ExecutionHistory()
    trend, message = _mastery_projection(inputs.assessment)
    consistency = _study_consistency_percent(inputs.schedule, inputs.as_of.date())
    hours = _hours_studied(inputs)
    weekly_growth = _weekly_growth_message(inputs)
    gap_count = (
        len(inputs.assessment.knowledge_gaps) if inputs.assessment is not None else 0
    )
    recommendation_count = 0
    if inputs.recommendation_set is not None:
        recommendation_count = inputs.recommendation_set.recommendation_count()
    elif inputs.evaluation is not None and inputs.evaluation.summary is not None:
        recommendation_count = inputs.evaluation.summary.recommendation_count
    return ProgressSummary(
        student_id=inputs.student_id,
        mastery_trend=trend,
        mastery_message=message,
        completed_missions=len(history.completed_mission_ids),
        abandoned_missions=len(history.abandoned_mission_ids),
        in_progress_missions=len(history.in_progress_mission_ids),
        study_consistency_percent=consistency,
        hours_studied=hours,
        weekly_growth_message=weekly_growth,
        knowledge_gap_count=gap_count,
        recommendation_count=recommendation_count,
    )


def determine_primary_focus(inputs: HomeInputs) -> PrimaryFocus:
    """Answer \"What should I do right now?\" from existing artefacts.

    Continues the student's current learning state. Never invents a generic
    navigation CTA when a concrete learning action is available.
    """
    execution = inputs.current_execution

    # Completed mission awaiting reflection — keep the journey continuous.
    if (
        execution is not None
        and execution.status is ExecutionStatus.COMPLETED
        and not execution.reflection_history
    ):
        return _focus_from_execution(
            execution,
            action_kind=FocusActionKind.REVIEW_REFLECTION,
            action_label="Review Reflection",
            reason="Your mission is complete — capture a short reflection next.",
        )

    # Paused mission / in-progress session → resume without losing context.
    if execution is not None and execution.status is ExecutionStatus.PAUSED:
        return _focus_from_execution(
            execution,
            action_kind=FocusActionKind.RESUME_SESSION,
            action_label="Resume Session",
            reason="You have a paused session ready to continue.",
        )

    today = inputs.as_of.date()
    todays_session = _primary_session_on(inputs.schedule, today)
    if (
        todays_session is not None
        and todays_session.status is SessionStatus.IN_PROGRESS
        and (
            execution is None
            or execution.status
            in (ExecutionStatus.PLANNED, ExecutionStatus.PAUSED)
        )
    ):
        mission = _todays_next_mission(inputs.schedule, inputs.mission_plan, today)
        return PrimaryFocus(
            mission_id=str(mission.mission_id) if mission is not None else None,
            mission_title=mission_title(mission) if mission is not None else None,
            estimated_duration_minutes=(
                mission.estimate.duration_minutes if mission is not None else None
            ),
            study_objective=(
                study_objective_label(mission) if mission is not None else None
            ),
            reason="Your study session is already under way — pick up where you left off.",
            action_kind=FocusActionKind.RESUME_SESSION,
            action_label="Resume Session",
            has_focus=True,
        )

    if execution is not None and execution.status in (
        ExecutionStatus.STARTED,
        ExecutionStatus.RESUMED,
    ):
        return _focus_from_execution(
            execution,
            action_kind=FocusActionKind.CONTINUE_MISSION,
            action_label="Continue Mission",
            reason="You're mid-mission — pick up where you left off.",
        )

    todays_mission = _todays_next_mission(inputs.schedule, inputs.mission_plan, today)
    if todays_mission is not None and _is_checkpoint_mission(todays_mission):
        return PrimaryFocus(
            mission_id=str(todays_mission.mission_id),
            mission_title=mission_title(todays_mission),
            estimated_duration_minutes=todays_mission.estimate.duration_minutes,
            study_objective=study_objective_label(todays_mission),
            reason="A checkpoint is coming up — prepare with focused practice.",
            action_kind=FocusActionKind.PREPARE_CHECKPOINT,
            action_label="Prepare Checkpoint",
            has_focus=True,
        )

    if todays_mission is not None:
        return PrimaryFocus(
            mission_id=str(todays_mission.mission_id),
            mission_title=mission_title(todays_mission),
            estimated_duration_minutes=todays_mission.estimate.duration_minutes,
            study_objective=study_objective_label(todays_mission),
            reason=_todays_focus_reason(todays_mission),
            action_kind=FocusActionKind.START_MISSION,
            action_label="Start today's mission",
            has_focus=True,
        )

    pending = _next_pending_mission(inputs.mission_plan, inputs.execution_history)
    if pending is not None and _is_checkpoint_mission(pending):
        return PrimaryFocus(
            mission_id=str(pending.mission_id),
            mission_title=mission_title(pending),
            estimated_duration_minutes=pending.estimate.duration_minutes,
            study_objective=study_objective_label(pending),
            reason="Your next planned work prepares an upcoming checkpoint.",
            action_kind=FocusActionKind.PREPARE_CHECKPOINT,
            action_label="Prepare Checkpoint",
            has_focus=True,
        )

    if pending is not None:
        return PrimaryFocus(
            mission_id=str(pending.mission_id),
            mission_title=mission_title(pending),
            estimated_duration_minutes=pending.estimate.duration_minutes,
            study_objective=study_objective_label(pending),
            reason="This is your next planned mission.",
            action_kind=FocusActionKind.START_MISSION,
            action_label="Start next mission",
            has_focus=True,
        )

    if inputs.schedule is not None:
        return PrimaryFocus(
            mission_id=None,
            mission_title=None,
            estimated_duration_minutes=None,
            study_objective=None,
            reason="No mission is queued for right now — check your schedule.",
            action_kind=FocusActionKind.VIEW_SCHEDULE,
            action_label="View schedule",
            has_focus=False,
        )

    return PrimaryFocus(
        mission_id=None,
        mission_title=None,
        estimated_duration_minutes=None,
        study_objective=None,
        reason="Nothing is queued yet. Your home will update as study work appears.",
        action_kind=FocusActionKind.NONE,
        action_label="Check back soon",
        has_focus=False,
    )


def compose_todays_session(inputs: HomeInputs) -> TodaysStudySessionCard:
    today = inputs.as_of.date()
    session = _primary_session_on(inputs.schedule, today)
    if session is None:
        return TodaysStudySessionCard(
            session_date=today,
            start_time=None,
            end_time=None,
            estimated_duration_minutes=0,
            mission_count=0,
            status_label="No session scheduled",
            has_session=False,
        )
    objectives = tuple(
        humanise_identifier(code.value) for code in session.objectives
    )
    summary = ", ".join(objectives) if objectives else None
    return TodaysStudySessionCard(
        session_date=session.session_date,
        start_time=session.start_time,
        end_time=session.end_time,
        estimated_duration_minutes=session.estimated_duration_minutes,
        mission_count=len(session.scheduled_mission_ids),
        status_label=humanise_identifier(session.status.value),
        session_id=str(session.session_id),
        has_session=True,
        objectives_summary=summary,
    )


def compose_progress_card(inputs: HomeInputs) -> ProgressCard:
    summary = summarise_progress(inputs)
    has_data = (
        inputs.assessment is not None
        or inputs.execution_history is not None
        or inputs.schedule is not None
        or inputs.evaluation is not None
    )
    return ProgressCard(
        mastery_trend=summary.mastery_trend,
        mastery_message=summary.mastery_message,
        completed_missions=summary.completed_missions,
        study_consistency_percent=summary.study_consistency_percent,
        hours_studied=summary.hours_studied,
        weekly_growth_message=summary.weekly_growth_message,
        has_progress_data=has_data,
    )


def compose_momentum_card(inputs: HomeInputs) -> MomentumCard:
    today = inputs.as_of.date()
    streak = _current_streak_days(inputs.schedule, today)
    weekly = _weekly_consistency_percent(inputs.schedule, today)
    completion = _recent_completion_rate_percent(inputs.execution_history)
    average = _average_session_duration_minutes(inputs.schedule, inputs.mission_plan)
    message = _momentum_message(streak, weekly, completion)
    has_data = inputs.schedule is not None or inputs.execution_history is not None
    return MomentumCard(
        current_streak_days=streak,
        weekly_consistency_percent=weekly,
        recent_completion_rate_percent=completion,
        average_session_duration_minutes=average,
        momentum_message=message,
        has_momentum_data=has_data,
    )


def compose_upcoming_milestone(inputs: HomeInputs) -> UpcomingMilestoneCard:
    today = inputs.as_of.date()
    exam = inputs.exam_target
    if exam is not None and exam.exam_date >= today:
        days = (exam.exam_date - today).days
        return UpcomingMilestoneCard(
            title=f"Exam: {humanise_identifier(exam.examination_id)}",
            kind=MilestoneKind.EXAM,
            milestone_date=exam.exam_date,
            days_until=days,
            detail=f"{days} day{'s' if days != 1 else ''} remaining",
            has_milestone=True,
        )

    next_session = _next_future_session(inputs.schedule, today)
    if next_session is not None:
        days = (next_session.session_date - today).days
        return UpcomingMilestoneCard(
            title="Next study session",
            kind=MilestoneKind.STUDY_SESSION,
            milestone_date=next_session.session_date,
            days_until=days,
            detail=(
                f"{next_session.estimated_duration_minutes} minutes planned"
            ),
            has_milestone=True,
        )

    checkpoint = _next_checkpoint_mission(inputs.mission_plan, inputs.execution_history)
    if checkpoint is not None:
        return UpcomingMilestoneCard(
            title=mission_title(checkpoint),
            kind=MilestoneKind.CHECKPOINT,
            milestone_date=None,
            days_until=None,
            detail=study_objective_label(checkpoint),
            has_milestone=True,
        )

    return UpcomingMilestoneCard(
        title="No upcoming milestone",
        kind=MilestoneKind.STUDY_SESSION,
        milestone_date=None,
        days_until=None,
        detail="Milestones will appear as your plan develops.",
        has_milestone=False,
    )


def compose_exam_readiness(inputs: HomeInputs) -> ExamReadinessCard:
    exam = inputs.exam_target
    if exam is None:
        return ExamReadinessCard(
            available=False,
            readiness_label="No exam target set",
            readiness_percent=None,
            trend=ReadinessTrend.UNKNOWN,
            trend_message="Set an exam target to see readiness projections.",
            target_exam_label=None,
            exam_date=None,
            days_remaining=None,
            next_milestone=None,
        )

    today = inputs.as_of.date()
    days_remaining = (exam.exam_date - today).days
    readiness_percent: float | None = None
    trend = ReadinessTrend.UNKNOWN
    if inputs.assessment is not None:
        readiness_percent = round(
            float(inputs.assessment.overall_mastery.magnitude) * 100.0, 2
        )
        trend = readiness_trend_from_stability(
            inputs.assessment.overall_stability.band
        )
    elif inputs.evaluation is not None and inputs.evaluation.summary is not None:
        readiness_percent = round(
            float(inputs.evaluation.summary.mastery_magnitude) * 100.0, 2
        )
        trend = readiness_trend_from_stability(
            inputs.evaluation.summary.stability_band
        )

    milestone = compose_upcoming_milestone(inputs)
    next_milestone = milestone.title if milestone.has_milestone else None
    return ExamReadinessCard(
        available=True,
        readiness_label=readiness_label_from_percent(readiness_percent),
        readiness_percent=readiness_percent,
        trend=trend,
        trend_message=readiness_message_for(trend),
        target_exam_label=humanise_identifier(exam.examination_id),
        exam_date=exam.exam_date,
        days_remaining=days_remaining,
        next_milestone=next_milestone,
    )


def compose_achievement_card(
    achievements: tuple[HomeAchievement, ...],
) -> AchievementCard:
    items = tuple(
        AchievementItem(
            achievement_id=item.achievement_id,
            title=item.title,
            description=item.description,
            earned_at=item.earned_at,
            category=item.category,
        )
        for item in achievements
    )
    return AchievementCard(items=items)


def compose_learning_insights(inputs: HomeInputs) -> LearningInsightCard:
    insights: list[LearningInsight] = []

    improved = _most_improved_subject(inputs.assessment)
    if improved is not None:
        insights.append(improved)

    weakest = _weakest_competency(inputs.assessment)
    if weakest is not None:
        insights.append(weakest)

    opportunity = _biggest_opportunity(inputs)
    if opportunity is not None:
        insights.append(opportunity)

    quality = _mission_completion_quality(inputs.execution_history)
    if quality is not None:
        insights.append(quality)

    prerequisite = _upcoming_prerequisite(inputs.mission_plan, inputs.execution_history)
    if prerequisite is not None:
        insights.append(prerequisite)

    return LearningInsightCard(insights=tuple(insights))


def compose_quick_actions(
    inputs: HomeInputs, *, focus: PrimaryFocus | None = None
) -> QuickActionsCard:
    focus = focus or determine_primary_focus(inputs)
    actions: list[QuickAction] = []
    execution = inputs.current_execution

    if focus.action_kind is FocusActionKind.REVIEW_REFLECTION:
        actions.append(
            QuickAction(
                kind=QuickActionKind.REVIEW_REFLECTION,
                label="Review Reflection",
                enabled=True,
                mission_id=focus.mission_id,
                detail=focus.reason,
            )
        )
    elif focus.action_kind is FocusActionKind.RESUME_SESSION:
        actions.append(
            QuickAction(
                kind=QuickActionKind.RESUME_SESSION,
                label="Resume Session",
                enabled=True,
                mission_id=focus.mission_id,
            )
        )
    elif focus.action_kind is FocusActionKind.CONTINUE_MISSION:
        actions.append(
            QuickAction(
                kind=QuickActionKind.CONTINUE_MISSION,
                label="Continue Mission",
                enabled=True,
                mission_id=focus.mission_id
                or (str(execution.mission_id) if execution is not None else None),
            )
        )
    elif focus.action_kind is FocusActionKind.PREPARE_CHECKPOINT:
        actions.append(
            QuickAction(
                kind=QuickActionKind.PREPARE_CHECKPOINT,
                label="Prepare Checkpoint",
                enabled=True,
                mission_id=focus.mission_id,
            )
        )
    elif focus.action_kind is FocusActionKind.RESUME_MISSION:
        actions.append(
            QuickAction(
                kind=QuickActionKind.RESUME_PAUSED_MISSION,
                label="Resume Session",
                enabled=True,
                mission_id=focus.mission_id,
            )
        )
    elif focus.has_focus and focus.action_kind is FocusActionKind.START_MISSION:
        actions.append(
            QuickAction(
                kind=QuickActionKind.START_TODAYS_MISSION,
                label="Start today's mission",
                enabled=True,
                mission_id=focus.mission_id,
            )
        )

    yesterday = inputs.as_of.date() - timedelta(days=1)
    if _primary_session_on(inputs.schedule, yesterday) is not None:
        actions.append(
            QuickAction(
                kind=QuickActionKind.REVIEW_YESTERDAY,
                label="Review yesterday",
                enabled=True,
                detail="Look back at yesterday's study session",
            )
        )

    if inputs.schedule is not None:
        actions.append(
            QuickAction(
                kind=QuickActionKind.VIEW_SCHEDULE,
                label="View schedule",
                enabled=True,
            )
        )

    revision = _next_revision_mission(inputs.mission_plan, inputs.execution_history)
    if revision is not None:
        actions.append(
            QuickAction(
                kind=QuickActionKind.CONTINUE_REVISION,
                label="Continue revision",
                enabled=True,
                mission_id=str(revision.mission_id),
                detail=mission_title(revision),
            )
        )

    return QuickActionsCard(actions=tuple(actions))


# --- internal helpers -----------------------------------------------------


def _focus_card(focus: PrimaryFocus) -> TodaysFocusCard:
    if focus.has_focus and focus.mission_title:
        headline = f"Today's focus is {focus.mission_title}."
    elif focus.action_kind is FocusActionKind.VIEW_SCHEDULE:
        headline = "Check your schedule for what to do next."
    else:
        headline = "Nothing queued for right now."
    return TodaysFocusCard(
        headline=headline,
        mission_title=focus.mission_title,
        estimated_duration_minutes=focus.estimated_duration_minutes,
        study_objective=focus.study_objective,
        reason=focus.reason,
        primary_action_label=focus.action_label,
        primary_action_kind=focus.action_kind,
        mission_id=focus.mission_id,
        has_focus=focus.has_focus,
    )


def _focus_from_execution(
    execution: MissionExecution,
    *,
    action_kind: FocusActionKind,
    action_label: str,
    reason: str,
) -> PrimaryFocus:
    mission = execution.mission
    return PrimaryFocus(
        mission_id=str(mission.mission_id),
        mission_title=mission_title(mission),
        estimated_duration_minutes=mission.estimate.duration_minutes,
        study_objective=study_objective_label(mission),
        reason=reason,
        action_kind=action_kind,
        action_label=action_label,
        has_focus=True,
    )


def _todays_focus_reason(mission: Mission) -> str:
    if mission.is_prerequisite():
        return "A prerequisite needs attention before you move forward."
    scope = humanise_identifier(mission.competency_id) or humanise_identifier(
        mission.subject_id
    )
    if scope:
        return f"Today's focus is {scope}."
    return "This is the highest-priority work queued for today."


def _is_checkpoint_mission(mission: Mission) -> bool:
    return (
        mission.mission_type is MissionType.CHECKPOINT_PREPARATION
        or mission.objective.code is MissionObjectiveCode.PREPARE_CHECKPOINT
    )


def _primary_session_on(
    schedule: StudySchedule | None, day: date
) -> StudySession | None:
    if schedule is None:
        return None
    sessions = sorted(
        schedule.sessions_on(day),
        key=lambda session: (session.sequence_index, session.start_time),
    )
    for session in sessions:
        if session.status is not SessionStatus.CANCELLED:
            return session
    return None


def _todays_next_mission(
    schedule: StudySchedule | None,
    plan: MissionPlan | None,
    today: date,
) -> Mission | None:
    session = _primary_session_on(schedule, today)
    if session is None or plan is None:
        return None
    by_id = {mission.mission_id: mission for mission in plan.missions}
    for mission_id in session.scheduled_mission_ids:
        mission = by_id.get(mission_id)
        if mission is not None:
            return mission
    return None


def _next_pending_mission(
    plan: MissionPlan | None,
    history: ExecutionHistory | None,
) -> Mission | None:
    if plan is None or plan.is_empty():
        return None
    completed = set(history.completed_mission_ids) if history is not None else set()
    in_progress = (
        set(history.in_progress_mission_ids) if history is not None else set()
    )
    for mission in sorted(plan.missions, key=lambda item: item.ordering.rank):
        if mission.mission_id in completed:
            continue
        if mission.mission_id in in_progress:
            continue
        return mission
    return None


def _next_revision_mission(
    plan: MissionPlan | None,
    history: ExecutionHistory | None,
) -> Mission | None:
    if plan is None:
        return None
    completed = set(history.completed_mission_ids) if history is not None else set()
    for mission in sorted(plan.missions, key=lambda item: item.ordering.rank):
        if mission.mission_id in completed:
            continue
        if mission.mission_type in _REVISION_TYPES:
            return mission
    return None


def _next_checkpoint_mission(
    plan: MissionPlan | None,
    history: ExecutionHistory | None,
) -> Mission | None:
    if plan is None:
        return None
    completed = set(history.completed_mission_ids) if history is not None else set()
    for mission in sorted(plan.missions, key=lambda item: item.ordering.rank):
        if mission.mission_id in completed:
            continue
        if mission.mission_type is MissionType.CHECKPOINT_PREPARATION:
            return mission
    return None


def _next_future_session(
    schedule: StudySchedule | None, today: date
) -> StudySession | None:
    if schedule is None:
        return None
    candidates = [
        session
        for session in schedule.active_sessions()
        if session.session_date > today
    ]
    if not candidates:
        return None
    return sorted(
        candidates, key=lambda session: (session.session_date, session.start_time)
    )[0]


def _mastery_projection(
    assessment: MasteryAssessment | None,
) -> tuple[MasteryTrendLabel, str]:
    if assessment is None:
        trend = MasteryTrendLabel.NOT_YET_ASSESSED
        return trend, mastery_message_for(trend)
    trend = mastery_trend_from_band(assessment.overall_mastery.band)
    return trend, mastery_message_for(trend)


def _study_consistency_percent(
    schedule: StudySchedule | None, today: date
) -> float:
    if schedule is None:
        return 0.0
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    planned = 0
    completed = 0
    for session in schedule.sessions:
        if session.session_date < week_start or session.session_date > week_end:
            continue
        if session.session_date > today:
            continue
        if session.status is SessionStatus.CANCELLED:
            continue
        planned += 1
        if session.status is SessionStatus.COMPLETED:
            completed += 1
    if planned == 0:
        return 0.0
    return round((completed / planned) * 100.0, 2)


def _weekly_consistency_percent(
    schedule: StudySchedule | None, today: date
) -> float:
    return _study_consistency_percent(schedule, today)


def _hours_studied(inputs: HomeInputs) -> float:
    seconds = 0.0
    history = inputs.execution_history
    plan = inputs.mission_plan
    if history is not None and plan is not None:
        by_id = {mission.mission_id: mission for mission in plan.missions}
        for mission_id in history.completed_mission_ids:
            mission = by_id.get(mission_id)
            if mission is not None:
                seconds += mission.estimate.duration_minutes * 60.0
    if inputs.current_execution is not None:
        if inputs.current_execution.status in _ACTIVE_EXECUTION:
            seconds += max(0.0, inputs.current_execution.elapsed_study_time_seconds)
        elif (
            inputs.current_execution.status is ExecutionStatus.COMPLETED
            and (
                history is None
                or inputs.current_execution.mission_id
                not in history.completed_mission_ids
            )
        ):
            seconds += max(0.0, inputs.current_execution.elapsed_study_time_seconds)
    return round(seconds / 3600.0, 2)


def _weekly_growth_message(inputs: HomeInputs) -> str:
    if inputs.evaluation is not None and inputs.evaluation.summary is not None:
        summary = inputs.evaluation.summary
        if summary.knowledge_gap_count == 0:
            return "No open knowledge gaps in your latest evaluation."
        if summary.knowledge_gap_count == 1:
            return "One knowledge gap remains in focus this week."
        return (
            f"{summary.knowledge_gap_count} knowledge gaps remain in focus this week."
        )
    if inputs.assessment is not None:
        gaps = len(inputs.assessment.knowledge_gaps)
        if gaps == 0:
            return "You're covering ground without open gaps."
        return f"{gaps} knowledge gap{'s' if gaps != 1 else ''} still need attention."
    history = inputs.execution_history
    if history is not None and history.completed_mission_ids:
        count = len(history.completed_mission_ids)
        return f"You've completed {count} mission{'s' if count != 1 else ''} so far."
    return "Weekly growth will appear as you complete study work."


def _current_streak_days(schedule: StudySchedule | None, today: date) -> int:
    if schedule is None:
        return 0
    completed_days = {
        session.session_date
        for session in schedule.sessions
        if session.status is SessionStatus.COMPLETED
        and session.session_date <= today
    }
    # Also treat study days that had any non-cancelled session today/past
    # as streak-capable when completed_days is empty but day was studied.
    streak = 0
    cursor = today
    while True:
        day = schedule.day_for(cursor)
        studied = cursor in completed_days
        if not studied and day is not None and day.kind is DayKind.STUDY:
            # Count today as streak if an in-progress or planned session exists
            # and we have active work today; otherwise require COMPLETED.
            sessions = schedule.sessions_on(cursor)
            studied = any(
                session.status is SessionStatus.COMPLETED for session in sessions
            )
            if not studied and cursor == today:
                studied = any(
                    session.status
                    in (SessionStatus.IN_PROGRESS, SessionStatus.COMPLETED)
                    for session in sessions
                )
        if not studied:
            break
        streak += 1
        cursor = cursor - timedelta(days=1)
        if streak > 366:
            break
    return streak


def _recent_completion_rate_percent(history: ExecutionHistory | None) -> float:
    if history is None:
        return 0.0
    completed = len(history.completed_mission_ids)
    abandoned = len(history.abandoned_mission_ids)
    total = completed + abandoned
    if total == 0:
        return 0.0
    return round((completed / total) * 100.0, 2)


def _average_session_duration_minutes(
    schedule: StudySchedule | None,
    plan: MissionPlan | None,
) -> float:
    if schedule is not None and schedule.sessions:
        total = sum(session.estimated_duration_minutes for session in schedule.sessions)
        return round(total / len(schedule.sessions), 2)
    if plan is not None and not plan.is_empty():
        total = plan.total_duration_minutes()
        return round(total / plan.mission_count(), 2)
    return 0.0


def _momentum_message(streak: int, weekly: float, completion: float) -> str:
    if streak >= 3:
        return f"You're on a {streak}-day study streak — keep the momentum."
    if weekly >= 70.0:
        return "Your weekly consistency is strong."
    if completion >= 70.0:
        return "You're finishing most of the missions you start."
    if streak > 0:
        return f"{streak}-day streak underway."
    return "Start a session today to build momentum."


def _most_improved_subject(
    assessment: MasteryAssessment | None,
) -> LearningInsight | None:
    if assessment is None or not assessment.subject_assessments:
        return None
    ranked = sorted(
        assessment.subject_assessments,
        key=lambda subject: (
            -subject.mastery.magnitude,
            subject.subject_id.value,
        ),
    )
    top = ranked[0]
    label = humanise_identifier(top.subject_id.value)
    return LearningInsight(
        kind=InsightKind.MOST_IMPROVED_SUBJECT,
        title="Most improved subject",
        message=f"{label} is your strongest assessed subject right now.",
    )


def _weakest_competency(
    assessment: MasteryAssessment | None,
) -> LearningInsight | None:
    if assessment is None:
        return None
    if assessment.knowledge_gaps:
        gap = sorted(
            assessment.knowledge_gaps,
            key=lambda item: (
                item.severity.value,
                item.mastery_score.magnitude,
                item.competency_id.value,
            ),
        )[0]
        label = humanise_identifier(gap.competency_id.value)
        return LearningInsight(
            kind=InsightKind.WEAKEST_COMPETENCY,
            title="Weakest competency",
            message=f"{label} needs the most attention.",
        )
    competencies = [
        competency
        for subject in assessment.subject_assessments
        for competency in subject.competency_assessments
        if competency.mastery.has_evidence()
    ]
    if not competencies:
        return None
    weakest = sorted(
        competencies,
        key=lambda item: (item.mastery.magnitude, item.competency_id.value),
    )[0]
    label = humanise_identifier(weakest.competency_id.value)
    return LearningInsight(
        kind=InsightKind.WEAKEST_COMPETENCY,
        title="Weakest competency",
        message=f"{label} is your lowest assessed competency.",
    )


def _biggest_opportunity(inputs: HomeInputs) -> LearningInsight | None:
    if inputs.evaluation is not None and inputs.evaluation.decisions:
        decision = min(inputs.evaluation.decisions, key=lambda item: item.rank)
        scope = humanise_identifier(decision.competency_id) or humanise_identifier(
            decision.subject_id
        )
        category = humanise_identifier(decision.category)
        detail = f"{category}" if not scope else f"{category} for {scope}"
        return LearningInsight(
            kind=InsightKind.BIGGEST_OPPORTUNITY,
            title="Biggest opportunity",
            message=f"Your top opportunity is {detail}.",
        )
    if inputs.recommendation_set is not None:
        top = inputs.recommendation_set.highest_priority()
        if top is not None:
            target = top.target
            scope = ""
            if target.competency_id is not None:
                scope = humanise_identifier(target.competency_id.value)
            elif target.subject_id is not None:
                scope = humanise_identifier(target.subject_id.value)
            category = humanise_identifier(top.category.value)
            detail = f"{category}" if not scope else f"{category} for {scope}"
            return LearningInsight(
                kind=InsightKind.BIGGEST_OPPORTUNITY,
                title="Biggest opportunity",
                message=f"Your top opportunity is {detail}.",
            )
    return None


def _mission_completion_quality(
    history: ExecutionHistory | None,
) -> LearningInsight | None:
    if history is None:
        return None
    completed = len(history.completed_mission_ids)
    abandoned = len(history.abandoned_mission_ids)
    total = completed + abandoned
    if total == 0:
        return None
    rate = round((completed / total) * 100.0)
    return LearningInsight(
        kind=InsightKind.MISSION_COMPLETION_QUALITY,
        title="Mission completion quality",
        message=f"You complete {rate}% of the missions you start.",
    )


def _upcoming_prerequisite(
    plan: MissionPlan | None,
    history: ExecutionHistory | None,
) -> LearningInsight | None:
    if plan is None:
        return None
    completed = set(history.completed_mission_ids) if history is not None else set()
    for mission in sorted(plan.missions, key=lambda item: item.ordering.rank):
        if mission.mission_id in completed:
            continue
        if mission.is_prerequisite():
            label = mission_title(mission)
            return LearningInsight(
                kind=InsightKind.UPCOMING_PREREQUISITE,
                title="Upcoming prerequisite",
                message=f"Next prerequisite work: {label}.",
            )
    return None
