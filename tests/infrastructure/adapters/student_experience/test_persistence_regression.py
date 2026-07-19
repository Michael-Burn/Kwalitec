"""Persistence, independence, and regression for Experience production adapters."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.mission import ExperienceMissionAdapter
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.adapters.student_twin import ExperienceTwinAdapter
from app.infrastructure.persistence.optimistic_locking import OptimisticLockError
from app.infrastructure.persistence.unit_of_work import UnitOfWork

ROOT = Path(__file__).resolve().parents[4]

EXPERIENCE_PURE_MODULES = (
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "student_experience"
    / "defaults.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "student_experience"
    / "projection_store.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "adaptive"
    / "adapter.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "journey"
    / "adapter.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "orchestrator"
    / "adapter.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "student_twin"
    / "experience_adapter.py",
    ROOT
    / "app"
    / "infrastructure"
    / "adapters"
    / "mission"
    / "experience_adapter.py",
)

FORBIDDEN_IMPORT_PREFIXES = (
    "flask",
    "sqlalchemy",
)


def test_build_production_experience_default():
    composition, service = build_production_experience()
    assert composition.twin.is_available()
    home = service.get_home("default")
    assert home.student_id == "default"


def test_snapshot_persistence_on_put():
    store = ExperienceProjectionStore()
    twin = ExperienceTwinAdapter(store=store)
    twin.put_projection("snap-1", {"display_name": "A", "authority": "student_twin"})
    latest = store.snapshots.latest(store.TWIN, "snap-1")
    assert latest is not None
    assert latest.payload["display_name"] == "A"


def test_optimistic_locking_conflict():
    store = ExperienceProjectionStore()
    store.save(store.twin, "lock-1", {"v": 1})
    with pytest.raises(OptimisticLockError):
        store.save(store.twin, "lock-1", {"v": 2}, expected_version=99)


def test_uow_registers_writes():
    uow = UnitOfWork()
    store = ExperienceProjectionStore(uow=uow)
    with uow.transaction():
        store.save(store.mission, "m-1", {"student_id": "u1"})
        assert len(uow.items) >= 1


def test_learning_loop_preserves_adaptive_authority():
    composition = StudentExperienceComposition(
        seed_demo_learners=False, learning_loop=None
    )
    composition.seed_learner("auth-1", demo=True)
    service = composition.build_service()
    service.start_session("auth-1")
    doc = composition.store.get(composition.store.adaptive, "auth-1")
    assert doc["next_action_authority"] is True
    mission = composition.store.get(composition.store.mission, "auth-1")
    assert mission["next_action_authority"] is False


def test_experience_adapters_do_not_import_flask():
    for path in EXPERIENCE_PURE_MODULES:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prefix in FORBIDDEN_IMPORT_PREFIXES:
                        assert not alias.name.startswith(prefix), path
            elif isinstance(node, ast.ImportFrom) and node.module:
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    assert not node.module.startswith(prefix), path


def test_preview_ports_module_removed():
    preview = (
        ROOT / "app" / "presentation" / "student" / "preview_ports.py"
    )
    assert not preview.exists()


def test_protocols_still_structural():
    assert isinstance(ExperienceTwinAdapter(), StudentTwinPort)
    assert isinstance(ExperienceAdaptiveAdapter(), AdaptiveDecisionPort)
    assert isinstance(ExperienceMissionAdapter(), MissionPort)
