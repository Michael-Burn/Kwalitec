"""PTP-003 Honest Product Communication — shared student-facing phrases.

Owns presentation honesty for educational claims. Does not recalculate
Estimated Knowledge, readiness, recommendations, or Evidence Authority ranks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimCategory(str, Enum):
    """Student-facing claim taxonomy (Product Communication Standard)."""

    OBSERVED_FACT = "Observed Fact"
    DERIVED_FACT = "Derived Fact"
    ESTIMATED_VALUE = "Estimated Value"
    UNAVAILABLE = "Unavailable"
    COMING_SOON = "Coming Soon"
    NOT_SUPPORTED = "Not Supported"


@dataclass(frozen=True)
class ClaimSpeech:
    """Minimal honesty packet for a student-facing claim."""

    category: ClaimCategory
    label: str
    basis: str


class ProductCommunicationService:
    """Canonical microcopy for Version 1 educational claim honesty."""

    # Estimated Knowledge
    ESTIMATED_KNOWLEDGE_LABEL = "Estimated Knowledge"
    ESTIMATED_KNOWLEDGE_BASIS = "Based on your recorded practice outcomes."
    ESTIMATED_KNOWLEDGE_BADGE_TITLE = ESTIMATED_KNOWLEDGE_BASIS
    ESTIMATED_KNOWLEDGE_EMPTY = (
        "Estimated knowledge appears here after practice results are recorded — "
        "completing a topic alone is not understanding."
    )
    ESTIMATED_KNOWLEDGE_EMPTY_STRONG = (
        "Strong estimated knowledge appears here as practice results accumulate."
    )

    # Estimated readiness
    ESTIMATED_READINESS_LABEL = "Estimated readiness"
    READINESS_UNAVAILABLE = (
        "We need more recorded practice before this estimate becomes available."
    )
    READINESS_UNAVAILABLE_BASIS = (
        "Estimated readiness uses syllabus coverage, Estimated Knowledge from "
        "recorded practice, and recent review habits."
    )
    ESTIMATED_READINESS_SELF_REPORT = (
        "Estimated readiness depends on practice results you recorded — "
        "not independently verified exam performance."
    )

    # Practice Results / Accuracy
    PRACTICE_RESULTS_BASIS = (
        "These results reflect the answers you recorded after today's study session."
    )
    PRACTICE_RESULTS_NOT_MASTERY = (
        "This is not a knowledge or mastery rating."
    )
    ACCURACY_BASIS = (
        "Accuracy is calculated from practice results you recorded — "
        "not a verified exam score."
    )
    ACCURACY_EMPTY = (
        "Accuracy appears after you record practice results in Study Sessions."
    )

    # Derived coverage
    SYLLABUS_COVERAGE_LABEL = "Syllabus coverage"

    # Coming Soon feature shells (not examination support — PTP-001 owns papers)
    LEARNING_OUTCOMES_UNAVAILABLE = "Not available yet"

    # Marketing / soft claims
    LOGIN_ANALYTICS_FEATURE = "Estimated readiness insights"

    @staticmethod
    def estimated_knowledge() -> ClaimSpeech:
        return ClaimSpeech(
            category=ClaimCategory.ESTIMATED_VALUE,
            label=ProductCommunicationService.ESTIMATED_KNOWLEDGE_LABEL,
            basis=ProductCommunicationService.ESTIMATED_KNOWLEDGE_BASIS,
        )

    @staticmethod
    def estimated_readiness_unavailable() -> ClaimSpeech:
        return ClaimSpeech(
            category=ClaimCategory.UNAVAILABLE,
            label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
            basis=ProductCommunicationService.READINESS_UNAVAILABLE,
        )

    @staticmethod
    def practice_results() -> ClaimSpeech:
        return ClaimSpeech(
            category=ClaimCategory.OBSERVED_FACT,
            label="Practice Results",
            basis=ProductCommunicationService.PRACTICE_RESULTS_BASIS,
        )

    @staticmethod
    def accuracy() -> ClaimSpeech:
        return ClaimSpeech(
            category=ClaimCategory.DERIVED_FACT,
            label="Accuracy",
            basis=ProductCommunicationService.ACCURACY_BASIS,
        )
