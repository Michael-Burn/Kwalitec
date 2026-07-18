"""SubjectService — register and query curriculum subject products."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import (
    subject_snapshot,
    subject_summary,
)
from app.application.curriculum_management.dto.subject_snapshot import (
    SubjectSnapshot,
)
from app.application.curriculum_management.dto.subject_summary import (
    SubjectSummary,
)
from app.application.curriculum_management.exceptions import (
    SubjectAlreadyExists,
    SubjectNotFound,
)
from app.domain.curriculum_management.subject import Subject
from app.domain.curriculum_management.subject_identifier import SubjectIdentifier
from app.domain.curriculum_management.subject_metadata import SubjectMetadata


class SubjectService:
    """Manage educational product (Subject) registrations.

    Framework-independent. In-memory only.
    """

    def __init__(self, catalogue: CurriculumCatalogue | None = None) -> None:
        self._catalogue = catalogue or CurriculumCatalogue()

    @property
    def catalogue(self) -> CurriculumCatalogue:
        """Shared in-memory catalogue."""
        return self._catalogue

    def create_subject(
        self,
        code: str,
        title: str,
        *,
        subject_id: str | None = None,
        description: str = "",
        exam_board: str | None = None,
        academic_year: str | None = None,
        locale: str = "en-GB",
        tags: list[str] | tuple[str, ...] | None = None,
    ) -> SubjectSnapshot:
        """Register a new subject product.

        Raises:
            SubjectAlreadyExists: When code or id is already registered.
        """
        identifier = SubjectIdentifier.create(code)
        if self._catalogue.get_subject_by_code(identifier.code) is not None:
            raise SubjectAlreadyExists(
                f"Subject code already exists: {identifier.code}"
            )
        sid = subject_id or self._catalogue.next_id("subject")
        if self._catalogue.has_subject(sid):
            raise SubjectAlreadyExists(f"Subject already exists: {sid}")
        metadata = SubjectMetadata.create(
            title,
            description=description,
            exam_board=exam_board,
            academic_year=academic_year,
            locale=locale,
            tags=tags,
        )
        subject = Subject.create(sid, identifier, metadata)
        self._catalogue.put_subject(subject)
        return subject_snapshot(subject)

    def get_subject(self, subject_id: str) -> SubjectSnapshot:
        """Return a subject snapshot.

        Raises:
            SubjectNotFound: When missing.
        """
        subject = self._require_subject(subject_id)
        return subject_snapshot(subject)

    def get_subject_by_code(self, code: str) -> SubjectSnapshot:
        """Return a subject snapshot by product code."""
        subject = self._catalogue.get_subject_by_code(code)
        if subject is None:
            raise SubjectNotFound(f"Subject not found for code: {code!r}")
        return subject_snapshot(subject)

    def list_subjects(self) -> tuple[SubjectSummary, ...]:
        """List all registered subjects as summaries."""
        rows: list[SubjectSummary] = []
        for subject in self._catalogue.list_subjects():
            active = None
            if subject.active_version_id:
                active = self._catalogue.get_version(subject.active_version_id)
            rows.append(subject_summary(subject, active_version=active))
        return tuple(rows)

    def update_metadata(
        self,
        subject_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        exam_board: str | None = None,
        academic_year: str | None = None,
        locale: str | None = None,
        tags: list[str] | tuple[str, ...] | None = None,
    ) -> SubjectSnapshot:
        """Update subject metadata fields (identity/code unchanged)."""
        subject = self._require_subject(subject_id)
        md = subject.metadata
        updated = SubjectMetadata.create(
            title if title is not None else md.title,
            description=md.description if description is None else description,
            exam_board=md.exam_board if exam_board is None else exam_board,
            academic_year=(
                md.academic_year if academic_year is None else academic_year
            ),
            locale=md.locale if locale is None else locale,
            tags=md.tags if tags is None else tags,
        )
        subject = subject.with_metadata(updated)
        self._catalogue.put_subject(subject)
        return subject_snapshot(subject)

    def set_active_version(
        self,
        subject_id: str,
        version_id: str | None,
    ) -> SubjectSnapshot:
        """Point the subject at an active version id (caller enforces policy)."""
        subject = self._require_subject(subject_id)
        if version_id is not None and version_id not in subject.version_ids:
            # Allow setting only known versions; publish flow registers first.
            raise SubjectNotFound(
                f"Version {version_id!r} is not registered on subject"
            )
        subject = subject.with_active_version(version_id)
        self._catalogue.put_subject(subject)
        return subject_snapshot(subject)

    def _require_subject(self, subject_id: str) -> Subject:
        subject = self._catalogue.get_subject(subject_id)
        if subject is None:
            raise SubjectNotFound(f"Subject not found: {subject_id!r}")
        return subject
