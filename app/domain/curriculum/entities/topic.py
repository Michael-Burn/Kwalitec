"""Topic — atomic educational concept in the curriculum graph.

Models structure only. Must not store copyrighted notes, questions, or
official syllabus prose.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.topic_difficulty import TopicDifficulty
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Topic:
    """One educational concept within a curriculum.

    Attributes:
        topic_id: Unique topic identity.
        name: Short operational label (not copyrighted syllabus text).
        difficulty: Relative difficulty band.
        estimated_effort_minutes: Structural effort estimate in minutes.
        learning_objective_refs: Ordered curriculum objective identity refs.
        journey_ref: Optional Learning Journey identity binding.
        module_id: Optional owning module identity.
        sequence_index: Order within the owning module (0-based).
        metadata: Free-form structural key/value pairs (no content blobs).
    """

    topic_id: TopicId
    name: str
    difficulty: TopicDifficulty = TopicDifficulty.FOUNDATIONAL
    estimated_effort_minutes: int = 0
    learning_objective_refs: tuple[str, ...] = field(default_factory=tuple)
    journey_ref: str | None = None
    module_id: str | None = None
    sequence_index: int = 0
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str | TopicId,
        name: str,
        *,
        difficulty: TopicDifficulty | str = TopicDifficulty.FOUNDATIONAL,
        estimated_effort_minutes: int = 0,
        learning_objective_refs: list[str] | tuple[str, ...] | None = None,
        journey_ref: str | None = None,
        module_id: str | None = None,
        sequence_index: int = 0,
        metadata: dict[str, str] | list[tuple[str, str]] | None = None,
    ) -> Topic:
        """Construct a Topic after validating invariants.

        Raises:
            ValueError: On empty identities/name, negative effort/index, or
                empty objective refs.
        """
        tid = TopicId.of(topic_id)
        label = require_non_empty(name, "name")
        if estimated_effort_minutes < 0:
            raise ValueError("estimated_effort_minutes must be non-negative")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        difficulty_value = (
            difficulty
            if isinstance(difficulty, TopicDifficulty)
            else TopicDifficulty(difficulty)
        )
        refs: list[str] = []
        for ref in learning_objective_refs or ():
            refs.append(require_non_empty(ref, "learning_objective_refs item"))
        if len(set(refs)) != len(refs):
            raise ValueError("learning_objective_refs must be unique")
        meta_pairs = _normalize_metadata(metadata)
        return cls(
            topic_id=tid,
            name=label,
            difficulty=difficulty_value,
            estimated_effort_minutes=estimated_effort_minutes,
            learning_objective_refs=tuple(refs),
            journey_ref=optional_non_empty(journey_ref),
            module_id=optional_non_empty(module_id),
            sequence_index=sequence_index,
            metadata=meta_pairs,
        )

    @property
    def id(self) -> str:
        """String form of topic identity."""
        return self.topic_id.value


def _normalize_metadata(
    metadata: dict[str, str] | list[tuple[str, str]] | None,
) -> tuple[tuple[str, str], ...]:
    if metadata is None:
        return ()
    if isinstance(metadata, dict):
        items = list(metadata.items())
    else:
        items = list(metadata)
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for key, value in items:
        k = require_non_empty(key, "metadata key")
        v = require_non_empty(value, "metadata value")
        if k in seen:
            raise ValueError("metadata keys must be unique")
        seen.add(k)
        pairs.append((k, v))
    return tuple(pairs)
