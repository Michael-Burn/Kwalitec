"""Curriculum graph package."""

from __future__ import annotations

from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.graph.graph_builder import GraphBuilder
from app.domain.curriculum.graph.graph_edge import GraphEdge
from app.domain.curriculum.graph.graph_node import GraphNode
from app.domain.curriculum.graph.graph_validator import (
    GraphValidationResult,
    GraphValidator,
    validate_dependency_endpoints,
    validate_requires_dag,
)

__all__ = [
    "CurriculumGraph",
    "GraphBuilder",
    "GraphEdge",
    "GraphNode",
    "GraphValidationResult",
    "GraphValidator",
    "validate_dependency_endpoints",
    "validate_requires_dag",
]
