"""ReleaseService — release notes and release views."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import release_snapshot
from app.application.curriculum_management.dto.release_snapshot import (
    ReleaseSnapshot,
)
from app.application.curriculum_management.exceptions import (
    ReleaseError,
    VersionNotFound,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.domain.curriculum_management.release_notes import (
    ReleaseNoteEntry,
    ReleaseNotes,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class ReleaseService:
    """Capture educational change notes for subject versions."""

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def set_notes(
        self,
        version_id: str,
        *,
        headline: str = "",
        entries: list[tuple[str, str]] | None = None,
        notes_id: str | None = None,
    ) -> ReleaseSnapshot:
        """Replace release notes for a version.

        ``entries`` items are ``(text, category)`` pairs.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        nid = notes_id or self._catalogue.next_id("notes")
        built: list[ReleaseNoteEntry] = []
        for index, item in enumerate(entries or ()):
            text, category = item[0], item[1] if len(item) > 1 else "general"
            built.append(
                ReleaseNoteEntry.create(
                    f"{nid}-e{index + 1}",
                    text,
                    category=category,
                )
            )
        try:
            notes = ReleaseNotes.create(
                nid,
                version_id,
                entries=built,
                headline=headline,
            )
        except ValueError as exc:
            raise ReleaseError(str(exc)) from exc
        version = version.with_release_notes(notes)
        self._catalogue.put_version(version)
        return release_snapshot(version)

    def add_entry(
        self,
        version_id: str,
        text: str,
        *,
        category: str = "general",
        entry_id: str | None = None,
    ) -> ReleaseSnapshot:
        """Append a single release note entry."""
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        notes = version.release_notes
        if notes is None:
            notes = ReleaseNotes.create(
                self._catalogue.next_id("notes"),
                version_id,
            )
        eid = entry_id or self._catalogue.next_id("note-entry")
        try:
            entry = ReleaseNoteEntry.create(eid, text, category=category)
            notes = notes.with_entry(entry)
        except ValueError as exc:
            raise ReleaseError(str(exc)) from exc
        version = version.with_release_notes(notes)
        self._catalogue.put_version(version)
        return release_snapshot(version)

    def get_release(self, version_id: str) -> ReleaseSnapshot:
        """Return the release snapshot for a version."""
        return release_snapshot(self._require_version(version_id))

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
