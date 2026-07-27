"""Graph edge — directed relationship between two concept nodes."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_graph.relationship import RelationshipType


@dataclass(frozen=True)
class GraphEdge:
    """Directed edge connecting two curriculum concepts on a Learning Graph.

    ``supporting_evidence`` cites curriculum evidence ids (CIP-003 retrieval),
    never raw vector hits.
    """

    edge_id: str
    graph_id: str
    from_concept_id: str
    to_concept_id: str
    relationship_type: RelationshipType
    strength: float = 1.0
    confidence: float = 0.0
    provenance: str = ""
    supporting_evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.edge_id or "").strip():
            raise ValueError("edge_id is required")
        if not (self.from_concept_id or "").strip():
            raise ValueError("from_concept_id is required")
        if not (self.to_concept_id or "").strip():
            raise ValueError("to_concept_id is required")
        if self.from_concept_id == self.to_concept_id:
            raise ValueError("edge cannot be self-referential")
        rel = self.relationship_type
        if not isinstance(rel, RelationshipType):
            object.__setattr__(
                self, "relationship_type", RelationshipType(str(rel))
            )
        object.__setattr__(self, "strength", _clamp(self.strength))
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence or ())
        )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
