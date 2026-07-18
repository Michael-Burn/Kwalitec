"""Immutable result of a single pipeline stage execution."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.domain.learning_orchestrator.pipeline_stage import (
    PipelineStageName,
    StageOutcome,
)


@dataclass(frozen=True)
class PipelineResult:
    """Isolated stage outcome — success, failure, warnings, diagnostics.

    Failures here are isolated: the orchestrator reports them and never
    recovers educational state.
    """

    stage: PipelineStageName
    outcome: StageOutcome
    duration_ms: float = 0.0
    warnings: tuple[str, ...] = ()
    diagnostics: MappingProxyType | None = None
    error: str | None = None
    payload: MappingProxyType | None = None
    attempt_count: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(self, "warnings", tuple(self.warnings))
        if self.diagnostics is None:
            object.__setattr__(self, "diagnostics", MappingProxyType({}))
        elif not isinstance(self.diagnostics, MappingProxyType):
            object.__setattr__(
                self,
                "diagnostics",
                MappingProxyType(dict(self.diagnostics)),
            )
        if self.payload is None:
            object.__setattr__(self, "payload", MappingProxyType({}))
        elif not isinstance(self.payload, MappingProxyType):
            object.__setattr__(
                self, "payload", MappingProxyType(dict(self.payload))
            )

    @property
    def succeeded(self) -> bool:
        """True when the stage completed successfully (warnings allowed)."""
        return self.outcome in {StageOutcome.SUCCESS, StageOutcome.WARNING}

    @property
    def failed(self) -> bool:
        """True when the stage reported failure."""
        return self.outcome == StageOutcome.FAILURE

    @property
    def skipped(self) -> bool:
        """True when the stage was skipped."""
        return self.outcome == StageOutcome.SKIPPED

    @classmethod
    def success(
        cls,
        stage: PipelineStageName,
        *,
        duration_ms: float = 0.0,
        warnings: tuple[str, ...] = (),
        diagnostics: dict | MappingProxyType | None = None,
        payload: dict | MappingProxyType | None = None,
        attempt_count: int = 1,
    ) -> PipelineResult:
        """Factory for a successful stage result."""
        outcome = (
            StageOutcome.WARNING if warnings else StageOutcome.SUCCESS
        )
        return cls(
            stage=stage,
            outcome=outcome,
            duration_ms=duration_ms,
            warnings=warnings,
            diagnostics=diagnostics,  # type: ignore[arg-type]
            payload=payload,  # type: ignore[arg-type]
            attempt_count=attempt_count,
        )

    @classmethod
    def failure(
        cls,
        stage: PipelineStageName,
        *,
        error: str,
        duration_ms: float = 0.0,
        warnings: tuple[str, ...] = (),
        diagnostics: dict | MappingProxyType | None = None,
        payload: dict | MappingProxyType | None = None,
        attempt_count: int = 1,
    ) -> PipelineResult:
        """Factory for a failed stage result."""
        return cls(
            stage=stage,
            outcome=StageOutcome.FAILURE,
            duration_ms=duration_ms,
            warnings=warnings,
            diagnostics=diagnostics,  # type: ignore[arg-type]
            error=error,
            payload=payload,  # type: ignore[arg-type]
            attempt_count=attempt_count,
        )

    @classmethod
    def skip(
        cls,
        stage: PipelineStageName,
        *,
        reason: str,
        duration_ms: float = 0.0,
    ) -> PipelineResult:
        """Factory for a skipped stage result."""
        return cls(
            stage=stage,
            outcome=StageOutcome.SKIPPED,
            duration_ms=duration_ms,
            warnings=(reason,),
            diagnostics=MappingProxyType({"skip_reason": reason}),
        )
