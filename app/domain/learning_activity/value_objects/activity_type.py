"""Extensible vocabulary of Learning Activity kinds.

New activity types may be added without changing engine orchestration.
Unknown or future types resolve via ``ActivityType.resolve`` / CUSTOM.
"""

from __future__ import annotations

from enum import StrEnum


class ActivityType(StrEnum):
    """Canonical Learning Activity type vocabulary.

    Values are stable snake_case identifiers. Orchestration dispatches on
    structural type tags only — never on generated study content.
    """

    INTRODUCTION = "introduction"
    CONCEPT_LEARNING = "concept_learning"
    WORKED_EXAMPLE = "worked_example"
    GUIDED_PRACTICE = "guided_practice"
    INDEPENDENT_PRACTICE = "independent_practice"
    KNOWLEDGE_CHECK = "knowledge_check"
    REFLECTION = "reflection"
    SUMMARY = "summary"
    SPACED_RECALL = "spaced_recall"
    NEXT_INTENTION = "next_intention"
    REVIEW = "review"
    CUSTOM = "custom"

    @classmethod
    def resolve(cls, value: ActivityType | str) -> ActivityType:
        """Resolve a type token to an ``ActivityType``.

        Known members are returned as-is. Unrecognised strings map to CUSTOM
        so future activity kinds do not break existing orchestration.
        """
        if isinstance(value, ActivityType):
            return value
        token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
        if not token:
            return cls.CUSTOM
        try:
            return cls(token)
        except ValueError:
            # Accept UPPER_SNAKE enum names as well as values.
            upper = token.upper()
            if upper in cls.__members__:
                return cls[upper]
            return cls.CUSTOM

    @classmethod
    def known_values(cls) -> tuple[str, ...]:
        """Stable ordered catalogue of known activity type values."""
        return tuple(member.value for member in cls)
