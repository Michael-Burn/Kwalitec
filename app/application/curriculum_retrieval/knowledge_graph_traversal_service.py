"""Knowledge graph traversal for retrieval expansion (CIP-003)."""

from __future__ import annotations

from collections import deque

from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeRelationType
from app.models.curriculum_intelligence import CipCurriculumEntity, CipKnowledgeRelation
from app.models.curriculum_studio_foundation import StudioFoundationDocument


class KnowledgeGraphTraversalService:
    """BFS neighbourhood and typed neighbour helpers over CIP knowledge graph."""

    PREREQ_TYPES = frozenset(
        {
            KnowledgeRelationType.DEPENDS_ON.value,
            KnowledgeRelationType.REQUIRES.value,
        }
    )
    RELATED_TYPES = frozenset(
        {
            KnowledgeRelationType.SUPPORTS.value,
            KnowledgeRelationType.EXTENDS.value,
            KnowledgeRelationType.APPEARS_IN.value,
            KnowledgeRelationType.PARENT_OF.value,
            KnowledgeRelationType.CHILD_OF.value,
        }
    )
    FORMULA_TYPES = frozenset({KnowledgeRelationType.FORMULA_FOR.value})
    EXAMPLE_TYPES = frozenset({KnowledgeRelationType.EXAMPLE_OF.value})
    LO_TYPES = frozenset({KnowledgeRelationType.LEARNING_OBJECTIVE_OF.value})
    PRACTICE_TYPES = frozenset({KnowledgeRelationType.TESTED_IN.value})

    def neighbours(
        self,
        entity_id: str,
        *,
        workspace_id: str | None = None,
        max_hops: int = 1,
        relation_types: frozenset[str] | None = None,
    ) -> list[dict]:
        """Return neighbour entities within ``max_hops`` (BFS).

        Each item: entity_id, kind, title, distance, relation_type, direction.
        """
        allowed_docs = self._document_ids(workspace_id) if workspace_id else None
        visited: dict[str, int] = {entity_id: 0}
        results: list[dict] = []
        queue: deque[str] = deque([entity_id])

        while queue:
            current = queue.popleft()
            distance = visited[current]
            if distance >= max_hops:
                continue
            for edge in self._edges_for(current, allowed_docs):
                if relation_types and edge["relation_type"] not in relation_types:
                    continue
                neighbour = edge["neighbour_id"]
                if neighbour in visited:
                    continue
                visited[neighbour] = distance + 1
                queue.append(neighbour)
                entity = CipCurriculumEntity.query.filter_by(
                    entity_id=neighbour
                ).first()
                if entity is None:
                    continue
                if allowed_docs is not None and entity.document_id not in allowed_docs:
                    continue
                results.append(
                    {
                        "entity_id": neighbour,
                        "kind": entity.kind,
                        "title": entity.title,
                        "distance": distance + 1,
                        "relation_type": edge["relation_type"],
                        "direction": edge["direction"],
                        "confidence": float(edge["confidence"]),
                    }
                )

        results.sort(
            key=lambda item: (
                item["distance"],
                -float(item["confidence"]),
                item["entity_id"],
            )
        )
        return results

    def expand_entity_ids(
        self,
        seed_ids: list[str] | tuple[str, ...],
        *,
        workspace_id: str | None = None,
        max_hops: int = 1,
    ) -> dict[str, int]:
        """Return entity_id → graph distance from nearest seed (0 for seeds)."""
        distances: dict[str, int] = {}
        for seed in seed_ids:
            distances[seed] = 0
            for neighbour in self.neighbours(
                seed, workspace_id=workspace_id, max_hops=max_hops
            ):
                eid = neighbour["entity_id"]
                dist = int(neighbour["distance"])
                if eid not in distances or dist < distances[eid]:
                    distances[eid] = dist
        return distances

    def related_concepts(
        self,
        entity_id: str,
        *,
        workspace_id: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Related concept neighbours (supports / extends / hierarchy)."""
        items = self.neighbours(
            entity_id,
            workspace_id=workspace_id,
            max_hops=1,
            relation_types=self.RELATED_TYPES,
        )
        return [i for i in items if i["kind"] == "concept"][:limit]

    def prerequisites(
        self,
        entity_id: str,
        *,
        workspace_id: str | None = None,
    ) -> list[dict]:
        """Prerequisite neighbours via depends_on / requires."""
        return self.neighbours(
            entity_id,
            workspace_id=workspace_id,
            max_hops=1,
            relation_types=self.PREREQ_TYPES,
        )

    def typed_neighbour_ids(
        self,
        entity_id: str,
        *,
        relation_types: frozenset[str],
        workspace_id: str | None = None,
        kind_filter: str | None = None,
    ) -> tuple[str, ...]:
        """Return neighbour entity ids for given relation types."""
        items = self.neighbours(
            entity_id,
            workspace_id=workspace_id,
            max_hops=1,
            relation_types=relation_types,
        )
        ids: list[str] = []
        for item in items:
            if kind_filter and item["kind"] != kind_filter:
                continue
            ids.append(item["entity_id"])
        return tuple(ids)

    def mean_edge_strength(
        self,
        entity_id: str,
        *,
        workspace_id: str | None = None,
    ) -> float:
        """Mean relation confidence for 1-hop edges (0 if none)."""
        items = self.neighbours(entity_id, workspace_id=workspace_id, max_hops=1)
        if not items:
            return 0.0
        return sum(float(i["confidence"]) for i in items) / len(items)

    def _document_ids(self, workspace_id: str) -> set[int]:
        rows = StudioFoundationDocument.query.filter_by(
            workspace_id=workspace_id
        ).all()
        return {int(r.id) for r in rows}

    def _edges_for(
        self, entity_id: str, allowed_docs: set[int] | None
    ) -> list[dict]:
        q_from = CipKnowledgeRelation.query.filter_by(from_entity_id=entity_id)
        q_to = CipKnowledgeRelation.query.filter_by(to_entity_id=entity_id)
        if allowed_docs is not None:
            q_from = q_from.filter(CipKnowledgeRelation.document_id.in_(allowed_docs))
            q_to = q_to.filter(CipKnowledgeRelation.document_id.in_(allowed_docs))
        edges: list[dict] = []
        for rel in q_from.all():
            edges.append(
                {
                    "neighbour_id": rel.to_entity_id,
                    "relation_type": rel.relation_type,
                    "direction": "out",
                    "confidence": float(rel.confidence or 0.0),
                }
            )
        for rel in q_to.all():
            edges.append(
                {
                    "neighbour_id": rel.from_entity_id,
                    "relation_type": rel.relation_type,
                    "direction": "in",
                    "confidence": float(rel.confidence or 0.0),
                }
            )
        return edges
