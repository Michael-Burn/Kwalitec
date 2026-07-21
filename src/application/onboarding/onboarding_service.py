"""OnboardingService — first-run evidence collection and Twin initialization handoff.

Framework-independent. Autosaves each step, resumes incomplete sessions, and
emits ``CompletedOnboarding`` + ``StudentTwinInitializationRequest``.

Forbidden: educational recommendations, mission planning, AI, Flask,
SQLAlchemy imports.
"""

from __future__ import annotations

from application.onboarding.errors import OnboardingApplicationError
from application.onboarding.payload_mapper import build_payload, parse_step
from application.onboarding.ports import (
    Clock,
    OnboardingIdGenerator,
    OnboardingRepository,
    StudentTwinInitializer,
)
from application.onboarding.requests import (
    AdvanceStepRequest,
    CompleteOnboardingRequest,
    GoBackRequest,
    ResumeOnboardingRequest,
    SaveStepRequest,
    SkipOptionalRequest,
    StartOnboardingRequest,
)
from application.onboarding.results import (
    CompletedOnboarding,
    OnboardingResult,
    OnboardingSnapshot,
    StudentTwinInitializationRequest,
)
from domain.onboarding.enums import (
    DiagnosticChoice,
    OnboardingStatus,
    OnboardingStep,
)
from domain.onboarding.errors import OnboardingDomainError, OnboardingValidationError
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession
from domain.onboarding.step_payloads import (
    ConfidencePayload,
    ExamHistoryPayload,
    IfoaProfilePayload,
    OptionalDiagnosticPayload,
    StudyHabitsPayload,
    WeeklyAvailabilityPayload,
)

DASHBOARD_REDIRECT_PATH = "/eos/dashboard/"


class OnboardingService:
    """Orchestrate onboarding collection and Student Twin initialization request."""

    def __init__(
        self,
        *,
        repository: OnboardingRepository,
        twin_initializer: StudentTwinInitializer,
        clock: Clock,
        id_generator: OnboardingIdGenerator,
    ) -> None:
        self._repository = repository
        self._twin_initializer = twin_initializer
        self._clock = clock
        self._id_generator = id_generator

    def start(self, request: StartOnboardingRequest) -> OnboardingResult:
        student_id = StudentId(request.student_id)
        existing = self._repository.get_in_progress_for_student(student_id)
        if existing is not None:
            return OnboardingResult(
                success=True,
                message="resumed incomplete onboarding",
                snapshot=OnboardingSnapshot.from_session(existing),
            )
        session = OnboardingSession.start(
            onboarding_id=self._id_generator.next_identity(),
            student_id=student_id,
            now=self._clock.now(),
        )
        self._repository.save(session)
        return OnboardingResult(
            success=True,
            message="onboarding started",
            snapshot=OnboardingSnapshot.from_session(session),
        )

    def resume(self, request: ResumeOnboardingRequest) -> OnboardingResult:
        student_id = StudentId(request.student_id)
        session = self._repository.get_in_progress_for_student(student_id)
        if session is None:
            raise OnboardingApplicationError(
                "no incomplete onboarding to resume",
                code="not_found",
            )
        return OnboardingResult(
            success=True,
            message="onboarding resumed",
            snapshot=OnboardingSnapshot.from_session(session),
        )

    def save_step(self, request: SaveStepRequest) -> OnboardingResult:
        session = self._load_owned(request.onboarding_id, request.student_id)
        step = parse_step(request.step)
        try:
            payload = build_payload(step, request.payload)
            updated = session.autosave(step, payload, now=self._clock.now())
        except (OnboardingDomainError, OnboardingValidationError) as exc:
            raise OnboardingApplicationError(str(exc), code="validation_error") from exc
        self._repository.save(updated)
        return OnboardingResult(
            success=True,
            message="step autosaved",
            snapshot=OnboardingSnapshot.from_session(updated),
        )

    def advance(self, request: AdvanceStepRequest) -> OnboardingResult:
        session = self._load_owned(request.onboarding_id, request.student_id)
        try:
            updated = session.advance(now=self._clock.now())
        except (OnboardingDomainError, OnboardingValidationError) as exc:
            raise OnboardingApplicationError(str(exc), code="validation_error") from exc
        self._repository.save(updated)
        return OnboardingResult(
            success=True,
            message="advanced",
            snapshot=OnboardingSnapshot.from_session(updated),
        )

    def go_back(self, request: GoBackRequest) -> OnboardingResult:
        session = self._load_owned(request.onboarding_id, request.student_id)
        try:
            updated = session.go_back(now=self._clock.now())
        except OnboardingDomainError as exc:
            raise OnboardingApplicationError(str(exc), code="navigation_error") from exc
        self._repository.save(updated)
        return OnboardingResult(
            success=True,
            message="moved back",
            snapshot=OnboardingSnapshot.from_session(updated),
        )

    def skip_optional(self, request: SkipOptionalRequest) -> OnboardingResult:
        session = self._load_owned(request.onboarding_id, request.student_id)
        try:
            updated = session.skip_optional(now=self._clock.now())
        except (OnboardingDomainError, OnboardingValidationError) as exc:
            raise OnboardingApplicationError(str(exc), code="validation_error") from exc
        self._repository.save(updated)
        return OnboardingResult(
            success=True,
            message="optional diagnostic skipped",
            snapshot=OnboardingSnapshot.from_session(updated),
        )

    def complete(self, request: CompleteOnboardingRequest) -> OnboardingResult:
        session = self._load_owned(request.onboarding_id, request.student_id)
        try:
            sealed = session.mark_completed(now=self._clock.now())
        except (OnboardingDomainError, OnboardingValidationError) as exc:
            raise OnboardingApplicationError(str(exc), code="validation_error") from exc
        init_request = self._build_twin_request(sealed)
        twin_id = self._twin_initializer.initialize(init_request)
        sealed = sealed.__class__(
            onboarding_id=sealed.onboarding_id,
            student_id=sealed.student_id,
            status=OnboardingStatus.COMPLETED,
            current_step=OnboardingStep.DASHBOARD_REDIRECT,
            payloads=sealed.payloads,
            created_at=sealed.created_at,
            updated_at=self._clock.now(),
            completed_at=sealed.completed_at,
            saved_steps=sealed.saved_steps,
        )
        self._repository.save(sealed)
        completed = CompletedOnboarding(
            onboarding_id=str(sealed.onboarding_id),
            student_id=str(sealed.student_id),
            completed_at=sealed.completed_at or self._clock.now(),
            twin_initialization=init_request,
            twin_id=twin_id,
            redirect_path=DASHBOARD_REDIRECT_PATH,
        )
        return OnboardingResult(
            success=True,
            message="onboarding completed",
            snapshot=OnboardingSnapshot.from_session(sealed),
            completed=completed,
        )

    def _load_owned(self, onboarding_id: str, student_id: str) -> OnboardingSession:
        session = self._repository.get(OnboardingId(onboarding_id))
        if session is None:
            raise OnboardingApplicationError(
                "onboarding session not found",
                code="not_found",
            )
        if str(session.student_id) != StudentId(student_id).value:
            raise OnboardingApplicationError(
                "onboarding session does not belong to this student",
                code="forbidden",
            )
        return session

    def _build_twin_request(
        self, session: OnboardingSession
    ) -> StudentTwinInitializationRequest:
        profile = session.require_payload(OnboardingStep.IFOA_PROFILE)
        history = session.require_payload(OnboardingStep.EXAM_HISTORY)
        availability = session.require_payload(OnboardingStep.WEEKLY_AVAILABILITY)
        confidence = session.require_payload(OnboardingStep.CONFIDENCE)
        habits = session.require_payload(OnboardingStep.STUDY_HABITS)
        assert isinstance(profile, IfoaProfilePayload)
        assert isinstance(history, ExamHistoryPayload)
        assert isinstance(availability, WeeklyAvailabilityPayload)
        assert isinstance(confidence, ConfidencePayload)
        assert isinstance(habits, StudyHabitsPayload)
        diagnostic = session.payloads.get(OnboardingStep.OPTIONAL_DIAGNOSTIC)
        if isinstance(diagnostic, OptionalDiagnosticPayload):
            diagnostic_choice = diagnostic.choice.value
        else:
            diagnostic_choice = DiagnosticChoice.SKIPPED.value
        return StudentTwinInitializationRequest(
            student_id=str(session.student_id),
            onboarding_id=str(session.onboarding_id),
            pathway=profile.pathway.value,
            exam_paper=profile.exam_paper,
            intended_sitting_label=profile.intended_sitting_label,
            prior_study=history.prior_study.value,
            core_reading=history.core_reading.value,
            previous_attempts=history.previous_attempts,
            sitting_intent=history.sitting_intent.value,
            weekday_minutes=availability.weekday_minutes,
            weekend_minutes=availability.weekend_minutes,
            preferred_session_minutes=availability.preferred_session_minutes,
            confidence_band=confidence.band.value,
            confidence_notes=confidence.notes,
            study_habit_preference=habits.preference.value,
            typical_start_time=habits.typical_start_time,
            diagnostic_choice=diagnostic_choice,
        )
