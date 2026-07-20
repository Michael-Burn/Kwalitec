"""Presentation view models for Learning Session Experience surfaces.

Formatting and labels only. Never compute readiness, recommendations,
missions, evidence, or educational progress — those arrive from snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import OverviewSnapshot
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.facade import SessionFlowSnapshot
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.navigation import (
    SessionNavStep,
    build_session_steps,
    page_meta,
)

FORBIDDEN_LEARNER_TERMS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "graph node",
    "graph edge",
    "evidence spine",
    "mastery score",
)


@dataclass(frozen=True)
class SessionShellViewModel:
    session_id: str
    student_id: str
    active_surface: str
    page_eyebrow: str = ""
    page_title: str = ""
    page_description: str = ""
    steps: tuple[SessionNavStep, ...] = ()
    topic_title: str = ""


@dataclass(frozen=True)
class ProgressBarViewModel:
    percent: int = 0
    label: str = ""
    completed: int = 0
    remaining: int = 0
    total: int = 0
    current_topic: str = ""
    remaining_time_label: str = ""
    has_progress: bool = False


@dataclass(frozen=True)
class OverviewViewModel:
    objective: str = ""
    learning_goal: str = ""
    why_studying: str = ""
    estimated_duration_label: str = ""
    activity_count_label: str = ""
    topics: tuple[str, ...] = ()
    expected_improvement_label: str = ""
    begin_label: str = "Begin Session"
    begin_enabled: bool = False
    session_id: str = ""
    mission_id: str | None = None


@dataclass(frozen=True)
class ActivityViewModel:
    activity_id: str = ""
    question: str = ""
    context: str = ""
    supporting_material: str = ""
    hints: tuple[str, ...] = ()
    answer_prompt: str = "Your answer"
    explanation: str = ""
    next_action_label: str = "Continue"
    topic_title: str = ""
    position_label: str = ""
    has_hints: bool = False
    has_explanation: bool = False
    is_final: bool = False
    session_id: str = ""


@dataclass(frozen=True)
class ReflectionViewModel:
    key_insight: str = ""
    concept_confidence: str = ""
    suggested_improvement: str = ""
    reflection_prompt: str = ""
    topic_title: str = ""
    next_action_label: str = "Continue to Summary"
    session_id: str = ""
    has_insight: bool = False


@dataclass(frozen=True)
class CompletionViewModel:
    topics_completed: tuple[str, ...] = ()
    time_studied_label: str = ""
    activities_completed_label: str = ""
    learning_insights: tuple[str, ...] = ()
    readiness_change_label: str = ""
    next_recommendation: str = ""
    next_session_label: str = ""
    return_home_label: str = "Return Home"
    return_home_enabled: bool = True
    session_id: str = ""


@dataclass(frozen=True)
class SessionPageViewModel:
    shell: SessionShellViewModel
    overview: OverviewViewModel | None = None
    activity: ActivityViewModel | None = None
    progress: ProgressBarViewModel | None = None
    reflection: ReflectionViewModel | None = None
    completion: CompletionViewModel | None = None
    primary_cta_label: str = ""
    primary_cta_enabled: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


def page_from_flow(flow: SessionFlowSnapshot) -> SessionPageViewModel:
    """Map a SessionFlowSnapshot to a presentation view model."""
    surface = SessionSurface(flow.surface)
    eyebrow, title, description = page_meta(surface)
    shell = SessionShellViewModel(
        session_id=flow.workspace.session_id,
        student_id=flow.workspace.student_id,
        active_surface=flow.surface,
        page_eyebrow=eyebrow,
        page_title=title,
        page_description=description,
        steps=build_session_steps(surface, session_id=flow.workspace.session_id),
        topic_title=flow.workspace.topic_title,
    )
    overview = overview_vm(flow.overview) if flow.overview else None
    activity = activity_vm(flow.activity) if flow.activity else None
    progress = progress_vm(flow.progress) if flow.progress else None
    reflection = reflection_vm(flow.reflection) if flow.reflection else None
    completion = completion_vm(flow.completion) if flow.completion else None
    cta_label, cta_enabled = _primary_cta(
        surface, overview, activity, reflection, completion
    )
    return SessionPageViewModel(
        shell=shell,
        overview=overview,
        activity=activity,
        progress=progress,
        reflection=reflection,
        completion=completion,
        primary_cta_label=cta_label,
        primary_cta_enabled=cta_enabled,
    )


def overview_vm(snap: OverviewSnapshot) -> OverviewViewModel:
    minutes = snap.estimated_minutes
    duration = "" if minutes is None else f"About {minutes} minutes"
    activities = (
        "No activities listed"
        if snap.activity_count <= 0
        else f"{snap.activity_count} learning "
        f"{'activity' if snap.activity_count == 1 else 'activities'}"
    )
    improvement = ""
    if snap.expected_readiness_improvement is not None:
        pct = abs(int(round(snap.expected_readiness_improvement * 100)))
        if snap.expected_readiness_improvement >= 0:
            improvement = f"Expected readiness lift · about {pct}%"
        else:
            improvement = "Expected readiness change noted"
    begin = snap.begin_action
    return OverviewViewModel(
        objective=snap.objective or "Today's learning objective",
        learning_goal=snap.learning_goal,
        why_studying=snap.why_studying,
        estimated_duration_label=duration,
        activity_count_label=activities,
        topics=snap.topics,
        expected_improvement_label=improvement,
        begin_label=(begin.label if begin else "Begin Session"),
        begin_enabled=bool(snap.can_begin),
        session_id=snap.session_id,
        mission_id=begin.mission_id if begin else None,
    )


def activity_vm(snap: ActivitySnapshot) -> ActivityViewModel:
    return ActivityViewModel(
        activity_id=snap.activity_id,
        question=snap.question,
        context=snap.context,
        supporting_material=snap.supporting_material,
        hints=snap.hints,
        answer_prompt=snap.answer_prompt,
        explanation=snap.explanation,
        next_action_label=snap.next_action_label,
        topic_title=snap.topic_title,
        position_label=f"Activity {snap.activity_index} of {snap.activities_total}",
        has_hints=snap.has_hints,
        has_explanation=snap.has_explanation,
        is_final=snap.is_final_activity,
        session_id=snap.session_id,
    )


def progress_vm(snap: ProgressSnapshot) -> ProgressBarViewModel:
    remaining = ""
    if snap.estimated_remaining_minutes is not None:
        remaining = f"About {snap.estimated_remaining_minutes} minutes remaining"
    return ProgressBarViewModel(
        percent=snap.progress_percent,
        label=f"{snap.progress_percent}% complete",
        completed=snap.activities_completed,
        remaining=snap.activities_remaining,
        total=snap.activities_total,
        current_topic=snap.current_topic,
        remaining_time_label=remaining,
        has_progress=snap.activities_total > 0,
    )


def reflection_vm(snap: ReflectionSnapshot) -> ReflectionViewModel:
    return ReflectionViewModel(
        key_insight=snap.key_insight,
        concept_confidence=snap.concept_confidence,
        suggested_improvement=snap.suggested_improvement,
        reflection_prompt=snap.reflection_prompt,
        topic_title=snap.topic_title,
        next_action_label=snap.next_action_label,
        session_id=snap.session_id,
        has_insight=snap.has_insight,
    )


def completion_vm(snap: CompletionSnapshot) -> CompletionViewModel:
    time_label = ""
    if snap.time_studied_minutes is not None:
        time_label = f"{snap.time_studied_minutes} minutes studied"
    activities = f"{snap.activities_completed} activities completed"
    next_session = ""
    if snap.estimated_next_session_minutes is not None:
        next_session = (
            f"Next session · about {snap.estimated_next_session_minutes} minutes"
        )
    home = snap.return_home
    return CompletionViewModel(
        topics_completed=snap.topics_completed,
        time_studied_label=time_label,
        activities_completed_label=activities,
        learning_insights=snap.learning_insights,
        readiness_change_label=snap.exam_readiness_change_label,
        next_recommendation=snap.next_recommendation,
        next_session_label=next_session,
        return_home_label=(home.label if home else "Return Home"),
        return_home_enabled=bool(snap.can_return_home),
        session_id=snap.session_id,
    )


def _primary_cta(surface, overview, activity, reflection, completion):
    if surface is SessionSurface.OVERVIEW and overview:
        return overview.begin_label, overview.begin_enabled
    if surface is SessionSurface.ACTIVITY and activity:
        return activity.next_action_label, True
    if surface is SessionSurface.REFLECTION and reflection:
        return reflection.next_action_label, True
    if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE} and completion:
        return completion.return_home_label, completion.return_home_enabled
    return "", False


def contains_forbidden_terms(text: str) -> bool:
    """True when learner-facing copy includes forbidden internal terms."""
    lowered = (text or "").lower()
    return any(term in lowered for term in FORBIDDEN_LEARNER_TERMS)
