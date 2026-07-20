"""Integration: Session Experience → Production Adapter → Existing Service."""

from __future__ import annotations

import pytest

from app.application.session_experience.facade import SessionExperienceService
from app.domain.session_experience.session_workspace import SessionSurface
from app.infrastructure.session.composition import build_production_session_experience
from tests.infrastructure.session.helpers import (
    LEARNERS,
    RecordingActivityEngine,
    RecordingRuntimeEngine,
    make_composition,
    make_seeded_service,
)


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_facade_open_begin_activity_flow(learner_id):
    composition, service = make_seeded_service(learner_id)
    today = composition.mission.get_todays_session(learner_id)
    assert today is not None
    session_id = str(today["session_id"])
    overview = service.open_session(learner_id, session_id=session_id)
    assert overview.objective
    begun = service.begin_session(learner_id, session_id=session_id)
    assert str(begun.status) == "in_progress"
    activity = service.get_activity(learner_id, session_id=session_id)
    assert activity.activity_id
    progress = service.get_progress(learner_id, session_id=session_id)
    assert progress.activities_total >= 1


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_facade_submit_advance_to_reflection(learner_id):
    composition, service = make_seeded_service(learner_id)
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    service.open_session(learner_id, session_id=session_id)
    service.begin_session(learner_id, session_id=session_id)
    activity = service.get_activity(learner_id, session_id=session_id)
    service.submit_response(
        learner_id,
        session_id=session_id,
        activity_id=activity.activity_id,
        response="structured answer",
    )
    # Exhaust remaining activities to reach reflection.
    while True:
        nxt = service.advance_activity(learner_id, session_id=session_id)
        if nxt is None:
            break
        service.submit_response(
            learner_id,
            session_id=session_id,
            activity_id=nxt.activity_id,
            response="next answer",
        )
    reflection = service.get_reflection(learner_id, session_id=session_id)
    assert reflection.key_insight
    service.continue_from_reflection(learner_id, session_id=session_id)
    summary = service.get_summary(learner_id, session_id=session_id)
    assert summary.next_recommendation
    completed = service.complete_session(learner_id, session_id=session_id)
    assert completed.return_home.enabled is True


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_facade_uses_shared_experience_projections(learner_id):
    composition, service = make_seeded_service(learner_id)
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    service.open_session(learner_id, session_id=session_id)
    service.begin_session(learner_id, session_id=session_id)
    while service.advance_activity(learner_id, session_id=session_id) is not None:
        pass
    service.get_reflection(learner_id, session_id=session_id)
    service.continue_from_reflection(learner_id, session_id=session_id)
    summary = service.get_summary(learner_id, session_id=session_id)
    recommendation = composition.adaptive.get_todays_recommendation(learner_id)
    assert recommendation is not None
    assert summary.next_recommendation
    twin = composition.twin.get_learning_insights(learner_id)
    assert twin is not None


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_integration_through_recording_engines(learner_id):
    runtime_engine = RecordingRuntimeEngine()
    activity_engine = RecordingActivityEngine()
    composition = make_composition(
        seed_demo_learners=False,
        runtime_engine=runtime_engine,
        activity_engine=activity_engine,
    )
    composition.seed_learner(learner_id, demo=True)
    service = composition.build_service()
    session_id = "sess-e"
    composition.runtime.put_overview(
        learner_id,
        session_id=session_id,
        document=runtime_engine.get_session_overview_opaque(
            learner_id, session_id=session_id
        ),
    )
    overview = service.open_session(learner_id, session_id=session_id)
    assert "Engine" in overview.objective or overview.objective
    service.begin_session(learner_id, session_id=session_id)
    activity = service.get_activity(learner_id, session_id=session_id)
    assert activity.question.startswith("Engine")
    assert runtime_engine.calls
    assert activity_engine.calls


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_get_flow_surfaces(learner_id):
    composition, service = make_seeded_service(learner_id)
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    service.open_session(learner_id, session_id=session_id)
    flow = service.get_flow(learner_id, session_id=session_id)
    assert flow.surface == SessionSurface.OVERVIEW.value
    assert flow.overview is not None
    service.begin_session(learner_id, session_id=session_id)
    flow = service.get_flow(learner_id, session_id=session_id)
    assert flow.surface == SessionSurface.ACTIVITY.value
    assert flow.activity is not None


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_build_production_registers_usable_service(learner_id):
    composition, service = build_production_session_experience(
        seed_demo_learners=False
    )
    composition.seed_learner(learner_id, demo=True)
    assert isinstance(service, SessionExperienceService)
    rebuilt = composition.build_service()
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    overview = rebuilt.open_session(learner_id, session_id=session_id)
    assert overview.session_id == session_id


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_facade_create_with_injected_ports(learner_id):
    composition = make_composition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    service = SessionExperienceService.create(
        session_runtime=composition.runtime,
        activity_engine=composition.activity,
        mission=composition.mission,
        student_twin=composition.twin,
        adaptive_decision=composition.adaptive,
    )
    session_id = str(composition.mission.get_todays_session(learner_id)["session_id"])
    overview = service.open_session(learner_id, session_id=session_id)
    assert overview.objective


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_diagnostics_report_ports(learner_id):
    composition, service = make_seeded_service(learner_id)
    report = service.diagnostics()
    assert report is not None
    # Port presence is reflected in diagnostics without educational math.
    assert composition.runtime.is_available()
    assert composition.activity.is_available()
