"""Update strategy package for the Twin Update Pipeline.

Contains the abstract strategy contract and concrete update strategies
registered with ``TwinUpdatePipeline``. Further specialised strategies
(BehaviourUpdateStrategy, PerformanceUpdateStrategy,
PredictionSnapshotStrategy, …) land in later capabilities.
"""

from __future__ import annotations

from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.strategies.knowledge_update_strategy import (
    KNOWLEDGE_EVIDENCE_TYPES,
    KnowledgeUpdateStrategy,
)
from app.domain.twin.strategies.memory_update_strategy import (
    MEMORY_EVIDENCE_TYPES,
    MemoryUpdateStrategy,
)

__all__ = [
    "BaseUpdateStrategy",
    "KNOWLEDGE_EVIDENCE_TYPES",
    "KnowledgeUpdateStrategy",
    "MEMORY_EVIDENCE_TYPES",
    "MemoryUpdateStrategy",
]
