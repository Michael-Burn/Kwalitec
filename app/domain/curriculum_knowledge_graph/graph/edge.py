"""Directed typed edge in the Curriculum Knowledge Graph."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import (
    optional_non_empty,
    require_non_empty,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)


@dataclass(frozen=True)
class CkgEdge:
    """One directed educational relationship between two stable ids."""

    edge_id: str
    from_stable_id: StableCurriculumId
    to_stable_id: StableCurriculumId
    relationship_type: CkgRelationshipType
    sequence_index: int = 0
    rationale: str | None = None

    @classmethod
    def create(
        cls,
        from_stable_id: str | StableCurriculumId,
        to_stable_id: str | StableCurriculumId,
        relationship_type: CkgRelationshipType | str,
        *,
        edge_id: str | None = None,
        sequence_index: int = 0,
        rationale: str | None = None,
    ) -> CkgEdge:
        """Construct an edge after validating endpoints and type."""
        source = StableCurriculumId.of(from_stable_id)
        target = StableCurriculumId.of(to_stable_id)
        if source.value == target.value:
            raise ValueError("CKG edge cannot be a self-loop")
        rel = (
            relationship_type
            if isinstance(relationship_type, CkgRelationshipType)
            else CkgRelationshipType(relationship_type)
        )
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        eid = edge_id or f"{source.value}|{rel.value}|{target.value}"
        return cls(
            edge_id=require_non_empty(eid, "edge_id"),
            from_stable_id=source,
            to_stable_id=target,
            relationship_type=rel,
            sequence_index=sequence_index,
            rationale=optional_non_empty(rationale),
        )
