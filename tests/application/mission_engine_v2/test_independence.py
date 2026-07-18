"""Framework independence and dependency injection tests."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from app.application.mission_engine_v2.engine import MissionEngineV2
from app.application.mission_engine_v2.ports.curriculum_navigation_port import (
    CurriculumNavigationPort,
)
from app.application.mission_engine_v2.ports.journey_engine_port import (
    JourneyEnginePort,
)
from app.application.mission_engine_v2.ports.session_runtime_port import (
    SessionRuntimePort,
)
from tests.application.mission_engine_v2.helpers import (
    TODAY,
    FakeJourneyEngine,
    FakeNavigation,
    FakeSessionRuntime,
    make_engine,
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services.mission_service",
    "app.application.mission_engine.engine",
)


def test_mission_engine_v2_no_forbidden_imports():
    root = Path("app/application/mission_engine_v2")
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


def test_import_engine_without_app_context():
    engine = MissionEngineV2(
        journey_engine=FakeJourneyEngine(),
        session_runtime=FakeSessionRuntime(),
        navigation=FakeNavigation(),
    )
    assert engine.engine_id == "v2"


def test_no_flask_sqlalchemy_in_source():
    root = Path("app/application/mission_engine_v2")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_journey_engine_port_is_protocol():
    assert issubclass(FakeJourneyEngine, JourneyEnginePort)


def test_session_runtime_port_satisfied_by_fake():
    runtime = FakeSessionRuntime(phases={"s1": "active"})
    assert runtime.runtime_phase_for("s1") == "active"


def test_navigation_port_satisfied_by_fake():
    nav = FakeNavigation(topics=("a", "b"))
    assert nav.topic_available("a") is True
    assert nav.ordered_topic_ids() == ("a", "b")


def test_engine_uses_injected_fakes():
    journey = FakeJourneyEngine()
    engine = make_engine(journey=journey)
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    assert any("snapshot" in c for c in journey.calls)


def test_engine_no_v1_mission_engine_import():
    root = Path("app/application/mission_engine_v2")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "app.application.mission_engine.engine" not in text
        assert "MissionEngine(" not in text


def test_mission_engine_v2_package_docstring():
    import app.application.mission_engine_v2 as pkg

    assert "Framework-independent" in pkg.__doc__


def test_ports_are_runtime_checkable():
    assert issubclass(JourneyEnginePort, object)
    assert hasattr(JourneyEnginePort, "snapshot")


def test_all_ports_define_callable_methods():
    for port_cls in (JourneyEnginePort, SessionRuntimePort, CurriculumNavigationPort):
        assert any(
            not name.startswith("_") and callable(member)
            for name, member in inspect.getmembers(port_cls)
        )


def test_engine_constructor_accepts_all_deps():
    engine = MissionEngineV2(
        journey_engine=FakeJourneyEngine(),
        session_runtime=FakeSessionRuntime(),
        navigation=FakeNavigation(),
        available=True,
    )
    assert engine.is_available() is True


def test_coordinator_injected_via_engine():
    engine = make_engine()
    assert engine._coordinator is not None


def test_in_memory_ledger_not_persisted():
    engine = make_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine2 = make_engine()
    assert len(engine2.all_missions()) == 0
