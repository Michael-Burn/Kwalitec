"""Immutable WorkflowResult — outcome of one workflow execution step chain."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class WorkflowResult:
    """Structural result of executing a named platform workflow.

    Carries port-step traces and timings for diagnostics. Contains no
    educational conclusions — only orchestration outcomes.
    """

    workflow: str
    success: bool
    steps: tuple[str, ...] = ()
    duration_ms: float = 0.0
    step_timings_ms: MappingProxyType | None = None
    error: str | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))
        if self.step_timings_ms is None:
            object.__setattr__(self, "step_timings_ms", MappingProxyType({}))
        elif not isinstance(self.step_timings_ms, MappingProxyType):
            object.__setattr__(
                self,
                "step_timings_ms",
                MappingProxyType(dict(self.step_timings_ms)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
