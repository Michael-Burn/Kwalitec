"""Update strategy package for the Twin Update Pipeline.

Contains the abstract strategy contract and concrete update strategies
registered with ``TwinUpdatePipeline``. Further specialised strategies
(PredictionSnapshotStrategy, …) land in later capabilities.
"""

from __future__ import annotations

from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.strategies.behaviour_update_strategy import (
    BEHAVIOUR_EVIDENCE_TYPES,
    BehaviourUpdateStrategy,
)
from app.domain.twin.strategies.knowledge_update_strategy import (
    KNOWLEDGE_EVIDENCE_TYPES,
    KnowledgeUpdateStrategy,
)
from app.domain.twin.strategies.memory_update_strategy import (
    MEMORY_EVIDENCE_TYPES,
    MemoryUpdateStrategy,
)
from app.domain.twin.strategies.performance_update_strategy import (
    PERFORMANCE_EVIDENCE_TYPES,
    PerformanceUpdateStrategy,
)

__all__ = [
    "BEHAVIOUR_EVIDENCE_TYPES",
    "BaseUpdateStrategy",
    "BehaviourUpdateStrategy",
    "KNOWLEDGE_EVIDENCE_TYPES",
    "KnowledgeUpdateStrategy",
    "MEMORY_EVIDENCE_TYPES",
    "MemoryUpdateStrategy",
    "PERFORMANCE_EVIDENCE_TYPES",
    "PerformanceUpdateStrategy",
]
