"""WorkspaceResourceProvider — study resources for the workspace surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkspaceResource:
    """Immutable study resource projection for the workspace surface."""

    resource_id: str
    title: str
    detail: str = ""
    kind: str = "task"
    estimated_minutes: int | None = None


class WorkspaceResourceProvider(ABC):
    """Outbound port for study resources attached to a session or mission.

    Implementations live in infrastructure. Never invents educational
    content or generates recommendations.
    """

    @abstractmethod
    def list_resources(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        limit: int = 10,
    ) -> tuple[WorkspaceResource, ...]:
        """Return study resources for the current workspace context."""
