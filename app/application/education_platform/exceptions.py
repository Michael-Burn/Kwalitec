"""Application-layer exceptions for the Educational Composition Layer.

Framework-independent. Raised when composition, registration, validation,
or workflow execution rules are violated. Never encode educational reasoning.
"""

from __future__ import annotations


class EducationPlatformError(Exception):
    """Base exception for Educational Composition Layer failures."""


class DependencyError(EducationPlatformError):
    """A required port is missing, duplicated, or unlawfully replaced."""


class ValidationError(EducationPlatformError):  # noqa: N818
    """Platform composition failed validation policy checks."""


class WorkflowError(EducationPlatformError):
    """A workflow could not be executed under current composition."""


class OrchestrationError(EducationPlatformError):
    """Orchestration could not produce a lawful execution order."""


class CompositionError(EducationPlatformError):
    """Composition root could not assemble a valid platform."""


class PortUnavailable(EducationPlatformError):  # noqa: N818
    """A registered port reports itself unavailable."""
