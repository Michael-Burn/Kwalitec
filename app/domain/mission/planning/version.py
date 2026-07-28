"""Mission planning version identity (AP-002D5)."""

from __future__ import annotations

from dataclasses import dataclass

# Bump when planning mapping / mission candidate semantics change.
PLANNING_VERSION = "AP-002D5.planning.v1"


@dataclass(frozen=True, slots=True)
class PlanningVersion:
    """Frozen Mission Engine planning contract version."""

    value: str = PLANNING_VERSION

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("planning version is required")

    def __str__(self) -> str:
        return self.value
