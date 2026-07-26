"""Unit tests — JourneyContextAssembler (P2-MS002)."""

from __future__ import annotations

import pytest

from app.application.unified_journey import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_PLACEHOLDER,
    SOURCE_ADAPTIVE,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
    JourneyContext,
    JourneyContextAssembler,
    JourneyStage,
    JourneySubsystemInputs,
    NextBestAction,
    empty_journey_context,
)


@pytest.fixture
def assembler() -> JourneyContextAssembler:
    return JourneyContextAssembler()


def test_assemble_placeholder_when_no_inputs(assembler):
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
    )
    assert isinstance(context, JourneyContext)
    assert context.availability == AVAILABILITY_PLACEHOLDER
    assert context.source == "placeholder"
    assert context.mission_title == "Today's primary mission"
    assert context.cta_enabled is False
    assert context.endpoint == "student.home"


def test_assemble_from_runtime_a_recommendation(assembler):
    inputs = JourneySubsystemInputs(
        runtime_a={
            "title": "Practice differentials",
            "why_it_matters": "Builds exam-critical fluency",
            "expected_outcome": "Higher readiness on Topic B",
            "estimated_minutes": 30,
            "cta_label": "Start Today's Session",
            "endpoint": "student.start_session",
            "completion_state": "not_started",
            "urgency": "normal",
        }
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert context.availability == AVAILABILITY_AVAILABLE
    assert context.source == SOURCE_RUNTIME_A
    assert context.mission_title == "Practice differentials"
    assert context.mission_reason == "Builds exam-critical fluency"
    assert context.estimated_duration == "30 minutes"
    assert context.expected_outcome == "Higher readiness on Topic B"
    assert context.completion_state == "not_started"
    assert context.urgency == "normal"
    assert context.cta_enabled is True
    assert context.endpoint == "student.start_session"


def test_assemble_prefers_stage_primary_subsystem(assembler):
    # Daily mission primary is Runtime A — even if Strategy also has a title.
    inputs = JourneySubsystemInputs(
        runtime_a={"title": "Runtime mission", "estimated_minutes": 20},
        strategy={"title": "Strategy intervention", "estimated_minutes": 45},
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert context.source == SOURCE_RUNTIME_A
    assert context.mission_title == "Runtime mission"


def test_assemble_revision_prefers_adaptive(assembler):
    inputs = JourneySubsystemInputs(
        runtime_a={"title": "Runtime mission"},
        adaptive={
            "title": "Revise Topic A",
            "why_it_matters": "Spaced review window",
            "estimated_minutes": 25,
        },
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.REVISION_MODE,
        inputs=inputs,
    )
    assert context.source == SOURCE_ADAPTIVE
    assert context.mission_title == "Revise Topic A"
    assert context.estimated_duration == "25 minutes"


def test_assemble_nested_next_action_payload(assembler):
    inputs = JourneySubsystemInputs(
        strategy={
            "next_action": {
                "title": "Recovery focus",
                "why_it_matters": "Fatigue recovery",
                "expected_outcome": "Sustainable pace",
                "estimated_minutes": 15,
            }
        }
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.EXAM_READINESS,
        inputs=inputs,
    )
    assert context.source == SOURCE_STRATEGY
    assert context.mission_title == "Recovery focus"
    assert context.mission_reason == "Fatigue recovery"


def test_assemble_supporting_insights_from_twin_and_evidence(assembler):
    inputs = JourneySubsystemInputs(
        runtime_a={"title": "Mission"},
        digital_twin={
            "explanation_summary": {
                "why_summary": "Consistent study rhythm this week",
                "facet_explanation_summaries": ["Load remains manageable"],
            }
        },
        evidence={"summary": "Three sessions completed"},
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert "Consistent study rhythm this week" in context.supporting_insights
    assert "Load remains manageable" in context.supporting_insights
    assert "Three sessions completed" in context.supporting_insights


def test_assemble_partial_projection_without_title(assembler):
    inputs = JourneySubsystemInputs(
        runtime_a={"estimated_minutes": 10, "urgency": "high"},
        digital_twin={"insight": "Keep sessions short"},
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert context.availability == AVAILABILITY_PLACEHOLDER
    assert context.mission_title == ""
    assert context.estimated_duration == "10 minutes"
    assert context.urgency == "high"
    assert "Keep sessions short" in context.supporting_insights


def test_assemble_null_subsystem_maps(assembler):
    inputs = JourneySubsystemInputs(
        runtime_a={},
        adaptive={},
        strategy={},
        digital_twin={},
        evidence={},
    )
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert context.availability == AVAILABILITY_PLACEHOLDER
    assert context.supporting_insights == ()


def test_assemble_passes_through_explicit_context(assembler):
    provided = JourneyContext(
        stage=JourneyStage.PLANNING,
        mission_title="Finish plan",
        source=SOURCE_RUNTIME_A,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )
    inputs = JourneySubsystemInputs(journey_context=provided)
    assert (
        assembler.assemble(
            student_id="42",
            stage=JourneyStage.PLANNING,
            inputs=inputs,
        )
        is provided
    )


def test_assemble_from_explicit_next_action(assembler):
    action = NextBestAction(
        action_id="adaptive.1",
        stage=JourneyStage.REVISION_MODE,
        title="Revise equity",
        why_it_matters="High return",
        expected_outcome="Retention",
        estimated_minutes=20,
        cta_label="Begin Revision",
        endpoint="student.revision",
        source=SOURCE_ADAPTIVE,
        availability=AVAILABILITY_AVAILABLE,
    )
    inputs = JourneySubsystemInputs(next_action=action)
    context = assembler.assemble(
        student_id="42",
        stage=JourneyStage.REVISION_MODE,
        inputs=inputs,
    )
    assert context.mission_title == "Revise equity"
    assert context.source == SOURCE_ADAPTIVE
    assert context.estimated_duration == "20 minutes"


def test_empty_journey_context_helper():
    context = empty_journey_context(stage=JourneyStage.WEEKLY_REVIEW)
    assert context.stage is JourneyStage.WEEKLY_REVIEW
    assert context.availability == AVAILABILITY_PLACEHOLDER


def test_assembler_rejects_empty_student_id(assembler):
    with pytest.raises(ValueError):
        assembler.assemble(student_id="", stage=JourneyStage.DAILY_MISSION)


def test_assembler_does_not_mutate_inputs(assembler):
    payload = {"title": "Mission", "estimated_minutes": 12}
    inputs = JourneySubsystemInputs(runtime_a=payload)
    assembler.assemble(
        student_id="42",
        stage=JourneyStage.DAILY_MISSION,
        inputs=inputs,
    )
    assert payload == {"title": "Mission", "estimated_minutes": 12}
