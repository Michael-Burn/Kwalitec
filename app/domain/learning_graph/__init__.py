"""Learning Graph (SDT-003) domain package.

Canonical representation of how a learner's knowledge is interconnected.
Complements Curriculum Intelligence (WHAT) and Student Digital Twin (WHO)
with relational prerequisite / dependency structure (HOW knowledge connects).

No LLM. Curriculum evidence enters only via CurriculumRetrievalService at the
application layer.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "DEPENDENCY_RELATIONSHIPS",
    "DependencyChain",
    "DependencyHop",
    "GraphEdge",
    "GraphNode",
    "GraphProjection",
    "GraphSnapshot",
    "GraphUpdate",
    "GraphUpdateKind",
    "ImpactAnalysis",
    "LearningGraph",
    "MasteryLink",
    "PROJECTION_VERSION",
    "PrerequisiteRelationship",
    "PrerequisiteStatus",
    "ProjectionBatch",
    "ProjectionContext",
    "ProjectionReference",
    "ProjectionRelationshipType",
    "ProjectionResult",
    "ProjectionVersion",
    "RecoveryPath",
    "RelationshipProjection",
    "RelationshipType",
    "TraversalResult",
    "connected_concepts",
    "generate_recovery_path",
    "impact_analysis",
    "is_prerequisite_edge",
    "learning_path",
    "traverse_dependencies",
    "traverse_prerequisites",
]

_EXPORT_MODULES = {
    "RelationshipType": "app.domain.learning_graph.relationship",
    "DEPENDENCY_RELATIONSHIPS": "app.domain.learning_graph.relationship",
    "GraphNode": "app.domain.learning_graph.graph_node",
    "PrerequisiteStatus": "app.domain.learning_graph.graph_node",
    "GraphEdge": "app.domain.learning_graph.graph_edge",
    "PrerequisiteRelationship": "app.domain.learning_graph.prerequisite",
    "is_prerequisite_edge": "app.domain.learning_graph.prerequisite",
    "DependencyChain": "app.domain.learning_graph.dependency",
    "DependencyHop": "app.domain.learning_graph.dependency",
    "MasteryLink": "app.domain.learning_graph.mastery_link",
    "GraphSnapshot": "app.domain.learning_graph.graph_snapshot",
    "GraphUpdate": "app.domain.learning_graph.graph_update",
    "GraphUpdateKind": "app.domain.learning_graph.graph_update",
    "TraversalResult": "app.domain.learning_graph.graph_traversal",
    "RecoveryPath": "app.domain.learning_graph.graph_traversal",
    "ImpactAnalysis": "app.domain.learning_graph.graph_traversal",
    "traverse_prerequisites": "app.domain.learning_graph.graph_traversal",
    "traverse_dependencies": "app.domain.learning_graph.graph_traversal",
    "connected_concepts": "app.domain.learning_graph.graph_traversal",
    "generate_recovery_path": "app.domain.learning_graph.graph_traversal",
    "impact_analysis": "app.domain.learning_graph.graph_traversal",
    "learning_path": "app.domain.learning_graph.graph_traversal",
    "LearningGraph": "app.domain.learning_graph.learning_graph",
    "PROJECTION_VERSION": "app.domain.learning_graph.projections.version",
    "ProjectionVersion": "app.domain.learning_graph.projections.version",
    "ProjectionRelationshipType": (
        "app.domain.learning_graph.projections.relationship_type"
    ),
    "ProjectionReference": "app.domain.learning_graph.projections.reference",
    "ProjectionContext": "app.domain.learning_graph.projections.context",
    "RelationshipProjection": "app.domain.learning_graph.projections.relationship",
    "GraphProjection": "app.domain.learning_graph.projections.projection",
    "ProjectionBatch": "app.domain.learning_graph.projections.batch",
    "ProjectionResult": "app.domain.learning_graph.projections.result",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
