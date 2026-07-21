"""Flask onboarding adapter — first-run Student Twin initialization surface.

Thin HTTP adapters over framework-independent onboarding services and
presentation view models. Collects declarations only.
"""

from __future__ import annotations

from adapters.flask.onboarding.controller import OnboardingController
from adapters.flask.onboarding.dependency_provider import (
    OnboardingAdapterDependencies,
    OnboardingDependencyProvider,
    get_onboarding_dependencies,
)
from adapters.flask.onboarding.factory import build_onboarding_service


def __getattr__(name: str):
    if name in {"onboarding_bp", "register_onboarding"}:
        from adapters.flask.onboarding.routes import onboarding_bp, register_onboarding

        if name == "onboarding_bp":
            return onboarding_bp
        return register_onboarding
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "OnboardingAdapterDependencies",
    "OnboardingController",
    "OnboardingDependencyProvider",
    "build_onboarding_service",
    "get_onboarding_dependencies",
    "onboarding_bp",
    "register_onboarding",
]
