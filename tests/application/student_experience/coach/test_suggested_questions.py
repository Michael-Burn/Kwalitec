"""Suggested question tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import (
    LearningCoachService,
    SuggestedQuestionKind,
)
from tests.application.student_experience.coach.conftest import (
    make_empty_inputs,
    make_full_inputs,
)


def test_suggested_questions_include_canonical_prompts(
    service: LearningCoachService,
) -> None:
    conversation = service.build_conversation(make_full_inputs())
    questions = conversation.suggested_questions
    by_kind = {item.kind: item for item in questions.questions}

    assert by_kind[SuggestedQuestionKind.WHY_NEXT_MISSION].prompt == (
        "Why is this my next mission?"
    )
    assert by_kind[SuggestedQuestionKind.WHAT_IMPROVED].prompt == (
        "What improved this week?"
    )
    assert by_kind[SuggestedQuestionKind.WHY_READINESS].prompt == (
        "Why isn't my readiness higher?"
    )
    assert by_kind[SuggestedQuestionKind.FOCUS_TODAY].prompt == (
        "What should I focus on today?"
    )
    assert by_kind[SuggestedQuestionKind.MISS_SESSION].prompt == (
        "What happens if I miss today's session?"
    )


def test_suggested_question_rationales_are_non_empty(
    service: LearningCoachService,
) -> None:
    conversation = service.build_conversation(make_full_inputs())
    for question in conversation.suggested_questions.questions:
        assert question.rationale.strip()
        assert question.prompt.strip()


def test_empty_inputs_still_offer_focus_and_improvement_questions(
    service: LearningCoachService,
) -> None:
    conversation = service.build_conversation(make_empty_inputs())
    by_kind = {item.kind: item for item in conversation.suggested_questions.questions}
    assert by_kind[SuggestedQuestionKind.FOCUS_TODAY].enabled is True
    assert by_kind[SuggestedQuestionKind.WHAT_IMPROVED].enabled is True
    assert by_kind[SuggestedQuestionKind.WHY_READINESS].enabled is False
