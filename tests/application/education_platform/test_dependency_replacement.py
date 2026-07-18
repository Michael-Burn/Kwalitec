"""Dependency replacement and hot-swap behaviour tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.exceptions import DependencyError
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_platform,
    make_request,
)


def test_replace_curriculum_changes_subject():
    platform = make_platform()
    platform.replace_port(
        "curriculum",
        FakeCurriculum(subject_id="subject-z", topic_ids=("tz",)),
    )
    resp = platform.generate_subject(make_request(subject_id=None))
    assert resp.subject_plan.subject_id == "subject-z"
    assert resp.subject_plan.topic_ids == ("tz",)


def test_replace_blueprint_changes_session_count():
    platform = make_platform()
    platform.replace_port("blueprint", FakeBlueprint(session_count=4))
    resp = platform.generate_learning_sessions(make_request())
    assert len(resp.sessions) == 4


def test_replace_journey_changes_id():
    platform = make_platform()
    platform.replace_port("journey", FakeJourney(journey_id="journey-x"))
    resp = platform.generate_journey(make_request())
    assert resp.journey_id == "journey-x"


def test_replace_mission_changes_type():
    platform = make_platform()
    platform.replace_port("mission", FakeMission(mission_type="deferred"))
    resp = platform.generate_daily_missions(make_request())
    assert resp.missions[0].mission_type == "deferred"


def test_replace_activity_changes_ids():
    platform = make_platform()
    platform.replace_port(
        "activity", FakeActivity(activity_ids=("only-one",))
    )
    resp = platform.generate_learning_activities(make_request())
    assert len(resp.activity_ids) == 1
    assert resp.activity_ids[0].endswith("only-one")


def test_replace_session_topic():
    platform = make_platform()
    platform.replace_port("session", FakeSession(topic_id="topic-z"))
    resp = platform.generate_learning_sessions(
        make_request(topic_id=None)
    )
    assert resp.sessions[0].topic_id == "topic-z"


def test_replace_unknown_raises():
    platform = make_platform()
    with pytest.raises(DependencyError):
        platform.replace_port("ghost", FakeCurriculum())


def test_replace_then_health_reflects_version():
    platform = make_platform()
    platform.replace_port(
        "curriculum", FakeCurriculum(component_version="8.0.0")
    )
    health = platform.health_status()
    assert health["components"]["curriculum"]["component_version"] == "8.0.0"


def test_replace_unavailable_degrades_health():
    platform = make_platform()
    platform.replace_port("mission", FakeMission(available=False))
    health = platform.health_status()
    assert health["platform_status"] == "unhealthy"
    assert health["components"]["mission"]["available"] is False


def test_sequential_replacements():
    platform = make_platform()
    platform.replace_port("blueprint", FakeBlueprint(blueprint_id="bp-a"))
    r1 = platform.generate_journey(make_request())
    platform.replace_port("blueprint", FakeBlueprint(blueprint_id="bp-b"))
    r2 = platform.generate_journey(make_request())
    assert r1.blueprint_id == "bp-a"
    assert r2.blueprint_id == "bp-b"


@pytest.mark.parametrize(
    "name,factory",
    [
        ("curriculum", FakeCurriculum),
        ("blueprint", FakeBlueprint),
        ("journey", FakeJourney),
        ("session", FakeSession),
        ("activity", FakeActivity),
        ("mission", FakeMission),
    ],
)
def test_replace_each_port_keeps_platform_usable(name, factory):
    platform = make_platform()
    platform.replace_port(name, factory())
    resp = platform.validate_platform()
    assert resp.success
    assert resp.validation_passed is True
