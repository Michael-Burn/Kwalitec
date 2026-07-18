"""Approval — explicit human gate before publication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ApprovalDecision(StrEnum):
    """Outcome of an approval review."""

    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class Approval:
    """Immutable approval (or rejection) record for a subject version."""

    approval_id: str
    version_id: str
    reviewer_id: str
    decision: ApprovalDecision
    rationale: str = ""
    decided_at: str | None = None

    @classmethod
    def create(
        cls,
        approval_id: str,
        version_id: str,
        reviewer_id: str,
        decision: ApprovalDecision | str,
        *,
        rationale: str = "",
        decided_at: str | None = None,
    ) -> Approval:
        """Construct an Approval after validating invariants."""
        resolved = (
            decision
            if isinstance(decision, ApprovalDecision)
            else ApprovalDecision(str(decision).strip().lower())
        )
        return cls(
            approval_id=_require_non_empty(approval_id, "approval_id"),
            version_id=_require_non_empty(version_id, "version_id"),
            reviewer_id=_require_non_empty(reviewer_id, "reviewer_id"),
            decision=resolved,
            rationale=(rationale or "").strip(),
            decided_at=(
                None
                if decided_at is None
                else _require_non_empty(decided_at, "decided_at")
            ),
        )

    @property
    def is_approved(self) -> bool:
        """True when the decision is APPROVED."""
        return self.decision is ApprovalDecision.APPROVED


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
