"""FV-001 founder validation metrics and workflow tests."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.founder_validation.metrics_service import (
    FounderValidationMetricsService,
)
from app.application.founder_validation.telemetry import (
    FounderValidationTelemetry,
    decision_refresh_ms_from_result,
)
from app.application.founder_validation.workflows import (
    VERSION_1_STUDENT_JOURNEY,
    workflow_catalogue,
    workflow_ids,
)
from app.application.learner_lifecycle.dto import StageExecutionRecord
from app.application.learner_lifecycle.stages import LifecycleStage
from app.application.runtime_integration.dto import (
    FallbackReason,
    IntegrationSurface,
)
from app.application.runtime_integration.telemetry import RuntimeIntegrationTelemetry
from app.extensions import db
from app.models.learner_lifecycle import LlpLifecycleOperation
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.subject import Subject
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


def _subject(user_id: int) -> Subject:
    row = Subject(user_id=user_id, name="CS1", colour="#336699", active=True)
    db.session.add(row)
    db.session.commit()
    return row


def _mission(user_id: int, subject_id: int, *, status: str) -> Mission:
    m = Mission(
        user_id=user_id,
        subject_id=subject_id,
        mission_date=date.today(),
        title="FV mission",
        status=status,
    )
    db.session.add(m)
    db.session.commit()
    return m


def _llp(
    *,
    operation_id: str,
    operation_type: str,
    status: str,
    student_id: int,
) -> None:
    row = LlpLifecycleOperation(
        operation_id=operation_id,
        operation_type=operation_type,
        status=status,
        student_id=student_id,
        instance_id=f"sci-{operation_id}",
        completed_stages_json="[]",
        attempt_count=1,
        orchestrator_version="llp.v1",
    )
    db.session.add(row)
    db.session.commit()


def test_workflow_catalogue_covers_version_1_journey():
    ids = workflow_ids()
    assert "study_plan" in ids
    assert "study_session" in ids
    assert "educational_decisions" in ids
    assert "revision_planner" in ids
    assert len(VERSION_1_STUDENT_JOURNEY) == len(workflow_catalogue())
    assert len(ids) >= 12


def test_decision_refresh_ms_from_result():
    class _Result:
        stages = (
            StageExecutionRecord(
                stage=LifecycleStage.TWIN_BELIEFS,
                succeeded=True,
                attempts=1,
                duration_ms=10.0,
            ),
            StageExecutionRecord(
                stage=LifecycleStage.EDUCATIONAL_DECISIONS,
                succeeded=True,
                attempts=1,
                duration_ms=42.5,
            ),
        )

    assert decision_refresh_ms_from_result(_Result()) == pytest.approx(42.5)


def test_metrics_report_from_llp_missions_and_ris(ctx):
    user = _user("fv001-metrics@example.com")
    _plan(user.id)
    subject = _subject(user.id)
    _mission(user.id, subject.id, status="Completed")
    _mission(user.id, subject.id, status="Pending")
    _llp(
        operation_id="op-onboard-ok",
        operation_type="onboard",
        status="completed",
        student_id=user.id,
    )
    _llp(
        operation_id="op-onboard-fail",
        operation_type="onboard",
        status="failed",
        student_id=user.id,
    )
    _llp(
        operation_id="op-evidence-ok",
        operation_type="evidence_refresh",
        status="completed",
        student_id=user.id,
    )

    ris = RuntimeIntegrationTelemetry()
    ris.record_educational_intelligence(
        student_id=user.id,
        subject="CS1",
        surface=IntegrationSurface.DASHBOARD,
        instance_id="sci-1",
        decision_id="dec-1",
    )
    ris.record_fallback(
        student_id=user.id,
        subject="CS1",
        reason=FallbackReason.NO_ACTIVE_SCI,
        surface=IntegrationSurface.DASHBOARD,
    )

    fv = FounderValidationTelemetry()
    fv.record_lifecycle_outcome(
        kind="evidence",
        succeeded=True,
        student_id=user.id,
        decision_refresh_ms=55.0,
    )
    fv.record_lifecycle_outcome(
        kind="evidence",
        succeeded=True,
        student_id=user.id,
        decision_refresh_ms=45.0,
    )

    report = FounderValidationMetricsService(
        ris_telemetry=ris,
        fv_telemetry=fv,
    ).build_report()

    assert report.onboarding_completion.numerator == 1
    assert report.onboarding_completion.denominator == 2
    assert report.evidence_recording_success.numerator == 1
    assert report.evidence_recording_success.denominator == 1
    assert report.session_completion.numerator == 1
    assert report.session_completion.denominator == 2
    assert report.experience_model_generation.numerator == 1
    assert report.runtime_a_fallback.numerator == 1
    assert report.decision_refresh_latency.sample_count == 2
    assert report.decision_refresh_latency.mean_ms == pytest.approx(50.0)
    assert report.system_failures == 0


def test_fv_metrics_cli(runner, ctx):
    result = runner.invoke(args=["fv-metrics", "--compact"])
    assert result.exit_code == 0, result.output
    assert "FV-001" in result.output
    assert "workflows" in result.output
    assert "onboarding_completion" in result.output
