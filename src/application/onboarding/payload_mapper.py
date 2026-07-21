"""Map raw step dictionaries into domain payload value objects."""

from __future__ import annotations

from typing import Any

from application.onboarding.errors import OnboardingApplicationError
from domain.onboarding.enums import (
    ConfidenceBand,
    CoreReadingDeclaration,
    DiagnosticChoice,
    ExamSittingIntent,
    IfoaPathway,
    OnboardingStep,
    PriorStudyPosture,
    StudyHabitPreference,
)
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


def parse_step(step: str) -> OnboardingStep:
    try:
        return OnboardingStep(step)
    except ValueError as exc:
        raise OnboardingApplicationError(
            f"unknown onboarding step: {step!r}",
            code="invalid_step",
        ) from exc


def build_payload(step: OnboardingStep, raw: dict[str, Any]) -> StepPayload:
    """Construct and structurally validate a domain payload from a dict."""
    data = dict(raw or {})
    try:
        if step is OnboardingStep.WELCOME:
            return WelcomePayload(acknowledged=_bool(data.get("acknowledged")))
        if step is OnboardingStep.IFOA_PROFILE:
            return IfoaProfilePayload(
                pathway=IfoaPathway(_str(data.get("pathway"))),
                exam_paper=_str(data.get("exam_paper")),
                intended_sitting_label=_str(data.get("intended_sitting_label")),
            )
        if step is OnboardingStep.EXAM_HISTORY:
            return ExamHistoryPayload(
                prior_study=PriorStudyPosture(_str(data.get("prior_study"))),
                core_reading=CoreReadingDeclaration(_str(data.get("core_reading"))),
                previous_attempts=_int(data.get("previous_attempts"), default=0),
                sitting_intent=ExamSittingIntent(_str(data.get("sitting_intent"))),
            )
        if step is OnboardingStep.WEEKLY_AVAILABILITY:
            return WeeklyAvailabilityPayload(
                weekday_minutes=_int(data.get("weekday_minutes"), default=0),
                weekend_minutes=_int(data.get("weekend_minutes"), default=0),
                preferred_session_minutes=_int(
                    data.get("preferred_session_minutes"), default=60
                ),
            )
        if step is OnboardingStep.CONFIDENCE:
            return ConfidencePayload(
                band=ConfidenceBand(_str(data.get("band"))),
                notes=_str(data.get("notes")),
            )
        if step is OnboardingStep.STUDY_HABITS:
            return StudyHabitsPayload(
                preference=StudyHabitPreference(_str(data.get("preference"))),
                typical_start_time=_str(data.get("typical_start_time")),
            )
        if step is OnboardingStep.OPTIONAL_DIAGNOSTIC:
            return OptionalDiagnosticPayload(
                choice=DiagnosticChoice(_str(data.get("choice"), default="skipped"))
            )
        if step is OnboardingStep.REVIEW:
            return ReviewPayload(confirmed=_bool(data.get("confirmed")))
    except (ValueError, TypeError, KeyError) as exc:
        raise OnboardingApplicationError(
            f"invalid payload for {step.value}: {exc}",
            code="invalid_payload",
        ) from exc
    raise OnboardingApplicationError(
        f"step {step.value} does not accept a payload",
        code="invalid_step",
    )


def _str(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _int(value: Any, *, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)
