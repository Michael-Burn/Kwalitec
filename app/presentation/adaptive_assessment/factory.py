"""Factory / DI helpers for Adaptive Assessment presentation."""

from __future__ import annotations

from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckExperienceService,
    get_quick_check_experience_service,
    reset_quick_check_experience_service,
)


def get_service() -> QuickCheckExperienceService:
    """Return the wired Quick Check experience service."""
    return get_quick_check_experience_service()


def reset_service(
    service: QuickCheckExperienceService | None = None,
) -> QuickCheckExperienceService:
    """Replace the process service (tests)."""
    return reset_quick_check_experience_service(service)
