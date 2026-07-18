"""Regression guards for Student Experience foundation."""

from __future__ import annotations

from pathlib import Path

from app.application.student_experience.ports import PORT_NAMES
from app.domain.student_experience.experience_workspace import CANONICAL_SURFACES
from tests.application.student_experience.helpers import make_experience


def test_port_names_stable():
    assert PORT_NAMES == (
        "student_twin",
        "adaptive_decision",
        "mission",
        "learning_journey",
        "learning_orchestrator",
    )


def test_canonical_surfaces_stable():
    assert tuple(s.value for s in CANONICAL_SURFACES) == (
        "home",
        "journey",
        "revision",
        "history",
        "profile",
    )


def test_required_application_modules_exist():
    root = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "student_experience"
    )
    for name in (
        "home_service.py",
        "journey_service.py",
        "revision_service.py",
        "history_service.py",
        "profile_service.py",
        "explanation_service.py",
        "dashboard_service.py",
        "diagnostics.py",
        "exceptions.py",
        "student_experience_service.py",
    ):
        assert (root / name).exists()


def test_required_dto_modules_exist():
    root = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "student_experience"
        / "dto"
    )
    for name in (
        "home_snapshot.py",
        "journey_snapshot.py",
        "revision_snapshot.py",
        "history_snapshot.py",
        "profile_snapshot.py",
        "explanation_snapshot.py",
    ):
        assert (root / name).exists()


def test_open_workspace_reuse():
    exp = make_experience()
    a = exp.open_workspace("stu-1")
    b = exp.open_workspace("stu-1")
    assert a.workspace_id == b.workspace_id


def test_full_happy_path():
    exp = make_experience()
    exp.open_workspace("stu-1", display_name="Alex")
    home = exp.get_home("stu-1")
    assert home.has_recommendation
    rev = exp.get_revision("stu-1")
    assert rev.has_revision
    handle = exp.start_session("stu-1")
    assert handle.mission_id
    report = exp.diagnostics()
    assert report.session_count == 1
