"""Unit tests for EQ-001 educational quality domain rules."""

from __future__ import annotations

from datetime import date

from app.domain.educational_quality.rules import (
    build_journey_explanation,
    build_mission_educational_rationale,
    build_prerequisite_validation,
    contains_forbidden_jargon,
    project_study_plan_pacing,
)


def test_mission_rationale_avoids_mastery_claims():
    text = build_mission_educational_rationale(
        topic_code="1.1",
        topic_title="Core",
        objective_codes=("1.1.1",),
        prerequisite_ids=(),
    )
    assert "1.1" in text
    assert "mastery" not in text.lower()
    assert "exam ready" not in text.lower()
    assert not contains_forbidden_jargon(text)


def test_prerequisite_validation():
    result = build_prerequisite_validation(
        required_ids=("t1", "t2"),
        completed_topic_ids=("t1",),
    )
    assert result["all_satisfied"] is False
    assert result["missing_ids"] == ["t2"]
    assert result["satisfied_ids"] == ["t1"]


def test_journey_explanation_answers_three_questions():
    payload = build_journey_explanation(
        current_topic_id="t2",
        current_topic_code="2.1",
        current_topic_title="Applied",
        previous_topic_id="t1",
        previous_topic_code="1.1",
        next_topic_id="t3",
        next_topic_code="3.1",
        next_topic_title="Advanced",
        coverage_ratio=0.33,
        journey_stage="learning",
        syllabus_complete=False,
        completed_count=1,
        total_count=3,
    )
    assert "2.1" in payload["why_today"]
    assert "1.1" in payload["why_previous_complete"]
    assert "3.1" in payload["unlocks_next"]
    assert payload["explanation_schema_complete"] is True


def test_pacing_revision_and_honest_shortfall():
    templates = (
        {"topic_id": "t1", "recommended_minutes": 120},
        {"topic_id": "t2", "recommended_minutes": 120},
    )
    ok = project_study_plan_pacing(
        topic_templates=templates,
        exam_date=date(2026, 12, 1),
        as_of=date(2026, 8, 1),
    )
    assert ok["exam_date_aware"] is True
    assert ok["revision_minutes"] >= 60
    assert ok["feasible"] is True

    tight = project_study_plan_pacing(
        topic_templates=templates,
        exam_date=date(2026, 8, 2),
        as_of=date(2026, 8, 1),
        weekday_minutes=20,
        weekend_minutes=20,
    )
    assert tight["feasible"] is False
    assert tight["shortfall_minutes"] > 0
    assert "silently compressed" in tight["notes"] or "shortfall" in tight["notes"]
