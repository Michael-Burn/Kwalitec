"""Observation Diagnostics service — operational aggregation (P2-MS007).

Exposes publish counters, flag state, intake latency, publisher health,
JourneyTrace lifecycle, and an internal-only dashboard model.

Never carries student-identifying information or educational conclusions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from app.infrastructure.adapters.experience_observation.contracts import (
    PUBLISH_STATUS_FAILED,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_SKIPPED,
    ExperienceObservation,
    ObservationPublishResult,
)
from app.infrastructure.adapters.experience_observation.dashboard import (
    ExperienceDiagnosticsDashboard,
    FeatureFlagDiagnostics,
    ObservationCounters,
    PublisherHealthSummary,
)
from app.infrastructure.adapters.experience_observation.health import (
    HEALTH_STATUS_UNAVAILABLE,
    PipelineHealthChecker,
    PipelineHealthReport,
    build_pipeline_health_checker,
)
from app.infrastructure.adapters.experience_observation.journey_trace import (
    OBSERVATION_STATUS_FAILED,
    OBSERVATION_STATUS_PENDING,
    OBSERVATION_STATUS_PUBLISHED,
    OBSERVATION_STATUS_SKIPPED,
    PIPELINE_STAGE_ASSEMBLED,
    PIPELINE_STAGE_EVIDENCE_ACK,
    PIPELINE_STAGE_FAILED,
    PIPELINE_STAGE_JOURNEY_EVENT,
    PIPELINE_STAGE_PUBLISH_ATTEMPTED,
    PIPELINE_STAGE_SKIPPED,
    JourneyTrace,
    JourneyTraceStore,
    build_journey_trace,
    build_journey_trace_store,
)
from app.infrastructure.adapters.experience_observation.telemetry import (
    ExperienceDiagnosticsLogger,
    build_experience_diagnostics_logger,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry


def _mean(sum_value: float, count: int) -> float:
    if count <= 0:
        return 0.0
    return round(float(sum_value) / float(count), 3)


@dataclass
class ObservationDiagnosticsService:
    """Mutable in-process diagnostics aggregator for the observation pipeline.

    Thread-safe counters + JourneyTrace store. Observational only.
    """

    enabled: bool = True
    observation_flag: bool = False
    evidence_flag: bool = False
    unified_journey_flag: bool = False
    publisher: Any | None = None
    evidence: Any | None = None
    trace_store: JourneyTraceStore = field(default_factory=build_journey_trace_store)
    logger: ExperienceDiagnosticsLogger | None = None
    events: EventRegistry | None = None
    _lock: Lock = field(default_factory=Lock, repr=False)
    _published: int = 0
    _accepted: int = 0
    _rejected: int = 0
    _skipped: int = 0
    _journey_events: int = 0
    _latency_ms_sum: float = 0.0
    _latency_ms_count: int = 0

    def __post_init__(self) -> None:
        if self.logger is None:
            self.logger = build_experience_diagnostics_logger(
                enabled=self.enabled,
                events=self.events,
            )

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_journey_event(
        self,
        *,
        experience_event: str,
        journey_stage: str,
        timestamp: str,
        correlation_id: str | None = None,
        observation_id: str = "",
    ) -> JourneyTrace | None:
        """Record JourneyEvent entry into the observation pipeline."""
        if not self.enabled:
            return None
        corr = (
            (correlation_id or "").strip()
            or CorrelationContext.get_correlation_id()
        )
        with self._lock:
            self._journey_events += 1
        trace = build_journey_trace(
            correlation_id=corr,
            journey_stage=journey_stage,
            experience_event=experience_event,
            observation_status=OBSERVATION_STATUS_PENDING,
            timestamp=timestamp,
            pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
            observation_id=observation_id,
        )
        self.trace_store.append(trace)
        assert self.logger is not None
        self.logger.log_journey_event(
            correlation_id=corr,
            journey_stage=journey_stage,
            experience_event=experience_event,
            trace_id=trace.trace_id,
            pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
        )
        return trace

    def record_publish(
        self,
        result: ObservationPublishResult,
        *,
        timestamp: str | None = None,
        latency_ms: float | None = None,
    ) -> JourneyTrace | None:
        """Record an ObservationPublishResult into counters + traces + logs."""
        if not self.enabled:
            return None
        if not isinstance(result, ObservationPublishResult):
            raise TypeError("result must be an ObservationPublishResult")

        observation = result.observation
        if observation is None:
            # Flag-off path before assembly — still count skips operationally.
            with self._lock:
                self._skipped += 1
            return None

        status = result.status
        corr = observation.correlation_id or CorrelationContext.get_correlation_id()
        ts = (timestamp or observation.timestamp or "").strip()
        latency = float(latency_ms) if latency_ms is not None else None

        with self._lock:
            if status == PUBLISH_STATUS_PUBLISHED:
                self._published += 1
                self._accepted += 1
                if latency is not None:
                    self._latency_ms_sum += latency
                    self._latency_ms_count += 1
            elif status == PUBLISH_STATUS_FAILED:
                self._rejected += 1
                if latency is not None:
                    self._latency_ms_sum += latency
                    self._latency_ms_count += 1
            elif status == PUBLISH_STATUS_SKIPPED:
                self._skipped += 1

        # Assembled stage
        assembled = build_journey_trace(
            correlation_id=corr,
            journey_stage=observation.journey_stage,
            experience_event=observation.experience_event,
            observation_status=OBSERVATION_STATUS_PENDING,
            timestamp=ts,
            pipeline_stage=PIPELINE_STAGE_ASSEMBLED,
            observation_id=observation.observation_id,
        )
        self.trace_store.append(assembled)

        # Publish attempted / outcome stage
        if status == PUBLISH_STATUS_PUBLISHED:
            pipe = PIPELINE_STAGE_EVIDENCE_ACK
            obs_status = OBSERVATION_STATUS_PUBLISHED
        elif status == PUBLISH_STATUS_FAILED:
            pipe = PIPELINE_STAGE_FAILED
            obs_status = OBSERVATION_STATUS_FAILED
        else:
            pipe = PIPELINE_STAGE_SKIPPED
            obs_status = OBSERVATION_STATUS_SKIPPED

        # Intermediate publish_attempted for accepted / rejected paths
        if status in {PUBLISH_STATUS_PUBLISHED, PUBLISH_STATUS_FAILED}:
            attempted = build_journey_trace(
                correlation_id=corr,
                journey_stage=observation.journey_stage,
                experience_event=observation.experience_event,
                observation_status=OBSERVATION_STATUS_PENDING,
                timestamp=ts,
                pipeline_stage=PIPELINE_STAGE_PUBLISH_ATTEMPTED,
                observation_id=observation.observation_id,
                latency_ms=latency,
            )
            self.trace_store.append(attempted)

        outcome = build_journey_trace(
            correlation_id=corr,
            journey_stage=observation.journey_stage,
            experience_event=observation.experience_event,
            observation_status=obs_status,
            timestamp=ts,
            pipeline_stage=pipe,
            observation_id=observation.observation_id,
            evidence_id=result.evidence_id,
            reason=result.reason,
            latency_ms=latency,
        )
        self.trace_store.append(outcome)

        assert self.logger is not None
        self.logger.log_observation_published(
            correlation_id=corr,
            journey_stage=observation.journey_stage,
            experience_event=observation.experience_event,
            observation_status=obs_status,
            observation_id=observation.observation_id,
            reason=result.reason,
            trace_id=outcome.trace_id,
            latency_ms=latency,
        )
        self.logger.log_evidence_ack(
            correlation_id=corr,
            experience_event=observation.experience_event,
            observation_id=observation.observation_id,
            evidence_id=result.evidence_id,
            observation_status=obs_status,
            reason=result.reason,
            trace_id=outcome.trace_id,
            latency_ms=latency,
        )
        return outcome

    def record_observation(
        self,
        observation: ExperienceObservation,
        *,
        pipeline_stage: str = PIPELINE_STAGE_ASSEMBLED,
        observation_status: str = OBSERVATION_STATUS_PENDING,
    ) -> JourneyTrace | None:
        """Record a standalone assembled observation (without publish)."""
        if not self.enabled:
            return None
        if not isinstance(observation, ExperienceObservation):
            raise TypeError("observation must be an ExperienceObservation")
        corr = observation.correlation_id or CorrelationContext.get_correlation_id()
        trace = build_journey_trace(
            correlation_id=corr,
            journey_stage=observation.journey_stage,
            experience_event=observation.experience_event,
            observation_status=observation_status,
            timestamp=observation.timestamp,
            pipeline_stage=pipeline_stage,
            observation_id=observation.observation_id,
        )
        self.trace_store.append(trace)
        return trace

    # ------------------------------------------------------------------
    # Snapshots / queries
    # ------------------------------------------------------------------

    def counters(self) -> ObservationCounters:
        """Immutable counter snapshot."""
        with self._lock:
            return ObservationCounters(
                observations_published=self._published,
                observations_accepted=self._accepted,
                observations_rejected=self._rejected,
                observations_skipped=self._skipped,
                journey_events_traced=self._journey_events,
                intake_latency_ms_sum=self._latency_ms_sum,
                intake_latency_ms_count=self._latency_ms_count,
                mean_intake_latency_ms=_mean(
                    self._latency_ms_sum, self._latency_ms_count
                ),
            )

    def feature_flag_state(self) -> FeatureFlagDiagnostics:
        """Current feature-flag projection used by this diagnostics instance."""
        return FeatureFlagDiagnostics(
            enable_experience_diagnostics=self.enabled,
            enable_experience_observation=self.observation_flag,
            enable_evidence_platform=self.evidence_flag,
            enable_unified_journey=self.unified_journey_flag,
        )

    def publisher_health(self) -> PublisherHealthSummary:
        """Publisher availability / binding summary."""
        pub = self.publisher
        if pub is None:
            return PublisherHealthSummary(available=False)
        return PublisherHealthSummary(
            available=True,
            enabled=bool(getattr(pub, "enabled", False)),
            publisher_id=str(getattr(pub, "publisher_id", "") or ""),
            publisher_version=str(getattr(pub, "publisher_version", "") or ""),
            evidence_bound=getattr(pub, "evidence", None) is not None,
        )

    def health_checker(self) -> PipelineHealthChecker:
        """Build a health checker bound to current DI / flag state."""
        return build_pipeline_health_checker(
            diagnostics_enabled=self.enabled,
            observation_flag=self.observation_flag,
            evidence_flag=self.evidence_flag,
            publisher=self.publisher,
            evidence=self.evidence,
        )

    def pipeline_health(self) -> PipelineHealthReport:
        """Evaluate Observation → Evidence pipeline health."""
        if not self.enabled:
            return PipelineHealthReport(
                overall_status=HEALTH_STATUS_UNAVAILABLE,
                overall_ok=False,
                checks=(),
                diagnostics_enabled=False,
                observation_flag=self.observation_flag,
                evidence_flag=self.evidence_flag,
            )
        return self.health_checker().evaluate()

    def traces_for(
        self, correlation_id: str
    ) -> tuple[JourneyTrace, ...]:
        """Return stored traces for a correlation id (pipeline lineage)."""
        return self.trace_store.by_correlation_id(correlation_id)

    def recent_traces(self, *, limit: int = 50) -> tuple[JourneyTrace, ...]:
        """Recent JourneyTrace records for ops dashboards."""
        return self.trace_store.recent(limit=limit)

    def dashboard(self, *, recent_limit: int = 50) -> ExperienceDiagnosticsDashboard:
        """Build an internal-only diagnostics dashboard DTO."""
        return ExperienceDiagnosticsDashboard(
            diagnostics_enabled=self.enabled,
            feature_flags=self.feature_flag_state(),
            counters=self.counters(),
            publisher_health=self.publisher_health(),
            pipeline_health=self.pipeline_health(),
            recent_traces=self.recent_traces(limit=recent_limit),
        )

    def bind_publisher(self, publisher: Any | None) -> None:
        """Late-bind publisher reference after DI construction."""
        self.publisher = publisher

    def bind_evidence(self, evidence: Any | None) -> None:
        """Late-bind Evidence adapter reference after DI construction."""
        self.evidence = evidence

    def reset(self) -> None:
        """Reset counters and traces (tests / ops)."""
        with self._lock:
            self._published = 0
            self._accepted = 0
            self._rejected = 0
            self._skipped = 0
            self._journey_events = 0
            self._latency_ms_sum = 0.0
            self._latency_ms_count = 0
        self.trace_store.clear()
        if self.logger is not None:
            self.logger.clear()


def build_experience_observation_diagnostics(
    *,
    enabled: bool,
    observation_flag: bool = False,
    evidence_flag: bool = False,
    unified_journey_flag: bool = False,
    publisher: Any | None = None,
    evidence: Any | None = None,
    events: EventRegistry | None = None,
    trace_store: JourneyTraceStore | None = None,
    logger: ExperienceDiagnosticsLogger | None = None,
) -> ObservationDiagnosticsService | None:
    """DI helper — construct diagnostics only when ENABLE_EXPERIENCE_DIAGNOSTICS."""
    if not enabled:
        return None
    return ObservationDiagnosticsService(
        enabled=True,
        observation_flag=observation_flag,
        evidence_flag=evidence_flag,
        unified_journey_flag=unified_journey_flag,
        publisher=publisher,
        evidence=evidence,
        events=events,
        trace_store=trace_store or build_journey_trace_store(),
        logger=logger,
    )
