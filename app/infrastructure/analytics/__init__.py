"""PRD-001 analytics event infrastructure (Phases A–E + EP-002 ops).

Passive observation pipeline only. Never calculates educational truth,
never modifies Twin / EducationalState / Learning Evidence.

Phase B wires Study Session lifecycle emits
(``session.started`` / ``session.completed``) **after** educational
persistence succeeds.

Phase C wires Reflection lifecycle emits
(``reflection.submitted`` / ``reflection.completed``) **after**
authoritative reflection capture succeeds.

Phase D wires Educational State snapshot observation
(``educational_state.snapshot``) **after** EducationalStateService
assembles a material content-hash change. Hash + metadata only —
Educational State payload is never stored in analytics.

Phase E wires Twin evolution observation (``twin.evolved``) **after**
durable TwinRepository persist, and registers Journey progression
(``journey.progressed``) builders. Journey production emit is deferred
until a durable LearningJourneyRepository adapter exists (ADR-026).

EP-002 adds durable SQL outbox drain, replay, dead-letter, retention
enforcement, privacy workflows, and operational metrics. Feature flag
``ANALYTICS_EVENTS_V1`` defaults OFF → dispatcher is a no-op.
"""

from __future__ import annotations

from app.infrastructure.analytics.audit import AuditMetadata
from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.correlation import new_correlation_id
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchResult,
    DispatchStatus,
)
from app.infrastructure.analytics.educational_state_events import (
    EDUCATIONAL_STATE_SNAPSHOT,
    build_educational_state_snapshot_event,
    emit_educational_state_event,
    emit_educational_state_snapshot,
)
from app.infrastructure.analytics.feature_flag import (
    ANALYTICS_EVENTS_V1,
    AnalyticsFeatureFlag,
    resolve_analytics_feature_flag,
)
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.journey_events import (
    JOURNEY_PROGRESSED,
    build_journey_progressed_event,
    emit_journey_event,
    emit_journey_progressed,
)
from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)
from app.infrastructure.analytics.privacy import (
    AnalyticsConsentPolicy,
    AnalyticsPrivacyService,
    ConsentVerdict,
    DeletionResult,
    ExportResult,
)
from app.infrastructure.analytics.reflection_events import (
    PROCESSING_COMPLETED,
    REFLECTION_COMPLETED,
    REFLECTION_SUBMITTED,
    REFLECTION_TYPE_JOURNEY_SESSION,
    build_reflection_completed_event,
    build_reflection_submitted_event,
    emit_reflection_completed,
    emit_reflection_event,
    emit_reflection_lifecycle,
    emit_reflection_submitted,
)
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.replay import AnalyticsReplayService, ReplayResult
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.session_events import (
    COMPLETION_ABANDONED_AFTER_START,
    COMPLETION_COMPLETED,
    SESSION_COMPLETED,
    SESSION_STARTED,
    build_session_completed_event,
    build_session_started_event,
    emit_session_completed,
    emit_session_event,
    emit_session_started,
)
from app.infrastructure.analytics.twin_events import (
    EVOLUTION_BIRTH,
    EVOLUTION_SUCCESSOR,
    TWIN_EVOLVED,
    build_twin_evolved_event,
    emit_twin_event,
    emit_twin_evolved,
)
from app.infrastructure.analytics.validator import AnalyticsEventValidator
from app.infrastructure.analytics.versioning import AnalyticsEventVersion
from app.infrastructure.analytics.worker import AnalyticsOutboxWorker, WorkerBatchResult

__all__ = [
    "ANALYTICS_EVENTS_V1",
    "ANALYTICS_METRICS",
    "COMPLETION_ABANDONED_AFTER_START",
    "COMPLETION_COMPLETED",
    "EDUCATIONAL_STATE_SNAPSHOT",
    "EVOLUTION_BIRTH",
    "EVOLUTION_SUCCESSOR",
    "JOURNEY_PROGRESSED",
    "PROCESSING_COMPLETED",
    "REFLECTION_COMPLETED",
    "REFLECTION_SUBMITTED",
    "REFLECTION_TYPE_JOURNEY_SESSION",
    "SESSION_COMPLETED",
    "SESSION_STARTED",
    "TWIN_EVOLVED",
    "AnalyticsConsentPolicy",
    "AnalyticsEvent",
    "AnalyticsEventDispatcher",
    "AnalyticsEventRegistry",
    "AnalyticsEventSerializer",
    "AnalyticsEventValidator",
    "AnalyticsEventVersion",
    "AnalyticsFeatureFlag",
    "AnalyticsOperationalMetrics",
    "AnalyticsOutboxWorker",
    "AnalyticsPrivacyService",
    "AnalyticsReplayService",
    "AuditMetadata",
    "ConsentVerdict",
    "DeletionResult",
    "DispatchResult",
    "DispatchStatus",
    "ExportResult",
    "ReplayResult",
    "WorkerBatchResult",
    "build_educational_state_snapshot_event",
    "build_idempotency_key",
    "build_journey_progressed_event",
    "build_reflection_completed_event",
    "build_reflection_submitted_event",
    "build_session_completed_event",
    "build_session_started_event",
    "build_twin_evolved_event",
    "emit_educational_state_event",
    "emit_educational_state_snapshot",
    "emit_journey_event",
    "emit_journey_progressed",
    "emit_reflection_completed",
    "emit_reflection_event",
    "emit_reflection_lifecycle",
    "emit_reflection_submitted",
    "emit_session_completed",
    "emit_session_event",
    "emit_session_started",
    "emit_twin_event",
    "emit_twin_evolved",
    "new_correlation_id",
    "resolve_analytics_feature_flag",
]
