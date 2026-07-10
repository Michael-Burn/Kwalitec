"""Performance domain state for the Student Digital Twin.

Represents assessment performance structure. Structural slots only — no
accuracy trends, calibration math, or scoring algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class PerformanceSummary:
    """Structural performance summary for a scoped assessment slice.

    Attributes:
        scope_id: Scope identity (topic, quiz, mock, or similar).
        summary: Structured facts describing observed performance
            (stored, not computed here).
    """

    scope_id: str
    summary: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        scope_id: str,
        *,
        summary: dict[str, Any] | None = None,
    ) -> PerformanceSummary:
        """Construct a PerformanceSummary.

        Args:
            scope_id: Non-empty scope identity.
            summary: Optional structured performance facts.

        Returns:
            A frozen PerformanceSummary.

        Raises:
            ValueError: If ``scope_id`` is empty or blank.
        """
        normalized = scope_id.strip() if isinstance(scope_id, str) else ""
        if not normalized:
            raise ValueError("scope_id must be a non-empty string")
        return cls(scope_id=normalized, summary=dict(summary or {}))


@dataclass(frozen=True)
class PerformanceState:
    """Measured assessment performance structure for the learner.

    Attributes:
        assessment_ids: References to assessment / attempt evidence.
        performance_summaries: Structural performance summary collection.
        last_updated: When this performance snapshot was last materialised.
    """

    assessment_ids: tuple[str, ...] = ()
    performance_summaries: tuple[PerformanceSummary, ...] = ()
    last_updated: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        assessment_ids: list[str] | tuple[str, ...] | None = None,
        performance_summaries: list[PerformanceSummary]
        | tuple[PerformanceSummary, ...]
        | None = None,
        last_updated: datetime | None = None,
    ) -> PerformanceState:
        """Construct a PerformanceState.

        Args:
            assessment_ids: Optional assessment reference collection.
            performance_summaries: Optional performance summary collection.
            last_updated: Optional materialisation timestamp.

        Returns:
            A frozen PerformanceState instance.
        """
        return cls(
            assessment_ids=tuple(assessment_ids or ()),
            performance_summaries=tuple(performance_summaries or ()),
            last_updated=last_updated,
        )
