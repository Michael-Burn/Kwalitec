"""Framework independence for Student Digital Twin application."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
)


def test_application_modules_have_no_forbidden_imports():
    root = Path("app/application/student_twin")
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


def test_no_flask_sqlalchemy():
    root = Path("app/application/student_twin")
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
    import app.application.student_twin as st

    assert st.StudentTwinEngine is not None
    assert "MasteryCalculator" in dir(st)


@pytest.mark.parametrize(
    "name",
    [
        "StudentTwinEngine",
        "EvidenceAggregator",
        "MasteryCalculator",
        "ConfidenceCalculator",
        "RetentionEstimator",
        "ReadinessEstimator",
        "WeaknessAnalyser",
        "RecommendationService",
        "SnapshotService",
        "TimelineService",
        "ComparisonService",
        "ExplanationService",
        "TwinDiagnostics",
        "EvidencePolicy",
        "MasteryPolicy",
        "ConfidencePolicy",
        "RecommendationPolicy",
        "TwinSnapshotDTO",
        "StudentTwinError",
        "EvidenceRejected",
    ],
)
def test_lazy_export_resolves(name):
    import app.application.student_twin as st

    assert getattr(st, name) is not None


def test_import_without_app_context():
    from app.application.student_twin.twin_engine import StudentTwinEngine

    engine = StudentTwinEngine()
    twin = engine.create_twin("learner-x", twin_id="twin-x")
    assert twin.event_count == 0
