"""LearningGraphTraversalService — deterministic graph traversal (SDT-003).

Responsibilities:
  - prerequisite traversal
  - dependency discovery
  - learning path generation
  - impact analysis
  - connected concept discovery
  - recovery path generation

All traversals are deterministic (BFS with sorted adjacency).
"""

from __future__ import annotations

from typing import Any

from app.domain.learning_graph.dependency import DependencyChain
from app.domain.learning_graph.graph_traversal import (
    ImpactAnalysis,
    RecoveryPath,
    TraversalResult,
)
from app.domain.learning_graph.learning_graph import LearningGraph


class LearningGraphTraversalService:
    """Application facade over Learning Graph deterministic traversal."""

    def prerequisites(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 8,
    ) -> TraversalResult:
        return graph.traverse_prerequisites(concept_id, max_depth=max_depth)

    def dependencies(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 8,
    ) -> TraversalResult:
        return graph.traverse_dependencies(concept_id, max_depth=max_depth)

    def learning_path(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 8,
    ) -> DependencyChain:
        return graph.learning_path_for(concept_id, max_depth=max_depth)

    def recovery_path(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 8,
    ) -> RecoveryPath:
        return graph.recovery_path(concept_id, max_depth=max_depth)

    def impact(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 8,
    ) -> ImpactAnalysis:
        return graph.impact(concept_id, max_depth=max_depth)

    def connected(
        self,
        graph: LearningGraph,
        concept_id: str,
        *,
        max_depth: int = 2,
    ) -> TraversalResult:
        return graph.connected(concept_id, max_depth=max_depth)

    @staticmethod
    def traversal_as_dict(result: TraversalResult) -> dict[str, Any]:
        return {
            "kind": result.kind,
            "seed_concept_id": result.seed_concept_id,
            "visited_concept_ids": list(result.visited_concept_ids),
            "depth_by_concept": [
                {"concept_id": c, "depth": d} for c, d in result.depth_by_concept
            ],
            "chains": [
                {
                    "seed_concept_id": chain.seed_concept_id,
                    "direction": chain.direction,
                    "length": chain.length,
                    "concept_ids": list(chain.concept_ids),
                    "hops": [
                        {
                            "concept_id": h.concept_id,
                            "concept_title": h.concept_title,
                            "mastery_score": h.mastery_score,
                            "depth": h.depth,
                            "via_edge_id": h.via_edge_id,
                            "relationship_type": (
                                h.relationship_type.value
                                if h.relationship_type
                                else None
                            ),
                        }
                        for h in chain.hops
                    ],
                }
                for chain in result.chains
            ],
        }

    @staticmethod
    def recovery_as_dict(path: RecoveryPath) -> dict[str, Any]:
        return {
            "seed_concept_id": path.seed_concept_id,
            "concept_ids": list(path.concept_ids),
            "length": path.length,
            "reason": path.reason,
            "hops": [
                {
                    "concept_id": h.concept_id,
                    "concept_title": h.concept_title,
                    "mastery_score": h.mastery_score,
                    "depth": h.depth,
                }
                for h in path.hops
            ],
        }

    @staticmethod
    def impact_as_dict(analysis: ImpactAnalysis) -> dict[str, Any]:
        return {
            "seed_concept_id": analysis.seed_concept_id,
            "impacted_concept_ids": list(analysis.impacted_concept_ids),
            "reason": analysis.reason,
            "hops": [
                {
                    "concept_id": h.concept_id,
                    "concept_title": h.concept_title,
                    "mastery_score": h.mastery_score,
                    "depth": h.depth,
                }
                for h in analysis.hops
            ],
        }

    @staticmethod
    def learning_path_as_dict(chain: DependencyChain) -> dict[str, Any]:
        return {
            "seed_concept_id": chain.seed_concept_id,
            "direction": chain.direction,
            "length": chain.length,
            "concept_ids": list(chain.concept_ids),
            "hops": [
                {
                    "concept_id": h.concept_id,
                    "concept_title": h.concept_title,
                    "mastery_score": h.mastery_score,
                    "depth": h.depth,
                }
                for h in chain.hops
            ],
        }
