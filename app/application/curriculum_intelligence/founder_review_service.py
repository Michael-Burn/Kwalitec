"""FounderReviewService — durable review workflow without overwriting provenance."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.audit_service import AuditService
from app.application.curriculum_intelligence.confidence_scoring_service import (
    ConfidenceScoringService,
)
from app.application.curriculum_intelligence.exceptions import (
    CurriculumIntelligenceError,
)
from app.application.curriculum_intelligence.provenance_service import ProvenanceService
from app.domain.curriculum_intelligence.audit import AuditAction
from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind
from app.domain.curriculum_intelligence.provenance import ProvenanceSubjectKind
from app.domain.curriculum_intelligence.review import (
    ReviewDecision,
    ReviewRecord,
    ReviewStatus,
    VerificationStatus,
)
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipConfidenceRecord,
    CipCurriculumEntity,
    CipReviewRecord,
    CipValidationIssue,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


class FounderReviewService:
    """Founder approve / reject / remap workflow for CIP mappings."""

    def __init__(
        self,
        *,
        audit: AuditService | None = None,
        provenance: ProvenanceService | None = None,
        confidence: ConfidenceScoringService | None = None,
    ) -> None:
        self._audit = audit or AuditService()
        self._provenance = provenance or ProvenanceService()
        self._confidence = confidence or ConfidenceScoringService()

    def review_queue(
        self, *, workspace_id: str, document_id: int | None = None
    ) -> list[dict]:
        """Return Founder-facing review queue items (educational concepts only)."""
        q = CipConfidenceRecord.query.filter_by(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, needs_review=True
        )
        if document_id is not None:
            q = q.filter_by(document_id=document_id)
        conf_rows = q.order_by(CipConfidenceRecord.score.asc()).all()

        items: list[dict] = []
        seen: set[str] = set()
        for conf in conf_rows:
            entity = CipCurriculumEntity.query.filter_by(
                entity_id=conf.subject_id
            ).first()
            if entity is None:
                continue
            if workspace_id:
                from app.models.curriculum_studio_foundation import (
                    StudioFoundationDocument,
                )

                doc = db.session.get(StudioFoundationDocument, entity.document_id)
                if doc is None or doc.workspace_id != workspace_id:
                    continue
            status = self.current_status(
                subject_kind=conf.subject_kind, subject_id=conf.subject_id
            )
            if status in {ReviewStatus.APPROVED, ReviewStatus.REJECTED}:
                continue
            if conf.subject_id in seen:
                continue
            seen.add(conf.subject_id)
            prov = self._provenance.get_for_subject(
                subject_kind=conf.subject_kind, subject_id=conf.subject_id
            )
            pages = list(prov.source_pages) if prov else []
            evidence = []
            if prov:
                for ev in prov.evidence:
                    evidence.append(
                        {
                            "page": ev.page_number,
                            "paragraph": ev.paragraph_index,
                            "excerpt": ev.excerpt,
                        }
                    )
            items.append(
                {
                    "entity_id": entity.entity_id,
                    "title": entity.title,
                    "kind": entity.kind,
                    "confidence": round(conf.score, 2),
                    "confidence_percent": int(round(conf.score * 100)),
                    "confidence_reason": conf.reason,
                    "source_pages": pages,
                    "supporting_evidence": evidence,
                    "suggested_learning_objective": self._suggest_lo(entity),
                    "review_status": status.value,
                    "document_id": entity.document_id,
                    "version_label": entity.version_label,
                }
            )

        # Also surface unresolved validation failures as queue entries.
        val_issues = (
            CipValidationIssue.query.filter(
                CipValidationIssue.severity == "error",
                CipValidationIssue.subject_kind == "entity",
            )
            .order_by(CipValidationIssue.id.desc())
            .limit(100)
            .all()
        )
        for issue in val_issues:
            if issue.subject_id in seen:
                continue
            entity = CipCurriculumEntity.query.filter_by(
                entity_id=issue.subject_id
            ).first()
            if entity is None:
                continue
            if workspace_id:
                from app.models.curriculum_studio_foundation import (
                    StudioFoundationDocument,
                )

                doc = db.session.get(StudioFoundationDocument, entity.document_id)
                if doc is None or doc.workspace_id != workspace_id:
                    continue
            seen.add(issue.subject_id)
            items.append(
                {
                    "entity_id": entity.entity_id,
                    "title": entity.title,
                    "kind": entity.kind,
                    "confidence": round(entity.confidence, 2),
                    "confidence_percent": int(round(entity.confidence * 100)),
                    "confidence_reason": issue.message,
                    "source_pages": [],
                    "supporting_evidence": [],
                    "suggested_learning_objective": self._suggest_lo(entity),
                    "review_status": ReviewStatus.NEEDS_REVIEW.value,
                    "document_id": entity.document_id,
                    "version_label": entity.version_label,
                    "validation_issue": issue.kind,
                }
            )
        return items

    def approve(
        self,
        *,
        entity_id: str,
        actor_id: str,
        workspace_id: str,
        reason: str = "",
    ) -> ReviewRecord:
        """Approve a mapped entity without altering provenance."""
        return self._decide(
            entity_id=entity_id,
            actor_id=actor_id,
            workspace_id=workspace_id,
            decision=ReviewDecision.APPROVE,
            review_status=ReviewStatus.APPROVED,
            verification_status=VerificationStatus.VERIFIED,
            reason=reason or "Approved by Founder",
            audit_action=AuditAction.ENTITY_APPROVED,
            remap_target_id="",
        )

    def reject(
        self,
        *,
        entity_id: str,
        actor_id: str,
        workspace_id: str,
        reason: str = "",
    ) -> ReviewRecord:
        """Reject a mapped entity; provenance remains intact."""
        return self._decide(
            entity_id=entity_id,
            actor_id=actor_id,
            workspace_id=workspace_id,
            decision=ReviewDecision.REJECT,
            review_status=ReviewStatus.REJECTED,
            verification_status=VerificationStatus.DISPUTED,
            reason=reason or "Rejected by Founder",
            audit_action=AuditAction.ENTITY_REJECTED,
            remap_target_id="",
        )

    def remap(
        self,
        *,
        entity_id: str,
        actor_id: str,
        workspace_id: str,
        remap_target_id: str,
        reason: str = "",
        suggested_learning_objective: str = "",
    ) -> ReviewRecord:
        """Record a remap decision; does not mutate the original entity row."""
        target = (remap_target_id or "").strip()
        if not target:
            raise CurriculumIntelligenceError(
                "Remap requires a target learning objective or entity id.",
                code="remap_target_required",
            )
        return self._decide(
            entity_id=entity_id,
            actor_id=actor_id,
            workspace_id=workspace_id,
            decision=ReviewDecision.REMAP,
            review_status=ReviewStatus.REMAPPED,
            verification_status=VerificationStatus.DISPUTED,
            reason=reason or "Remapped by Founder",
            audit_action=AuditAction.ENTITY_REMAPPED,
            remap_target_id=target,
            suggested_learning_objective=suggested_learning_objective,
        )

    def current_status(
        self, *, subject_kind: str, subject_id: str
    ) -> ReviewStatus:
        """Latest review status, or needs_review / pending from confidence."""
        row = (
            CipReviewRecord.query.filter_by(
                subject_kind=subject_kind, subject_id=subject_id
            )
            .order_by(CipReviewRecord.id.desc())
            .first()
        )
        if row is not None:
            return ReviewStatus(row.review_status)
        conf = self._confidence.latest_for_subject(
            subject_kind=subject_kind, subject_id=subject_id
        )
        if conf is not None and conf.needs_review:
            return ReviewStatus.NEEDS_REVIEW
        return ReviewStatus.PENDING

    def history_for_entity(self, entity_id: str) -> list[ReviewRecord]:
        """Append-only review history for an entity."""
        rows = (
            CipReviewRecord.query.filter_by(
                subject_kind=ProvenanceSubjectKind.ENTITY.value,
                subject_id=entity_id,
            )
            .order_by(CipReviewRecord.id.asc())
            .all()
        )
        return [self._to_domain(r) for r in rows]

    def entity_details(self, entity_id: str) -> dict | None:
        """Founder-facing entity detail with provenance + confidence + reviews."""
        entity = CipCurriculumEntity.query.filter_by(entity_id=entity_id).first()
        if entity is None:
            return None
        prov = self._provenance.get_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        conf = self._confidence.latest_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        reviews = self.history_for_entity(entity_id)
        return {
            "entity_id": entity.entity_id,
            "kind": entity.kind,
            "title": entity.title,
            "body": entity.body,
            "version_label": entity.version_label,
            "document_id": entity.document_id,
            "parent_entity_id": entity.parent_entity_id,
            "confidence": {
                "score": conf.score if conf else entity.confidence,
                "band": conf.band.value if conf else "",
                "reason": conf.reason if conf else "",
                "needs_review": conf.needs_review if conf else entity.needs_review,
                "factors": [
                    {
                        "code": f.code,
                        "label": f.label,
                        "contribution": f.contribution,
                        "detail": f.detail,
                    }
                    for f in (conf.factors if conf else ())
                ],
            },
            "provenance": None
            if prov is None
            else {
                "provenance_id": prov.provenance_id,
                "source_document_id": prov.source_document_id,
                "source_version": prov.source_version_label,
                "source_pages": list(prov.source_pages),
                "source_paragraphs": list(prov.source_paragraphs),
                "parser_version": prov.parser_version,
                "pipeline_job_id": prov.pipeline_job_id,
                "chain": self._provenance.chain_for_entity(entity_id),
                "evidence": [
                    {
                        "page": e.page_number,
                        "paragraph": e.paragraph_index,
                        "excerpt": e.excerpt,
                        "role": e.evidence_role,
                    }
                    for e in prov.evidence
                ],
            },
            "review_status": self.current_status(
                subject_kind=ProvenanceSubjectKind.ENTITY.value,
                subject_id=entity_id,
            ).value,
            "reviews": [
                {
                    "review_id": r.review_id,
                    "decision": r.decision.value,
                    "status": r.review_status.value,
                    "actor_id": r.actor_id,
                    "reason": r.reason,
                    "created_at": r.created_at_iso,
                }
                for r in reviews
            ],
        }

    def _decide(
        self,
        *,
        entity_id: str,
        actor_id: str,
        workspace_id: str,
        decision: ReviewDecision,
        review_status: ReviewStatus,
        verification_status: VerificationStatus,
        reason: str,
        audit_action: AuditAction,
        remap_target_id: str,
        suggested_learning_objective: str = "",
    ) -> ReviewRecord:
        entity = CipCurriculumEntity.query.filter_by(entity_id=entity_id).first()
        if entity is None:
            raise CurriculumIntelligenceError(
                "Curriculum entity not found.",
                code="entity_not_found",
            )
        conf = self._confidence.latest_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        prov = self._provenance.get_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        now = _utc_now()
        review_id = f"rev-{uuid4().hex[:12]}"
        row = CipReviewRecord(
            review_id=review_id,
            subject_kind=ProvenanceSubjectKind.ENTITY.value,
            subject_id=entity_id,
            document_id=entity.document_id,
            workspace_id=workspace_id,
            decision=decision.value,
            review_status=review_status.value,
            verification_status=verification_status.value,
            actor_id=actor_id or "founder",
            reason=reason,
            suggested_learning_objective=suggested_learning_objective
            or self._suggest_lo(entity),
            remap_target_id=remap_target_id,
            confidence_at_review=conf.score if conf else entity.confidence,
            pipeline_job_id=prov.pipeline_job_id if prov else "",
            provenance_id=prov.provenance_id if prov else None,
            created_at=now,
        )
        db.session.add(row)
        # Clear needs_review flag on confidence snapshot after terminal decision.
        if conf is not None and decision in {
            ReviewDecision.APPROVE,
            ReviewDecision.REJECT,
        }:
            conf_row = CipConfidenceRecord.query.filter_by(
                confidence_id=conf.confidence_id
            ).first()
            if conf_row is not None and decision is ReviewDecision.APPROVE:
                conf_row.needs_review = False
        self._audit.record(
            action=audit_action,
            actor_id=actor_id or "founder",
            subject_kind=ProvenanceSubjectKind.ENTITY.value,
            subject_id=entity_id,
            message=reason,
            document_id=entity.document_id,
            pipeline_job_id=row.pipeline_job_id,
            document_version=entity.version_label,
            workspace_id=workspace_id,
            attributes={"decision": decision.value},
        )
        self._audit.record(
            action=AuditAction.ENTITY_REVIEWED,
            actor_id=actor_id or "founder",
            subject_kind=ProvenanceSubjectKind.ENTITY.value,
            subject_id=entity_id,
            message=f"Reviewed: {decision.value}",
            document_id=entity.document_id,
            pipeline_job_id=row.pipeline_job_id,
            document_version=entity.version_label,
            workspace_id=workspace_id,
        )
        db.session.flush()
        return self._to_domain(row)

    @staticmethod
    def _suggest_lo(entity: CipCurriculumEntity) -> str:
        lo = CurriculumEntityKind.LEARNING_OBJECTIVE.value
        if entity.kind == lo:
            return entity.title[:128]
        cursor = None
        if entity.parent_entity_id:
            cursor = CipCurriculumEntity.query.filter_by(
                entity_id=entity.parent_entity_id
            ).first()
        while cursor is not None:
            if cursor.kind == lo:
                return cursor.title[:128]
            if not cursor.parent_entity_id:
                break
            cursor = CipCurriculumEntity.query.filter_by(
                entity_id=cursor.parent_entity_id
            ).first()
        return ""

    @staticmethod
    def _to_domain(row: CipReviewRecord) -> ReviewRecord:
        return ReviewRecord(
            review_id=row.review_id,
            subject_kind=row.subject_kind,
            subject_id=row.subject_id,
            document_id=row.document_id,
            workspace_id=row.workspace_id,
            decision=ReviewDecision(row.decision),
            review_status=ReviewStatus(row.review_status),
            verification_status=VerificationStatus(row.verification_status),
            actor_id=row.actor_id,
            reason=row.reason,
            suggested_learning_objective=row.suggested_learning_objective,
            remap_target_id=row.remap_target_id,
            confidence_at_review=row.confidence_at_review,
            pipeline_job_id=row.pipeline_job_id,
            provenance_id=row.provenance_id,
            created_at_iso=_iso(row.created_at) if row.created_at else "",
        )
