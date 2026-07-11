"""Aggregate outcome of a Twin Update Pipeline run.

An UpdateResult is the sole output of the pipeline. It records the original
and updated Twin snapshots, which strategies ran, and processing messages.
It does not persist, recommend, or encode educational algorithms.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from app.domain.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class UpdateResult:
    """Outcome of coordinating Twin updates via registered strategies.

    Attributes:
        original_twin: Twin snapshot supplied to the pipeline.
        updated_twin: Twin snapshot after applicable strategies (may equal
            ``original_twin`` when nothing changed).
        applied_strategies: Names of strategies that ran, in execution order.
        processing_messages: Human-readable pipeline notes.
        success: True when the pipeline completed without strategy failure.
    """

    original_twin: DigitalTwin
    updated_twin: DigitalTwin
    applied_strategies: tuple[str, ...] = field(default_factory=tuple)
    processing_messages: tuple[str, ...] = field(default_factory=tuple)
    success: bool = True

    @classmethod
    def create(
        cls,
        original_twin: DigitalTwin,
        updated_twin: DigitalTwin,
        *,
        applied_strategies: Sequence[str] | Iterable[str] | None = None,
        processing_messages: Sequence[str] | Iterable[str] | None = None,
        success: bool = True,
    ) -> UpdateResult:
        """Construct an UpdateResult.

        Args:
            original_twin: Twin passed into the pipeline.
            updated_twin: Twin produced by the pipeline.
            applied_strategies: Optional strategy name list (defaults empty).
            processing_messages: Optional message list (defaults empty).
            success: Whether the run completed successfully (defaults True).

        Returns:
            A frozen UpdateResult instance.
        """
        return cls(
            original_twin=original_twin,
            updated_twin=updated_twin,
            applied_strategies=tuple(applied_strategies or ()),
            processing_messages=tuple(processing_messages or ()),
            success=success,
        )
