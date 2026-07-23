"""Knowledge Dependency Graph bounded context — pure educational domain model.

EDU-003.3 implementation of the Knowledge Dependency Graph.

Pure Domain-Driven Design only: an aggregate, value objects, policies, and
specifications. No persistence, Flask, ORM, HTTP APIs, repositories,
serialization, graph databases, or AI.

KnowledgeGraph models how knowledge nodes depend upon, support, and relate
to one another. It represents educational truth — the canonical source of
prerequisite relationships used by future mastery estimation,
recommendation, curriculum traversal, and educational reasoning. It is
independent of courses, subjects, UI navigation, study plans, and missions.
It does not estimate mastery, recommend, update student state, update the
digital twin, or persist itself.
"""

from __future__ import annotations

from domain.education.knowledge_graph.aggregates.knowledge_graph import (
    KnowledgeGraph,
)
from domain.education.knowledge_graph.enums import (
    DependencyStrengthBand,
    KnowledgeNodeKind,
    RelationshipType,
)
from domain.education.knowledge_graph.ids import (
    KnowledgeGraphId,
    KnowledgeNodeId,
    KnowledgeRelationshipId,
)
from domain.education.knowledge_graph.policies.cycle_detection_policy import (
    CycleDetectionPolicy,
)
from domain.education.knowledge_graph.policies.graph_validation_policy import (
    GraphValidationPolicy,
)
from domain.education.knowledge_graph.policies.learning_path_policy import (
    LearningPathPolicy,
)
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)
from domain.education.knowledge_graph.specifications.acyclic_prerequisite_specification import (  # noqa: E501
    AcyclicPrerequisiteSpecification,
)
from domain.education.knowledge_graph.specifications.knowledge_graph_consistency_specification import (  # noqa: E501
    KnowledgeGraphConsistencySpecification,
)
from domain.education.knowledge_graph.specifications.relationship_validity_specification import (  # noqa: E501
    RelationshipValiditySpecification,
)
from domain.education.knowledge_graph.value_objects.concept_cluster import (
    ConceptCluster,
)
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_node import (
    KnowledgeNode,
)
from domain.education.knowledge_graph.value_objects.knowledge_path import (
    KnowledgePath,
)
from domain.education.knowledge_graph.value_objects.knowledge_relationship import (
    KnowledgeRelationship,
)
from domain.education.knowledge_graph.value_objects.knowledge_snapshot import (
    KnowledgeSnapshot,
)
from domain.education.knowledge_graph.value_objects.learning_depth import (
    LearningDepth,
)
from domain.education.knowledge_graph.value_objects.relationship_metadata import (
    RelationshipMetadata,
)

__all__ = [
    # Aggregate
    "KnowledgeGraph",
    # Value objects
    "KnowledgeNode",
    "KnowledgeRelationship",
    "KnowledgeEdge",
    "DependencyStrength",
    "RelationshipMetadata",
    "LearningDepth",
    "KnowledgePath",
    "ConceptCluster",
    "KnowledgeSnapshot",
    # Identity
    "KnowledgeGraphId",
    "KnowledgeNodeId",
    "KnowledgeRelationshipId",
    # Enums
    "RelationshipType",
    "KnowledgeNodeKind",
    "DependencyStrengthBand",
    # Policies
    "GraphValidationPolicy",
    "RelationshipPolicy",
    "CycleDetectionPolicy",
    "LearningPathPolicy",
    # Specifications
    "KnowledgeGraphConsistencySpecification",
    "AcyclicPrerequisiteSpecification",
    "RelationshipValiditySpecification",
]
