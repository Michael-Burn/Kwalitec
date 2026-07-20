"""In-memory registry for Learning Session Experience workspaces / sessions.

Presentation state only — never educational truth.
"""

from __future__ import annotations

from app.domain.session_experience.learning_session import LearningSession
from app.domain.session_experience.session_workspace import SessionWorkspace


class SessionExperienceRegistry:
    """Mutable in-process registry for session workspaces / handles."""

    def __init__(self) -> None:
        self._workspaces: dict[str, SessionWorkspace] = {}
        self._sessions: dict[str, LearningSession] = {}
        self._by_session: dict[str, str] = {}
        self._by_student_active: dict[str, str] = {}

    @property
    def workspace_count(self) -> int:
        return len(self._workspaces)

    @property
    def session_count(self) -> int:
        return len(self._sessions)

    def put_workspace(self, workspace: SessionWorkspace) -> None:
        self._workspaces[workspace.workspace_id] = workspace
        self._by_session[workspace.session_id] = workspace.workspace_id
        self._by_student_active[workspace.student_id] = workspace.workspace_id

    def get_workspace(self, workspace_id: str) -> SessionWorkspace | None:
        return self._workspaces.get(workspace_id)

    def get_workspace_for_session(
        self, session_id: str
    ) -> SessionWorkspace | None:
        wid = self._by_session.get(session_id)
        if wid is None:
            return None
        return self._workspaces.get(wid)

    def get_workspace_for_student(
        self, student_id: str
    ) -> SessionWorkspace | None:
        wid = self._by_student_active.get(student_id)
        if wid is None:
            return None
        return self._workspaces.get(wid)

    def list_workspaces(self) -> tuple[SessionWorkspace, ...]:
        return tuple(self._workspaces.values())

    def put_session(self, session: LearningSession) -> None:
        self._sessions[session.experience_session_id] = session
        self._sessions[session.session_id] = session

    def get_session(self, session_key: str) -> LearningSession | None:
        return self._sessions.get(session_key)

    def list_sessions(self) -> tuple[LearningSession, ...]:
        seen: set[str] = set()
        ordered: list[LearningSession] = []
        for session in self._sessions.values():
            if session.experience_session_id in seen:
                continue
            seen.add(session.experience_session_id)
            ordered.append(session)
        return tuple(ordered)
