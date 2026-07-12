"""TwinProvider — Application Layer Twin retrieval adapter.

Retrieves an existing Student Digital Twin for Educational Orchestrator, or
signals honest absence. Owns retrieval, absence signalling, optional adaptation
of TwinRepository (durable load) or an interim TwinSource, and retrieval
validation.

Never computes, updates, or fabricates a Twin. Never persists Twins. Never
invokes StudentCalibrationBuilder, CalibrationBirthPersister, or Educational
Orchestrator. Never derives Readiness, calls Decision / Recommendation /
Mission, or imports Flask / routes / templates / ORM. Twin belief mutation
remains on the Evidence → Twin Update Pipeline path (ADR-002).

Flow: Student Identity → TwinProvider → TwinRepository.retrieve_current_twin
→ DigitalTwin | TwinAbsent. Incomplete or missing persistence yields TwinAbsent,
not a fabricated Twin.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from app.application.twin_repository.twin_repository import TwinRepository
from app.application.twin_repository.types import (
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
)
from app.domain.twin.digital_twin import DigitalTwin


class TwinAbsenceReason(str, Enum):
    """Why TwinProvider could not return a lawful DigitalTwin."""

    MISSING_IDENTITY = "missing_identity"
    MISSING = "missing"
    CORRUPT = "corrupt"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class TwinRetrievalContext:
    """Product / sitting scope for Twin retrieval — wiring only.

    Never an educational scoring input. Never used to invent Twin beliefs.
    """

    curriculum_id: str | None = None
    sitting_id: str | None = None
    surface_intent: str | None = None
    snapshot_hint: str | None = None


@dataclass(frozen=True)
class TwinAbsent:
    """Explicit signal that no lawful Twin can be returned for the request.

    Absence is a first-class outcome — never papered over with a starter Twin
    or Mid preparedness theatre.
    """

    reason: TwinAbsenceReason
    student_id: str | None = None
    detail: str | None = None


class TwinSource(Protocol):
    """Interim persistence load seam for TwinProvider.

    Implementations may adapt legacy / test doubles. They must never fabricate
    Twin beliefs. Returning ``None`` means no Twin exists. Raising signals
    unavailable / unreadable storage for TwinProvider to map to honest absence
    — TwinProvider does not repair corrupt payloads.

    Durable product load prefers ``TwinRepository`` via TwinProvider injection.
    """

    def load(
        self,
        student_id: str,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | None: ...


class TwinProvider:
    """Application retrieval adapter: DigitalTwin or TwinAbsent only.

    Called by Educational Orchestrator (or Application composition). Domains
    never import TwinProvider; they receive Twin snapshots as arguments.
    TwinRepository remains persistence only; TwinProvider maps load honesty.
    """

    def __init__(
        self,
        *,
        repository: TwinRepository | None = None,
        source: TwinSource | None = None,
    ) -> None:
        """Wire durable TwinRepository and/or an interim TwinSource.

        Args:
            repository: TwinRepository persistence adapter. When set, Provider
                delegates current-Twin load to ``retrieve_current_twin`` and maps
                Persistence honesty signals to ``TwinAbsent``.
            source: Interim / test Twin load seam. Used only when ``repository``
                is not configured. When both are unset, retrieval returns
                ``TwinAbsent`` (honest absence).
        """
        self._repository = repository
        self._source = source

    @property
    def repository(self) -> TwinRepository | None:
        """Injected TwinRepository when wired for durable retrieval."""
        return self._repository

    def retrieve(
        self,
        student_id: str | None,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | TwinAbsent:
        """Retrieve an existing Twin for the authorised student scope.

        Args:
            student_id: Authorised learner identity (already ownership-validated
                by Presentation / Application). Required for retrieval.
            context: Optional product / sitting scope and non-authoritative
                retrieval hints (sitting_id / curriculum_id forwarded to
                TwinRepository scope).

        Returns:
            The existing ``DigitalTwin`` snapshot, or ``TwinAbsent`` when no
            Twin exists, identity is missing, the payload is corrupt, or
            storage is unavailable / incomplete.
        """
        normalized = _normalize_student_id(student_id)
        if normalized is None:
            return TwinAbsent(
                reason=TwinAbsenceReason.MISSING_IDENTITY,
                student_id=None,
                detail="authorised student identity is required",
            )

        if self._repository is not None:
            return self._retrieve_from_repository(
                normalized, context=context
            )

        if self._source is None:
            # No TwinRepository and no interim source — honest absence.
            # Do not fabricate a starter Twin from legacy mastery peers.
            return TwinAbsent(
                reason=TwinAbsenceReason.MISSING,
                student_id=normalized,
                detail="no Twin persistence source configured",
            )

        try:
            loaded = self._source.load(normalized, context=context)
        except Exception as exc:
            # Any store failure becomes honest absence — never invent an in-memory Twin.
            return TwinAbsent(
                reason=TwinAbsenceReason.UNAVAILABLE,
                student_id=normalized,
                detail=f"Twin source unavailable: {exc}",
            )

        return _validate_retrieved(loaded, expected_student_id=normalized)

    def _retrieve_from_repository(
        self,
        student_id: str,
        *,
        context: TwinRetrievalContext | None,
    ) -> DigitalTwin | TwinAbsent:
        """Delegate current-Twin load to TwinRepository; map honesty signals."""
        assert self._repository is not None

        sitting_id = context.sitting_id if context is not None else None
        curriculum_id = context.curriculum_id if context is not None else None

        try:
            scope = TwinScope.create(
                student_id,
                sitting_id=sitting_id,
                curriculum_id=curriculum_id,
            )
        except ValueError as exc:
            return TwinAbsent(
                reason=TwinAbsenceReason.CORRUPT,
                student_id=student_id,
                detail=f"invalid Twin retrieval scope: {exc}",
            )

        try:
            result = self._repository.retrieve_current_twin(scope)
        except Exception as exc:
            return TwinAbsent(
                reason=TwinAbsenceReason.UNAVAILABLE,
                student_id=student_id,
                detail=f"TwinRepository unavailable: {exc}",
            )

        if isinstance(result, TwinPersistenceFailure):
            return _map_persistence_failure(
                result, expected_student_id=student_id
            )

        return _validate_retrieved(result, expected_student_id=student_id)


def _map_persistence_failure(
    failure: TwinPersistenceFailure,
    *,
    expected_student_id: str,
) -> TwinAbsent:
    """Map TwinRepository honesty cargo to TwinAbsent — never repair beliefs."""
    reason = failure.reason
    detail = failure.detail

    if reason is TwinPersistenceFailureReason.MISSING:
        return TwinAbsent(
            reason=TwinAbsenceReason.MISSING,
            student_id=expected_student_id,
            detail=detail or "no Twin snapshot for requested scope",
        )
    if reason is TwinPersistenceFailureReason.CORRUPT:
        return TwinAbsent(
            reason=TwinAbsenceReason.CORRUPT,
            student_id=expected_student_id,
            detail=detail or "stored Twin cargo is corrupt",
        )
    if reason is TwinPersistenceFailureReason.UNAVAILABLE:
        return TwinAbsent(
            reason=TwinAbsenceReason.UNAVAILABLE,
            student_id=expected_student_id,
            detail=detail or "Twin storage unavailable",
        )
    # REJECTED / DUPLICATE / CONCURRENT are not expected on retrieve_current;
    # treat as corrupt retrieval honesty rather than fabricating a Twin.
    return TwinAbsent(
        reason=TwinAbsenceReason.CORRUPT,
        student_id=expected_student_id,
        detail=detail or f"TwinRepository retrieve honesty: {reason.value}",
    )


def _normalize_student_id(student_id: str | None) -> str | None:
    """Require a non-blank student identity; never guess."""
    if student_id is None:
        return None
    if not isinstance(student_id, str):
        return None
    normalized = student_id.strip()
    if not normalized:
        return None
    return normalized


def _validate_retrieved(
    loaded: object,
    *,
    expected_student_id: str,
) -> DigitalTwin | TwinAbsent:
    """Accept only a lawful DigitalTwin for the requested student.

    Corrupt or mismatched payloads become TwinAbsent — never repaired.
    """
    if loaded is None:
        return TwinAbsent(
            reason=TwinAbsenceReason.MISSING,
            student_id=expected_student_id,
            detail="no Twin snapshot for requested scope",
        )

    if not isinstance(loaded, DigitalTwin):
        return TwinAbsent(
            reason=TwinAbsenceReason.CORRUPT,
            student_id=expected_student_id,
            detail=f"retrieved payload is not a DigitalTwin ({type(loaded)!r})",
        )

    identity = getattr(loaded, "identity", None)
    twin_student_id = getattr(identity, "student_id", None)
    if not isinstance(twin_student_id, str) or not twin_student_id.strip():
        return TwinAbsent(
            reason=TwinAbsenceReason.CORRUPT,
            student_id=expected_student_id,
            detail="retrieved Twin identity.student_id is missing",
        )

    if twin_student_id.strip() != expected_student_id:
        return TwinAbsent(
            reason=TwinAbsenceReason.CORRUPT,
            student_id=expected_student_id,
            detail=(
                "retrieved Twin student_id does not match authorised identity"
            ),
        )

    return loaded
