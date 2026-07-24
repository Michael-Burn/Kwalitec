"""PRD-001 Phase A — Analytics event infrastructure.

Passive observation pipeline only. Never calculates educational truth,
never modifies Twin / EducationalState / Learning Evidence, and never
emits domain events until a later authorised phase wires lifecycle hooks.

Feature flag ``ANALYTICS_EVENTS_V1`` defaults OFF → dispatcher is a no-op.
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
from app.infrastructure.analytics.feature_flag import (
    ANALYTICS_EVENTS_V1,
    AnalyticsFeatureFlag,
    resolve_analytics_feature_flag,
)
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import AnalyticsEventValidator
from app.infrastructure.analytics.versioning import AnalyticsEventVersion

__all__ = [
    "ANALYTICS_EVENTS_V1",
    "AnalyticsEvent",
    "AnalyticsEventDispatcher",
    "AnalyticsEventRegistry",
    "AnalyticsEventSerializer",
    "AnalyticsEventValidator",
    "AnalyticsEventVersion",
    "AnalyticsFeatureFlag",
    "AuditMetadata",
    "DispatchResult",
    "DispatchStatus",
    "build_idempotency_key",
    "new_correlation_id",
    "resolve_analytics_feature_flag",
]
