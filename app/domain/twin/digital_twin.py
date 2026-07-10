"""Student Digital Twin aggregate.

Immutable composition of learner-state domains. Exposes state objects only —
no update pipeline, persistence, prediction, or recommendation logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.goal_state import GoalState
from app.domain.twin.identity_state import IdentityState
from app.domain.twin.knowledge_state import KnowledgeState
from app.domain.twin.memory_state import MemoryState
from app.domain.twin.performance_state import PerformanceState
from app.domain.twin.prediction_state import PredictionState


@dataclass(frozen=True)
class DigitalTwin:
    """Authoritative learner-state aggregate for one student.

    The Twin is the single source of truth for learner state relative to a
    syllabus and sitting. This object holds structural domain snapshots; later
    capabilities update and consume them.

    Attributes:
        identity: Who the learner is.
        goals: What the learner is trying to achieve.
        knowledge: Current knowledge structure.
        memory: Current retention structure.
        behaviour: Study behaviour structure.
        performance: Assessment performance structure.
        predictions: Current prediction snapshots.
    """

    identity: IdentityState
    goals: GoalState
    knowledge: KnowledgeState
    memory: MemoryState
    behaviour: BehaviourState
    performance: PerformanceState
    predictions: PredictionState

    @classmethod
    def create(
        cls,
        identity: IdentityState,
        *,
        goals: GoalState | None = None,
        knowledge: KnowledgeState | None = None,
        memory: MemoryState | None = None,
        behaviour: BehaviourState | None = None,
        performance: PerformanceState | None = None,
        predictions: PredictionState | None = None,
    ) -> DigitalTwin:
        """Construct a DigitalTwin aggregate.

        Omitted domain states default to empty structural snapshots so a Twin
        can be born with Identity alone.

        Args:
            identity: Required identity state (scopes the Twin).
            goals: Optional goals state (defaults to empty).
            knowledge: Optional knowledge state (defaults to empty).
            memory: Optional memory state (defaults to empty).
            behaviour: Optional behaviour state (defaults to empty).
            performance: Optional performance state (defaults to empty).
            predictions: Optional prediction state (defaults to empty).

        Returns:
            A frozen DigitalTwin instance.
        """
        return cls(
            identity=identity,
            goals=goals if goals is not None else GoalState.create(),
            knowledge=knowledge if knowledge is not None else KnowledgeState.create(),
            memory=memory if memory is not None else MemoryState.create(),
            behaviour=behaviour if behaviour is not None else BehaviourState.create(),
            performance=(
                performance if performance is not None else PerformanceState.create()
            ),
            predictions=(
                predictions if predictions is not None else PredictionState.create()
            ),
        )
