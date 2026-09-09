"""Volume matrices for Student Experience application."""

from __future__ import annotations

import pytest

from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    ExperienceSurface,
)
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeOrchestratorPort,
    FakeTwinPort,
    make_experience,
)

PORT_COMBOS = []
for mask in range(32):
    PORT_COMBOS.append(mask)


@pytest.mark.parametrize("mask", PORT_COMBOS)
def test_diagnostics_port_mask(mask):
    twin = FakeTwinPort(available=bool(mask & 1))
    adaptive = FakeAdaptivePort(available=bool(mask & 2))
    mission = FakeMissionPort(available=bool(mask & 4))
    journey = FakeJourneyPort(available=bool(mask & 8))
    orch = FakeOrchestratorPort(available=bool(mask & 16))
    exp = make_experience(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
        learning_journey=journey,
        learning_orchestrator=orch,
    )
    report = exp.diagnostics()
    assert report.port_availability["student_twin"] is bool(mask & 1)
    assert report.port_availability["adaptive_decision"] is bool(mask & 2)
    assert report.port_availability["mission"] is bool(mask & 4)
    assert report.port_availability["learning_journey"] is bool(mask & 8)
    assert report.port_availability["learning_orchestrator"] is bool(mask & 16)


@pytest.mark.parametrize("surface", list(ExperienceSurface))
@pytest.mark.parametrize("include_all", [False, True])
def test_dashboard_surface_matrix(surface, include_all):
    dash = make_experience().get_dashboard(
        "stu-1", surface=surface, include_all_surfaces=include_all
    )
    assert dash.active_surface == surface.value
    assert len(dash.navigation) == len(CANONICAL_SURFACES)
    if include_all:
        assert dash.home is not None
        assert dash.profile is not None


@pytest.mark.parametrize("days", range(0, 20))
def test_home_countdown_matrix_via_twin(days):
    twin = FakeTwinPort()
    original = twin.get_readiness_summary

    def patched(student_id):
        data = dict(original(student_id) or {})
        data["exam_countdown_days"] = days
        return data

    twin.get_readiness_summary = patched  # type: ignore[method-assign]
    home = make_experience(student_twin=twin).get_home("stu-1")
    assert home.exam_countdown_days == days


@pytest.mark.parametrize("ratio_i", range(0, 11))
def test_journey_progress_matrix(ratio_i):
    ratio = ratio_i / 10
    journey_port = FakeJourneyPort()
    original = journey_port.get_journey_progress

    def patched(student_id):
        data = dict(original(student_id) or {})
        data["overall_progress_ratio"] = ratio
        return data

    journey_port.get_journey_progress = patched  # type: ignore[method-assign]
    snap = make_experience(learning_journey=journey_port).get_journey("stu-1")
    assert snap.overall_progress_ratio == ratio
    assert snap.progress_percent == int(round(ratio * 100))


@pytest.mark.parametrize("n_alts", range(0, 6))
def test_revision_due_counts(n_alts):
    from tests.application.student_experience.helpers import (
        _spacing_with_due_packages,
    )

    spacing = _spacing_with_due_packages("stu-1", count=1 + n_alts)
    snap = make_experience(spacing_scheduler=spacing).get_revision("stu-1")
    assert snap.option_count == 1 + n_alts
    assert len(snap.due_now) == 1 + n_alts
