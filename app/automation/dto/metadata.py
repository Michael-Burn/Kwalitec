"""Immutable workflow metadata exposed by the registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowMetadata:
    """Read-only description of a registered automation workflow."""

    id: str
    name: str
    description: str
