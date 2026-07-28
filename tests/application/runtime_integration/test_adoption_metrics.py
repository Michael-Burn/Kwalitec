"""Adoption metrics coverage tests (RI-002)."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import pytest

from app.application.runtime_integration.adoption_metrics import AdoptionMetricsService
from app.application.runtime_integration.dto import (
    FallbackReason,
    IntegrationSurface,
)
from app.application.runtime_integration.telemetry import RuntimeIntegrationTelemetry
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgGraphEdition
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import SciStudentCurriculumInstance
from app.models.study_plan import StudyPlan
from app.models.user import User


def _user(email: str) -> User:
    u = User(email=email, is_active_user=True)
    u.set_password("password123")
    u.alpha_onboarding_completed = True
    db.session.add(u)
    db.session.commit()
    return u


def _plan(user_id: int) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        archived=False,
    )
    db.session.add(plan)
    db.session.commit()
    return plan


def _edition(subject: str, edition_id: str, *, published: bool) -> CkgGraphEdition:
    row = CkgGraphEdition(
        edition_id=edition_id,
        subject_code=subject,
        edition_label="2026",
        title=f"{subject} edition",
        publication_state="published" if published else "draft",
    )
    db.session.add(row)
    db.session.commit()
    return row


def _sci(student_id: int, edition_id: str, instance_id: str, subject: str) -> None:
    row = SciStudentCurriculumInstance(
        instance_id=instance_id,
        student_id=student_id,
        subject_code=subject,
        edition_id=edition_id,
        is_active=True,
    )
    db.session.add(row)
    db.session.commit()


def _decision(instance_id: str, decision_id: str) -> None:
    now = datetime.now(UTC).replace(tzinfo=None)
    row = EreEducationalDecision(
        decision_id=decision_id,
        instance_id=instance_id,
        decision_type="study_new",
        curriculum_target="CS1.LO1",
        priority=0.8,
        rank_position=1,
        rationale_summary="Study next objective.",
        reasoned_at=now,
    )
    db.session.add(row)
    db.session.commit()


def test_coverage_metrics_from_db(app, db, ctx) -> None:
    a = _user("ri002-a@test.example")
    b = _user("ri002-b@test.example")
    _plan(a.id)
    _plan(b.id)
    published = _edition("CS1", "ed-ri002-cs1", published=True)
    _edition("CM1", "ed-ri002-cm1", published=False)
    _sci(a.id, published.edition_id, "sci-ri002-a", "CS1")
    _decision("sci-ri002-a", "ere-ri002-a")

    svc = AdoptionMetricsService(telemetry=RuntimeIntegrationTelemetry())
    sci = svc.sci_coverage()
    assert sci.numerator == 1
    assert sci.denominator == 2
    assert sci.pct == pytest.approx(50.0)

    pub = svc.published_curriculum_coverage()
    assert pub.numerator == 1
    assert pub.denominator == 2

    decisions = svc.educational_decision_coverage()
    assert decisions.numerator == 1
    assert decisions.denominator == 1


def test_report_includes_telemetry_route_usage(app, db, ctx) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    telemetry.record_educational_intelligence(
        student_id=1,
        subject="CS1",
        surface=IntegrationSurface.DASHBOARD,
        instance_id="sci-1",
        decision_id="ere-1",
        timestamp="2026-07-28T10:00:00Z",
    )
    telemetry.record_fallback(
        student_id=2,
        subject=None,
        reason=FallbackReason.NO_ACTIVE_SCI,
        surface=IntegrationSurface.RECOMMENDATION,
        missing_prerequisite="active_student_curriculum_instance",
        timestamp="2026-07-28T11:00:00Z",
    )
    report = AdoptionMetricsService(telemetry=telemetry).build_report()
    assert report.experience_model_generation_rate == pytest.approx(0.5)
    assert report.runtime_a_fallback_rate == pytest.approx(0.5)
    assert report.educational_intelligence_request_pct == pytest.approx(50.0)
    surfaces = {s.surface for s in report.route_level_usage}
    assert surfaces == {"dashboard", "recommendation"}
    assert "no_active_sci" in report.fallback_by_reason
    assert "2026-07-28" in report.telemetry.daily_ei_counts
