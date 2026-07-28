"""Deterministic presentation catalogues (EX-001).

Wording simplifies Educational Decision fields for students without removing
explainability. Catalogues are fixed — no generative AI.
"""

from __future__ import annotations

from app.domain.educational_experience_engine.urgency import UrgencyLevel
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)

# Student-facing titles keyed by educational decision type.
_DECISION_TITLES: dict[str, str] = {
    DecisionType.STUDY_NEW.value: "Study {target}",
    DecisionType.REVISE.value: "Revise {target}",
    DecisionType.STRENGTHEN_CONFIDENCE.value: "Strengthen confidence on {target}",
    DecisionType.SATISFY_PREREQUISITE.value: "Cover prerequisite {target}",
    DecisionType.CONTINUE_PATH.value: "Continue with {target}",
}

_DECISION_SUMMARIES: dict[str, str] = {
    DecisionType.STUDY_NEW.value: (
        "Make progress on {area} by studying this learning objective next."
    ),
    DecisionType.REVISE.value: (
        "Return to {area} to restore retention before knowledge fades further."
    ),
    DecisionType.STRENGTHEN_CONFIDENCE.value: (
        "You have started {area}; build confidence so progress stays reliable."
    ),
    DecisionType.SATISFY_PREREQUISITE.value: (
        "Complete this prerequisite so later curriculum in {area} can unlock."
    ),
    DecisionType.CONTINUE_PATH.value: (
        "Keep momentum on {area} by continuing from your recent study."
    ),
}

_OUTCOME_COPY: dict[str, str] = {
    ExpectedOutcome.INTRODUCE_NODE.value: (
        "Introduce this curriculum area and establish first understanding"
    ),
    ExpectedOutcome.ADVANCE_MASTERY.value: (
        "Advance mastery of this curriculum area"
    ),
    ExpectedOutcome.RESTORE_RETENTION.value: (
        "Restore retention so previously learned material stays available"
    ),
    ExpectedOutcome.RAISE_CONFIDENCE.value: (
        "Raise confidence so your understanding feels dependable"
    ),
    ExpectedOutcome.UNLOCK_DEPENDENT.value: (
        "Unlock dependent curriculum that requires this prerequisite"
    ),
    ExpectedOutcome.MAINTAIN_MOMENTUM.value: (
        "Maintain study momentum along your current curriculum path"
    ),
}

_MOTIVATION: dict[str, str] = {
    DecisionType.STUDY_NEW.value: (
        "A clear next step keeps your syllabus moving forward."
    ),
    DecisionType.REVISE.value: (
        "Short, timely revision protects what you have already earned."
    ),
    DecisionType.STRENGTHEN_CONFIDENCE.value: (
        "Confidence grows with focused practice — one solid block helps."
    ),
    DecisionType.SATISFY_PREREQUISITE.value: (
        "Prerequisites are the foundation; covering them unlocks what follows."
    ),
    DecisionType.CONTINUE_PATH.value: (
        "Continuing where you left off is often the highest-value next action."
    ),
}

_NEXT_STEPS: dict[str, tuple[str, ...]] = {
    DecisionType.STUDY_NEW.value: (
        "Open the recommended curriculum area",
        "Read or watch the core explanation",
        "Complete one short practice check",
        "Note what still feels unclear",
    ),
    DecisionType.REVISE.value: (
        "Revisit the key ideas for this area",
        "Attempt a short recall or practice set",
        "Mark what you recovered vs still shaky",
        "Schedule a lighter follow-up if needed",
    ),
    DecisionType.STRENGTHEN_CONFIDENCE.value: (
        "Review your last attempt briefly",
        "Practice the weakest sub-skill",
        "Explain the idea in your own words",
        "Confirm you feel clearer before moving on",
    ),
    DecisionType.SATISFY_PREREQUISITE.value: (
        "Study the prerequisite curriculum target",
        "Check understanding with a quick exercise",
        "Confirm the blocker is cleared",
        "Return to the dependent topic when ready",
    ),
    DecisionType.CONTINUE_PATH.value: (
        "Resume the curriculum area you were studying",
        "Complete the next natural chunk",
        "Capture one takeaway",
        "Stop at a clean boundary for next time",
    ),
}


def title_for(decision_type: str, curriculum_target: str) -> str:
    template = _DECISION_TITLES.get(
        decision_type, "Focus on {target}"
    )
    return template.format(target=_short_label(curriculum_target))


def summary_for(decision_type: str, curriculum_area: str) -> str:
    template = _DECISION_SUMMARIES.get(
        decision_type,
        "Focus on {area} based on your educational recommendation.",
    )
    return template.format(area=curriculum_area)


def outcome_for(expected_outcome: str) -> str:
    return _OUTCOME_COPY.get(
        expected_outcome,
        "Make measurable educational progress on this curriculum target",
    )


def motivation_for(decision_type: str) -> str:
    return _MOTIVATION.get(
        decision_type,
        "A focused study block moves you closer to exam readiness.",
    )


def next_steps_for(decision_type: str) -> tuple[str, ...]:
    return _NEXT_STEPS.get(
        decision_type,
        (
            "Open the recommended curriculum area",
            "Complete a focused study block",
            "Check understanding before finishing",
        ),
    )


def effort_label(minutes: int) -> str:
    mins = max(0, int(minutes))
    if mins <= 0:
        return "Flexible duration"
    if mins < 60:
        return f"About {mins} minutes"
    hours, rem = divmod(mins, 60)
    if rem == 0:
        unit = "hour" if hours == 1 else "hours"
        return f"About {hours} {unit}"
    return f"About {hours} h {rem} min"


def urgency_for(*, priority: float, decision_type: str) -> UrgencyLevel:
    """Map decision priority/type to presentation urgency (never mutates decision)."""
    p = float(priority)
    if decision_type == DecisionType.REVISE.value and p >= 0.55:
        return UrgencyLevel.CRITICAL
    if decision_type == DecisionType.SATISFY_PREREQUISITE.value and p >= 0.5:
        return UrgencyLevel.HIGH
    if p >= 0.75:
        return UrgencyLevel.CRITICAL
    if p >= 0.55:
        return UrgencyLevel.HIGH
    if p >= 0.35:
        return UrgencyLevel.MODERATE
    return UrgencyLevel.LOW


def prerequisite_explanation(
    *,
    decision_type: str,
    prerequisite_chain: tuple[str, ...],
) -> str:
    if decision_type == DecisionType.SATISFY_PREREQUISITE.value:
        if prerequisite_chain:
            chain = ", ".join(_short_label(p) for p in prerequisite_chain[:4])
            return (
                "This action clears a prerequisite blocker. "
                f"Related prerequisites considered: {chain}."
            )
        return (
            "This action clears a prerequisite so dependent curriculum can unlock."
        )
    if prerequisite_chain:
        chain = ", ".join(_short_label(p) for p in prerequisite_chain[:4])
        return f"Prerequisites already considered for this recommendation: {chain}."
    return "No outstanding prerequisite blocker was identified for this action."


def curriculum_area_label(curriculum_target: str) -> str:
    """Human-readable curriculum area from a stable id (presentation only)."""
    return _short_label(curriculum_target)


def _short_label(stable_id: str) -> str:
    raw = (stable_id or "").strip()
    if not raw:
        return "this curriculum area"
    # Prefer the final segment of dotted / path-like ids.
    for sep in (".", "/", ":"):
        if sep in raw:
            raw = raw.rsplit(sep, 1)[-1]
    return raw.replace("_", " ").strip() or "this curriculum area"
