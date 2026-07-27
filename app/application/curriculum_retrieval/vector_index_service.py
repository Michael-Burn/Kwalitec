"""Vector index orchestration — application façade over VectorStorePort."""

from __future__ import annotations

from app.application.curriculum_retrieval.embedding_generation_service import (
    EmbeddingGenerationService,
)
from app.application.curriculum_retrieval.ports.vector_store_port import (
    EmbeddingModelPort,
    VectorHit,
    VectorStorePort,
)
from app.domain.curriculum_retrieval.embedding import EmbeddingIndexStatus
from app.models.curriculum_intelligence import CipEmbeddingRecord


class VectorIndexService:
    """Own index lifecycle: rebuild, search by text, resolve vector → entity."""

    def __init__(
        self,
        *,
        embeddings: EmbeddingGenerationService | None = None,
        model: EmbeddingModelPort | None = None,
        store: VectorStorePort | None = None,
    ) -> None:
        self._embeddings = embeddings or EmbeddingGenerationService(
            model=model, store=store
        )

    @property
    def embeddings(self) -> EmbeddingGenerationService:
        return self._embeddings

    def rebuild_document(
        self,
        *,
        document_id: int,
        workspace_id: str,
        job_id: str = "",
        graph_id: str = "",
    ) -> int:
        """(Re)index all embeddable entities for a document. Returns indexed count."""
        records = self._embeddings.generate_for_document(
            document_id=document_id,
            workspace_id=workspace_id,
            job_id=job_id,
            graph_id=graph_id,
        )
        return sum(
            1 for r in records if r.status is EmbeddingIndexStatus.INDEXED
        )

    def search(
        self,
        *,
        query_text: str,
        workspace_id: str,
        limit: int = 20,
        document_id: int | None = None,
    ) -> list[tuple[str, float]]:
        """Semantic search → list of (entity_id, similarity). Never exposes vectors."""
        query_vector = self._embeddings.embed_text(query_text)
        filters: dict[str, str] = {"workspace_id": workspace_id}
        if document_id is not None:
            filters["document_id"] = str(document_id)
        hits = self._embeddings.store.search(
            query_vector=query_vector,
            limit=limit,
            filter_metadata=filters,
        )
        return self._hits_to_entities(hits)

    def resolve_vector_id(self, vector_id: str) -> CipEmbeddingRecord | None:
        """Map opaque vector_id to embedding metadata row."""
        return CipEmbeddingRecord.query.filter_by(vector_id=vector_id).first()

    def _hits_to_entities(self, hits: list[VectorHit]) -> list[tuple[str, float]]:
        results: list[tuple[str, float]] = []
        seen: set[str] = set()
        for hit in hits:
            meta = dict(hit.metadata)
            entity_id = meta.get("entity_id")
            if not entity_id:
                row = self.resolve_vector_id(hit.vector_id)
                entity_id = row.entity_id if row else None
            if not entity_id or entity_id in seen:
                continue
            seen.add(entity_id)
            results.append((entity_id, float(hit.score)))
        return results
