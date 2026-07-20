"""Wrap EducationalPipeline with operational timing and success/failure metrics.

Architecture Source
    APP-004 Production Readiness & Version 2 Release

Does not alter educational stage order or decisions.
"""

from __future__ import annotations

from typing import Protocol

from application.pipeline.pipeline_request import PipelineRequest
from application.pipeline.pipeline_result import PipelineResult
from infrastructure.observability.logging import StructuredLogger
from infrastructure.observability.metrics import PipelineMetrics
from infrastructure.observability.timing import timed


class _PipelineLike(Protocol):
    def run(self, request: PipelineRequest) -> PipelineResult: ...


class ObservedEducationalPipeline:
    """Decorator around EducationalPipeline for operational observability."""

    def __init__(
        self,
        pipeline: _PipelineLike,
        *,
        metrics: PipelineMetrics | None = None,
        logger: StructuredLogger | None = None,
    ) -> None:
        self._pipeline = pipeline
        self._metrics = metrics or PipelineMetrics()
        self._logger = logger or StructuredLogger("kwalitec.eos.pipeline")

    @property
    def metrics(self) -> PipelineMetrics:
        return self._metrics

    @property
    def inner(self) -> _PipelineLike:
        return self._pipeline

    def run(self, request: PipelineRequest) -> PipelineResult:
        self._metrics.incr("pipeline_started")
        student_id = getattr(request, "student_id", "")
        self._logger.info(
            "pipeline_started",
            student_id=student_id,
            event="pipeline_started",
        )
        try:
            with timed("pipeline_execution", None) as slot:
                result = self._pipeline.run(request)
            duration_ms = slot[0]
            self._metrics.record_timing("pipeline_execution", duration_ms)
            self._metrics.incr("pipeline_succeeded")
            stages = getattr(result, "stages_completed", ())
            self._logger.info(
                "pipeline_succeeded",
                student_id=student_id,
                event="pipeline_succeeded",
                duration_ms=round(duration_ms, 3),
                stages_completed=len(stages),
            )
            return result
        except Exception as exc:
            self._metrics.incr("pipeline_failed")
            self._logger.error(
                "pipeline_failed",
                student_id=student_id,
                event="pipeline_failed",
                error_type=type(exc).__name__,
            )
            raise
