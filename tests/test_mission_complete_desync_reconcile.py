"""Mission-complete reverse desync self-heal (failed_open after accepted evidence).

When session UX closes as completed but the mission-complete write fails open,
the durable ``mission_complete_status=failed_open`` signal must be reconciled
on the next Home touchpoint — without re-running evidence acceptance.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.application.educational_runtime_engine.exceptions import (
    MissionInstanceNotFound,
)
from app.application.founder_validation.telemetry import DEFAULT_FV_TELEMETRY
from app.application.learning_session.runtime_phase import RuntimePhase
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore


@pytest.fixture(autouse=True)
def _clear_fv_telemetry():
    DEFAULT_FV_TELEMETRY.clear()
    yield
    DEFAULT_FV_TELEMETRY.clear()


def _fv_kinds() -> list[str]:
    with DEFAULT_FV_TELEMETRY._lock:
        return [e.kind for e in DEFAULT_FV_TELEMETRY._events]


def _seed_desync(
    store: SessionDocumentStore,
    *,
    session_id: str = "sess-desync-1",
    student_id: str = "42",
    mission_instance_id: str = "mid-desync-1",
    package_id: str = "pkg-desync-1",
    may_advance_progress: bool = True,
) -> LearningSessionPersistenceAdapter:
    persistence = LearningSessionPersistenceAdapter(store=store)
    handle = {
        "session_id": session_id,
        "student_id": student_id,
        "topic_id": "topic-1",
        "mission_instance_id": mission_instance_id,
        "status": "completed",
        "phase": RuntimePhase.COMPLETED.value,
        "evidence_disposition": "accepted",
        "evidence_package_id": package_id,
        "mission_completed": False,
        "mission_complete_status": "failed_open",
        "progress_advanced": False,
        "twin_updated": False,
    }
    store.save("lsr.handle", session_id, handle)
    store.save(
        "lsr.evidence_package",
        session_id,
        {
            "package_id": package_id,
            "validation": {
                "disposition": "accepted",
                "lifecycle_state": "accepted",
                "may_complete_session": True,
                "may_complete_mission": True,
                "may_advance_progress": may_advance_progress,
                "may_update_twin": False,
                "reason": "accepted_for_test",
                "student_explanation": "ok",
            },
            "observations": [
                {"type_id": "practice_correct", "observation_id": "obs-1"},
            ],
        },
    )
    return persistence


class TestMissionCompleteDesyncReconcileSuccess:
    def test_failed_open_desync_heals_on_reconcile_touchpoint(self):
        store = SessionDocumentStore()
        persistence = _seed_desync(store)
        package_before = persistence.load_evidence_package(
            session_id="sess-desync-1"
        )

        completer = MagicMock()
        completer.complete_mission.return_value = {"ok": True}
        engine = LearningSessionRuntimeEngine(
            persistence=persistence,
            mission_completer=completer,
        )

        results = engine.reconcile_mission_complete_desyncs(student_id="42")

        assert len(results) == 1
        assert results[0]["healed"] is True
        assert results[0]["mission_completed"] is True
        assert results[0]["status"] == "completed"

        healed = persistence.load(session_id="sess-desync-1")
        assert healed is not None
        assert healed["mission_completed"] is True
        assert healed["mission_complete_status"] == "completed"
        assert healed["evidence_disposition"] == "accepted"

        package_after = persistence.load_evidence_package(
            session_id="sess-desync-1"
        )
        assert package_after == package_before

        completer.complete_mission.assert_called_once()
        kwargs = completer.complete_mission.call_args.kwargs
        assert kwargs["user_id"] == 42
        assert kwargs["mission_instance_id"] == "mid-desync-1"
        assert kwargs["evidence_package_id"] == "pkg-desync-1"

        # Second touchpoint: no longer desynced, no infinite retry.
        second = engine.reconcile_mission_complete_desyncs(student_id="42")
        assert second == []
        assert completer.complete_mission.call_count == 1


class TestMissionCompleteDesyncReconcilePermanent:
    def test_missing_mission_becomes_stable_terminal_not_limbo(self):
        store = SessionDocumentStore()
        persistence = _seed_desync(store)
        completer = MagicMock()
        completer.complete_mission.side_effect = MissionInstanceNotFound(
            "mid-desync-1"
        )
        engine = LearningSessionRuntimeEngine(
            persistence=persistence,
            mission_completer=completer,
        )

        results = engine.reconcile_mission_complete_desyncs(student_id="42")

        assert len(results) == 1
        assert results[0]["healed"] is False
        assert results[0]["mission_completed"] is False
        assert results[0]["status"] == "failed_permanent_mission_missing"

        terminal = persistence.load(session_id="sess-desync-1")
        assert terminal is not None
        assert terminal["mission_completed"] is False
        assert (
            terminal["mission_complete_status"]
            == "failed_permanent_mission_missing"
        )
        assert terminal["evidence_disposition"] == "accepted"

        # Permanent terminal is not selected for further retries.
        second = engine.reconcile_mission_complete_desyncs(student_id="42")
        assert second == []
        assert completer.complete_mission.call_count == 1


class TestMissionCompleteDesyncReconcileObservability:
    def test_success_and_abandon_emit_distinct_fv_signals(self):
        store = SessionDocumentStore()
        persistence = _seed_desync(store, session_id="sess-ok")
        completer_ok = MagicMock()
        completer_ok.complete_mission.return_value = {"ok": True}
        engine_ok = LearningSessionRuntimeEngine(
            persistence=persistence,
            mission_completer=completer_ok,
        )
        engine_ok.reconcile_mission_complete_desyncs(student_id="42")
        assert "mission_complete_desync_reconciled" in _fv_kinds()

        DEFAULT_FV_TELEMETRY.clear()
        store_fail = SessionDocumentStore()
        persistence_fail = _seed_desync(
            store_fail,
            session_id="sess-gone",
            mission_instance_id="mid-gone",
        )
        completer_fail = MagicMock()
        completer_fail.complete_mission.side_effect = MissionInstanceNotFound(
            "mid-gone"
        )
        engine_fail = LearningSessionRuntimeEngine(
            persistence=persistence_fail,
            mission_completer=completer_fail,
        )
        engine_fail.reconcile_mission_complete_desyncs(student_id="42")
        assert "mission_complete_desync_reconcile_abandoned" in _fv_kinds()
        assert "mission_complete_desync_reconciled" not in _fv_kinds()


class TestFindMissionCompleteDesyncsSignal:
    def test_rejected_evidence_is_not_a_desync_candidate(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        store.save(
            "lsr.handle",
            "sess-rejected",
            {
                "session_id": "sess-rejected",
                "student_id": "42",
                "status": "completed",
                "phase": RuntimePhase.COMPLETED.value,
                "evidence_disposition": "rejected",
                "mission_completed": False,
                "mission_complete_status": "failed_open",
                "mission_instance_id": "mid-x",
            },
        )
        assert (
            persistence.find_mission_complete_desyncs(student_id="42") == []
        )

    def test_never_accepted_without_failed_open_is_not_selected(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        store.save(
            "lsr.handle",
            "sess-plain",
            {
                "session_id": "sess-plain",
                "student_id": "42",
                "status": "completed",
                "phase": RuntimePhase.COMPLETED.value,
                "evidence_disposition": "accepted",
                "mission_completed": False,
                "mission_complete_status": "",
                "mission_instance_id": "mid-x",
            },
        )
        assert (
            persistence.find_mission_complete_desyncs(student_id="42") == []
        )
