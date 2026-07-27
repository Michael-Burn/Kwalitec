"""ConfidenceScoringService — explainable confidence for CIP mappings (CIP-002)."""

from __future__ import annotations

from uuid import uuid4

from app.domain.curriculum_intelligence.confidence import (
    ConfidenceFactor,
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
)
from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeRelation
from app.domain.curriculum_intelligence.provenance import ProvenanceSubjectKind
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipConfidenceFactor,
    CipConfidenceRecord,
    CipStructuralNode,
)


class ConfidenceScoringService:
    """Derive explainable confidence records from mapped entities / relations.

    Does not mutate CIP-001 mapping outputs — records sit alongside them.
    """

    REVIEW_THRESHOLD = 0.6

    def score_entity(
        self,
        entity: CurriculumKnowledgeEntity,
        *,
        provenance_id: str | None = None,
        document_id: int,
    ) -> ConfidenceRecord:
        """Build and persist a confidence record for one curriculum entity."""
        factors = self._entity_factors(entity)
        score = self._clamp(entity.confidence)
        # Prefer pipeline score but never exceed factor-implied ceiling.
        factor_ceiling = self._factor_ceiling(factors)
        if factor_ceiling is not None:
            score = min(score, factor_ceiling)
        reason = self._entity_reason(entity, factors, score)
        needs_review = entity.needs_review or score < self.REVIEW_THRESHOLD
        record = ConfidenceRecord(
            confidence_id=f"conf-{uuid4().hex[:12]}",
            subject_kind=ProvenanceSubjectKind.ENTITY.value,
            subject_id=entity.entity_id,
            score=score,
            band=confidence_band_from_score(score),
            reason=reason,
            factors=tuple(factors),
            needs_review=needs_review,
            review_threshold=self.REVIEW_THRESHOLD,
            provenance_id=provenance_id,
        )
        self._persist(record, document_id=document_id)
        return record

    def score_relation(
        self,
        relation: KnowledgeRelation,
        *,
        provenance_id: str | None = None,
        document_id: int,
    ) -> ConfidenceRecord:
        """Build and persist a confidence record for one knowledge relation."""
        factors = [
            ConfidenceFactor(
                code="edge_confidence",
                label="Graph edge confidence",
                weight=1.0,
                contribution=self._clamp(relation.confidence),
                detail=relation.relation_type.value,
            )
        ]
        if relation.needs_review:
            factors.append(
                ConfidenceFactor(
                    code="review_flag",
                    label="Flagged for review during graph build",
                    weight=0.2,
                    contribution=-0.15,
                    detail="needs_review",
                )
            )
        score = self._clamp(relation.confidence)
        reason = (
            f"Relation {relation.relation_type.value} confidence {score:.2f}"
            + (
                "; sequential dependency inferred"
                if relation.needs_review
                else "; deterministic hierarchy edge"
            )
        )
        record = ConfidenceRecord(
            confidence_id=f"conf-{uuid4().hex[:12]}",
            subject_kind=ProvenanceSubjectKind.RELATION.value,
            subject_id=relation.relation_id,
            score=score,
            band=confidence_band_from_score(score),
            reason=reason[:512],
            factors=tuple(factors),
            needs_review=relation.needs_review or score < self.REVIEW_THRESHOLD,
            review_threshold=self.REVIEW_THRESHOLD,
            provenance_id=provenance_id,
        )
        self._persist(record, document_id=document_id)
        return record

    def latest_for_subject(
        self, *, subject_kind: str, subject_id: str
    ) -> ConfidenceRecord | None:
        """Return the most recent confidence record for a subject."""
        row = (
            CipConfidenceRecord.query.filter_by(
                subject_kind=subject_kind, subject_id=subject_id
            )
            .order_by(CipConfidenceRecord.id.desc())
            .first()
        )
        if row is None:
            return None
        return self._to_domain(row)

    def _entity_factors(
        self, entity: CurriculumKnowledgeEntity
    ) -> list[ConfidenceFactor]:
        factors: list[ConfidenceFactor] = []
        structural = None
        if entity.structural_node_id:
            structural = CipStructuralNode.query.filter_by(
                node_id=entity.structural_node_id
            ).first()

        if structural is not None:
            factors.append(
                ConfidenceFactor(
                    code="parser_confidence",
                    label="Structural parser confidence",
                    weight=0.45,
                    contribution=self._clamp(structural.confidence) * 0.45,
                    detail=structural.kind,
                )
            )
            if structural.kind == "numbered_section":
                factors.append(
                    ConfidenceFactor(
                        code="numbered_heading",
                        label="Detected from numbered heading",
                        weight=0.2,
                        contribution=0.2,
                        detail=structural.title[:120],
                    )
                )
            if structural.source_page is not None:
                factors.append(
                    ConfidenceFactor(
                        code="page_anchor",
                        label="Anchored to source page",
                        weight=0.1,
                        contribution=0.1,
                        detail=f"page {structural.source_page}",
                    )
                )
        else:
            factors.append(
                ConfidenceFactor(
                    code="no_structural_anchor",
                    label="No structural node linked",
                    weight=0.2,
                    contribution=-0.1,
                    detail="",
                )
            )

        if entity.kind is CurriculumEntityKind.LEARNING_OBJECTIVE:
            factors.append(
                ConfidenceFactor(
                    code="objective_heuristic",
                    label="Learning objective inferred from wording",
                    weight=0.15,
                    contribution=0.05,
                    detail="objective hint match",
                )
            )
        if entity.kind is CurriculumEntityKind.SUBJECT:
            factors.append(
                ConfidenceFactor(
                    code="subject_root",
                    label="Subject root from document metadata",
                    weight=0.3,
                    contribution=0.3,
                    detail=entity.title[:120],
                )
            )
        if entity.source_pages:
            factors.append(
                ConfidenceFactor(
                    code="source_pages",
                    label="Source page evidence present",
                    weight=0.1,
                    contribution=0.1,
                    detail=",".join(str(p) for p in entity.source_pages),
                )
            )
        if entity.needs_review:
            factors.append(
                ConfidenceFactor(
                    code="mapper_review_flag",
                    label="Mapper flagged uncertain",
                    weight=0.25,
                    contribution=-0.2,
                    detail=entity.kind.value,
                )
            )
        return factors

    @staticmethod
    def _entity_reason(
        entity: CurriculumKnowledgeEntity,
        factors: list[ConfidenceFactor],
        score: float,
    ) -> str:
        positives = [f.label for f in factors if f.contribution >= 0]
        if score >= 0.85 and positives:
            return (
                f"{', '.join(positives[:3])}, validated by parser."
            )[:512]
        if entity.needs_review or score < 0.6:
            return (
                "Heading inferred or formatting ambiguous; "
                f"confidence {score:.2f} requires Founder review."
            )[:512]
        return (
            f"Mapped as {entity.kind.value} with confidence {score:.2f}."
        )[:512]

    def _persist(self, record: ConfidenceRecord, *, document_id: int) -> None:
        # Replace prior confidence rows for the same subject (keep history via audit).
        prior = CipConfidenceRecord.query.filter_by(
            subject_kind=record.subject_kind, subject_id=record.subject_id
        ).all()
        for row in prior:
            db.session.delete(row)
        db.session.flush()

        root = CipConfidenceRecord(
            confidence_id=record.confidence_id,
            subject_kind=record.subject_kind,
            subject_id=record.subject_id,
            score=record.score,
            band=record.band.value,
            reason=record.reason,
            needs_review=record.needs_review,
            review_threshold=record.review_threshold,
            provenance_id=record.provenance_id,
            document_id=document_id,
        )
        db.session.add(root)
        db.session.flush()
        for factor in record.factors:
            db.session.add(
                CipConfidenceFactor(
                    factor_id=f"cfac-{uuid4().hex[:12]}",
                    confidence_id=record.confidence_id,
                    code=factor.code,
                    label=factor.label,
                    weight=factor.weight,
                    contribution=factor.contribution,
                    detail=factor.detail[:512],
                )
            )

    @staticmethod
    def _to_domain(row: CipConfidenceRecord) -> ConfidenceRecord:
        factors = tuple(
            ConfidenceFactor(
                code=f.code,
                label=f.label,
                weight=f.weight,
                contribution=f.contribution,
                detail=f.detail,
            )
            for f in row.factors
        )
        return ConfidenceRecord(
            confidence_id=row.confidence_id,
            subject_kind=row.subject_kind,
            subject_id=row.subject_id,
            score=row.score,
            band=confidence_band_from_score(row.score),
            reason=row.reason,
            factors=factors,
            needs_review=row.needs_review,
            review_threshold=row.review_threshold,
            provenance_id=row.provenance_id,
        )

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _factor_ceiling(factors: list[ConfidenceFactor]) -> float | None:
        if not factors:
            return None
        total = sum(f.contribution for f in factors)
        # Soft ceiling: base 0.5 + positive contributions, clamped.
        return max(0.0, min(1.0, 0.5 + total * 0.5))
