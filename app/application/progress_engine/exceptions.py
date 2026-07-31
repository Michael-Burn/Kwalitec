"""Progress Engine exceptions (SR-003)."""

from __future__ import annotations


class ProgressEngineError(Exception):
    """Base error for Progress Engine."""


class CoverageAdvanceRejected(ProgressEngineError):  # noqa: N818
    """Coverage advancement refused (rejected evidence or Authority denial)."""


class DuplicateProgressWriter(ProgressEngineError):  # noqa: N818
    """Raised when a second progress writer attempts to register."""


class ProgressSingularityDisabled(ProgressEngineError):  # noqa: N818
    """SR_PROGRESS_SINGULARITY is off — legacy path remains."""
