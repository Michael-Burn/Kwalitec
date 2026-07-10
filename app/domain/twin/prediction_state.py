"""Prediction domain state for the Student Digital Twin.

Represents current prediction snapshots. Structural storage only — no
prediction algorithms, calibration, or forecasting logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def _validate_probability(name: str, value: float | None) -> None:
    if value is not None and not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0 inclusive, got {value}")


@dataclass(frozen=True)
class PredictionState:
    """Forward-looking estimate snapshots derived elsewhere from Twin state.

    Attributes:
        readiness_snapshot: Stored readiness estimate when available.
        pass_probability_snapshot: Stored pass-probability estimate when
            available (0–1).
        as_of: Timestamp for which the snapshots apply.
        metadata: Extensible prediction metadata (model version, factors, …).
    """

    readiness_snapshot: float | None = None
    pass_probability_snapshot: float | None = None
    as_of: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        readiness_snapshot: float | None = None,
        pass_probability_snapshot: float | None = None,
        as_of: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PredictionState:
        """Construct a PredictionState.

        Args:
            readiness_snapshot: Optional stored readiness estimate.
            pass_probability_snapshot: Optional pass probability in
                ``[0.0, 1.0]``.
            as_of: Optional as-of timestamp for the snapshots.
            metadata: Optional extensible metadata bag.

        Returns:
            A frozen PredictionState instance.

        Raises:
            ValueError: If ``pass_probability_snapshot`` is out of range.
        """
        _validate_probability(
            "pass_probability_snapshot", pass_probability_snapshot
        )
        return cls(
            readiness_snapshot=readiness_snapshot,
            pass_probability_snapshot=pass_probability_snapshot,
            as_of=as_of,
            metadata=dict(metadata or {}),
        )
