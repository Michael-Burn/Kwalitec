"""Risk summary tests for Exam Readiness Experience (XP-003)."""

from __future__ import annotations

from datetime import time, timedelta

from application.education.revision_planner.enums import SessionStatus
from application.student_experience.readiness import ExamReadinessService, RiskKind
from domain.education.recommendation_engine import RecommendationCategory
from tests.application.student_experience.home.conftest import (
    TODAY,
    make_assessment,
    make_exam_target,
    make_gap,
    make_recommendation,
    make_recommendation_set,
    make_schedule,
    make_session,
)
from tests.application.student_experience.readiness.conftest import (
    make_empty_inputs,
    make_full_inputs,
    make_prerequisite_gap,
)


def test_summarise_risks_covers_expected_kinds(
    service: ExamReadinessService,
) -> None:
    risks = service.summarise_risks(make_full_inputs())
    kinds = {item.kind for item in risks.items}
    assert RiskKind.WEAKEST_COMPETENCY in kinds
    assert RiskKind.INCOMPLETE_PREREQUISITE in kinds
    assert RiskKind.REVISION_GAP in kinds
    assert RiskKind.OVERDUE_MISSION in kinds
    assert risks.has_risks is True


def test_schedule_pressure_when_sessions_exceed_days(
    service: ExamReadinessService,
) -> None:
    exam = make_exam_target(exam_date=TODAY + timedelta(days=5))
    sessions = tuple(
        make_session(
            session_id=f"s-{index}",
            session_date=TODAY + timedelta(days=index),
            mission_ids=(f"mission-{index}",),
            status=SessionStatus.PLANNED,
            start=time(9, 0),
            end=time(9, 30),
        )
        for index in range(8)
    )
    schedule = make_schedule(sessions=sessions, exam_target=exam)
    risks = service.summarise_risks(
        make_empty_inputs(schedule=schedule, exam_target=exam)
    )
    kinds = {item.kind for item in risks.items}
    assert RiskKind.SCHEDULE_PRESSURE in kinds


def test_weakest_competency_from_knowledge_gap(
    service: ExamReadinessService,
) -> None:
    assessment = make_assessment(
        gaps=(make_gap(competency_id="algebra-core", mastery=0.15),),
    )
    risks = service.summarise_risks(make_empty_inputs(assessment=assessment))
    weakest = next(
        item for item in risks.items if item.kind is RiskKind.WEAKEST_COMPETENCY
    )
    assert "Algebra Core" in weakest.message


def test_prerequisite_risk_from_gap(service: ExamReadinessService) -> None:
    assessment = make_assessment(
        gaps=(
            make_prerequisite_gap(
                competency_id="algebra-core",
                related="conditional-probability-core",
            ),
        ),
    )
    risks = service.summarise_risks(make_empty_inputs(assessment=assessment))
    kinds = {item.kind for item in risks.items}
    assert RiskKind.INCOMPLETE_PREREQUISITE in kinds


def test_revision_gap_from_recommendation(service: ExamReadinessService) -> None:
    recommendations = make_recommendation_set(
        (
            make_recommendation(
                category=RecommendationCategory.INCREASE_REVISION_FREQUENCY,
                competency="bayes-theorem",
            ),
        )
    )
    risks = service.summarise_risks(
        make_empty_inputs(recommendation_set=recommendations)
    )
    kinds = {item.kind for item in risks.items}
    assert RiskKind.REVISION_GAP in kinds


def test_risks_empty_without_signals(service: ExamReadinessService) -> None:
    risks = service.summarise_risks(make_empty_inputs())
    assert risks.has_risks is False
    assert "No readiness risks" in risks.summary
