"""Concept cluster — a group of nodes joined by advisory relationships.

Architecture Source
    CONCEPT_NETWORK_MODEL.md
Concept
    Clusters
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeNodeId


@dataclass(frozen=True, slots=True)
class ConceptCluster(EducationalValueObject):
    """Immutable grouping of nodes connected through advisory relationships.

    Clusters describe network structure (Concept Network Model §5.3) — they
    are not curriculum modules, courses, or subjects.
    """

    cluster_id: str
    node_ids: tuple[KnowledgeNodeId, ...]

    def _validate(self) -> None:
        object.__setattr__(
            self, "cluster_id", require_non_empty_text(self.cluster_id, "cluster_id")
        )
        if isinstance(self.node_ids, list):
            object.__setattr__(self, "node_ids", tuple(self.node_ids))
        if not isinstance(self.node_ids, tuple):
            raise EducationalInvariantViolation(
                "node_ids must be a tuple of KnowledgeNodeId",
                invariant="ConceptCluster.node_ids.type",
            )
        if len(self.node_ids) < 2:
            raise EducationalInvariantViolation(
                "a concept cluster must contain at least two nodes",
                invariant="ConceptCluster.node_ids.min_size",
            )
        for node_id in self.node_ids:
            if not isinstance(node_id, KnowledgeNodeId):
                raise EducationalInvariantViolation(
                    "every cluster member must be a KnowledgeNodeId",
                    invariant="ConceptCluster.node_ids.element_type",
                )
        if len(self.node_ids) != len({node_id.value for node_id in self.node_ids}):
            raise EducationalInvariantViolation(
                "a concept cluster must not repeat nodes",
                invariant="ConceptCluster.node_ids.unique",
            )

    @property
    def size(self) -> int:
        return len(self.node_ids)

    def contains(self, node_id: KnowledgeNodeId) -> bool:
        return node_id in self.node_ids
