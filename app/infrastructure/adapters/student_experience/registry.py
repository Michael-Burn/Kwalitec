"""Persisted Experience workspace / session registry.

Replaces transient in-memory-only presentation registries with repository-backed
persistence while preserving the ExperienceRegistry method surface.
"""

from __future__ import annotations

from typing import Any

from app.domain.student_experience.experience_session import (
    ExperienceSession,
    ExperienceSessionStatus,
)
from app.domain.student_experience.experience_workspace import (
    ExperienceSurface,
    ExperienceWorkspace,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)


class PersistedExperienceRegistry:
    """Repository-backed registry for experience workspaces and sessions."""

    def __init__(self, store: ExperienceProjectionStore) -> None:
        self._store = store
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
        self._store.save(
            self._store.workspaces,
            workspace.workspace_id,
            {
                "workspace_id": workspace.workspace_id,
                "student_id": workspace.student_id,
                "active_surface": workspace.active_surface.value,
                "examination_label": workspace.examination_label,
                "display_name": workspace.display_name,
            },
        )

    def get_workspace(self, workspace_id: str) -> ExperienceWorkspace | None:
        cached = self._workspaces.get(workspace_id)
        if cached is not None:
            return cached
        doc = self._store.get(self._store.workspaces, workspace_id)
        if doc is None:
            return None
        workspace = self._workspace_from_doc(doc)
        self._workspaces[workspace.workspace_id] = workspace
        self._by_student[workspace.student_id] = workspace.workspace_id
        return workspace

    def get_workspace_for_student(
        self, student_id: str
    ) -> ExperienceWorkspace | None:
        wid = self._by_student.get(student_id)
        if wid is not None:
            return self.get_workspace(wid)
        for key in self._store.workspaces.list_ids():
            doc = self._store.get(self._store.workspaces, key)
            if doc and doc.get("student_id") == student_id:
                return self.get_workspace(key)
        return None

    def list_workspaces(self) -> tuple[ExperienceWorkspace, ...]:
        return tuple(self._workspaces.values())

    def put_session(self, session: ExperienceSession) -> None:
        self._sessions[session.experience_session_id] = session
        self._store.save(
            self._store.sessions,
            session.experience_session_id,
            {
                "experience_session_id": session.experience_session_id,
                "student_id": session.student_id,
                "status": session.status.value,
                "mission_id": session.mission_id,
                "session_id": session.session_id,
                "topic_title": session.topic_title,
                "estimated_minutes": session.estimated_minutes,
                "started_at": session.started_at,
            },
        )

    def get_session(self, experience_session_id: str) -> ExperienceSession | None:
        cached = self._sessions.get(experience_session_id)
        if cached is not None:
            return cached
        doc = self._store.get(self._store.sessions, experience_session_id)
        if doc is None:
            return None
        session = self._session_from_doc(doc)
        self._sessions[session.experience_session_id] = session
        return session

    def list_sessions(self) -> tuple[ExperienceSession, ...]:
        return tuple(self._sessions.values())

    @staticmethod
    def _workspace_from_doc(doc: dict[str, Any]) -> ExperienceWorkspace:
        surface_raw = str(doc.get("active_surface") or "home")
        try:
            surface = ExperienceSurface(surface_raw)
        except ValueError:
            surface = ExperienceSurface.HOME
        return ExperienceWorkspace.create(
            str(doc["workspace_id"]),
            str(doc["student_id"]),
            active_surface=surface,
            examination_label=str(doc.get("examination_label") or ""),
            display_name=str(doc.get("display_name") or ""),
        )

    @staticmethod
    def _session_from_doc(doc: dict[str, Any]) -> ExperienceSession:
        status_raw = str(doc.get("status") or "in_progress")
        try:
            status = ExperienceSessionStatus(status_raw)
        except ValueError:
            status = ExperienceSessionStatus.IN_PROGRESS
        return ExperienceSession.create(
            str(doc["experience_session_id"]),
            str(doc["student_id"]),
            status=status,
            mission_id=(
                None
                if doc.get("mission_id") is None
                else str(doc.get("mission_id"))
            ),
            session_id=(
                None
                if doc.get("session_id") is None
                else str(doc.get("session_id"))
            ),
            topic_title=str(doc.get("topic_title") or ""),
            estimated_minutes=(
                None
                if doc.get("estimated_minutes") is None
                else int(doc["estimated_minutes"])
            ),
            started_at=str(doc.get("started_at") or ""),
        )
