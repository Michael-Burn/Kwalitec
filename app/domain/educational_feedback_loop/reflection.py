"""Student reflection prompts (ILE-005).

Optional brief questions — invite educational judgement, never coerce.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.educational_feedback_loop.enums import (
    REFLECTION_ANSWER_LABELS,
    REFLECTION_PROMPT_TEXT,
    ReflectionAnswer,
    StudentReflectionPromptId,
)


@dataclass(frozen=True)
class StudentReflectionPrompt:
    """One optional reflective question for a recommendation record."""

    prompt_id: str
    question: str
    answer_choices: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class StudentReflectionInvite:
    """Optional reflection invite for a journal recommendation entry."""

    decision_id: str
    recommendation_title: str
    prompts: tuple[StudentReflectionPrompt, ...]
    intro_line: str
    optional_note_label: str
    submit_label: str
    skip_label: str
    available: bool = True


_ANSWER_CHOICES: tuple[tuple[str, str], ...] = tuple(
    (a.value, REFLECTION_ANSWER_LABELS[a])
    for a in (
        ReflectionAnswer.YES,
        ReflectionAnswer.MOSTLY,
        ReflectionAnswer.NO,
        ReflectionAnswer.SKIPPED,
    )
)


def compose_reflection_invite(
    *,
    decision_id: str,
    recommendation_title: str = "",
    already_reflected: bool = False,
) -> StudentReflectionInvite:
    """Compose an optional student reflection invite.

    Reflection remains optional. Empty invite when already reflected or
    no decision id.
    """
    title = (recommendation_title or "this guidance").strip()
    if already_reflected or not (decision_id or "").strip():
        return StudentReflectionInvite(
            decision_id=decision_id or "",
            recommendation_title=title,
            prompts=(),
            intro_line="",
            optional_note_label="",
            submit_label="",
            skip_label="",
            available=False,
        )

    prompts = tuple(
        StudentReflectionPrompt(
            prompt_id=pid.value,
            question=REFLECTION_PROMPT_TEXT[pid],
            answer_choices=_ANSWER_CHOICES,
        )
        for pid in (
            StudentReflectionPromptId.HELPED,
            StudentReflectionPromptId.TIMING,
            StudentReflectionPromptId.UNDERSTOOD_WHY,
            StudentReflectionPromptId.SAME_DECISION,
        )
    )
    return StudentReflectionInvite(
        decision_id=decision_id.strip(),
        recommendation_title=title,
        prompts=prompts,
        intro_line=(
            "Optional reflection — a few calm questions about whether "
            f"“{title}” was educationally useful. You can skip any question."
        ),
        optional_note_label="Anything else worth remembering? (optional)",
        submit_label="Save reflection",
        skip_label="Skip for now",
        available=True,
    )
