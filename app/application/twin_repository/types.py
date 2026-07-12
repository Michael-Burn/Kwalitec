"""TwinRepository immutable types — educational persistence cargo only.

Snapshot identity, scope, authorship, and honesty signals for Capability 3.7.3.
Never educational judgements, readiness scores, or storage-engine details.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from app.domain.twin.digital_twin import DigitalTwin

SNAPSHOT_FORMAT_VERSION_1_0 = "1.0"


class TwinAuthorship(str, Enum):
    """Who authored the Twin snapshot content (not who stored it)."""

    BIRTH = "birth"
    SUCCESSOR = "successor"


class TwinPersistenceFailureReason(str, Enum):
    """Honest TwinRepository failure postures (Capability 3.7.3 §5)."""

    MISSING = "missing"
    CORRUPT = "corrupt"
    UNAVAILABLE = "unavailable"
    DUPLICATE = "duplicate"
    CONCURRENT = "concurrent"
    REJECTED = "rejected"


@dataclass(frozen=True)
class TwinScope:
    """Authorised student / sitting scope for Twin persistence.

    Wiring identity only — never an educational scoring input.
    """

    student_id: str
    sitting_id: str | None = None
    curriculum_id: str | None = None

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        sitting_id: str | None = None,
        curriculum_id: str | None = None,
    ) -> TwinScope:
        """Construct a normalised TwinScope.

        Raises:
            ValueError: If ``student_id`` is blank.
        """
        normalized = student_id.strip() if isinstance(student_id, str) else ""
        if not normalized:
            raise ValueError("student_id must be a non-empty string")
        sitting = sitting_id.strip() if isinstance(sitting_id, str) else None
        if sitting == "":
            sitting = None
        curriculum = (
            curriculum_id.strip() if isinstance(curriculum_id, str) else None
        )
        if curriculum == "":
            curriculum = None
        return cls(
            student_id=normalized,
            sitting_id=sitting,
            curriculum_id=curriculum,
        )


@dataclass(frozen=True)
class TwinSnapshotIdentity:
    """Durable snapshot identity distinct from the student."""

    snapshot_id: str
    sequence: int
    format_version: str = SNAPSHOT_FORMAT_VERSION_1_0

    @classmethod
    def create(
        cls,
        snapshot_id: str,
        *,
        sequence: int,
        format_version: str = SNAPSHOT_FORMAT_VERSION_1_0,
    ) -> TwinSnapshotIdentity:
        """Construct snapshot identity.

        Raises:
            ValueError: If ``snapshot_id`` is blank or ``sequence`` is invalid.
        """
        normalized = snapshot_id.strip() if isinstance(snapshot_id, str) else ""
        if not normalized:
            raise ValueError("snapshot_id must be a non-empty string")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
            raise ValueError("sequence must be an integer >= 1")
        version = (
            format_version.strip()
            if isinstance(format_version, str)
            else SNAPSHOT_FORMAT_VERSION_1_0
        )
        if not version:
            raise ValueError("format_version must be a non-empty string")
        return cls(
            snapshot_id=normalized,
            sequence=sequence,
            format_version=version,
        )


@dataclass(frozen=True)
class TwinSnapshotRecord:
    """Immutable persisted Twin snapshot with Persistence metadata.

    The Twin aggregate is educational state as authored elsewhere.
    Metadata supports identity, ordering, and current designation only.
    """

    identity: TwinSnapshotIdentity
    scope: TwinScope
    twin: DigitalTwin
    authorship: TwinAuthorship
    persisted_at: datetime | None = None
    provenance: dict[str, Any] | None = None

    @classmethod
    def create(
        cls,
        *,
        identity: TwinSnapshotIdentity,
        scope: TwinScope,
        twin: DigitalTwin,
        authorship: TwinAuthorship,
        persisted_at: datetime | None = None,
        provenance: dict[str, Any] | None = None,
    ) -> TwinSnapshotRecord:
        """Construct an immutable snapshot record."""
        return cls(
            identity=identity,
            scope=scope,
            twin=twin,
            authorship=authorship,
            persisted_at=persisted_at,
            provenance=dict(provenance) if provenance is not None else None,
        )


@dataclass(frozen=True)
class PersistAcknowledgement:
    """Success cargo: the snapshot is durably current."""

    snapshot_id: str
    sequence: int
    scope: TwinScope
    authorship: TwinAuthorship


@dataclass(frozen=True)
class TwinPersistenceFailure:
    """Honesty cargo when TwinRepository cannot complete an operation."""

    reason: TwinPersistenceFailureReason
    scope: TwinScope | None = None
    detail: str | None = None
    snapshot_id: str | None = None


@dataclass(frozen=True)
class CurrentSnapshotRef:
    """Current designation resolution without inventing educational state."""

    snapshot_id: str
    sequence: int
    scope: TwinScope
    twin: DigitalTwin


@dataclass(frozen=True)
class SnapshotHistory:
    """Ordered Twin lineage (birth → successors) for one scope."""

    scope: TwinScope
    snapshots: tuple[TwinSnapshotRecord, ...]
    current_snapshot_id: str | None

    @property
    def is_empty(self) -> bool:
        """True when no snapshots exist for the scope."""
        return len(self.snapshots) == 0
