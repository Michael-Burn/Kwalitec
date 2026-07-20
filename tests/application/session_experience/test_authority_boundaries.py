"""Authority boundary tests — Session Experience must not own educational law."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.session_experience.ports import PORT_NAMES
from tests.application.session_experience.helpers import (
    FakeAdaptivePort,
    FakeSessionRuntimePort,
    FakeTwinPort,
    make_session_experience,
)

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "session_experience"
)

BANNED_IMPORT_PREFIXES = (
    "app.application.learning_session",
    "app.application.learning_activity",
    "app.application.student_twin",
    "app.application.adaptive_learning",
    "app.application.learning_journey",
    "app.application.mission_engine",
    "app.domain.student_twin",
    "app.domain.adaptive_learning",
    "app.domain.learning_journey",
    "flask",
    "sqlalchemy",
)

BANNED_SOURCE_TOKENS = (
    "compute_readiness",
    "calculate_mastery",
    "generate_mission",
    "recommend_next_action",
    "store_evidence",
)


def _import_offenders() -> list[str]:
    found: list[str] = []
    for path in APP_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == p or alias.name.startswith(p + ".")
                        for p in BANNED_IMPORT_PREFIXES
                    ):
                        found.append(f"{path.name}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == p or node.module.startswith(p + ".")
                    for p in BANNED_IMPORT_PREFIXES
                ):
                    found.append(f"{path.name}: from {node.module}")
    return found


def test_application_does_not_import_engines():
    assert _import_offenders() == []


@pytest.mark.parametrize("token", BANNED_SOURCE_TOKENS)
def test_facade_source_avoids_banned_calc_tokens(token):
    text = (APP_ROOT / "facade.py").read_text(encoding="utf-8")
    assert token not in text


def test_completion_uses_twin_and_adaptive_facts_not_invention():
    twin = FakeTwinPort()
    adaptive = FakeAdaptivePort()
    svc = make_session_experience(student_twin=twin, adaptive_decision=adaptive)
    svc.open_session("stu-1", session_id="sess-1")
    summary = svc.get_summary("stu-1", session_id="sess-1")
    assert "consolidations" in summary.next_recommendation.lower()


def test_response_routes_through_runtime_evidence_port():
    runtime = FakeSessionRuntimePort()
    svc = make_session_experience(session_runtime=runtime)
    svc.open_session("stu-1", session_id="sess-1")
    svc.begin_session("stu-1", session_id="sess-1")
    activity = svc.get_activity("stu-1", session_id="sess-1")
    svc.submit_response(
        "stu-1",
        session_id="sess-1",
        activity_id=activity.activity_id,
        response="Answer",
    )
    assert runtime.response_calls


@pytest.mark.parametrize("port_name", PORT_NAMES)
def test_port_names_documented(port_name):
    assert isinstance(port_name, str)
    assert port_name
