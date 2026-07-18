"""Dependency — directed relationship between two topics."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Dependency:
    """Directed educational relationship from source to target.

    Semantics: ``source`` depends on ``target`` when type is REQUIRES
    (i.e. target is a prerequisite of source). For REVISION / RELATED,
    the edge is associative; direction still records authoring order.

    Attributes:
        dependency_id: Stable identity for this relationship.
        source_topic_id: Topic that holds the relationship.
        target_topic_id: Related / required topic.
        dependency_type: Relationship kind.
        rationale: Optional short operational note (not syllabus prose).
    """

    dependency_id: str
    source_topic_id: TopicId
    target_topic_id: TopicId
    dependency_type: DependencyType
    rationale: str | None = None

    @classmethod
    def create(
        cls,
        dependency_id: str,
        source_topic_id: str | TopicId,
        target_topic_id: str | TopicId,
        dependency_type: DependencyType | str,
        *,
        rationale: str | None = None,
    ) -> Dependency:
        """Construct a Dependency after validating invariants.

        Raises:
            ValueError: On empty ids, self-loops, or invalid type.
        """
        did = require_non_empty(dependency_id, "dependency_id")
        source = TopicId.of(source_topic_id)
        target = TopicId.of(target_topic_id)
        if source == target:
            raise ValueError("dependency cannot be a self-loop")
        dtype = (
            dependency_type
            if isinstance(dependency_type, DependencyType)
            else DependencyType(dependency_type)
        )
        return cls(
            dependency_id=did,
            source_topic_id=source,
            target_topic_id=target,
            dependency_type=dtype,
            rationale=optional_non_empty(rationale),
        )
