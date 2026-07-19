"""Port-contract and behavioural tests for Experience production adapters."""

from __future__ import annotations

import pytest

from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.application.student_experience.ports.learning_orchestrator_port import (
    LearningOrchestratorPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.journey import ExperienceJourneyAdapter
from app.infrastructure.adapters.mission import ExperienceMissionAdapter
from app.infrastructure.adapters.orchestrator import ExperienceOrchestratorAdapter
from app.infrastructure.adapters.student_twin import ExperienceTwinAdapter
from tests.infrastructure.adapters.student_experience.helpers import (
    LEARNERS,
    make_composition,
    make_seeded_service,
)

ADAPTERS = (
    (ExperienceTwinAdapter, StudentTwinPort),
    (ExperienceAdaptiveAdapter, AdaptiveDecisionPort),
    (ExperienceMissionAdapter, MissionPort),
    (ExperienceJourneyAdapter, LearningJourneyPort),
    (ExperienceOrchestratorAdapter, LearningOrchestratorPort),
)


@pytest.mark.parametrize("factory,port", ADAPTERS)
def test_experience_adapter_satisfies_protocol(factory, port):
    adapter = factory()
    assert isinstance(adapter, port)
    assert adapter.is_available() is True
    assert adapter.component_id
    assert adapter.component_version


@pytest.mark.parametrize("available", [True, False])
@pytest.mark.parametrize("factory,port", ADAPTERS)
def test_experience_adapter_availability(factory, port, available):
    adapter = factory()
    adapter.set_available(available)
    assert adapter.is_available() is available
    assert isinstance(adapter, port)


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_seeded_home_projection(learner_id):
    composition, service = make_seeded_service(learner_id)
    home = service.get_home(learner_id)
    assert home.student_id == learner_id
    assert home.has_recommendation is True
    assert home.exam_readiness is not None
    assert composition.adaptive.get_todays_recommendation(learner_id)


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_seeded_journey_projection(learner_id):
    _, service = make_seeded_service(learner_id)
    journey = service.get_journey(learner_id)
    assert journey.student_id == learner_id
    assert journey.current_topic is not None or journey.overall_progress_ratio >= 0


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_seeded_revision_projection(learner_id):
    _, service = make_seeded_service(learner_id)
    revision = service.get_revision(learner_id)
    assert revision.student_id == learner_id
    assert revision.has_revision is True


@pytest.mark.parametrize("learner_id", LEARNERS)
def test_seeded_history_and_profile(learner_id):
    _, service = make_seeded_service(learner_id)
    history = service.get_history(learner_id)
    profile = service.get_profile(learner_id)
    assert history.student_id == learner_id
    assert profile.student_id == learner_id
    assert history.total_study_minutes >= 0


@pytest.mark.parametrize("learner_id", LEARNERS[:5])
def test_mission_start_emits_session_and_updates_twin(learner_id):
    composition, service = make_seeded_service(learner_id)
    before = composition.twin.get_learning_insights(learner_id) or {}
    before_count = int(before.get("sessions_completed") or 0)
    handle = service.start_session(learner_id)
    assert handle.session_id
    assert handle.status.value == "in_progress"
    after = composition.twin.get_learning_insights(learner_id) or {}
    assert int(after.get("sessions_completed") or 0) >= before_count + 1
    types = {e.event_type for e in composition.events.published()}
    assert "LearningSessionStarted" in types
    assert "LearningSessionCompleted" in types
    assert "RecommendationAccepted" in types


@pytest.mark.parametrize("learner_id", LEARNERS[:4])
def test_adaptive_accept_dismiss(learner_id):
    composition = make_composition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    accepted = composition.adaptive.accept_recommendation(
        learner_id, decision_id="d1"
    )
    dismissed = composition.adaptive.dismiss_recommendation(
        learner_id, decision_id="d1"
    )
    assert accepted["accepted"] is True
    assert dismissed["dismissed"] is True
    types = {e.event_type for e in composition.events.published()}
    assert "RecommendationAccepted" in types
    assert "RecommendationDismissed" in types


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_orchestrator_activity_acknowledge(learner_id):
    composition = make_composition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    status = composition.orchestrator.get_activity_status(learner_id)
    assert status is not None
    ack = composition.orchestrator.acknowledge_activity(
        learner_id, activity_id="act-1"
    )
    assert ack["acknowledged"] is True


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
def test_persisted_workspace_registry(learner_id):
    composition, service = make_seeded_service(learner_id)
    workspace = service.open_workspace(learner_id, examination_label="Exam")
    loaded = composition.registry.get_workspace(workspace.workspace_id)
    assert loaded is not None
    assert loaded.student_id == learner_id
    again = composition.registry.get_workspace_for_student(learner_id)
    assert again is not None
    assert again.workspace_id == workspace.workspace_id
