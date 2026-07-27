"""Ports for curriculum evidence retrieval (CIP-003).

Application and domain never depend on a concrete vector technology or
embedding model implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class VectorHit:
    """Opaque vector-store hit keyed by vector_id (infrastructure concern).

    Application services map vector_id → educational entity via embedding
    metadata — consumers never see this type.
    """

    vector_id: str
    score: float
    metadata: tuple[tuple[str, str], ...] = ()


class EmbeddingModelPort(ABC):
    """Produce deterministic dense vectors for educational text."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Stable model identifier persisted with embedding metadata."""

    @property
    @abstractmethod
    def embedding_version(self) -> str:
        """Model version token."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Fixed output dimensionality."""

    @abstractmethod
    def embed(self, text: str) -> tuple[float, ...]:
        """Embed text into a fixed-length float vector."""


class VectorStorePort(ABC):
    """Abstract vector index. Only infrastructure adapters implement this."""

    @abstractmethod
    def upsert(
        self,
        *,
        vector_id: str,
        vector: tuple[float, ...],
        metadata: dict[str, str] | None = None,
    ) -> None:
        """Insert or replace a vector by id."""

    @abstractmethod
    def delete(self, vector_id: str) -> None:
        """Remove a vector if present."""

    @abstractmethod
    def search(
        self,
        *,
        query_vector: tuple[float, ...],
        limit: int = 10,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[VectorHit]:
        """Return top-k hits by cosine similarity (deterministic tie-break)."""

    @abstractmethod
    def get(self, vector_id: str) -> tuple[float, ...] | None:
        """Return a stored vector payload, or None."""

    @abstractmethod
    def count(self, *, filter_metadata: dict[str, str] | None = None) -> int:
        """Count indexed vectors, optionally filtered by metadata."""


# Process-local default ports (bound by infrastructure composition / tests).
# Application services fall back to these when no port is explicitly injected
# so existing call sites keep working without importing infrastructure here.
_default_embedding_model: EmbeddingModelPort | None = None
_default_vector_store: VectorStorePort | None = None


def bind_default_embedding_model_port(port: EmbeddingModelPort | None) -> None:
    """Bind the process-local default embedding model (composition / tests)."""
    global _default_embedding_model
    _default_embedding_model = port


def get_default_embedding_model_port() -> EmbeddingModelPort | None:
    """Return the bound default embedding model port, or None when unbound."""
    return _default_embedding_model


def bind_default_vector_store_port(port: VectorStorePort | None) -> None:
    """Bind the process-local default vector store (composition / tests)."""
    global _default_vector_store
    _default_vector_store = port


def get_default_vector_store_port() -> VectorStorePort | None:
    """Return the bound default vector store port, or None when unbound."""
    return _default_vector_store
