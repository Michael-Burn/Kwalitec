"""Publication Engine — Founder-explicit draft → published transition."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import or_

from app.application.curriculum_publishing.audit_trail_service import (
    AuditTrailService,
)
from app.application.curriculum_publishing.dto import PublicationResult
from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
)
from app.application.curriculum_publishing.edition_snapshot_service import (
    EditionSnapshotService,
)
from app.application.curriculum_publishing.exceptions import (
    PublishingGateError,
    gate_from_invariant,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.curriculum_publishing.invariants import (
    PublicationInvariant,
    PublicationInvariantError,
    assert_can_publish,
)
from app.domain.curriculum_publishing.review_state import NodeReviewStatus
from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgDefinition,
    CkgEdge,
    CkgFormula,
    CkgGraphEdition,
    CkgLearningObjective,
    CkgLoLink,
    CkgNodeProvenance,
    CkgNodeReviewState,
    CkgPracticeExercise,
    CkgReadingReference,
    CkgSection,
    CkgSubject,
    CkgSubsection,
    CkgSyllabusOutcome,
    CkgTopic,
    CkgWorkedExample,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class PublicationEngine:
    """Publish a Founder-approved draft as the sole published edition per subject.

    Validation alone never publishes. Archives any previously published edition
    for the same subject after snapshotting it for history.
    """

    def __init__(
        self,
        *,
        loader: EditionGraphLoader | None = None,
        snapshots: EditionSnapshotService | None = None,
        audit: AuditTrailService | None = None,
    ) -> None:
        self._loader = loader or EditionGraphLoader()
        self._snapshots = snapshots or EditionSnapshotService(self._loader)
        self._audit = audit or AuditTrailService()

    def publish(
        self,
        edition_id: str,
        *,
        publisher: str,
        rationale: str,
    ) -> PublicationResult:
        """Execute the publication transition with full auditability."""
        edition = self._loader.require_edition(edition_id)
        rejected = CkgNodeReviewState.query.filter_by(
            edition_id=edition_id,
            status=NodeReviewStatus.REJECTED.value,
        ).count()
        try:
            assert_can_publish(
                publication_state=edition.publication_state,
                validation_status=edition.validation_status,
                review_status=edition.review_status,
                publisher=publisher,
                rationale=rationale,
                rejected_node_count=rejected,
            )
        except PublicationInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        previous = (
            CkgGraphEdition.query.filter_by(
                subject_code=edition.subject_code,
                publication_state=PublicationState.PUBLISHED.value,
            )
            .filter(CkgGraphEdition.edition_id != edition_id)
            .first()
        )

        # Live node tables hold at most one graph per subject. A successor draft
        # may only exist after prepare_successor_draft archived the prior
        # published live nodes. If a published row still owns live nodes while
        # this draft also has nodes, refuse rather than corrupt identity.
        if previous is not None:
            prev_subject = CkgSubject.query.filter_by(
                graph_edition_id=previous.edition_id
            ).first()
            draft_subject = CkgSubject.query.filter_by(
                graph_edition_id=edition_id
            ).first()
            if prev_subject is not None and draft_subject is not None:
                raise PublishingGateError(
                    f"[{PublicationInvariant.SINGLE_PUBLISHED_PER_SUBJECT.value}] "
                    "Previous published edition still owns live nodes; call "
                    "prepare_successor_draft before extracting a successor draft"
                )

        previous_edition_id = previous.edition_id if previous else None
        if previous is not None:
            # Snapshot if none exists yet, then archive metadata only.
            if self._snapshots.latest_for_edition(previous.edition_id) is None:
                self._snapshots.capture(
                    previous.edition_id,
                    capture_reason="archive_before_publish",
                    captured_by=publisher,
                )
            previous.publication_state = PublicationState.ARCHIVED.value
            previous.updated_at = _utc_now()
        elif previous_edition_id is None:
            # After prepare_successor_draft the prior edition is already archived;
            # still record lineage to the most recent archived edition.
            prior_archived = (
                CkgGraphEdition.query.filter_by(
                    subject_code=edition.subject_code,
                    publication_state=PublicationState.ARCHIVED.value,
                )
                .filter(CkgGraphEdition.edition_id != edition_id)
                .order_by(CkgGraphEdition.updated_at.desc())
                .first()
            )
            if prior_archived is not None:
                previous_edition_id = prior_archived.edition_id

        snapshot_id = self._snapshots.capture(
            edition_id,
            capture_reason="publication",
            captured_by=publisher,
        )

        now = _utc_now()
        edition.publication_state = PublicationState.PUBLISHED.value
        edition.published_at = now
        edition.published_by = (publisher or "").strip()
        edition.previous_edition_id = previous_edition_id
        edition.publication_rationale = (rationale or "").strip()
        edition.updated_at = now

        record_id = self._audit.record_publication(
            edition_id=edition_id,
            subject_code=edition.subject_code,
            publisher=publisher,
            published_at=now,
            previous_edition_id=previous_edition_id,
            publication_rationale=rationale,
            validation_status=edition.validation_status,
            review_status=edition.review_status,
            review_completed_at=edition.review_completed_at,
            snapshot_id=snapshot_id,
            detail={
                "edition_label": edition.edition_label,
                "title": edition.title,
            },
        )
        db.session.commit()

        return PublicationResult(
            edition_id=edition_id,
            subject_code=edition.subject_code,
            publication_record_id=record_id,
            snapshot_id=snapshot_id,
            previous_edition_id=previous_edition_id,
            published_at=now.isoformat(),
            publisher=(publisher or "").strip(),
        )

    def prepare_successor_draft(
        self,
        subject_code: str,
        *,
        actor: str,
        rationale: str,
    ) -> str | None:
        """Archive the published edition for a subject and clear live nodes.

        Enables EI-002 extraction of a new edition_label without stable_id
        collisions. Returns the archived edition_id, or None if none published.
        """
        code = subject_code.upper()
        published = CkgGraphEdition.query.filter_by(
            subject_code=code,
            publication_state=PublicationState.PUBLISHED.value,
        ).first()
        if published is None:
            return None
        if not (rationale or "").strip():
            raise PublishingGateError(
                "Rationale is required to archive a published edition "
                "for successor draft preparation"
            )

        snapshot_id = self._snapshots.capture(
            published.edition_id,
            capture_reason="successor_prepare",
            captured_by=actor,
        )
        self._delete_live_graph(published.edition_id, code)
        published.publication_state = PublicationState.ARCHIVED.value
        published.updated_at = _utc_now()
        self._audit.record_editorial(
            edition_id=published.edition_id,
            action="successor_prepare",
            actor=actor,
            detail={
                "rationale": rationale,
                "snapshot_id": snapshot_id,
                "subject_code": code,
            },
        )
        db.session.commit()
        return published.edition_id

    def _delete_live_graph(self, edition_id: str, subject_code: str) -> None:
        """Remove live nodes/edges for a subject after snapshot archive."""
        prefix = subject_code.upper()
        subjects = CkgSubject.query.filter_by(graph_edition_id=edition_id).all()
        subject_ids = [s.stable_id for s in subjects] or [prefix]

        CkgNodeProvenance.query.filter_by(edition_id=edition_id).delete()
        CkgNodeReviewState.query.filter_by(edition_id=edition_id).delete()
        # Keep validation reports and publication audits for history.

        for model in (
            CkgDefinition,
            CkgFormula,
            CkgWorkedExample,
            CkgPracticeExercise,
            CkgReadingReference,
            CkgSyllabusOutcome,
        ):
            model.query.filter(
                or_(
                    model.stable_id == prefix,
                    model.stable_id.like(f"{prefix}.%"),
                )
            ).delete(synchronize_session=False)

        lo_rows = CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.like(f"{prefix}.%")
        ).all()
        lo_ids = [r.stable_id for r in lo_rows]
        if lo_ids:
            CkgLoLink.query.filter(CkgLoLink.lo_stable_id.in_(lo_ids)).delete(
                synchronize_session=False
            )

        CkgEdge.query.filter(
            or_(
                CkgEdge.from_stable_id == prefix,
                CkgEdge.from_stable_id.like(f"{prefix}.%"),
                CkgEdge.to_stable_id == prefix,
                CkgEdge.to_stable_id.like(f"{prefix}.%"),
            )
        ).delete(synchronize_session=False)

        CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgSubsection.query.filter(
            CkgSubsection.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgSection.query.filter(
            CkgSection.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgTopic.query.filter(CkgTopic.stable_id.like(f"{prefix}.%")).delete(
            synchronize_session=False
        )
        CkgSubject.query.filter(CkgSubject.stable_id.in_(subject_ids)).delete(
            synchronize_session=False
        )
        db.session.flush()
