"""Analytics Engine orchestrator (MS-006 E4).

Deterministic AnalyticsSummary construction:
aggregate → assign summary_id → optional AnalyticsExport → telemetry.

Consumes immutable PolicyEvaluation, ExperimentObservation, and EvidenceRecord
inputs only. Never mutates inputs, never promotes policies, never persists,
never changes educational behaviour.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from app.infrastructure.adapters.evidence_platform.aggregator import (
    AnalyticsAggregator,
    AnalyticsValidationError,
    build_analytics_aggregator,
)
from app.infrastructure.adapters.evidence_platform.analytics_telemetry import (
    emit_completed,
    emit_failed,
    emit_latency,
    emit_requested,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    ANALYTICS_AUDIENCE_GOVERNANCE,
    AnalyticsExport,
    AnalyticsSummary,
    EvidenceRecord,
    ExperimentObservation,
    PolicyEvaluation,
    serialize_canonical,
)
from app.infrastructure.events.registry import EventRegistry


class AnalyticsEngine:
    """Create immutable AnalyticsSummary artefacts (E4).

    Identical PolicyEvaluation / ExperimentObservation / EvidenceRecord
    inputs → identical AnalyticsSummary every execution.
    """

    ENGINE_ID = "analytics_engine"
    ENGINE_VERSION = "1.0.0-e4"

    def __init__(
        self,
        *,
        aggregator: AnalyticsAggregator | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._aggregator = aggregator or AnalyticsAggregator(enabled=True)
        self._events = events
        self._enabled = bool(enabled)

    @property
    def engine_id(self) -> str:
        return self.ENGINE_ID

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    @property
    def aggregator(self) -> AnalyticsAggregator:
        return self._aggregator

    def is_enabled(self) -> bool:
        return self._enabled

    def aggregate(
        self,
        *,
        evaluations: Sequence[PolicyEvaluation] = (),
        observations: Sequence[ExperimentObservation] = (),
        evidence_records: Sequence[EvidenceRecord] = (),
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
        period: Mapping[str, Any] | None = None,
    ) -> AnalyticsSummary:
        """Aggregate observational inputs into an immutable AnalyticsSummary.

        Inputs are never mutated. No policy promotion.
        """
        self._ensure_enabled()
        started = time.perf_counter()
        evals = tuple(evaluations or ())
        obs = tuple(observations or ())
        records = tuple(evidence_records or ())
        if self._events is not None:
            emit_requested(
                self._events,
                audience=audience,
                evaluation_count=len(evals),
                observation_count=len(obs),
                evidence_count=len(records),
            )
        try:
            eval_snapshots = tuple(item.serialize() for item in evals)
            obs_snapshots = tuple(item.serialize() for item in obs)
            record_snapshots = tuple(item.serialize() for item in records)

            draft = self._aggregator.aggregate(
                evaluations=evals,
                observations=obs,
                evidence_records=records,
                audience=audience,
                as_of=as_of,
                period=period,
            )
            summary_id = deterministic_summary_id(draft)
            summary = replace(draft, summary_id=summary_id)

            for original, current in zip(eval_snapshots, evals, strict=True):
                if current.serialize() != original:
                    raise AnalyticsValidationError(
                        "PolicyEvaluation mutated during analytics aggregation"
                    )
            for original, current in zip(obs_snapshots, obs, strict=True):
                if current.serialize() != original:
                    raise AnalyticsValidationError(
                        "ExperimentObservation mutated during analytics aggregation"
                    )
            for original, current in zip(record_snapshots, records, strict=True):
                if current.serialize() != original:
                    raise AnalyticsValidationError(
                        "EvidenceRecord mutated during analytics aggregation"
                    )

            if self._events is not None:
                emit_completed(
                    self._events,
                    summary_id=summary.summary_id,
                    audience=summary.audience,
                    evaluation_count=summary.evaluation_count,
                    observation_count=summary.observation_count,
                    evidence_count=summary.evidence_count,
                    metric_count=len(summary.metric_series),
                    contents_ref=summary.contents_ref,
                )
                emit_latency(
                    self._events,
                    audience=summary.audience,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=True,
                )
            return summary
        except Exception as exc:
            if self._events is not None:
                emit_failed(
                    self._events,
                    audience=audience,
                    error_code=type(exc).__name__,
                    message=str(exc),
                )
                emit_latency(
                    self._events,
                    audience=audience,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=False,
                )
            raise

    def export(
        self,
        summary: AnalyticsSummary,
        *,
        audience: str | None = None,
        redaction_level: str = "standard",
        created_at: str | None = None,
    ) -> AnalyticsExport:
        """Build an immutable AnalyticsExport from an AnalyticsSummary.

        Forbidden audience: student_coaching. No educational behaviour change.
        """
        self._ensure_enabled()
        if not isinstance(summary, AnalyticsSummary):
            raise AnalyticsValidationError("summary must be an AnalyticsSummary")
        resolved_audience = (audience or summary.audience or "").strip().lower()
        if resolved_audience == "student_coaching":
            raise AnalyticsValidationError(
                "student_coaching is a forbidden analytics audience"
            )
        export_id = deterministic_export_id(summary, resolved_audience)
        return AnalyticsExport(
            export_id=export_id,
            export_version=summary.summary_version,
            audience=resolved_audience or ANALYTICS_AUDIENCE_GOVERNANCE,
            contents_ref=summary.contents_ref or summary.summary_id,
            redaction_level=redaction_level,
            metric_ids=tuple(series.metric_id for series in summary.metric_series),
            created_at=created_at if created_at is not None else summary.as_of,
            limitations=summary.limitations,
        )

    def _ensure_enabled(self) -> None:
        if not self._enabled:
            raise AnalyticsValidationError(
                "AnalyticsEngine is disabled (feature flag OFF)"
            )


def deterministic_summary_id(summary: AnalyticsSummary) -> str:
    """Derive summary_id from material fields (excludes summary_id)."""
    material = summary.to_canonical_dict()
    material["summary_id"] = ""
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"asum-{digest[:24]}"


def deterministic_export_id(summary: AnalyticsSummary, audience: str) -> str:
    """Derive export_id from summary contents_ref + audience."""
    material = {
        "audience": audience,
        "contents_ref": summary.contents_ref,
        "summary_id": summary.summary_id,
        "summary_version": summary.summary_version,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"aexp-{digest[:24]}"


def build_analytics_engine(
    *,
    enabled: bool,
    aggregator: AnalyticsAggregator | None = None,
    events: EventRegistry | None = None,
) -> AnalyticsEngine | None:
    """DI helper — construct AnalyticsEngine only when the flag is on."""
    if not enabled:
        return None
    wired_aggregator = aggregator or build_analytics_aggregator(enabled=True)
    if wired_aggregator is None:
        return None
    return AnalyticsEngine(
        aggregator=wired_aggregator,
        events=events,
        enabled=True,
    )
