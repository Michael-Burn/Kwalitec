"""MissionEnginePort adapter contract tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_engine_v2.exceptions import (
    MissionFactoryError,
    MissionNotFound,
)
from app.application.mission_engine_v2.lifecycle import MissionState
from tests.application.mission_engine_v2.helpers import (
    TODAY,
    make_adapter_request,
    make_engine,
)


def test_engine_id_property():
    engine = make_engine()
    assert engine.engine_id == "v2"


def test_is_available_toggle():
    engine = make_engine(available=False)
    assert engine.is_available() is False


def test_generate_mission_via_port():
    engine = make_engine()
    request = make_adapter_request(operation="generate")
    snapshot = engine.generate_mission(request)
    assert isinstance(snapshot, MissionSnapshot)
    assert snapshot.engine_id == "v2"
    assert snapshot.engine_version == "2.0.0"
    assert snapshot.learner_id == "learner-1"


def test_adapter_snapshot_fields_and_metadata():
    engine = make_engine()
    request = make_adapter_request(operation="generate")
    snapshot = engine.generate_mission(request)
    assert snapshot.topic_id == "topic-a"
    assert snapshot.session_id
    assert snapshot.effort == "medium"
    assert snapshot.metadata["operation"] == "generate"
    assert "state" in snapshot.metadata


def test_port_lifecycle_methods_exist():
    engine = make_engine()
    for method_name in ("resume_mission", "pause_mission", "skip_mission", "archive_mission"):  # noqa: E501
        assert callable(getattr(engine, method_name))


def test_generate_mission_revision_flag():
    engine = make_engine()
    request = make_adapter_request(context={"as_of_date": TODAY.isoformat(), "is_revision": True})  # noqa: E501
    snapshot = engine.generate_mission(request)
    assert snapshot.is_revision is True


def test_generate_mission_requires_journey_id():
    engine = make_engine()
    request = make_adapter_request()
    object.__setattr__(request, "journey_id", None)
    with pytest.raises(MissionFactoryError, match="journey_id"):
        engine.generate_mission(request)


def test_resume_mission_via_port():
    engine = make_engine()
    created = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(created.mission_id)
    engine.pause_mission_by_id(created.mission_id)
    request = make_adapter_request(
        operation="resume",
        mission_id=created.mission_id,
    )
    snapshot = engine.resume_mission(request)
    assert snapshot.metadata["state"] == MissionState.ACTIVE.value


def test_pause_mission_via_port():
    engine = make_engine()
    created = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(created.mission_id)
    request = make_adapter_request(operation="pause", mission_id=created.mission_id)
    snapshot = engine.pause_mission(request)
    assert snapshot.metadata["state"] == MissionState.PAUSED.value


def test_skip_mission_maps_to_defer():
    engine = make_engine()
    created = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(created.mission_id)
    request = make_adapter_request(operation="skip", mission_id=created.mission_id)
    snapshot = engine.skip_mission(request)
    assert snapshot.metadata["slot"] == "deferred"


def test_archive_mission_via_port():
    engine = make_engine()
    created = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(created.mission_id)
    request = make_adapter_request(operation="archive", mission_id=created.mission_id)
    snapshot = engine.archive_mission(request)
    assert snapshot.metadata["state"] == MissionState.ARCHIVED.value


def test_port_operations_require_mission_id():
    engine = make_engine()
    request = make_adapter_request(operation="pause", mission_id=None)
    with pytest.raises(MissionNotFound):
        engine.pause_mission(request)
