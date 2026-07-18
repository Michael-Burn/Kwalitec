"""Framework independence and isolation for Curriculum Ingestion app layer."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.application.education_platform",
    "app.application.curriculum_management",
    "app.application.instructional_blueprint.engine",
    "app.application.learning_journey",
    "app.application.learning_activity",
    "app.application.learning_session",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
)


def test_application_modules_have_no_forbidden_imports():
    root = Path("app/application/curriculum_ingestion")
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
    root = Path("app/application/curriculum_ingestion")
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


def test_import_engine_without_app_context():
    from app.application.curriculum_ingestion import CurriculumIngestionEngine
    from tests.application.curriculum_ingestion.helpers import make_request

    engine = CurriculumIngestionEngine()
    snap = engine.ingest(make_request())
    assert snap.passed


def test_package_lazy_exports():
    import app.application.curriculum_ingestion as ci

    assert ci.CurriculumIngestionEngine is not None
    assert ci.ExtractionPolicy is not None
    assert "ValidationService" in dir(ci)


def test_does_not_import_forbidden_packages_in_source():
    root = Path("app/application/curriculum_ingestion")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "education_platform" not in text
        assert "curriculum_management" not in text
        assert "mission_engine" not in text
        assert "learning_journey" not in text
        assert "learning_session" not in text
        assert "learning_activity" not in text


def test_engine_constants():
    from app.application.curriculum_ingestion import CurriculumIngestionEngine

    assert CurriculumIngestionEngine.ENGINE_ID == "curriculum_ingestion"
    assert CurriculumIngestionEngine.ENGINE_VERSION == "1.0.0"
