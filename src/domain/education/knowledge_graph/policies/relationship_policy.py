"""Policy governing knowledge relationship type classification and integrity.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md / CONCEPT_NETWORK_MODEL.md
Concept
    Relationship Policy
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import RelationshipType
from domain.education.knowledge_graph.ids import KnowledgeNodeId
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_relationship import (
    KnowledgeRelationship,
)

_STRUCTURAL_TYPES = frozenset(
    {
        RelationshipType.PREREQUISITE,
        RelationshipType.REQUIRES,
        RelationshipType.FOUNDATIONAL,
        RelationshipType.DERIVED_FROM,
    }
)

_ADVISORY_TYPES = frozenset(
    {
        RelationshipType.SUPPORTS,
        RelationshipType.REINFORCES,
        RelationshipType.OPTIONAL,
        RelationshipType.RELATED,
    }
)


class RelationshipPolicy:
    """Classifies relationship types and enforces per-edge admission rules.

    Structural types (``PREREQUISITE``, ``REQUIRES``, ``FOUNDATIONAL``,
    ``DERIVED_FROM``) encode directed educational dependency and are
    subject to the acyclic invariant. Advisory types (``SUPPORTS``,
    ``REINFORCES``, ``OPTIONAL``, ``RELATED``) are educational annotations
    that carry no acyclic requirement.
    """

    @staticmethod
    def structural_types() -> frozenset[RelationshipType]:
        return _STRUCTURAL_TYPES

    @staticmethod
    def advisory_types() -> frozenset[RelationshipType]:
        return _ADVISORY_TYPES

    @staticmethod
    def is_structural(relationship_type: RelationshipType) -> bool:
        return relationship_type in _STRUCTURAL_TYPES

    @staticmethod
    def is_advisory(relationship_type: RelationshipType) -> bool:
        return relationship_type in _ADVISORY_TYPES

    @staticmethod
    def assert_valid_type(relationship_type: RelationshipType) -> None:
        """Require ``relationship_type`` to be a recognised RelationshipType."""
        if not isinstance(relationship_type, RelationshipType):
            raise EducationalInvariantViolation(
                "relationship type must be a valid RelationshipType",
                invariant="RelationshipPolicy.relationship_type.valid",
            )

    @staticmethod
    def assert_no_self_relationship(
        owner_node_id: KnowledgeNodeId,
        relationship: KnowledgeRelationship,
    ) -> None:
        """Forbid a node relating to itself (educationally meaningless)."""
        relationship.assert_not_self(owner_node_id)

    @staticmethod
    def assert_not_duplicate(
        existing: Sequence[KnowledgeEdge],
        source_node_id: KnowledgeNodeId,
        candidate: KnowledgeRelationship,
    ) -> None:
        """Forbid duplicate (source, target, type) relationship edges."""
        for edge in existing:
            if edge.source_node_id == source_node_id and edge.relationship.same_edge(
                candidate
            ):
                raise EducationalInvariantViolation(
                    "duplicate knowledge relationship is not allowed",
                    invariant="RelationshipPolicy.relationship.duplicate",
                )

    @staticmethod
    def assert_can_connect(
        existing: Sequence[KnowledgeEdge],
        source_node_id: KnowledgeNodeId,
        candidate: KnowledgeRelationship,
    ) -> None:
        """Run full admission checks for a new relationship edge."""
        RelationshipPolicy.assert_valid_type(candidate.relationship_type)
        RelationshipPolicy.assert_no_self_relationship(source_node_id, candidate)
        RelationshipPolicy.assert_not_duplicate(existing, source_node_id, candidate)
