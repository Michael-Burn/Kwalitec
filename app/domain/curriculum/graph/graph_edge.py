"""GraphEdge — directed dependency edge within the Curriculum Graph."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class GraphEdge:
    """Directed edge from source to target with a dependency kind.

    For REQUIRES: source requires target (target is prerequisite of source).
    Edge identity is optional for ephemeral graph edges.

    Attributes:
        source_id: Topic that holds the relationship.
        target_id: Related / required topic.
        dependency_type: Relationship kind.
        edge_id: Optional stable identity.
        rationale: Optional short operational note.
    """

    source_id: TopicId
    target_id: TopicId
    dependency_type: DependencyType
    edge_id: str | None = None
    rationale: str | None = None

    @classmethod
    def create(
        cls,
        source_id: str | TopicId,
        target_id: str | TopicId,
        dependency_type: DependencyType | str,
        *,
        edge_id: str | None = None,
        rationale: str | None = None,
    ) -> GraphEdge:
        """Construct a GraphEdge after validating invariants."""
        source = TopicId.of(source_id)
        target = TopicId.of(target_id)
        if source == target:
            raise ValueError("graph edge cannot be a self-loop")
        dtype = (
            dependency_type
            if isinstance(dependency_type, DependencyType)
            else DependencyType(dependency_type)
        )
        eid = None if edge_id is None else require_non_empty(edge_id, "edge_id")
        return cls(
            source_id=source,
            target_id=target,
            dependency_type=dtype,
            edge_id=eid,
            rationale=optional_non_empty(rationale),
        )

    @property
    def is_hard(self) -> bool:
        """True when this edge is a hard prerequisite (REQUIRES)."""
        return self.dependency_type is DependencyType.REQUIRES
