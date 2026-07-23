"""Knowledge path — an ordered dependency chain between two nodes.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Dependency Path / Learning Path
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeNodeId


@dataclass(frozen=True, slots=True)
class KnowledgePath(EducationalValueObject):
    """Immutable, ordered sequence of distinct nodes forming a path.

    A path with a single node denotes a trivial path (start equals end).
    A path never repeats a node — repetition would describe a cycle, not a
    learning path.
    """

    nodes: tuple[KnowledgeNodeId, ...]

    def _validate(self) -> None:
        if isinstance(self.nodes, list):
            object.__setattr__(self, "nodes", tuple(self.nodes))
        if not isinstance(self.nodes, tuple):
            raise EducationalInvariantViolation(
                "nodes must be a tuple of KnowledgeNodeId",
                invariant="KnowledgePath.nodes.type",
            )
        if len(self.nodes) == 0:
            raise EducationalInvariantViolation(
                "a knowledge path must contain at least one node",
                invariant="KnowledgePath.nodes.non_empty",
            )
        for node_id in self.nodes:
            if not isinstance(node_id, KnowledgeNodeId):
                raise EducationalInvariantViolation(
                    "every path element must be a KnowledgeNodeId",
                    invariant="KnowledgePath.nodes.element_type",
                )
        if len(self.nodes) != len({node_id.value for node_id in self.nodes}):
            raise EducationalInvariantViolation(
                "a knowledge path must not repeat nodes",
                invariant="KnowledgePath.nodes.no_repeats",
            )

    @property
    def start(self) -> KnowledgeNodeId:
        return self.nodes[0]

    @property
    def end(self) -> KnowledgeNodeId:
        return self.nodes[-1]

    @property
    def step_count(self) -> int:
        """Number of hops (edges) traversed by this path."""
        return len(self.nodes) - 1

    def contains(self, node_id: KnowledgeNodeId) -> bool:
        return node_id in self.nodes

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self) -> Iterator[KnowledgeNodeId]:
        return iter(self.nodes)
