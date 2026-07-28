"""Inferred learning-state catalogue for Twin beliefs (EI-006)."""

from __future__ import annotations

from enum import StrEnum


class LearningState(StrEnum):
    """Discrete educational disposition derived from evidence-backed scores.

    States are mutually exclusive after deterministic precedence resolution.
    They never encode recommendations or mission intents.
    """

    UNKNOWN = "unknown"
    EXPLORING = "exploring"
    DEVELOPING = "developing"
    CONSOLIDATING = "consolidating"
    MASTERED = "mastered"
    REVISING = "revising"
    STRUGGLING = "struggling"
