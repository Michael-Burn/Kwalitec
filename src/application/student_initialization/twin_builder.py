"""Map onboarding confidence declarations onto Twin confidence memory."""

from __future__ import annotations

from application.onboarding.results import StudentTwinInitializationRequest
from application.student_initialization.errors import OnboardingValidationError
from domain.education.digital_twin import (
    ConfidenceProfile,
    EducationalDigitalTwin,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.ids import DigitalTwinId
from domain.onboarding.enums import ConfidenceBand

_CONFIDENCE_MAP: dict[str, ConfidenceLevel] = {
    ConfidenceBand.LOW.value: ConfidenceLevel.LOW,
    ConfidenceBand.MODERATE.value: ConfidenceLevel.MEDIUM,
    ConfidenceBand.HIGH.value: ConfidenceLevel.HIGH,
    ConfidenceBand.UNSURE.value: ConfidenceLevel.UNKNOWN,
}


def map_confidence_profile(
    confidence_band: str,
) -> ConfidenceProfile:
    """Map a declared confidence band to Twin ``ConfidenceProfile`` memory.

    Mapping stores the self-declared prior only. It does not calibrate mastery
    or diagnose false confidence.
    """
    level = _CONFIDENCE_MAP.get((confidence_band or "").strip().lower())
    if level is None:
        raise OnboardingValidationError(
            f"unsupported confidence_band: {confidence_band!r}"
        )
    return ConfidenceProfile.of(level)


def build_student_twin(
    *,
    twin_id: str,
    declarations: StudentTwinInitializationRequest,
) -> EducationalDigitalTwin:
    """Create an ACTIVE Educational Digital Twin from sealed declarations."""
    student_id = (declarations.student_id or "").strip()
    if not student_id:
        raise OnboardingValidationError("student_id is required")
    identity = (twin_id or "").strip()
    if not identity:
        raise OnboardingValidationError("twin_id is required")
    return EducationalDigitalTwin.create(
        twin_id=DigitalTwinId(identity),
        student_id=student_id,
        confidence=map_confidence_profile(declarations.confidence_band),
    )
