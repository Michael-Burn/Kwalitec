"""Tests for Educational Intelligence Platform production orchestration (PR-001)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.educational_intelligence_pipeline import (
    EducationalPipelineOrchestrator,
    PipelineEventType,
    PipelineStage,
)
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from tests.application.reasoning.conftest import make_bundle, make_item
from tests.certification.educational_intelligence.fingerprints import build_fingerprints
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)

FIXED_AT = datetime(2026, 7, 28, 14, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def _cold_twin() -> StudentDigitalTwin:
    return StudentDigitalTwin.create(
        twin_id="twin-pr001",
        student=Student(student_id="student-pr001", display_name="PR001 Learner"),
        created_at=FIXED_AT,
    )


def _bundle():
    return make_bundle(
        bundle_id="bundle-pr001",
        session_id="sess-pr001",
        items=(
            make_item(
                item_id="item-1",
                observation_id="obs-1",
                question_id="q-1",
                correctness="correct",
                confidence=4,
            ),
            make_item(
                item_id="item-2",
                observation_id="obs-2",
                question_id="q-2",
                correctness="incorrect",
                confidence=2,
                hints_used=1,
            ),
        ),
    )


class TestPipelineOrchestration:
    def test_execute_runs_all_stages_in_order(self) -> None:
        orch = EducationalPipelineOrchestrator()
        result = orch.execute(
            _cold_twin(),
            _bundle(),
            correlation_id="corr-pr001",
            reasoning_request_id="rrq-pr001",
            pipeline_id="eip-pr001",
            at=FIXED_AT,
            persist=False,
        )
        assert result.succeeded
        assert result.outcome == "completed"
        assert result.interpretation is not None
        assert result.decision_set is not None
        assert result.twin is not None
        assert result.projection is not None
        assert result.mission is not None
        assert result.explanation is not None

        stage_events = [
            e.stage
            for e in result.events
            if e.event_type == PipelineEventType.PIPELINE_STAGE_COMPLETED
        ]
        assert stage_events == list(PipelineStage.ordered())

    def test_pipeline_started_and_completed_events(self) -> None:
        orch = EducationalPipelineOrchestrator()
        result = orch.execute(
            _cold_twin(),
            _bundle(),
            correlation_id="corr-events",
            reasoning_request_id="rrq-events",
            pipeline_id="eip-events",
            at=FIXED_AT,
            persist=False,
        )
        types = [e.event_type for e in result.events]
        assert types[0] == PipelineEventType.PIPELINE_STARTED
        assert types[-1] == PipelineEventType.PIPELINE_COMPLETED
        assert PipelineEventType.PIPELINE_STAGE_STARTED in types
        assert PipelineEventType.PIPELINE_STAGE_COMPLETED in types

    def test_failure_emits_pipeline_failed(self) -> None:
        class BoomInterpreter:
            def interpret_bundle(self, *args, **kwargs):
                raise RuntimeError("interpret boom")

        orch = EducationalPipelineOrchestrator(interpreter=BoomInterpreter())  # type: ignore[arg-type]
        result = orch.execute(
            _cold_twin(),
            _bundle(),
            correlation_id="corr-fail",
            reasoning_request_id="rrq-fail",
            pipeline_id="eip-fail",
            at=FIXED_AT,
            persist=False,
        )
        assert result.outcome == "failed"
        assert result.failed_stage == PipelineStage.INTERPRETATION
        assert result.failure_cause is not None
        assert "RuntimeError" in result.failure_cause
        assert any(
            e.event_type == PipelineEventType.PIPELINE_FAILED for e in result.events
        )
        assert any(
            e.event_type == PipelineEventType.PIPELINE_STAGE_FAILED
            for e in result.events
        )


class TestPerformanceCollection:
    def test_metrics_recorded_for_all_stages(self) -> None:
        orch = EducationalPipelineOrchestrator()
        result = orch.execute(
            _cold_twin(),
            _bundle(),
            correlation_id="corr-metrics",
            reasoning_request_id="rrq-metrics",
            pipeline_id="eip-metrics",
            at=FIXED_AT,
            persist=False,
        )
        m = result.metrics
        assert m.total_ms > 0
        assert m.interpretation_ms >= 0
        assert m.decision_ms >= 0
        assert m.twin_update_ms >= 0
        assert m.graph_projection_ms >= 0
        assert m.mission_planning_ms >= 0
        assert m.tutor_explanation_ms >= 0
        assert len(m.stage_timings) == 6
        payload = m.to_dict()
        assert "total_ms" in payload
        assert len(payload["stages"]) == 6


class TestRegressionParity:
    def test_orchestrator_matches_certification_harness_fingerprints(self) -> None:
        twin = _cold_twin()
        bundle = _bundle()
        corr = "corr-parity"
        rrq = "rrq-parity"

        harness = EducationalIntelligencePipelineHarness()
        certified = harness.run(
            twin,
            bundle,
            correlation_id=corr,
            reasoning_request_id=rrq,
            at=FIXED_AT,
            graph_id="lg-parity",
            persist=False,
        )

        orch = EducationalPipelineOrchestrator()
        production = orch.execute(
            twin,
            bundle,
            correlation_id=corr,
            reasoning_request_id=rrq,
            pipeline_id="eip-parity",
            at=FIXED_AT,
            graph_id="lg-parity",
            persist=False,
        )
        assert production.succeeded
        assert certified.certified

        cert_fp = certified.fingerprints
        prod_fp = build_fingerprints(
            observation_set=production.observation_set,
            decision_set=production.decision_set,
            twin=production.twin,
            projection=production.projection,
            mission=production.mission,
            explanation=production.explanation,
        )
        assert prod_fp == cert_fp
