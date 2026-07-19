"""High-volume matrices for Student Experience production integration."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.journey import ExperienceJourneyAdapter
from app.infrastructure.adapters.mission import ExperienceMissionAdapter
from app.infrastructure.adapters.orchestrator import ExperienceOrchestratorAdapter
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.adapters.student_twin import ExperienceTwinAdapter
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.serialization import EventSerializer
from app.infrastructure.events.types.experience import EXPERIENCE_EVENT_TYPES
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from tests.infrastructure.adapters.student_experience.helpers import (
    LEARNERS,
    OPS,
    SURFACES,
)

SUBJECTS = tuple(f"exp-S{i}" for i in range(6))


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("event_type", EXPERIENCE_EVENT_TYPES)
def test_experience_event_identity_grid(learner_id, event_type):
    event = IntegrationEvent.create(
        event_type,
        {"student_id": learner_id},
        correlation_id=f"{learner_id}:{event_type}",
        source="experience_volume",
    )
    ser = EventSerializer()
    restored = ser.from_json(ser.to_json(event))
    assert restored.payload["student_id"] == learner_id
    assert restored.event_type == event_type


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("surface", SURFACES)
def test_surface_view_event_grid(learner_id, surface):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    composition.emit_surface_viewed(surface, learner_id)
    if surface in {"home", "journey", "history"}:
        types = {e.event_type for e in composition.events.published()}
        assert any(
            t.endswith("Viewed") or t == "StudentHomeViewed" for t in types
        )


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("op", OPS)
def test_projection_store_op_grid(learner_id, op):
    store = ExperienceProjectionStore(uow=UnitOfWork())
    twin = ExperienceTwinAdapter(store=store)
    adaptive = ExperienceAdaptiveAdapter(store=store)
    journey = ExperienceJourneyAdapter(store=store)
    mission = ExperienceMissionAdapter(store=store)
    orch = ExperienceOrchestratorAdapter(store=store)
    composition = StudentExperienceComposition(
        store=store,
        seed_demo_learners=False,
        learning_loop=None,
    )
    composition.twin = twin
    composition.adaptive = adaptive
    composition.journey = journey
    composition.mission = mission
    composition.orchestrator = orch
    composition.seed_learner(learner_id, demo=True)

    if op == "seed":
        assert twin.get_learner_summary(learner_id) is not None
    elif op == "read":
        assert adaptive.get_todays_recommendation(learner_id) is not None
        assert journey.get_topic_list(learner_id)
        assert mission.get_todays_session(learner_id) is not None
        assert orch.get_activity_status(learner_id) is not None
    elif op == "session":
        # Rebind mission hook for learning loop without full orchestrator.
        mission_local = ExperienceMissionAdapter(
            store=store,
            events=composition.events,
            on_session_started=composition._run_learning_loop,
        )
        composition.mission = mission_local
        result = mission_local.start_session(learner_id)
        assert result["status"] == "in_progress"
        assert result["session_id"]
    else:  # recalc
        twin_doc = store.get(store.twin, learner_id) or {"student_id": learner_id}
        ack = adaptive.recalculate_from_twin(learner_id, twin_payload=twin_doc)
        assert ack["next_action_authority"] is True
        assert ack["authority"] == "adaptive_decision_engine"


@pytest.mark.parametrize("learner_id", LEARNERS[:8])
@pytest.mark.parametrize("subject_id", SUBJECTS[:4])
def test_end_to_end_learning_loop_grid(learner_id, subject_id):
    composition = StudentExperienceComposition(
        seed_demo_learners=False,
        learning_loop=None,
    )
    sid = f"{learner_id}:{subject_id}"
    composition.seed_learner(sid, demo=True)
    service = composition.build_service()
    home_before = service.get_home(sid)
    assert home_before.has_recommendation is True
    handle = service.start_session(sid)
    assert handle.student_id == sid
    home_after = service.get_home(sid)
    assert home_after.student_id == sid
    history = service.get_history(sid)
    assert history.total_study_minutes >= 0
    types = {e.event_type for e in composition.events.published()}
    assert "LearningSessionStarted" in types
    assert "LearningSessionCompleted" in types


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
@pytest.mark.parametrize("subject_id", SUBJECTS[:3])
@pytest.mark.parametrize(
    "adapter_name",
    ("twin", "adaptive", "mission", "journey", "orchestrator"),
)
def test_adapter_read_authority_grid(learner_id, subject_id, adapter_name):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    sid = f"{learner_id}-{subject_id}"
    composition.seed_learner(sid, demo=True)
    if adapter_name == "twin":
        summary = composition.twin.get_readiness_summary(sid)
        assert summary is not None
        doc = composition.store.get(composition.store.twin, sid)
        assert doc["authority"] == "student_twin"
    elif adapter_name == "adaptive":
        rec = composition.adaptive.get_todays_recommendation(sid)
        assert rec is not None
        doc = composition.store.get(composition.store.adaptive, sid)
        assert doc["next_action_authority"] is True
    elif adapter_name == "mission":
        session = composition.mission.get_todays_session(sid)
        assert session is not None
        doc = composition.store.get(composition.store.mission, sid)
        assert doc["next_action_authority"] is False
    elif adapter_name == "journey":
        progress = composition.journey.get_journey_progress(sid)
        assert progress is not None
        doc = composition.store.get(composition.store.journey, sid)
        assert doc["authority"] == "learning_journey"
    else:
        status = composition.orchestrator.get_activity_status(sid)
        assert status is not None
        doc = composition.store.get(composition.store.activity, sid)
        assert doc["authority"] == "learning_orchestrator"


@pytest.mark.parametrize("learner_id", LEARNERS[:6])
@pytest.mark.parametrize("surface", SURFACES)
def test_dashboard_surface_grid(learner_id, surface):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    service = composition.build_service()
    dash = service.get_dashboard(learner_id, surface=surface)
    assert dash.workspace_id
    assert dash.student_id == learner_id
    assert dash.active_surface == surface
