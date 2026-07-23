"""Determinism tests for Exam Readiness Experience (XP-003)."""

from __future__ import annotations

from application.student_experience.readiness import ExamReadinessService
from tests.application.student_experience.readiness.conftest import make_full_inputs


def test_identical_inputs_produce_identical_readiness(
    service: ExamReadinessService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_readiness(inputs, readiness_id="readiness-det")
    second = service.build_readiness(inputs, readiness_id="readiness-det")
    assert first == second
    snap_a = service.build_snapshot(first, snapshot_id="rsnap-det")
    snap_b = service.build_snapshot(second, snapshot_id="rsnap-det")
    assert snap_a == snap_b


def test_summary_methods_are_deterministic(service: ExamReadinessService) -> None:
    inputs = make_full_inputs()
    assert service.summarise_strengths(inputs) == service.summarise_strengths(inputs)
    assert service.summarise_risks(inputs) == service.summarise_risks(inputs)
    assert service.compose_action_plan(inputs) == service.compose_action_plan(inputs)
