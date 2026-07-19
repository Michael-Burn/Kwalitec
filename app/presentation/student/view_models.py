"""Presentation view models for Student Experience surfaces.

Formatting and labels only. Never compute readiness, recommendations,
missions, or journeys — those arrive from application snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.student_experience.dashboard_service import (
    DashboardSnapshot,
    NavigationItemSnapshot,
)
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
from app.presentation.student.navigation import StudentNavItem, build_navigation

# Terms that must never appear in learner-facing copy.
FORBIDDEN_LEARNER_TERMS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "graph node",
    "graph edge",
)


@dataclass(frozen=True)
class ExplanationViewModel:
    summary: str = ""
    why_recommended: str = ""
    evidence_points: tuple[str, ...] = ()
    expected_benefit: str = ""
    confidence_label: str = ""
    is_complete: bool = False
    has_content: bool = False


@dataclass(frozen=True)
class RecommendationCardViewModel:
    title: str = ""
    summary: str = ""
    benefit_label: str = ""
    time_label: str = ""
    reason: str = ""
    cta_label: str = "Start Today's Session"
    cta_enabled: bool = False
    has_recommendation: bool = False


@dataclass(frozen=True)
class ReadinessCardViewModel:
    readiness_label: str = ""
    readiness_percent_label: str = ""
    trend_label: str = ""
    confidence_label: str = ""
    has_readiness: bool = False


@dataclass(frozen=True)
class CountdownCardViewModel:
    days: int | None = None
    label: str = ""
    examination_label: str = ""
    has_countdown: bool = False


@dataclass(frozen=True)
class JourneyTopicViewModel:
    topic_id: str = ""
    title: str = ""
    status_label: str = ""
    prerequisite_note: str = ""


@dataclass(frozen=True)
class JourneyCardViewModel:
    current_topic_title: str = ""
    progress_percent: int = 0
    progress_label: str = ""
    next_topic_title: str = ""
    estimated_completion_label: str = ""
    has_journey: bool = False


@dataclass(frozen=True)
class JourneyPageViewModel:
    examination_label: str = ""
    current: JourneyTopicViewModel | None = None
    completed: tuple[JourneyTopicViewModel, ...] = ()
    upcoming: tuple[JourneyTopicViewModel, ...] = ()
    progress_percent: int = 0
    progress_label: str = ""
    estimated_completion_label: str = ""
    prerequisite_notes: tuple[str, ...] = ()
    completed_count: int = 0
    upcoming_count: int = 0
    primary_cta_label: str = "Continue Journey"
    primary_cta_enabled: bool = False


@dataclass(frozen=True)
class RevisionOptionViewModel:
    option_id: str = ""
    topic_title: str = ""
    priority_label: str = ""
    time_label: str = ""
    expected_benefit: str = ""
    explanation: ExplanationViewModel | None = None
    is_primary: bool = False


@dataclass(frozen=True)
class RevisionPageViewModel:
    primary: RevisionOptionViewModel | None = None
    alternatives: tuple[RevisionOptionViewModel, ...] = ()
    empty_message: str = ""
    has_revision: bool = False
    option_count: int = 0
    primary_cta_label: str = "Begin Revision"
    primary_cta_enabled: bool = False


@dataclass(frozen=True)
class HistorySessionViewModel:
    session_id: str = ""
    topic_title: str = ""
    completed_at: str = ""
    duration_label: str = ""
    outcome_label: str = "Completed"


@dataclass(frozen=True)
class HistoryPageViewModel:
    sessions: tuple[HistorySessionViewModel, ...] = ()
    total_study_label: str = ""
    readiness_points: tuple[tuple[str, str], ...] = ()
    mastered_topics: tuple[str, ...] = ()
    revision_history: tuple[str, ...] = ()
    achievements: tuple[AchievementSnapshot, ...] = ()
    session_count: int = 0
    mastered_count: int = 0
    readiness_trend_label: str = ""
    primary_cta_label: str = "Return Home"
    primary_cta_enabled: bool = True


@dataclass(frozen=True)
class ProfilePageViewModel:
    display_name: str = ""
    examination_label: str = ""
    preferences: StudyPreferencesSnapshot = field(
        default_factory=StudyPreferencesSnapshot
    )
    statistics: LearningStatisticsSnapshot = field(
        default_factory=LearningStatisticsSnapshot
    )
    goals: tuple[LearningGoalSnapshot, ...] = ()
    account: AccountSettingsSnapshot = field(
        default_factory=AccountSettingsSnapshot
    )
    preferences_days_label: str = ""
    readiness_percent_label: str = ""
    total_study_label: str = ""
    primary_cta_label: str = "Update Study Preferences"
    primary_cta_enabled: bool = True
    primary_cta_endpoint: str = "settings.index"


@dataclass(frozen=True)
class HomePageViewModel:
    greeting: str = ""
    examination_label: str = ""
    countdown: CountdownCardViewModel = field(
        default_factory=CountdownCardViewModel
    )
    readiness: ReadinessCardViewModel = field(
        default_factory=ReadinessCardViewModel
    )
    recommendation: RecommendationCardViewModel = field(
        default_factory=RecommendationCardViewModel
    )
    explanation: ExplanationViewModel | None = None
    start_session: StartSessionActionSnapshot | None = None
    estimated_study_label: str = ""
    expected_benefit_label: str = ""
    can_start_session: bool = False
    primary_cta_label: str = "Start Today's Session"
    primary_cta_enabled: bool = False
    mission_id: str = ""
    session_id: str = ""


@dataclass(frozen=True)
class StudentShellViewModel:
    """Shared shell chrome for every student surface."""

    active_surface: str
    active_label: str
    navigation: tuple[StudentNavItem, ...]
    page_title: str
    page_eyebrow: str = "Your learning"
    page_description: str = ""
    learning_activity_status: str = ""


@dataclass(frozen=True)
class StudentPageViewModel:
    """Composite page payload passed to templates."""

    shell: StudentShellViewModel
    home: HomePageViewModel | None = None
    journey: JourneyPageViewModel | None = None
    revision: RevisionPageViewModel | None = None
    history: HistoryPageViewModel | None = None
    profile: ProfilePageViewModel | None = None


def format_minutes(minutes: int | None) -> str:
    """Format study minutes for display."""
    if minutes is None:
        return ""
    if minutes <= 0:
        return "Less than a minute"
    if minutes == 1:
        return "1 minute"
    if minutes < 60:
        return f"{minutes} minutes"
    hours, rem = divmod(minutes, 60)
    if rem == 0:
        return "1 hour" if hours == 1 else f"{hours} hours"
    hour_part = "1 hour" if hours == 1 else f"{hours} hours"
    return f"{hour_part} {rem} min"


def format_readiness_percent(value: float | None) -> str:
    """Format a readiness ratio (0–1 or 0–100) as a percent label."""
    if value is None:
        return ""
    ratio = float(value)
    if ratio <= 1.0:
        pct = int(round(ratio * 100))
    else:
        pct = int(round(ratio))
    return f"{pct}%"


def format_benefit(delta: float | None, fallback: str = "") -> str:
    """Format expected readiness improvement for display."""
    if fallback:
        return fallback
    if delta is None:
        return ""
    pct = abs(delta)
    if pct <= 1.0:
        pct = pct * 100
    return f"About {pct:.0f}% readiness gain"


def contains_forbidden_term(text: str) -> bool:
    """True when learner-facing copy leaks internal architecture terms."""
    lowered = (text or "").lower()
    return any(term in lowered for term in FORBIDDEN_LEARNER_TERMS)


def explanation_vm(
    snap: ExplanationSnapshot | None,
) -> ExplanationViewModel | None:
    if snap is None:
        return None
    return ExplanationViewModel(
        summary=snap.summary,
        why_recommended=snap.why_recommended,
        evidence_points=snap.evidence_points,
        expected_benefit=snap.expected_benefit,
        confidence_label=snap.confidence_label,
        is_complete=snap.is_complete,
        has_content=bool(
            snap.summary
            or snap.why_recommended
            or snap.evidence_points
            or snap.expected_benefit
        ),
    )


def home_vm(snap: HomeSnapshot) -> HomePageViewModel:
    start = snap.start_session
    cta_enabled = bool(snap.can_start_session and start and start.enabled)
    cta_label = (
        (start.label if start and start.label else "Start Today's Session")
        if cta_enabled
        else "Start Today's Session"
    )
    benefit = format_benefit(
        snap.expected_readiness_improvement,
        fallback=(
            snap.explanation.expected_benefit if snap.explanation else ""
        ),
    )
    return HomePageViewModel(
        greeting=snap.greeting or "Welcome back",
        examination_label=snap.examination_label,
        countdown=CountdownCardViewModel(
            days=snap.exam_countdown_days,
            label=_countdown_label(snap.exam_countdown_days),
            examination_label=snap.examination_label,
            has_countdown=snap.exam_countdown_days is not None,
        ),
        readiness=ReadinessCardViewModel(
            readiness_label=snap.exam_readiness_label or "Exam Readiness",
            readiness_percent_label=format_readiness_percent(
                snap.exam_readiness
            ),
            trend_label="",
            confidence_label=(
                snap.explanation.confidence_label if snap.explanation else ""
            ),
            has_readiness=snap.exam_readiness is not None,
        ),
        recommendation=RecommendationCardViewModel(
            title=snap.recommendation_title,
            summary=snap.recommendation_summary,
            benefit_label=benefit,
            time_label=format_minutes(snap.estimated_study_minutes),
            reason=(
                snap.explanation.why_recommended if snap.explanation else ""
            ),
            cta_label=cta_label,
            cta_enabled=cta_enabled,
            has_recommendation=snap.has_recommendation,
        ),
        explanation=explanation_vm(snap.explanation),
        start_session=start,
        estimated_study_label=format_minutes(snap.estimated_study_minutes),
        expected_benefit_label=benefit,
        can_start_session=snap.can_start_session,
        primary_cta_label=cta_label,
        primary_cta_enabled=cta_enabled,
        mission_id=(start.mission_id or "") if start else "",
        session_id=(start.session_id or "") if start else "",
    )


def journey_vm(snap: JourneySnapshot) -> JourneyPageViewModel:
    has_current = snap.current_topic is not None
    return JourneyPageViewModel(
        examination_label=snap.examination_label,
        current=_topic_vm(snap.current_topic) if snap.current_topic else None,
        completed=tuple(_topic_vm(t) for t in snap.completed_topics),
        upcoming=tuple(_topic_vm(t) for t in snap.upcoming_topics),
        progress_percent=snap.progress_percent,
        progress_label=f"{snap.progress_percent}% complete",
        estimated_completion_label=snap.estimated_completion_label,
        prerequisite_notes=snap.prerequisite_visibility,
        completed_count=snap.completed_count,
        upcoming_count=snap.upcoming_count,
        primary_cta_label="Continue with current topic"
        if has_current
        else "Explore your journey",
        primary_cta_enabled=has_current or bool(snap.upcoming_topics),
    )


def journey_card_vm(snap: JourneySnapshot) -> JourneyCardViewModel:
    next_topic = snap.upcoming_topics[0] if snap.upcoming_topics else None
    return JourneyCardViewModel(
        current_topic_title=(
            snap.current_topic.title if snap.current_topic else ""
        ),
        progress_percent=snap.progress_percent,
        progress_label=f"{snap.progress_percent}% complete",
        next_topic_title=next_topic.title if next_topic else "",
        estimated_completion_label=snap.estimated_completion_label,
        has_journey=bool(
            snap.current_topic or snap.completed_topics or snap.upcoming_topics
        ),
    )


def revision_vm(snap: RevisionSnapshot) -> RevisionPageViewModel:
    primary = _revision_option_vm(snap.primary) if snap.primary else None
    return RevisionPageViewModel(
        primary=primary,
        alternatives=tuple(_revision_option_vm(o) for o in snap.alternatives),
        empty_message=snap.empty_message
        or "No revision focus is ready yet. Check back after your next session.",
        has_revision=snap.has_revision,
        option_count=snap.option_count,
        primary_cta_label="Begin Revision",
        primary_cta_enabled=snap.has_revision and primary is not None,
    )


def history_vm(snap: HistorySnapshot) -> HistoryPageViewModel:
    points = tuple(
        (p.recorded_at, format_readiness_percent(p.exam_readiness) or p.label)
        for p in snap.readiness_progression
    )
    trend = _readiness_trend_label(snap.readiness_progression)
    return HistoryPageViewModel(
        sessions=tuple(_session_vm(s) for s in snap.completed_sessions),
        total_study_label=format_minutes(snap.total_study_minutes)
        or "No study time recorded yet",
        readiness_points=points,
        mastered_topics=snap.mastered_topics,
        revision_history=snap.revision_history,
        achievements=snap.recent_achievements,
        session_count=snap.session_count,
        mastered_count=snap.mastered_count,
        readiness_trend_label=trend,
        primary_cta_label="Return Home",
        primary_cta_enabled=True,
    )


def profile_vm(snap: ProfileSnapshot) -> ProfilePageViewModel:
    prefs = snap.preferences
    days = ", ".join(prefs.preferred_study_days) if prefs.preferred_study_days else ""
    return ProfilePageViewModel(
        display_name=snap.display_name,
        examination_label=snap.examination_label,
        preferences=prefs,
        statistics=snap.statistics,
        goals=snap.goals,
        account=snap.account,
        preferences_days_label=days,
        readiness_percent_label=format_readiness_percent(
            snap.statistics.current_exam_readiness
        ),
        total_study_label=format_minutes(snap.statistics.total_study_minutes),
        primary_cta_label="Open account settings",
        primary_cta_enabled=True,
        primary_cta_endpoint="settings.index",
    )


def shell_vm(
    *,
    active_surface: str,
    page_title: str,
    page_description: str = "",
    learning_activity_status: str = "",
    navigation: tuple[NavigationItemSnapshot, ...] | None = None,
) -> StudentShellViewModel:
    if navigation:
        nav = tuple(
            StudentNavItem(
                surface=item.surface,
                label=item.label,
                endpoint=f"student.{item.surface}",
                active=item.active,
            )
            for item in navigation
        )
    else:
        nav = build_navigation(active_surface)
    active_label = next(
        (item.label for item in nav if item.active),
        active_surface.title(),
    )
    return StudentShellViewModel(
        active_surface=active_surface,
        active_label=active_label,
        navigation=nav,
        page_title=page_title,
        page_eyebrow="Your learning",
        page_description=page_description,
        learning_activity_status=learning_activity_status,
    )


def page_from_dashboard(
    dash: DashboardSnapshot,
    *,
    surface: str,
) -> StudentPageViewModel:
    """Build a page view model from a dashboard snapshot for ``surface``."""
    descriptions = {
        "home": "What you should do next, and why.",
        "journey": "Where you are on the path to exam readiness.",
        "revision": "The highest-value revision for today.",
        "history": "Your educational progress over time.",
        "profile": "Examination, preferences, goals, and account.",
    }
    titles = {
        "home": "Home",
        "journey": "Journey",
        "revision": "Revision",
        "history": "History",
        "profile": "Profile",
    }
    shell = shell_vm(
        active_surface=surface,
        page_title=titles.get(surface, surface.title()),
        page_description=descriptions.get(surface, ""),
        learning_activity_status=dash.learning_activity_status,
        navigation=dash.navigation,
    )
    return StudentPageViewModel(
        shell=shell,
        home=home_vm(dash.home) if dash.home else None,
        journey=journey_vm(dash.journey) if dash.journey else None,
        revision=revision_vm(dash.revision) if dash.revision else None,
        history=history_vm(dash.history) if dash.history else None,
        profile=profile_vm(dash.profile) if dash.profile else None,
    )


def _topic_vm(topic: JourneyTopicSnapshot) -> JourneyTopicViewModel:
    return JourneyTopicViewModel(
        topic_id=topic.topic_id,
        title=topic.title,
        status_label=topic.status_label,
        prerequisite_note=topic.prerequisite_note,
    )


def _revision_option_vm(
    option: RevisionOptionSnapshot,
) -> RevisionOptionViewModel:
    return RevisionOptionViewModel(
        option_id=option.option_id,
        topic_title=option.topic_title,
        priority_label=option.priority_label,
        time_label=format_minutes(option.estimated_study_minutes),
        expected_benefit=option.expected_benefit,
        explanation=explanation_vm(option.explanation),
        is_primary=option.is_primary,
    )


def _session_vm(session: CompletedSessionSnapshot) -> HistorySessionViewModel:
    return HistorySessionViewModel(
        session_id=session.session_id,
        topic_title=session.topic_title,
        completed_at=session.completed_at,
        duration_label=format_minutes(session.study_minutes),
        outcome_label="Completed",
    )


def _countdown_label(days: int | None) -> str:
    if days is None:
        return ""
    if days < 0:
        return "Exam date passed"
    if days == 0:
        return "Exam is today"
    if days == 1:
        return "1 day until exam"
    return f"{days} days until exam"


def _readiness_trend_label(
    points: tuple[ReadinessPointSnapshot, ...],
) -> str:
    if len(points) < 2:
        return "Not enough history for a trend yet"
    first = points[0].exam_readiness
    last = points[-1].exam_readiness
    if last > first:
        return "Readiness is improving"
    if last < first:
        return "Readiness needs attention"
    return "Readiness is steady"
