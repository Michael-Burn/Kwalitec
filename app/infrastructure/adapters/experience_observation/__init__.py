"""Experience Observation Bridge (P2-MS006) + Diagnostics (P2-MS007).

One-way Experience → Learning Evidence Platform observation bridge.
Immutable factual observations only — no educational interpretation,
persistence, scoring, analytics, or authority changes.

Feature flags:
- ``KWALITEC_EXPERIENCE_OBSERVATION`` / ``ENABLE_EXPERIENCE_OBSERVATION``
  (default OFF). Independently controllable from ``ENABLE_EVIDENCE_PLATFORM``.
- ``KWALITEC_EXPERIENCE_DIAGNOSTICS`` / ``ENABLE_EXPERIENCE_DIAGNOSTICS``
  (default OFF). Independently controllable from all other flags.
"""

from __future__ import annotations

from .assembler import ObservationAssembler, build_observation_assembler
from .contracts import (
    AUTHORITY_EXPERIENCE_OBSERVATION,
    CONTRACT_VERSION,
    EXPERIENCE_EVENT_MISSION_STARTED,
    EXPERIENCE_EVENT_REFLECTION_COMPLETED,
    EXPERIENCE_EVENT_REFLECTION_SKIPPED,
    EXPERIENCE_EVENT_REFLECTION_STARTED,
    EXPERIENCE_EVENT_SESSION_COMPLETED,
    EXPERIENCE_EVENT_SESSION_STARTED,
    OBSERVABLE_EXPERIENCE_EVENTS,
    PUBLISH_STATUS_FAILED,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_SKIPPED,
    PUBLISH_STATUSES,
    REASON_EVIDENCE_REJECTED,
    REASON_EVIDENCE_UNAVAILABLE,
    REASON_FLAG_OFF,
    REASON_NOT_OBSERVABLE,
    EvidenceObservationPort,
    ExperienceObservation,
    ExperienceObservationPublisherPort,
    ObservationPublishResult,
    deterministic_observation_id,
    serialize_canonical,
)
from .dashboard import (
    ExperienceDiagnosticsDashboard,
    FeatureFlagDiagnostics,
    ObservationCounters,
    PublisherHealthSummary,
)
from .diagnostics import (
    ObservationDiagnosticsService,
    build_experience_observation_diagnostics,
)
from .evidence_mapper import observation_to_observed_event
from .health import (
    CHECK_DI_WIRING,
    CHECK_EVIDENCE_INTAKE,
    CHECK_FEATURE_FLAGS,
    CHECK_PUBLISHER,
    HEALTH_STATUS_DEGRADED,
    HEALTH_STATUS_OK,
    HEALTH_STATUS_UNAVAILABLE,
    HealthCheckResult,
    PipelineHealthChecker,
    PipelineHealthReport,
    build_pipeline_health_checker,
)
from .journey_trace import (
    AUTHORITY_JOURNEY_TRACE,
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
    deterministic_trace_id,
)
from .publisher import (
    ExperienceObservationPublisher,
    build_experience_observation_publisher,
)
from .telemetry import (
    ExperienceDiagnosticsLogger,
    build_experience_diagnostics_logger,
)

__all__ = [
    "AUTHORITY_EXPERIENCE_OBSERVATION",
    "AUTHORITY_JOURNEY_TRACE",
    "CHECK_DI_WIRING",
    "CHECK_EVIDENCE_INTAKE",
    "CHECK_FEATURE_FLAGS",
    "CHECK_PUBLISHER",
    "CONTRACT_VERSION",
    "EXPERIENCE_EVENT_MISSION_STARTED",
    "EXPERIENCE_EVENT_REFLECTION_COMPLETED",
    "EXPERIENCE_EVENT_REFLECTION_SKIPPED",
    "EXPERIENCE_EVENT_REFLECTION_STARTED",
    "EXPERIENCE_EVENT_SESSION_COMPLETED",
    "EXPERIENCE_EVENT_SESSION_STARTED",
    "HEALTH_STATUS_DEGRADED",
    "HEALTH_STATUS_OK",
    "HEALTH_STATUS_UNAVAILABLE",
    "OBSERVABLE_EXPERIENCE_EVENTS",
    "OBSERVATION_STATUS_FAILED",
    "OBSERVATION_STATUS_PENDING",
    "OBSERVATION_STATUS_PUBLISHED",
    "OBSERVATION_STATUS_SKIPPED",
    "PIPELINE_STAGE_ASSEMBLED",
    "PIPELINE_STAGE_EVIDENCE_ACK",
    "PIPELINE_STAGE_FAILED",
    "PIPELINE_STAGE_JOURNEY_EVENT",
    "PIPELINE_STAGE_PUBLISH_ATTEMPTED",
    "PIPELINE_STAGE_SKIPPED",
    "PUBLISH_STATUS_FAILED",
    "PUBLISH_STATUS_PUBLISHED",
    "PUBLISH_STATUS_SKIPPED",
    "PUBLISH_STATUSES",
    "REASON_EVIDENCE_REJECTED",
    "REASON_EVIDENCE_UNAVAILABLE",
    "REASON_FLAG_OFF",
    "REASON_NOT_OBSERVABLE",
    "EvidenceObservationPort",
    "ExperienceDiagnosticsDashboard",
    "ExperienceDiagnosticsLogger",
    "ExperienceObservation",
    "ExperienceObservationPublisher",
    "ExperienceObservationPublisherPort",
    "FeatureFlagDiagnostics",
    "HealthCheckResult",
    "JourneyTrace",
    "JourneyTraceStore",
    "ObservationAssembler",
    "ObservationCounters",
    "ObservationDiagnosticsService",
    "ObservationPublishResult",
    "PipelineHealthChecker",
    "PipelineHealthReport",
    "PublisherHealthSummary",
    "build_experience_diagnostics_logger",
    "build_experience_observation_diagnostics",
    "build_experience_observation_publisher",
    "build_journey_trace",
    "build_journey_trace_store",
    "build_observation_assembler",
    "build_pipeline_health_checker",
    "deterministic_observation_id",
    "deterministic_trace_id",
    "observation_to_observed_event",
    "serialize_canonical",
]
