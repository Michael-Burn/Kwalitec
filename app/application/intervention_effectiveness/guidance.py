"""Student-safe intervention effectiveness feedback (KWP-010).

Natural educational language only — never verdict labels, scores,
percentages, or authority jargon.
"""

from __future__ import annotations

from app.application.intervention_effectiveness.dto import (
    EffectivenessEvidenceInput,
    EffectivenessVerdict,
    InterventionKind,
)
from app.application.intervention_effectiveness.rules import EffectivenessDecision

# Authority / psych jargon — never reach students.
_FORBIDDEN_AUTHORITY: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "educational+",
    "fsm",
    "runtime",
    "cognitive load",
    "overloaded",
    "very demanding",
    "load points",
)

# Verdict / score vocabulary — must not appear in student feedback.
_FORBIDDEN_VERDICT: tuple[str, ...] = (
    "recommendation effective",
    "recommendation partially effective",
    "recommendation ineffective",
    "insufficient evidence",
    "verdict",
    "effectiveness score",
)


def feedback_for(
    decision: EffectivenessDecision,
    evidence: EffectivenessEvidenceInput,
) -> str:
    """Natural student feedback about whether prior guidance helped."""
    if decision.verdict is EffectivenessVerdict.INSUFFICIENT_EVIDENCE:
        return ""

    topic = evidence.topic_title or evidence.prior.topic_title or "this topic"
    kind = decision.intervention_kind
    verdict = decision.verdict

    if kind is InterventionKind.CONSOLIDATION:
        return _consolidation_copy(verdict, topic)
    if kind is InterventionKind.REINFORCEMENT:
        return _reinforcement_copy(verdict, topic)
    if kind is InterventionKind.REDUCE_SESSION_LENGTH:
        return _reduce_length_copy(verdict, topic)
    if kind is InterventionKind.INCREASE_SPACING:
        return _increase_spacing_copy(verdict, topic)
    if kind is InterventionKind.DECREASE_SPACING:
        return _decrease_spacing_copy(verdict, topic)
    if kind is InterventionKind.INCREASE_CHALLENGE:
        return _challenge_copy(verdict, topic)
    if kind is InterventionKind.RECOVERY:
        return _recovery_copy(verdict, topic)
    if kind is InterventionKind.SLOW_PROGRESSION:
        return _slow_copy(verdict, topic)
    if kind is InterventionKind.ADVANCE:
        return _advance_copy(verdict, topic)
    return _maintain_copy(verdict, topic)


def explanation_for(
    decision: EffectivenessDecision,
    evidence: EffectivenessEvidenceInput,
) -> str:
    """Brief founder/audit-adjacent explanation (student-safe phrasing)."""
    if decision.verdict is EffectivenessVerdict.INSUFFICIENT_EVIDENCE:
        return (
            "Not enough follow-up practice yet to judge whether the "
            "previous recommendation helped."
        )
    topic = evidence.topic_title or evidence.prior.topic_title or "this topic"
    kind = decision.intervention_kind.value.replace("_", " ")
    return (
        f"Follow-up practice on {topic} was compared with the earlier "
        f"{kind} recommendation."
    )


def scrub(text: str) -> str:
    """Remove forbidden fragments from student copy."""
    out = text or ""
    lowered = out.lower()
    for fragment in (*_FORBIDDEN_AUTHORITY, *_FORBIDDEN_VERDICT):
        idx = lowered.find(fragment)
        while idx >= 0:
            out = out[:idx] + out[idx + len(fragment) :]
            lowered = out.lower()
            idx = lowered.find(fragment)
    return " ".join(out.split()).strip()


def _consolidation_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"The additional reinforcement appears to have strengthened "
            f"your understanding of {topic}."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Consolidation on {topic} helped a little. Keep reinforcing "
            "the parts that still feel unsettled."
        )
    return (
        f"Extra consolidation on {topic} has not settled yet: another "
        "focused pass is worth trying before moving on."
    )


def _reinforcement_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"The additional reinforcement appears to have strengthened "
            f"your understanding of {topic}."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Reinforcement on {topic} reduced some mistakes. A little "
            "more practice should lock it in."
        )
    return (
        f"Mistakes on {topic} are still showing up after reinforcement. "
        "slow down and revisit the core steps."
    )


def _reduce_length_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Shorter Sessions on {topic} appear to have helped you stay "
            "focused without losing ground."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Keeping {topic} Sessions shorter is helping somewhat. "
            "stay with focused, shorter passes for now."
        )
    return (
        f"Shorter Sessions alone have not eased the load on {topic} yet. "
        "pair them with closer reinforcement."
    )


def _increase_spacing_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Leaving a little more space before revisiting {topic} still "
            "left your understanding intact."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Spacing on {topic} looks workable so far. Keep watching "
            "how well it holds after the gap."
        )
    return (
        f"Wider spacing on {topic} did not hold. Return sooner next time."
    )


def _decrease_spacing_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Coming back to {topic} sooner appears to have helped today's "
            "practice settle."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Closer practice on {topic} is helping a little. Keep the "
            "gap short for now."
        )
    return (
        f"Closer revisits on {topic} have not cleared the difficulty yet. "
        "focus on the steps that still slip."
    )


def _challenge_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Taking on a tougher pass of {topic} went well. Your "
            "performance held under more challenge."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"The harder pass on {topic} was partly successful: stretch "
            "gently on the next Session."
        )
    return (
        f"The harder pass on {topic} was a stretch too far for now. "
        "return to a steadier level before challenging again."
    )


def _recovery_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Returning to {topic} rebuilt momentum. You are back on "
            "firmer ground."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"You re-engaged with {topic}. Keep the recovery Sessions "
            "steady until it feels solid again."
        )
    return (
        f"Recovery on {topic} still needs attention: start with a short, "
        "honest practice pass."
    )


def _slow_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Slowing the pace on {topic} appears to have made Sessions "
            "more complete and steady."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"A slower pace on {topic} is helping somewhat: finish one "
            "clear block before starting another."
        )
    return (
        f"Slowing down has not stabilised {topic} yet: shorten the next "
        "Session and finish what you start."
    )


def _advance_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Moving forward from {topic} looks well supported by today's "
            "practice."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Progress from {topic} is underway: confirm the foundations "
            "once more if anything still feels soft."
        )
    return (
        f"Advancing from {topic} looks early: reinforce it before taking "
        "the next step."
    )


def _maintain_copy(verdict: EffectivenessVerdict, topic: str) -> str:
    if verdict is EffectivenessVerdict.EFFECTIVE:
        return (
            f"Keeping a steady pace on {topic} continues to serve you well."
        )
    if verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
        return (
            f"Your current pace on {topic} is holding: stay consistent."
        )
    return (
        f"The current pace on {topic} is slipping: adjust with closer "
        "reinforcement or a shorter Session."
    )
