"""PipelineMetricsService — CIP quality metrics snapshots (CIP-002)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.domain.curriculum_intelligence.quality_metrics import PipelineQualityMetrics
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipConfidenceRecord,
    CipCurriculumEntity,
    CipExtractedDocument,
    CipKnowledgeRelation,
    CipQualityMetrics,
    CipReviewRecord,
    CipStructuralNode,
    CipValidationReport,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


class PipelineMetricsService:
    """Compute and persist pipeline quality metrics for Founder dashboards."""

    def record_for_job(
        self,
        *,
        document_id: int,
        pipeline_job_id: str,
        workspace_id: str,
        parse_id: str = "",
        map_id: str = "",
        graph_id: str = "",
    ) -> PipelineQualityMetrics:
        """Snapshot quality metrics after a pipeline run."""
        entities = CipCurriculumEntity.query.filter_by(document_id=document_id).all()
        if map_id:
            entities = [e for e in entities if e.map_id == map_id] or entities
        relations = CipKnowledgeRelation.query.filter_by(document_id=document_id).all()
        if graph_id:
            relations = [r for r in relations if r.graph_id == graph_id] or relations

        extraction = (
            CipExtractedDocument.query.filter_by(document_id=document_id)
            .order_by(CipExtractedDocument.id.desc())
            .first()
        )
        extraction_success = 1.0 if extraction and extraction.page_count > 0 else 0.0

        structural_q = CipStructuralNode.query.filter_by(document_id=document_id)
        if parse_id:
            structural_q = structural_q.filter_by(parse_id=parse_id)
        nodes = structural_q.all()
        if nodes:
            high = sum(1 for n in nodes if float(n.confidence) >= 0.55)
            parser_success = high / len(nodes)
        else:
            parser_success = 0.0

        if entities:
            mean_conf = sum(float(e.confidence) for e in entities) / len(entities)
        else:
            mean_conf = 0.0

        # Completeness: share of entities with at least one outgoing/incoming edge.
        linked: set[str] = set()
        for rel in relations:
            linked.add(rel.from_entity_id)
            linked.add(rel.to_entity_id)
        completeness = (len(linked) / len(entities)) if entities else 0.0

        # Consistency: share of relations whose endpoints exist.
        entity_ids = {e.entity_id for e in entities}
        if relations:
            valid = sum(
                1
                for r in relations
                if r.from_entity_id in entity_ids and r.to_entity_id in entity_ids
            )
            consistency = valid / len(relations)
        else:
            consistency = 1.0 if entities else 0.0

        needing_review = CipConfidenceRecord.query.filter_by(
            document_id=document_id, needs_review=True
        ).count()

        approvals = CipReviewRecord.query.filter_by(
            document_id=document_id, decision="approve"
        ).count()
        corrections = CipReviewRecord.query.filter(
            CipReviewRecord.document_id == document_id,
            CipReviewRecord.decision.in_(("reject", "remap")),
        ).count()

        latest_val = (
            CipValidationReport.query.filter_by(document_id=document_id)
            .order_by(CipValidationReport.id.desc())
            .first()
        )
        val_errors = int(latest_val.error_count) if latest_val else 0

        now = _utc_now()
        metrics = PipelineQualityMetrics(
            metrics_id=f"met-{uuid4().hex[:12]}",
            document_id=document_id,
            pipeline_job_id=pipeline_job_id,
            workspace_id=workspace_id,
            extraction_success_rate=round(extraction_success, 4),
            parser_success_rate=round(parser_success, 4),
            mean_mapping_confidence=round(mean_conf, 4),
            graph_completeness=round(min(1.0, completeness), 4),
            graph_consistency=round(consistency, 4),
            entities_requiring_review=int(needing_review),
            founder_approvals=int(approvals),
            founder_corrections=int(corrections),
            entity_count=len(entities),
            relation_count=len(relations),
            validation_error_count=val_errors,
            created_at_iso=_iso(now),
        )
        self._persist(metrics)
        return metrics

    def latest_for_document(self, document_id: int) -> PipelineQualityMetrics | None:
        row = (
            CipQualityMetrics.query.filter_by(document_id=document_id)
            .order_by(CipQualityMetrics.id.desc())
            .first()
        )
        return None if row is None else self._to_domain(row)

    def latest_for_workspace(self, workspace_id: str) -> list[PipelineQualityMetrics]:
        rows = (
            CipQualityMetrics.query.filter_by(workspace_id=workspace_id)
            .order_by(CipQualityMetrics.id.desc())
            .limit(50)
            .all()
        )
        # Deduplicate by document (latest first).
        seen: set[int] = set()
        out: list[PipelineQualityMetrics] = []
        for row in rows:
            if row.document_id in seen:
                continue
            seen.add(row.document_id)
            out.append(self._to_domain(row))
        return out

    def workspace_summary(self, workspace_id: str) -> dict:
        """Aggregate Founder-facing metrics for the Metrics tab."""
        items = self.latest_for_workspace(workspace_id)
        if not items:
            return {
                "document_count": 0,
                "mean_mapping_confidence": 0.0,
                "entities_requiring_review": 0,
                "founder_approvals": 0,
                "founder_corrections": 0,
                "graph_completeness": 0.0,
                "graph_consistency": 0.0,
                "validation_error_count": 0,
                "documents": [],
            }
        return {
            "document_count": len(items),
            "mean_mapping_confidence": round(
                sum(i.mean_mapping_confidence for i in items) / len(items), 4
            ),
            "entities_requiring_review": sum(
                i.entities_requiring_review for i in items
            ),
            "founder_approvals": sum(i.founder_approvals for i in items),
            "founder_corrections": sum(i.founder_corrections for i in items),
            "graph_completeness": round(
                sum(i.graph_completeness for i in items) / len(items), 4
            ),
            "graph_consistency": round(
                sum(i.graph_consistency for i in items) / len(items), 4
            ),
            "validation_error_count": sum(i.validation_error_count for i in items),
            "documents": [self._public(i) for i in items],
        }

    def _persist(self, metrics: PipelineQualityMetrics) -> None:
        db.session.add(
            CipQualityMetrics(
                metrics_id=metrics.metrics_id,
                document_id=metrics.document_id,
                pipeline_job_id=metrics.pipeline_job_id,
                workspace_id=metrics.workspace_id,
                extraction_success_rate=metrics.extraction_success_rate,
                parser_success_rate=metrics.parser_success_rate,
                mean_mapping_confidence=metrics.mean_mapping_confidence,
                graph_completeness=metrics.graph_completeness,
                graph_consistency=metrics.graph_consistency,
                entities_requiring_review=metrics.entities_requiring_review,
                founder_approvals=metrics.founder_approvals,
                founder_corrections=metrics.founder_corrections,
                entity_count=metrics.entity_count,
                relation_count=metrics.relation_count,
                validation_error_count=metrics.validation_error_count,
            )
        )
        db.session.flush()

    @staticmethod
    def _to_domain(row: CipQualityMetrics) -> PipelineQualityMetrics:
        return PipelineQualityMetrics(
            metrics_id=row.metrics_id,
            document_id=row.document_id,
            pipeline_job_id=row.pipeline_job_id,
            workspace_id=row.workspace_id,
            extraction_success_rate=row.extraction_success_rate,
            parser_success_rate=row.parser_success_rate,
            mean_mapping_confidence=row.mean_mapping_confidence,
            graph_completeness=row.graph_completeness,
            graph_consistency=row.graph_consistency,
            entities_requiring_review=row.entities_requiring_review,
            founder_approvals=row.founder_approvals,
            founder_corrections=row.founder_corrections,
            entity_count=row.entity_count,
            relation_count=row.relation_count,
            validation_error_count=row.validation_error_count,
            created_at_iso=_iso(row.created_at) if row.created_at else "",
        )

    @staticmethod
    def _public(metrics: PipelineQualityMetrics) -> dict:
        return {
            "document_id": metrics.document_id,
            "extraction_success_percent": int(
                round(metrics.extraction_success_rate * 100)
            ),
            "parser_success_percent": int(round(metrics.parser_success_rate * 100)),
            "mean_mapping_confidence": metrics.mean_mapping_confidence,
            "graph_completeness": metrics.graph_completeness,
            "graph_consistency": metrics.graph_consistency,
            "entities_requiring_review": metrics.entities_requiring_review,
            "founder_approvals": metrics.founder_approvals,
            "founder_corrections": metrics.founder_corrections,
            "entity_count": metrics.entity_count,
            "relation_count": metrics.relation_count,
            "validation_error_count": metrics.validation_error_count,
        }
