"""Analytics event dispatcher — passive, fail-open, flag-gated.

When ``ANALYTICS_EVENTS_V1`` is off (default), ``dispatch`` is a pure no-op
with no database writes and no educational side effects.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.correlation import new_correlation_id
from app.infrastructure.analytics.feature_flag import (
    AnalyticsFeatureFlag,
    resolve_analytics_feature_flag,
)
from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)
from app.infrastructure.analytics.outbox import (
    AnalyticsOutboxPort,
    MemoryOutboxSink,
    NullOutboxSink,
    serialize_for_outbox,
)
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import AnalyticsEventValidator

logger = logging.getLogger(__name__)


class DispatchStatus(str, Enum):
    """Outcome of a dispatch attempt."""

    DISABLED = "disabled"
    ENQUEUED = "enqueued"
    DUPLICATE = "duplicate"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass(frozen=True)
class DispatchResult:
    """Result of :meth:`AnalyticsEventDispatcher.dispatch`."""

    status: DispatchStatus
    event_id: str = ""
    outbox_id: str = ""
    errors: tuple[str, ...] = ()
    elapsed_ms: float = 0.0


class AnalyticsEventDispatcher:
    """Validate and enqueue analytics events behind the feature flag.

    Never calculates educational scores. Never modifies Twin / EducationalState.
    Fail-open: exceptions are caught and returned as ``FAILED`` (logged).
    """

    def __init__(
        self,
        *,
        registry: AnalyticsEventRegistry | None = None,
        validator: AnalyticsEventValidator | None = None,
        serializer: AnalyticsEventSerializer | None = None,
        outbox: AnalyticsOutboxPort | None = None,
        feature_flag: AnalyticsFeatureFlag | None = None,
        metrics: AnalyticsOperationalMetrics | None = None,
    ) -> None:
        self._registry = registry or AnalyticsEventRegistry.phase_e_default()
        self._validator = validator or AnalyticsEventValidator(self._registry)
        self._serializer = serializer or AnalyticsEventSerializer()
        self._feature_flag = (
            feature_flag
            if feature_flag is not None
            else resolve_analytics_feature_flag()
        )
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS
        if outbox is not None:
            self._outbox = outbox
        elif self._feature_flag.enabled:
            self._outbox = MemoryOutboxSink()
        else:
            self._outbox = NullOutboxSink()

    @property
    def feature_flag(self) -> AnalyticsFeatureFlag:
        """Active feature flag snapshot."""
        return self._feature_flag

    @property
    def registry(self) -> AnalyticsEventRegistry:
        """Active event type registry."""
        return self._registry

    @property
    def outbox(self) -> AnalyticsOutboxPort:
        """Active outbox sink."""
        return self._outbox

    def dispatch(self, event: AnalyticsEvent) -> DispatchResult:
        """Dispatch one analytics event (or no-op when flag disabled).

        Target overhead: &lt; 5 ms p95 for the synchronous path (validate +
        serialize + enqueue). Measured in the Phase A performance harness.
        """
        started = time.perf_counter()
        try:
            if not self._feature_flag.enabled:
                result = DispatchResult(
                    status=DispatchStatus.DISABLED,
                    event_id=event.event_id,
                    elapsed_ms=_elapsed_ms(started),
                )
                self._metrics.record_dispatch(
                    status=result.status.value, elapsed_ms=result.elapsed_ms
                )
                return result

            # Ensure correlation id for observability.
            correlation_id = event.correlation_id or new_correlation_id()
            if correlation_id != event.correlation_id:
                event = AnalyticsEvent.create(
                    event.event_type,
                    user_id=event.user_id,
                    payload=dict(event.payload),
                    event_id=event.event_id,
                    occurred_at=event.occurred_at,
                    schema_version=event.schema_version,
                    idempotency_key=event.idempotency_key,
                    correlation_id=correlation_id,
                    audit=event.audit,
                )

            validation = self._validator.validate(event)
            if not validation.ok:
                result = DispatchResult(
                    status=DispatchStatus.REJECTED,
                    event_id=event.event_id,
                    errors=validation.errors,
                    elapsed_ms=_elapsed_ms(started),
                )
                self._metrics.record_dispatch(
                    status=result.status.value, elapsed_ms=result.elapsed_ms
                )
                return result

            stamped = AnalyticsEvent.create(
                event.event_type,
                user_id=event.user_id,
                payload=dict(event.payload),
                event_id=event.event_id,
                occurred_at=event.occurred_at,
                schema_version=event.schema_version,
                idempotency_key=event.idempotency_key,
                correlation_id=event.correlation_id,
                audit=event.audit.with_emit(
                    flag_enabled=True,
                    sink=getattr(self._outbox, "name", "outbox"),
                    source="dispatcher",
                ),
            )
            payload_json = serialize_for_outbox(stamped, self._serializer)
            before_keys = {
                (r.user_id, r.event_type, r.idempotency_key)
                for r in self._outbox.pending()
            }
            record = self._outbox.enqueue(stamped, payload_json=payload_json)
            key = (stamped.user_id, stamped.event_type, stamped.idempotency_key)
            status = (
                DispatchStatus.DUPLICATE
                if key in before_keys
                else DispatchStatus.ENQUEUED
            )
            result = DispatchResult(
                status=status,
                event_id=stamped.event_id,
                outbox_id=record.outbox_id,
                elapsed_ms=_elapsed_ms(started),
            )
            self._metrics.record_dispatch(
                status=result.status.value, elapsed_ms=result.elapsed_ms
            )
            return result
        except Exception:  # noqa: BLE001 — fail-open for educational UX
            logger.exception(
                "analytics.emit_failed event_id=%s type=%s",
                getattr(event, "event_id", ""),
                getattr(event, "event_type", ""),
            )
            result = DispatchResult(
                status=DispatchStatus.FAILED,
                event_id=getattr(event, "event_id", ""),
                errors=("analytics.emit_failed",),
                elapsed_ms=_elapsed_ms(started),
            )
            self._metrics.record_dispatch(
                status=result.status.value, elapsed_ms=result.elapsed_ms
            )
            return result


def _elapsed_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000.0
