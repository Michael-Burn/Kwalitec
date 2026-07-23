"""Reflection prompt tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import (
    LearningCoachService,
    ReflectionPromptKind,
)
from tests.application.student_experience.coach.conftest import (
    make_empty_inputs,
    make_full_inputs,
)


def test_reflection_prompts_after_study(
    service: LearningCoachService,
) -> None:
    reflection = service.build_reflection(make_full_inputs())
    assert reflection.available is True
    by_kind = {item.kind: item for item in reflection.prompts}
    assert by_kind[ReflectionPromptKind.MOST_DIFFICULT].prompt == (
        "What was most difficult today?"
    )
    assert by_kind[ReflectionPromptKind.BECAME_CLEARER].prompt == (
        "What became clearer?"
    )
    assert by_kind[ReflectionPromptKind.STILL_UNCERTAIN].prompt == (
        "What still feels uncertain?"
    )


def test_reflection_unavailable_without_study(
    service: LearningCoachService,
) -> None:
    reflection = service.build_reflection(make_empty_inputs())
    assert reflection.available is False
    assert reflection.prompts == ()
