"""Specification: structural prerequisite relationships form no cycle.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    AcyclicPrerequisiteSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.policies.cycle_detection_policy import (
    CycleDetectionPolicy,
)
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)

if TYPE_CHECKING:
    from domain.education.knowledge_graph.aggregates.knowledge_graph import (
        KnowledgeGraph,
    )


class AcyclicPrerequisiteSpecification:
    """True when structural (strict dependency) relationships are acyclic.

    Only ``PREREQUISITE``, ``REQUIRES``, ``FOUNDATIONAL``, and
    ``DERIVED_FROM`` relationships participate — advisory relationships
    (``SUPPORTS``, ``REINFORCES``, ``OPTIONAL``, ``RELATED``) carry no
    acyclic requirement and are excluded from this check.
    """

    def is_satisfied_by(self, graph: KnowledgeGraph) -> bool:
        structural_pairs = [
            (edge.source_node_id, edge.target_node_id)
            for edge in graph.edges
            if RelationshipPolicy.is_structural(edge.relationship_type)
        ]
        return CycleDetectionPolicy.find_cycle(structural_pairs) is None

    def assert_satisfied_by(self, graph: KnowledgeGraph) -> None:
        if not self.is_satisfied_by(graph):
            raise EducationalInvariantViolation(
                "structural prerequisite relationships contain a cycle",
                invariant="AcyclicPrerequisiteSpecification.cycle_detected",
            )
