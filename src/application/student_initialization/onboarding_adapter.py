"""Adapter implementing onboarding's ``StudentTwinInitializer`` port."""

from __future__ import annotations

from application.onboarding.ports import StudentTwinInitializer
from application.onboarding.results import (
    CompletedOnboarding,
    StudentTwinInitializationRequest,
)
from application.student_initialization.errors import OnboardingValidationError
from application.student_initialization.ports import Clock
from application.student_initialization.student_initialization_service import (
    StudentInitializationService,
)


class StudentTwinInitializerAdapter(StudentTwinInitializer):
    """Bridge onboarding hand-off cargo into Student Twin Initialization.

    Onboarding emits ``StudentTwinInitializationRequest``; this adapter wraps
    it as ``CompletedOnboarding`` and delegates to ``StudentInitializationService``.
    """

    def __init__(
        self,
        service: StudentInitializationService,
        clock: Clock,
    ) -> None:
        self._service = service
        self._clock = clock

    def initialize(self, request: StudentTwinInitializationRequest) -> str:
        if not isinstance(request, StudentTwinInitializationRequest):
            raise OnboardingValidationError(
                "expected StudentTwinInitializationRequest"
            )
        completed = CompletedOnboarding(
            onboarding_id=request.onboarding_id,
            student_id=request.student_id,
            completed_at=self._clock.now(),
            twin_initialization=request,
        )
        result = self._service.initialize(completed)
        return result.twin_id
