"""TwinProvider — Application Layer Twin retrieval adapter.

Retrieves an existing Student Digital Twin for Educational Orchestrator, or
signals honest absence. Owns retrieval, absence signalling, optional adaptation
of an interim / future persistence source, and retrieval validation.

Never computes, updates, or fabricates a Twin. Never derives Readiness, calls
Decision / Recommendation / Mission, or imports Flask / routes / templates /
ORM. Twin belief mutation remains on the Evidence → Twin Update Pipeline path
(ADR-002). Durable TwinRepository is future; incomplete persistence yields
TwinAbsent, not a fabricated Twin.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

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
    """Interim or future persistence load seam for TwinProvider.

    Implementations may adapt legacy / durable storage. They must never
    fabricate Twin beliefs. Returning ``None`` means no Twin exists.
    Raising signals unavailable / unreadable storage for TwinProvider to map
    to honest absence — TwinProvider does not repair corrupt payloads.
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
    """

    def __init__(self, *, source: TwinSource | None = None) -> None:
        """Wire an optional Twin load source.

        Args:
            source: Interim / future persistence adapter. When ``None``,
                durable Twin persistence is treated as incomplete and every
                retrieval returns ``TwinAbsent`` (honest absence).
        """
        self._source = source

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
                retrieval hints.

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

        if self._source is None:
            # TwinRepository / durable Twin persistence is not yet available.
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
