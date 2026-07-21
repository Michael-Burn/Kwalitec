"""Onboarding adapter dependencies — injectable collaborators."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from flask import Flask, current_app, g, has_app_context, has_request_context

from application.onboarding.onboarding_service import OnboardingService

ONBOARDING_DEPS_EXTENSION = "eos_onboarding_dependencies"
ONBOARDING_DEPS_G_KEY = "eos_onboarding_dependencies"


@dataclass(frozen=True, slots=True)
class OnboardingAdapterDependencies:
    """Collaborators for onboarding HTTP handlers."""

    onboarding_service: OnboardingService | None = None


class OnboardingDependencyProvider:
    """Resolve ``OnboardingAdapterDependencies`` from Flask context or overrides."""

    def __init__(
        self, dependencies: OnboardingAdapterDependencies | None = None
    ) -> None:
        self._dependencies = dependencies or OnboardingAdapterDependencies()

    def override(self, **kwargs: Any) -> OnboardingAdapterDependencies:
        self._dependencies = replace(self._dependencies, **kwargs)
        return self._dependencies

    def resolve(self) -> OnboardingAdapterDependencies:
        if has_request_context():
            bound = getattr(g, ONBOARDING_DEPS_G_KEY, None)
            if isinstance(bound, OnboardingAdapterDependencies):
                return bound
        if has_app_context():
            app_deps = current_app.extensions.get(ONBOARDING_DEPS_EXTENSION)
            if isinstance(app_deps, OnboardingAdapterDependencies):
                return app_deps
        return self._dependencies

    @staticmethod
    def bind(app: Flask, dependencies: OnboardingAdapterDependencies) -> None:
        app.extensions[ONBOARDING_DEPS_EXTENSION] = dependencies

    @staticmethod
    def bind_request(dependencies: OnboardingAdapterDependencies) -> None:
        if not has_request_context():
            raise RuntimeError("bind_request requires an active request context")
        setattr(g, ONBOARDING_DEPS_G_KEY, dependencies)


def get_onboarding_dependencies() -> OnboardingAdapterDependencies:
    """Module-level convenience for route handlers."""
    return OnboardingDependencyProvider().resolve()
