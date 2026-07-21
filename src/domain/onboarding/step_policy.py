"""Step ordering and completion policies for onboarding.

Deterministic navigation rules. No educational recommendations.
"""

from __future__ import annotations

from domain.onboarding.enums import COLLECTION_STEPS, OnboardingStep
from domain.onboarding.errors import OnboardingDomainError, OnboardingValidationError
from domain.onboarding.step_payloads import (
    ConfidencePayload,
    ExamHistoryPayload,
    IfoaProfilePayload,
    OptionalDiagnosticPayload,
    ReviewPayload,
    StepPayload,
    StudyHabitsPayload,
    WeeklyAvailabilityPayload,
    WelcomePayload,
)

_PAYLOAD_TYPES: dict[OnboardingStep, type[StepPayload]] = {
    OnboardingStep.WELCOME: WelcomePayload,
    OnboardingStep.IFOA_PROFILE: IfoaProfilePayload,
    OnboardingStep.EXAM_HISTORY: ExamHistoryPayload,
    OnboardingStep.WEEKLY_AVAILABILITY: WeeklyAvailabilityPayload,
    OnboardingStep.CONFIDENCE: ConfidencePayload,
    OnboardingStep.STUDY_HABITS: StudyHabitsPayload,
    OnboardingStep.OPTIONAL_DIAGNOSTIC: OptionalDiagnosticPayload,
    OnboardingStep.REVIEW: ReviewPayload,
}


class StepNavigationPolicy:
    """Ordered navigation across collection steps."""

    @staticmethod
    def collection_steps() -> tuple[OnboardingStep, ...]:
        return COLLECTION_STEPS

    @staticmethod
    def index_of(step: OnboardingStep) -> int:
        try:
            return COLLECTION_STEPS.index(step)
        except ValueError as exc:
            raise OnboardingDomainError(
                f"step {step.value!r} is not a collection step"
            ) from exc

    @classmethod
    def next_step(cls, step: OnboardingStep) -> OnboardingStep | None:
        index = cls.index_of(step)
        if index + 1 >= len(COLLECTION_STEPS):
            return None
        return COLLECTION_STEPS[index + 1]

    @classmethod
    def previous_step(cls, step: OnboardingStep) -> OnboardingStep | None:
        index = cls.index_of(step)
        if index <= 0:
            return None
        return COLLECTION_STEPS[index - 1]

    @classmethod
    def progress_percent(cls, step: OnboardingStep) -> float:
        index = cls.index_of(step)
        total = len(COLLECTION_STEPS)
        if total <= 1:
            return 100.0
        return round((index / (total - 1)) * 100.0, 2)

    @staticmethod
    def is_optional(step: OnboardingStep) -> bool:
        return step is OnboardingStep.OPTIONAL_DIAGNOSTIC

    @staticmethod
    def assert_payload_type(step: OnboardingStep, payload: StepPayload) -> None:
        expected = _PAYLOAD_TYPES.get(step)
        if expected is None:
            raise OnboardingDomainError(
                f"step {step.value!r} does not accept a payload"
            )
        if not isinstance(payload, expected):
            raise OnboardingValidationError(
                f"payload type {type(payload).__name__} is invalid for {step.value}",
                step=step.value,
            )
        payload.validate()
