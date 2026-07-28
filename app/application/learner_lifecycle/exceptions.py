"""Exceptions for Learner Lifecycle Orchestration (LP-001)."""

from __future__ import annotations


class LifecycleError(Exception):
    """Base error for lifecycle orchestration failures."""


class LifecycleStageError(LifecycleError):
    """A coordinated Educational Intelligence stage failed."""

    def __init__(
        self,
        message: str,
        *,
        stage: str,
        operation_id: str | None = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.operation_id = operation_id
        self.cause = cause


class LifecycleInconsistentError(LifecycleError):
    """Learner educational state is incomplete relative to the EI pipeline."""


class LifecycleNotFoundError(LifecycleError):
    """Requested lifecycle operation or instance was not found."""


class LifecycleRetryExhaustedError(LifecycleStageError):
    """Technical retries for a stage were exhausted."""
