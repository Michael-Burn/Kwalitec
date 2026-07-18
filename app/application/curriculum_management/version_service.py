"""VersionService — create and query subject version releases."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import version_snapshot
from app.application.curriculum_management.dto.version_snapshot import (
    VersionSnapshot,
)
from app.application.curriculum_management.exceptions import (
    SubjectNotFound,
    VersionAlreadyExists,
    VersionNotFound,
)
from app.application.curriculum_management.policies.version_policy import (
    VersionPolicy,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class VersionService:
    """Manage versioned subject releases (e.g. CS1 2026.1).

    Framework-independent. In-memory only.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def create_version(
        self,
        subject_id: str,
        version_label: str,
        *,
        version_id: str | None = None,
        section_refs: list[str] | tuple[str, ...] | None = None,
    ) -> VersionSnapshot:
        """Create a DRAFT subject version under ``subject_id``.

        Raises:
            SubjectNotFound: When the subject is missing.
            VersionAlreadyExists: When id or label collides.
        """
        subject = self._catalogue.get_subject(subject_id)
        if subject is None:
            raise SubjectNotFound(f"Subject not found: {subject_id!r}")
        label = VersionPolicy.assert_valid_label(version_label)
        if self._catalogue.find_version_by_label(subject_id, label) is not None:
            raise VersionAlreadyExists(
                f"Version label {label!r} already exists for {subject_id}"
            )
        vid = version_id or self._catalogue.next_id("version")
        if self._catalogue.has_version(vid):
            raise VersionAlreadyExists(f"Version already exists: {vid}")
        version = SubjectVersion.create(
            vid,
            subject_id,
            label,
            section_refs=section_refs,
        )
        subject = subject.with_version(vid)
        self._catalogue.put_subject(subject)
        self._catalogue.put_version(version)
        return version_snapshot(version)

    def get_version(self, version_id: str) -> VersionSnapshot:
        """Return a version snapshot."""
        return version_snapshot(self._require_version(version_id))

    def list_versions(
        self,
        *,
        subject_id: str | None = None,
    ) -> tuple[VersionSnapshot, ...]:
        """List versions, optionally filtered by subject."""
        return tuple(
            version_snapshot(v)
            for v in self._catalogue.list_versions(subject_id=subject_id)
        )

    def set_section_refs(
        self,
        version_id: str,
        section_refs: list[str] | tuple[str, ...],
    ) -> VersionSnapshot:
        """Replace declared section references on a mutable version."""
        version = self._require_version(version_id)
        VersionPolicy.assert_mutable(version)
        version = version.with_section_refs(section_refs)
        self._catalogue.put_version(version)
        return version_snapshot(version)

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
