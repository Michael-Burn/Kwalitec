"""Deterministic Phase-1 embedding model — feature hashing, no external deps.

Suitable for development and tests. Replaceable via EmbeddingModelPort without
domain changes (future: sentence-transformers, commercial APIs).
"""

from __future__ import annotations

import hashlib
import math
import re

from app.application.curriculum_retrieval.ports.vector_store_port import (
    EmbeddingModelPort,
)
from app.domain.curriculum_retrieval.embedding import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_EMBEDDING_VERSION,
)

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


class HashingEmbeddingModel(EmbeddingModelPort):
    """Bag-of-hashed-tokens embedding with L2 normalisation."""

    def __init__(
        self,
        *,
        dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        embedding_version: str = DEFAULT_EMBEDDING_VERSION,
    ) -> None:
        if dimensions < 8:
            raise ValueError("dimensions must be >= 8")
        self._dimensions = dimensions
        self._model_name = model_name
        self._embedding_version = embedding_version

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def embedding_version(self) -> str:
        return self._embedding_version

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str) -> tuple[float, ...]:
        tokens = _TOKEN_RE.findall((text or "").lower())
        vec = [0.0] * self._dimensions
        if not tokens:
            # Stable non-zero placeholder so empty text remains searchable.
            seed = hashlib.sha256(b"empty").digest()
            for i in range(self._dimensions):
                vec[i] = ((seed[i % len(seed)] / 255.0) * 2.0) - 1.0
            return _l2_normalise(vec)

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self._dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            # Mild TF weighting via repeat count is implicit via accumulation.
            vec[index] += sign
            # Bigram hash for short phrases
            if len(token) >= 3:
                bi = hashlib.sha256((token[:3]).encode("utf-8")).digest()
                bi_index = int.from_bytes(bi[:4], "big") % self._dimensions
                bi_sign = 1.0 if bi[4] % 2 == 0 else -1.0
                vec[bi_index] += 0.5 * bi_sign

        return _l2_normalise(vec)


def _l2_normalise(values: list[float]) -> tuple[float, ...]:
    norm = math.sqrt(sum(v * v for v in values))
    if norm <= 0:
        return tuple(0.0 for _ in values)
    return tuple(v / norm for v in values)


def cosine_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """Cosine similarity for equal-length vectors (already L2-normalised → dot)."""
    if len(a) != len(b) or not a:
        return 0.0
    return float(sum(x * y for x, y in zip(a, b, strict=True)))
