"""Reflection field mapping — session / state → capture field views.

Forwards already-decided study-session display facts and optional student
evidence strings into reflection field chrome. Does not diagnose, score, or
decide what the student should study next.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import (
    Badge,
    Button,
    Card,
    CardVariant,
    Section,
    Tone,
    primary_button,
)
from presentation.reflection.confidence_scale import ConfidenceScale
from presentation.reflection.reflection_view_model import (
    ConfidenceFieldView,
    DifficultyFieldView,
    MissionCompletionFieldView,
    ReflectionSummaryFieldView,
    StudentNotesFieldView,
    WeakConceptFieldView,
)

_DEFAULT_CONFIDENCE_PROMPT = "How confident do you feel about this session?"
_DEFAULT_DIFFICULTY_PROMPT = "How difficult did this session feel?"
_DEFAULT_WEAK_PROMPT = "Which concept still feels unclear?"
_DEFAULT_WEAK_PLACEHOLDER = "Name one concept that needs more practice."
_DEFAULT_NOTES_PROMPT = "Add any notes from this session."
_DEFAULT_SUMMARY_HEADLINE = "Reflection summary"
_DEFAULT_SUMMARY_DETAIL = (
    "Your reflection will appear here as you capture confidence, "
    "difficulty, notes, and concepts that still need practice."
)
_COMPLETE_LABEL = "Session complete"
_INCOMPLETE_LABEL = "Session in progress"
_COMPLETE_DETAIL = "This session has reached completion. Reflect on the work you did."
_INCOMPLETE_DETAIL = (
    "Reflection is available when the session reaches the reflection stage "
    "or completion."
)


class ReflectionMapper:
    """Map study-session and runtime inputs into reflection field views."""

    @classmethod
    def map_confidence(
        cls,
        *,
        prompt: str | None = None,
        selected: str | None = None,
    ) -> ConfidenceFieldView:
        """Build the confidence capture field with Design System scale chrome."""
        scale = ConfidenceScale.confidence(
            prompt=_text(prompt, fallback=_DEFAULT_CONFIDENCE_PROMPT),
            selected=selected,
        )
        value_label = scale.selected_label
        detail = value_label or "Select how confident you feel about this session."
        return ConfidenceFieldView(
            prompt=scale.prompt,
            scale=scale,
            value_label=value_label,
            section=Section(
                title="Confidence",
                description=detail,
                eyebrow="Reflection",
            ),
        )

    @classmethod
    def map_difficulty(
        cls,
        *,
        prompt: str | None = None,
        selected: str | None = None,
    ) -> DifficultyFieldView:
        """Build the difficulty capture field with Design System scale chrome."""
        scale = ConfidenceScale.difficulty(
            prompt=_text(prompt, fallback=_DEFAULT_DIFFICULTY_PROMPT),
            selected=selected,
        )
        value_label = scale.selected_label
        detail = value_label or "Select how difficult this session felt."
        return DifficultyFieldView(
            prompt=scale.prompt,
            scale=scale,
            value_label=value_label,
            section=Section(
                title="Difficulty",
                description=detail,
                eyebrow="Reflection",
            ),
        )

    @classmethod
    def map_mission_completion(
        cls,
        session: Any = None,
        state: Any = None,
    ) -> MissionCompletionFieldView:
        """Project session completion posture into a status field."""
        is_complete = _is_complete(state)
        checklist = _completion_checklist(session)
        label = _COMPLETE_LABEL if is_complete else _INCOMPLETE_LABEL
        detail = _COMPLETE_DETAIL if is_complete else _INCOMPLETE_DETAIL
        completion = getattr(session, "completion", None) if session else None
        completion_detail = _text(getattr(completion, "detail", None))
        if completion_detail:
            detail = completion_detail
        badge = Badge(
            label=label,
            tone=Tone.SUCCESS if is_complete else Tone.NEUTRAL,
        )
        return MissionCompletionFieldView(
            label=label,
            detail=detail,
            is_complete=is_complete,
            badge=badge,
            checklist=checklist,
            section=Section(
                title="Mission completion",
                description=detail,
                eyebrow="Session",
            ),
        )

    @classmethod
    def map_weak_concept(
        cls,
        *,
        value: str | None = None,
        prompt: str | None = None,
        mission_objective: str | None = None,
    ) -> WeakConceptFieldView:
        """Build the weak-concept free-text capture field."""
        resolved_prompt = _text(prompt, fallback=_DEFAULT_WEAK_PROMPT)
        cleaned_value = _text(value)
        placeholder = _DEFAULT_WEAK_PLACEHOLDER
        objective = _text(mission_objective)
        if objective and not cleaned_value:
            placeholder = (
                f"For example, a part of: {_first_sentence(objective)}"
            )
        detail = cleaned_value or placeholder
        return WeakConceptFieldView(
            prompt=resolved_prompt,
            placeholder=placeholder,
            value=cleaned_value,
            section=Section(
                title="Weak concept",
                description=detail,
                eyebrow="Reflection",
            ),
        )

    @classmethod
    def map_student_notes(
        cls,
        session: Any = None,
        *,
        value: str | None = None,
        prompt: str | None = None,
    ) -> StudentNotesFieldView:
        """Forward study-session notes into the reflection notes field."""
        resolved_prompt = _text(prompt, fallback=_DEFAULT_NOTES_PROMPT)
        notes_section = getattr(session, "study_notes", None) if session else None
        from_session = _text(getattr(notes_section, "description", None))
        cleaned = _text(value) or from_session
        detail = cleaned or "No notes captured for this session yet."
        return StudentNotesFieldView(
            prompt=resolved_prompt,
            value=cleaned,
            section=Section(
                title="Student notes",
                description=detail,
                eyebrow="Notes",
            ),
        )

    @classmethod
    def map_summary(
        cls,
        *,
        confidence: ConfidenceFieldView,
        mission_completion: MissionCompletionFieldView,
        difficulty: DifficultyFieldView,
        weak_concept: WeakConceptFieldView,
        student_notes: StudentNotesFieldView,
        reflection_prompt: str | None = None,
    ) -> ReflectionSummaryFieldView:
        """Assemble a read-only summary of captured reflection evidence."""
        lines: list[str] = []
        if mission_completion.label:
            lines.append(f"Completion: {mission_completion.label}")
        if confidence.value_label:
            lines.append(f"Confidence: {confidence.value_label}")
        if difficulty.value_label:
            lines.append(f"Difficulty: {difficulty.value_label}")
        if weak_concept.value:
            lines.append(f"Weak concept: {weak_concept.value}")
        if student_notes.value:
            lines.append(f"Notes: {student_notes.value}")

        prompt = _text(reflection_prompt)
        if prompt and prompt not in lines:
            lines.insert(0, prompt)

        detail = (
            "\n".join(lines) if lines else _DEFAULT_SUMMARY_DETAIL
        )
        card = Card(
            title=_DEFAULT_SUMMARY_HEADLINE,
            body=detail,
            eyebrow="Summary",
            variant=CardVariant.DEFAULT,
        )
        return ReflectionSummaryFieldView(
            headline=_DEFAULT_SUMMARY_HEADLINE,
            detail=detail,
            lines=tuple(lines),
            card=card,
            section=Section(
                title=_DEFAULT_SUMMARY_HEADLINE,
                description=detail,
                eyebrow="Summary",
            ),
        )

    @classmethod
    def primary_action(cls, *, is_ready: bool) -> Button:
        """Return the primary continue CTA for the reflection surface."""
        label = "Continue to Summary" if is_ready else "Return Home"
        return primary_button(label)


def _is_complete(state: Any) -> bool:
    if state is None:
        return False
    if bool(getattr(state, "is_terminal", False)):
        return True
    stage = getattr(state, "stage", None)
    raw = getattr(stage, "value", stage)
    return str(raw).strip().lower() in {"completed", "reflection"}


def _completion_checklist(session: Any) -> tuple[str, ...]:
    completion = getattr(session, "completion", None) if session else None
    items = getattr(completion, "checklist", ()) if completion else ()
    if items is None:
        return ()
    try:
        return tuple(
            text
            for text in (_text(item) for item in items)
            if text
        )
    except TypeError:
        return ()


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _first_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    if len(cleaned) > 80:
        return cleaned[:77].rstrip() + "…"
    return cleaned
