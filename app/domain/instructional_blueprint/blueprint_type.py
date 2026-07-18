"""Catalogue of instructional blueprint kinds.

Blueprints describe HOW a topic should be taught structurally.
They never encode syllabus content, questions, or student state.
"""

from __future__ import annotations

from enum import StrEnum


class BlueprintType(StrEnum):
    """Canonical instructional blueprint type vocabulary.

    Values are stable snake_case identifiers. Selection and compilation
    dispatch on structural type tags only — never on generated study content.
    """

    CONCEPT_MASTERY = "concept_mastery"
    CALCULATION_INTENSIVE = "calculation_intensive"
    THEORY_HEAVY = "theory_heavy"
    REVISION = "revision"
    MIXED_PRACTICE = "mixed_practice"
    EXAM_PRACTICE = "exam_practice"
    CASE_STUDY = "case_study"
    CUSTOM = "custom"

    @classmethod
    def resolve(cls, value: BlueprintType | str) -> BlueprintType:
        """Resolve a type token to a ``BlueprintType``.

        Known members are returned as-is. Unrecognised strings map to CUSTOM
        so future blueprint kinds do not break existing orchestration.
        """
        if isinstance(value, BlueprintType):
            return value
        token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
        if not token:
            return cls.CUSTOM
        try:
            return cls(token)
        except ValueError:
            upper = token.upper()
            if upper in cls.__members__:
                return cls[upper]
            return cls.CUSTOM

    @classmethod
    def known_values(cls) -> tuple[str, ...]:
        """Stable ordered catalogue of known blueprint type values."""
        return tuple(member.value for member in cls)

    @classmethod
    def known_members(cls) -> tuple[BlueprintType, ...]:
        """Stable ordered catalogue of known blueprint type members."""
        return tuple(cls)
