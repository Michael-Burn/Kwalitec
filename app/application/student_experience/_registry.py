"""In-memory registry for Student Experience workspaces and sessions.

Presentation state only — never educational truth.
"""

from __future__ import annotations

from app.domain.student_experience.experience_session import ExperienceSession
from app.domain.student_experience.experience_workspace import (
    ExperienceWorkspace,
)


class ExperienceRegistry:
    """Mutable in-process registry for experience workspaces / sessions."""

    def __init__(self) -> None:
        self._workspaces: dict[str, ExperienceWorkspace] = {}
        self._sessions: dict[str, ExperienceSession] = {}
        self._by_student: dict[str, str] = {}

    @property
    def workspace_count(self) -> int:
        return len(self._workspaces)

    @property
    def session_count(self) -> int:
        return len(self._sessions)

    def put_workspace(self, workspace: ExperienceWorkspace) -> None:
        self._workspaces[workspace.workspace_id] = workspace
        self._by_student[workspace.student_id] = workspace.workspace_id

    def get_workspace(self, workspace_id: str) -> ExperienceWorkspace | None:
        return self._workspaces.get(workspace_id)

    def get_workspace_for_student(
        self, student_id: str
    ) -> ExperienceWorkspace | None:
        wid = self._by_student.get(student_id)
        if wid is None:
            return None
        return self._workspaces.get(wid)

    def list_workspaces(self) -> tuple[ExperienceWorkspace, ...]:
        return tuple(self._workspaces.values())

    def put_session(self, session: ExperienceSession) -> None:
        self._sessions[session.experience_session_id] = session

    def get_session(self, experience_session_id: str) -> ExperienceSession | None:
        return self._sessions.get(experience_session_id)

    def list_sessions(self) -> tuple[ExperienceSession, ...]:
        return tuple(self._sessions.values())
