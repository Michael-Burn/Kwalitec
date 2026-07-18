"""Subject — educational product managed by Curriculum Management."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum_management.subject_identifier import SubjectIdentifier
from app.domain.curriculum_management.subject_metadata import SubjectMetadata


@dataclass(frozen=True)
class Subject:
    """Educational product (e.g. CS1, CM1, CB2).

    Never stores PDFs. Owns version identities and metadata only.
    """

    subject_id: str
    identifier: SubjectIdentifier
    metadata: SubjectMetadata
    version_ids: tuple[str, ...] = field(default_factory=tuple)
    active_version_id: str | None = None

    @classmethod
    def create(
        cls,
        subject_id: str,
        identifier: SubjectIdentifier | str,
        metadata: SubjectMetadata,
        *,
        version_ids: list[str] | tuple[str, ...] | None = None,
        active_version_id: str | None = None,
    ) -> Subject:
        """Construct a Subject after validating invariants."""
        sid = _require_non_empty(subject_id, "subject_id")
        ident = (
            identifier
            if isinstance(identifier, SubjectIdentifier)
            else SubjectIdentifier.create(identifier)
        )
        versions = tuple(
            _require_non_empty(v, "version_id") for v in (version_ids or ())
        )
        if len(versions) != len(set(versions)):
            raise ValueError("duplicate version_id within subject")
        active = active_version_id
        if active is not None:
            active = _require_non_empty(active, "active_version_id")
            if active not in versions:
                raise ValueError("active_version_id must be one of version_ids")
        return cls(
            subject_id=sid,
            identifier=ident,
            metadata=metadata,
            version_ids=versions,
            active_version_id=active,
        )

    @property
    def code(self) -> str:
        """Product code (CS1, CM1, …)."""
        return self.identifier.code

    @property
    def title(self) -> str:
        """Display title from metadata."""
        return self.metadata.title

    @property
    def version_count(self) -> int:
        """Number of registered version identities."""
        return len(self.version_ids)

    def with_version(self, version_id: str) -> Subject:
        """Return a subject with an appended version identity."""
        vid = _require_non_empty(version_id, "version_id")
        if vid in self.version_ids:
            raise ValueError(f"duplicate version_id: {vid!r}")
        return Subject(
            subject_id=self.subject_id,
            identifier=self.identifier,
            metadata=self.metadata,
            version_ids=(*self.version_ids, vid),
            active_version_id=self.active_version_id,
        )

    def with_active_version(self, version_id: str | None) -> Subject:
        """Return a subject with a new active version pointer."""
        if version_id is None:
            return Subject(
                subject_id=self.subject_id,
                identifier=self.identifier,
                metadata=self.metadata,
                version_ids=self.version_ids,
                active_version_id=None,
            )
        vid = _require_non_empty(version_id, "version_id")
        if vid not in self.version_ids:
            raise ValueError("active_version_id must be one of version_ids")
        return Subject(
            subject_id=self.subject_id,
            identifier=self.identifier,
            metadata=self.metadata,
            version_ids=self.version_ids,
            active_version_id=vid,
        )

    def with_metadata(self, metadata: SubjectMetadata) -> Subject:
        """Return a subject with replacement metadata."""
        return Subject(
            subject_id=self.subject_id,
            identifier=self.identifier,
            metadata=metadata,
            version_ids=self.version_ids,
            active_version_id=self.active_version_id,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
