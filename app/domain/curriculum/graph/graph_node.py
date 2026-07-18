"""GraphNode — topic node within the Curriculum Graph."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.value_objects.topic_difficulty import TopicDifficulty
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class GraphNode:
    """Node representing a Topic in the Curriculum Graph.

    Attributes:
        topic_id: Topic identity.
        name: Operational topic label.
        difficulty: Relative difficulty band.
        estimated_effort_minutes: Structural effort estimate.
        payload: Optional Topic entity (structure only).
    """

    topic_id: TopicId
    name: str
    difficulty: TopicDifficulty = TopicDifficulty.FOUNDATIONAL
    estimated_effort_minutes: int = 0
    payload: Topic | None = field(default=None, compare=False)

    @classmethod
    def from_topic(cls, topic: Topic) -> GraphNode:
        """Build a node from a Topic entity."""
        return cls(
            topic_id=topic.topic_id,
            name=topic.name,
            difficulty=topic.difficulty,
            estimated_effort_minutes=topic.estimated_effort_minutes,
            payload=topic,
        )

    @classmethod
    def create(
        cls,
        topic_id: str | TopicId,
        name: str,
        *,
        difficulty: TopicDifficulty | str = TopicDifficulty.FOUNDATIONAL,
        estimated_effort_minutes: int = 0,
        payload: Topic | None = None,
    ) -> GraphNode:
        """Construct a GraphNode with identity validation via Topic when needed."""
        from app.domain.curriculum.entities._text import require_non_empty

        tid = TopicId.of(topic_id)
        label = require_non_empty(name, "name")
        if estimated_effort_minutes < 0:
            raise ValueError("estimated_effort_minutes must be non-negative")
        difficulty_value = (
            difficulty
            if isinstance(difficulty, TopicDifficulty)
            else TopicDifficulty(difficulty)
        )
        return cls(
            topic_id=tid,
            name=label,
            difficulty=difficulty_value,
            estimated_effort_minutes=estimated_effort_minutes,
            payload=payload,
        )
