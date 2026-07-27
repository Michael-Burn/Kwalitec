"""CIP-003 curriculum retrieval infrastructure adapters."""

from __future__ import annotations

from app.infrastructure.adapters.curriculum_retrieval.hashing_embedding_model import (
    HashingEmbeddingModel,
    cosine_similarity,
)
from app.infrastructure.adapters.curriculum_retrieval.local_vector_store import (
    LocalVectorStoreAdapter,
)

__all__ = [
    "HashingEmbeddingModel",
    "LocalVectorStoreAdapter",
    "cosine_similarity",
]


def get_retrieval_embedding_extension():
    """Lazy factory to avoid circular imports with application services."""
    from app.infrastructure.adapters.curriculum_retrieval.embedding_extension import (
        RetrievalEmbeddingExtension,
    )

    return RetrievalEmbeddingExtension()
