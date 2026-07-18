"""Core service / use-case tests for Student Experience."""

from __future__ import annotations

import pytest

from app.application.student_experience.exceptions import (
    PortUnavailable,
    WorkspaceNotFound,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeOrchestratorPort,
    FakeTwinPort,
    make_experience,
)


def test_home_projection_fields():
    exp = make_experience()
    home = exp.get_home("stu-1")
    assert home.student_id == "stu-1"
    assert home.exam_countdown_days == 42
    assert home.exam_readiness == 0.62
    assert home.has_recommendation
    assert home.can_start_session
    assert home.explanation is not None
    assert home.explanation.is_complete


def test_journey_projection_fields():
    exp = make_experience()
    journey = exp.get_journey("stu-1")
    assert journey.current_topic is not None
    assert journey.completed_count == 1
    assert journey.upcoming_count == 1
    assert 0 <= journey.overall_progress_ratio <= 1


def test_revision_projection_fields():
    exp = make_experience()
    rev = exp.get_revision("stu-1")
    assert rev.has_revision
    assert rev.primary is not None
    assert rev.option_count == 2


def test_history_projection_fields():
    exp = make_experience()
    hist = exp.get_history("stu-1")
    assert hist.session_count == 1
    assert hist.total_study_minutes == 120
    assert hist.mastered_count == 1
    assert len(hist.readiness_progression) == 2


def test_profile_projection_fields():
    exp = make_experience()
    profile = exp.get_profile("stu-1")
    assert profile.examination_label == "CPA"
    assert profile.preferences.preferred_session_minutes == 45
    assert profile.goals


def test_explain_recommendation():
    exp = make_experience()
    expl = exp.explain("stu-1")
    assert expl.is_complete
    assert expl.why_recommended


def test_dashboard_active_surface():
    exp = make_experience()
    dash = exp.get_dashboard("stu-1", surface="home")
    assert dash.active_surface == "home"
    assert dash.home is not None
    assert dash.journey is None
    assert len(dash.navigation) == 5


def test_dashboard_all_surfaces():
    exp = make_experience()
    dash = exp.get_dashboard("stu-1", include_all_surfaces=True)
    assert dash.home and dash.journey and dash.revision
    assert dash.history and dash.profile


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_navigate_all_surfaces(surface):
    exp = make_experience()
    ws = exp.open_workspace("stu-1")
    updated = exp.navigate(ws.workspace_id, surface)
    assert updated.active_surface is surface


def test_navigate_missing_workspace():
    exp = make_experience()
    with pytest.raises(WorkspaceNotFound):
        exp.navigate("missing", "home")


def test_port_unavailable_home():
    exp = make_experience(student_twin=FakeTwinPort(available=False))
    with pytest.raises(PortUnavailable):
        exp.get_home("stu-1")


def test_port_unavailable_journey():
    exp = make_experience(learning_journey=FakeJourneyPort(available=False))
    with pytest.raises(PortUnavailable):
        exp.get_journey("stu-1")


def test_port_unavailable_revision():
    exp = make_experience(adaptive_decision=FakeAdaptivePort(available=False))
    with pytest.raises(PortUnavailable):
        exp.get_revision("stu-1")


def test_port_unavailable_mission_start():
    exp = make_experience(mission=FakeMissionPort(available=False))
    with pytest.raises(PortUnavailable):
        exp.start_session("stu-1")


def test_diagnostics_report():
    exp = make_experience()
    exp.open_workspace("stu-1")
    report = exp.diagnostics()
    assert report.workspace_count == 1
    assert "student_twin" in report.registered_ports
    assert report.canonical_surfaces


def test_learning_activity_status_label():
    orch = FakeOrchestratorPort()
    exp = make_experience(learning_orchestrator=orch)
    dash = exp.get_dashboard("stu-1")
    status = dash.learning_activity_status.lower()
    assert "activity" in status or dash.learning_activity_status
