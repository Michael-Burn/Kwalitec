"""Tutor explanation version identity (AP-002D6)."""

from __future__ import annotations

from dataclasses import dataclass

# Bump when explanation schema / section semantics change.
EXPLANATION_VERSION = "AP-002D6.explanation.v1"


@dataclass(frozen=True, slots=True)
class ExplanationVersion:
    """Frozen Tutor explanation contract version."""

    value: str = EXPLANATION_VERSION

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("explanation version is required")

    def __str__(self) -> str:
        return self.value
