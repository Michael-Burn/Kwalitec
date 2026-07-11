"""Twin Update Pipeline coordinator.

Accepts a Digital Twin and one or more Learning Evidence records, invokes
registered update strategies that support the context, and returns an
UpdateResult with a new Twin snapshot. Orchestration only — no educational
algorithms, persistence, recommendations, or planning.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.update_context import UpdateContext
from app.domain.twin.update_result import UpdateResult


class TwinUpdatePipeline:
    """Registry-backed coordinator that invokes applicable update strategies.

    Additional strategies are registered without modifying this class
    (open for extension). Invocation order follows registration order.
    Every registered strategy that reports ``supports(context)`` is applied;
    each application receives a context whose Twin reflects prior strategies.
    """

    def __init__(
        self, strategies: list[BaseUpdateStrategy] | None = None
    ) -> None:
        """Initialise with an optional initial strategy list.

        Args:
            strategies: Strategies to register at construction time.
        """
        self._strategies: list[BaseUpdateStrategy] = list(strategies or [])

    def register(self, strategy: BaseUpdateStrategy) -> None:
        """Register a strategy for future invocations.

        Args:
            strategy: Strategy implementation to add to the registry.
        """
        self._strategies.append(strategy)

    @property
    def strategies(self) -> tuple[BaseUpdateStrategy, ...]:
        """Return a snapshot of registered strategies (registration order)."""
        return tuple(self._strategies)

    def update(
        self,
        twin: DigitalTwin,
        evidence: LearningEvidence | Sequence[LearningEvidence],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> UpdateResult:
        """Coordinate Twin updates from ``evidence`` via registered strategies.

        Args:
            twin: Current Digital Twin snapshot. Not mutated.
            evidence: One or more Learning Evidence records. Not mutated.
            metadata: Optional processing metadata copied into UpdateContext.

        Returns:
            UpdateResult containing original and updated Twin snapshots.
            When no strategies are registered, ``updated_twin`` is the
            original Twin and processing messages explain the no-op.

        Notes:
            Does not persist, recommend, plan, or implement educational
            belief-revision algorithms. Strategies own domain-specific logic
            in later capabilities.
        """
        context = UpdateContext.create(twin, evidence, metadata=metadata)
        messages: list[str] = []

        if not self._strategies:
            messages.append(
                "No update strategies registered; returning original Twin."
            )
            return UpdateResult.create(
                original_twin=twin,
                updated_twin=twin,
                applied_strategies=(),
                processing_messages=messages,
                success=True,
            )

        current_twin = twin
        applied: list[str] = []

        for strategy in self._strategies:
            if not strategy.supports(context):
                messages.append(
                    f"Skipped strategy {strategy.name!r} (not applicable)."
                )
                continue
            current_twin = strategy.apply(context)
            applied.append(strategy.name)
            messages.append(f"Applied strategy {strategy.name!r}.")
            context = context.with_twin(current_twin)

        if not applied:
            messages.append(
                "No applicable update strategies; returning original Twin."
            )

        return UpdateResult.create(
            original_twin=twin,
            updated_twin=current_twin,
            applied_strategies=applied,
            processing_messages=messages,
            success=True,
        )
