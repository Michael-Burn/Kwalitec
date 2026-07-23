"""Determinism tests for Learning Journey Experience (XP-002)."""

from __future__ import annotations

from application.student_experience.progress import LearningJourneyService
from tests.application.student_experience.progress.conftest import make_rich_inputs


def test_identical_inputs_produce_identical_journey(
    service: LearningJourneyService,
) -> None:
    inputs = make_rich_inputs()
    first = service.build_journey(inputs, journey_id="journey-det")
    second = service.build_journey(inputs, journey_id="journey-det")
    assert first == second
    snap_a = service.build_snapshot(first, snapshot_id="jsnap-det")
    snap_b = service.build_snapshot(second, snapshot_id="jsnap-det")
    assert snap_a == snap_b


def test_summary_methods_are_deterministic(service: LearningJourneyService) -> None:
    inputs = make_rich_inputs()
    assert service.build_timeline(inputs) == service.build_timeline(inputs)
    assert service.summarise_growth(inputs) == service.summarise_growth(inputs)
    assert service.summarise_habits(inputs) == service.summarise_habits(inputs)
    assert service.summarise_consistency(inputs) == service.summarise_consistency(
        inputs
    )
