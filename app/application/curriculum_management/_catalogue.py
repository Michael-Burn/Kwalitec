"""In-memory catalogue shared by Curriculum Management services.

Never persists. Framework-independent.
"""

from __future__ import annotations

from app.domain.curriculum_management.subject import Subject
from app.domain.curriculum_management.subject_version import SubjectVersion


class CurriculumCatalogue:
    """Mutable in-memory store for subjects and versions.

    Services share one catalogue instance. No Flask / SQLAlchemy.
    """

    def __init__(self) -> None:
        self._subjects: dict[str, Subject] = {}
        self._versions: dict[str, SubjectVersion] = {}
        self._code_index: dict[str, str] = {}
        self._preview_seq: int = 0
        self._counters: dict[str, int] = {}

    def clear(self) -> None:
        """Remove all catalogue entries (test helper)."""
        self._subjects.clear()
        self._versions.clear()
        self._code_index.clear()
        self._preview_seq = 0
        self._counters.clear()

    def next_id(self, prefix: str) -> str:
        """Allocate a deterministic sequential identity token."""
        n = self._counters.get(prefix, 0) + 1
        self._counters[prefix] = n
        return f"{prefix}-{n}"

    def next_preview_id(self) -> str:
        """Allocate a preview identity."""
        self._preview_seq += 1
        return f"preview-{self._preview_seq}"

    # ---- subjects ----

    def put_subject(self, subject: Subject) -> None:
        """Insert or replace a subject."""
        existing = self._code_index.get(subject.code)
        if existing is not None and existing != subject.subject_id:
            raise ValueError(f"subject code already registered: {subject.code}")
        self._subjects[subject.subject_id] = subject
        self._code_index[subject.code] = subject.subject_id

    def get_subject(self, subject_id: str) -> Subject | None:
        """Return a subject by id, or None."""
        return self._subjects.get(subject_id)

    def get_subject_by_code(self, code: str) -> Subject | None:
        """Return a subject by product code, or None."""
        sid = self._code_index.get((code or "").strip().upper())
        if sid is None:
            return None
        return self._subjects.get(sid)

    def list_subjects(self) -> tuple[Subject, ...]:
        """All subjects ordered by code."""
        return tuple(
            sorted(self._subjects.values(), key=lambda s: (s.code, s.subject_id))
        )

    def has_subject(self, subject_id: str) -> bool:
        """True when subject_id is registered."""
        return subject_id in self._subjects

    # ---- versions ----

    def put_version(self, version: SubjectVersion) -> None:
        """Insert or replace a subject version."""
        self._versions[version.version_id] = version

    def get_version(self, version_id: str) -> SubjectVersion | None:
        """Return a version by id, or None."""
        return self._versions.get(version_id)

    def list_versions(
        self,
        *,
        subject_id: str | None = None,
    ) -> tuple[SubjectVersion, ...]:
        """All versions, optionally filtered by subject, ordered by label."""
        versions = list(self._versions.values())
        if subject_id is not None:
            versions = [v for v in versions if v.subject_id == subject_id]
        return tuple(
            sorted(
                versions,
                key=lambda v: (v.subject_id, v.version_label, v.version_id),
            )
        )

    def has_version(self, version_id: str) -> bool:
        """True when version_id is registered."""
        return version_id in self._versions

    def find_version_by_label(
        self,
        subject_id: str,
        version_label: str,
    ) -> SubjectVersion | None:
        """Return the version matching subject + label, or None."""
        for version in self._versions.values():
            if (
                version.subject_id == subject_id
                and version.version_label == version_label
            ):
                return version
        return None
