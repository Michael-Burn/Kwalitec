"""Port-contract and behavioural tests for Session production adapters."""

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
from app.infrastructure.session.adaptive_adapter import SessionAdaptiveAdapter
from app.infrastructure.session.mission_adapter import SessionMissionAdapter
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.twin_adapter import SessionTwinAdapter
from tests.infrastructure.session.helpers import (
    LEARNERS,
    SESSIONS,
    RecordingActivityEngine,
    RecordingRuntimeEngine,
    make_composition,
)

ADAPTERS = (
    (SessionRuntimeAdapter, SessionRuntimePort),
    (SessionActivityAdapter, ActivityEnginePort),
    (SessionMissionAdapter, MissionPort),
    (SessionTwinAdapter, StudentTwinPort),
    (SessionAdaptiveAdapter, AdaptiveDecisionPort),
)


@pytest.mark.parametrize("factory,port", ADAPTERS)
def test_session_adapter_satisfies_protocol(factory, port):
    adapter = factory()
    assert isinstance(adapter, port)
    assert adapter.is_available() is True
    assert adapter.component_id
    assert adapter.component_version


@pytest.mark.parametrize("available", [True, False])
@pytest.mark.parametrize("factory,port", ADAPTERS)
def test_session_adapter_availability(factory, port, available):
    adapter = factory()
    adapter.set_available(available)
    assert adapter.is_available() is available
    assert isinstance(adapter, port)


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
@pytest.mark.parametrize("session_id", SESSIONS[:3])
def test_runtime_overview_and_begin(learner_id, session_id):
    runtime = SessionRuntimeAdapter()
    overview = runtime.get_session_overview(learner_id, session_id=session_id)
    assert overview is not None
    assert overview["session_id"] == session_id
    assert overview["objective"]
    begun = runtime.begin_session(learner_id, session_id=session_id)
    assert begun["status"] == "in_progress"
    snapshot = runtime.get_runtime_snapshot(learner_id, session_id=session_id)
    assert snapshot is not None
    assert snapshot["activities_total"] >= 1


@pytest.mark.parametrize("learner_id", LEARNERS[:4])
@pytest.mark.parametrize("session_id", SESSIONS[:2])
def test_runtime_reflection_completion_record(learner_id, session_id):
    runtime = SessionRuntimeAdapter()
    runtime.begin_session(learner_id, session_id=session_id)
    recorded = runtime.record_response(
        learner_id,
        session_id=session_id,
        activity_id="act-1",
        response="an answer",
    )
    assert recorded["recorded"] is True
    reflection = runtime.get_reflection(learner_id, session_id=session_id)
    assert reflection is not None
    assert reflection["key_insight"]
    completed = runtime.complete_session(learner_id, session_id=session_id)
    assert completed["status"] == "completed"
    summary = runtime.get_completion_summary(learner_id, session_id=session_id)
    assert summary is not None
    assert summary["activities_completed"] >= 0


@pytest.mark.parametrize("learner_id", LEARNERS[:4])
def test_runtime_delegates_to_engine(learner_id):
    engine = RecordingRuntimeEngine()
    runtime = SessionRuntimeAdapter(runtime_engine=engine)
    overview = runtime.get_session_overview(learner_id, session_id="sess-e")
    assert overview["objective"] == "Engine objective"
    begun = runtime.begin_session(learner_id, session_id="sess-e")
    assert begun["engine"] is True
    assert runtime.record_response(
        learner_id, session_id="sess-e", activity_id="a1", response="x"
    )["engine"] is True
    assert runtime.complete_session(learner_id, session_id="sess-e")["engine"] is True
    assert engine.calls


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
@pytest.mark.parametrize("session_id", SESSIONS[:2])
def test_activity_current_submit_advance(learner_id, session_id):
    activity = SessionActivityAdapter(activity_count=3)
    current = activity.get_current_activity(learner_id, session_id=session_id)
    assert current is not None
    assert current["activity_id"]
    submitted = activity.submit_response(
        learner_id,
        session_id=session_id,
        activity_id=str(current["activity_id"]),
        response="my answer",
    )
    assert submitted["phase"] == "explained"
    nxt = activity.advance_activity(learner_id, session_id=session_id)
    assert nxt is not None
    progress = activity.get_activity_progress(learner_id, session_id=session_id)
    assert progress is not None
    assert progress["activities_total"] == 3


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_activity_sequence_exhausts(learner_id):
    activity = SessionActivityAdapter(activity_count=2)
    session_id = "sess-ex"
    assert activity.get_current_activity(learner_id, session_id=session_id)
    activity.advance_activity(learner_id, session_id=session_id)
    last = activity.advance_activity(learner_id, session_id=session_id)
    assert last is None


@pytest.mark.parametrize("learner_id", LEARNERS[:4])
def test_activity_delegates_to_engine(learner_id):
    engine = RecordingActivityEngine()
    activity = SessionActivityAdapter(activity_engine=engine)
    current = activity.get_current_activity(learner_id, session_id="s1")
    assert current["question"].startswith("Engine")
    activity.submit_response(
        learner_id, session_id="s1", activity_id="eng-1", response="ans"
    )
    activity.advance_activity(learner_id, session_id="s1")
    progress = activity.get_activity_progress(learner_id, session_id="s1")
    assert progress["activities_total"] == 2
    assert "current" in engine.calls


@pytest.mark.parametrize("learner_id", LEARNERS[:8])
def test_mission_todays_session_and_status(learner_id):
    mission = SessionMissionAdapter(seed_demo=True)
    today = mission.get_todays_session(learner_id)
    assert today is not None
    assert today["session_id"]
    assert today.get("next_action_authority") is not True
    status = mission.get_session_status(
        learner_id, session_id=str(today["session_id"])
    )
    assert status is not None
    assert status["session_id"] == today["session_id"]


@pytest.mark.parametrize("learner_id", LEARNERS[:8])
def test_twin_readiness_and_insights(learner_id):
    twin = SessionTwinAdapter(seed_demo=True)
    readiness = twin.get_readiness_summary(learner_id)
    assert readiness is not None
    assert readiness.get("exam_readiness") is not None
    insights = twin.get_learning_insights(learner_id)
    assert insights is not None


@pytest.mark.parametrize("learner_id", LEARNERS[:8])
def test_adaptive_todays_recommendation(learner_id):
    adaptive = SessionAdaptiveAdapter(seed_demo=True)
    recommendation = adaptive.get_todays_recommendation(learner_id)
    assert recommendation is not None
    assert recommendation.get("title") or recommendation.get("topic_title")


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_mission_twin_adaptive_reuse_delegates(learner_id):
    composition = make_composition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    assert composition.mission.delegate is not None
    assert composition.twin.delegate is not None
    assert composition.adaptive.delegate is not None
    assert composition.mission.get_todays_session(learner_id)
    assert composition.twin.get_readiness_summary(learner_id)
    assert composition.adaptive.get_todays_recommendation(learner_id)
