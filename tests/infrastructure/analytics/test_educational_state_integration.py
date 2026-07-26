"""Integration + negative tests — Educational State snapshot observation.

Educational State assembly must succeed even when analytics fails or is disabled.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.application.educational_state import (
    EducationalStateService,
    reset_snapshot_observation_state,
)
from app.infrastructure.analytics.dispatcher import AnalyticsEventDispatcher
from app.infrastructure.analytics.educational_state_events import (
    EDUCATIONAL_STATE_SNAPSHOT,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.validator import (
    AnalyticsEventValidator,
    ValidationResult,
)
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeTwinPort,
)


@pytest.fixture(autouse=True)
def _reset_material_change_memory() -> None:
    reset_snapshot_observation_state()
    yield
    reset_snapshot_observation_state()


def _service() -> EducationalStateService:
    return EducationalStateService(
        student_twin=FakeTwinPort(),
        adaptive_decision=FakeAdaptivePort(),
        mission=FakeMissionPort(),
        learning_journey=FakeJourneyPort(),
    )


def _enabled_dispatcher(
    outbox: MemoryOutboxSink | None = None,
) -> AnalyticsEventDispatcher:
    sink = outbox if outbox is not None else MemoryOutboxSink()
    return AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=sink,
        registry=AnalyticsEventRegistry.phase_d_default(),
    )


class TestEducationalStateInstrumentationIntegration:
    def test_load_emits_snapshot_when_flag_on(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert snapshot.twin_available is True
        assert len(outbox.pending()) == 1
        record = outbox.pending()[0]
        assert record.event_type == EDUCATIONAL_STATE_SNAPSHOT
        assert "content_hash" in record.payload_json
        assert "snapshot_id" in record.payload_json
        assert "learner_summary" not in record.payload_json
        assert "readiness_summary" not in record.payload_json
        assert "recommendation" not in record.payload_json

    def test_cache_hit_does_not_re_emit(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            first = service.load("42")
            second = service.load("42")

        assert first is second
        assert len(outbox.pending()) == 1

    def test_identical_reassemble_skips_emit_material_gate(self) -> None:
        """Same content hash after clear_cache must not re-emit."""
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            service.load("42")
            service.clear_cache()
            service.load("42")

        assert len(outbox.pending()) == 1

    def test_material_change_emits_again(self) -> None:
        twin = FakeTwinPort()
        service = EducationalStateService(
            student_twin=twin,
            adaptive_decision=FakeAdaptivePort(),
            mission=FakeMissionPort(),
            learning_journey=FakeJourneyPort(),
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            service.load("42")
            service.clear_cache()
            with patch.object(
                twin,
                "get_readiness_summary",
                return_value={
                    "examination_label": "CPA",
                    "exam_countdown_days": 10,
                    "exam_readiness": 0.95,
                    "readiness_score": 0.95,
                },
            ):
                service.load("42")

        assert len(outbox.pending()) == 2

    def test_non_numeric_student_id_skips_emit(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            snapshot = service.load("stu-1")

        assert snapshot.student_id == "stu-1"
        assert outbox.pending() == ()

    def test_flag_off_load_succeeds_zero_writes(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_d_default(),
        )

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert snapshot.twin_available is True
        assert outbox.pending() == ()


class TestEducationalStateInstrumentationNegative:
    """Educational State assembly must still succeed when analytics fails."""

    def test_dispatcher_unavailable(self) -> None:
        service = _service()

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            side_effect=RuntimeError("dispatcher unavailable"),
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert snapshot.twin_available is True

    def test_hash_generation_failure(self) -> None:
        service = _service()

        with patch(
            "app.application.educational_state.content_hash"
            ".compute_educational_state_content_hash",
            side_effect=RuntimeError("hash boom"),
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert snapshot.twin_available is True

    def test_outbox_unavailable(self) -> None:
        class BoomOutbox(MemoryOutboxSink):
            def enqueue(self, event, *, payload_json: str = ""):  # type: ignore[override]
                raise RuntimeError("outbox unavailable")

        service = _service()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=BoomOutbox(),
            registry=AnalyticsEventRegistry.phase_d_default(),
        )

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert snapshot.twin_available is True

    def test_registry_rejection(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_a_default(),
        )

        with patch(
            "app.infrastructure.analytics.educational_state_events"
            ".AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert outbox.pending() == ()

    def test_validation_failure(self) -> None:
        service = _service()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with (
            patch(
                "app.infrastructure.analytics.educational_state_events"
                ".AnalyticsEventDispatcher",
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
            snapshot = service.load("42")

        assert snapshot.student_id == "42"
        assert outbox.pending() == ()
