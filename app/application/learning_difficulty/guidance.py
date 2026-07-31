"""Student-safe difficulty / load guidance (KWP-009).

Never expose internal bands (very demanding, overloaded, cognitive load)
or psychological labels. Natural educational recommendations only.
"""

from __future__ import annotations

from app.application.learning_difficulty.dto import (
    LOAD_RECOMMENDATION_TITLES,
    DifficultyEvidenceInput,
    LoadRecommendation,
    ObjectiveComplexity,
    ObservedDifficulty,
)
from app.application.learning_difficulty.rules import DifficultyDecision

_FORBIDDEN: tuple[str, ...] = (
    "cognitive load",
    "mental load",
    "burnout",
    "anxiety",
    "fatigue",
    "overloaded",
    "very demanding",
    "very-demanding",
    "load points",
    "digital twin",
    "student twin",
    "evidence authority",
    "educational+",
    "fsm",
    "runtime",
    "psychological",
)


def title_for(recommendation: LoadRecommendation) -> str:
    return LOAD_RECOMMENDATION_TITLES[recommendation]


def guidance_for(
    decision: DifficultyDecision,
    evidence: DifficultyEvidenceInput,
) -> str:
    """Natural student guidance for a load recommendation."""
    topic = evidence.topic_title or "this topic"
    rec = decision.recommendation

    if rec is LoadRecommendation.REDUCE_SESSION_LENGTH:
        return (
            f"Keep the next Session on {topic} shorter — a focused "
            "reinforcement pass works better than a long stretch right now."
        )

    if rec is LoadRecommendation.SPLIT_TOPIC:
        return (
            f"Break {topic} into smaller pieces and master one part at a "
            "time before combining them."
        )

    if rec is LoadRecommendation.TAKE_CONSOLIDATION_SESSION:
        return (
            f"This topic has required more practice than recent topics. "
            f"A shorter reinforcement session is recommended before "
            f"progressing from {topic}."
        )

    if rec is LoadRecommendation.DECREASE_SPACING:
        return (
            f"Return to {topic} sooner than usual — closer practice will "
            "help today's work settle before moving on."
        )

    if rec is LoadRecommendation.INCREASE_SPACING:
        return (
            f"{topic} looks stable enough to leave a little more space "
            "before the next revisit."
        )

    if rec is LoadRecommendation.INCREASE_CHALLENGE:
        return (
            f"You handled {topic} comfortably — try a slightly harder "
            "stretch when you are ready."
        )

    if rec is LoadRecommendation.MAINTAIN_PACE:
        return (
            f"Keep the current pace on {topic} — today's demand looks "
            "in balance with recent Sessions."
        )

    # CONTINUE
    return (
        f"Continue with {topic} at a steady pace — recent practice shows "
        "you can keep moving without adding pressure."
    )


def explanation_for(
    decision: DifficultyDecision,
    evidence: DifficultyEvidenceInput,
) -> str:
    """Cause-level WHY for load / pacing — student-safe, no band labels."""
    topic = evidence.topic_title or "this topic"
    objective = decision.objective_complexity
    observed = decision.observed_difficulty
    incorrect = evidence.practice_incorrect
    reinforcement = evidence.reinforcement_session_count
    duration = evidence.session_duration_minutes

    # Prefer concrete evidence language over internal band names.
    if decision.recommendation is LoadRecommendation.TAKE_CONSOLIDATION_SESSION:
        if gap_language(objective, observed):
            return (
                f"{topic} is normally {objective_phrase(objective)}, but "
                f"today's practice made it feel harder — "
                f"{gap_language(objective, observed)}."
            )
        if reinforcement >= 1:
            return (
                f"{topic} has needed extra practice across recent Sessions, "
                "so consolidating before progressing protects understanding."
            )
        if incorrect >= 2:
            return (
                f"Misses on {topic} today show the material still needs a "
                "shorter reinforcement pass before new work."
            )
        return (
            f"Recent work on {topic} has been more demanding than usual, "
            "so a consolidation Session is the safer next step."
        )

    if decision.recommendation is LoadRecommendation.REDUCE_SESSION_LENGTH:
        if duration is not None and duration >= 50:
            return (
                f"Today's Session ran about {duration} minutes with "
                f"substantial practice demand on {topic} — shorter next "
                "time keeps quality high."
            )
        return (
            f"Recent practice on {topic} has been dense — a shorter "
            "Session will keep the next pass productive."
        )

    if decision.recommendation is LoadRecommendation.SPLIT_TOPIC:
        return (
            f"{topic} has taken several practice passes with repeated "
            "misses — working one part at a time reduces the load."
        )

    if decision.recommendation is LoadRecommendation.DECREASE_SPACING:
        if evidence.retention_risk:
            return (
                f"{topic} benefits from an earlier return so today's "
                "gains do not fade between Sessions."
            )
        return (
            f"Practice on {topic} still needs closer follow-up so gaps "
            "do not widen before the next Session."
        )

    if decision.recommendation is LoadRecommendation.INCREASE_SPACING:
        return (
            f"Strong, clean practice on {topic} supports leaving a little "
            "more space before the next revisit."
        )

    if decision.recommendation is LoadRecommendation.INCREASE_CHALLENGE:
        return (
            f"You answered today's practice on {topic} correctly with "
            "comfortable demand — a harder stretch is a natural next step."
        )

    if decision.recommendation is LoadRecommendation.MAINTAIN_PACE:
        return (
            f"Demand on {topic} looks balanced with recent Sessions — "
            "keeping the current pace is appropriate."
        )

    if evidence.recovered_after_misses or evidence.recovered_after_difficult:
        return (
            f"Earlier misses on {topic} were followed by correct answers — "
            "continuing steadily builds on that recovery."
        )

    return (
        f"Today's practice on {topic} supports continuing without "
        "changing pace or Session length."
    )


def objective_phrase(objective: ObjectiveComplexity) -> str:
    """Student-safe phrase for objective complexity (no internal jargon)."""
    return {
        ObjectiveComplexity.LIGHT: "a lighter topic",
        ObjectiveComplexity.MODERATE: "a moderately demanding topic",
        ObjectiveComplexity.DEMANDING: "a demanding topic",
        ObjectiveComplexity.INTENSIVE: "an intensive topic",
        ObjectiveComplexity.UNKNOWN: "this topic",
    }[objective]


def gap_language(
    objective: ObjectiveComplexity,
    observed: ObservedDifficulty,
) -> str:
    """Explain objective vs observed gap without band labels."""
    if objective in {
        ObjectiveComplexity.LIGHT,
        ObjectiveComplexity.MODERATE,
    } and observed in {
        ObservedDifficulty.DEMANDING,
        ObservedDifficulty.VERY_DEMANDING,
    }:
        return "more practice than usual was needed"
    if (
        objective is ObjectiveComplexity.DEMANDING
        and observed is ObservedDifficulty.VERY_DEMANDING
    ):
        return "even the usual demand ran high today"
    return ""


def scrub(text: str) -> str:
    """Remove forbidden fragments from student-facing copy."""
    lowered = text.lower()
    for fragment in _FORBIDDEN:
        if fragment in lowered:
            # Soft scrub: drop the sentence containing the fragment.
            parts = [p.strip() for p in text.replace("—", ".").split(".") if p.strip()]
            kept = [p for p in parts if fragment not in p.lower()]
            return ". ".join(kept).strip() or text
    return text
