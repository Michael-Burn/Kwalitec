"""Basic retrieval intent detection (deterministic, no LLM)."""

from __future__ import annotations

from enum import StrEnum


class QueryIntent(StrEnum):
    """Coarse educational intent inferred from a retrieval query."""

    GENERAL = "general"
    DEFINITION = "definition"
    FORMULA = "formula"
    EXAMPLE = "example"
    PRACTICE = "practice"
    PREREQUISITE = "prerequisite"
    RELATED = "related"
    LEARNING_OBJECTIVE = "learning_objective"


_INTENT_KEYWORDS: tuple[tuple[QueryIntent, tuple[str, ...]], ...] = (
    (
        QueryIntent.DEFINITION,
        ("define", "definition", "what is", "meaning of", "means"),
    ),
    (
        QueryIntent.FORMULA,
        ("formula", "equation", "calculate", "compute", "expression"),
    ),
    (
        QueryIntent.EXAMPLE,
        ("example", "worked", "illustrat", "demo"),
    ),
    (
        QueryIntent.PRACTICE,
        ("practice", "question", "exercise", "past paper", "exam question"),
    ),
    (
        QueryIntent.PREREQUISITE,
        ("prerequisite", "prereq", "depends on", "before", "require"),
    ),
    (
        QueryIntent.RELATED,
        ("related", "similar", "connected", "neighbour", "neighbor"),
    ),
    (
        QueryIntent.LEARNING_OBJECTIVE,
        ("learning objective", "objective", "outcome", "lo "),
    ),
)


def detect_intent(text: str) -> QueryIntent:
    """Detect a basic query intent from free text.

    Deterministic keyword scan. First match wins; otherwise GENERAL.
    """
    lowered = (text or "").strip().lower()
    if not lowered:
        return QueryIntent.GENERAL
    for intent, keywords in _INTENT_KEYWORDS:
        for keyword in keywords:
            if keyword in lowered:
                return intent
    return QueryIntent.GENERAL
