"""EvidenceUpdateResult — summary of an educational evidence update.

Reports what was stored (or skipped as duplicate). Never carries diagnosis,
recommendations, or planning outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvidenceUpdateOutcome(StrEnum):
    """Outcome of an evidence update attempt."""

    APPLIED = "applied"
    DUPLICATE = "duplicate"


@dataclass(frozen=True, slots=True)
class EvidenceUpdateAuditEntry:
    """One auditable step recorded during evidence update."""

    kind: str
    detail: str
    evidence_id: str = ""

    def __post_init__(self) -> None:
        kind = (self.kind or "").strip()
        if not kind:
            raise ValueError("kind is required")
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "detail", (self.detail or "").strip())
        object.__setattr__(
            self, "evidence_id", (self.evidence_id or "").strip()
        )


@dataclass(frozen=True, slots=True)
class EvidenceUpdateResult:
    """Immutable summary returned after validating, transforming, and storing.

    Attributes:
        evidence_id: Stable evidence identity.
        student_id: Learner identity on the stored (or existing) record.
        outcome: Whether the update was newly applied or an idempotent duplicate.
        item_count: Number of observational items on the evidence record.
        strength_level: Epistemic strength vocabulary from the Evidence domain.
        confidence_level: Observational recording-confidence vocabulary.
        status: Evidence record lifecycle status.
        twin_updated: True when Twin evidence history was appended in this call.
        audit_trail: Ordered audit entries for this update attempt.
    """

    evidence_id: str
    student_id: str
    outcome: EvidenceUpdateOutcome
    item_count: int
    strength_level: str
    confidence_level: str
    status: str
    twin_updated: bool
    audit_trail: tuple[EvidenceUpdateAuditEntry, ...] = ()

    @property
    def applied(self) -> bool:
        """True when a new evidence record was stored in this call."""
        return self.outcome is EvidenceUpdateOutcome.APPLIED

    @property
    def duplicate(self) -> bool:
        """True when an identical evidence identity was already present."""
        return self.outcome is EvidenceUpdateOutcome.DUPLICATE

    def __post_init__(self) -> None:
        evidence_id = (self.evidence_id or "").strip()
        if not evidence_id:
            raise ValueError("evidence_id is required")
        object.__setattr__(self, "evidence_id", evidence_id)

        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ValueError("student_id is required")
        object.__setattr__(self, "student_id", student_id)

        if not isinstance(self.outcome, EvidenceUpdateOutcome):
            raise ValueError("outcome must be an EvidenceUpdateOutcome")

        if isinstance(self.item_count, bool) or not isinstance(self.item_count, int):
            raise ValueError("item_count must be an int")
        if self.item_count < 0:
            raise ValueError("item_count must be >= 0")

        object.__setattr__(
            self, "strength_level", (self.strength_level or "").strip()
        )
        object.__setattr__(
            self, "confidence_level", (self.confidence_level or "").strip()
        )
        object.__setattr__(self, "status", (self.status or "").strip())

        if not isinstance(self.twin_updated, bool):
            raise ValueError("twin_updated must be a bool")

        trail = tuple(self.audit_trail or ())
        for entry in trail:
            if not isinstance(entry, EvidenceUpdateAuditEntry):
                raise ValueError(
                    "audit_trail entries must be EvidenceUpdateAuditEntry"
                )
        object.__setattr__(self, "audit_trail", trail)
