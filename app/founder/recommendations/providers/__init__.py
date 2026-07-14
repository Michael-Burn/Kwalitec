"""Providers for Founder Recommendation Engine (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.providers.template_provider import (
    TemplateProvider,
    UnknownTemplateError,
)

__all__ = [
    "TemplateProvider",
    "UnknownTemplateError",
]
