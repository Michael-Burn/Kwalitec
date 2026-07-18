"""Shared helpers for Mission Adapter application tests."""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.application.mission_adapter.adapter import MissionAdapter
from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.exceptions import EngineUnavailable
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)

NOW = datetime(2026, 7, 18, 14, 0, tzinfo=UTC)


class FakeEngine:
    """Deterministic MissionEnginePort double for adapter tests."""

    def __init__(
        self,
        *,
        engine_id: str,
        engine_version: str = "1.0",
        available: bool = True,
        journey_id: str = "journey-1",
        topic_id: str = "topic-a",
        session_id: str = "session-1",
        effort: str = "medium",
        mission_type: str = "today",
        is_revision: bool = False,
        sequence_index: int = 0,
        explanation_keys: tuple[str, ...] = ("why", "what"),
        fail_ops: frozenset[str] | set[str] | None = None,
        call_log: list[str] | None = None,
    ) -> None:
        self._engine_id = engine_id
        self._engine_version = engine_version
        self._available = available
        self._journey_id = journey_id
        self._topic_id = topic_id
        self._session_id = session_id
        self._effort = effort
        self._mission_type = mission_type
        self._is_revision = is_revision
        self._sequence_index = sequence_index
        self._explanation_keys = explanation_keys
        self._fail_ops = frozenset(fail_ops or ())
        self.calls: list[str] = call_log if call_log is not None else []

    @property
    def engine_id(self) -> str:
        return self._engine_id

    @property
    def engine_version(self) -> str:
        return self._engine_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def _snapshot(self, request: AdapterRequest, op: str) -> MissionSnapshot:
        self.calls.append(op)
        if op in self._fail_ops:
            raise EngineUnavailable(f"{self._engine_id} failed on {op}")
        mid = request.mission_id or f"{self._engine_id}-mission"
        return MissionSnapshot(
            mission_id=mid,
            learner_id=request.learner_id,
            journey_id=request.journey_id or self._journey_id,
            topic_id=request.topic_id or self._topic_id,
            session_id=request.session_id or self._session_id,
            effort=self._effort,
            mission_type=self._mission_type,
            is_revision=self._is_revision,
            sequence_index=self._sequence_index,
            explanation_keys=self._explanation_keys,
            engine_id=self._engine_id,
            engine_version=self._engine_version,
            metadata=MappingProxyType({"op": op}),
        )

    def generate_mission(self, request: AdapterRequest) -> MissionSnapshot:
        return self._snapshot(request, "generate_mission")

    def resume_mission(self, request: AdapterRequest) -> MissionSnapshot:
        return self._snapshot(request, "resume_mission")

    def pause_mission(self, request: AdapterRequest) -> MissionSnapshot:
        return self._snapshot(request, "pause_mission")

    def skip_mission(self, request: AdapterRequest) -> MissionSnapshot:
        return self._snapshot(request, "skip_mission")

    def archive_mission(self, request: AdapterRequest) -> MissionSnapshot:
        return self._snapshot(request, "archive_mission")


def make_request(
    *,
    operation: str = "generate_mission",
    learner_id: str = "learner-1",
    mission_id: str | None = None,
    journey_id: str | None = "journey-1",
    topic_id: str | None = "topic-a",
    session_id: str | None = "session-1",
    organisation_id: str | None = None,
    cohort_id: str | None = None,
    environment: str = "production",
    correlation_id: str | None = "corr-1",
) -> AdapterRequest:
    return AdapterRequest(
        operation=operation,
        learner_id=learner_id,
        mission_id=mission_id,
        journey_id=journey_id,
        topic_id=topic_id,
        session_id=session_id,
        organisation_id=organisation_id,
        cohort_id=cohort_id,
        environment=environment,
        correlation_id=correlation_id,
    )


def make_v1(**kwargs) -> FakeEngine:
    defaults = {"engine_id": "v1", "engine_version": "v1-1.0"}
    defaults.update(kwargs)
    return FakeEngine(**defaults)


def make_v2(**kwargs) -> FakeEngine:
    defaults = {"engine_id": "v2", "engine_version": "v2-1.0"}
    defaults.update(kwargs)
    return FakeEngine(**defaults)


def make_adapter(
    *,
    v1: FakeEngine | None = None,
    v2: FakeEngine | None = None,
    phase: MigrationPhase = MigrationPhase.LEGACY_ONLY,
    global_v2_enabled: bool = False,
    allowed_cohorts: set[str] | None = None,
    allowed_organisations: set[str] | None = None,
    allowed_environments: set[str] | None = None,
) -> MissionAdapter:
    migration = MigrationManager(initial_phase=phase)
    return MissionAdapter.create(
        v1_engine=v1 if v1 is not None else make_v1(),
        v2_engine=v2,
        global_v2_enabled=global_v2_enabled,
        migration_manager=migration,
        allowed_cohorts=allowed_cohorts,
        allowed_organisations=allowed_organisations,
        allowed_environments=allowed_environments,
        clock=lambda: NOW,
    )
