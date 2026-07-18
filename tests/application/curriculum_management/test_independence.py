"""Framework independence and isolation for Curriculum Management app layer."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.application.education_platform",
    "app.application.instructional_blueprint.engine",
    "app.application.learning_journey",
    "app.application.learning_activity",
    "app.application.learning_session",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
)


def test_application_modules_have_no_forbidden_imports():
    root = Path("app/application/curriculum_management")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN
                    ):
                        offenders.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN
                ):
                    offenders.append(f"{path}: from {node.module}")
    assert offenders == []


def test_no_flask_sqlalchemy_imports_in_source():
    root = Path("app/application/curriculum_management")
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


def test_import_facade_without_app_context():
    from app.application.curriculum_management import CurriculumManagementFacade

    facade = CurriculumManagementFacade()
    snap = facade.subjects.create_subject("CS1", "Core Stats")
    assert snap.code == "CS1"


def test_package_lazy_exports():
    import app.application.curriculum_management as cm

    assert cm.SubjectService is not None
    assert cm.PublicationPolicy is not None
    assert "ValidationService" in dir(cm)


def test_does_not_import_education_platform_in_source():
    root = Path("app/application/curriculum_management")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "education_platform" not in text
        assert "mission_engine" not in text
        assert "learning_journey" not in text
