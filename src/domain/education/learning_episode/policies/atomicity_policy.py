"""Policy enforcing Educational Atomicity on Learning Episodes.

Architecture Source
    EDUCATIONAL_ATOMICITY.md / LEARNING_EPISODE_INVARIANTS.md (E1, E11)
Concept
    Atomicity Policy
"""

from __future__ import annotations

import re

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.entities.episode_goal import EpisodeGoal

_NON_ATOMIC_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bentire\s+chapter\b",
        r"\ball\s+of\s+(the\s+)?chapter\b",
        r"\brevise\s+(the\s+)?whole\b",
        r"\ball\s+glms?\b",
        r"\beverything\s+weak\b",
        r"\bdo\s+chapter\s+\d+\b",
        r"\bwhole\s+subject\b",
        r"\bfinish\s+(the\s+)?chapter\b",
        r"\bmaster\s+the\s+topic\b",
        r"\ball\s+topics?\b",
    )
)

_MULTI_PURPOSE_CONNECTOR = re.compile(
    r"\b(?:and also|as well as|in addition to)\b",
    re.IGNORECASE,
)


class AtomicityPolicy:
    """Enforces one educational capability per Learning Episode."""

    @staticmethod
    def assert_atomic_goal(goal: EpisodeGoal) -> EpisodeGoal:
        """Reject chapter-sized or multi-purpose teaching goals."""
        if not isinstance(goal, EpisodeGoal):
            raise EducationalInvariantViolation(
                "atomicity requires an EpisodeGoal",
                invariant="AtomicityPolicy.goal.type",
            )
        AtomicityPolicy.assert_atomic_statement(goal.statement)
        AtomicityPolicy.assert_atomic_statement(goal.educational_purpose)
        statement_key = goal.statement.strip().casefold()
        purpose_key = goal.educational_purpose.strip().casefold()
        if statement_key != purpose_key:
            # Purpose and statement may differ in wording but must not fork aims.
            if _MULTI_PURPOSE_CONNECTOR.search(goal.educational_purpose):
                raise EducationalInvariantViolation(
                    "educational purpose must name one capability, not a bundle",
                    invariant="AtomicityPolicy.purpose.single",
                )
        return goal

    @staticmethod
    def assert_atomic_statement(statement: str) -> str:
        cleaned = (statement or "").strip()
        if not cleaned:
            raise EducationalInvariantViolation(
                "atomic statement must be non-empty",
                invariant="AtomicityPolicy.statement.non_empty",
            )
        for pattern in _NON_ATOMIC_PATTERNS:
            if pattern.search(cleaned):
                raise EducationalInvariantViolation(
                    "teaching goal violates Educational Atomicity "
                    "(one capability per episode)",
                    invariant="AtomicityPolicy.non_atomic_scope",
                )
        if _MULTI_PURPOSE_CONNECTOR.search(cleaned):
            raise EducationalInvariantViolation(
                "teaching goal appears to bundle multiple educational purposes",
                invariant="AtomicityPolicy.multi_purpose",
            )
        return cleaned

    @staticmethod
    def is_atomic_statement(statement: str) -> bool:
        """Return True when ``statement`` appears capability-scoped."""
        try:
            AtomicityPolicy.assert_atomic_statement(statement)
        except EducationalInvariantViolation:
            return False
        return True
