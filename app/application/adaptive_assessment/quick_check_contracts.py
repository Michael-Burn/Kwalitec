"""Quick Check presentation contracts — ILE-001B.

Immutable DTOs for Mission entry, introduction, questions, progress,
completion, and Mission return. Presentation only — no educational
intelligence, selection, or Twin state.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.adaptive_assessment.accessibility import (
    AccessibilityMetadata,
    accessibility_for_session,
)
from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.selected_learning_check import (
    LearningCheckItem,
    SelectedLearningCheck,
    get_already_selected_quick_check,
)
from app.application.adaptive_assessment.session_registry import (
    SessionTypeId,
    get_session_type,
)


@dataclass(frozen=True)
class QuickCheckMissionCardContract:
    """Mission entry card for Quick Check invitation."""

    session_type_id: str
    title: str
    duration_label: str
    invitation: str
    continue_label: str
    why_this_label: str
    tutor_note: str
    defer_label: str
    available: bool
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckIntroductionContract:
    """Learner introduction / why-this-check surface."""

    title: str
    body: str
    duration_label: str
    begin_label: str
    defer_label: str
    why_control_label: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckProgressContract:
    """Calm progress chrome — never exam numbering or scores."""

    label: str
    percent: int
    accessible_label: str
    show_numeric_position: bool = False


@dataclass(frozen=True)
class QuickCheckQuestionContract:
    """One question presentation surface."""

    item_id: str
    stem: str
    response_kind: str
    choices: tuple[str, ...]
    hint: str
    hint_visible: bool
    hint_label: str
    hint_request_label: str
    response_prompt: str
    next_label: str
    pause_label: str
    pause_accessible: str
    progress: QuickCheckProgressContract
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckReflectionContract:
    """Post-questions reflection surface."""

    title: str
    prompt: str
    continue_label: str
    pause_label: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckCompletionContract:
    """Completion surface — never grades, pass/fail, or mastery claims."""

    thank_you: str
    evidence_summary: str
    uncertainty_summary: str
    mission_benefit: str
    return_label: str
    use_to_guide: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckPausedContract:
    """Pause / resume surface."""

    body: str
    resume_label: str
    resume_accessible: str
    defer_label: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class QuickCheckMissionReturnContract:
    """Mission reintegration acknowledgement after completion."""

    acknowledgement: str
    session_type_id: str


def _quick_check_a11y() -> AccessibilityMetadata:
    return accessibility_for_session(SessionTypeId.QUICK_CHECK)


def build_quick_check_mission_card(
    *,
    available: bool,
) -> QuickCheckMissionCardContract:
    """Build the Mission entry card contract from registries."""
    session = get_session_type(SessionTypeId.QUICK_CHECK)
    return QuickCheckMissionCardContract(
        session_type_id=session.identifier,
        title=session.display_name,
        duration_label=session.expected_duration_label,
        invitation=resolve_copy("quick_check.invitation.headline"),
        continue_label=resolve_copy("quick_check.invitation.cta"),
        why_this_label=resolve_copy("quick_check.invitation.why_this"),
        tutor_note=resolve_copy("quick_check.invitation.tutor_available"),
        defer_label=resolve_copy("action.defer"),
        available=available,
        accessibility=_quick_check_a11y(),
    )


def build_quick_check_introduction() -> QuickCheckIntroductionContract:
    """Build the introduction / why-this-check contract."""
    session = get_session_type(SessionTypeId.QUICK_CHECK)
    return QuickCheckIntroductionContract(
        title=resolve_copy("quick_check.intro.title"),
        body=resolve_copy("explain.why_body"),
        duration_label=session.expected_duration_label,
        begin_label=resolve_copy("quick_check.intro.begin"),
        defer_label=resolve_copy("action.defer"),
        why_control_label=resolve_copy("explain.why_am_i_seeing_this"),
        accessibility=_quick_check_a11y(),
    )


def build_calm_progress(
    *,
    index: int,
    total: int,
) -> QuickCheckProgressContract:
    """Build calm progress without 'Question N of M' exam chrome."""
    if total <= 0:
        percent = 0
        ratio = 0.0
    else:
        # Mid-item progress: completed fraction of the journey.
        percent = int(round(((index + 0.5) / total) * 100))
        percent = max(0, min(100, percent))
        ratio = (index + 1) / total
    if ratio < 0.4:
        label = resolve_copy("quick_check.progress.steady")
    elif ratio < 0.85:
        label = resolve_copy("quick_check.progress.making")
    else:
        label = resolve_copy("quick_check.progress.almost")
    return QuickCheckProgressContract(
        label=label,
        percent=percent,
        accessible_label=resolve_copy("a11y.quick_check.progress"),
        show_numeric_position=False,
    )


def build_quick_check_question(
    item: LearningCheckItem,
    *,
    index: int,
    total: int,
    hint_visible: bool = False,
) -> QuickCheckQuestionContract:
    """Build a question presentation contract for one already-selected item."""
    return QuickCheckQuestionContract(
        item_id=item.item_id,
        stem=item.stem,
        response_kind=item.response_kind,
        choices=item.choices,
        hint=item.hint,
        hint_visible=hint_visible,
        hint_label=resolve_copy("quick_check.hint.label"),
        hint_request_label=resolve_copy("quick_check.hint.request"),
        response_prompt=resolve_copy("quick_check.response.prompt"),
        next_label=resolve_copy("quick_check.action.next"),
        pause_label=resolve_copy("action.pause"),
        pause_accessible=resolve_copy("a11y.quick_check.pause"),
        progress=build_calm_progress(index=index, total=total),
        accessibility=_quick_check_a11y(),
    )


def build_quick_check_reflection() -> QuickCheckReflectionContract:
    """Build the reflection surface contract."""
    return QuickCheckReflectionContract(
        title=resolve_copy("quick_check.reflection.title"),
        prompt=resolve_copy("quick_check.reflection.prompt"),
        continue_label=resolve_copy("quick_check.reflection.continue"),
        pause_label=resolve_copy("action.pause"),
        accessibility=_quick_check_a11y(),
    )


def build_quick_check_completion() -> QuickCheckCompletionContract:
    """Build the completion surface — evidence honest, never graded."""
    return QuickCheckCompletionContract(
        thank_you=resolve_copy("quick_check.completion.thank_you"),
        evidence_summary=resolve_copy("quick_check.completion.evidence"),
        uncertainty_summary=resolve_copy("quick_check.completion.uncertain"),
        mission_benefit=resolve_copy(
            "quick_check.completion.mission_benefit"
        ),
        return_label=resolve_copy("quick_check.completion.return"),
        use_to_guide=resolve_copy("feedback.use_to_guide"),
        accessibility=_quick_check_a11y(),
    )


def build_quick_check_paused() -> QuickCheckPausedContract:
    """Build the pause / resume surface contract."""
    return QuickCheckPausedContract(
        body=resolve_copy("quick_check.paused.body"),
        resume_label=resolve_copy("quick_check.action.resume"),
        resume_accessible=resolve_copy("a11y.quick_check.resume"),
        defer_label=resolve_copy("action.defer"),
        accessibility=_quick_check_a11y(),
    )


def build_quick_check_mission_return() -> QuickCheckMissionReturnContract:
    """Build Mission reintegration acknowledgement."""
    return QuickCheckMissionReturnContract(
        acknowledgement=resolve_copy("quick_check.mission.evidence_ack"),
        session_type_id=SessionTypeId.QUICK_CHECK,
    )


def default_selected_learning_check() -> SelectedLearningCheck:
    """Return the already-selected Quick Check pack (no selection)."""
    return get_already_selected_quick_check()
