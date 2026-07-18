"""DependencyRegistry registration, replacement, and isolation tests."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.exceptions import DependencyError
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_full_ports,
)


def test_register_and_get():
    reg = DependencyRegistry()
    port = FakeCurriculum()
    reg.register("curriculum", port)
    assert reg.get("curriculum") is port


def test_register_none_raises():
    reg = DependencyRegistry()
    with pytest.raises(DependencyError):
        reg.register("curriculum", None)


def test_duplicate_register_raises():
    reg = DependencyRegistry()
    reg.register("curriculum", FakeCurriculum())
    with pytest.raises(DependencyError, match="Duplicate"):
        reg.register("curriculum", FakeCurriculum())


def test_unknown_port_name_raises():
    reg = DependencyRegistry()
    with pytest.raises(DependencyError):
        reg.register("twin", FakeCurriculum())


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_all_canonical_ports_registerable(name):
    reg = DependencyRegistry()
    ports = make_full_ports()
    reg.register(name, ports[name])
    assert reg.has(name)


def test_replace_returns_previous():
    reg = DependencyRegistry()
    first = FakeCurriculum()
    second = FakeCurriculum(subject_id="other")
    reg.register("curriculum", first)
    prev = reg.replace("curriculum", second)
    assert prev is first
    assert reg.get("curriculum") is second


def test_replace_unregistered_raises():
    reg = DependencyRegistry()
    with pytest.raises(DependencyError, match="unregistered"):
        reg.replace("curriculum", FakeCurriculum())


def test_replace_with_none_raises():
    reg = DependencyRegistry()
    reg.register("curriculum", FakeCurriculum())
    with pytest.raises(DependencyError):
        reg.replace("curriculum", None)


def test_get_missing_raises():
    reg = DependencyRegistry()
    with pytest.raises(DependencyError, match="not registered"):
        reg.get("curriculum")


def test_has_false_when_missing():
    reg = DependencyRegistry()
    assert reg.has("curriculum") is False


def test_unregister():
    reg = DependencyRegistry()
    port = FakeCurriculum()
    reg.register("curriculum", port)
    assert reg.unregister("curriculum") is port
    assert not reg.has("curriculum")


def test_unregister_missing_raises():
    reg = DependencyRegistry()
    with pytest.raises(DependencyError):
        reg.unregister("curriculum")


def test_clear():
    reg = DependencyRegistry()
    for name, port in make_full_ports().items():
        reg.register(name, port)
    reg.clear()
    assert len(reg) == 0


def test_registered_names_canonical_order():
    reg = DependencyRegistry()
    # Register out of order
    reg.register("mission", FakeMission())
    reg.register("curriculum", FakeCurriculum())
    reg.register("session", FakeSession())
    assert reg.registered_names() == ("curriculum", "session", "mission")


def test_missing_names():
    reg = DependencyRegistry()
    reg.register("curriculum", FakeCurriculum())
    missing = reg.missing_names()
    assert "curriculum" not in missing
    assert "blueprint" in missing
    assert missing == tuple(n for n in DEPENDENCY_CHAIN if n != "curriculum")


def test_as_mapping_is_proxy():
    reg = DependencyRegistry()
    reg.register("curriculum", FakeCurriculum())
    view = reg.as_mapping()
    assert isinstance(view, MappingProxyType)
    with pytest.raises(TypeError):
        view["curriculum"] = FakeCurriculum()  # type: ignore[index]


def test_contains():
    reg = DependencyRegistry()
    reg.register("curriculum", FakeCurriculum())
    assert "curriculum" in reg
    assert "blueprint" not in reg
    assert 1 not in reg


def test_len():
    reg = DependencyRegistry()
    assert len(reg) == 0
    reg.register("curriculum", FakeCurriculum())
    reg.register("blueprint", FakeBlueprint())
    assert len(reg) == 2


def test_never_instantiates_engines():
    """Registry source must not construct concrete engines."""
    import ast
    from pathlib import Path

    path = Path("app/application/education_platform/dependency_registry.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    calls = [
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    ]
    forbidden = {
        "InstructionalBlueprintEngine",
        "LearningJourneyEngine",
        "LearningSessionRuntime",
        "LearningActivityEngine",
        "MissionEngineV2",
        "MissionAdapter",
    }
    assert forbidden.isdisjoint(calls)


def test_full_registration_no_missing():
    reg = DependencyRegistry()
    for name, port in make_full_ports().items():
        reg.register(name, port)
    assert reg.missing_names() == ()


@pytest.mark.parametrize(
    "port_cls",
    [
        FakeCurriculum,
        FakeBlueprint,
        FakeJourney,
        FakeSession,
        FakeActivity,
        FakeMission,
    ],
)
def test_replace_each_port_type(port_cls):
    name = {
        FakeCurriculum: "curriculum",
        FakeBlueprint: "blueprint",
        FakeJourney: "journey",
        FakeSession: "session",
        FakeActivity: "activity",
        FakeMission: "mission",
    }[port_cls]
    reg = DependencyRegistry()
    reg.register(name, port_cls())
    replacement = port_cls()
    prev = reg.replace(name, replacement)
    assert prev is not replacement
    assert reg.get(name) is replacement


def test_register_does_not_copy_port():
    reg = DependencyRegistry()
    port = FakeJourney()
    reg.register("journey", port)
    port.calls.append("external")
    assert reg.get("journey").calls == ["external"]
