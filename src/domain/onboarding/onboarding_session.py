"""OnboardingSession aggregate — first-run educational evidence collection.

Collects structured declarations only. Does not diagnose, recommend, plan
missions, call AI, or create educational Twin state.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime

from domain.onboarding.enums import (
    COLLECTION_STEPS,
    DiagnosticChoice,
    OnboardingStatus,
    OnboardingStep,
)
from domain.onboarding.errors import OnboardingDomainError, OnboardingInvariantViolation
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.step_payloads import OptionalDiagnosticPayload, StepPayload
from domain.onboarding.step_policy import StepNavigationPolicy


@dataclass(frozen=True, slots=True)
class OnboardingSession:
    """Immutable draft session that advances through collection steps."""

    onboarding_id: OnboardingId
    student_id: StudentId
    status: OnboardingStatus
    current_step: OnboardingStep
    payloads: Mapping[OnboardingStep, StepPayload]
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    saved_steps: frozenset[OnboardingStep] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        object.__setattr__(self, "payloads", dict(self.payloads))
        if self.status is OnboardingStatus.COMPLETED and self.completed_at is None:
            raise OnboardingInvariantViolation(
                "completed sessions require completed_at",
                invariant="completed_at_required",
            )
        if self.current_step not in COLLECTION_STEPS and self.status is (
            OnboardingStatus.IN_PROGRESS
        ):
            raise OnboardingInvariantViolation(
                "in-progress sessions must be on a collection step",
                invariant="current_step_collection",
            )

    @classmethod
    def start(
        cls,
        *,
        onboarding_id: OnboardingId,
        student_id: StudentId,
        now: datetime,
    ) -> OnboardingSession:
        """Open a new incomplete onboarding session at Welcome."""
        return cls(
            onboarding_id=onboarding_id,
            student_id=student_id,
            status=OnboardingStatus.IN_PROGRESS,
            current_step=OnboardingStep.WELCOME,
            payloads={},
            created_at=now,
            updated_at=now,
            completed_at=None,
            saved_steps=frozenset(),
        )

    def assert_in_progress(self) -> None:
        if self.status is not OnboardingStatus.IN_PROGRESS:
            raise OnboardingDomainError(
                f"onboarding is {self.status.value}, not in progress"
            )

    def autosave(
        self,
        step: OnboardingStep,
        payload: StepPayload,
        *,
        now: datetime,
    ) -> OnboardingSession:
        """Persist a step payload without advancing navigation."""
        self.assert_in_progress()
        StepNavigationPolicy.assert_payload_type(step, payload)
        payloads = dict(self.payloads)
        payloads[step] = payload
        return replace(
            self,
            payloads=payloads,
            updated_at=now,
            saved_steps=frozenset(set(self.saved_steps) | {step}),
        )

    def advance(self, *, now: datetime) -> OnboardingSession:
        """Validate the current step and move to the next collection step."""
        self.assert_in_progress()
        payload = self.payloads.get(self.current_step)
        if payload is None:
            raise OnboardingDomainError(
                f"step {self.current_step.value} has not been saved"
            )
        StepNavigationPolicy.assert_payload_type(self.current_step, payload)
        nxt = StepNavigationPolicy.next_step(self.current_step)
        if nxt is None:
            raise OnboardingDomainError("already at the final collection step")
        return replace(self, current_step=nxt, updated_at=now)

    def go_back(self, *, now: datetime) -> OnboardingSession:
        """Move to the previous collection step without clearing drafts."""
        self.assert_in_progress()
        prev = StepNavigationPolicy.previous_step(self.current_step)
        if prev is None:
            raise OnboardingDomainError("already at the first collection step")
        return replace(self, current_step=prev, updated_at=now)

    def skip_optional(self, *, now: datetime) -> OnboardingSession:
        """Skip the optional diagnostic step with an explicit skip declaration."""
        self.assert_in_progress()
        if not StepNavigationPolicy.is_optional(self.current_step):
            raise OnboardingDomainError(
                f"step {self.current_step.value} cannot be skipped"
            )
        skip_payload = OptionalDiagnosticPayload(choice=DiagnosticChoice.SKIPPED)
        saved = self.autosave(self.current_step, skip_payload, now=now)
        return saved.advance(now=now)

    def mark_completed(self, *, now: datetime) -> OnboardingSession:
        """Seal the session after Review confirmation."""
        self.assert_in_progress()
        if self.current_step is not OnboardingStep.REVIEW:
            raise OnboardingDomainError("onboarding can only complete from review")
        for step in COLLECTION_STEPS:
            if step is OnboardingStep.OPTIONAL_DIAGNOSTIC:
                continue
            payload = self.payloads.get(step)
            if payload is None:
                raise OnboardingDomainError(
                    f"required step {step.value} is incomplete"
                )
            StepNavigationPolicy.assert_payload_type(step, payload)
        optional = self.payloads.get(OnboardingStep.OPTIONAL_DIAGNOSTIC)
        if optional is not None:
            StepNavigationPolicy.assert_payload_type(
                OnboardingStep.OPTIONAL_DIAGNOSTIC, optional
            )
        review = self.payloads[OnboardingStep.REVIEW]
        StepNavigationPolicy.assert_payload_type(OnboardingStep.REVIEW, review)
        return replace(
            self,
            status=OnboardingStatus.COMPLETED,
            current_step=OnboardingStep.BUILD_STUDENT_TWIN,
            updated_at=now,
            completed_at=now,
        )

    def require_payload(self, step: OnboardingStep) -> StepPayload:
        payload = self.payloads.get(step)
        if payload is None:
            raise OnboardingDomainError(f"missing payload for {step.value}")
        return payload

    def progress_percent(self) -> float:
        if self.status is OnboardingStatus.COMPLETED:
            return 100.0
        return StepNavigationPolicy.progress_percent(self.current_step)
