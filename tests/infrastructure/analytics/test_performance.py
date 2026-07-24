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
from app.infrastructure.analytics.registry import (
    INFRASTRUCTURE_PROBE,
    AnalyticsEventRegistry,
)

DISPATCH_BUDGET_MS_P95 = 5.0
HASH_BUDGET_MS_P95 = 20.0
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
        registry=AnalyticsEventRegistry.phase_b_default(),
    )
    samples = []
    for i in range(SAMPLE_SIZE):
        result = dispatcher.dispatch(_event(i))
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"enabled p95={p95:.3f} ms"


def test_session_event_dispatch_under_budget() -> None:
    """Phase B session builders + dispatch stay under the 5 ms p95 budget."""
    from app.infrastructure.analytics.session_events import (
        COMPLETION_COMPLETED,
        build_session_completed_event,
        build_session_started_event,
    )

    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
        registry=AnalyticsEventRegistry.phase_b_default(),
    )
    samples = []
    for i in range(SAMPLE_SIZE):
        if i % 2 == 0:
            event = build_session_started_event(user_id=1, mission_id=i + 1)
        else:
            event = build_session_completed_event(
                user_id=1,
                mission_id=i + 1,
                completion_status=COMPLETION_COMPLETED,
                duration_seconds=600,
            )
        result = dispatcher.dispatch(event)
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"session p95={p95:.3f} ms"


def test_reflection_event_dispatch_under_budget() -> None:
    """Phase C reflection builders + dispatch stay under the 5 ms p95 budget."""
    from app.infrastructure.analytics.reflection_events import (
        build_reflection_completed_event,
        build_reflection_submitted_event,
    )

    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
        registry=AnalyticsEventRegistry.phase_c_default(),
    )
    samples = []
    for i in range(SAMPLE_SIZE):
        if i % 2 == 0:
            event = build_reflection_submitted_event(
                user_id=1,
                reflection_id=f"ref-{i}",
                session_id=f"sess-{i}",
            )
        else:
            event = build_reflection_completed_event(
                user_id=1,
                reflection_id=f"ref-{i}",
            )
        result = dispatcher.dispatch(event)
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"reflection p95={p95:.3f} ms"


def test_educational_state_snapshot_dispatch_under_budget() -> None:
    """Phase D snapshot builders + dispatch stay under the 5 ms p95 budget."""
    from app.infrastructure.analytics.educational_state_events import (
        build_educational_state_snapshot_event,
    )

    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
        registry=AnalyticsEventRegistry.phase_d_default(),
    )
    digest = "ab" * 32
    samples = []
    for i in range(SAMPLE_SIZE):
        event = build_educational_state_snapshot_event(
            user_id=1,
            snapshot_id=f"snap-{i}",
            content_hash=digest,
        )
        result = dispatcher.dispatch(event)
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"ess snapshot p95={p95:.3f} ms"


def test_journey_and_twin_event_dispatch_under_budget() -> None:
    """Phase E journey + twin builders + dispatch stay under 5 ms p95."""
    from app.infrastructure.analytics.journey_events import (
        build_journey_progressed_event,
    )
    from app.infrastructure.analytics.twin_events import (
        EVOLUTION_BIRTH,
        build_twin_evolved_event,
    )

    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
        registry=AnalyticsEventRegistry.phase_e_default(),
    )
    digest = "cd" * 32
    samples = []
    for i in range(SAMPLE_SIZE):
        if i % 2 == 0:
            event = build_journey_progressed_event(
                user_id=1,
                journey_id=f"j-{i}",
                curriculum_node_id=f"node-{i}",
                transition_id="start_journey",
            )
        else:
            event = build_twin_evolved_event(
                user_id=1,
                twin_snapshot_id=f"twin-snap-{i}",
                twin_version=str(i),
                evolution_reason=EVOLUTION_BIRTH,
                snapshot_hash=digest,
            )
        result = dispatcher.dispatch(event)
        assert result.status is DispatchStatus.ENQUEUED
        samples.append(result.elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < DISPATCH_BUDGET_MS_P95, f"phase e p95={p95:.3f} ms"


def test_twin_snapshot_hash_under_budget() -> None:
    """Twin snapshot_hash generation stays under the 20 ms p95 budget."""
    import time

    from app.application.twin_repository.content_hash import (
        compute_twin_snapshot_hash,
    )

    payload = (
        '{"format_version":"1.0","twin":{"identity":{"student_id":"1"},'
        '"knowledge":{"topics":[' + ",".join(f'{{"id":"t{i}"}}' for i in range(40)) + "]}}}"
    )
    samples = []
    for _ in range(SAMPLE_SIZE):
        started = time.perf_counter()
        digest = compute_twin_snapshot_hash(payload)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        assert len(digest) == 64
        samples.append(elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < HASH_BUDGET_MS_P95, f"twin snapshot_hash p95={p95:.3f} ms"


def test_educational_state_content_hash_under_budget() -> None:
    """Hash generation stays under the PRD-001 §10 20 ms p95 budget."""
    import time

    from app.application.educational_state import EducationalStateSnapshot
    from app.application.educational_state.content_hash import (
        compute_educational_state_content_hash,
    )

    snapshot = EducationalStateSnapshot(
        student_id="1",
        learner_summary={"name": "Ada", "topics": list(range(50))},
        readiness_summary={"level": "building", "detail": {"a": 1, "b": 2}},
        recommendation={"topic_id": "t1"},
        todays_session={"mission_id": 9},
        journey_progress={"pct": 10},
        journey_topics=tuple({"id": f"t{i}"} for i in range(20)),
        learning_insights={"streak": 3},
        revision_options=tuple({"id": f"r{i}"} for i in range(10)),
        twin_available=True,
        adaptive_available=True,
        mission_available=True,
        journey_available=True,
    )
    samples = []
    for _ in range(SAMPLE_SIZE):
        started = time.perf_counter()
        digest = compute_educational_state_content_hash(snapshot)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        assert len(digest) == 64
        samples.append(elapsed_ms)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < HASH_BUDGET_MS_P95, f"content_hash p95={p95:.3f} ms"


@pytest.mark.parametrize("enabled", [False, True])
def test_dispatch_returns_elapsed_ms(enabled: bool) -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=enabled),
        outbox=MemoryOutboxSink(),
    )
    result = dispatcher.dispatch(_event(0))
    assert result.elapsed_ms >= 0.0
