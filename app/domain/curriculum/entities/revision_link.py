"""RevisionLink — concepts that should be revised together."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class RevisionLink:
    """Undirected educational association for joint revision.

    Stored with a canonical ordered pair (lexicographically smaller id
    first) so A⇄B and B⇄A collapse to one link.

    Attributes:
        revision_link_id: Stable identity.
        topic_a_id: First topic in canonical order.
        topic_b_id: Second topic in canonical order.
        rationale: Optional short operational note.
    """

    revision_link_id: str
    topic_a_id: TopicId
    topic_b_id: TopicId
    rationale: str | None = None

    @classmethod
    def create(
        cls,
        revision_link_id: str,
        topic_a_id: str | TopicId,
        topic_b_id: str | TopicId,
        *,
        rationale: str | None = None,
    ) -> RevisionLink:
        """Construct a RevisionLink after validating invariants.

        Raises:
            ValueError: On empty ids or self-links.
        """
        rid = require_non_empty(revision_link_id, "revision_link_id")
        a = TopicId.of(topic_a_id)
        b = TopicId.of(topic_b_id)
        if a == b:
            raise ValueError("revision link cannot be a self-loop")
        # Canonical order: lexicographically smaller first.
        if a.value > b.value:
            a, b = b, a
        return cls(
            revision_link_id=rid,
            topic_a_id=a,
            topic_b_id=b,
            rationale=optional_non_empty(rationale),
        )

    def involves(self, topic_id: str | TopicId) -> bool:
        """True when the topic participates in this revision link."""
        tid = TopicId.of(topic_id)
        return tid in {self.topic_a_id, self.topic_b_id}

    def other(self, topic_id: str | TopicId) -> TopicId:
        """Return the paired topic.

        Raises:
            ValueError: When topic_id is not part of this link.
        """
        tid = TopicId.of(topic_id)
        if tid == self.topic_a_id:
            return self.topic_b_id
        if tid == self.topic_b_id:
            return self.topic_a_id
        raise ValueError("topic_id is not part of this revision link")

    def pair(self) -> tuple[TopicId, TopicId]:
        """Canonical (a, b) pair."""
        return (self.topic_a_id, self.topic_b_id)
