"""Reasoning history — explainable audit of Twin updates."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

REASONING_VERSION = "sdt001.reasoning_v1"


@dataclass(frozen=True)
class ReasoningStep:
    """One explainable step within a reasoning run."""

    code: str
    detail: str
    inputs: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    outputs: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(self, "inputs", MappingProxyType(dict(self.inputs or {})))
        object.__setattr__(self, "outputs", MappingProxyType(dict(self.outputs or {})))


@dataclass(frozen=True)
class ReasoningRecord:
    """Append-only record of one StudentReasoningService run."""

    reasoning_id: str
    twin_id: str
    triggered_by: str
    observation_ids: tuple[str, ...]
    steps: tuple[ReasoningStep, ...]
    summary: str
    created_at: datetime
    reasoning_version: str = REASONING_VERSION

    def __post_init__(self) -> None:
        if not (self.reasoning_id or "").strip():
            raise ValueError("reasoning_id is required")
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "observation_ids", tuple(self.observation_ids or ()))
        object.__setattr__(self, "steps", tuple(self.steps or ()))
