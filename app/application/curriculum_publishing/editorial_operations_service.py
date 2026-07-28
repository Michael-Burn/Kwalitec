"""Editorial Operations — auditable Founder mutations on draft editions."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.application.curriculum_extraction.graph_validation_service import (
    GraphValidationService,
)
from app.application.curriculum_publishing.audit_trail_service import (
    AuditTrailService,
)
from app.application.curriculum_publishing.dto import MetadataEdit
from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
)
from app.application.curriculum_publishing.exceptions import (
    NodeNotFoundError,
    PublishingGateError,
    gate_from_invariant,
)
from app.domain.curriculum_extraction.publication_state import ValidationStatus
from app.domain.curriculum_publishing.editorial_action import EditorialAction
from app.domain.curriculum_publishing.invariants import (
    PublicationInvariantError,
    assert_can_approve_edition,
    assert_draft_only_editorial,
)
from app.domain.curriculum_publishing.review_state import (
    NodeReviewStatus,
    ReviewStatus,
)
from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgDefinition,
    CkgFormula,
    CkgLearningObjective,
    CkgNodeReviewState,
    CkgPracticeExercise,
    CkgReadingReference,
    CkgSection,
    CkgSubsection,
    CkgSyllabusOutcome,
    CkgTopic,
    CkgValidationReport,
    CkgWorkedExample,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


_METADATA_MODELS: tuple[tuple[type, frozenset[str]], ...] = (
    (
        CkgTopic,
        frozenset({"title", "difficulty", "estimated_study_minutes"}),
    ),
    (
        CkgSection,
        frozenset({"title", "difficulty", "estimated_study_minutes"}),
    ),
    (
        CkgSubsection,
        frozenset({"title", "difficulty", "estimated_study_minutes"}),
    ),
    (
        CkgLearningObjective,
        frozenset(
            {
                "statement",
                "difficulty",
                "estimated_study_minutes",
                "cognitive_level",
                "learning_type",
            }
        ),
    ),
    (CkgDefinition, frozenset({"title", "body"})),
    (CkgFormula, frozenset({"title", "notation"})),
    (CkgWorkedExample, frozenset({"title", "summary"})),
    (CkgPracticeExercise, frozenset({"title", "difficulty"})),
    (CkgReadingReference, frozenset({"title"})),
    (CkgSyllabusOutcome, frozenset({"statement_ref"})),
)


class EditorialOperationsService:
    """Mutate draft editions under Founder editorial governance."""

    def __init__(
        self,
        *,
        loader: EditionGraphLoader | None = None,
        audit: AuditTrailService | None = None,
        validator: GraphValidationService | None = None,
    ) -> None:
        self._loader = loader or EditionGraphLoader()
        self._audit = audit or AuditTrailService()
        self._validator = validator or GraphValidationService()

    def start_review(self, edition_id: str, *, actor: str) -> None:
        """Mark edition review as in progress."""
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state, operation="start review"
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc
        edition.review_status = ReviewStatus.IN_REVIEW.value
        edition.updated_at = _utc_now()
        self._audit.record_editorial(
            edition_id=edition_id,
            action=EditorialAction.START_REVIEW,
            actor=actor,
        )
        db.session.commit()

    def approve_node(
        self,
        edition_id: str,
        stable_id: str,
        *,
        actor: str,
        notes: str = "",
    ) -> None:
        self._set_node_review(
            edition_id,
            stable_id,
            status=NodeReviewStatus.APPROVED,
            actor=actor,
            notes=notes,
            action=EditorialAction.APPROVE_NODE,
        )

    def reject_node(
        self,
        edition_id: str,
        stable_id: str,
        *,
        actor: str,
        notes: str = "",
    ) -> None:
        self._set_node_review(
            edition_id,
            stable_id,
            status=NodeReviewStatus.REJECTED,
            actor=actor,
            notes=notes,
            action=EditorialAction.REJECT_NODE,
        )

    def edit_metadata(
        self,
        edition_id: str,
        stable_id: str,
        edit: MetadataEdit,
        *,
        actor: str,
    ) -> dict[str, Any]:
        """Edit educational metadata on a draft node. Returns applied changes."""
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state, operation="edit metadata"
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        changes = edit.as_changes()
        if not changes:
            raise PublishingGateError("No metadata changes provided")

        applied: dict[str, Any] = {}
        for model, allowed in _METADATA_MODELS:
            row = model.query.filter_by(stable_id=stable_id).first()
            if row is None:
                continue
            before: dict[str, Any] = {}
            after: dict[str, Any] = {}
            for key, value in changes.items():
                if key not in allowed:
                    continue
                if not hasattr(row, key):
                    continue
                before[key] = getattr(row, key)
                setattr(row, key, value)
                after[key] = value
                applied[key] = value
            if applied:
                self._audit.record_editorial(
                    edition_id=edition_id,
                    action=EditorialAction.EDIT_METADATA,
                    actor=actor,
                    stable_id=stable_id,
                    detail={"before": before, "after": after},
                )
                # Metadata edits invalidate prior edition approval.
                if edition.review_status == ReviewStatus.APPROVED.value:
                    edition.review_status = ReviewStatus.IN_REVIEW.value
                    edition.approved_by = None
                    edition.review_completed_at = None
                edition.updated_at = _utc_now()
                db.session.commit()
                return applied

        raise NodeNotFoundError(
            f"No editable node {stable_id} in edition {edition_id}"
        )

    def resolve_validation_issue(
        self,
        edition_id: str,
        *,
        issue_code: str,
        actor: str,
        stable_id: str | None = None,
        resolution_notes: str = "",
    ) -> None:
        """Record resolution of a validation issue (auditable)."""
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state,
                operation="resolve validation issue",
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc
        self._audit.record_editorial(
            edition_id=edition_id,
            action=EditorialAction.RESOLVE_VALIDATION_ISSUE,
            actor=actor,
            stable_id=stable_id,
            detail={
                "issue_code": issue_code,
                "resolution_notes": resolution_notes,
            },
        )
        edition.updated_at = _utc_now()
        db.session.commit()

    def revalidate(self, edition_id: str, *, actor: str) -> dict[str, Any]:
        """Reload draft from ORM, re-run validation, store report."""
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state, operation="revalidate"
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        bundle = self._loader.load_draft_bundle(edition_id)
        report = self._validator.validate(bundle)
        edition.validation_status = (
            ValidationStatus.PASSED.value
            if report.passed
            else ValidationStatus.FAILED.value
        )
        # Failed revalidation clears edition approval.
        if not report.passed and edition.review_status == ReviewStatus.APPROVED.value:
            edition.review_status = ReviewStatus.IN_REVIEW.value
            edition.approved_by = None
            edition.review_completed_at = None

        db.session.add(
            CkgValidationReport(
                report_id=f"val-{uuid4().hex[:12]}",
                edition_id=edition_id,
                passed=report.passed,
                issue_count=report.issue_count,
                report_json=json.dumps(report.to_dict(), sort_keys=True),
                created_at=_utc_now(),
            )
        )
        self._audit.record_editorial(
            edition_id=edition_id,
            action=EditorialAction.REVALIDATE,
            actor=actor,
            detail={
                "passed": report.passed,
                "issue_count": report.issue_count,
            },
        )
        edition.updated_at = _utc_now()
        db.session.commit()
        return report.to_dict()

    def approve_edition(self, edition_id: str, *, actor: str) -> None:
        """Founder edition-level approval (required before publish)."""
        edition = self._loader.require_edition(edition_id)
        rejected = self._rejected_count(edition_id)
        try:
            assert_can_approve_edition(
                publication_state=edition.publication_state,
                validation_status=edition.validation_status,
                rejected_node_count=rejected,
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        now = _utc_now()
        edition.review_status = ReviewStatus.APPROVED.value
        edition.approved_by = (actor or "").strip()
        edition.review_completed_at = now
        edition.updated_at = now
        self._audit.record_editorial(
            edition_id=edition_id,
            action=EditorialAction.APPROVE_EDITION,
            actor=actor,
            detail={"review_completed_at": now.isoformat()},
        )
        db.session.commit()

    def reject_edition(
        self, edition_id: str, *, actor: str, notes: str = ""
    ) -> None:
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state, operation="reject edition"
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc
        edition.review_status = ReviewStatus.REJECTED.value
        edition.approved_by = None
        edition.review_completed_at = None
        edition.updated_at = _utc_now()
        self._audit.record_editorial(
            edition_id=edition_id,
            action=EditorialAction.REJECT_EDITION,
            actor=actor,
            detail={"notes": notes},
        )
        db.session.commit()

    def _set_node_review(
        self,
        edition_id: str,
        stable_id: str,
        *,
        status: NodeReviewStatus,
        actor: str,
        notes: str,
        action: EditorialAction,
    ) -> None:
        edition = self._loader.require_edition(edition_id)
        try:
            assert_draft_only_editorial(
                edition.publication_state, operation=action.value
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        ids = set(self._loader.collect_stable_ids(edition_id))
        if stable_id not in ids:
            raise NodeNotFoundError(
                f"Node {stable_id} not found in edition {edition_id}"
            )

        row = CkgNodeReviewState.query.filter_by(
            edition_id=edition_id, stable_id=stable_id
        ).first()
        now = _utc_now()
        if row is None:
            row = CkgNodeReviewState(
                edition_id=edition_id,
                stable_id=stable_id,
                status=status.value,
                reviewer=(actor or "").strip(),
                notes=notes or "",
                created_at=now,
                updated_at=now,
            )
            db.session.add(row)
        else:
            row.status = status.value
            row.reviewer = (actor or "").strip()
            row.notes = notes or ""
            row.updated_at = now

        if edition.review_status == ReviewStatus.PENDING.value:
            edition.review_status = ReviewStatus.IN_REVIEW.value
        if (
            status is NodeReviewStatus.REJECTED
            and edition.review_status == ReviewStatus.APPROVED.value
        ):
            edition.review_status = ReviewStatus.IN_REVIEW.value
            edition.approved_by = None
            edition.review_completed_at = None

        self._audit.record_editorial(
            edition_id=edition_id,
            action=action,
            actor=actor,
            stable_id=stable_id,
            detail={"status": status.value, "notes": notes},
        )
        edition.updated_at = now
        db.session.commit()

    def _rejected_count(self, edition_id: str) -> int:
        return CkgNodeReviewState.query.filter_by(
            edition_id=edition_id,
            status=NodeReviewStatus.REJECTED.value,
        ).count()
