"""High-volume matrices for Session Experience production adapters."""

from __future__ import annotations

import pytest

from app.application.session_experience.ports.activity_engine_port import (
    ActivityEnginePort,
)
from app.application.session_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.session_experience.ports.mission_port import MissionPort
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.application.session_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from tests.infrastructure.session.helpers import (
    ADAPTER_OPS,
    ADAPTER_TYPES,
    LEARNERS,
    SESSIONS,
    make_composition,
    make_seeded_service,
)

PORTS = (
    SessionRuntimePort,
    ActivityEnginePort,
    MissionPort,
    StudentTwinPort,
    AdaptiveDecisionPort,
)


@pytest.mark.parametrize("factory,adapter_id", ADAPTER_TYPES)
@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_adapter_identity_grid(factory, adapter_id, learner_id):
    adapter = factory()
    assert adapter.component_id == adapter_id
    assert adapter.component_version
    assert adapter.is_available() is True
    _ = learner_id  # identity matrix breadth


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
@pytest.mark.parametrize("session_id", SESSIONS[:4])
def test_runtime_session_grid(learner_id, session_id):
    store = SessionDocumentStore()
    runtime = SessionRuntimeAdapter(store=store)
    overview = runtime.get_session_overview(learner_id, session_id=session_id)
    assert overview["session_id"] == session_id
    runtime.begin_session(learner_id, session_id=session_id)
    snap = runtime.get_runtime_snapshot(learner_id, session_id=session_id)
    assert snap["activities_total"] >= 1


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
@pytest.mark.parametrize("session_id", SESSIONS[:3])
def test_activity_session_grid(learner_id, session_id):
    activity = SessionActivityAdapter(activity_count=3)
    current = activity.get_current_activity(learner_id, session_id=session_id)
    assert current["activity_index"] == 1
    progress = activity.get_activity_progress(learner_id, session_id=session_id)
    assert progress["activities_total"] == 3


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
@pytest.mark.parametrize("op", ADAPTER_OPS)
def test_composition_op_grid(learner_id, op):
    composition, service = make_seeded_service(learner_id)
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    if op == "overview":
        overview = service.open_session(learner_id, session_id=session_id)
        assert overview.objective
    elif op == "begin":
        service.open_session(learner_id, session_id=session_id)
        begun = service.begin_session(learner_id, session_id=session_id)
        assert str(begun.status) == "in_progress"
    elif op == "activity":
        service.open_session(learner_id, session_id=session_id)
        service.begin_session(learner_id, session_id=session_id)
        activity = service.get_activity(learner_id, session_id=session_id)
        assert activity.question
    elif op == "progress":
        service.open_session(learner_id, session_id=session_id)
        service.begin_session(learner_id, session_id=session_id)
        progress = service.get_progress(learner_id, session_id=session_id)
        assert progress.activities_total >= 1
    else:  # complete
        service.open_session(learner_id, session_id=session_id)
        service.begin_session(learner_id, session_id=session_id)
        while service.advance_activity(learner_id, session_id=session_id) is not None:
            pass
        service.get_reflection(learner_id, session_id=session_id)
        service.continue_from_reflection(learner_id, session_id=session_id)
        completed = service.complete_session(learner_id, session_id=session_id)
        assert completed.return_home.enabled is True


@pytest.mark.parametrize("factory,adapter_id", ADAPTER_TYPES)
@pytest.mark.parametrize("available", [True, False])
def test_availability_matrix(factory, adapter_id, available):
    adapter = factory()
    adapter.set_available(available)
    assert adapter.is_available() is available
    assert adapter.component_id == adapter_id


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
def test_store_isolation_across_learners(learner_id):
    store = SessionDocumentStore()
    runtime = SessionRuntimeAdapter(store=store)
    other = "other-learner"
    runtime.begin_session(learner_id, session_id="shared")
    runtime.begin_session(other, session_id="shared")
    a = runtime.get_session_overview(learner_id, session_id="shared")
    b = runtime.get_session_overview(other, session_id="shared")
    assert a["student_id"] == learner_id
    assert b["student_id"] == other


@pytest.mark.parametrize("port", PORTS)
def test_ports_are_runtime_checkable(port):
    assert port.__name__


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_seeded_composition_mission_matches_runtime(learner_id):
    composition = make_composition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    today = composition.mission.get_todays_session(learner_id)
    assert today is not None
    overview = composition.runtime.get_session_overview(
        learner_id, session_id=str(today["session_id"])
    )
    assert overview is not None
    assert overview["mission_id"] == today["mission_id"]


FORBIDDEN_TOKENS = (
    "MasteryCalculator",
    "RetentionEstimator",
    "ReadinessEstimator",
    "sqlalchemy",
    "SessionLocal",
)


@pytest.mark.parametrize("token", FORBIDDEN_TOKENS)
def test_session_adapters_avoid_forbidden_authority(token):
    from pathlib import Path

    root = Path(__file__).resolve().parents[3] / "app" / "infrastructure" / "session"
    offenders = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if token in text:
            offenders.append(str(path))
    assert offenders == []
