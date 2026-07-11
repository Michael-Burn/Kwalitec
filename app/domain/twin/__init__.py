"""Student Digital Twin domain package.

Framework-independent immutable state objects representing a learner's current
exam-preparation state, plus the Twin Update Pipeline orchestration framework.
See README.md.
"""

from __future__ import annotations

from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.goal_state import GoalState
from app.domain.twin.identity_state import IdentityState
from app.domain.twin.knowledge_state import KnowledgeState, TopicMasteryRecord
from app.domain.twin.memory_state import MemoryState, RetentionRecord
from app.domain.twin.performance_state import PerformanceState, PerformanceSummary
from app.domain.twin.prediction_state import PredictionState
from app.domain.twin.strategies import (
    KNOWLEDGE_EVIDENCE_TYPES,
    BaseUpdateStrategy,
    KnowledgeUpdateStrategy,
)
from app.domain.twin.update_context import UpdateContext
from app.domain.twin.update_pipeline import TwinUpdatePipeline
from app.domain.twin.update_result import UpdateResult
from app.domain.twin.update_strategy import UpdateStrategy

__all__ = [
    "BaseUpdateStrategy",
    "BehaviourState",
    "DigitalTwin",
    "GoalState",
    "IdentityState",
    "KNOWLEDGE_EVIDENCE_TYPES",
    "KnowledgeState",
    "KnowledgeUpdateStrategy",
    "MemoryState",
    "PerformanceState",
    "PerformanceSummary",
    "PredictionState",
    "RetentionRecord",
    "TopicMasteryRecord",
    "TwinUpdatePipeline",
    "UpdateContext",
    "UpdateResult",
    "UpdateStrategy",
]
