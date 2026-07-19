"""Factory / production port wiring tests."""

from __future__ import annotations

from app.application.student_experience.student_experience_service import (
    StudentExperienceService,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.presentation.student.factory import (
    build_experience_service,
    get_experience_service,
    set_experience_service,
)
from tests.application.student_experience.helpers import make_experience


def test_build_with_production_adapters():
    service = build_experience_service(use_production_adapters=True)
    assert isinstance(service, StudentExperienceService)


def test_production_seeded_home():
    composition, _service = build_production_experience(seed_demo_learners=False)
    composition.seed_learner("prod-user", demo=True)
    home = composition.build_service().get_home("prod-user")
    assert home.student_id == "prod-user"
    assert home.has_recommendation is True


def test_build_without_production_adapters_allows_none():
    service = build_experience_service(use_production_adapters=False)
    assert isinstance(service, StudentExperienceService)


def test_set_and_get_experience_service(experience_app):
    custom = make_experience()
    set_experience_service(custom, app=experience_app)
    with experience_app.app_context():
        assert get_experience_service() is custom


def test_production_mission_start():
    composition, service = build_production_experience(seed_demo_learners=False)
    composition.seed_learner("u1", demo=True)
    handle = service.start_session("u1", mission_id="m1")
    assert handle.status.value == "in_progress"
    assert handle.mission_id == "m1"


def test_explicit_port_overrides_skip_production():
    custom = make_experience()
    service = build_experience_service(
        student_twin=custom._ports["student_twin"],
        adaptive_decision=custom._ports["adaptive_decision"],
        mission=custom._ports["mission"],
        learning_journey=custom._ports["learning_journey"],
        learning_orchestrator=custom._ports["learning_orchestrator"],
    )
    home = service.get_home("stu-1")
    assert home.has_recommendation is True
