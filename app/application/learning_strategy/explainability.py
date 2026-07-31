"""Explainability packaging for Learning Strategy recommendations (KWP-007).

Every recommendation answers WHY in student-safe language.
Never exposes Twin / Evidence Authority / Educational+ / FSM / calibration labels.
"""

from __future__ import annotations

from app.application.learning_strategy.dto import (
    STRATEGY_TITLES,
    ConfidenceCalibration,
    StrategyAction,
    StrategyEvidenceInput,
)
from app.application.learning_strategy.rules import StrategyDecision

_FORBIDDEN: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "educational+",
    "educational +",
    "evidence package",
    "over-confident",
    "overconfident",
    "under-confident",
    "underconfident",
    "calibration",
    "fsm",
    "runtime",
)


def recommendation_body(
    decision: StrategyDecision,
    evidence: StrategyEvidenceInput,
) -> str:
    """Short educational recommendation body (not a score)."""
    topic = evidence.topic_title or "today's topic"
    next_topic = evidence.next_topic_title
    action = decision.action

    if action is StrategyAction.ADVANCE_TOPIC:
        if next_topic:
            return f"Move forward to {next_topic} after today's solid work on {topic}."
        return f"You are ready to advance beyond {topic}."
    if action is StrategyAction.CONSOLIDATE_UNDERSTANDING:
        return (
            f"Stay with {topic} and consolidate the ideas behind today's "
            "missed practice before advancing."
        )
    if action is StrategyAction.IMMEDIATE_REINFORCEMENT:
        return (
            f"Reinforce {topic} in the next Session — today's practice "
            "needs another pass."
        )
    if action is StrategyAction.SCHEDULED_REVISION:
        return (
            f"Schedule a short revision of {topic} soon so earlier learning "
            "does not fade."
        )
    if action is StrategyAction.INCREASE_CHALLENGE:
        return (
            f"Increase challenge on the next step — {topic} looks stable "
            "enough for harder practice."
        )
    if action is StrategyAction.RECOVER_PRIOR_KNOWLEDGE:
        return (
            f"Recover prior knowledge on {topic} before introducing new "
            "material."
        )
    if action is StrategyAction.MAINTAIN_CURRENT_PACE:
        return f"Maintain your current pace on {topic}."
    if action is StrategyAction.SLOW_PROGRESSION:
        return (
            f"Slow progression on {topic} until understanding is clearer."
        )
    if action is StrategyAction.REPEAT_PRACTICE:
        return f"Repeat practice on {topic} before moving on."
    if action is StrategyAction.PRACTICE_FOR_CERTAINTY:
        return (
            f"Keep practising {topic} so your certainty matches what you "
            "already showed."
        )
    return f"Continue studying {topic}."


def explanation_for(
    decision: StrategyDecision,
    evidence: StrategyEvidenceInput,
) -> str:
    """Build the WHY sentence students should understand."""
    topic = evidence.topic_title or "this topic"
    lead = (
        evidence.learning_objectives[0]
        if evidence.learning_objectives
        else topic
    )
    next_topic = evidence.next_topic_title
    action = decision.action
    correct = evidence.practice_correct
    incorrect = evidence.practice_incorrect

    if action is StrategyAction.IMMEDIATE_REINFORCEMENT:
        if incorrect >= 2:
            text = (
                f"Today's Session revisits {lead} because repeated practice "
                "misses show they need reinforcement before introducing "
                "new material."
            )
        else:
            text = (
                f"Today's Session revisits {lead} because practice suggests "
                "reinforcement before moving on."
            )
    elif action is StrategyAction.CONSOLIDATE_UNDERSTANDING:
        if decision.calibration is ConfidenceCalibration.OVER_CONFIDENT:
            text = (
                f"Consolidate {lead} first — practice outcomes and how sure "
                "you felt do not yet line up, which often means a concept "
                "needs another careful pass."
            )
        else:
            text = (
                f"Consolidate {lead} because today's incorrect practice "
                "outweighed correct answers."
            )
    elif action is StrategyAction.PRACTICE_FOR_CERTAINTY:
        text = (
            f"Return to {lead} with light practice because you answered "
            "correctly but still seemed unsure — certainty grows from "
            "repeated success."
        )
    elif action is StrategyAction.ADVANCE_TOPIC:
        if next_topic:
            text = (
                f"Advance toward {next_topic} because today's practice on "
                f"{topic} was strong and study was accepted as complete."
            )
        else:
            text = (
                f"Advance from {topic} because practice was accurate and "
                "today's study was accepted."
            )
    elif action is StrategyAction.INCREASE_CHALLENGE:
        text = (
            f"Increase challenge after {topic} — recent sittings show "
            "sustained accurate practice."
        )
    elif action is StrategyAction.RECOVER_PRIOR_KNOWLEDGE:
        if evidence.abandoned:
            text = (
                f"Recover {topic} gently — the previous Session did not "
                "finish, so rebuilding continuity comes first."
            )
        elif evidence.days_since_topic_practice is not None:
            text = (
                f"Recover {topic} before new material — it has been "
                f"{evidence.days_since_topic_practice} days since solid "
                "practice here."
            )
        else:
            text = (
                f"Recover prior knowledge on {topic} because recent signals "
                "suggest it needs rebuilding first."
            )
    elif action is StrategyAction.SCHEDULED_REVISION:
        text = (
            f"Schedule revision for {topic} because a longer gap since "
            "practice raises the chance of fading recall."
        )
    elif action is StrategyAction.SLOW_PROGRESSION:
        text = (
            f"Slow progression on {topic} because recent finishes were "
            "partial or understanding still looks mixed."
        )
    elif action is StrategyAction.REPEAT_PRACTICE:
        text = (
            f"Repeat practice on {topic} because today's scored attempts "
            "were incorrect."
        )
    else:
        if correct or incorrect:
            text = (
                f"Maintain pace on {topic} — today's evidence does not "
                "call for a sharper change yet."
            )
        else:
            text = (
                f"Maintain your current pace on {topic} while more practice "
                "evidence accumulates."
            )

    return _scrub(text)


def title_for(action: StrategyAction) -> str:
    return STRATEGY_TITLES.get(action, "Maintain Current Pace")


def _scrub(text: str) -> str:
    lowered = text.lower()
    for fragment in _FORBIDDEN:
        if fragment in lowered:
            # Soften rather than fail — should not appear from our templates.
            text = text.replace(fragment, "").replace(fragment.title(), "")
    return " ".join(text.split()).strip()
