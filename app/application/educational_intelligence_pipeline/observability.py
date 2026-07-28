"""Structured, privacy-safe pipeline logging.

Logs operational identifiers and timings only. Never logs observation
payloads, decision bodies, mastery scores, mission content, or tutor prose.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from app.application.educational_intelligence_pipeline.events import PipelineEvent
from app.application.educational_intelligence_pipeline.metrics import PipelineMetrics

logger = logging.getLogger("kwalitec.educational_intelligence_pipeline")

# Fields that must never appear in operational logs.
FORBIDDEN_LOG_KEYS = frozenset(
    {
        "observation",
        "observations",
        "decision",
        "decisions",
        "mastery",
        "confidence_score",
        "explanation_text",
        "mission_text",
        "tutor_text",
        "evidence_items",
        "payload",
        "belief",
        "answer",
        "response",
    }
)


def sanitize_log_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """Strip forbidden educational payload keys from a log field map."""
    return {k: v for k, v in fields.items() if k.lower() not in FORBIDDEN_LOG_KEYS}


def log_pipeline_event(event: PipelineEvent) -> None:
    """Emit a structured operational log line for a pipeline event."""
    fields = sanitize_log_fields(event.to_log_fields())
    logger.info(
        "pipeline_event %s",
        json.dumps(fields, default=str, separators=(",", ":")),
        extra={"pipeline_event": fields},
    )


def log_pipeline_summary(
    *,
    pipeline_id: str,
    correlation_id: str,
    student_id: str | None,
    assessment_session_id: str | None,
    reasoning_request_id: str | None,
    outcome: str,
    metrics: PipelineMetrics,
    failure_cause: str | None = None,
) -> None:
    """Emit an end-of-run operational summary (identifiers + timings only)."""
    fields = sanitize_log_fields(
        {
            "pipeline_id": pipeline_id,
            "correlation_id": correlation_id,
            "student_id": student_id,
            "assessment_session_id": assessment_session_id,
            "reasoning_request_id": reasoning_request_id,
            "outcome": outcome,
            "failure_cause": failure_cause,
            "execution_time_ms": round(metrics.total_ms, 3),
            "stage_timing": {
                "interpretation_ms": round(metrics.interpretation_ms, 3),
                "decision_ms": round(metrics.decision_ms, 3),
                "twin_update_ms": round(metrics.twin_update_ms, 3),
                "graph_projection_ms": round(metrics.graph_projection_ms, 3),
                "mission_planning_ms": round(metrics.mission_planning_ms, 3),
                "tutor_explanation_ms": round(metrics.tutor_explanation_ms, 3),
            },
        }
    )
    logger.info(
        "pipeline_summary %s",
        json.dumps(fields, default=str, separators=(",", ":")),
        extra={"pipeline_summary": fields},
    )
