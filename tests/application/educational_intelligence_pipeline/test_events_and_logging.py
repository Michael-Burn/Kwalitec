"""Operational events and observability tests (PR-001)."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from app.application.educational_intelligence_pipeline.events import (
    PipelineEvent,
    PipelineEventCollector,
    PipelineEventType,
)
from app.application.educational_intelligence_pipeline.metrics import PipelineMetrics
from app.application.educational_intelligence_pipeline.observability import (
    FORBIDDEN_LOG_KEYS,
    log_pipeline_event,
    log_pipeline_summary,
    sanitize_log_fields,
)
from app.application.educational_intelligence_pipeline.stages import PipelineStage

FIXED_AT = datetime(2026, 7, 28, 14, 0, 0, tzinfo=UTC).replace(tzinfo=None)


class TestOperationalEvents:
    def test_collector_emits_catalogue(self) -> None:
        c = PipelineEventCollector()
        c.started(
            pipeline_id="p1",
            correlation_id="c1",
            student_id="s1",
            assessment_session_id="a1",
            reasoning_request_id="r1",
            occurred_at=FIXED_AT,
        )
        c.stage_started(
            pipeline_id="p1",
            correlation_id="c1",
            stage=PipelineStage.INTERPRETATION,
            occurred_at=FIXED_AT,
        )
        c.stage_completed(
            pipeline_id="p1",
            correlation_id="c1",
            stage=PipelineStage.INTERPRETATION,
            duration_ms=1.5,
            occurred_at=FIXED_AT,
        )
        c.completed(
            pipeline_id="p1",
            correlation_id="c1",
            student_id="s1",
            assessment_session_id="a1",
            reasoning_request_id="r1",
            duration_ms=10.0,
            occurred_at=FIXED_AT,
        )
        assert [e.event_type for e in c.events] == [
            PipelineEventType.PIPELINE_STARTED,
            PipelineEventType.PIPELINE_STAGE_STARTED,
            PipelineEventType.PIPELINE_STAGE_COMPLETED,
            PipelineEventType.PIPELINE_COMPLETED,
        ]

    def test_event_log_fields_exclude_educational_payloads(self) -> None:
        event = PipelineEvent(
            event_type=PipelineEventType.PIPELINE_STARTED,
            pipeline_id="p1",
            correlation_id="c1",
            occurred_at=FIXED_AT,
            student_id="s1",
            assessment_session_id="sess",
            reasoning_request_id="rrq",
        )
        fields = event.to_log_fields()
        assert "pipeline_id" in fields
        assert "correlation_id" in fields
        for key in FORBIDDEN_LOG_KEYS:
            assert key not in fields


class TestLoggingPrivacy:
    def test_sanitize_strips_forbidden_keys(self) -> None:
        dirty = {
            "pipeline_id": "p1",
            "mastery": 0.9,
            "explanation_text": "secret educational prose",
            "outcome": "completed",
        }
        clean = sanitize_log_fields(dirty)
        assert clean == {"pipeline_id": "p1", "outcome": "completed"}
        assert "mastery" not in clean
        assert "explanation_text" not in clean

    def test_log_pipeline_event_emits_json(self, caplog) -> None:
        event = PipelineEvent(
            event_type=PipelineEventType.PIPELINE_COMPLETED,
            pipeline_id="p1",
            correlation_id="c1",
            occurred_at=FIXED_AT,
            outcome="completed",
            duration_ms=12.5,
        )
        with caplog.at_level(
            logging.INFO,
            logger="kwalitec.educational_intelligence_pipeline",
        ):
            log_pipeline_event(event)
        assert any("pipeline_event" in r.message for r in caplog.records)
        assert any("PipelineCompleted" in r.message for r in caplog.records)

    def test_log_pipeline_summary_includes_timings(self, caplog) -> None:
        metrics = PipelineMetrics(total_ms=42.0, interpretation_ms=5.0)
        with caplog.at_level(
            logging.INFO,
            logger="kwalitec.educational_intelligence_pipeline",
        ):
            log_pipeline_summary(
                pipeline_id="p1",
                correlation_id="c1",
                student_id="s1",
                assessment_session_id="a1",
                reasoning_request_id="r1",
                outcome="completed",
                metrics=metrics,
            )
        assert any("pipeline_summary" in r.message for r in caplog.records)
        assert any("execution_time_ms" in r.message for r in caplog.records)
