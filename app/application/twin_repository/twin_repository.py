"""TwinRepository — SQLAlchemy-backed durable Twin snapshot adapter.

Persists and retrieves immutable Digital Twin snapshots via SQLite /
SQLAlchemy. Owns persist / load / current designation / history / honesty
signalling only.

Never creates Twins. Never mutates stored snapshot rows. Never performs
educational reasoning. Never invokes readiness / decision / recommendation /
mission engines. Never participates in product-day composition.

Contract operations match Capability 3.7.3 Version 1.0. Storage technology
is an Application adapter concern (Capability 3.8.2); Domains remain free of ORM.

See Capabilities 3.7.1–3.7.3, 3.8.2, and APPLICATION_LAYER_ARCHITECTURE.md.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from app.application.twin_repository.codec import (
    TwinCodecError,
    decode_provenance,
    decode_twin,
    encode_provenance,
    encode_twin,
)
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
from app.extensions import db
from app.models.twin_snapshot import TwinSnapshot

logger = logging.getLogger(__name__)

PersistBirthResult = PersistAcknowledgement | TwinPersistenceFailure
PersistSuccessorResult = PersistAcknowledgement | TwinPersistenceFailure
RetrieveCurrentResult = DigitalTwin | TwinPersistenceFailure
RetrieveHistoryResult = SnapshotHistory | TwinPersistenceFailure
DetermineCurrentResult = CurrentSnapshotRef | TwinPersistenceFailure


class TwinRepository:
    """Durable Application persistence adapter: immutable Twin snapshots only.

    Calibration birth and update-strategy succession produce Twins elsewhere.
    This repository stores and returns them via SQLAlchemy. Domains never
    import this class; they receive Twin snapshots as arguments.
    """

    def __init__(self) -> None:
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

        try:
            existing = self._ordered_rows(resolved_scope)
            if existing:
                current = existing[-1]
                return TwinPersistenceFailure(
                    reason=TwinPersistenceFailureReason.DUPLICATE,
                    scope=resolved_scope,
                    snapshot_id=current.snapshot_id,
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

            when = persisted_at or datetime.now(UTC)
            twin_payload = encode_twin(twin)
            row = TwinSnapshot(
                snapshot_id=new_id,
                student_id=resolved_scope.student_id,
                sitting_id=resolved_scope.sitting_id,
                curriculum_id=resolved_scope.curriculum_id,
                sequence=1,
                format_version=SNAPSHOT_FORMAT_VERSION_1_0,
                authorship=TwinAuthorship.BIRTH.value,
                twin_payload=twin_payload,
                provenance_payload=encode_provenance(provenance),
                persisted_at=self._naive_utc(when),
            )
            db.session.add(row)
            db.session.commit()
        except TwinCodecError as exc:
            db.session.rollback()
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=resolved_scope,
                detail=str(exc),
            )
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.warning("Twin persist birth storage unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=resolved_scope,
                detail="Twin storage unavailable",
            )

        ack = PersistAcknowledgement(
            snapshot_id=new_id,
            sequence=1,
            scope=resolved_scope,
            authorship=TwinAuthorship.BIRTH,
        )
        self._observe_twin_evolved(ack, twin_payload)
        return ack

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

        try:
            rows = self._ordered_rows(normalised)
        except SQLAlchemyError as exc:
            logger.warning("Twin retrieve current storage unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=normalised,
                detail="Twin storage unavailable",
            )

        if not rows:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.MISSING,
                scope=normalised,
                detail="no Twin snapshot for requested scope",
            )

        current = rows[-1]
        try:
            return decode_twin(current.twin_payload)
        except TwinCodecError as exc:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.CORRUPT,
                scope=normalised,
                snapshot_id=current.snapshot_id,
                detail=str(exc),
            )

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

        Does not mutate prior snapshot rows. Optional
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

        try:
            history = self._ordered_rows(resolved_scope)
            if not history:
                return TwinPersistenceFailure(
                    reason=TwinPersistenceFailureReason.MISSING,
                    scope=resolved_scope,
                    detail="no Birth Twin to succeed; Persist Birth Twin first",
                )

            current = history[-1]
            if expected_current_snapshot_id is not None:
                expected = expected_current_snapshot_id.strip()
                if expected != current.snapshot_id:
                    return TwinPersistenceFailure(
                        reason=TwinPersistenceFailureReason.CONCURRENT,
                        scope=resolved_scope,
                        snapshot_id=current.snapshot_id,
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

            sequence = current.sequence + 1
            when = persisted_at or datetime.now(UTC)
            twin_payload = encode_twin(twin)
            # Prior rows stay untouched — only insert successor.
            row = TwinSnapshot(
                snapshot_id=new_id,
                student_id=resolved_scope.student_id,
                sitting_id=resolved_scope.sitting_id,
                curriculum_id=resolved_scope.curriculum_id,
                sequence=sequence,
                format_version=SNAPSHOT_FORMAT_VERSION_1_0,
                authorship=TwinAuthorship.SUCCESSOR.value,
                twin_payload=twin_payload,
                provenance_payload=encode_provenance(provenance),
                persisted_at=self._naive_utc(when),
            )
            db.session.add(row)
            db.session.commit()
        except TwinCodecError as exc:
            db.session.rollback()
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.REJECTED,
                scope=resolved_scope,
                detail=str(exc),
            )
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.warning("Twin persist successor storage unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=resolved_scope,
                detail="Twin storage unavailable",
            )

        ack = PersistAcknowledgement(
            snapshot_id=new_id,
            sequence=sequence,
            scope=resolved_scope,
            authorship=TwinAuthorship.SUCCESSOR,
        )
        self._observe_twin_evolved(ack, twin_payload)
        return ack

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

        try:
            rows = self._ordered_rows(normalised)
        except SQLAlchemyError as exc:
            logger.warning("Twin retrieve history storage unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=normalised,
                detail="Twin storage unavailable",
            )

        records: list[TwinSnapshotRecord] = []
        for row in rows:
            try:
                twin = decode_twin(row.twin_payload)
                provenance = decode_provenance(row.provenance_payload)
            except TwinCodecError as exc:
                return TwinPersistenceFailure(
                    reason=TwinPersistenceFailureReason.CORRUPT,
                    scope=normalised,
                    snapshot_id=row.snapshot_id,
                    detail=str(exc) or "corrupt Twin in lineage",
                )
            records.append(
                TwinSnapshotRecord.create(
                    identity=TwinSnapshotIdentity.create(
                        row.snapshot_id,
                        sequence=row.sequence,
                        format_version=row.format_version,
                    ),
                    scope=normalised,
                    twin=twin,
                    authorship=TwinAuthorship(row.authorship),
                    persisted_at=row.persisted_at,
                    provenance=provenance,
                )
            )

        current_id = records[-1].identity.snapshot_id if records else None
        return SnapshotHistory(
            scope=normalised,
            snapshots=tuple(records),
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

        try:
            rows = self._ordered_rows(normalised)
        except SQLAlchemyError as exc:
            logger.warning("Twin determine current storage unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                scope=normalised,
                detail="Twin storage unavailable",
            )

        if not rows:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.MISSING,
                scope=normalised,
                detail="no current Twin designation for requested scope",
            )

        current = rows[-1]
        try:
            twin = decode_twin(current.twin_payload)
        except TwinCodecError as exc:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.CORRUPT,
                scope=normalised,
                snapshot_id=current.snapshot_id,
                detail=str(exc) or "current snapshot cargo is corrupt",
            )

        return CurrentSnapshotRef(
            snapshot_id=current.snapshot_id,
            sequence=current.sequence,
            scope=normalised,
            twin=twin,
        )

    # ── Test / adapter seams (non-educational) ───────────────────────────────

    def mark_unavailable(self) -> None:
        """Simulate storage unavailable for honesty-path tests."""
        self._available = False

    def mark_available(self) -> None:
        """Restore storage availability after ``mark_unavailable``."""
        self._available = True

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _ordered_rows(self, scope: TwinScope) -> list[TwinSnapshot]:
        query = TwinSnapshot.query.filter_by(student_id=scope.student_id)
        if scope.sitting_id is None:
            query = query.filter(TwinSnapshot.sitting_id.is_(None))
        else:
            query = query.filter_by(sitting_id=scope.sitting_id)
        if scope.curriculum_id is None:
            query = query.filter(TwinSnapshot.curriculum_id.is_(None))
        else:
            query = query.filter_by(curriculum_id=scope.curriculum_id)
        return query.order_by(TwinSnapshot.sequence.asc()).all()

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
        try:
            exists = (
                TwinSnapshot.query.filter_by(snapshot_id=normalized).first()
                is not None
            )
        except SQLAlchemyError as exc:
            logger.warning("Twin snapshot id lookup unavailable: %s", exc)
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.UNAVAILABLE,
                snapshot_id=normalized,
                detail="Twin storage unavailable",
            )
        if exists:
            return TwinPersistenceFailure(
                reason=TwinPersistenceFailureReason.DUPLICATE,
                snapshot_id=normalized,
                detail="snapshot identity already exists",
            )
        return normalized

    @staticmethod
    def _observe_twin_evolved(
        ack: PersistAcknowledgement,
        encoded_twin_payload: str,
    ) -> None:
        """PRD-001 Phase E — observe Twin succession after durable commit."""
        from app.application.twin_repository.observation import (
            observe_twin_evolved_after_persist,
        )

        observe_twin_evolved_after_persist(
            ack,
            encoded_twin_payload=encoded_twin_payload,
        )

    @staticmethod
    def _naive_utc(value: datetime) -> datetime:
        """Store UTC timestamps as naive datetime for SQLite DateTime columns."""
        if value.tzinfo is not None:
            return value.astimezone(UTC).replace(tzinfo=None)
        return value
