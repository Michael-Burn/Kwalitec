"""CIP-003 curriculum retrieval infrastructure adapters."""

from __future__ import annotations

from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    bind_default_embedding_extension_port,
)
from app.application.curriculum_retrieval.ports.vector_store_port import (
    bind_default_embedding_model_port,
    bind_default_vector_store_port,
)
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

# Process-local default ports for application services that do not receive
# explicit injection (e.g. ``EmbeddingGenerationService()`` bare construction).
# Embedding model / vector store must bind before the embedding extension,
# which eagerly constructs a VectorIndexService → EmbeddingGenerationService.
bind_default_embedding_model_port(HashingEmbeddingModel())
bind_default_vector_store_port(LocalVectorStoreAdapter())

from app.infrastructure.adapters.curriculum_retrieval.embedding_extension import (  # noqa: E402
    RetrievalEmbeddingExtension,
)

bind_default_embedding_extension_port(RetrievalEmbeddingExtension())


def get_retrieval_embedding_extension():
    """Lazy factory to avoid circular imports with application services."""
    from app.infrastructure.adapters.curriculum_retrieval.embedding_extension import (
        RetrievalEmbeddingExtension,
    )

    return RetrievalEmbeddingExtension()
