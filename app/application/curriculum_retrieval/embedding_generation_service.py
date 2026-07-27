"""Generate embeddings for educational entities (not PDFs / pages / chunks)."""

from __future__ import annotations

import hashlib
import logging
import uuid

from app.application.curriculum_retrieval.ports.vector_store_port import (
    EmbeddingModelPort,
    VectorStorePort,
    get_default_embedding_model_port,
    get_default_vector_store_port,
)
from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind
from app.domain.curriculum_retrieval.embedding import (
    EMBEDDABLE_ENTITY_KINDS,
    EmbeddingIndexStatus,
    EmbeddingRecord,
)
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipCurriculumEntity,
    CipEmbeddingRecord,
    CipProvenanceRecord,
)
from app.models.curriculum_studio_foundation import StudioFoundationDocument

logger = logging.getLogger(__name__)


class EmbeddingGenerationService:
    """Build entity text → embedding metadata + vector upsert.

    ``model`` / ``store`` must be injected by the caller's composition root.
    When omitted, the process-local default ports bound by infrastructure
    composition are used (see ``ports.vector_store_port``).
    """

    def __init__(
        self,
        *,
        model: EmbeddingModelPort | None = None,
        store: VectorStorePort | None = None,
    ) -> None:
        resolved_model = model or get_default_embedding_model_port()
        resolved_store = store or get_default_vector_store_port()
        if resolved_model is None or resolved_store is None:
            raise RuntimeError(
                "EmbeddingGenerationService requires an EmbeddingModelPort and "
                "VectorStorePort — inject them or bind process-local defaults "
                "via infrastructure composition"
            )
        self._model = resolved_model
        self._store = resolved_store

    @property
    def model(self) -> EmbeddingModelPort:
        return self._model

    @property
    def store(self) -> VectorStorePort:
        return self._store

    def embed_text(self, text: str) -> tuple[float, ...]:
        """Embed arbitrary text with the configured model."""
        return self._model.embed(text)

    def content_fingerprint(self, *, title: str, body: str, kind: str) -> str:
        """Stable fingerprint of embeddable content."""
        payload = f"{kind}\n{title.strip()}\n{body.strip()}".encode()
        return hashlib.sha256(payload).hexdigest()[:40]

    def build_embed_text(self, entity: CipCurriculumEntity) -> str:
        """Compose educational text for an entity (definitional for concepts)."""
        kind = entity.kind or ""
        title = (entity.title or "").strip()
        body = (entity.body or "").strip()
        # Concepts carry definitional body; other kinds include a kind cue.
        if kind == CurriculumEntityKind.CONCEPT.value:
            return f"Definition: {title}. {body}".strip()
        if kind == CurriculumEntityKind.FORMULA.value:
            return f"Formula: {title}. {body}".strip()
        if kind == CurriculumEntityKind.EXAMPLE.value:
            return f"Worked example: {title}. {body}".strip()
        if kind == CurriculumEntityKind.PRACTICE_QUESTION.value:
            return f"Practice question: {title}. {body}".strip()
        if kind == CurriculumEntityKind.LEARNING_OBJECTIVE.value:
            return f"Learning objective: {title}. {body}".strip()
        return f"{kind.replace('_', ' ').title()}: {title}. {body}".strip()

    def is_embeddable(self, kind: str) -> bool:
        try:
            return CurriculumEntityKind(kind) in EMBEDDABLE_ENTITY_KINDS
        except ValueError:
            return False

    def generate_for_document(
        self,
        *,
        document_id: int,
        workspace_id: str,
        job_id: str = "",
        graph_id: str = "",
    ) -> list[EmbeddingRecord]:
        """Generate / refresh embeddings for all embeddable entities on a document."""
        entities = CipCurriculumEntity.query.filter_by(document_id=document_id).all()
        records: list[EmbeddingRecord] = []
        for entity in entities:
            record = self.generate_for_entity(
                entity,
                workspace_id=workspace_id,
                job_id=job_id,
                graph_id=graph_id,
            )
            if record is not None:
                records.append(record)
        db.session.flush()
        return records

    def generate_for_entity(
        self,
        entity: CipCurriculumEntity,
        *,
        workspace_id: str,
        job_id: str = "",
        graph_id: str = "",
    ) -> EmbeddingRecord | None:
        """Generate embedding for one entity. Skips non-embeddable kinds."""
        if not self.is_embeddable(entity.kind):
            return None

        fingerprint = self.content_fingerprint(
            title=entity.title or "",
            body=entity.body or "",
            kind=entity.kind,
        )
        existing = (
            CipEmbeddingRecord.query.filter_by(
                entity_id=entity.entity_id,
                embedding_version=self._model.embedding_version,
            )
            .order_by(CipEmbeddingRecord.id.desc())
            .first()
        )
        if (
            existing is not None
            and existing.content_fingerprint == fingerprint
            and existing.status == EmbeddingIndexStatus.INDEXED.value
            and existing.model_name == self._model.model_name
        ):
            return self._to_domain(existing)

        provenance = (
            CipProvenanceRecord.query.filter_by(
                subject_kind="entity",
                subject_id=entity.entity_id,
            )
            .order_by(CipProvenanceRecord.id.desc())
            .first()
        )
        provenance_id = provenance.provenance_id if provenance else None

        vector_id = existing.vector_id if existing else f"vec_{uuid.uuid4().hex[:20]}"
        embedding_id = (
            existing.embedding_id if existing else f"emb_{uuid.uuid4().hex[:20]}"
        )

        try:
            text = self.build_embed_text(entity)
            vector = self._model.embed(text)
            self._store.upsert(
                vector_id=vector_id,
                vector=vector,
                metadata={
                    "entity_id": entity.entity_id,
                    "entity_kind": entity.kind,
                    "document_id": str(entity.document_id),
                    "workspace_id": workspace_id,
                },
            )
            status = EmbeddingIndexStatus.INDEXED
            error = ""
        except Exception as exc:  # noqa: BLE001 — persist failure, continue batch
            logger.exception("Embedding failed for entity %s", entity.entity_id)
            status = EmbeddingIndexStatus.FAILED
            error = str(exc)[:500]

        if existing is None:
            row = CipEmbeddingRecord(
                embedding_id=embedding_id,
                entity_id=entity.entity_id,
                entity_kind=entity.kind,
                document_id=int(entity.document_id),
                workspace_id=workspace_id,
                vector_id=vector_id,
                model_name=self._model.model_name,
                embedding_version=self._model.embedding_version,
                dimensions=self._model.dimensions,
                status=status.value,
                content_fingerprint=fingerprint,
                provenance_id=provenance_id,
                graph_id=graph_id or "",
                job_id=job_id or "",
                error_message=error,
            )
            db.session.add(row)
        else:
            row = existing
            row.entity_kind = entity.kind
            row.document_id = int(entity.document_id)
            row.workspace_id = workspace_id
            row.model_name = self._model.model_name
            row.dimensions = self._model.dimensions
            row.status = status.value
            row.content_fingerprint = fingerprint
            row.provenance_id = provenance_id
            row.graph_id = graph_id or row.graph_id
            row.job_id = job_id or row.job_id
            row.error_message = error

        db.session.flush()
        return self._to_domain(row)

    def status_for_workspace(self, workspace_id: str) -> dict:
        """Aggregate embedding index status for Founder UI."""
        doc_ids = [
            int(d.id)
            for d in StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id
            ).all()
        ]
        if not doc_ids:
            return {
                "workspace_id": workspace_id,
                "indexed": 0,
                "pending": 0,
                "failed": 0,
                "stale": 0,
                "skipped": 0,
                "total": 0,
                "model_name": self._model.model_name,
                "embedding_version": self._model.embedding_version,
                "dimensions": self._model.dimensions,
                "vector_count": 0,
            }

        rows = CipEmbeddingRecord.query.filter(
            CipEmbeddingRecord.document_id.in_(doc_ids)
        ).all()
        counts = {
            "indexed": 0,
            "pending": 0,
            "failed": 0,
            "stale": 0,
            "skipped": 0,
        }
        for row in rows:
            key = (row.status or "pending").lower()
            if key in counts:
                counts[key] += 1
        return {
            "workspace_id": workspace_id,
            **counts,
            "total": len(rows),
            "model_name": self._model.model_name,
            "embedding_version": self._model.embedding_version,
            "dimensions": self._model.dimensions,
            "vector_count": self._store.count(
                filter_metadata={"workspace_id": workspace_id}
            ),
        }

    def _to_domain(self, row: CipEmbeddingRecord) -> EmbeddingRecord:
        try:
            status = EmbeddingIndexStatus(row.status)
        except ValueError:
            status = EmbeddingIndexStatus.PENDING
        return EmbeddingRecord(
            embedding_id=row.embedding_id,
            entity_id=row.entity_id,
            entity_kind=row.entity_kind,
            document_id=int(row.document_id),
            workspace_id=row.workspace_id,
            vector_id=row.vector_id,
            model_name=row.model_name,
            embedding_version=row.embedding_version,
            dimensions=int(row.dimensions),
            status=status,
            content_fingerprint=row.content_fingerprint,
            provenance_id=row.provenance_id,
            graph_id=row.graph_id or "",
            job_id=row.job_id or "",
            error_message=row.error_message or "",
        )
