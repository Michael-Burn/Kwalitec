"""Version history — Studio curriculum version vocabulary.

Supports Draft / Published / Archived, historical lookup,
rollback eligibility, and version comparison hooks.
No persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class StudioVersionStatus(StrEnum):
    """Curriculum version posture in Curriculum Studio."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class VersionRecord:
    """Single curriculum version record for Studio history."""

    version_id: str
    workspace_id: str
    subject_code: str
    version_label: str
    status: StudioVersionStatus = StudioVersionStatus.DRAFT
    created_at: str = ""
    published_at: str | None = None
    archived_at: str | None = None
    parent_version_id: str | None = None
    rollback_snapshot_id: str | None = None
    notes: str = ""

    @classmethod
    def create(
        cls,
        version_id: str,
        workspace_id: str,
        subject_code: str,
        version_label: str,
        *,
        status: StudioVersionStatus | str = StudioVersionStatus.DRAFT,
        created_at: str = "",
        published_at: str | None = None,
        archived_at: str | None = None,
        parent_version_id: str | None = None,
        rollback_snapshot_id: str | None = None,
        notes: str = "",
    ) -> VersionRecord:
        """Construct a VersionRecord after validating invariants."""
        resolved = (
            status
            if isinstance(status, StudioVersionStatus)
            else StudioVersionStatus(str(status).strip().lower())
        )
        return cls(
            version_id=_require_non_empty(version_id, "version_id"),
            workspace_id=_require_non_empty(workspace_id, "workspace_id"),
            subject_code=_require_non_empty(subject_code, "subject_code").upper(),
            version_label=_require_non_empty(version_label, "version_label"),
            status=resolved,
            created_at=(created_at or "").strip(),
            published_at=(
                None
                if published_at is None
                else _require_non_empty(published_at, "published_at")
            ),
            archived_at=(
                None
                if archived_at is None
                else _require_non_empty(archived_at, "archived_at")
            ),
            parent_version_id=(
                None
                if parent_version_id is None
                else _require_non_empty(parent_version_id, "parent_version_id")
            ),
            rollback_snapshot_id=(
                None
                if rollback_snapshot_id is None
                else _require_non_empty(
                    rollback_snapshot_id, "rollback_snapshot_id"
                )
            ),
            notes=(notes or "").strip(),
        )

    @property
    def is_draft(self) -> bool:
        """True when status is DRAFT."""
        return self.status is StudioVersionStatus.DRAFT

    @property
    def is_published(self) -> bool:
        """True when status is PUBLISHED."""
        return self.status is StudioVersionStatus.PUBLISHED

    @property
    def is_archived(self) -> bool:
        """True when status is ARCHIVED."""
        return self.status is StudioVersionStatus.ARCHIVED

    @property
    def rollback_eligible(self) -> bool:
        """True when a published/archived version has a rollback snapshot."""
        return (
            self.status
            in {StudioVersionStatus.PUBLISHED, StudioVersionStatus.ARCHIVED}
            and self.rollback_snapshot_id is not None
        )

    def with_status(
        self,
        status: StudioVersionStatus | str,
        *,
        published_at: str | None = None,
        archived_at: str | None = None,
        rollback_snapshot_id: str | None = None,
    ) -> VersionRecord:
        """Return a copy with updated lifecycle fields."""
        resolved = (
            status
            if isinstance(status, StudioVersionStatus)
            else StudioVersionStatus(str(status).strip().lower())
        )
        return VersionRecord(
            version_id=self.version_id,
            workspace_id=self.workspace_id,
            subject_code=self.subject_code,
            version_label=self.version_label,
            status=resolved,
            created_at=self.created_at,
            published_at=(
                published_at if published_at is not None else self.published_at
            ),
            archived_at=(
                archived_at if archived_at is not None else self.archived_at
            ),
            parent_version_id=self.parent_version_id,
            rollback_snapshot_id=(
                rollback_snapshot_id
                if rollback_snapshot_id is not None
                else self.rollback_snapshot_id
            ),
            notes=self.notes,
        )


# Lawful version status transitions.
LAWFUL_VERSION_TRANSITIONS: dict[
    tuple[StudioVersionStatus, StudioVersionStatus], bool
] = {
    (StudioVersionStatus.DRAFT, StudioVersionStatus.PUBLISHED): True,
    (StudioVersionStatus.PUBLISHED, StudioVersionStatus.ARCHIVED): True,
    (StudioVersionStatus.DRAFT, StudioVersionStatus.ARCHIVED): False,
    (StudioVersionStatus.ARCHIVED, StudioVersionStatus.PUBLISHED): False,
    (StudioVersionStatus.ARCHIVED, StudioVersionStatus.DRAFT): False,
    (StudioVersionStatus.PUBLISHED, StudioVersionStatus.DRAFT): False,
}


def is_lawful_version_transition(
    current: StudioVersionStatus | str,
    target: StudioVersionStatus | str,
) -> bool:
    """True when ``current → target`` is a lawful version transition."""
    cur = (
        current
        if isinstance(current, StudioVersionStatus)
        else StudioVersionStatus(str(current).strip().lower())
    )
    tgt = (
        target
        if isinstance(target, StudioVersionStatus)
        else StudioVersionStatus(str(target).strip().lower())
    )
    if cur is tgt:
        return True
    return LAWFUL_VERSION_TRANSITIONS.get((cur, tgt), False)


@dataclass(frozen=True)
class VersionHistory:
    """Ordered historical collection of curriculum versions for a subject."""

    subject_code: str
    records: tuple[VersionRecord, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        subject_code: str,
        records: list[VersionRecord] | tuple[VersionRecord, ...] | None = None,
    ) -> VersionHistory:
        """Construct a VersionHistory; records ordered by creation then label."""
        code = _require_non_empty(subject_code, "subject_code").upper()
        recs = tuple(records or ())
        for record in recs:
            if record.subject_code != code:
                raise ValueError(
                    f"record subject_code {record.subject_code!r} "
                    f"must match history {code!r}"
                )
        return cls(subject_code=code, records=recs)

    @property
    def version_count(self) -> int:
        """Number of version records."""
        return len(self.records)

    def get(self, version_id: str) -> VersionRecord | None:
        """Historical lookup by version_id."""
        for record in self.records:
            if record.version_id == version_id:
                return record
        return None

    def by_label(self, version_label: str) -> VersionRecord | None:
        """Historical lookup by version_label."""
        label = (version_label or "").strip()
        for record in self.records:
            if record.version_label == label:
                return record
        return None

    def published(self) -> tuple[VersionRecord, ...]:
        """All published versions."""
        return tuple(r for r in self.records if r.is_published)

    def drafts(self) -> tuple[VersionRecord, ...]:
        """All draft versions."""
        return tuple(r for r in self.records if r.is_draft)

    def archived(self) -> tuple[VersionRecord, ...]:
        """All archived versions."""
        return tuple(r for r in self.records if r.is_archived)

    def rollback_eligible(self) -> tuple[VersionRecord, ...]:
        """Versions that may be rolled back."""
        return tuple(r for r in self.records if r.rollback_eligible)

    def current_published(self) -> VersionRecord | None:
        """Most recently published version, if any."""
        published = self.published()
        return published[-1] if published else None

    def with_record(self, record: VersionRecord) -> VersionHistory:
        """Return a copy with ``record`` appended or replaced by version_id."""
        if record.subject_code != self.subject_code:
            raise ValueError("record subject_code must match history")
        others = tuple(
            r for r in self.records if r.version_id != record.version_id
        )
        return VersionHistory(
            subject_code=self.subject_code,
            records=(*others, record),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
