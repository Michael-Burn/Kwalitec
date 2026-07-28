"""Integrity invariants for Learning Evidence recording (EI-005).

Principle 1 — Twin beliefs must originate from recorded evidence.
Principle 2 — Evidence is immutable; corrections are additional events.
Principle 3 — Inference is a separate concern; this layer records only.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import StrEnum

from app.domain.learning_evidence.evidence_type import (
    EvidenceSource,
    EvidenceType,
    is_extensible_type_token,
    normalise_evidence_type,
)


class EvidenceInvariant(StrEnum):
    """Named evidence integrity invariants."""

    ACTIVE_INSTANCE_REQUIRED = "active_instance_required"
    NODE_IN_INSTANCE = "node_in_instance"
    VALID_TIMESTAMP = "valid_timestamp"
    VALID_EVIDENCE_TYPE = "valid_evidence_type"
    VALID_SOURCE = "valid_source"
    PAYLOAD_SCHEMA = "payload_schema"
    INSTANCE_REQUIRED = "instance_required"
    NODE_REQUIRED = "node_required"


class EvidenceInvariantError(ValueError):
    """Raised when a learning evidence invariant is violated."""

    def __init__(self, invariant: EvidenceInvariant, message: str) -> None:
        self.invariant = invariant
        super().__init__(f"[{invariant.value}] {message}")


def assert_valid_timestamp(
    occurred_at: datetime | None,
    *,
    now: datetime | None = None,
    max_future: timedelta = timedelta(days=1),
) -> None:
    """Reject missing or absurdly future timestamps."""
    if occurred_at is None:
        raise EvidenceInvariantError(
            EvidenceInvariant.VALID_TIMESTAMP,
            "occurred_at is required",
        )
    if not isinstance(occurred_at, datetime):
        raise EvidenceInvariantError(
            EvidenceInvariant.VALID_TIMESTAMP,
            f"occurred_at must be datetime, got {type(occurred_at).__name__}",
        )

    reference = now or datetime.now(UTC).replace(tzinfo=None)
    candidate = occurred_at.replace(tzinfo=None) if occurred_at.tzinfo else occurred_at
    if candidate > reference + max_future:
        raise EvidenceInvariantError(
            EvidenceInvariant.VALID_TIMESTAMP,
            f"occurred_at {candidate.isoformat()} is more than "
            f"{max_future.days} day(s) in the future",
        )


def assert_can_record(
    *,
    instance_id: str | None,
    instance_is_active: bool | None,
    node_stable_id: str | None,
    node_belongs_to_instance: bool,
    evidence_type: str | EvidenceType,
    source: str | EvidenceSource,
    occurred_at: datetime | None,
    now: datetime | None = None,
) -> str:
    """Validate a record-evidence request; return normalised evidence type.

    Args:
        instance_id: Student Curriculum Instance business id.
        instance_is_active: Whether the SCI is active (None = missing).
        node_stable_id: Curriculum node stable id.
        node_belongs_to_instance: True when node state exists for the SCI.
        evidence_type: Catalogue or extensible snake_case type.
        source: Observation source channel.
        occurred_at: When the educational activity occurred.
        now: Optional clock for timestamp checks.

    Returns:
        Normalised evidence type string.

    Raises:
        EvidenceInvariantError: When any integrity gate fails.
    """
    if not (instance_id or "").strip():
        raise EvidenceInvariantError(
            EvidenceInvariant.INSTANCE_REQUIRED,
            "A Student Curriculum Instance id is required",
        )
    if instance_is_active is None:
        raise EvidenceInvariantError(
            EvidenceInvariant.ACTIVE_INSTANCE_REQUIRED,
            f"Student Curriculum Instance {instance_id!r} was not found",
        )
    if not instance_is_active:
        raise EvidenceInvariantError(
            EvidenceInvariant.ACTIVE_INSTANCE_REQUIRED,
            f"Student Curriculum Instance {instance_id!r} is not active",
        )

    if not (node_stable_id or "").strip():
        raise EvidenceInvariantError(
            EvidenceInvariant.NODE_REQUIRED,
            "A curriculum node_stable_id is required",
        )
    if not node_belongs_to_instance:
        raise EvidenceInvariantError(
            EvidenceInvariant.NODE_IN_INSTANCE,
            f"Node {node_stable_id!r} is not part of instance {instance_id!r}",
        )

    normalised_type = normalise_evidence_type(evidence_type)
    if not normalised_type or not is_extensible_type_token(normalised_type):
        raise EvidenceInvariantError(
            EvidenceInvariant.VALID_EVIDENCE_TYPE,
            f"Invalid evidence_type {evidence_type!r}; expected snake_case token",
        )

    source_value = (
        source.value if isinstance(source, EvidenceSource) else (source or "").strip()
    )
    if source_value not in {member.value for member in EvidenceSource}:
        raise EvidenceInvariantError(
            EvidenceInvariant.VALID_SOURCE,
            f"Invalid evidence source {source!r}",
        )

    assert_valid_timestamp(occurred_at, now=now)
    return normalised_type
