"""Prerequisite — required knowledge link for a topic."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.entities._text import optional_non_empty, require_non_empty
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Prerequisite:
    """Hard required-knowledge link: ``topic`` requires ``required_topic``.

    Equivalent educational meaning to a Dependency of type REQUIRES, kept
    as a first-class entity for curriculum authoring clarity.

    Attributes:
        prerequisite_id: Stable identity.
        topic_id: Topic that requires prior knowledge.
        required_topic_id: Topic that must be completed / available first.
        rationale: Optional short operational note.
    """

    prerequisite_id: str
    topic_id: TopicId
    required_topic_id: TopicId
    rationale: str | None = None

    @classmethod
    def create(
        cls,
        prerequisite_id: str,
        topic_id: str | TopicId,
        required_topic_id: str | TopicId,
        *,
        rationale: str | None = None,
    ) -> Prerequisite:
        """Construct a Prerequisite after validating invariants.

        Raises:
            ValueError: On empty ids or self-requirement.
        """
        pid = require_non_empty(prerequisite_id, "prerequisite_id")
        tid = TopicId.of(topic_id)
        required = TopicId.of(required_topic_id)
        if tid == required:
            raise ValueError("topic cannot require itself")
        return cls(
            prerequisite_id=pid,
            topic_id=tid,
            required_topic_id=required,
            rationale=optional_non_empty(rationale),
        )

    def as_dependency_id(self) -> str:
        """Stable dependency identity derived from this prerequisite."""
        return f"prereq:{self.prerequisite_id}"
