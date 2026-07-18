"""Framework independence for Curriculum Ingestion domain."""

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
    "app.application.learning_journey",
    "app.application.learning_activity",
    "app.application.learning_session",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
)


def test_domain_modules_have_no_forbidden_imports():
    root = Path("app/domain/curriculum_ingestion")
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


def test_no_flask_sqlalchemy_in_domain_source():
    root = Path("app/domain/curriculum_ingestion")
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


def test_package_lazy_exports():
    import app.domain.curriculum_ingestion as ci

    assert ci.IngestionJob is not None
    assert ci.DocumentKind is not None
    assert "NormalizationResult" in dir(ci)


def test_import_without_app_context():
    from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
    from tests.domain.curriculum_ingestion.helpers import make_document

    job = IngestionJob.create("j1", [make_document()])
    assert job.document_count == 1


def test_domain_does_not_mention_sessions_or_missions_as_imports():
    root = Path("app/domain/curriculum_ingestion")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "learning_session" not in node.module
                assert "mission" not in node.module
                assert "learning_activity" not in node.module
