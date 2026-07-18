"""Immutable PipelineSnapshot — DTO projection of a stage result."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.domain.learning_orchestrator.pipeline_result import PipelineResult


@dataclass(frozen=True)
class PipelineSnapshot:
    """Read-only projection of one pipeline stage outcome."""

    stage: str
    outcome: str
    duration_ms: float = 0.0
    warnings: tuple[str, ...] = ()
    error: str | None = None
    attempt_count: int = 1
    diagnostics: MappingProxyType | None = None
    payload_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "payload_keys", tuple(self.payload_keys))
        if self.diagnostics is None:
            object.__setattr__(self, "diagnostics", MappingProxyType({}))
        elif not isinstance(self.diagnostics, MappingProxyType):
            object.__setattr__(
                self,
                "diagnostics",
                MappingProxyType(dict(self.diagnostics)),
            )

    @classmethod
    def from_result(cls, result: PipelineResult) -> PipelineSnapshot:
        """Project a domain ``PipelineResult`` into a DTO snapshot."""
        payload = result.payload or MappingProxyType({})
        return cls(
            stage=result.stage.value,
            outcome=result.outcome.value,
            duration_ms=result.duration_ms,
            warnings=result.warnings,
            error=result.error,
            attempt_count=result.attempt_count,
            diagnostics=result.diagnostics,
            payload_keys=tuple(sorted(payload.keys())),
        )

    @property
    def succeeded(self) -> bool:
        """True when outcome is success or warning."""
        return self.outcome in {"success", "warning"}

    @property
    def failed(self) -> bool:
        """True when outcome is failure."""
        return self.outcome == "failure"

    @property
    def skipped(self) -> bool:
        """True when outcome is skipped."""
        return self.outcome == "skipped"
