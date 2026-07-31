"""Student-safe diagnostic guidance — never expose category labels (KWP-008).

Internal categories identify probable causes; learners receive actionable
guidance only (e.g. "Review discount factors before continuing with annuities.").
"""

from __future__ import annotations

from app.application.learning_diagnostics.dto import (
    DiagnosticCategory,
    DiagnosticEvidenceInput,
)

_FORBIDDEN: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "educational+",
    "educational +",
    "evidence package",
    "prerequisite weakness",
    "conceptual misunderstanding",
    "formula recall weakness",
    "calculation accuracy",
    "reading interpretation",
    "exam technique",
    "confidence mismatch",
    "retention decay",
    "inconsistent practice",
    "over-confident",
    "overconfident",
    "under-confident",
    "underconfident",
    "calibration",
    "fsm",
    "runtime",
)


def guidance_for(
    category: DiagnosticCategory,
    evidence: DiagnosticEvidenceInput,
    *,
    related_topic: str = "",
    mismatch_polarity: str = "",
) -> str:
    """Actionable student guidance for a diagnostic category."""
    topic = evidence.topic_title or "this topic"
    prereq = (related_topic or evidence.prerequisite_title or "").strip()
    dependent = (evidence.dependent_topic_title or "").strip()
    objective = (
        evidence.learning_objectives[0]
        if evidence.learning_objectives
        else topic
    )

    if category is DiagnosticCategory.PREREQUISITE_WEAKNESS:
        if prereq and (dependent or topic):
            focus = dependent or topic
            return f"Review {prereq} before continuing with {focus}."
        if prereq:
            return f"Review {prereq} before continuing with new material."
        return (
            f"Revisit the earlier building blocks for {topic} before "
            "pushing further."
        )

    if category is DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING:
        return (
            f"Revisit the core idea behind {objective} — today's answers "
            "suggest the concept needs another careful pass."
        )

    if category is DiagnosticCategory.FORMULA_RECALL_WEAKNESS:
        return (
            f"Refresh the key formula for {objective}, then try a short "
            "practice set from memory."
        )

    if category is DiagnosticCategory.CALCULATION_ACCURACY:
        return (
            f"Slow down on the arithmetic for {topic} — check each "
            "calculation step before submitting."
        )

    if category is DiagnosticCategory.READING_INTERPRETATION:
        return (
            f"Re-read the material on {topic} carefully and underline what "
            "the question is asking before practising again."
        )

    if category is DiagnosticCategory.EXAM_TECHNIQUE:
        return (
            f"Practise completing {topic} under clearer steps — finish "
            "the method, then check the answer."
        )

    if category is DiagnosticCategory.CONFIDENCE_MISMATCH:
        if mismatch_polarity == "under":
            return (
                f"Your answers on {topic} were stronger than how sure you "
                "felt — keep practising so certainty catches up."
            )
        if mismatch_polarity == "over":
            return (
                f"Check assumptions on {topic} carefully before moving on — "
                "certainty alone is not understanding."
            )
        return (
            f"Align how sure you feel with how {topic} practice is going — "
            "honest self-check helps tomorrow's Session."
        )

    if category is DiagnosticCategory.RETENTION_DECAY:
        return (
            f"Return briefly to {topic} soon — a longer gap often fades "
            "recall."
        )

    if category is DiagnosticCategory.INCONSISTENT_PRACTICE:
        return (
            f"Keep a steadier study rhythm on {topic} — shorter, regular "
            "Sessions beat occasional long ones."
        )

    if category is DiagnosticCategory.IMPROVING_UNDERSTANDING:
        return (
            f"Keep building on {topic} — correct answers after earlier "
            "misses show understanding is improving."
        )

    if category is DiagnosticCategory.STRONG_PERFORMANCE:
        if evidence.next_topic_title:
            return (
                f"Carry today's strength on {topic} into "
                f"{evidence.next_topic_title}."
            )
        return f"Continue from a strong base on {topic}."

    return f"Continue studying {topic} while more practice results accumulate."


def explanation_for(
    category: DiagnosticCategory,
    evidence: DiagnosticEvidenceInput,
    *,
    related_topic: str = "",
    mismatch_polarity: str = "",
) -> str:
    """Cause-level WHY in learner language (no category labels)."""
    topic = evidence.topic_title or "this topic"
    prereq = (related_topic or evidence.prerequisite_title or "").strip()
    incorrect = evidence.practice_incorrect
    correct = evidence.practice_correct

    if category is DiagnosticCategory.PREREQUISITE_WEAKNESS:
        if prereq and evidence.strong_prerequisite:
            text = (
                f"Practice on {topic} struggled even though earlier work on "
                f"{prereq} looked solid — the link between them needs "
                "another pass."
            )
        elif prereq:
            text = (
                f"Misses on {topic} often trace back to gaps in {prereq}, "
                "so rebuilding that foundation comes first."
            )
        else:
            text = (
                f"Repeated misses on {topic} point to earlier building "
                "blocks that need reinforcement first."
            )
    elif category is DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING:
        text = (
            f"Incorrect practice on {topic} with high certainty often means "
            "a concept is still unsettled rather than a simple slip."
        )
    elif category is DiagnosticCategory.FORMULA_RECALL_WEAKNESS:
        text = (
            f"Numeric practice on {topic} missed in a pattern that fits "
            "forgetting a formula more than misreading the question."
        )
    elif category is DiagnosticCategory.CALCULATION_ACCURACY:
        text = (
            f"The method direction on {topic} looks present, but calculation "
            "steps did not land cleanly."
        )
    elif category is DiagnosticCategory.READING_INTERPRETATION:
        if evidence.reading_skipped:
            text = (
                f"Practice on {topic} was weak after reading was skipped or "
                "cut short — interpretation of the material needs another "
                "look."
            )
        else:
            text = (
                f"Practice misses on {topic} after reading suggest the "
                "question wording or key idea was not fully taken in."
            )
    elif category is DiagnosticCategory.EXAM_TECHNIQUE:
        text = (
            f"Partial finishes and mixed practice on {topic} suggest "
            "method completion and checking, not only content gaps."
        )
    elif category is DiagnosticCategory.CONFIDENCE_MISMATCH:
        if mismatch_polarity == "under":
            text = (
                f"Performance on {topic} outpaced how sure you felt — "
                "knowledge looks stronger than perceived."
            )
        elif mismatch_polarity == "over":
            text = (
                f"Certainty on {topic} ran ahead of practice outcomes — "
                "a careful concept check is warranted."
            )
        else:
            text = (
                f"How sure you felt about {topic} and how practice went "
                "do not yet line up."
            )
    elif category is DiagnosticCategory.RETENTION_DECAY:
        if evidence.days_since_topic_practice is not None:
            text = (
                f"It has been {evidence.days_since_topic_practice} days "
                f"since solid practice on {topic}, which raises the chance "
                "of fading recall."
            )
        else:
            text = (
                f"Recent signals on {topic} suggest earlier learning is "
                "fading and needs a short refresh."
            )
    elif category is DiagnosticCategory.INCONSISTENT_PRACTICE:
        text = (
            f"Recent study on {topic} has been uneven — mixed finishes "
            "and gaps make progress harder to hold."
        )
    elif category is DiagnosticCategory.IMPROVING_UNDERSTANDING:
        text = (
            f"You reached correct answers on {topic} after earlier misses "
            f"({correct} correct, {incorrect} to revisit) — understanding "
            "is moving in the right direction."
        )
    elif category is DiagnosticCategory.STRONG_PERFORMANCE:
        text = (
            f"Accurate practice and accepted study on {topic} show solid "
            "grasp for this sitting."
        )
    else:
        text = (
            f"Today's evidence on {topic} is still thin for a sharper "
            "cause diagnosis."
        )

    return _scrub(text)


def _scrub(text: str) -> str:
    lowered = text.lower()
    for fragment in _FORBIDDEN:
        if fragment in lowered:
            text = text.replace(fragment, "").replace(fragment.title(), "")
    return " ".join(text.split()).strip()
