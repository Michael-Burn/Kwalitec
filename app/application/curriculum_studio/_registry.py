"""In-memory workspace registry for Curriculum Studio.

Not a database. Not durable. Safe for unit tests and foundation wiring.
Stores Founder workspace / workflow projections and activity only.
Publication truth remains Curriculum Management via ports.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.version_history import (
    VersionHistory,
    VersionRecord,
)


@dataclass(frozen=True)
class ActivityEntry:
    """In-memory Founder activity record for dashboard projection."""

    activity_id: str
    kind: str
    message: str
    occurred_at: str = ""
    workspace_id: str | None = None
    subject_code: str | None = None
    version_id: str | None = None


class StudioRegistry:
    """Shared in-memory store for Studio workspaces and activity.

    Version records may be mirrored for Founder UX linkage, but
    Management remains the version / publication authority.
    """

    def __init__(self) -> None:
        self._workspaces: dict[str, CurriculumWorkspace] = {}
        self._histories: dict[str, VersionHistory] = {}
        self._versions: dict[str, VersionRecord] = {}
        self._activity: list[ActivityEntry] = []
        self._ingestion_jobs: dict[str, str] = {}  # workspace_id -> job_id
        self._activity_seq = 0

    def clear(self) -> None:
        """Remove all registered state."""
        self._workspaces.clear()
        self._histories.clear()
        self._versions.clear()
        self._activity.clear()
        self._ingestion_jobs.clear()
        self._activity_seq = 0

    # --- workspaces ---------------------------------------------------------

    def put_workspace(self, workspace: CurriculumWorkspace) -> None:
        """Insert or replace a workspace."""
        self._workspaces[workspace.workspace_id] = workspace

    def get_workspace(self, workspace_id: str) -> CurriculumWorkspace | None:
        """Return a workspace by id, or None."""
        return self._workspaces.get(workspace_id)

    def has_workspace(self, workspace_id: str) -> bool:
        """True when a workspace id is registered."""
        return workspace_id in self._workspaces

    def list_workspaces(self) -> tuple[CurriculumWorkspace, ...]:
        """All registered workspaces in insertion order."""
        return tuple(self._workspaces.values())

    def delete_workspace(self, workspace_id: str) -> bool:
        """Remove a workspace; return True when it existed."""
        return self._workspaces.pop(workspace_id, None) is not None

    # --- ingestion job linkage ----------------------------------------------

    def set_ingestion_job(self, workspace_id: str, job_id: str) -> None:
        """Link a workspace to an ingestion job id."""
        self._ingestion_jobs[workspace_id] = job_id

    def get_ingestion_job(self, workspace_id: str) -> str | None:
        """Return linked ingestion job id, or None."""
        return self._ingestion_jobs.get(workspace_id)

    # --- version history (local mirror for UX) ------------------------------

    def put_history(self, history: VersionHistory) -> None:
        """Insert or replace subject version history."""
        self._histories[history.subject_code] = history
        for record in history.records:
            self._versions[record.version_id] = record

    def get_history(self, subject_code: str) -> VersionHistory | None:
        """Return history for a subject code, or None."""
        return self._histories.get(subject_code.strip().upper())

    def put_version(self, record: VersionRecord) -> None:
        """Upsert a version record into subject history."""
        code = record.subject_code
        history = self._histories.get(code) or VersionHistory.create(code)
        updated = history.with_record(record)
        self.put_history(updated)

    def get_version(self, version_id: str) -> VersionRecord | None:
        """Return a version record by id, or None."""
        return self._versions.get(version_id)

    # --- activity -----------------------------------------------------------

    def record_activity(
        self,
        kind: str,
        message: str,
        *,
        occurred_at: str = "",
        workspace_id: str | None = None,
        subject_code: str | None = None,
        version_id: str | None = None,
    ) -> ActivityEntry:
        """Append a Founder activity entry and return it."""
        self._activity_seq += 1
        entry = ActivityEntry(
            activity_id=f"act-{self._activity_seq}",
            kind=kind,
            message=message,
            occurred_at=occurred_at,
            workspace_id=workspace_id,
            subject_code=subject_code,
            version_id=version_id,
        )
        self._activity.append(entry)
        return entry

    def list_activity(self, *, limit: int = 50) -> tuple[ActivityEntry, ...]:
        """Return recent activity newest-first."""
        items = list(reversed(self._activity))
        if limit > 0:
            items = items[:limit]
        return tuple(items)

    @property
    def workspace_count(self) -> int:
        """Number of registered workspaces."""
        return len(self._workspaces)

    @property
    def version_count(self) -> int:
        """Number of registered version records."""
        return len(self._versions)

    @property
    def activity_count(self) -> int:
        """Number of activity entries."""
        return len(self._activity)
