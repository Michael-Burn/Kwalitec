"""Module — ordered container of Topics within a Subject."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities._text import require_non_empty
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Module:
    """Ordered group of Topics within a Subject.

    Attributes:
        module_id: Stable module identity.
        name: Operational label (not copyrighted syllabus text).
        topics: Ordered topics belonging to this module.
        sequence_index: Order within the owning subject (0-based).
        subject_id: Optional owning subject identity.
    """

    module_id: str
    name: str
    topics: tuple[Topic, ...] = field(default_factory=tuple)
    sequence_index: int = 0
    subject_id: str | None = None

    @classmethod
    def create(
        cls,
        module_id: str,
        name: str,
        *,
        topics: list[Topic] | tuple[Topic, ...] | None = None,
        sequence_index: int = 0,
        subject_id: str | None = None,
    ) -> Module:
        """Construct a Module after validating invariants.

        Raises:
            ValueError: On empty identities, negative index, duplicate topic
                ids, or topic module_id mismatch.
        """
        mid = require_non_empty(module_id, "module_id")
        label = require_non_empty(name, "name")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        sid = (
            None
            if subject_id is None
            else require_non_empty(subject_id, "subject_id")
        )
        topics_t = tuple(topics or ())
        seen: set[TopicId] = set()
        for topic in topics_t:
            if topic.topic_id in seen:
                raise ValueError("duplicate topic_id within module")
            seen.add(topic.topic_id)
            if topic.module_id is not None and topic.module_id != mid:
                raise ValueError("topic module_id must match module")
        return cls(
            module_id=mid,
            name=label,
            topics=topics_t,
            sequence_index=sequence_index,
            subject_id=sid,
        )

    def ordered_topics(self) -> tuple[Topic, ...]:
        """Topics sorted by sequence_index ascending, then topic_id."""
        return tuple(
            sorted(
                self.topics,
                key=lambda t: (t.sequence_index, t.topic_id.value),
            )
        )

    def with_topic(self, topic: Topic) -> Module:
        """Return a new module with an appended topic."""
        if topic.module_id is not None and topic.module_id != self.module_id:
            raise ValueError("topic module_id must match module")
        if any(t.topic_id == topic.topic_id for t in self.topics):
            raise ValueError("duplicate topic_id within module")
        return Module(
            module_id=self.module_id,
            name=self.name,
            topics=(*self.topics, topic),
            sequence_index=self.sequence_index,
            subject_id=self.subject_id,
        )

    def topic_ids(self) -> tuple[TopicId, ...]:
        """Ordered topic identities."""
        return tuple(t.topic_id for t in self.ordered_topics())
