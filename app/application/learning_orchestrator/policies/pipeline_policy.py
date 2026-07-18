"""Stateless pipeline execution rules — isolation and continuation.

Controls whether later stages run after an earlier failure.
Never recovers educational state.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


@dataclass(frozen=True)
class PipelinePolicy:
    """Rules for stage isolation and continuation after failure.

    Attributes:
        continue_on_failure: When True, subsequent stages still run
            (isolation mode). When False, remaining stages are skipped.
        fail_fast_stages: Stages whose failure always stops the pipeline
            regardless of ``continue_on_failure``.
        require_prior_success: When True, a stage requires all prior
            non-skipped stages to have succeeded.
    """

    continue_on_failure: bool = True
    fail_fast_stages: frozenset[PipelineStageName] = frozenset()
    require_prior_success: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "fail_fast_stages", frozenset(self.fail_fast_stages)
        )

    @classmethod
    def isolated(cls) -> PipelinePolicy:
        """Default production policy — failures are isolated; pipeline continues."""
        return cls(continue_on_failure=True, require_prior_success=False)

    @classmethod
    def fail_fast(cls) -> PipelinePolicy:
        """Stop the pipeline after any stage failure."""
        return cls(continue_on_failure=False, require_prior_success=False)

    @classmethod
    def sequential(cls) -> PipelinePolicy:
        """Require prior success; stop on first failure."""
        return cls(continue_on_failure=False, require_prior_success=True)

    def should_continue_after(self, result: PipelineResult) -> bool:
        """True when later stages may run after ``result``."""
        if not result.failed:
            return True
        if result.stage in self.fail_fast_stages:
            return False
        return self.continue_on_failure

    def may_run_stage(
        self,
        stage: PipelineStageName,
        *,
        prior_results: tuple[PipelineResult, ...],
    ) -> tuple[bool, str | None]:
        """Decide whether ``stage`` may execute given prior results.

        Returns:
            ``(allowed, skip_reason)`` — when not allowed, ``skip_reason``
            explains why the stage should be skipped.
        """
        del stage  # stage identity unused; policy is uniform
        if not prior_results:
            return True, None
        failures = [r for r in prior_results if r.failed]
        if not failures:
            return True, None
        last_failure = failures[-1]
        if not self.should_continue_after(last_failure):
            return False, (
                f"skipped after failure in {last_failure.stage.value}"
            )
        if self.require_prior_success:
            return False, (
                f"requires prior success; {last_failure.stage.value} failed"
            )
        return True, None
