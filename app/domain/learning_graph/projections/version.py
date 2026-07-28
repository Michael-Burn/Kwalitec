"""Projection version identity (AP-002D4)."""

from __future__ import annotations

from dataclasses import dataclass

# Bump when projection mapping / relationship semantics change.
PROJECTION_VERSION = "AP-002D4.projection.v1"


@dataclass(frozen=True, slots=True)
class ProjectionVersion:
    """Frozen Learning Graph projection contract version."""

    value: str = PROJECTION_VERSION

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("projection version is required")

    def __str__(self) -> str:
        return self.value
