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
from app.presentation.formatting import (
    format_duration_estimate,
    format_remaining_minutes,
)
from app.presentation.session.navigation import (
    SessionNavStep,
    build_session_steps,
    page_meta,
)
from app.presentation.student.view_models import (
    ExplanationViewModel,
    explanation_vm,
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
    learning_objectives: tuple[str, ...] = ()
    expected_improvement_label: str = ""
    begin_label: str = "Start Session"
    begin_enabled: bool = False
    session_id: str = ""
    mission_id: str | None = None
    # Adaptive MES for Overview (pass-through; render in a later pass).
    explanation: ExplanationViewModel | None = None
    # Sitting package identity for Overview briefing authoring.
    educational_package_id: str = ""
    subject_code: str = ""


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
    activity_type: str = ""
    stage_label: str = ""
    has_hints: bool = False
    has_explanation: bool = False
    is_final: bool = False
    session_id: str = ""
    feedback_outcome: str = ""
    model_answer: str = ""
    common_mistake: str = ""
    next_action: str = ""
    scored_correct: bool | None = None


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
    headline: str = "Session complete"
    primary_topic: str = ""
    # KWP-002 — completion moment / Journey update (presentation only).
    journey_update_label: str = ""
    finish_outcome_label: str = ""
    # KWP-005 — Sitting Report presentation fields.
    what_studied: str = ""
    performance_summary: str = ""
    progress_explanation: str = ""
    tomorrow_preview: str = ""
    assessment_mode_active: bool = False
    assessment_summary: str = ""
    exercises_assigned: tuple[str, ...] = ()
    exercises_completed: tuple[str, ...] = ()
    strengthened: tuple[str, ...] = ()
    needs_reinforcement: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    learning_objectives: tuple[str, ...] = ()
    sitting_report_ready: bool = False
    # KWP-007 — Learning Strategy recommendation + WHY
    strategy_title: str = ""
    strategy_body: str = ""
    strategy_explanation: str = ""
    strategy_spacing_guidance: str = ""
    strategy_confidence_guidance: str = ""
    # KWP-008 — Learning Diagnostics guidance (no labels)
    diagnostic_guidance: str = ""
    diagnostic_explanation: str = ""
    # KWP-009 — Learning Difficulty / load guidance (no band labels)
    difficulty_guidance: str = ""
    difficulty_explanation: str = ""
    # KWP-010 — Intervention Effectiveness (natural feedback; no verdict labels)
    effectiveness_feedback: str = ""


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
    # PX-002A T1-2: shared duration formatting — matches Home/Mission wording
    # so the same estimate never reads differently on different screens.
    duration = format_duration_estimate(snap.estimated_minutes)
    activities = (
        "No activities listed"
        if snap.activity_count <= 0
        else f"{snap.activity_count} learning "
        f"{'activity' if snap.activity_count == 1 else 'activities'}"
    )
    improvement = ""
    if snap.expected_readiness_improvement is not None:
        pct = abs(int(round(snap.expected_readiness_improvement * 100)))
        if snap.expected_readiness_improvement >= 0 and pct > 0:
            improvement = (
                f"Possible readiness movement · about {pct}% "
                "(estimate, not a guarantee)"
            )
        else:
            improvement = "Possible readiness change noted (estimate only)"
    else:
        # Honest general purpose — do not invent a decorative percentage.
        improvement = (
            "This Session is meant to strengthen readiness on today's topic — "
            "how much depends on your practice."
        )
    begin = snap.begin_action
    return OverviewViewModel(
        objective=snap.objective or "Today's learning objective",
        learning_goal=snap.learning_goal,
        why_studying=snap.why_studying,
        estimated_duration_label=duration,
        activity_count_label=activities,
        topics=snap.topics,
        learning_objectives=tuple(snap.learning_objectives or ()),
        expected_improvement_label=improvement,
        begin_label=(begin.label if begin else "Start Session"),
        begin_enabled=bool(snap.can_begin),
        session_id=snap.session_id,
        mission_id=begin.mission_id if begin else None,
        explanation=explanation_vm(snap.explanation),
        educational_package_id=snap.educational_package_id or "",
        subject_code=snap.subject_code or "",
    )


def activity_vm(snap: ActivitySnapshot) -> ActivityViewModel:
    next_label = snap.next_action_label or "Continue"
    if snap.is_final_activity and next_label == "Continue":
        next_label = "Continue to Reflection"
    stage = (snap.stage_label or "").strip()
    position = f"Activity {snap.activity_index} of {snap.activities_total}"
    if stage:
        position = f"{stage} · {position}"
    return ActivityViewModel(
        activity_id=snap.activity_id,
        question=snap.question,
        context=snap.context,
        supporting_material=snap.supporting_material,
        hints=snap.hints,
        answer_prompt=snap.answer_prompt,
        explanation=snap.explanation,
        next_action_label=next_label,
        topic_title=snap.topic_title,
        position_label=position,
        activity_type=snap.activity_type or "",
        stage_label=stage,
        has_hints=snap.has_hints,
        has_explanation=snap.has_explanation,
        is_final=snap.is_final_activity,
        session_id=snap.session_id,
        feedback_outcome=snap.feedback_outcome,
        model_answer=snap.model_answer,
        common_mistake=snap.common_mistake,
        next_action=snap.next_action,
        scored_correct=snap.scored_correct,
    )


def progress_vm(snap: ProgressSnapshot) -> ProgressBarViewModel:
    remaining = format_remaining_minutes(snap.estimated_remaining_minutes)
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
    from app.presentation.session.sitting_report import (
        build_sitting_report,
        insights_from_sitting_report,
    )

    time_label = ""
    if snap.time_studied_minutes is not None:
        time_label = f"{snap.time_studied_minutes} minutes studied"
    activities = f"{snap.activities_completed} activities completed"
    next_session = ""
    if snap.estimated_next_session_minutes is not None:
        next_session = (
            f"Next Session · about {snap.estimated_next_session_minutes} minutes"
        )
    home = snap.return_home
    primary_topic = ""
    if snap.topics_completed:
        primary_topic = str(snap.topics_completed[0]).strip()
    meta_pairs = tuple(snap.metadata or ())
    meta = dict(meta_pairs)
    if not primary_topic:
        primary_topic = str(meta.get("topic_title") or "").strip()

    opaque = _sitting_opaque_from_metadata_pairs(meta_pairs)
    sitting = build_sitting_report(
        topic_title=primary_topic,
        opaque_summary=opaque,
        metadata=meta,
        next_recommendation=snap.next_recommendation,
    )
    insights = insights_from_sitting_report(sitting) or snap.learning_insights
    if not insights and primary_topic:
        insights = (
            f"Today's practice on {primary_topic} updates your Learning Insights",
        )
    if primary_topic:
        headline = sitting.headline or f"Sitting Report · {primary_topic}"
    else:
        headline = sitting.headline or "Sitting Report"
    journey_update = sitting.progress_explanation or ""
    if not journey_update:
        if primary_topic and snap.next_recommendation:
            journey_update = (
                f"You completed {primary_topic}. "
                f"Next focus: {snap.next_recommendation}."
            )
        elif primary_topic:
            journey_update = (
                f"You completed {primary_topic}. "
                "Your Journey is ready with the next step."
            )
        elif snap.next_recommendation:
            journey_update = (
                f"Journey updated · next focus: {snap.next_recommendation}."
            )
        else:
            journey_update = "Journey updated from today's honest practice."
    finish_outcome = (
        sitting.finish_outcome_label
        or snap.exam_readiness_change_label
        or ""
    )
    return CompletionViewModel(
        topics_completed=snap.topics_completed,
        time_studied_label=time_label,
        activities_completed_label=activities,
        learning_insights=insights,
        readiness_change_label=snap.exam_readiness_change_label,
        next_recommendation=snap.next_recommendation,
        next_session_label=next_session,
        return_home_label=(home.label if home else "Return Home"),
        return_home_enabled=bool(snap.can_return_home),
        session_id=snap.session_id,
        headline=headline,
        primary_topic=primary_topic,
        journey_update_label=journey_update,
        finish_outcome_label=finish_outcome,
        what_studied=sitting.what_studied,
        performance_summary=sitting.performance_summary,
        progress_explanation=sitting.progress_explanation,
        tomorrow_preview=sitting.tomorrow_preview
        or (
            f"Up next · {snap.next_recommendation}"
            if snap.next_recommendation
            else ""
        ),
        assessment_mode_active=sitting.assessment_mode_active,
        assessment_summary=sitting.assessment_summary,
        exercises_assigned=sitting.exercises_assigned,
        exercises_completed=sitting.exercises_completed,
        strengthened=sitting.strengthened,
        needs_reinforcement=sitting.needs_reinforcement,
        syllabus_refs=sitting.syllabus_refs,
        learning_objectives=sitting.learning_objectives
        or tuple(v for k, v in meta_pairs if k == "learning_objective"),
        sitting_report_ready=sitting.has_report,
        strategy_title=sitting.strategy_title,
        strategy_body=sitting.strategy_body,
        strategy_explanation=sitting.strategy_explanation,
        strategy_spacing_guidance=sitting.strategy_spacing_guidance,
        strategy_confidence_guidance=sitting.strategy_confidence_guidance,
        diagnostic_guidance=sitting.diagnostic_guidance,
        diagnostic_explanation=sitting.diagnostic_explanation,
        difficulty_guidance=sitting.difficulty_guidance,
        difficulty_explanation=sitting.difficulty_explanation,
        effectiveness_feedback=sitting.effectiveness_feedback,
    )


def _sitting_opaque_from_metadata_pairs(
    pairs: tuple[tuple[str, str], ...],
) -> dict:
    """Rebuild opaque sitting facts from CompletionSnapshot metadata pairs."""
    meta = dict(pairs)
    objectives = tuple(v for k, v in pairs if k == "learning_objective" and v)
    activities: list[dict] = []
    for key, value in pairs:
        if key != "activity_item":
            continue
        parts = str(value).split("|", 2)
        stage = parts[0] if parts else ""
        title = parts[1] if len(parts) > 1 else ""
        done = parts[2] == "1" if len(parts) > 2 else False
        refs = tuple(v for k, v in pairs if k == "syllabus_ref" and v)
        activities.append(
            {
                "stage": stage,
                "title": title,
                "completed": done,
                "syllabus_refs": refs if stage == "practice" else (),
            }
        )
    observations = [
        {"type_id": v} for k, v in pairs if k == "observation_type" and v
    ]
    return {
        "topic_title": meta.get("topic_title") or "",
        "reflection_note": meta.get("reflection_note") or "",
        "learning_objectives": objectives,
        "activities": activities,
        "observations": observations,
        "observation_type_ids": [o["type_id"] for o in observations],
        "syllabus_refs": tuple(v for k, v in pairs if k == "syllabus_ref" and v),
        "progress_advanced": meta.get("progress_advanced") == "true",
        "mission_completed": meta.get("mission_completed") == "true",
        "evidence_disposition": meta.get("evidence_disposition") or "",
        "educational_package_id": meta.get("educational_package_id") or "",
        "subject_id": meta.get("subject_id") or "",
        "finish_review": {
            "verdict": meta.get("finish_review") or "",
            "label": meta.get("finish_review_label") or "",
        },
        "substance": "package",
        # KWP-011 — carry frozen intelligence markers into opaque for report.
        "intelligence_snapshot": (
            {
                "student_sitting_report": {
                    k: meta[k]
                    for k in (
                        "strategy_title",
                        "strategy_body",
                        "strategy_explanation",
                        "strategy_spacing_guidance",
                        "strategy_momentum_guidance",
                        "strategy_confidence_guidance",
                        "diagnostic_guidance",
                        "diagnostic_explanation",
                        "difficulty_title",
                        "difficulty_guidance",
                        "difficulty_explanation",
                        "effectiveness_feedback",
                        "effectiveness_explanation",
                    )
                    if meta.get(k)
                },
                "captured_at": meta.get("intelligence_captured_at") or "",
            }
            if meta.get("intelligence_captured") == "true"
            or meta.get("strategy_title")
            else None
        ),
    }


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
