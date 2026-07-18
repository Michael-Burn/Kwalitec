"""Framework / curriculum / subject independence tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.instructional_blueprint.engine import (
    InstructionalBlueprintEngine,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "instructional_blueprint"
)
DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "instructional_blueprint"
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.curriculum",
    "app.domain.curriculum",
)


def _offenders(root: Path) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN_MODULES
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN_MODULES
                ):
                    found.append(f"{path}: from {node.module}")
    return found


def test_application_no_forbidden_imports():
    assert _offenders(APP_ROOT) == []


def test_domain_no_forbidden_imports():
    assert _offenders(DOMAIN_ROOT) == []


def test_import_engine_without_app_context():
    engine = InstructionalBlueprintEngine()
    assert engine.engine_id == "instructional_blueprint"


def test_no_flask_sqlalchemy_imports_in_source():
    for root in (APP_ROOT, DOMAIN_ROOT):
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


def test_subject_independent_selection():
    """Same structural intent yields same blueprint regardless of subject labels."""
    engine = InstructionalBlueprintEngine()
    a = engine.generate_sequence(intent_tags=("revision",), objective_ids=("math-1",))
    b = engine.generate_sequence(intent_tags=("revision",), objective_ids=("law-9",))
    assert a.compiled.activity_kinds == b.compiled.activity_kinds
    assert a.blueprint.blueprint_type == BlueprintType.REVISION


def test_curriculum_independent_no_topic_required():
    engine = InstructionalBlueprintEngine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.MIXED_PRACTICE)
    assert handle.plan is not None
    # No topic_id / curriculum_id on plan
    assert not hasattr(handle.plan, "topic_id")
    assert not hasattr(handle.plan, "curriculum_id")


def test_no_student_specific_api_on_engine():
    engine = InstructionalBlueprintEngine()
    methods = [name for name in dir(engine) if not name.startswith("_")]
    for forbidden in ("student", "mastery", "twin", "user_id"):
        assert not any(forbidden in name.lower() for name in methods)


def test_required_application_files_exist():
    required = {
        "engine.py",
        "blueprint_selector.py",
        "blueprint_validator.py",
        "blueprint_compiler.py",
        "blueprint_registry.py",
        "sequence_generator.py",
        "exceptions.py",
        "__init__.py",
    }
    present = {path.name for path in APP_ROOT.glob("*.py")}
    assert required <= present
    assert (APP_ROOT / "dto" / "blueprint_plan.py").exists()
    assert (APP_ROOT / "dto" / "compiled_blueprint.py").exists()
    assert (APP_ROOT / "dto" / "blueprint_snapshot.py").exists()
    assert (APP_ROOT / "policies" / "selection_policy.py").exists()
    assert (APP_ROOT / "policies" / "compilation_policy.py").exists()


def test_outputs_never_include_content_payloads():
    engine = InstructionalBlueprintEngine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.CONCEPT_MASTERY)
    snapshot = engine.snapshot(handle)
    blob = repr(snapshot) + repr(handle.plan) + repr(handle.compiled)
    for token in ("question=", "explanation=", "pdf=", "prompt="):
        assert token not in blob.lower()


@pytest.mark.parametrize(
    "module_path",
    [
        "app.application.instructional_blueprint.engine",
        "app.application.instructional_blueprint.blueprint_registry",
        "app.application.instructional_blueprint.blueprint_selector",
        "app.application.instructional_blueprint.blueprint_validator",
        "app.application.instructional_blueprint.blueprint_compiler",
        "app.application.instructional_blueprint.sequence_generator",
        "app.domain.instructional_blueprint.blueprint",
        "app.domain.instructional_blueprint.blueprint_type",
    ],
)
def test_modules_importable(module_path):
    __import__(module_path)
