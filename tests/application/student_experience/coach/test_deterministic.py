"""Determinism tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import LearningCoachService
from tests.application.student_experience.coach.conftest import make_full_inputs


def test_identical_inputs_produce_identical_context(
    service: LearningCoachService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_context(inputs, coach_id="coach-det")
    second = service.build_context(inputs, coach_id="coach-det")
    assert first == second

    conv_a = service.build_conversation(inputs, conversation_id="conv-det")
    conv_b = service.build_conversation(inputs, conversation_id="conv-det")
    assert conv_a == conv_b

    reflection_a = service.build_reflection(inputs)
    reflection_b = service.build_reflection(inputs)
    assert reflection_a == reflection_b

    snap_a = service.build_snapshot(first, snapshot_id="csnap-det")
    snap_b = service.build_snapshot(second, snapshot_id="csnap-det")
    assert snap_a == snap_b


def test_suggested_questions_are_deterministic(
    service: LearningCoachService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_conversation(inputs)
    second = service.build_conversation(inputs)
    assert first.suggested_questions == second.suggested_questions
    assert first.context_digest == second.context_digest
