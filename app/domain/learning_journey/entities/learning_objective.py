"""Educational objective bound to a Learning Journey.

References curriculum learning outcomes by identity. Does not store
copyrighted syllabus prose. Objective kinds are educational intents
(Understand / Apply / Analyse / Review / Revise) — not mastery scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ObjectiveKind(StrEnum):
    """Educational intent of an objective within a topic journey.

    These are operational categories, not Bloom taxonomy claims and not
    competence scores.
    """

    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYSE = "analyse"
    REVIEW = "review"
    REVISE = "revise"


@dataclass(frozen=True)
class LearningObjective:
    """Educational objective the journey aims to address.

    Attributes:
        objective_id: Stable journey-scoped identity.
        curriculum_objective_ref: Official curriculum objective / outcome id.
        topic_id: Canonical curriculum topic identity.
        kind: Educational intent category.
        title: Short operational label (not copyrighted syllabus text).
        sequence_index: Ordering within the journey (0-based).
    """

    objective_id: str
    curriculum_objective_ref: str
    topic_id: str
    kind: ObjectiveKind
    title: str
    sequence_index: int = 0

    @classmethod
    def create(
        cls,
        objective_id: str,
        curriculum_objective_ref: str,
        topic_id: str,
        kind: ObjectiveKind | str,
        title: str,
        *,
        sequence_index: int = 0,
    ) -> LearningObjective:
        """Construct a LearningObjective after validating invariants.

        Raises:
            ValueError: When required identities or title are empty, or
                sequence_index is negative.
        """
        oid = _require_non_empty(objective_id, "objective_id")
        cref = _require_non_empty(
            curriculum_objective_ref, "curriculum_objective_ref"
        )
        tid = _require_non_empty(topic_id, "topic_id")
        label = _require_non_empty(title, "title")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        kind_value = kind if isinstance(kind, ObjectiveKind) else ObjectiveKind(kind)
        return cls(
            objective_id=oid,
            curriculum_objective_ref=cref,
            topic_id=tid,
            kind=kind_value,
            title=label,
            sequence_index=sequence_index,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
