"""V1 adapter and framework-independence tests."""

from __future__ import annotations

import pytest

from app.application.mission_engine.adapters.v1_mission_adapter import (
    V1_STATUS_COMPLETED,
    V1_STATUS_IN_PROGRESS,
    V1_STATUS_PENDING,
    V1MissionAdapter,
    V1MissionView,
)
from app.application.mission_engine.mission_state import DeliveryAction, MissionState
from tests.application.mission_engine.helpers import (
    TODAY,
    active_journey,
    make_mission_engine,
)


@pytest.fixture
def adapter() -> V1MissionAdapter:
    return V1MissionAdapter()


def test_cutover_status_parallel(adapter):
    assert adapter.cutover_status() == "parallel_only"


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("Pending", MissionState.SCHEDULED),
        ("In Progress", MissionState.IN_PROGRESS),
        ("Completed", MissionState.COMPLETED),
        ("skipped", MissionState.SKIPPED),
        ("", MissionState.SCHEDULED),
    ],
)
def test_map_v1_status(adapter, status, expected):
    assert adapter.map_v1_status_to_state(status) == expected


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (MissionState.SCHEDULED, V1_STATUS_PENDING),
        (MissionState.ACTIVE, V1_STATUS_IN_PROGRESS),
        (MissionState.IN_PROGRESS, V1_STATUS_IN_PROGRESS),
        (MissionState.COMPLETED, V1_STATUS_COMPLETED),
        (MissionState.ARCHIVED, V1_STATUS_COMPLETED),
        (MissionState.DEFERRED, V1_STATUS_PENDING),
    ],
)
def test_map_state_to_v1(adapter, state, expected):
    assert adapter.map_state_to_v1_status(state) == expected


def test_to_summary(adapter):
    view = V1MissionView(
        mission_id="42",
        user_id="7",
        subject_id="3",
        mission_date=TODAY,
        title="V1 Title",
        status="Pending",
        study_plan_id="9",
    )
    summary = adapter.to_summary(view, journey_id="j", session_id="s", topic_id="t")
    assert summary.title == "V1 Title"
    assert summary.learner_id == "7"
    assert summary.delivery_action == DeliveryAction.TODAY


def test_to_v1_view(adapter):
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    view = adapter.to_v1_view(mission, subject_id="sub", study_plan_id="sp")
    assert view.title == mission.title
    assert view.status == V1_STATUS_IN_PROGRESS
    assert view.task_count == 1


def test_reconciliation_both(adapter):
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    view = adapter.to_v1_view(mission, subject_id="1")
    payload = adapter.reconciliation_payload(v1=view, v2=mission)
    assert payload["v1_present"] == "true"
    assert payload["v2_present"] == "true"
    assert payload["dates_match"] == "true"
    assert payload["cutover_status"] == "parallel_only"


def test_reconciliation_v1_only(adapter):
    view = V1MissionView(
        mission_id="1",
        user_id="u",
        subject_id="s",
        mission_date=TODAY,
        title="T",
        status="Pending",
    )
    payload = adapter.reconciliation_payload(v1=view, v2=None)
    assert payload["v2_present"] == "false"


def test_reconciliation_v2_only(adapter):
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    payload = adapter.reconciliation_payload(v1=None, v2=mission)
    assert payload["v1_present"] == "false"


def test_default_delivery_action(adapter):
    assert adapter.default_delivery_action_for_v1("Completed") == DeliveryAction.REVIEW
    assert (
        adapter.default_delivery_action_for_v1("In Progress")
        == DeliveryAction.CONTINUE
    )
    assert adapter.default_delivery_action_for_v1("Pending") == DeliveryAction.TODAY


def test_adapter_module_exports():
    from app.application.mission_engine import adapters

    assert adapters.V1MissionAdapter is V1MissionAdapter
    assert adapters.V1MissionView is V1MissionView


# --- Framework independence ---


FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services.mission_service",
)


def test_mission_engine_modules_have_no_flask_sqlalchemy():
    import ast
    from pathlib import Path

    root = Path("app/application/mission_engine")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN_MODULES
                    ):
                        offenders.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN_MODULES
                ):
                    offenders.append(f"{path}: from {node.module}")
    assert offenders == []


def test_import_mission_engine_without_app_context():
    from app.application.mission_engine.engine import MissionEngine

    engine = MissionEngine()
    assert engine.all_missions() == ()


def test_no_mission_service_import_in_package():
    import app.application.mission_engine.adapters.v1_mission_adapter as ad
    import app.application.mission_engine.engine as eng

    assert "MissionService" not in dir(eng)
    assert "MissionService" not in dir(ad)
