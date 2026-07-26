"""Integration + negative tests — Twin evolution observation.

Twin persistence must succeed even when analytics fails or is disabled.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

from app.application.twin_repository import (
    InMemoryTwinRepository,
    PersistAcknowledgement,
    TwinRepository,
    TwinScope,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState
from app.infrastructure.analytics.dispatcher import AnalyticsEventDispatcher
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.twin_events import TWIN_EVOLVED
from app.infrastructure.analytics.validator import (
    AnalyticsEventValidator,
    ValidationResult,
)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "42",
        "curriculum_id": "7",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 1),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    goals = overrides.pop(
        "goals",
        GoalState.create(target_completion_date=date(2026, 9, 1)),
    )
    knowledge = overrides.pop("knowledge", KnowledgeState.create())
    return DigitalTwin.create(
        identity,  # type: ignore[arg-type]
        goals=goals,  # type: ignore[arg-type]
        knowledge=knowledge,  # type: ignore[arg-type]
        **overrides,  # type: ignore[arg-type]
    )


def _scope(**overrides: object) -> TwinScope:
    defaults: dict[str, object] = {
        "student_id": "42",
        "sitting_id": "sep-2026",
        "curriculum_id": "7",
    }
    defaults.update(overrides)
    return TwinScope.create(**defaults)  # type: ignore[arg-type]


def _enabled_dispatcher(
    outbox: MemoryOutboxSink | None = None,
) -> AnalyticsEventDispatcher:
    sink = outbox if outbox is not None else MemoryOutboxSink()
    return AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=sink,
        registry=AnalyticsEventRegistry.phase_e_default(),
    )


class TestTwinEvolutionInstrumentationIntegration:
    def test_persist_birth_emits_when_flag_on(self) -> None:
        repo = InMemoryTwinRepository()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            ack = repo.persist_birth_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="birth-obs-1",
            )

        assert isinstance(ack, PersistAcknowledgement)
        assert len(outbox.pending()) == 1
        record = outbox.pending()[0]
        assert record.event_type == TWIN_EVOLVED
        assert "snapshot_hash" in record.payload_json
        assert "twin_snapshot_id" in record.payload_json
        assert "evolution_reason" in record.payload_json
        assert "knowledge" not in record.payload_json
        assert "twin_payload" not in record.payload_json

    def test_persist_successor_emits_when_flag_on(self) -> None:
        repo = InMemoryTwinRepository()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            birth = repo.persist_birth_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="birth-obs-2",
            )
            succ = repo.persist_successor_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="succ-obs-2",
            )

        assert isinstance(birth, PersistAcknowledgement)
        assert isinstance(succ, PersistAcknowledgement)
        assert len(outbox.pending()) == 2
        reasons = [
            r.payload_json for r in outbox.pending()
        ]
        assert any('"birth"' in p for p in reasons)
        assert any('"successor"' in p for p in reasons)

    def test_flag_off_persist_succeeds_without_emit(self) -> None:
        repo = InMemoryTwinRepository()
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_e_default(),
        )

        with patch(
            "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            ack = repo.persist_birth_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="birth-off-1",
            )

        assert isinstance(ack, PersistAcknowledgement)
        assert len(outbox.pending()) == 0

    def test_analytics_failure_does_not_break_persist(self) -> None:
        repo = InMemoryTwinRepository()
        broken = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=MemoryOutboxSink(),
            registry=AnalyticsEventRegistry.phase_e_default(),
            validator=AnalyticsEventValidator(AnalyticsEventRegistry.phase_e_default()),
        )

        with (
            patch(
                "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
                return_value=broken,
            ),
            patch.object(
                broken._validator,
                "validate",
                return_value=ValidationResult(ok=False, errors=("forced",)),
            ),
        ):
            ack = repo.persist_birth_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="birth-fail-1",
            )

        assert isinstance(ack, PersistAcknowledgement)
        assert ack.snapshot_id == "birth-fail-1"

    def test_non_numeric_student_id_skips_emit(self) -> None:
        repo = InMemoryTwinRepository()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)
        scope = _scope(student_id="student-42")
        twin = _twin(identity=_identity(student_id="student-42"))

        with patch(
            "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            ack = repo.persist_birth_twin(
                twin,
                scope=scope,
                snapshot_id="birth-skip-1",
            )

        assert isinstance(ack, PersistAcknowledgement)
        assert len(outbox.pending()) == 0

    def test_durable_persist_emits_when_flag_on(self, ctx) -> None:
        repo = TwinRepository()
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.twin_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            ack = repo.persist_birth_twin(
                _twin(),
                scope=_scope(),
                snapshot_id="birth-durable-obs-1",
            )

        assert isinstance(ack, PersistAcknowledgement)
        assert len(outbox.pending()) == 1
        assert outbox.pending()[0].event_type == TWIN_EVOLVED
