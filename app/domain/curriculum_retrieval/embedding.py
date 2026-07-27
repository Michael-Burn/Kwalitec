"""Embedding metadata contracts for CIP-003.

Embeddings attach to educational entities (not PDF pages or arbitrary chunks).
Vector payloads live behind VectorStorePort — never in domain objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind

# Phase-1 deterministic hashing embedder identity (no external model).
DEFAULT_EMBEDDING_MODEL = "kwalitec.hash_v1"
DEFAULT_EMBEDDING_VERSION = "1"
DEFAULT_EMBEDDING_DIMENSIONS = 64

# Entities eligible for embedding generation.
EMBEDDABLE_ENTITY_KINDS: frozenset[CurriculumEntityKind] = frozenset(
    {
        CurriculumEntityKind.LEARNING_OBJECTIVE,
        CurriculumEntityKind.CONCEPT,
        CurriculumEntityKind.FORMULA,
        CurriculumEntityKind.EXAMPLE,
        CurriculumEntityKind.PRACTICE_QUESTION,
        CurriculumEntityKind.TOPIC,
        CurriculumEntityKind.SUBTOPIC,
    }
)


class EmbeddingIndexStatus(StrEnum):
    """Lifecycle of an entity embedding in the index."""

    PENDING = "pending"
    INDEXED = "indexed"
    STALE = "stale"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class EmbeddingRecord:
    """Metadata for one entity embedding (no vector payload)."""

    embedding_id: str
    entity_id: str
    entity_kind: str
    document_id: int
    workspace_id: str
    vector_id: str
    model_name: str
    embedding_version: str
    dimensions: int
    status: EmbeddingIndexStatus
    content_fingerprint: str
    provenance_id: str | None = None
    graph_id: str = ""
    job_id: str = ""
    error_message: str = ""
