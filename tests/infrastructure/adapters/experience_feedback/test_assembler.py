"""Assembler tests — Experience Feedback Loop (P2-MS008)."""

from __future__ import annotations

from app.infrastructure.adapters.evidence_platform.contracts import (
    EvidenceFactualSummary,
)
from app.infrastructure.adapters.experience_feedback import (
    DEFAULT_SOURCE_DESCRIPTION,
    ExperienceFeedbackAssembler,
    build_experience_feedback_assembler,
)


def _summary(**overrides) -> EvidenceFactualSummary:
    base = dict(
        summary_id="evfact-1",
        student_id="42",
        reporting_period="this_week",
        completed_missions=3,
        completed_reflections=2,
        study_sessions=3,
        active_streak=4,
        generated_at="2026-07-25T12:00:00+00:00",
        evidence_refs=("e1", "e2"),
        source_description=DEFAULT_SOURCE_DESCRIPTION,
        provenance={"source_service": "evidence_factual_query"},
    )
    base.update(overrides)
    return EvidenceFactualSummary(**base)


def test_build_assembler_respects_enabled_flag():
    assert build_experience_feedback_assembler(enabled=False) is None
    assert isinstance(
        build_experience_feedback_assembler(enabled=True),
        ExperienceFeedbackAssembler,
    )


def test_assemble_maps_factual_fields_only():
    assembler = ExperienceFeedbackAssembler()
    feedback = assembler.assemble(_summary())
    assert feedback.completed_missions == 3
    assert feedback.completed_reflections == 2
    assert feedback.study_sessions == 3
    assert feedback.active_streak == 4
    assert feedback.evidence_summary_id == "evfact-1"
    assert feedback.evidence_refs == ("e1", "e2")
    assert feedback.source_description == DEFAULT_SOURCE_DESCRIPTION
    assert "mastery" not in feedback.serialize()
    assert "score" not in feedback.serialize()
    assert "recommendation" not in feedback.serialize()


def test_assemble_formats_presentation_facts_with_explainability():
    assembler = ExperienceFeedbackAssembler()
    feedback = assembler.assemble(_summary())
    keys = {fact.key for fact in feedback.facts}
    assert keys == {
        "completed_missions",
        "study_sessions",
        "completed_reflections",
        "active_streak",
    }
    for fact in feedback.facts:
        assert fact.source_description == DEFAULT_SOURCE_DESCRIPTION
        assert fact.label
        assert fact.value_label
    mission = next(f for f in feedback.facts if f.key == "completed_missions")
    assert "this week" in mission.label.lower()
    streak = next(f for f in feedback.facts if f.key == "active_streak")
    assert streak.value_label == "4 days"


def test_assemble_preserves_evidence_provenance():
    assembler = ExperienceFeedbackAssembler()
    feedback = assembler.assemble(_summary())
    assert feedback.provenance["via"] == "experience_feedback_assembler"
    assert feedback.provenance["evidence_summary_id"] == "evfact-1"
    assert feedback.provenance["evidence_provenance"]["source_service"] == (
        "evidence_factual_query"
    )


def test_assemble_does_not_invent_metrics():
    """Assembler must copy Evidence counts — never recompute."""
    assembler = ExperienceFeedbackAssembler()
    feedback = assembler.assemble(
        _summary(
            completed_missions=1,
            study_sessions=9,
            completed_reflections=0,
            active_streak=0,
        )
    )
    assert feedback.completed_missions == 1
    assert feedback.study_sessions == 9
    assert feedback.completed_reflections == 0
    assert feedback.active_streak == 0
    streak = next(f for f in feedback.facts if f.key == "active_streak")
    assert streak.value_label == "No active streak"
