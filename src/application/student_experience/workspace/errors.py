"""Errors for Adaptive Study Workspace composition."""

from __future__ import annotations


class WorkspaceExperienceError(Exception):
    """Base error for Adaptive Study Workspace failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "workspace_experience_error"


class WorkspaceInvariantViolation(WorkspaceExperienceError):  # noqa: N818
    """Raised when a workspace view model violates a shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="workspace_invariant_violation")
        self.invariant = invariant
