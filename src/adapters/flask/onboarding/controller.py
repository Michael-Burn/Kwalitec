"""OnboardingController — Flask-free orchestration for onboarding use-cases."""

from __future__ import annotations

from typing import Any

from adapters.flask.onboarding.dependency_provider import OnboardingAdapterDependencies
from application.onboarding.errors import OnboardingApplicationError
from application.onboarding.onboarding_service import OnboardingService
from application.onboarding.requests import (
    AdvanceStepRequest,
    CompleteOnboardingRequest,
    GoBackRequest,
    ResumeOnboardingRequest,
    SaveStepRequest,
    SkipOptionalRequest,
    StartOnboardingRequest,
)
from application.onboarding.results import OnboardingResult
from presentation.onboarding import OnboardingPresenter, OnboardingViewModel


class OnboardingController:
    """Invoke onboarding application services and present view models."""

    def __init__(self, dependencies: OnboardingAdapterDependencies) -> None:
        self._dependencies = dependencies

    @property
    def service(self) -> OnboardingService:
        service = self._dependencies.onboarding_service
        if service is None:
            raise RuntimeError("onboarding service is not configured")
        return service

    def start(self, *, student_id: str) -> OnboardingResult:
        return self.service.start(StartOnboardingRequest(student_id=student_id))

    def resume(self, *, student_id: str) -> OnboardingResult:
        return self.service.resume(ResumeOnboardingRequest(student_id=student_id))

    def save_step(
        self,
        *,
        onboarding_id: str,
        student_id: str,
        step: str,
        payload: dict[str, Any],
    ) -> OnboardingResult:
        return self.service.save_step(
            SaveStepRequest(
                onboarding_id=onboarding_id,
                student_id=student_id,
                step=step,
                payload=payload,
            )
        )

    def advance(self, *, onboarding_id: str, student_id: str) -> OnboardingResult:
        return self.service.advance(
            AdvanceStepRequest(onboarding_id=onboarding_id, student_id=student_id)
        )

    def go_back(self, *, onboarding_id: str, student_id: str) -> OnboardingResult:
        return self.service.go_back(
            GoBackRequest(onboarding_id=onboarding_id, student_id=student_id)
        )

    def skip_optional(
        self, *, onboarding_id: str, student_id: str
    ) -> OnboardingResult:
        return self.service.skip_optional(
            SkipOptionalRequest(onboarding_id=onboarding_id, student_id=student_id)
        )

    def complete(self, *, onboarding_id: str, student_id: str) -> OnboardingResult:
        return self.service.complete(
            CompleteOnboardingRequest(
                onboarding_id=onboarding_id, student_id=student_id
            )
        )

    def present(self, result: OnboardingResult) -> OnboardingViewModel:
        return OnboardingPresenter.present(
            result.snapshot,
            completed=result.completed,
        )


def onboarding_error_message(exc: Exception) -> str:
    if isinstance(exc, OnboardingApplicationError):
        return exc.message
    return "onboarding could not continue"
