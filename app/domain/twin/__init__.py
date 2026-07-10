"""Student Digital Twin domain package.

Framework-independent immutable state objects representing a learner's current
exam-preparation state. See README.md.
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

__all__ = [
    "BehaviourState",
    "DigitalTwin",
    "GoalState",
    "IdentityState",
    "KnowledgeState",
    "MemoryState",
    "PerformanceState",
    "PerformanceSummary",
    "PredictionState",
    "RetentionRecord",
    "TopicMasteryRecord",
]
