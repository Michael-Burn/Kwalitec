"""ApprovalService — human approval gate before publication."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import approval_snapshot
from app.application.curriculum_management.dto.approval_snapshot import (
    ApprovalSnapshot,
)
from app.application.curriculum_management.exceptions import (
    ApprovalError,
    VersionNotFound,
)
from app.application.curriculum_management.policies.approval_policy import (
    ApprovalPolicy,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.domain.curriculum_management.approval import Approval, ApprovalDecision
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class ApprovalService:
    """Record approval decisions for subject versions."""

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def approve(
        self,
        version_id: str,
        reviewer_id: str,
        *,
        rationale: str = "",
        decided_at: str | None = None,
        approval_id: str | None = None,
        advance_state: bool = True,
    ) -> ApprovalSnapshot:
        """Record an APPROVED decision and optionally advance state."""
        return self._decide(
            version_id,
            reviewer_id,
            ApprovalDecision.APPROVED,
            rationale=rationale,
            decided_at=decided_at,
            approval_id=approval_id,
            advance_state=advance_state,
        )

    def reject(
        self,
        version_id: str,
        reviewer_id: str,
        *,
        rationale: str = "",
        decided_at: str | None = None,
        approval_id: str | None = None,
    ) -> ApprovalSnapshot:
        """Record a REJECTED decision (does not advance publication)."""
        return self._decide(
            version_id,
            reviewer_id,
            ApprovalDecision.REJECTED,
            rationale=rationale,
            decided_at=decided_at,
            approval_id=approval_id,
            advance_state=False,
        )

    def latest(self, version_id: str) -> ApprovalSnapshot | None:
        """Return the latest approval snapshot, or None."""
        version = self._require_version(version_id)
        approval = version.latest_approval
        if approval is None:
            return None
        return approval_snapshot(approval)

    def _decide(
        self,
        version_id: str,
        reviewer_id: str,
        decision: ApprovalDecision,
        *,
        rationale: str,
        decided_at: str | None,
        approval_id: str | None,
        advance_state: bool,
    ) -> ApprovalSnapshot:
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        if decision is ApprovalDecision.APPROVED:
            ApprovalPolicy.assert_can_approve(version)
        elif version.state not in {
            PublicationState.PREVIEW_READY,
            PublicationState.APPROVED,
            PublicationState.BLUEPRINT_ASSIGNED,
        }:
            raise ApprovalError(
                f"Cannot record decision in state {version.state.value}"
            )

        aid = approval_id or self._catalogue.next_id("approval")
        approval = Approval.create(
            aid,
            version_id,
            reviewer_id,
            decision,
            rationale=rationale,
            decided_at=decided_at,
        )
        version = version.with_approval(approval)

        if (
            advance_state
            and decision is ApprovalDecision.APPROVED
            and version.state is PublicationState.PREVIEW_READY
        ):
            publication = version.publication
            assert publication is not None
            publication = publication.transition(
                PublicationTransitionEvent.MARK_APPROVED,
                actor_id=reviewer_id,
                reason="approved",
                occurred_at=decided_at,
            )
            version = version.with_publication(publication)

        self._catalogue.put_version(version)
        return approval_snapshot(approval)

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
