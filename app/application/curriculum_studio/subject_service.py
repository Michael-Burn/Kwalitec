"""SubjectService — Founder subject use-cases via Curriculum Management."""

from __future__ import annotations

from app.application.curriculum_studio._ports import require_management
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.dto.subject_snapshot import SubjectSnapshot
from app.application.curriculum_studio.exceptions import (
    SubjectAlreadyExists,
    SubjectNotFound,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)


class SubjectService:
    """Create and inspect educational product subjects.

    Authority: Curriculum Management. Studio projects only.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        metadata: dict | None = None,
    ) -> SubjectSnapshot:
        """Create Subject — delegates to Curriculum Management."""
        port = require_management(self._management, action="create_subject")
        code = subject_code.strip().upper()
        existing = port.get_subject_summary(code)
        if existing is not None:
            raise SubjectAlreadyExists(f"Subject already exists: {code!r}")
        summary = port.create_subject(
            code, title=title, metadata=metadata or {}
        )
        self._registry.record_activity(
            "subject_created",
            f"Created subject {code}",
            subject_code=code,
        )
        return _subject_snapshot(summary, fallback_code=code, fallback_title=title)

    def get_subject(self, subject_code: str) -> SubjectSnapshot:
        """Return a subject projection from Management."""
        port = require_management(self._management, action="get_subject")
        code = subject_code.strip().upper()
        summary = port.get_subject_summary(code)
        if summary is None:
            raise SubjectNotFound(f"Subject not found: {code!r}")
        return _subject_snapshot(summary, fallback_code=code)

    def list_subjects(self) -> tuple[SubjectSnapshot, ...]:
        """List subjects from Management."""
        port = require_management(self._management, action="list_subjects")
        return tuple(_subject_snapshot(s) for s in port.list_subjects())


def _subject_snapshot(
    summary: dict,
    *,
    fallback_code: str = "",
    fallback_title: str = "",
) -> SubjectSnapshot:
    code = str(summary.get("subject_code") or fallback_code).strip().upper()
    title = str(summary.get("title") or fallback_title or "")
    meta_raw = summary.get("metadata") or {}
    metadata: tuple[tuple[str, str], ...] = ()
    if isinstance(meta_raw, dict):
        metadata = tuple((str(k), str(v)) for k, v in sorted(meta_raw.items()))
    return SubjectSnapshot(
        subject_code=code,
        title=title,
        subject_id=(
            None
            if summary.get("subject_id") is None
            else str(summary.get("subject_id"))
        ),
        active_version_id=(
            None
            if summary.get("active_version_id") is None
            else str(summary.get("active_version_id"))
        ),
        version_count=int(summary.get("version_count") or 0),
        publication_state=(
            None
            if summary.get("publication_state") is None
            else str(summary.get("publication_state"))
        ),
        metadata=metadata,
    )
