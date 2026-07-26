"""Integration + negative tests — Journey progression observation.

Journey persistence / progression must succeed even when analytics fails.
Production durable Journey repository is deferred (ADR-026); tests exercise
the post-save observe helper contract.
"""

from __future__ import annotations

from unittest.mock import patch

from app.application.learning_journey.journey_observation import (
    observe_journey_progressed,
)
from app.domain.learning_journey.value_objects.journey_state import (
    JourneyTransitionEvent,
)
from app.infrastructure.analytics.dispatcher import AnalyticsEventDispatcher
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.journey_events import JOURNEY_PROGRESSED
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.validator import ValidationResult
from tests.application.learning_journey.helpers import (
    InMemoryJourneyRepository,
    make_journey,
)


def _enabled_dispatcher(
    outbox: MemoryOutboxSink | None = None,
) -> AnalyticsEventDispatcher:
    sink = outbox if outbox is not None else MemoryOutboxSink()
    return AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=sink,
        registry=AnalyticsEventRegistry.phase_e_default(),
    )


class TestJourneyProgressionObservationIntegration:
    def test_save_then_observe_emits_when_flag_on(self) -> None:
        repo = InMemoryJourneyRepository()
        journey = make_journey(learner_id="42").apply_transition(
            JourneyTransitionEvent.START_JOURNEY
        )
        repo.save(journey)

        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)
        with patch(
            "app.infrastructure.analytics.journey_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            observe_journey_progressed(
                journey,
                transition_id=JourneyTransitionEvent.START_JOURNEY.value,
            )

        assert len(outbox.pending()) == 1
        record = outbox.pending()[0]
        assert record.event_type == JOURNEY_PROGRESSED
        assert "journey_id" in record.payload_json
        assert "curriculum_node_id" in record.payload_json
        assert "transition_id" in record.payload_json
        assert "objectives" not in record.payload_json
        assert "recommendation" not in record.payload_json

    def test_flag_off_observe_is_noop(self) -> None:
        journey = make_journey(learner_id="42")
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_e_default(),
        )
        with patch(
            "app.infrastructure.analytics.journey_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            observe_journey_progressed(
                journey,
                transition_id="start_journey",
            )
        assert len(outbox.pending()) == 0

    def test_analytics_failure_does_not_raise(self) -> None:
        journey = make_journey(learner_id="42")
        broken = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=MemoryOutboxSink(),
            registry=AnalyticsEventRegistry.phase_e_default(),
        )
        with (
            patch(
                "app.infrastructure.analytics.journey_events.AnalyticsEventDispatcher",
                return_value=broken,
            ),
            patch.object(
                broken._validator,
                "validate",
                return_value=ValidationResult(ok=False, errors=("forced",)),
            ),
        ):
            observe_journey_progressed(
                journey,
                transition_id="start_journey",
            )

    def test_non_numeric_learner_skips_emit(self) -> None:
        journey = make_journey(learner_id="learner-1")
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)
        with patch(
            "app.infrastructure.analytics.journey_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            observe_journey_progressed(
                journey,
                transition_id="start_journey",
            )
        assert len(outbox.pending()) == 0
