"""Strength summary tests for Exam Readiness Experience (XP-003)."""

from __future__ import annotations

from application.student_experience.progress import TrendDirection
from application.student_experience.readiness import ExamReadinessService, StrengthKind
from tests.application.student_experience.home.conftest import make_assessment
from tests.application.student_experience.readiness.conftest import (
    SUBJECT_PROBABILITY,
    make_empty_inputs,
    make_full_inputs,
    make_minimal_journey_snapshot,
)


def test_summarise_strengths_includes_subjects_and_competencies(
    service: ExamReadinessService,
) -> None:
    strengths = service.summarise_strengths(make_full_inputs())
    kinds = {item.kind for item in strengths.items}
    assert StrengthKind.STRONGEST_SUBJECT in kinds
    assert StrengthKind.STRONGEST_COMPETENCY in kinds
    assert StrengthKind.MISSION_COMPLETION_QUALITY in kinds
    assert strengths.has_strengths is True
    assert any("Conditional Probability" in item.message for item in strengths.items)


def test_recent_improvement_from_journey_snapshot(
    service: ExamReadinessService,
) -> None:
    strengths = service.summarise_strengths(
        make_full_inputs(
            journey_snapshot=make_minimal_journey_snapshot(
                mastery_trend=TrendDirection.IMPROVING
            )
        )
    )
    kinds = {item.kind for item in strengths.items}
    assert StrengthKind.RECENT_IMPROVEMENT in kinds


def test_strengths_empty_without_inputs(service: ExamReadinessService) -> None:
    strengths = service.summarise_strengths(make_empty_inputs())
    assert strengths.has_strengths is False
    assert strengths.items == ()
    assert "will appear" in strengths.summary


def test_strongest_subject_prefers_highest_mastery(
    service: ExamReadinessService,
) -> None:
    assessment = make_assessment(
        subjects=(
            (SUBJECT_PROBABILITY, 0.90),
            ("algebra", 0.30),
        ),
        gaps=(),
        overall_mastery=0.80,
    )
    strengths = service.summarise_strengths(
        make_empty_inputs(assessment=assessment, execution_history=())
    )
    subject = next(
        item
        for item in strengths.items
        if item.kind is StrengthKind.STRONGEST_SUBJECT
    )
    assert subject.scope_label == "Conditional Probability"
