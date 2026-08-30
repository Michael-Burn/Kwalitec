"""Recommendation trust presentation helpers (EP-008.1).

Compose student-visible trust fields from authored Runtime A fragments only.
Never invent evidence, confidence, or educational effectiveness claims.
"""

from __future__ import annotations

from typing import Any

from app.application.student_experience.dto.recommendation_alternative_snapshot import (
    RecommendationAlternativeSnapshot,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)

# Home L2 alternatives cap (ENGINEERING_DESIGN §5 T10 / UI_SPEC §2.3).
HOME_ALTERNATIVES_CAP = 2

TRUST_STATE_COMPLETE = "complete"
TRUST_STATE_REFUSAL = "refusal"
TRUST_STATE_INCOMPLETE = "incomplete"

_COMPLETION_LOOP_FALLBACK = (
    "After you finish tonight's Session, Home shows the next step on your plan."
)

# Coherence codes that signal advice relative to Today's Mission (Q9).
_ADVISORY_COHERENCE = frozenset(
    {"advisory", "contextual", "wellbeing", "deferred"}
)


def compose_timeliness_line(
    *,
    reason: str = "",
    why_recommended: str = "",
    category: str = "",
    plan_coherence_label: str = "",
    plan_coherence: str = "",
    exam_countdown_days: int | None = None,
    honest_refusal: bool = False,
) -> str:
    """Compose L1 “why now” from authored fragments only.

    Prefer a distinct authored ``reason`` (timeliness narrative). Do not
    duplicate ``why_recommended``. Never invent countdown claims without
    authored category context. Refusal paths omit coherence theatre.
    """
    if honest_refusal:
        authored_reason = translate_to_student_language(reason)
        authored_why = translate_to_student_language(why_recommended)
        if authored_reason and authored_reason != authored_why:
            return authored_reason
        return ""

    authored_reason = translate_to_student_language(reason)
    authored_why = translate_to_student_language(why_recommended)
    if authored_reason and authored_reason != authored_why:
        return authored_reason

    cat = translate_to_student_language(category)
    if cat and exam_countdown_days is not None and exam_countdown_days >= 0:
        if exam_countdown_days == 0:
            return f"{cat} priority. Exam day."
        if exam_countdown_days == 1:
            return f"{cat} priority with 1 day to exam."
        return f"{cat} priority with {exam_countdown_days} days to exam."

    coherence = (plan_coherence or "").strip().lower()
    label = translate_to_student_language(plan_coherence_label)
    if label and coherence in _ADVISORY_COHERENCE:
        return label

    return ""


def compose_completion_loop_line(*, review_point: str = "") -> str:
    """Prefer authored review_point; omit invention when empty (caller may fallback)."""
    return translate_to_student_language(review_point)


def completion_loop_fallback() -> str:
    """Honest static line when no authored review_point (UI_SPEC §8)."""
    return _COMPLETION_LOOP_FALLBACK


def resolve_trust_state(
    *,
    honest_refusal: bool = False,
    is_complete: bool = False,
) -> str:
    """Map refusal / completeness onto Home ``trust_state`` vocabulary."""
    if honest_refusal:
        return TRUST_STATE_REFUSAL
    if is_complete:
        return TRUST_STATE_COMPLETE
    return TRUST_STATE_INCOMPLETE


def map_recommendation_alternatives(
    raw_alternatives: Any,
    *,
    honest_refusal: bool = False,
    cap: int = HOME_ALTERNATIVES_CAP,
) -> tuple[RecommendationAlternativeSnapshot, ...]:
    """Map bridge alternatives to DTOs; hide on refusal; cap for Home."""
    if honest_refusal:
        return ()
    if not isinstance(raw_alternatives, list | tuple):
        return ()
    mapped: list[RecommendationAlternativeSnapshot] = []
    for item in raw_alternatives:
        if not isinstance(item, dict):
            continue
        title = translate_to_student_language(
            str(item.get("title") or item.get("recommendation_label") or "")
        )
        if not title:
            continue
        why = translate_to_student_language(
            str(
                item.get("why_recommended")
                or item.get("reason")
                or item.get("summary")
                or ""
            )
        )
        benefit = translate_to_student_language(
            str(item.get("expected_benefit") or "")
        )
        next_action = translate_to_student_language(
            str(
                item.get("suggested_next_action")
                or item.get("next_action")
                or ""
            )
        )
        mapped.append(
            RecommendationAlternativeSnapshot(
                title=title,
                why_recommended=why,
                expected_benefit=benefit,
                suggested_next_action=next_action,
            )
        )
        if len(mapped) >= max(0, int(cap)):
            break
    return tuple(mapped)


def readiness_bridge_sentence(
    *,
    readiness_expected_benefit: str = "",
    expected_readiness_improvement_label: str = "",
) -> str:
    """Optional one-line tip↔readiness bridge from authored labels only."""
    benefit = translate_to_student_language(readiness_expected_benefit)
    if benefit:
        return f"Expected readiness change from tonight's focus: {benefit}."
    label = (expected_readiness_improvement_label or "").strip()
    if label:
        return f"Expected readiness change from tonight's focus: {label}."
    return ""
