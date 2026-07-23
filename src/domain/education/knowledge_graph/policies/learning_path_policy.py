"""Policy governing learning path construction and reachability.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Learning Path Policy
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeNodeId
from domain.education.knowledge_graph.value_objects.knowledge_path import (
    KnowledgePath,
)


class LearningPathPolicy:
    """Enforces admission rules for learning paths produced by the graph.

    A learning path is only meaningful when it is non-empty and reflects an
    actual chain of structural dependency edges. This policy does not
    compute paths itself — it validates candidates handed to it.
    """

    @staticmethod
    def assert_nonempty_path(path: KnowledgePath) -> KnowledgePath:
        if not isinstance(path, KnowledgePath):
            raise EducationalInvariantViolation(
                "path must be a KnowledgePath",
                invariant="LearningPathPolicy.path.type",
            )
        return path

    @staticmethod
    def assert_reachable(
        path: KnowledgePath | None,
        *,
        start: KnowledgeNodeId,
        target: KnowledgeNodeId,
    ) -> KnowledgePath:
        """Require a discovered path, raising an explanatory error otherwise."""
        if path is None:
            raise EducationalInvariantViolation(
                f"no learning path exists from {start.value} to {target.value}",
                invariant="LearningPathPolicy.unreachable",
            )
        return LearningPathPolicy.assert_nonempty_path(path)
