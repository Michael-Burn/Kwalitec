"""Map weekly availability declarations onto LearnerAvailability."""

from __future__ import annotations

from application.onboarding.results import StudentTwinInitializationRequest
from application.student_initialization.errors import OnboardingValidationError
from domain.study_planning import AvailabilityWindow, LearnerAvailability


def build_availability(
    declarations: StudentTwinInitializationRequest,
) -> LearnerAvailability:
    """Build a seven-day relative availability map from onboarding minutes.

    Days 0–4 use weekday minutes; days 5–6 use weekend minutes. Values must
    already be positive (validated during onboarding collection).
    """
    student_id = (declarations.student_id or "").strip()
    if not student_id:
        raise OnboardingValidationError("student_id is required")
    weekday = declarations.weekday_minutes
    weekend = declarations.weekend_minutes
    if not isinstance(weekday, int) or isinstance(weekday, bool) or weekday <= 0:
        raise OnboardingValidationError("weekday_minutes must be a positive integer")
    if not isinstance(weekend, int) or isinstance(weekend, bool) or weekend <= 0:
        raise OnboardingValidationError("weekend_minutes must be a positive integer")
    windows = tuple(
        AvailabilityWindow(
            day_index=day,
            available_minutes=weekday if day < 5 else weekend,
        )
        for day in range(7)
    )
    return LearnerAvailability.of(student_id, *windows)
