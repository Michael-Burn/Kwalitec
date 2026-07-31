"""Spaced revision decisions from educational evidence (KWP-007).

Timing vocabulary: Immediate / Tomorrow / This week / Later / No review.
Does not invent calendar dates — reuses evidence urgency patterns.
"""

from __future__ import annotations

from app.application.learning_strategy.dto import (
    SpacingDecision,
    StrategyAction,
    StrategyEvidenceInput,
)

# Align with Adaptive RevisionUrgency thresholds conceptually, plus NO_REVIEW.
_LONG_GAP_DAYS = 14
_MEDIUM_GAP_DAYS = 7


def decide_spacing(
    evidence: StrategyEvidenceInput,
    *,
    action: StrategyAction,
) -> tuple[SpacingDecision, str]:
    """Return (spacing decision, student-safe guidance)."""
    topic = evidence.topic_title or "this topic"
    incorrect = evidence.practice_incorrect
    correct = evidence.practice_correct
    days = evidence.days_since_topic_practice

    if action in {
        StrategyAction.IMMEDIATE_REINFORCEMENT,
        StrategyAction.CONSOLIDATE_UNDERSTANDING,
        StrategyAction.REPEAT_PRACTICE,
        StrategyAction.RECOVER_PRIOR_KNOWLEDGE,
    }:
        return (
            SpacingDecision.IMMEDIATE,
            f"Revisit {topic} in your next Session — today's practice needs "
            "reinforcement before new material.",
        )

    if action is StrategyAction.PRACTICE_FOR_CERTAINTY:
        return (
            SpacingDecision.TOMORROW,
            f"A short return to {topic} tomorrow will help certainty catch "
            "up with what you already showed.",
        )

    if action is StrategyAction.SLOW_PROGRESSION:
        return (
            SpacingDecision.TOMORROW,
            f"Keep {topic} close — tomorrow's Session should deepen "
            "understanding before advancing.",
        )

    if action is StrategyAction.SCHEDULED_REVISION or evidence.retention_risk:
        if days is not None and days >= _LONG_GAP_DAYS:
            return (
                SpacingDecision.LATER,
                f"Schedule a light return to {topic} later — it has been "
                "a while since solid practice.",
            )
        return (
            SpacingDecision.THIS_WEEK,
            f"Plan a short revision of {topic} this week to keep it fresh.",
        )

    if action is StrategyAction.ADVANCE_TOPIC and incorrect == 0 and correct > 0:
        if evidence.weak_topic or evidence.retention_risk:
            return (
                SpacingDecision.THIS_WEEK,
                f"You can advance, and still schedule a light check on "
                f"{topic} later this week.",
            )
        return (
            SpacingDecision.NO_REVIEW,
            f"{topic} does not need an immediate revisit — progress to the "
            "next focus when ready.",
        )

    if action is StrategyAction.INCREASE_CHALLENGE:
        return (
            SpacingDecision.NO_REVIEW,
            f"Keep moving — {topic} is stable enough for a harder stretch.",
        )

    if action is StrategyAction.MAINTAIN_CURRENT_PACE:
        if days is not None and days >= _MEDIUM_GAP_DAYS:
            return (
                SpacingDecision.THIS_WEEK,
                f"Maintain pace, and keep a light check on {topic} this week.",
            )
        if incorrect > 0:
            return (
                SpacingDecision.TOMORROW,
                f"A short revisit of {topic} tomorrow keeps today's gaps "
                "from widening.",
            )
        return (
            SpacingDecision.TOMORROW,
            f"Continue at the current pace — tomorrow picks up from {topic}.",
        )

    # Default: tomorrow when mixed signal, no review when empty.
    if incorrect > 0 or evidence.finish_verdict == "partially":
        return (
            SpacingDecision.TOMORROW,
            f"Return to {topic} tomorrow to consolidate today's Session.",
        )
    if correct > 0 and evidence.progress_advanced:
        return (
            SpacingDecision.NO_REVIEW,
            f"No immediate review required for {topic}.",
        )
    return (
        SpacingDecision.TOMORROW,
        f"Tomorrow's Session continues from {topic}.",
    )
