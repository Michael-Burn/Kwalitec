"""Lifecycle transition rules for MissionExecution."""

from __future__ import annotations

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.errors import MissionExecutionError

# Lawful (from_status, to_status) pairs.
_ALLOWED: frozenset[tuple[ExecutionStatus, ExecutionStatus]] = frozenset(
    {
        (ExecutionStatus.PLANNED, ExecutionStatus.STARTED),
        (ExecutionStatus.PLANNED, ExecutionStatus.EXPIRED),
        (ExecutionStatus.STARTED, ExecutionStatus.PAUSED),
        (ExecutionStatus.STARTED, ExecutionStatus.COMPLETED),
        (ExecutionStatus.STARTED, ExecutionStatus.ABANDONED),
        (ExecutionStatus.STARTED, ExecutionStatus.EXPIRED),
        (ExecutionStatus.PAUSED, ExecutionStatus.RESUMED),
        (ExecutionStatus.PAUSED, ExecutionStatus.COMPLETED),
        (ExecutionStatus.PAUSED, ExecutionStatus.ABANDONED),
        (ExecutionStatus.PAUSED, ExecutionStatus.EXPIRED),
        (ExecutionStatus.RESUMED, ExecutionStatus.PAUSED),
        (ExecutionStatus.RESUMED, ExecutionStatus.COMPLETED),
        (ExecutionStatus.RESUMED, ExecutionStatus.ABANDONED),
        (ExecutionStatus.RESUMED, ExecutionStatus.EXPIRED),
    }
)

_TERMINAL = frozenset(
    {
        ExecutionStatus.COMPLETED,
        ExecutionStatus.ABANDONED,
        ExecutionStatus.EXPIRED,
    }
)


class LifecycleRules:
    """Deterministic lifecycle transition table for MissionExecution."""

    @staticmethod
    def is_terminal(status: ExecutionStatus) -> bool:
        return status in _TERMINAL

    @staticmethod
    def is_allowed(from_status: ExecutionStatus, to_status: ExecutionStatus) -> bool:
        return (from_status, to_status) in _ALLOWED

    @staticmethod
    def validate(
        from_status: ExecutionStatus,
        to_status: ExecutionStatus,
        *,
        attempted: str,
    ) -> MissionExecutionError | None:
        """Return an error when the transition is illegal; otherwise None."""
        if from_status in _TERMINAL:
            return MissionExecutionError(
                code="execution_terminal",
                message=(
                    f"Cannot {attempted}: execution is already "
                    f"{from_status.value}"
                ),
                from_status=from_status.value,
                attempted=attempted,
            )
        if (from_status, to_status) not in _ALLOWED:
            return MissionExecutionError(
                code="invalid_lifecycle_transition",
                message=(
                    f"Cannot {attempted}: transition "
                    f"{from_status.value} → {to_status.value} is not allowed"
                ),
                from_status=from_status.value,
                attempted=attempted,
            )
        return None

    @staticmethod
    def requires_active_work(status: ExecutionStatus) -> bool:
        """True when step / confidence / reflection recording is lawful."""
        return status in {
            ExecutionStatus.STARTED,
            ExecutionStatus.RESUMED,
            ExecutionStatus.PAUSED,
        }
