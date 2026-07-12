"""Abstract update strategy interface for the Twin Update Pipeline.

Specialised strategies (KnowledgeUpdateStrategy, MemoryUpdateStrategy,
BehaviourUpdateStrategy, PerformanceUpdateStrategy, PredictionSnapshotStrategy,
…) inherit from this base. This module defines the contract only — no
educational update algorithms live here.

Readiness Aggregation (``app.domain.readiness``) is **not** an Update Strategy:
it is a read-side derive over Twin + Curriculum + Goals and must never be
registered on the Twin Update Pipeline as a belief writer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.update_context import UpdateContext


class BaseUpdateStrategy(ABC):
    """Strategy interface: UpdateContext → new DigitalTwin snapshot.

    Implementations must remain pure domain logic: produce a new immutable
    Twin from context without mutating inputs, persisting, recommending,
    planning, or importing frameworks.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable strategy identifier recorded in UpdateResult."""

    @abstractmethod
    def supports(self, context: UpdateContext) -> bool:
        """Return True if this strategy should run for ``context``.

        Args:
            context: Immutable update context under consideration.

        Returns:
            Whether ``apply`` should be invoked for this context.
        """

    @abstractmethod
    def apply(self, context: UpdateContext) -> DigitalTwin:
        """Produce an updated Twin snapshot from ``context``.

        Args:
            context: Immutable update context previously accepted by
                ``supports``. Must not be mutated. The Twin inside the
                context must not be mutated in place.

        Returns:
            A new (or identical) DigitalTwin instance. Never persists,
            recommends, plans, or encodes educational scoring here in the
            framework contract — specialised strategies own belief revision
            in later capabilities.
        """
