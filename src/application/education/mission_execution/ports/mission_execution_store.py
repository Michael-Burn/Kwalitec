"""MissionExecutionStore — load / save MissionExecution (interface only)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.education.mission_execution.ids import ExecutionId
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)


class MissionExecutionStore(ABC):
    """Outbound port for storing MissionExecution aggregates.

    Implementations live in infrastructure. This package does not persist
    executions; the port defines the contract only.
    """

    @abstractmethod
    def get(self, execution_id: ExecutionId) -> MissionExecution | None:
        """Load an execution by identity, or ``None`` when absent."""

    @abstractmethod
    def save(self, execution: MissionExecution) -> None:
        """Persist (or replace) an execution aggregate."""
