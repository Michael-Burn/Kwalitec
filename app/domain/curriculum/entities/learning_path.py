"""LearningPath — one valid ordered educational route through topics."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class LearningPath:
    """Ordered route of topic identities representing one valid pathway.

    Example structural route (illustrative labels only)::

        Probability → Random Variables → Expectation → Variance → MGFs

    Attributes:
        path_id: Stable path identity.
        name: Operational label.
        topic_ids: Ordered topic identities along the path.
        curriculum_id: Optional owning curriculum identity string.
        description: Optional short operational note (not syllabus prose).
    """

    path_id: str
    name: str
    topic_ids: tuple[TopicId, ...] = field(default_factory=tuple)
    curriculum_id: str | None = None
    description: str | None = None

    @classmethod
    def create(
        cls,
        path_id: str,
        name: str,
        topic_ids: list[str | TopicId] | tuple[str | TopicId, ...] | None = None,
        *,
        curriculum_id: str | None = None,
        description: str | None = None,
    ) -> LearningPath:
        """Construct a LearningPath after validating invariants.

        Raises:
            ValueError: On empty identities or duplicate topic ids.
        """
        pid = require_non_empty(path_id, "path_id")
        label = require_non_empty(name, "name")
        ids = tuple(TopicId.of(t) for t in (topic_ids or ()))
        if len(set(ids)) != len(ids):
            raise ValueError("learning path topic_ids must be unique")
        return cls(
            path_id=pid,
            name=label,
            topic_ids=ids,
            curriculum_id=optional_non_empty(curriculum_id),
            description=optional_non_empty(description),
        )

    def length(self) -> int:
        """Number of topics on the path."""
        return len(self.topic_ids)

    def index_of(self, topic_id: str | TopicId) -> int | None:
        """0-based index of topic on the path, or None if absent."""
        tid = TopicId.of(topic_id)
        try:
            return self.topic_ids.index(tid)
        except ValueError:
            return None

    def next_after(self, topic_id: str | TopicId) -> TopicId | None:
        """Next topic after ``topic_id``, or None at end / absent."""
        idx = self.index_of(topic_id)
        if idx is None or idx + 1 >= len(self.topic_ids):
            return None
        return self.topic_ids[idx + 1]

    def previous_before(self, topic_id: str | TopicId) -> TopicId | None:
        """Previous topic before ``topic_id``, or None at start / absent."""
        idx = self.index_of(topic_id)
        if idx is None or idx == 0:
            return None
        return self.topic_ids[idx - 1]

    def with_topic(self, topic_id: str | TopicId) -> LearningPath:
        """Append a topic to the end of the path."""
        tid = TopicId.of(topic_id)
        if tid in self.topic_ids:
            raise ValueError("learning path topic_ids must be unique")
        return LearningPath(
            path_id=self.path_id,
            name=self.name,
            topic_ids=(*self.topic_ids, tid),
            curriculum_id=self.curriculum_id,
            description=self.description,
        )
