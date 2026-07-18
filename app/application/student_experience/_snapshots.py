"""Domain → DTO snapshot mappers for Student Experience."""

from __future__ import annotations

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import (
    AchievementSnapshot,
    CompletedSessionSnapshot,
    HistorySnapshot,
    ReadinessPointSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.profile_snapshot import (
    AccountSettingsSnapshot,
    LearningGoalSnapshot,
    LearningStatisticsSnapshot,
    ProfileSnapshot,
    StudyPreferencesSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.domain.student_experience.experience_session import StartSessionAction
from app.domain.student_experience.history_projection import HistoryProjection
from app.domain.student_experience.journey_projection import (
    JourneyProjection,
    JourneyTopicCard,
)
from app.domain.student_experience.profile_projection import ProfileProjection
from app.domain.student_experience.recommendation_explanation import (
    RecommendationExplanation,
)
from app.domain.student_experience.revision_projection import (
    RevisionOption,
    RevisionProjection,
)
from app.domain.student_experience.student_home import StudentHome


def explanation_snapshot(
    explanation: RecommendationExplanation | None,
) -> ExplanationSnapshot | None:
    if explanation is None:
        return None
    return ExplanationSnapshot(
        summary=explanation.summary,
        why_recommended=explanation.why_recommended,
        evidence_points=explanation.evidence_points,
        expected_benefit=explanation.expected_benefit,
        confidence_label=explanation.confidence_label,
        is_complete=explanation.is_complete,
    )


def start_session_snapshot(
    action: StartSessionAction | None,
) -> StartSessionActionSnapshot | None:
    if action is None:
        return None
    return StartSessionActionSnapshot(
        label=action.label,
        enabled=action.enabled,
        can_start=action.can_start,
        mission_id=action.mission_id,
        session_id=action.session_id,
        estimated_minutes=action.estimated_minutes,
        topic_title=action.topic_title,
    )


def home_snapshot(home: StudentHome) -> HomeSnapshot:
    return HomeSnapshot(
        student_id=home.student_id,
        greeting=home.greeting,
        examination_label=home.examination_label,
        exam_countdown_days=home.exam_countdown_days,
        exam_readiness=home.exam_readiness,
        exam_readiness_label=home.exam_readiness_label,
        recommendation_title=home.recommendation_title,
        recommendation_summary=home.recommendation_summary,
        estimated_study_minutes=home.estimated_study_minutes,
        expected_readiness_improvement=home.expected_readiness_improvement,
        explanation=explanation_snapshot(home.explanation),
        start_session=start_session_snapshot(home.start_session),
        has_recommendation=home.has_recommendation,
        can_start_session=home.can_start_session,
        metadata=home.metadata,
    )


def _topic_snapshot(card: JourneyTopicCard) -> JourneyTopicSnapshot:
    return JourneyTopicSnapshot(
        topic_id=card.topic_id,
        title=card.title,
        status_label=card.status_label,
        prerequisite_note=card.prerequisite_note,
    )


def journey_snapshot(projection: JourneyProjection) -> JourneySnapshot:
    return JourneySnapshot(
        student_id=projection.student_id,
        current_topic=(
            None
            if projection.current_topic is None
            else _topic_snapshot(projection.current_topic)
        ),
        completed_topics=tuple(
            _topic_snapshot(t) for t in projection.completed_topics
        ),
        upcoming_topics=tuple(
            _topic_snapshot(t) for t in projection.upcoming_topics
        ),
        overall_progress_ratio=projection.overall_progress_ratio,
        progress_percent=projection.progress_percent,
        estimated_completion_label=projection.estimated_completion_label,
        prerequisite_visibility=projection.prerequisite_visibility,
        examination_label=projection.examination_label,
        completed_count=projection.completed_count,
        upcoming_count=projection.upcoming_count,
    )


def _revision_option_snapshot(option: RevisionOption) -> RevisionOptionSnapshot:
    return RevisionOptionSnapshot(
        option_id=option.option_id,
        topic_title=option.topic_title,
        priority_label=option.priority_label,
        estimated_study_minutes=option.estimated_study_minutes,
        expected_benefit=option.expected_benefit,
        explanation=explanation_snapshot(option.explanation),
        is_primary=option.is_primary,
    )


def revision_snapshot(projection: RevisionProjection) -> RevisionSnapshot:
    return RevisionSnapshot(
        student_id=projection.student_id,
        primary=(
            None
            if projection.primary is None
            else _revision_option_snapshot(projection.primary)
        ),
        alternatives=tuple(
            _revision_option_snapshot(o) for o in projection.alternatives
        ),
        empty_message=projection.empty_message,
        has_revision=projection.has_revision,
        option_count=projection.option_count,
    )


def history_snapshot(projection: HistoryProjection) -> HistorySnapshot:
    return HistorySnapshot(
        student_id=projection.student_id,
        completed_sessions=tuple(
            CompletedSessionSnapshot(
                session_id=s.session_id,
                topic_title=s.topic_title,
                completed_at=s.completed_at,
                study_minutes=s.study_minutes,
            )
            for s in projection.completed_sessions
        ),
        total_study_minutes=projection.total_study_minutes,
        readiness_progression=tuple(
            ReadinessPointSnapshot(
                recorded_at=p.recorded_at,
                exam_readiness=p.exam_readiness,
                label=p.label,
            )
            for p in projection.readiness_progression
        ),
        mastered_topics=projection.mastered_topics,
        revision_history=projection.revision_history,
        recent_achievements=tuple(
            AchievementSnapshot(
                achievement_id=a.achievement_id,
                title=a.title,
                earned_at=a.earned_at,
                description=a.description,
            )
            for a in projection.recent_achievements
        ),
        session_count=projection.session_count,
        mastered_count=projection.mastered_count,
    )


def profile_snapshot(projection: ProfileProjection) -> ProfileSnapshot:
    prefs = projection.preferences
    stats = projection.statistics
    account = projection.account
    return ProfileSnapshot(
        student_id=projection.student_id,
        display_name=projection.display_name,
        examination_label=projection.examination_label,
        preferences=StudyPreferencesSnapshot(
            preferred_session_minutes=prefs.preferred_session_minutes,
            preferred_study_days=prefs.preferred_study_days,
            reminder_enabled=prefs.reminder_enabled,
            quiet_hours_label=prefs.quiet_hours_label,
        ),
        statistics=LearningStatisticsSnapshot(
            total_study_minutes=stats.total_study_minutes,
            sessions_completed=stats.sessions_completed,
            topics_mastered=stats.topics_mastered,
            current_exam_readiness=stats.current_exam_readiness,
            study_streak_days=stats.study_streak_days,
        ),
        goals=tuple(
            LearningGoalSnapshot(
                goal_id=g.goal_id,
                title=g.title,
                target_label=g.target_label,
                progress_ratio=g.progress_ratio,
            )
            for g in projection.goals
        ),
        account=AccountSettingsSnapshot(
            email=account.email,
            notifications_enabled=account.notifications_enabled,
            locale=account.locale,
            timezone=account.timezone,
        ),
    )
