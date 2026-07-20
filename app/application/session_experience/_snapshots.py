"""Map domain projections to immutable application DTOs."""

from __future__ import annotations

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
    ReturnHomeActionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import (
    BeginSessionActionSnapshot,
    OverviewSnapshot,
)
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.domain.session_experience.activity_projection import ActivityProjection
from app.domain.session_experience.completion_projection import CompletionProjection
from app.domain.session_experience.learning_session import LearningSession
from app.domain.session_experience.reflection_projection import ReflectionProjection
from app.domain.session_experience.session_progress import SessionProgress


def overview_snapshot(session: LearningSession) -> OverviewSnapshot:
    action = None
    if session.begin_action is not None:
        action = BeginSessionActionSnapshot(
            label=session.begin_action.label,
            enabled=session.begin_action.enabled,
            can_begin=session.begin_action.can_begin,
            session_id=session.begin_action.session_id,
            mission_id=session.begin_action.mission_id,
        )
    return OverviewSnapshot(
        experience_session_id=session.experience_session_id,
        student_id=session.student_id,
        session_id=session.session_id,
        status=session.status.value,
        objective=session.objective,
        learning_goal=session.learning_goal,
        estimated_minutes=session.estimated_minutes,
        activity_count=session.activity_count,
        topics=session.topics,
        topic_count=session.topic_count,
        expected_readiness_improvement=session.expected_readiness_improvement,
        why_studying=session.why_studying,
        begin_action=action,
        can_begin=session.can_begin,
        metadata=session.metadata,
    )


def progress_snapshot(progress: SessionProgress) -> ProgressSnapshot:
    return ProgressSnapshot(
        session_id=progress.session_id,
        activities_completed=progress.activities_completed,
        activities_remaining=progress.activities_remaining,
        activities_total=progress.activities_total,
        estimated_remaining_minutes=progress.estimated_remaining_minutes,
        current_topic=progress.current_topic,
        overall_progress=progress.overall_progress,
        progress_percent=progress.progress_percent,
        is_complete=progress.is_complete,
        has_started=progress.has_started,
        metadata=progress.metadata,
    )


def activity_snapshot(activity: ActivityProjection) -> ActivitySnapshot:
    return ActivitySnapshot(
        activity_id=activity.activity_id,
        session_id=activity.session_id,
        question=activity.question,
        context=activity.context,
        supporting_material=activity.supporting_material,
        hints=activity.hints,
        answer_prompt=activity.answer_prompt,
        explanation=activity.explanation,
        phase=activity.phase.value,
        activity_index=activity.activity_index,
        activities_total=activity.activities_total,
        next_action_label=activity.next_action_label,
        topic_title=activity.topic_title,
        has_hints=activity.has_hints,
        has_explanation=activity.has_explanation,
        is_final_activity=activity.is_final_activity,
        metadata=activity.metadata,
    )


def reflection_snapshot(reflection: ReflectionProjection) -> ReflectionSnapshot:
    return ReflectionSnapshot(
        session_id=reflection.session_id,
        key_insight=reflection.key_insight,
        concept_confidence=reflection.concept_confidence,
        suggested_improvement=reflection.suggested_improvement,
        reflection_prompt=reflection.reflection_prompt,
        topic_title=reflection.topic_title,
        next_action_label=reflection.next_action_label,
        has_insight=reflection.has_insight,
        is_complete=reflection.is_complete,
        metadata=reflection.metadata,
    )


def completion_snapshot(completion: CompletionProjection) -> CompletionSnapshot:
    home = None
    if completion.return_home is not None:
        home = ReturnHomeActionSnapshot(
            label=completion.return_home.label,
            enabled=completion.return_home.enabled,
        )
    return CompletionSnapshot(
        session_id=completion.session_id,
        student_id=completion.student_id,
        topics_completed=completion.topics_completed,
        topic_count=completion.topic_count,
        time_studied_minutes=completion.time_studied_minutes,
        activities_completed=completion.activities_completed,
        learning_insights=completion.learning_insights,
        exam_readiness_change=completion.exam_readiness_change,
        exam_readiness_change_label=completion.exam_readiness_change_label,
        next_recommendation=completion.next_recommendation,
        estimated_next_session_minutes=completion.estimated_next_session_minutes,
        return_home=home,
        has_readiness_change=completion.has_readiness_change,
        can_return_home=completion.can_return_home,
        metadata=completion.metadata,
    )
