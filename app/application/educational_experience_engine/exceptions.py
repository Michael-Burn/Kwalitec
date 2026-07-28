"""Exceptions for Educational Experience Engine services (EX-001)."""

from __future__ import annotations


class ExperienceEngineError(Exception):
    """Base error for Educational Experience Engine application services."""


class DecisionRequiredError(ExperienceEngineError):
    """Raised when a transformation is requested without an Educational Decision."""


class ExperienceNotFoundError(ExperienceEngineError):
    """Raised when a requested experience projection cannot be produced."""
