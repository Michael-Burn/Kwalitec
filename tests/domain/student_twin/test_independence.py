"""Framework independence for Student Digital Twin domain."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.application",
    "app.services",
)


def test_domain_modules_have_no_forbidden_imports():
    root = Path("app/domain/student_twin")
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
    root = Path("app/domain/student_twin")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "flask" not in text.lower() or "flask" not in text
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_package_lazy_exports():
    import app.domain.student_twin as st

    assert st.DigitalTwin is not None
    assert st.EvidenceType is not None
    assert "MasteryState" in dir(st)


@pytest.mark.parametrize(
    "name",
    [
        "DigitalTwin",
        "EvidenceEvent",
        "EvidenceType",
        "ConfidenceBand",
        "KnowledgeState",
        "MasteryState",
        "RetentionState",
        "ReadinessState",
        "RecommendationState",
        "WeaknessProfile",
        "TwinSnapshot",
        "Learner",
        "TwinVersion",
        "TwinIdentity",
        "LearningHistory",
        "LearningVelocity",
        "EvidenceProfile",
        "ConfidenceState",
    ],
)
def test_lazy_export_resolves(name):
    import app.domain.student_twin as st

    assert getattr(st, name) is not None


def test_import_without_app_context():
    from app.domain.student_twin.digital_twin import DigitalTwin
    from tests.domain.student_twin.helpers import make_learner

    twin = DigitalTwin.create("t1", make_learner())
    assert twin.event_count == 0
