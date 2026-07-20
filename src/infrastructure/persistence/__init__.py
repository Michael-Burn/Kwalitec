"""Persistence layer — mapping (INF-001), models (INF-002), repositories (INF-003).

Mappers perform pure structural conversion between domain aggregates and
persistence DTOs. SQLAlchemy models and repository adapters live under
``persistence.sqlalchemy``.

Root re-exports for mappers are lazy so importing ``persistence.sqlalchemy``
does not load the domain graph.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "DigitalTwinMapper",
    "LearningEpisodeMapper",
    "EvidenceMapper",
    "SubjectKnowledgeMapper",
    "DiagnosisMapper",
    "HypothesisMapper",
    "PriorityMapper",
    "TeachingIntentionMapper",
    "TeachingStrategyMapper",
    "DecisionMapper",
    "OrchestratorMapper",
]

_MAPPER_EXPORTS = frozenset(__all__)


def __getattr__(name: str) -> Any:
    if name in _MAPPER_EXPORTS:
        from infrastructure.persistence import mappers

        return getattr(mappers, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
