"""Curriculum Evidence Retrieval (CIP-003) domain package.

Canonical evidence retrieval contracts. Every future AI capability must consume
curriculum evidence through CurriculumRetrievalService — never via direct
vector-store access.

No LLM. Embeddings are one retrieval strategy among graph, provenance,
confidence, metadata, and policy.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "DEFAULT_EMBEDDING_DIMENSIONS",
    "DEFAULT_EMBEDDING_MODEL",
    "DEFAULT_EMBEDDING_VERSION",
    "EMBEDDABLE_ENTITY_KINDS",
    "EmbeddingIndexStatus",
    "EmbeddingRecord",
    "EvidenceItem",
    "QueryIntent",
    "RankedEvidence",
    "RankingBreakdown",
    "RankingWeights",
    "RetrievalDiagnostics",
    "RetrievalProfile",
    "RetrievalQuery",
    "RetrievalResult",
    "detect_intent",
]

_EXPORT_MODULES = {
    "QueryIntent": "app.domain.curriculum_retrieval.intent",
    "detect_intent": "app.domain.curriculum_retrieval.intent",
    "RetrievalProfile": "app.domain.curriculum_retrieval.profile",
    "RankingWeights": "app.domain.curriculum_retrieval.profile",
    "RetrievalQuery": "app.domain.curriculum_retrieval.query",
    "EvidenceItem": "app.domain.curriculum_retrieval.result",
    "RankedEvidence": "app.domain.curriculum_retrieval.result",
    "RetrievalResult": "app.domain.curriculum_retrieval.result",
    "RetrievalDiagnostics": "app.domain.curriculum_retrieval.result",
    "RankingBreakdown": "app.domain.curriculum_retrieval.ranking",
    "EmbeddingRecord": "app.domain.curriculum_retrieval.embedding",
    "EmbeddingIndexStatus": "app.domain.curriculum_retrieval.embedding",
    "EMBEDDABLE_ENTITY_KINDS": "app.domain.curriculum_retrieval.embedding",
    "DEFAULT_EMBEDDING_MODEL": "app.domain.curriculum_retrieval.embedding",
    "DEFAULT_EMBEDDING_VERSION": "app.domain.curriculum_retrieval.embedding",
    "DEFAULT_EMBEDDING_DIMENSIONS": "app.domain.curriculum_retrieval.embedding",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
