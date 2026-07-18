"""Port protocol structural tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.ports.activity_port import ActivityPort
from app.application.education_platform.ports.blueprint_port import BlueprintPort
from app.application.education_platform.ports.curriculum_port import CurriculumPort
from app.application.education_platform.ports.journey_port import JourneyPort
from app.application.education_platform.ports.mission_port import MissionPort
from app.application.education_platform.ports.session_port import SessionPort
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_request,
)


@pytest.mark.parametrize(
    "protocol,instance",
    [
        (CurriculumPort, FakeCurriculum()),
        (BlueprintPort, FakeBlueprint()),
        (JourneyPort, FakeJourney()),
        (SessionPort, FakeSession()),
        (ActivityPort, FakeActivity()),
        (MissionPort, FakeMission()),
    ],
)
def test_fake_satisfies_protocol(protocol, instance):
    assert isinstance(instance, protocol)


def test_curriculum_port_methods():
    port = FakeCurriculum()
    req = make_request()
    plan = port.resolve_subject(req)
    assert plan.subject_id == "subject-1"
    assert port.topic_available("topic-a")
    assert not port.topic_available("missing")
    assert port.ordered_topic_ids() == ("topic-a", "topic-b")
    assert port.is_available()
    assert port.component_id == "curriculum"


def test_blueprint_port_methods():
    port = FakeBlueprint(session_count=3)
    req = make_request()
    assert port.select_blueprint_id(req) == "bp-standard"
    assert port.estimate_session_count(req) == 3


def test_journey_port_methods():
    port = FakeJourney()
    req = make_request()
    jid = port.create_journey(req)
    assert port.journey_exists(jid)


def test_session_port_methods():
    port = FakeSession()
    sessions = port.plan_sessions(make_request(), journey_id="j1", count=2)
    assert len(sessions) == 2
    assert sessions[0].sequence_index == 0
    assert sessions[1].sequence_index == 1


def test_activity_port_methods():
    port = FakeActivity()
    ids = port.plan_activity_ids(make_request(), session_id="s1")
    assert ids[0].startswith("s1:")


def test_mission_port_methods():
    port = FakeMission()
    missions = port.generate_missions(
        make_request(),
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
    )
    assert len(missions) == 1
    assert missions[0].learner_id == "learner-1"


def test_ports_package_exports():
    from app.application.education_platform import ports as ports_pkg

    for name in (
        "ActivityPort",
        "BlueprintPort",
        "CurriculumPort",
        "JourneyPort",
        "MissionPort",
        "SessionPort",
    ):
        assert hasattr(ports_pkg, name)


def test_unavailable_flags():
    for fake in (
        FakeCurriculum(available=False),
        FakeBlueprint(available=False),
        FakeJourney(available=False),
        FakeSession(available=False),
        FakeActivity(available=False),
        FakeMission(available=False),
    ):
        assert fake.is_available() is False
        fake.set_available(True)
        assert fake.is_available() is True


def test_component_versions_customisable():
    c = FakeCurriculum(component_version="9.9.9")
    assert c.component_version == "9.9.9"
