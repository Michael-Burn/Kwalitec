"""Founder Validation instrumentation and workflows (FV-001).

Observational product metrics and Version 1 journey catalogue for founder
dogfooding. Does not introduce Educational Intelligence layers or bypass
Runtime Integration.
"""

from __future__ import annotations

from app.application.founder_validation.dto import (
    FounderValidationMetricsReport,
    LatencyMetric,
    RateMetric,
    WorkflowStep,
)
from app.application.founder_validation.metrics_service import (
    FounderValidationMetricsService,
)
from app.application.founder_validation.telemetry import (
    DEFAULT_FV_TELEMETRY,
    FounderValidationTelemetry,
    decision_refresh_ms_from_result,
    total_duration_ms_from_result,
)
from app.application.founder_validation.workflows import (
    VERSION_1_STUDENT_JOURNEY,
    workflow_catalogue,
    workflow_ids,
)

__all__ = [
    "DEFAULT_FV_TELEMETRY",
    "FounderValidationMetricsReport",
    "FounderValidationMetricsService",
    "FounderValidationTelemetry",
    "LatencyMetric",
    "RateMetric",
    "VERSION_1_STUDENT_JOURNEY",
    "WorkflowStep",
    "decision_refresh_ms_from_result",
    "total_duration_ms_from_result",
    "workflow_catalogue",
    "workflow_ids",
]
