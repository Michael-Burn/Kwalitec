"""Performance harness — analytics dispatch overhead (PRD-001 §10).

Budget: event generation / dispatch path ≤ 5 ms p95 (in-process outbox).
"""

from __future__ import annotations

import statistics

import pytest

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import INFRASTRUCTURE_PROBE

DISPATCH_BUDGET_MS_P95 = 5.0
SAMPLE_SIZE = 200


def _event(i: int) -> AnalyticsEvent:
    return AnalyticsEvent.create(
        INFRASTRUCTURE_PROBE,
        user_id=1,
        payload={"i": i},
        idempotency_key=build_idempotency_key(
            user_id=1,
            event_type=INFRASTRUCTURE_PROBE,
            entity_key=f"perf-{i}",
        ),
    )


def test_dispatch_disabled_overhead_under_budget() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        outbox=MemoryOutboxSink(),
    )
    samples = []
    for i in range(SAMPLE_SIZE):
        result = dispatcher.dispatch(_event(i))
        assert result.status is DispatchStatus.DISABLED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]  # ~95th
    assert p95 < DISPATCH_BUDGET_MS_P95, f"disabled p95={p95:.3f} ms"


def test_dispatch_enabled_memory_outbox_under_budget() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
    )
    samples = []
    for i in range(SAMPLE_SIZE):
        result = dispatcher.dispatch(_event(i))
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"enabled p95={p95:.3f} ms"


@pytest.mark.parametrize("enabled", [False, True])
def test_dispatch_returns_elapsed_ms(enabled: bool) -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=enabled),
        outbox=MemoryOutboxSink(),
    )
    result = dispatcher.dispatch(_event(0))
    assert result.elapsed_ms >= 0.0
