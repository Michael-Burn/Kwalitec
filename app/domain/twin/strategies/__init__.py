"""Update strategy package for the Twin Update Pipeline.

Contains the abstract strategy contract. Specialised strategies
(KnowledgeUpdateStrategy, MemoryUpdateStrategy, BehaviourUpdateStrategy,
PerformanceUpdateStrategy, PredictionSnapshotStrategy, …) are registered
with ``TwinUpdatePipeline`` in later capabilities.
"""

from __future__ import annotations

from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy

__all__ = [
    "BaseUpdateStrategy",
]
