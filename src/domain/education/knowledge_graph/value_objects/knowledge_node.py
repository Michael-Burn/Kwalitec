"""Knowledge node — a teachable unit of knowledge within the graph.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Knowledge Node
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import KnowledgeNodeKind
from domain.education.knowledge_graph.ids import KnowledgeNodeId


@dataclass(frozen=True, slots=True)
class KnowledgeNode(EducationalValueObject):
    """Immutable node representing one unit of teachable knowledge.

    A node is independent of courses, subjects, UI navigation, study plans,
    and missions. It carries only the educational identity, label, kind,
    and an optional description supplied by an authorised writer.
    """

    node_id: KnowledgeNodeId
    label: str
    kind: KnowledgeNodeKind = KnowledgeNodeKind.CONCEPT
    description: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.node_id, KnowledgeNodeId):
            raise EducationalInvariantViolation(
                "node_id must be a KnowledgeNodeId",
                invariant="KnowledgeNode.node_id.type",
            )
        object.__setattr__(self, "label", require_non_empty_text(self.label, "label"))
        if not isinstance(self.kind, KnowledgeNodeKind):
            raise EducationalInvariantViolation(
                "kind must be a KnowledgeNodeKind",
                invariant="KnowledgeNode.kind.type",
            )
        if self.description is not None:
            object.__setattr__(
                self,
                "description",
                require_non_empty_text(self.description, "description"),
            )

    def with_label(self, label: str) -> KnowledgeNode:
        return KnowledgeNode(
            node_id=self.node_id,
            label=label,
            kind=self.kind,
            description=self.description,
        )

    def with_kind(self, kind: KnowledgeNodeKind) -> KnowledgeNode:
        return KnowledgeNode(
            node_id=self.node_id,
            label=self.label,
            kind=kind,
            description=self.description,
        )

    def with_description(self, description: str | None) -> KnowledgeNode:
        return KnowledgeNode(
            node_id=self.node_id,
            label=self.label,
            kind=self.kind,
            description=description,
        )

    def __str__(self) -> str:
        return f"{self.node_id.value}:{self.label}"
