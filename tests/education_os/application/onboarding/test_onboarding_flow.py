"""Step navigation, autosave, resume, validation, and Twin initialization (BR-002)."""

from __future__ import annotations

import pytest

from application.onboarding.errors import OnboardingApplicationError
from application.onboarding.requests import (
    AdvanceStepRequest,
    CompleteOnboardingRequest,
    GoBackRequest,
    ResumeOnboardingRequest,
    SaveStepRequest,
    SkipOptionalRequest,
    StartOnboardingRequest,
)
from domain.onboarding.enums import OnboardingStatus, OnboardingStep
from tests.education_os.application.onboarding.conftest import full_payloads


def test_start_creates_welcome_session(onboarding_service) -> None:
    result = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert result.success
    assert result.snapshot is not None
    assert result.snapshot.current_step is OnboardingStep.WELCOME
    assert result.snapshot.status is OnboardingStatus.IN_PROGRESS


def test_start_resumes_incomplete(onboarding_service) -> None:
    first = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    second = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert first.snapshot is not None
    assert second.snapshot is not None
    assert second.snapshot.onboarding_id == first.snapshot.onboarding_id
    assert "resumed" in second.message


def test_autosave_persists_without_advancing(onboarding_service) -> None:
    started = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    saved = onboarding_service.save_step(
        SaveStepRequest(
            onboarding_id=oid,
            student_id="stu-1",
            step="welcome",
            payload={"acknowledged": True},
        )
    )
    assert saved.snapshot is not None
    assert saved.snapshot.current_step is OnboardingStep.WELCOME
    assert "welcome" in saved.snapshot.saved_steps
    assert saved.snapshot.payloads["welcome"]["acknowledged"] is True


def test_advance_requires_saved_payload(onboarding_service) -> None:
    started = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert started.snapshot is not None
    with pytest.raises(OnboardingApplicationError):
        onboarding_service.advance(
            AdvanceStepRequest(
                onboarding_id=started.snapshot.onboarding_id,
                student_id="stu-1",
            )
        )


def test_step_navigation_forward_and_back(onboarding_service) -> None:
    started = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    onboarding_service.save_step(
        SaveStepRequest(
            onboarding_id=oid,
            student_id="stu-1",
            step="welcome",
            payload={"acknowledged": True},
        )
    )
    advanced = onboarding_service.advance(
        AdvanceStepRequest(onboarding_id=oid, student_id="stu-1")
    )
    assert advanced.snapshot is not None
    assert advanced.snapshot.current_step is OnboardingStep.IFOA_PROFILE
    back = onboarding_service.go_back(
        GoBackRequest(onboarding_id=oid, student_id="stu-1")
    )
    assert back.snapshot is not None
    assert back.snapshot.current_step is OnboardingStep.WELCOME


def test_validation_rejects_invalid_exam_history(onboarding_service) -> None:
    started = onboarding_service.start(StartOnboardingRequest(student_id="stu-1"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    with pytest.raises(OnboardingApplicationError):
        onboarding_service.save_step(
            SaveStepRequest(
                onboarding_id=oid,
                student_id="stu-1",
                step="exam_history",
                payload={
                    "prior_study": "first_time",
                    "core_reading": "none",
                    "previous_attempts": 2,
                    "sitting_intent": "first_sit",
                },
            )
        )


def test_skip_optional_diagnostic(onboarding_service) -> None:
    service = onboarding_service
    started = service.start(StartOnboardingRequest(student_id="stu-1"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    payloads = full_payloads()
    for step in (
        "welcome",
        "ifoa_profile",
        "exam_history",
        "weekly_availability",
        "confidence",
        "study_habits",
    ):
        service.save_step(
            SaveStepRequest(
                onboarding_id=oid,
                student_id="stu-1",
                step=step,
                payload=payloads[step],
            )
        )
        service.advance(AdvanceStepRequest(onboarding_id=oid, student_id="stu-1"))
    skipped = service.skip_optional(
        SkipOptionalRequest(onboarding_id=oid, student_id="stu-1")
    )
    assert skipped.snapshot is not None
    assert skipped.snapshot.current_step is OnboardingStep.REVIEW
    assert skipped.snapshot.payloads["optional_diagnostic"]["choice"] == "skipped"


def test_resume_incomplete(onboarding_service) -> None:
    started = onboarding_service.start(StartOnboardingRequest(student_id="stu-2"))
    assert started.snapshot is not None
    resumed = onboarding_service.resume(ResumeOnboardingRequest(student_id="stu-2"))
    assert resumed.snapshot is not None
    assert resumed.snapshot.onboarding_id == started.snapshot.onboarding_id


def test_complete_emits_twin_initialization(
    onboarding_service, twin_initializer
) -> None:
    service = onboarding_service
    started = service.start(StartOnboardingRequest(student_id="stu-3"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    payloads = full_payloads()
    for step in (
        "welcome",
        "ifoa_profile",
        "exam_history",
        "weekly_availability",
        "confidence",
        "study_habits",
        "optional_diagnostic",
    ):
        service.save_step(
            SaveStepRequest(
                onboarding_id=oid,
                student_id="stu-3",
                step=step,
                payload=payloads[step],
            )
        )
        service.advance(AdvanceStepRequest(onboarding_id=oid, student_id="stu-3"))
    service.save_step(
        SaveStepRequest(
            onboarding_id=oid,
            student_id="stu-3",
            step="review",
            payload=payloads["review"],
        )
    )
    completed = service.complete(
        CompleteOnboardingRequest(onboarding_id=oid, student_id="stu-3")
    )
    assert completed.success
    assert completed.completed is not None
    assert completed.completed.twin_id == "twin-1"
    assert completed.completed.redirect_path == "/eos/dashboard/"
    init = completed.completed.twin_initialization
    assert init.student_id == "stu-3"
    assert init.exam_paper == "CS1"
    assert init.pathway == "core_principles"
    assert init.declaration_confirmation is True
    assert len(twin_initializer.requests) == 1
    assert twin_initializer.requests[0].exam_paper == "CS1"


def test_end_to_end_onboarding_flow(onboarding_service, twin_initializer) -> None:
    """Full collection → Twin initialization → dashboard redirect cargo."""
    service = onboarding_service
    started = service.start(StartOnboardingRequest(student_id="stu-e2e"))
    assert started.snapshot is not None
    oid = started.snapshot.onboarding_id
    payloads = full_payloads()
    order = (
        "welcome",
        "ifoa_profile",
        "exam_history",
        "weekly_availability",
        "confidence",
        "study_habits",
        "optional_diagnostic",
        "review",
    )
    for index, step in enumerate(order):
        service.save_step(
            SaveStepRequest(
                onboarding_id=oid,
                student_id="stu-e2e",
                step=step,
                payload=payloads[step],
            )
        )
        if step == "review":
            result = service.complete(
                CompleteOnboardingRequest(onboarding_id=oid, student_id="stu-e2e")
            )
        else:
            result = service.advance(
                AdvanceStepRequest(onboarding_id=oid, student_id="stu-e2e")
            )
        assert result.success, step
        if index < len(order) - 1:
            assert result.snapshot is not None
            assert result.snapshot.current_step.value == order[index + 1]
    assert result.completed is not None
    assert result.completed.twin_initialization.contract_version == "1.0"
    assert twin_initializer.requests
