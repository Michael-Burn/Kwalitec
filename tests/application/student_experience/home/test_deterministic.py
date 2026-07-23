"""Determinism tests for Student Home Experience."""

from __future__ import annotations

from application.student_experience.home import StudentHomeService
from tests.application.student_experience.home.conftest import make_full_inputs


def test_identical_inputs_produce_identical_home(
    service: StudentHomeService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_home(inputs, home_id="home-det")
    second = service.build_home(inputs, home_id="home-det")

    assert first == second
    snap_a = service.build_snapshot(first, snapshot_id="snap-det")
    snap_b = service.build_snapshot(second, snapshot_id="snap-det")
    assert snap_a == snap_b


def test_focus_and_progress_are_deterministic(service: StudentHomeService) -> None:
    inputs = make_full_inputs()
    assert service.determine_primary_focus(inputs) == service.determine_primary_focus(
        inputs
    )
    assert service.summarise_progress(inputs) == service.summarise_progress(inputs)
