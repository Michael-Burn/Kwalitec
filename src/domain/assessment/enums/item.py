"""Question / item taxonomy and related policies.

Architecture Source
    knowledge/product/AP-002/QUESTION_MODEL.md
"""

from __future__ import annotations

from enum import StrEnum


class ItemType(StrEnum):
    """Assessment item types (evidence instruments, not exam items)."""

    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_RESPONSE = "multiple_response"
    NUMERIC = "numeric"
    FORMULA = "formula"
    FREE_TEXT = "free_text"
    WORKED_SOLUTION = "worked_solution"
    CONFIDENCE_RATING = "confidence_rating"
    REFLECTION = "reflection"
    CONCEPT_LINKING = "concept_linking"


class KnowledgeLevel(StrEnum):
    """Curriculum-aligned knowledge band for item selection metadata."""

    RECALL = "recall"
    UNDERSTANDING = "understanding"
    APPLICATION = "application"
    ANALYSIS = "analysis"


class HintPolicy(StrEnum):
    """Whether hints may be revealed during an item."""

    NONE = "none"
    AVAILABLE = "available"
    STAGED = "staged"


class RetryPolicy(StrEnum):
    """Whether retries are permitted before a committed response."""

    NONE = "none"
    LIMITED = "limited"
    UNLIMITED = "unlimited"
