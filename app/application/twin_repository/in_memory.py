"""In-memory TwinRepository — process-local Twin snapshot adapter.

Honours the TwinRepository Contract with process-local storage. Used by unit
tests and as a non-durable reference implementation. Product wiring uses the
SQLAlchemy-backed TwinRepository (Capability 3.8.2).

Never creates Twins. Never mutates stored snapshots. Never performs educational
reasoning. Never imports Flask / ORM.

See Capabilities 3.7.1–3.7.3 and APPLICATION_LAYER_ARCHITECTURE.md.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from app.application.twin_repository.types import (
    SNAPSHOT_FORMAT_VERSION_1_0,
    CurrentSnapshotRef,
    PersistAcknowledgement,
    SnapshotHistory,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
    TwinSnapshotIdentity,
    TwinSnapshotRecord,
)
from app.domain.twin.digital_twin import DigitalTwin

PersistBirthResult = PersistAcknowledgement | TwinPersistenceFailure
PersistSuccessorResult = PersistAcknowledgement | TwinPersistenceFailure
RetrieveCurrentResult = DigitalTwin | TwinPersistenceFailure
RetrieveHistoryResult = SnapshotHistory | TwinPersistenceFailure
DetermineCurrentResult = CurrentSnapshotRef | TwinPersistenceFailure


class InMemoryTwinRepository:
    """Process-local persistence adapter: immutable Twin snapshots only.

    Calibration birth and update-strategy succession produce Twins elsewhere.
    This repository stores and returns them. Domains never import this class;
    they receive Twin snapshots as arguments.
    """

    def __init__(self) -> None:
        # Process-local store: scope_key → ordered snapshot records.
        # Current designation is the last record in the sequence (replace-by-snapshot).
        self._histories: dict[str, list[TwinSnapshotRecord]] = {}
        self._snapshot_ids: set[str] = set()
        self._available = True

    # ── Contract operations (Capability 3.7.3 §3) ────────────────────────────

    def persist_birth_twin(
        self,
        twin: DigitalTwin,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        provenance: dict[str, Any] | None = None,
        persisted_at: datetime | None = None,
    ) -> PersistBirthResult:
        """Persist Birth Twin as the first durable snapshot and current.

        Args:
            twin: Complete immutable Birth Twin already authored elsewhere.
            scope: Authorised student / sitting scope. Defaults from Twin identity.
            snapshot_id: Optional explicit snapshot identity (must be unique).
            provenance: Opaque lineage cargo preserved without reinterpretation.
            persisted_at: Optional persist timestamp (defaults to UTC now).

        Returns:
            PersistAcknowledgement on success, or TwinPersistenceFailure honesty.
        """
        if not self._available:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                detail="Twin storage unavailable",
            )

        cargo = self._validate_twin_cargo(twin)
        if cargo is not None:
            return cargo

        resolved_scope = scope if scope is not None else self._scope_from_twin(twin)
        if isinstance(resolved_scope, TwinPersistenceFailure):
            return resolved_scope

        identity_check = self._validate_twin_matches_scope(twin, resolved_scope)
        if identity_check is not None:
            return identity_check

        key = self._scope_key(resolved_scope)
        if key in self._histories and self._histories[key]:
            current = self._histories[key][-1]
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.DUPLICATE,
                scope=resolved_scope,
                snapshot_id=current.identity.snapshot_id,
                detail="Birth Twin already exists for scope; use Persist Successor",
            )

        new_id = self._allocate_snapshot_id(snapshot_id)
        if isinstance(new_id, TwinPersistenceFailure):
            return TwinPersistenceFailure(
                reason=new_id.reason,
                scope=resolved_scope,
                snapshot_id=new_id.snapshot_id,
                detail=new_id.detail,
            )

        record = TwinSnapshotRecord.create(
            identity=TwinSnapshotIdentity.create(
                new_id,
                sequence=1,
                format_version=SNAPSHOT_FORMAT_VERSION_1_0,
            ),
            scope=resolved_scope,
            twin=twin,
            authorship=TwinAuthorship.BIRTH,
            persisted_at=persisted_at or datetime.now(UTC),
            provenance=provenance,
        )
        self._histories[key] = [record]
        self._snapshot_ids.add(new_id)

        return PersistAcknowledgement(
            snapshot_id=new_id,
            sequence=1,
            scope=resolved_scope,
            authorship=TwinAuthorship.BIRTH,
        )

    def retrieve_current_twin(
        self,
        scope: TwinScope,
    ) -> RetrieveCurrentResult:
        """Retrieve the Twin currently designated for the authorised scope.

        Returns:
            Immutable DigitalTwin, or honesty signal (missing / corrupt /
            unavailable). Never fabricates a Twin.
        """
        if not self._available:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=scope,
                detail="Twin storage unavailable",
            )

        try:
            normalised = TwinScope.create(
                scope.student_id,
                sitting_id=scope.sitting_id,
                curriculum_id=scope.curriculum_id,
            )
        except ValueError as exc:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=scope,
                detail=str(exc),
            )

        history = self._histories.get(self._scope_key(normalised), [])
        if not history:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.MISSING,
                scope=normalised,
                detail="no Twin snapshot for requested scope",
            )

        current = history[-1]
        if not isinstance(current.twin, DigitalTwin):
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.CORRUPT,
                scope=normalised,
                snapshot_id=current.identity.snapshot_id,
                detail="stored cargo is not a DigitalTwin",
            )
        return current.twin

    def persist_successor_twin(
        self,
        twin: DigitalTwin,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        expected_current_snapshot_id: str | None = None,
        provenance: dict[str, Any] | None = None,
        persisted_at: datetime | None = None,
    ) -> PersistSuccessorResult:
        """Persist successor Twin as new current; retain prior as history.

        Does not mutate prior snapshot content. Optional
        ``expected_current_snapshot_id`` enables concurrent-successor honesty.

        Args:
            twin: Complete immutable successor Twin already authored elsewhere.
            scope: Authorised student / sitting scope. Defaults from Twin identity.
            snapshot_id: Optional explicit snapshot identity (must be unique).
            expected_current_snapshot_id: When set, reject if current designation
                no longer matches (Concurrent successor).
            provenance: Opaque lineage cargo preserved without reinterpretation.
            persisted_at: Optional persist timestamp (defaults to UTC now).

        Returns:
            PersistAcknowledgement on success, or TwinPersistenceFailure honesty.
        """
        if not self._available:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                detail="Twin storage unavailable",
            )

        cargo = self._validate_twin_cargo(twin)
        if cargo is not None:
            return cargo

        resolved_scope = scope if scope is not None else self._scope_from_twin(twin)
        if isinstance(resolved_scope, TwinPersistenceFailure):
            return resolved_scope

        identity_check = self._validate_twin_matches_scope(twin, resolved_scope)
        if identity_check is not None:
            return identity_check

        key = self._scope_key(resolved_scope)
        history = self._histories.get(key, [])
        if not history:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.MISSING,
                scope=resolved_scope,
                detail="no Birth Twin to succeed; Persist Birth Twin first",
            )

        current = history[-1]
        if expected_current_snapshot_id is not None:
            expected = expected_current_snapshot_id.strip()
            if expected != current.identity.snapshot_id:
                return TwinPersistenceFailure(
                    reason=TwinPersistenceFailureReason.CONCURRENT,
                    scope=resolved_scope,
                    snapshot_id=current.identity.snapshot_id,
                    detail=(
                        "expected current snapshot no longer designated current"
                    ),
                )

        new_id = self._allocate_snapshot_id(snapshot_id)
        if isinstance(new_id, TwinPersistenceFailure):
            return TwinPersistenceFailure(
                reason=new_id.reason,
                scope=resolved_scope,
                snapshot_id=new_id.snapshot_id,
                detail=new_id.detail,
            )

        sequence = current.identity.sequence + 1
        # Prior record stays untouched in history — only append successor.
        record = TwinSnapshotRecord.create(
            identity=TwinSnapshotIdentity.create(
                new_id,
                sequence=sequence,
                format_version=SNAPSHOT_FORMAT_VERSION_1_0,
            ),
            scope=resolved_scope,
            twin=twin,
            authorship=TwinAuthorship.SUCCESSOR,
            persisted_at=persisted_at or datetime.now(UTC),
            provenance=provenance,
        )
        history.append(record)
        self._histories[key] = history
        self._snapshot_ids.add(new_id)

        return PersistAcknowledgement(
            snapshot_id=new_id,
            sequence=sequence,
            scope=resolved_scope,
            authorship=TwinAuthorship.SUCCESSOR,
        )

    def retrieve_snapshot_history(
        self,
        scope: TwinScope,
    ) -> RetrieveHistoryResult:
        """Return ordered Twin lineage (birth → successors) for the scope.

        Prior snapshots remain historically true. Empty scope yields an empty
        SnapshotHistory (honest emptiness), not invented intermediates.
        """
        if not self._available:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=scope,
                detail="Twin storage unavailable",
            )

        try:
            normalised = TwinScope.create(
                scope.student_id,
                sitting_id=scope.sitting_id,
                curriculum_id=scope.curriculum_id,
            )
        except ValueError as exc:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=scope,
                detail=str(exc),
            )

        history = self._histories.get(self._scope_key(normalised), [])
        for record in history:
            if not isinstance(record.twin, DigitalTwin):
                return TwinPersistenceFailure(
                    reason=TwinPersistenceFailureReason.CORRUPT,
                    scope=normalised,
                    snapshot_id=record.identity.snapshot_id,
                    detail="corrupt Twin in lineage",
                )

        current_id = history[-1].identity.snapshot_id if history else None
        return SnapshotHistory(
            scope=normalised,
            snapshots=tuple(history),
            current_snapshot_id=current_id,
        )

    def determine_current_snapshot(
        self,
        scope: TwinScope,
    ) -> DetermineCurrentResult:
        """Resolve which snapshot is current without inventing educational state."""
        if not self._available:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=scope,
                detail="Twin storage unavailable",
            )

        try:
            normalised = TwinScope.create(
                scope.student_id,
                sitting_id=scope.sitting_id,
                curriculum_id=scope.curriculum_id,
            )
        except ValueError as exc:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=scope,
                detail=str(exc),
            )

        history = self._histories.get(self._scope_key(normalised), [])
        if not history:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.MISSING,
                scope=normalised,
                detail="no current Twin designation for requested scope",
            )

        current = history[-1]
        if not isinstance(current.twin, DigitalTwin):
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.CORRUPT,
                scope=normalised,
                snapshot_id=current.identity.snapshot_id,
                detail="current snapshot cargo is corrupt",
            )

        return CurrentSnapshotRef(
            snapshot_id=current.identity.snapshot_id,
            sequence=current.identity.sequence,
            scope=normalised,
            twin=current.twin,
        )

    # ── Test / adapter seams (non-educational) ───────────────────────────────

    def mark_unavailable(self) -> None:
        """Simulate storage unavailable for honesty-path tests."""
        self._available = False

    def mark_available(self) -> None:
        """Restore storage availability after ``mark_unavailable``."""
        self._available = True

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _scope_key(self, scope: TwinScope) -> str:
        sitting = scope.sitting_id or ""
        curriculum = scope.curriculum_id or ""
        return f"{scope.student_id}\0{sitting}\0{curriculum}"

    def _scope_from_twin(
        self, twin: DigitalTwin
    ) -> TwinScope | TwinPersistenceFailure:
        identity = getattr(twin, "identity", None)
        student_id = getattr(identity, "student_id", None)
        if not isinstance(student_id, str) or not student_id.strip():
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                detail="Twin identity.student_id is required for scope",
            )
        curriculum_id = getattr(identity, "curriculum_id", None)
        return TwinScope.create(
            student_id,
            curriculum_id=curriculum_id if isinstance(curriculum_id, str) else None,
        )

    def _validate_twin_cargo(
        self, twin: object
    ) -> TwinPersistenceFailure | None:
        if twin is None:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                detail="Twin cargo is required; repository never invents Twins",
            )
        if not isinstance(twin, DigitalTwin):
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                detail=f"persist cargo must be DigitalTwin, got {type(twin)!r}",
            )
        return None

    def _validate_twin_matches_scope(
        self,
        twin: DigitalTwin,
        scope: TwinScope,
    ) -> TwinPersistenceFailure | None:
        twin_student = twin.identity.student_id.strip()
        if twin_student != scope.student_id:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=scope,
                detail="Twin student_id does not match authorised scope",
            )
        return None

    def _allocate_snapshot_id(
        self, snapshot_id: str | None
    ) -> str | TwinPersistenceFailure:
        if snapshot_id is None:
            return str(uuid.uuid4())
        if not isinstance(snapshot_id, str) or not snapshot_id.strip():
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                detail="snapshot_id must be a non-empty string when provided",
            )
        normalized = snapshot_id.strip()
        if normalized in self._snapshot_ids:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.DUPLICATE,
                snapshot_id=normalized,
                detail="snapshot identity already exists",
            )
        return normalized
