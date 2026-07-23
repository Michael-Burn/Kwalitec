"""Snapshot tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import CoachSnapshotId, LearningCoachService
from tests.application.student_experience.coach.conftest import (
    STUDENT_ID,
    make_full_inputs,
)


def test_build_snapshot_projects_compact_fields(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs(), coach_id="coach-snap")
    conversation = service.build_conversation(make_full_inputs(), context=context)
    reflection = service.build_reflection(make_full_inputs())
    snapshot = service.build_snapshot(
        context,
        snapshot_id=CoachSnapshotId("csnap-001"),
        suggested_question_count=len(conversation.suggested_questions.questions),
        reflection_prompt_count=len(reflection.prompts),
    )

    assert snapshot.snapshot_id.value == "csnap-001"
    assert snapshot.student_id == STUDENT_ID
    assert snapshot.focus_headline == context.current_focus.headline
    assert snapshot.readiness_label == context.readiness.readiness_label
    assert snapshot.journey_message == context.learning_journey.trajectory_message
    assert snapshot.explanation_card_count == len(context.explanation_cards.cards)
    assert snapshot.suggested_question_count == 5
    assert snapshot.reflection_prompt_count == len(reflection.prompts)
    assert snapshot.celebration_count == len(context.celebration_moments.moments)
    assert snapshot.improvement_count == len(context.recent_improvements)
    assert snapshot.risk_count == len(context.current_risks)
    assert snapshot.milestone_count == len(context.upcoming_milestones)


def test_deterministic_snapshot_id(service: LearningCoachService) -> None:
    context = service.build_context(make_full_inputs(), coach_id="coach-det")
    snapshot = service.build_snapshot(context)
    assert snapshot.snapshot_id.value.startswith("csnap:coach-det:")
