"""Founder Validation product metrics (FV-001).

Assembles baseline dogfood metrics from:
- LP-001 ``llp_lifecycle_operations`` persistence
- RI-002 adoption / RIS telemetry
- Mission completion rows
- Process-scoped FV telemetry (hook outcomes + decision refresh latency)

Observational only — does not reason, recommend, or mutate educational state.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func

from app.application.founder_validation.dto import (
    FounderValidationMetricsReport,
    LatencyMetric,
    RateMetric,
)
from app.application.founder_validation.telemetry import (
    DEFAULT_FV_TELEMETRY,
    FounderValidationTelemetry,
)
from app.application.learner_lifecycle.stages import OperationStatus, OperationType
from app.application.runtime_integration.adoption_metrics import AdoptionMetricsService
from app.application.runtime_integration.telemetry import (
    DEFAULT_TELEMETRY,
    RuntimeIntegrationTelemetry,
)
from app.extensions import db
from app.models.learner_lifecycle import LlpLifecycleOperation
from app.models.mission import Mission


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _percentile(sorted_values: list[float], pct: float) -> float | None:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (len(sorted_values) - 1) * pct
    low = int(rank)
    high = min(low + 1, len(sorted_values) - 1)
    weight = rank - low
    return sorted_values[low] * (1.0 - weight) + sorted_values[high] * weight


def _rate_from_counts(
    *,
    metric_id: str,
    label: str,
    numerator: int,
    denominator: int,
    definition: str,
) -> RateMetric:
    return RateMetric(
        metric_id=metric_id,
        label=label,
        numerator=max(0, numerator),
        denominator=max(0, denominator),
        definition=definition,
    )


class FounderValidationMetricsService:
    """Compute FV-001 baseline product metrics for operators and journals."""

    def __init__(
        self,
        *,
        adoption: AdoptionMetricsService | None = None,
        ris_telemetry: RuntimeIntegrationTelemetry | None = None,
        fv_telemetry: FounderValidationTelemetry | None = None,
    ) -> None:
        self._ris = ris_telemetry or DEFAULT_TELEMETRY
        self._fv = fv_telemetry or DEFAULT_FV_TELEMETRY
        self._adoption = adoption or AdoptionMetricsService(telemetry=self._ris)

    def build_report(self) -> FounderValidationMetricsReport:
        """Assemble the FV-001 product metrics snapshot."""
        adoption = self._adoption.build_report()
        fv_snap = self._fv.snapshot()
        onboard = self._lifecycle_rate(
            OperationType.ONBOARD.value,
            metric_id="onboarding_completion",
            label="Onboarding completion",
            definition=(
                "Completed LP-001 onboard operations / "
                "(completed + failed) onboard operations"
            ),
        )
        evidence = self._lifecycle_rate(
            OperationType.EVIDENCE_REFRESH.value,
            metric_id="evidence_recording_success",
            label="Evidence recording success",
            definition=(
                "Completed LP-001 evidence_refresh operations / "
                "(completed + failed) evidence_refresh operations"
            ),
        )
        # Prefer persisted LP rates; fall back to process FV telemetry when empty.
        if onboard.denominator == 0 and int(fv_snap["onboard_attempted"]) > 0:
            onboard = _rate_from_counts(
                metric_id="onboarding_completion",
                label="Onboarding completion",
                numerator=int(fv_snap["onboard_succeeded"]),
                denominator=int(fv_snap["onboard_attempted"]),
                definition=(
                    "Process-scoped FV onboard successes / attempts "
                    "(no persisted LLP rows yet)"
                ),
            )
        if evidence.denominator == 0 and int(fv_snap["evidence_attempted"]) > 0:
            evidence = _rate_from_counts(
                metric_id="evidence_recording_success",
                label="Evidence recording success",
                numerator=int(fv_snap["evidence_succeeded"]),
                denominator=int(fv_snap["evidence_attempted"]),
                definition=(
                    "Process-scoped FV evidence successes / attempts "
                    "(no persisted LLP rows yet)"
                ),
            )

        ris = adoption.telemetry
        ei_count = int(ris.educational_intelligence_count)
        fallback_count = int(ris.fallback_count)
        total_ris = int(ris.total_requests) or (ei_count + fallback_count)
        experience = _rate_from_counts(
            metric_id="experience_model_generation",
            label="Experience Model generation",
            numerator=ei_count,
            denominator=total_ris,
            definition="RIS EI-path requests / total RIS requests (RI-002)",
        )
        fallback = _rate_from_counts(
            metric_id="runtime_a_fallback",
            label="Runtime A fallback frequency",
            numerator=fallback_count,
            denominator=total_ris,
            definition="RIS Runtime A fallback requests / total RIS requests (RI-002)",
        )
        session = self._session_completion_rate()
        latency = self._decision_refresh_latency(fv_snap)
        lifecycle_failures = self._lifecycle_failure_rate()

        notes: list[str] = []
        if total_ris == 0:
            notes.append("No RIS telemetry samples in this process yet.")
        if onboard.denominator == 0:
            notes.append("No LP-001 onboard operations recorded yet.")
        if evidence.denominator == 0:
            notes.append("No LP-001 evidence_refresh operations recorded yet.")
        if session.denominator == 0:
            notes.append("No missions recorded yet for session completion.")

        return FounderValidationMetricsReport(
            onboarding_completion=onboard,
            sci_creation_success=adoption.sci_coverage,
            experience_model_generation=experience,
            runtime_a_fallback=fallback,
            session_completion=session,
            evidence_recording_success=evidence,
            decision_refresh_latency=latency,
            system_failures=int(fv_snap["system_failures"]),
            lifecycle_failures=lifecycle_failures,
            computed_at=_utc_now_iso(),
            notes=tuple(notes),
        )

    def build_operator_payload(self) -> dict[str, Any]:
        """Metrics report plus workflow catalogue for CLI / operator export."""
        from app.application.founder_validation.workflows import workflow_catalogue

        report = self.build_report()
        return {
            "programme": "FV-001",
            "metrics": report.to_dict(),
            "workflows": workflow_catalogue(),
            "fv_telemetry": self._fv.snapshot(),
        }

    @staticmethod
    def _lifecycle_rate(
        operation_type: str,
        *,
        metric_id: str,
        label: str,
        definition: str,
    ) -> RateMetric:
        completed = (
            db.session.query(func.count(LlpLifecycleOperation.id))
            .filter(
                LlpLifecycleOperation.operation_type == operation_type,
                LlpLifecycleOperation.status == OperationStatus.COMPLETED.value,
            )
            .scalar()
        )
        failed = (
            db.session.query(func.count(LlpLifecycleOperation.id))
            .filter(
                LlpLifecycleOperation.operation_type == operation_type,
                LlpLifecycleOperation.status == OperationStatus.FAILED.value,
            )
            .scalar()
        )
        completed_n = int(completed or 0)
        failed_n = int(failed or 0)
        return _rate_from_counts(
            metric_id=metric_id,
            label=label,
            numerator=completed_n,
            denominator=completed_n + failed_n,
            definition=definition,
        )

    @staticmethod
    def _lifecycle_failure_rate() -> RateMetric:
        failed = (
            db.session.query(func.count(LlpLifecycleOperation.id))
            .filter(LlpLifecycleOperation.status == OperationStatus.FAILED.value)
            .scalar()
        )
        total = db.session.query(func.count(LlpLifecycleOperation.id)).scalar()
        failed_n = int(failed or 0)
        total_n = int(total or 0)
        return _rate_from_counts(
            metric_id="lifecycle_failures",
            label="Lifecycle operation failures",
            numerator=failed_n,
            denominator=total_n,
            definition="Failed LP-001 operations / all LP-001 operations",
        )

    @staticmethod
    def _session_completion_rate() -> RateMetric:
        completed = (
            db.session.query(func.count(Mission.id))
            .filter(Mission.status == "Completed")
            .scalar()
        )
        total = db.session.query(func.count(Mission.id)).scalar()
        completed_n = int(completed or 0)
        total_n = int(total or 0)
        return _rate_from_counts(
            metric_id="session_completion",
            label="Session / mission completion",
            numerator=completed_n,
            denominator=total_n,
            definition="Missions with status Completed / all missions",
        )

    @staticmethod
    def _decision_refresh_latency(fv_snap: dict[str, Any]) -> LatencyMetric:
        samples = [
            float(v) for v in (fv_snap.get("decision_refresh_samples_ms") or [])
        ]
        samples.sort()
        mean = (sum(samples) / len(samples)) if samples else None
        return LatencyMetric(
            metric_id="decision_refresh_latency",
            label="Decision refresh latency",
            sample_count=len(samples),
            mean_ms=mean,
            p95_ms=_percentile(samples, 0.95),
            definition=(
                "Duration of LP-001 educational_decisions stage (ms) from "
                "FV process telemetry after evidence / onboard hooks"
            ),
        )
