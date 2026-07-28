"""Interpretation version identity (AP-002D2)."""

from __future__ import annotations

from dataclasses import dataclass

# Bump when interpretation mapping / category semantics change.
INTERPRETATION_VERSION = "AP-002D2.interpretation.v1"


@dataclass(frozen=True, slots=True)
class InterpretationVersion:
    """Frozen interpreter contract version."""

    value: str = INTERPRETATION_VERSION

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("interpretation version is required")

    def __str__(self) -> str:
        return self.value
