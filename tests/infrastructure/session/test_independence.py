"""Independence and packaging checks for Session Experience infrastructure."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.session_experience.facade import SessionExperienceService
from app.infrastructure.session import SESSION_INFRASTRUCTURE_VERSION
from app.infrastructure.session.composition import build_production_session_experience
from app.presentation.session.factory import (
    build_session_experience_service,
)

ROOT = Path(__file__).resolve().parents[3]
SESSION_INFRA = ROOT / "app" / "infrastructure" / "session"
APP_SESSION = ROOT / "app" / "application" / "session_experience"

REQUIRED_FILES = (
    "__init__.py",
    "runtime_adapter.py",
    "activity_adapter.py",
    "mission_adapter.py",
    "twin_adapter.py",
    "adaptive_adapter.py",
)


def test_required_adapter_modules_present():
    names = {p.name for p in SESSION_INFRA.glob("*.py")}
    for required in REQUIRED_FILES:
        assert required in names


def test_session_infrastructure_version():
    assert SESSION_INFRASTRUCTURE_VERSION.startswith("v2-020a")


def test_application_does_not_import_session_infrastructure():
    forbidden = ("app.infrastructure",)
    found: list[str] = []
    for path in APP_SESSION.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in forbidden
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in forbidden
                ):
                    found.append(f"{path}: from {node.module}")
    assert found == []


def test_facade_create_without_builder_returns_empty_ports():
    SessionExperienceService.set_production_builder(None)
    service = SessionExperienceService.create(use_production_adapters=True)
    assert isinstance(service, SessionExperienceService)


def test_facade_create_with_builder_uses_production():
    _, production = build_production_session_experience(seed_demo_learners=False)
    SessionExperienceService.set_production_builder(lambda: production)
    service = SessionExperienceService.create(use_production_adapters=True)
    assert service is production
    SessionExperienceService.set_production_builder(None)


def test_presentation_factory_defaults_to_production():
    service = build_session_experience_service()
    assert isinstance(service, SessionExperienceService)
    # Production service can open a seeded default session.
    overview = service.open_session("default", session_id="sess-1")
    assert overview.objective


def test_presentation_factory_allows_disabled_production():
    service = build_session_experience_service(use_production_adapters=False)
    assert isinstance(service, SessionExperienceService)


@pytest.mark.parametrize(
    "module_name",
    [
        "runtime_adapter",
        "activity_adapter",
        "mission_adapter",
        "twin_adapter",
        "adaptive_adapter",
        "composition",
        "defaults",
        "store",
    ],
)
def test_session_modules_importable(module_name):
    mod = __import__(
        f"app.infrastructure.session.{module_name}",
        fromlist=["*"],
    )
    assert mod is not None
