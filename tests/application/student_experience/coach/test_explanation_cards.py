"""Explanation card tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import (
    ExplanationCardKind,
    LearningCoachService,
)
from tests.application.student_experience.coach.conftest import (
    make_empty_inputs,
    make_full_inputs,
)
from tests.application.student_experience.home.conftest import make_evaluation


def test_mission_purpose_card_explains_current_mission(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs())
    card = context.explanation_cards.by_kind(ExplanationCardKind.MISSION_PURPOSE)
    assert card is not None
    assert "mission" in card.title.lower() or "purpose" in card.title.lower()
    assert card.body.strip()


def test_recommendation_rationale_uses_evaluation_decision(
    service: LearningCoachService,
) -> None:
    context = service.build_context(
        make_full_inputs(evaluation=make_evaluation())
    )
    card = context.explanation_cards.by_kind(
        ExplanationCardKind.RECOMMENDATION_RATIONALE
    )
    assert card is not None
    assert "recommendation" in card.title.lower()
    assert "focus competency" in card.body.lower() or "gap" in card.body.lower()


def test_empty_inputs_omit_most_explanation_cards(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_empty_inputs())
    assert len(context.explanation_cards.cards) == 0
