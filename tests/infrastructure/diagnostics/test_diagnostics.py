"""Observability diagnostics tests."""

from __future__ import annotations

import pytest

from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.diagnostics.pipeline_metrics import PipelineMetrics
from app.infrastructure.diagnostics.tracing import ExecutionTracer
from tests.infrastructure.helpers import LEARNERS, SUBJECTS


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_correlation_context_bind(learner_id):
    with CorrelationContext.bind(
        correlation_id=f"corr-{learner_id}", causation_id="cause"
    ) as ids:
        assert ids.correlation_id == f"corr-{learner_id}"
        assert CorrelationContext.get_correlation_id() == f"corr-{learner_id}"
        assert CorrelationContext.get_causation_id() == "cause"
    assert CorrelationContext.get_correlation_id() == ""


@pytest.mark.parametrize("adapter_id", SUBJECTS)
def test_adapter_diagnostics(adapter_id):
    diag = AdapterDiagnostics()
    diag.record_health(adapter_id, available=True, version="1.0.0")
    diag.record_call(adapter_id)
    diag.record_call(adapter_id, error=True)
    health = diag.health(adapter_id)
    assert health is not None
    assert health.available is True
    metrics = diag.metrics()
    assert metrics["call_counts"][adapter_id] == 2
    assert metrics["error_counts"][adapter_id] == 1


@pytest.mark.parametrize("name", sorted(PipelineMetrics.ALLOWED_COUNTERS))
def test_pipeline_metrics_allowed(name):
    metrics = PipelineMetrics()
    metrics.incr(name, stage="x")
    assert metrics.get(name) == 1


@pytest.mark.parametrize(
    "bad",
    ["mastery", "readiness", "roi", "educational_benefit", "topic_complete"],
)
def test_pipeline_metrics_refuse_educational(bad):
    metrics = PipelineMetrics()
    with pytest.raises(ValueError, match="refused"):
        metrics.incr(bad)


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_tracer_spans(learner_id):
    tracer = ExecutionTracer()
    with CorrelationContext.bind(correlation_id=f"c-{learner_id}"):
        span_id = tracer.start("stage", learner_id=learner_id)
        span = tracer.end(span_id, status="ok")
    assert span.correlation_id == f"c-{learner_id}"
    assert span.duration_ms is not None
    assert tracer.diagnostics()["completed_spans"] == 1


@pytest.mark.parametrize("level", ["info", "warning", "error", "debug"])
def test_structured_logger_includes_correlation(level):
    logger = StructuredLogger("test.infra")
    with CorrelationContext.bind(correlation_id="corr-z", causation_id="cause-z"):
        record = getattr(logger, level)("hello", adapter="x")
    assert record["correlation_id"] == "corr-z"
    assert record["causation_id"] == "cause-z"
    assert record["message"] == "hello"
