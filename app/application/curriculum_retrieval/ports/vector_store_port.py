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
