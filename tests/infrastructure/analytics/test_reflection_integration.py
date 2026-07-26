"""Integration + negative tests — Reflection analytics instrumentation.

Reflection capture must succeed even when analytics fails or is disabled.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.application.learning_session.exceptions import ReflectionRequired
from app.application.learning_session.reflection_manager import ReflectionManager
from app.application.learning_session.runtime import LearningSessionRuntime
from app.domain.learning_journey.entities.journey_reflection import ReflectionPosture
from app.domain.learning_journey.value_objects.session_state import SessionState
from app.infrastructure.analytics.dispatcher import AnalyticsEventDispatcher
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.reflection_events import (
    REFLECTION_COMPLETED,
    REFLECTION_SUBMITTED,
)
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.validator import (
    AnalyticsEventValidator,
    ValidationResult,
)
from tests.application.learning_session.helpers import (
    NOW,
    completed_handle,
    make_session,
)


def _enabled_dispatcher(
    outbox: MemoryOutboxSink | None = None,
) -> AnalyticsEventDispatcher:
    sink = outbox if outbox is not None else MemoryOutboxSink()
    return AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=sink,
        registry=AnalyticsEventRegistry.phase_c_default(),
    )


def _completed_with_pending(manager: ReflectionManager | None = None):
    mgr = manager or ReflectionManager(clock=lambda: NOW, id_factory=lambda: "r1")
    session = mgr.attach_pending(make_session(state=SessionState.COMPLETED))
    return mgr, session


class TestReflectionInstrumentationIntegration:
    def test_capture_emits_submitted_and_completed_when_flag_on(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = manager.capture(
                session,
                summary="Learned limits",
                challenges="Notation",
                user_id=42,
            )

        assert updated.reflection is not None
        assert updated.reflection.posture == ReflectionPosture.CAPTURED
        assert summary.is_captured
        assert len(outbox.pending()) == 2
        types = [r.event_type for r in outbox.pending()]
        assert types.count(REFLECTION_SUBMITTED) == 1
        assert types.count(REFLECTION_COMPLETED) == 1

    def test_capture_without_user_id_skips_emit(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = manager.capture(
                session,
                summary="Learned limits",
                challenges="Notation",
            )

        assert summary.is_captured
        assert updated.reflection_captured
        assert outbox.pending() == ()

    def test_runtime_collect_reflection_emits_when_user_id_provided(self) -> None:
        rt = LearningSessionRuntime(
            clock=lambda: NOW,
            id_factory=lambda: "rt1",
        )
        handle = completed_handle(rt, with_reflection=False)
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = rt.collect_reflection(
                handle,
                summary="Clarity on cashflows",
                challenges="Timing symbols",
                user_id=7,
            )

        assert summary.is_captured
        assert updated.session.reflection is not None
        assert len(outbox.pending()) == 2

    def test_flag_off_capture_succeeds_zero_writes(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_c_default(),
        )

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = manager.capture(
                session,
                summary="Learned limits",
                challenges="Notation",
                user_id=42,
            )

        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED
        assert outbox.pending() == ()


class TestReflectionInstrumentationNegative:
    """Reflection workflow must still succeed when analytics fails."""

    def test_dispatcher_unavailable(self) -> None:
        manager, session = _completed_with_pending()

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            side_effect=RuntimeError("dispatcher unavailable"),
        ):
            updated, summary = manager.capture(
                session,
                summary="Still learned",
                challenges="Still unclear",
                user_id=1,
            )

        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED

    def test_outbox_unavailable(self) -> None:
        class BoomOutbox(MemoryOutboxSink):
            def enqueue(self, event, *, payload_json: str = ""):  # type: ignore[override]
                raise RuntimeError("outbox unavailable")

        manager, session = _completed_with_pending()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=BoomOutbox(),
            registry=AnalyticsEventRegistry.phase_c_default(),
        )

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = manager.capture(
                session,
                summary="Still learned",
                challenges="Still unclear",
                user_id=1,
            )

        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED

    def test_registry_rejection(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        # Phase A registry rejects reflection event types.
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_a_default(),
        )

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated, summary = manager.capture(
                session,
                summary="Still learned",
                challenges="Still unclear",
                user_id=1,
            )

        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED
        assert outbox.pending() == ()

    def test_validation_failure(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with (
            patch(
                "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
                return_value=dispatcher,
            ),
            patch.object(
                AnalyticsEventValidator,
                "validate",
                return_value=ValidationResult(
                    ok=False, errors=("payload invalid",)
                ),
            ),
        ):
            updated, summary = manager.capture(
                session,
                summary="Still learned",
                challenges="Still unclear",
                user_id=1,
            )

        assert summary.is_captured
        assert updated.reflection.posture == ReflectionPosture.CAPTURED
        assert outbox.pending() == ()

    def test_failed_capture_does_not_emit(self) -> None:
        manager, session = _completed_with_pending()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.reflection_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            with pytest.raises(ReflectionRequired):
                manager.capture(
                    session,
                    summary="",
                    challenges="x",
                    user_id=1,
                )

        assert outbox.pending() == ()
