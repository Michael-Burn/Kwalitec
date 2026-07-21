"""Student Onboarding presentation — first-run evidence collection chrome.

Immutable view models and Design System mapping. Collects declarations only.
Never diagnoses, recommends, plans missions, or invokes AI.
"""

from __future__ import annotations

from presentation.onboarding.onboarding_mapper import OnboardingMapper
from presentation.onboarding.onboarding_presenter import OnboardingPresenter
from presentation.onboarding.onboarding_view_model import (
    OnboardingFieldView,
    OnboardingStepView,
    OnboardingViewModel,
)

__all__ = [
    "OnboardingFieldView",
    "OnboardingMapper",
    "OnboardingPresenter",
    "OnboardingStepView",
    "OnboardingViewModel",
]
