"""Decision version identity (AP-002D3)."""

from __future__ import annotations

from dataclasses import dataclass

# Bump when decision mapping / Twin update semantics change.
DECISION_VERSION = "AP-002D3.decision.v1"


@dataclass(frozen=True, slots=True)
class DecisionVersion:
    """Frozen decision contract version."""

    value: str = DECISION_VERSION

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("decision version is required")

    def __str__(self) -> str:
        return self.value
