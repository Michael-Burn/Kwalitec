"""Presenter behaviour for Student Onboarding (BR-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.onboarding.results import (
    CompletedOnboarding,
    OnboardingSnapshot,
    StudentTwinInitializationRequest,
)
from domain.onboarding.enums import OnboardingStatus, OnboardingStep
from presentation.onboarding import OnboardingPresenter


def test_presenter_builds_progress_and_stepper() -> None:
    snapshot = OnboardingSnapshot(
        onboarding_id="ob-1",
        student_id="stu-1",
        status=OnboardingStatus.IN_PROGRESS,
        current_step=OnboardingStep.CONFIDENCE,
        progress_percent=57.14,
        payloads={"confidence": {"band": "moderate"}},
        saved_steps=("welcome", "ifoa_profile"),
        updated_at=datetime(2026, 7, 20, tzinfo=UTC),
    )
    view = OnboardingPresenter.present(snapshot)
    assert view.current_step.key == "confidence"
    assert view.progress_bar.percent == 57.14
    assert any(step.current for step in view.stepper.steps)
    assert view.primary_action_key == "advance"


def test_review_step_uses_complete_action() -> None:
    snapshot = OnboardingSnapshot(
        onboarding_id="ob-1",
        student_id="stu-1",
        status=OnboardingStatus.IN_PROGRESS,
        current_step=OnboardingStep.REVIEW,
        progress_percent=100.0,
        payloads={
            "ifoa_profile": {"exam_paper": "CS1", "pathway": "core_principles"},
        },
        saved_steps=("welcome", "ifoa_profile"),
        updated_at=datetime(2026, 7, 20, tzinfo=UTC),
    )
    view = OnboardingPresenter.present(snapshot)
    assert view.primary_action_key == "complete"
    assert view.review_lines


def test_completed_view_marks_redirect() -> None:
    completed = CompletedOnboarding(
        onboarding_id="ob-1",
        student_id="stu-1",
        completed_at=datetime(2026, 7, 20, tzinfo=UTC),
        twin_initialization=StudentTwinInitializationRequest(
            student_id="stu-1",
            onboarding_id="ob-1",
            pathway="core_principles",
            exam_paper="CS1",
            intended_sitting_label="",
            prior_study="first_time",
            core_reading="none",
            previous_attempts=0,
            sitting_intent="first_sit",
            weekday_minutes=60,
            weekend_minutes=60,
            preferred_session_minutes=45,
            confidence_band="moderate",
            confidence_notes="",
            study_habit_preference="mixed",
            typical_start_time="",
            diagnostic_choice="skipped",
        ),
        twin_id="twin-9",
        redirect_path="/eos/dashboard/",
    )
    view = OnboardingPresenter.present(None, completed=completed)
    assert view.is_complete
    assert view.redirect_path == "/eos/dashboard/"
    assert view.progress_percent == 100.0
