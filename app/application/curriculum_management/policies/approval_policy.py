"""Stateless approval policy."""

from __future__ import annotations

from app.application.curriculum_management.exceptions import PolicyViolation
from app.domain.curriculum_management.approval import Approval, ApprovalDecision
from app.domain.curriculum_management.publication_state import PublicationState
from app.domain.curriculum_management.subject_version import SubjectVersion


class ApprovalPolicy:
    """Deterministic approval gate rules (stateless)."""

    @staticmethod
    def assert_can_approve(version: SubjectVersion) -> None:
        """Raise when approval cannot be recorded."""
        if version.state not in {
            PublicationState.PREVIEW_READY,
            PublicationState.APPROVED,
        }:
            raise PolicyViolation(
                "Approval requires PREVIEW_READY (or re-approval of APPROVED); "
                f"got {version.state.value}"
            )
        latest = version.latest_validation
        if latest is None or not latest.passed:
            raise PolicyViolation("Approval requires a passing validation report")
        if not version.assignments:
            raise PolicyViolation("Approval requires at least one blueprint assignment")

    @staticmethod
    def assert_decision_is_approval(approval: Approval) -> None:
        """Raise when decision is not APPROVED."""
        if approval.decision is not ApprovalDecision.APPROVED:
            raise PolicyViolation(
                f"Expected APPROVED decision; got {approval.decision.value}"
            )

    @staticmethod
    def can_advance_to_approved(version: SubjectVersion) -> bool:
        """True when policy preconditions for APPROVED are met."""
        try:
            ApprovalPolicy.assert_can_approve(version)
        except PolicyViolation:
            return False
        return True
