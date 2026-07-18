"""Application-layer exceptions for the Learning Orchestrator.

Framework-independent. Raised when coordination, port, or policy rules
are violated. Never encode educational reasoning.
"""

from __future__ import annotations


class LearningOrchestratorError(Exception):
    """Base exception for Learning Orchestrator failures."""


class OrchestrationError(LearningOrchestratorError):
    """Orchestration could not produce a lawful execution."""


class PipelineError(LearningOrchestratorError):
    """A pipeline stage could not complete under current policy."""


class PortUnavailable(LearningOrchestratorError):  # noqa: N818
    """A registered port reports itself unavailable."""


class PortError(LearningOrchestratorError):
    """A port call failed or returned an unlawful response."""


class PolicyViolation(LearningOrchestratorError):  # noqa: N818
    """An orchestration or pipeline policy rule was violated."""


class EventDispatchError(LearningOrchestratorError):
    """An event could not be dispatched to the pipeline."""


class DependencyError(LearningOrchestratorError):
    """A required port dependency is missing or unlawfully substituted."""
