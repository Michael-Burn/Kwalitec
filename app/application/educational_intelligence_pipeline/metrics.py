"""Performance metrics for the Educational Intelligence pipeline.

Records timings only. Does not optimise or alter educational behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.educational_intelligence_pipeline.stages import PipelineStage


@dataclass(frozen=True, slots=True)
class StageTiming:
    """Wall-clock timing for a single pipeline stage."""

    stage: PipelineStage
    duration_ms: float
    succeeded: bool


@dataclass(slots=True)
class PipelineMetrics:
    """Accumulated stage timings for one pipeline execution."""

    interpretation_ms: float = 0.0
    decision_ms: float = 0.0
    twin_update_ms: float = 0.0
    graph_projection_ms: float = 0.0
    mission_planning_ms: float = 0.0
    tutor_explanation_ms: float = 0.0
    total_ms: float = 0.0
    stage_timings: list[StageTiming] = field(default_factory=list)

    def record_stage(
        self,
        stage: PipelineStage,
        duration_ms: float,
        *,
        succeeded: bool = True,
    ) -> None:
        """Record a stage timing without mutating educational outputs."""
        self.stage_timings.append(
            StageTiming(stage=stage, duration_ms=duration_ms, succeeded=succeeded)
        )
        attr = _STAGE_ATTR.get(stage)
        if attr is not None:
            setattr(self, attr, duration_ms)

    def to_dict(self) -> dict[str, float | list[dict[str, object]]]:
        """Serialise metrics for operational logs (timings only)."""
        return {
            "interpretation_ms": round(self.interpretation_ms, 3),
            "decision_ms": round(self.decision_ms, 3),
            "twin_update_ms": round(self.twin_update_ms, 3),
            "graph_projection_ms": round(self.graph_projection_ms, 3),
            "mission_planning_ms": round(self.mission_planning_ms, 3),
            "tutor_explanation_ms": round(self.tutor_explanation_ms, 3),
            "total_ms": round(self.total_ms, 3),
            "stages": [
                {
                    "stage": t.stage.value,
                    "duration_ms": round(t.duration_ms, 3),
                    "succeeded": t.succeeded,
                }
                for t in self.stage_timings
            ],
        }


_STAGE_ATTR: dict[PipelineStage, str] = {
    PipelineStage.INTERPRETATION: "interpretation_ms",
    PipelineStage.DECISION: "decision_ms",
    PipelineStage.TWIN_UPDATE: "twin_update_ms",
    PipelineStage.GRAPH_PROJECTION: "graph_projection_ms",
    PipelineStage.MISSION_PLANNING: "mission_planning_ms",
    PipelineStage.TUTOR_EXPLANATION: "tutor_explanation_ms",
}


class MetricsCollector:
    """Thin collector used by the orchestrator during a single run."""

    def __init__(self) -> None:
        self.metrics = PipelineMetrics()

    def record(
        self,
        stage: PipelineStage,
        duration_ms: float,
        *,
        succeeded: bool = True,
    ) -> None:
        self.metrics.record_stage(stage, duration_ms, succeeded=succeeded)

    def set_total(self, total_ms: float) -> None:
        self.metrics.total_ms = total_ms
