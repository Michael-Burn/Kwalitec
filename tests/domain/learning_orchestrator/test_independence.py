"""Domain independence and edge cases."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEventType,
)
from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "learning_orchestrator"
)

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.application",
)


def test_domain_has_no_application_imports():
    found = []
    for path in DOMAIN_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN
                    ):
                        found.append(f"{path}: {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN
                ):
                    found.append(f"{path}: {node.module}")
    assert found == []


@pytest.mark.parametrize("event_type", list(OrchestrationEventType))
@pytest.mark.parametrize("state", list(OrchestrationState))
def test_event_state_matrix_exists(event_type, state):
    assert event_type.value
    assert state.value


@pytest.mark.parametrize("stage", list(PipelineStageName))
@pytest.mark.parametrize("event_type", list(OrchestrationEventType))
def test_stage_event_matrix_tokens(stage, event_type):
    assert isinstance(stage.value, str)
    assert isinstance(event_type.value, str)
    assert "_" in event_type.value or event_type.value.isalpha()
