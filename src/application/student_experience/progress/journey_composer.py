"""Journey composition helpers — project Education OS histories to view models.

Composition only. No mastery estimation, recommendation generation,
mission generation, scheduling, persistence, or AI.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.enums import MissionType
from application.education.revision_planner.enums import SessionStatus
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.progress.enums import (
    JourneyMilestoneKind,
    TimelineEventKind,
    TrajectoryLabel,
    TrendDirection,
)
from application.student_experience.progress.ids import JourneyId, JourneySnapshotId
from application.student_experience.progress.journey_inputs import JourneyInputs
from application.student_experience.progress.models.achievement_timeline import (
    AchievementTimeline,
    AchievementTimelineItem,
)
from application.student_experience.progress.models.consistency_card import (
    ConsistencyCard,
)
from application.student_experience.progress.models.growth_card import GrowthCard
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)
from application.student_experience.progress.models.learning_trend_card import (
    LearningTrendCard,
)
from application.student_experience.progress.models.milestone_card import (
    JourneyMilestone,
    MilestoneCard,
)
from application.student_experience.progress.models.monthly_summary import (
    MonthlySummary,
)
from application.student_experience.progress.models.progress_overview_card import (
    ProgressOverviewCard,
)
from application.student_experience.progress.models.study_habits_card import (
    StudyHabitsCard,
)
from application.student_experience.progress.models.timeline_card import (
    TimelineCard,
    TimelineEvent,
)
from application.student_experience.progress.models.weekly_summary import WeeklySummary
from application.student_experience.progress.ports.milestone_provider import (
    ProvidedMilestone,
)
from application.student_experience.progress.presentation import (
    count_phrase,
    humanise_identifier,
    study_time_band,
    study_time_message,
    trajectory_from_activity,
    trajectory_message,
    trend_from_deltas,
    trend_message,
    weekday_label,
    weekday_message,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import MasteryBand

_COMPLETED = ExecutionStatus.COMPLETED
_ABANDONED = ExecutionStatus.ABANDONED
_REVISION_TYPES = frozenset(
    {
        MissionType.REVISION_SESSION,
        MissionType.REVISE_PREREQUISITE,
        MissionType.MAINTENANCE_REVIEW,
        MissionType.CONSOLIDATE_KNOWLEDGE,
    }
)
_CHECKPOINT_TYPES = frozenset({MissionType.CHECKPOINT_PREPARATION})
_TIMELINE_LIMIT = 40


def compose_journey(
    inputs: JourneyInputs,
    *,
    journey_id: JourneyId,
    provided_milestones: tuple[ProvidedMilestone, ...] = (),
) -> LearningJourneyViewModel:
    """Compose a full LearningJourneyViewModel from Education OS histories."""
    growth = summarise_growth(inputs)
    consistency = summarise_consistency(inputs)
    habits = summarise_habits(inputs)
    timeline = build_timeline(inputs)
    overview = compose_progress_overview(inputs, growth=growth, consistency=consistency)
    milestones = compose_milestones(inputs, provided=provided_milestones)
    trends = compose_learning_trends(inputs, consistency=consistency)
    achievements = compose_achievement_timeline(milestones)
    weekly = compose_weekly_summary(inputs)
    monthly = compose_monthly_summary(inputs)
    return LearningJourneyViewModel(
        journey_id=journey_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        timeline=timeline,
        progress_overview=overview,
        growth=growth,
        consistency=consistency,
        study_habits=habits,
        milestones=milestones,
        learning_trends=trends,
        achievement_timeline=achievements,
        weekly_summary=weekly,
        monthly_summary=monthly,
    )


def compose_snapshot(
    journey: LearningJourneyViewModel,
    *,
    snapshot_id: JourneySnapshotId,
    home_focus_headline: str | None = None,
) -> JourneySnapshot:
    """Project a LearningJourneyViewModel into a compact JourneySnapshot."""
    return JourneySnapshot(
        snapshot_id=snapshot_id,
        student_id=journey.student_id,
        captured_at=journey.composed_at,
        trajectory=journey.progress_overview.trajectory,
        trajectory_message=journey.progress_overview.trajectory_message,
        timeline_event_count=len(journey.timeline.events),
        milestone_count=len(journey.milestones.milestones),
        current_streak_days=journey.consistency.current_streak_days,
        longest_streak_days=journey.consistency.longest_streak_days,
        weekly_missions_completed=journey.growth.weekly_missions_completed,
        monthly_missions_completed=journey.growth.monthly_missions_completed,
        mastery_trend=journey.learning_trends.mastery_trend,
        consistency_message=journey.consistency.consistency_message,
        habits_message=journey.study_habits.preferred_study_time_message,
        home_focus_headline=home_focus_headline,
    )


def build_timeline(inputs: JourneyInputs) -> TimelineCard:
    """Compose chronological educational events — descriptive only."""
    events: list[TimelineEvent] = []
    events.extend(_timeline_from_executions(inputs.execution_history))
    events.extend(_timeline_from_assessments(inputs.assessment_history))
    events.extend(_timeline_from_recommendations(inputs.recommendation_history))
    events.extend(_timeline_from_schedules(inputs.schedule_history))
    events.extend(_timeline_from_evaluations(inputs.evaluation_history))
    events.sort(key=lambda event: event.occurred_at)
    if len(events) > _TIMELINE_LIMIT:
        events = events[-_TIMELINE_LIMIT:]
    if not events:
        return TimelineCard(
            events=(),
            headline="Your learning timeline",
            has_events=False,
        )
    return TimelineCard(
        events=tuple(events),
        headline="Your learning timeline",
        has_events=True,
    )


def summarise_growth(inputs: JourneyInputs) -> GrowthCard:
    """Compose weekly and monthly growth from historical artefacts."""
    today = inputs.as_of.date()
    week_start = today - timedelta(days=6)
    month_start = today - timedelta(days=29)
    weekly_missions = _completed_missions_between(
        inputs.execution_history, week_start, today
    )
    monthly_missions = _completed_missions_between(
        inputs.execution_history, month_start, today
    )
    weekly_delta = _mastery_delta_between(
        inputs.assessment_history, week_start, today
    )
    monthly_delta = _mastery_delta_between(
        inputs.assessment_history, month_start, today
    )
    mastery_values = tuple(
        assessment.overall_mastery.magnitude
        for assessment in _sorted_assessments(inputs.assessment_history)
    )
    mastery_trend = trend_from_deltas(mastery_values)
    weekly_message = _growth_message(
        period="week",
        missions=weekly_missions,
        mastery_delta=weekly_delta,
    )
    monthly_message = _growth_message(
        period="month",
        missions=monthly_missions,
        mastery_delta=monthly_delta,
    )
    has_data = (
        weekly_missions > 0
        or monthly_missions > 0
        or weekly_delta is not None
        or monthly_delta is not None
    )
    return GrowthCard(
        weekly_missions_completed=weekly_missions,
        monthly_missions_completed=monthly_missions,
        weekly_mastery_delta=weekly_delta,
        monthly_mastery_delta=monthly_delta,
        weekly_growth_message=weekly_message,
        monthly_growth_message=monthly_message,
        mastery_trend=mastery_trend,
        has_growth_data=has_data,
    )


def summarise_consistency(inputs: JourneyInputs) -> ConsistencyCard:
    """Compose streak, frequency, and completion consistency."""
    today = inputs.as_of.date()
    study_days = _study_days(inputs)
    current_streak = _current_streak(study_days, today)
    longest_streak = _longest_streak(study_days)
    avg_weekly = _average_weekly_sessions(inputs, today)
    completion_rate = _completion_rate_percent(inputs)
    frequency = _frequency_message(avg_weekly, study_days)
    message = _consistency_message(current_streak, longest_streak, completion_rate)
    has_data = bool(study_days) or bool(inputs.execution_history) or bool(
        inputs.study_statistics
    )
    return ConsistencyCard(
        current_streak_days=current_streak,
        longest_streak_days=longest_streak,
        study_frequency_message=frequency,
        average_weekly_sessions=avg_weekly,
        average_completion_rate_percent=completion_rate,
        consistency_message=message,
        has_consistency_data=has_data,
    )


def summarise_habits(inputs: JourneyInputs) -> StudyHabitsCard:
    """Compose deterministic study habits from execution and schedule history."""
    preferred_hour = _preferred_hour(inputs)
    preferred_band = study_time_band(preferred_hour)
    weekday = _most_productive_weekday(inputs)
    weekday_lbl = weekday_label(weekday)
    avg_duration = _average_session_minutes(inputs)
    reliability = _completion_rate_percent(inputs)
    quality = _mission_quality_message(inputs)
    has_data = (
        preferred_hour is not None
        or weekday is not None
        or avg_duration > 0.0
        or bool(inputs.execution_history)
        or bool(inputs.study_statistics)
    )
    return StudyHabitsCard(
        preferred_study_time=preferred_band,
        preferred_study_time_message=study_time_message(preferred_band),
        average_session_duration_minutes=avg_duration,
        most_productive_weekday=weekday_lbl,
        most_productive_weekday_message=weekday_message(weekday_lbl),
        completion_reliability_percent=reliability,
        completion_reliability_message=_reliability_message(reliability),
        mission_completion_quality_message=quality,
        has_habits_data=has_data,
    )


def compose_progress_overview(
    inputs: JourneyInputs,
    *,
    growth: GrowthCard,
    consistency: ConsistencyCard,
) -> ProgressOverviewCard:
    """Compose trajectory, growth highlights, and momentum language."""
    completed = _completed_count(inputs)
    trajectory = trajectory_from_activity(
        completed_missions=completed,
        current_streak=consistency.current_streak_days,
        weekly_missions=growth.weekly_missions_completed,
    )
    if trajectory is TrajectoryLabel.UNKNOWN and inputs.home_snapshot is not None:
        if inputs.home_snapshot.completed_missions > 0:
            trajectory = TrajectoryLabel.BUILDING
    strongest = _strongest_subject(inputs.assessment_history)
    improved = _most_improved_competency(inputs.assessment_history)
    momentum = _momentum_message(
        consistency.current_streak_days,
        growth.weekly_missions_completed,
        inputs.home_snapshot,
    )
    has_data = (
        completed > 0
        or growth.has_growth_data
        or consistency.has_consistency_data
        or strongest is not None
        or inputs.home_snapshot is not None
    )
    return ProgressOverviewCard(
        trajectory=trajectory,
        trajectory_message=trajectory_message(trajectory),
        weekly_growth_message=growth.weekly_growth_message,
        monthly_growth_message=growth.monthly_growth_message,
        strongest_subject=strongest,
        most_improved_competency=improved,
        learning_momentum_message=momentum,
        has_overview_data=has_data,
    )


def compose_milestones(
    inputs: JourneyInputs,
    *,
    provided: tuple[ProvidedMilestone, ...] = (),
) -> MilestoneCard:
    """Compose projected educational milestones from history and provider."""
    milestones: list[JourneyMilestone] = []
    completed = _completed_executions(inputs.execution_history)
    if completed:
        first = min(
            completed,
            key=lambda execution: execution.finished_at or inputs.as_of,
        )
        milestones.append(
            JourneyMilestone(
                kind=JourneyMilestoneKind.FIRST_MISSION,
                title="Completed first mission",
                message="You completed your first mission.",
                reached_at=first.finished_at or first.started_at,
            )
        )
    if any(
        execution.mission.mission_type in _REVISION_TYPES for execution in completed
    ):
        revision = next(
            execution
            for execution in completed
            if execution.mission.mission_type in _REVISION_TYPES
        )
        milestones.append(
            JourneyMilestone(
                kind=JourneyMilestoneKind.FIRST_REVISION_CYCLE,
                title="Completed first revision cycle",
                message="You finished your first revision session.",
                reached_at=revision.finished_at or revision.started_at,
            )
        )
    for assessment in _sorted_assessments(inputs.assessment_history):
        for subject in assessment.subject_assessments:
            for competency in subject.competency_assessments:
                if competency.mastery.band is MasteryBand.MASTERED:
                    label = humanise_identifier(str(competency.competency_id))
                    milestones.append(
                        JourneyMilestone(
                            kind=JourneyMilestoneKind.COMPETENCY_MASTERED,
                            title=f"Mastered {label}",
                            message=f"You reached mastery in {label}.",
                            reached_at=assessment.assessed_at,
                        )
                    )
            if subject.mastery.band is MasteryBand.MASTERED:
                label = humanise_identifier(str(subject.subject_id))
                milestones.append(
                    JourneyMilestone(
                        kind=JourneyMilestoneKind.SUBJECT_FINISHED,
                        title=f"Finished {label}",
                        message=f"You finished {label}.",
                        reached_at=assessment.assessed_at,
                    )
                )
    if inputs.home_snapshot is not None and inputs.home_snapshot.exam_available:
        readiness = (inputs.home_snapshot.exam_readiness_label or "").lower()
        if "ready" in readiness or "strong" in readiness:
            milestones.append(
                JourneyMilestone(
                    kind=JourneyMilestoneKind.READINESS_TARGET,
                    title="Reached readiness target",
                    message="You reached your exam readiness target.",
                    reached_at=inputs.home_snapshot.captured_at,
                )
            )
    streak_days = _current_streak(_study_days(inputs), inputs.as_of.date())
    if streak_days >= 7:
        milestones.append(
            JourneyMilestone(
                kind=JourneyMilestoneKind.STREAK,
                title="Seven-day study streak",
                message="You studied for seven days in a row.",
                reached_at=inputs.as_of,
            )
        )
    for item in provided:
        milestones.append(
            JourneyMilestone(
                kind=item.kind,
                title=item.title.strip(),
                message=item.description.strip(),
                reached_at=item.reached_at,
            )
        )
    # Deterministic de-duplication by kind+title, preserving order.
    seen: set[tuple[str, str]] = set()
    unique: list[JourneyMilestone] = []
    for milestone in milestones:
        key = (milestone.kind.value, milestone.title)
        if key in seen:
            continue
        seen.add(key)
        unique.append(milestone)
    fallback = datetime.min.replace(tzinfo=inputs.as_of.tzinfo)
    unique.sort(key=lambda item: item.reached_at or fallback)
    return MilestoneCard(
        milestones=tuple(unique),
        headline="Milestones",
        has_milestones=bool(unique),
    )


def compose_learning_trends(
    inputs: JourneyInputs,
    *,
    consistency: ConsistencyCard,
) -> LearningTrendCard:
    """Compose historical trends only — never forecasts."""
    mastery_values = tuple(
        assessment.overall_mastery.magnitude
        for assessment in _sorted_assessments(inputs.assessment_history)
    )
    confidence_values = tuple(
        assessment.overall_confidence.score.magnitude
        for assessment in _sorted_assessments(inputs.assessment_history)
    )
    mastery_trend = trend_from_deltas(mastery_values)
    confidence_trend = trend_from_deltas(confidence_values)
    consistency_trend = _consistency_trend(inputs)
    completion_trend = _mission_completion_trend(inputs)
    has_data = (
        mastery_trend is not TrendDirection.UNKNOWN
        or confidence_trend is not TrendDirection.UNKNOWN
        or consistency_trend is not TrendDirection.UNKNOWN
        or completion_trend is not TrendDirection.UNKNOWN
        or consistency.has_consistency_data
    )
    return LearningTrendCard(
        mastery_trend=mastery_trend,
        mastery_trend_message=trend_message(mastery_trend, subject="mastery"),
        confidence_trend=confidence_trend,
        confidence_trend_message=trend_message(confidence_trend, subject="confidence"),
        consistency_trend=consistency_trend,
        consistency_trend_message=trend_message(
            consistency_trend, subject="consistency"
        ),
        mission_completion_trend=completion_trend,
        mission_completion_trend_message=trend_message(
            completion_trend, subject="mission completion"
        ),
        has_trend_data=has_data,
    )


def compose_achievement_timeline(milestones: MilestoneCard) -> AchievementTimeline:
    """Project milestones into a chronological achievement timeline."""
    items: list[AchievementTimelineItem] = []
    for index, milestone in enumerate(milestones.milestones):
        if milestone.reached_at is None:
            continue
        items.append(
            AchievementTimelineItem(
                achievement_id=f"milestone:{milestone.kind.value}:{index}",
                title=milestone.title,
                description=milestone.message,
                earned_at=milestone.reached_at,
                category=milestone.kind.value,
            )
        )
    items.sort(key=lambda item: item.earned_at)
    return AchievementTimeline(
        items=tuple(items),
        headline="Achievements",
        has_items=bool(items),
    )


def compose_weekly_summary(inputs: JourneyInputs) -> WeeklySummary:
    """Compose a weekly historical summary ending at ``as_of``."""
    today = inputs.as_of.date()
    week_start = today - timedelta(days=6)
    missions = _completed_missions_between(inputs.execution_history, week_start, today)
    sessions = _completed_sessions_between(inputs.schedule_history, week_start, today)
    minutes = _study_minutes_between(inputs, week_start, today)
    days = len(
        {
            day
            for day in _study_days(inputs)
            if week_start <= day <= today
        }
    )
    if missions or sessions or minutes > 0:
        message = (
            f"This week you completed {count_phrase(missions, 'mission')} "
            f"across {count_phrase(days, 'study day')}."
        )
    else:
        message = "No study activity recorded this week yet."
    return WeeklySummary(
        week_start=week_start,
        week_end=today,
        missions_completed=missions,
        sessions_completed=sessions,
        study_minutes=minutes,
        study_days=days,
        summary_message=message,
    )


def compose_monthly_summary(inputs: JourneyInputs) -> MonthlySummary:
    """Compose a monthly historical summary ending at ``as_of``."""
    today = inputs.as_of.date()
    month_start = today - timedelta(days=29)
    missions = _completed_missions_between(inputs.execution_history, month_start, today)
    sessions = _completed_sessions_between(inputs.schedule_history, month_start, today)
    minutes = _study_minutes_between(inputs, month_start, today)
    days = len(
        {
            day
            for day in _study_days(inputs)
            if month_start <= day <= today
        }
    )
    if missions or sessions or minutes > 0:
        message = (
            f"This month you completed {count_phrase(missions, 'mission')} "
            f"across {count_phrase(days, 'study day')}."
        )
    else:
        message = "No study activity recorded this month yet."
    return MonthlySummary(
        month_start=month_start,
        month_end=today,
        missions_completed=missions,
        sessions_completed=sessions,
        study_minutes=minutes,
        study_days=days,
        summary_message=message,
    )


# ---------------------------------------------------------------------------
# Timeline helpers
# ---------------------------------------------------------------------------


def _timeline_from_executions(
    executions: tuple[MissionExecution, ...],
) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    for execution in executions:
        if execution.status is not _COMPLETED:
            continue
        occurred = execution.finished_at or execution.started_at
        if occurred is None:
            continue
        scope = humanise_identifier(
            execution.mission.competency_id
        ) or humanise_identifier(execution.mission.subject_id)
        if execution.mission.mission_type in _CHECKPOINT_TYPES:
            kind = TimelineEventKind.CHECKPOINT_COMPLETED
            message = f"Checkpoint completed{f' — {scope}' if scope else ''}."
            event_title = "Checkpoint completed"
        else:
            kind = TimelineEventKind.MISSION_COMPLETED
            message = f"Mission completed{f': {scope}' if scope else ''}."
            event_title = "Mission completed"
        events.append(
            TimelineEvent(
                kind=kind,
                occurred_at=occurred,
                title=event_title,
                message=message,
            )
        )
    return events


def _timeline_from_assessments(
    assessments: tuple[MasteryAssessment, ...],
) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    ordered = _sorted_assessments(assessments)
    previous: MasteryAssessment | None = None
    for assessment in ordered:
        if previous is not None:
            delta = (
                assessment.overall_mastery.magnitude
                - previous.overall_mastery.magnitude
            )
            if delta > 0.02:
                events.append(
                    TimelineEvent(
                        kind=TimelineEventKind.MASTERY_IMPROVED,
                        occurred_at=assessment.assessed_at,
                        title="Mastery improved",
                        message="Your overall mastery improved.",
                    )
                )
            improved = _competencies_strengthened(previous, assessment)
            for label in improved:
                events.append(
                    TimelineEvent(
                        kind=TimelineEventKind.COMPETENCY_STRENGTHENED,
                        occurred_at=assessment.assessed_at,
                        title="Competency strengthened",
                        message=f"{label} strengthened.",
                    )
                )
        previous = assessment
    return events


def _timeline_from_recommendations(recommendation_history) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    ordered = sorted(recommendation_history, key=lambda item: item.recommended_at)
    previous_signature: str | None = None
    for recommendation_set in ordered:
        top = recommendation_set.highest_priority()
        signature = ""
        if top is not None:
            subject = (
                str(top.target.subject_id) if top.target.subject_id is not None else ""
            )
            competency = (
                str(top.target.competency_id)
                if top.target.competency_id is not None
                else ""
            )
            signature = f"{top.category.value}:{subject}:{competency}"
        if previous_signature is not None and signature != previous_signature:
            label = humanise_identifier(competency or subject) if top else "focus"
            events.append(
                TimelineEvent(
                    kind=TimelineEventKind.RECOMMENDATION_CHANGED,
                    occurred_at=recommendation_set.recommended_at,
                    title="Recommendation changed",
                    message=(
                        "Your study focus changed"
                        f"{f' to {label}' if label else ''}."
                    ),
                )
            )
        previous_signature = signature
    return events


def _timeline_from_schedules(
    schedules: tuple[StudySchedule, ...],
) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    for schedule in schedules:
        for session in schedule.sessions:
            if session.status in (SessionStatus.CANCELLED, SessionStatus.RESCHEDULED):
                continue
            occurred = datetime.combine(session.session_date, session.start_time)
            if schedule.generated_at.tzinfo is not None and occurred.tzinfo is None:
                occurred = occurred.replace(tzinfo=schedule.generated_at.tzinfo)
            count = len(session.scheduled_mission_ids)
            if count <= 0:
                continue
            events.append(
                TimelineEvent(
                    kind=TimelineEventKind.MISSION_SCHEDULED,
                    occurred_at=occurred,
                    title="Mission scheduled",
                    message=(
                        f"{count_phrase(count, 'mission')} scheduled "
                        f"for {session.session_date.isoformat()}."
                    ),
                )
            )
    return events


def _timeline_from_evaluations(evaluation_history) -> list[TimelineEvent]:
    events: list[TimelineEvent] = []
    for evaluation in evaluation_history:
        if not evaluation.success or evaluation.summary is None:
            continue
        events.append(
            TimelineEvent(
                kind=TimelineEventKind.EVALUATION_RECORDED,
                occurred_at=evaluation.summary.evaluated_at,
                title="Learning checkpoint recorded",
                message="A learning checkpoint was recorded.",
            )
        )
    return events


# ---------------------------------------------------------------------------
# Scalar helpers
# ---------------------------------------------------------------------------


def _sorted_assessments(
    assessments: tuple[MasteryAssessment, ...],
) -> list[MasteryAssessment]:
    return sorted(assessments, key=lambda item: item.assessed_at)


def _completed_executions(
    executions: tuple[MissionExecution, ...],
) -> list[MissionExecution]:
    return [
        execution
        for execution in executions
        if execution.status is _COMPLETED
    ]


def _completed_count(inputs: JourneyInputs) -> int:
    if inputs.study_statistics is not None:
        return inputs.study_statistics.completed_missions
    return len(_completed_executions(inputs.execution_history))


def _completed_missions_between(
    executions: tuple[MissionExecution, ...],
    start: date,
    end: date,
) -> int:
    count = 0
    for execution in _completed_executions(executions):
        occurred = execution.finished_at or execution.started_at
        if occurred is None:
            continue
        day = occurred.date()
        if start <= day <= end:
            count += 1
    return count


def _completed_sessions_between(
    schedules: tuple[StudySchedule, ...],
    start: date,
    end: date,
) -> int:
    count = 0
    for schedule in schedules:
        for session in schedule.sessions:
            if session.status is not SessionStatus.COMPLETED:
                continue
            if start <= session.session_date <= end:
                count += 1
    return count


def _study_minutes_between(
    inputs: JourneyInputs,
    start: date,
    end: date,
) -> float:
    minutes = 0.0
    for execution in inputs.execution_history:
        occurred = execution.finished_at or execution.started_at
        if occurred is None:
            continue
        day = occurred.date()
        if start <= day <= end:
            minutes += max(execution.elapsed_study_time_seconds, 0.0) / 60.0
    if minutes <= 0.0 and inputs.study_statistics is not None:
        # Fall back to proportional share of supplied totals when history is empty.
        stats = inputs.study_statistics
        if stats.study_day_count > 0 and stats.total_study_minutes > 0:
            span_days = (end - start).days + 1
            share = min(span_days / max(stats.study_day_count, 1), 1.0)
            minutes = stats.total_study_minutes * share
    return round(minutes, 2)


def _mastery_delta_between(
    assessments: tuple[MasteryAssessment, ...],
    start: date,
    end: date,
) -> float | None:
    ordered = [
        assessment
        for assessment in _sorted_assessments(assessments)
        if start <= assessment.assessed_at.date() <= end
    ]
    if len(ordered) < 2:
        # Compare nearest before-window vs latest in/after window when possible.
        before = [
            assessment
            for assessment in _sorted_assessments(assessments)
            if assessment.assessed_at.date() < start
        ]
        in_window = [
            assessment
            for assessment in _sorted_assessments(assessments)
            if start <= assessment.assessed_at.date() <= end
        ]
        if before and in_window:
            return round(
                in_window[-1].overall_mastery.magnitude
                - before[-1].overall_mastery.magnitude,
                4,
            )
        return None
    return round(
        ordered[-1].overall_mastery.magnitude - ordered[0].overall_mastery.magnitude,
        4,
    )


def _growth_message(
    *,
    period: str,
    missions: int,
    mastery_delta: float | None,
) -> str:
    if missions <= 0 and mastery_delta is None:
        return f"{period.capitalize()}ly growth will appear as you complete study work."
    parts: list[str] = []
    if missions > 0:
        parts.append(
            f"You've completed {count_phrase(missions, 'mission')} this {period}."
        )
    if mastery_delta is not None and mastery_delta > 0:
        parts.append("Your mastery improved over this period.")
    elif mastery_delta is not None and mastery_delta < 0:
        parts.append("Your mastery softened over this period.")
    elif mastery_delta is not None:
        parts.append("Your mastery held steady over this period.")
    return " ".join(parts)


def _study_days(inputs: JourneyInputs) -> set[date]:
    days: set[date] = set()
    for execution in inputs.execution_history:
        if execution.status not in (
            _COMPLETED,
            ExecutionStatus.STARTED,
            ExecutionStatus.RESUMED,
            ExecutionStatus.PAUSED,
        ):
            continue
        occurred = (
            execution.finished_at
            or execution.started_at
            or execution.last_active_at
        )
        if occurred is not None:
            days.add(occurred.date())
    for schedule in inputs.schedule_history:
        for session in schedule.sessions:
            if session.status in (
                SessionStatus.COMPLETED,
                SessionStatus.IN_PROGRESS,
            ):
                days.add(session.session_date)
            elif (
                session.status is SessionStatus.PLANNED
                and session.session_date <= inputs.as_of.date()
            ):
                # Planned past sessions do not count as studied.
                continue
    return days


def _current_streak(study_days: set[date], today: date) -> int:
    if not study_days:
        return 0
    cursor = today
    if cursor not in study_days:
        cursor = today - timedelta(days=1)
        if cursor not in study_days:
            return 0
    streak = 0
    while cursor in study_days:
        streak += 1
        cursor -= timedelta(days=1)
        if streak > 366:
            break
    return streak


def _longest_streak(study_days: set[date]) -> int:
    if not study_days:
        return 0
    ordered = sorted(study_days)
    longest = 1
    current = 1
    for index in range(1, len(ordered)):
        if ordered[index] == ordered[index - 1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def _average_weekly_sessions(inputs: JourneyInputs, today: date) -> float:
    stats = inputs.study_statistics
    if stats is not None and stats.total_sessions > 0:
        weeks = max(stats.study_day_count / 7.0, 1.0)
        return round(stats.total_sessions / weeks, 2)
    window_start = today - timedelta(days=27)
    sessions = 0
    for schedule in inputs.schedule_history:
        for session in schedule.sessions:
            if session.status not in (
                SessionStatus.COMPLETED,
                SessionStatus.IN_PROGRESS,
            ):
                continue
            if window_start <= session.session_date <= today:
                sessions += 1
    if sessions == 0:
        # Count completed executions as session proxies.
        sessions = _completed_missions_between(
            inputs.execution_history, window_start, today
        )
    return round(sessions / 4.0, 2)


def _completion_rate_percent(inputs: JourneyInputs) -> float:
    if inputs.study_statistics is not None:
        stats = inputs.study_statistics
        total = stats.completed_missions + stats.abandoned_missions
        if total > 0:
            return round(100.0 * stats.completed_missions / total, 2)
    completed = 0
    abandoned = 0
    for execution in inputs.execution_history:
        if execution.status is _COMPLETED:
            completed += 1
        elif execution.status is _ABANDONED:
            abandoned += 1
    total = completed + abandoned
    if total <= 0:
        return 0.0
    return round(100.0 * completed / total, 2)


def _frequency_message(avg_weekly: float, study_days: set[date]) -> str:
    if avg_weekly <= 0 and not study_days:
        return "Study frequency will appear as you build a study rhythm."
    if avg_weekly >= 5:
        return "You study frequently each week."
    if avg_weekly >= 2:
        return "You study a few times each week."
    if study_days:
        return f"You've studied on {count_phrase(len(study_days), 'day')} so far."
    return "Study frequency will appear as you build a study rhythm."


def _consistency_message(
    current_streak: int, longest_streak: int, completion_rate: float
) -> str:
    if current_streak >= 3:
        return f"You're on a {current_streak}-day study streak — keep going."
    if longest_streak >= 3:
        return f"Your longest streak is {longest_streak} days."
    if completion_rate >= 80:
        return "Your completion reliability is strong."
    if completion_rate > 0:
        return "You're building consistency one session at a time."
    return "Consistency will appear as you complete study work."


def _preferred_hour(inputs: JourneyInputs) -> int | None:
    hours: list[int] = []
    for execution in inputs.execution_history:
        started = execution.started_at
        if started is not None:
            hours.append(started.hour)
    for schedule in inputs.schedule_history:
        for session in schedule.sessions:
            if session.status in (
                SessionStatus.COMPLETED,
                SessionStatus.IN_PROGRESS,
                SessionStatus.PLANNED,
            ):
                hours.append(session.start_time.hour)
    if not hours:
        return None
    counts = Counter(hours)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _most_productive_weekday(inputs: JourneyInputs) -> int | None:
    weekdays: list[int] = []
    for execution in _completed_executions(inputs.execution_history):
        occurred = execution.finished_at or execution.started_at
        if occurred is not None:
            weekdays.append(occurred.weekday())
    for schedule in inputs.schedule_history:
        for session in schedule.sessions:
            if session.status is SessionStatus.COMPLETED:
                weekdays.append(session.session_date.weekday())
    if not weekdays:
        return None
    counts = Counter(weekdays)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _average_session_minutes(inputs: JourneyInputs) -> float:
    stats = inputs.study_statistics
    if stats is not None and stats.average_session_minutes > 0:
        return stats.average_session_minutes
    durations: list[float] = []
    for execution in inputs.execution_history:
        if execution.elapsed_study_time_seconds > 0:
            durations.append(execution.elapsed_study_time_seconds / 60.0)
    for schedule in inputs.schedule_history:
        for session in schedule.sessions:
            if session.status is SessionStatus.COMPLETED:
                durations.append(float(session.estimated_duration_minutes))
    if not durations:
        return 0.0
    return round(sum(durations) / len(durations), 2)


def _reliability_message(percent: float) -> str:
    if percent <= 0:
        return "Completion reliability will appear as you finish missions."
    if percent >= 85:
        return "You finish most missions you start."
    if percent >= 60:
        return "You complete a solid share of the missions you start."
    return "Finishing started missions will strengthen your reliability."


def _mission_quality_message(inputs: JourneyInputs) -> str:
    completed = _completed_executions(inputs.execution_history)
    if not completed:
        return "Mission completion quality will appear after you finish missions."
    rates: list[float] = []
    for execution in completed:
        total_steps = len(execution.mission.steps)
        if total_steps <= 0:
            continue
        rates.append(100.0 * len(execution.completed_step_ids) / total_steps)
    if not rates:
        return "You've completed missions — keep building quality."
    average = sum(rates) / len(rates)
    if average >= 90:
        return "You complete missions with high step coverage."
    if average >= 70:
        return "You complete most mission steps."
    return "Completing more steps per mission will lift quality."


def _strongest_subject(
    assessments: tuple[MasteryAssessment, ...],
) -> str | None:
    if not assessments:
        return None
    latest = _sorted_assessments(assessments)[-1]
    if not latest.subject_assessments:
        return None
    strongest = max(
        latest.subject_assessments,
        key=lambda subject: subject.mastery.magnitude,
    )
    return humanise_identifier(str(strongest.subject_id)) or None


def _most_improved_competency(
    assessments: tuple[MasteryAssessment, ...],
) -> str | None:
    ordered = _sorted_assessments(assessments)
    if len(ordered) < 2:
        return None
    first = ordered[0]
    last = ordered[-1]
    best_label: str | None = None
    best_delta = 0.0
    first_map = _competency_magnitudes(first)
    last_map = _competency_magnitudes(last)
    for competency_id, magnitude in last_map.items():
        prior = first_map.get(competency_id)
        if prior is None:
            continue
        delta = magnitude - prior
        if delta > best_delta:
            best_delta = delta
            best_label = humanise_identifier(competency_id)
    return best_label if best_delta > 0.02 else None


def _competency_magnitudes(assessment: MasteryAssessment) -> dict[str, float]:
    values: dict[str, float] = {}
    for subject in assessment.subject_assessments:
        for competency in subject.competency_assessments:
            values[str(competency.competency_id)] = competency.mastery.magnitude
    return values


def _competencies_strengthened(
    previous: MasteryAssessment,
    current: MasteryAssessment,
) -> list[str]:
    before = _competency_magnitudes(previous)
    after = _competency_magnitudes(current)
    strengthened: list[str] = []
    for competency_id, magnitude in after.items():
        prior = before.get(competency_id)
        if prior is not None and magnitude - prior > 0.05:
            strengthened.append(humanise_identifier(competency_id))
    return strengthened[:3]


def _momentum_message(
    streak: int,
    weekly_missions: int,
    home_snapshot,
) -> str:
    if weekly_missions > 0:
        return (
            f"You've completed {count_phrase(weekly_missions, 'mission')} this week."
        )
    if streak > 0:
        return f"You're on a {streak}-day study streak."
    if home_snapshot is not None and home_snapshot.momentum_message:
        return home_snapshot.momentum_message
    return "Learning momentum will appear as you study."


def _consistency_trend(inputs: JourneyInputs) -> TrendDirection:
    today = inputs.as_of.date()
    recent_start = today - timedelta(days=13)
    prior_start = today - timedelta(days=27)
    prior_end = today - timedelta(days=14)
    recent_days = {
        day for day in _study_days(inputs) if recent_start <= day <= today
    }
    prior_days = {
        day for day in _study_days(inputs) if prior_start <= day <= prior_end
    }
    if not recent_days and not prior_days:
        return TrendDirection.UNKNOWN
    return trend_from_deltas(
        (float(len(prior_days)), float(len(recent_days))),
        epsilon=0.5,
    )


def _mission_completion_trend(inputs: JourneyInputs) -> TrendDirection:
    today = inputs.as_of.date()
    recent = _completed_missions_between(
        inputs.execution_history, today - timedelta(days=13), today
    )
    prior = _completed_missions_between(
        inputs.execution_history,
        today - timedelta(days=27),
        today - timedelta(days=14),
    )
    if recent == 0 and prior == 0:
        return TrendDirection.UNKNOWN
    return trend_from_deltas((float(prior), float(recent)), epsilon=0.5)
