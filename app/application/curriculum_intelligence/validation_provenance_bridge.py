"""ValidationProvenanceBridge — CIP-002 post-processing after CIP-001 stages.

Does not alter CIP-001 pipeline stage contracts. Invoked by PipelineCoordinator
after map / graph / ready to materialise provenance, confidence, validation,
metrics, and audit events.
"""

from __future__ import annotations

from app.application.curriculum_intelligence.audit_service import AuditService
from app.application.curriculum_intelligence.confidence_scoring_service import (
    ConfidenceScoringService,
)
from app.application.curriculum_intelligence.graph_validation_service import (
    GraphValidationService,
)
from app.application.curriculum_intelligence.pipeline_metrics_service import (
    PipelineMetricsService,
)
from app.application.curriculum_intelligence.provenance_service import ProvenanceService
from app.domain.curriculum_intelligence.audit import AuditAction
from app.domain.curriculum_intelligence.curriculum_entity import CurriculumMap
from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeGraph
from app.domain.curriculum_intelligence.provenance import ProvenanceSubjectKind
from app.domain.curriculum_intelligence.structural_document import StructuralDocument
from app.models.curriculum_intelligence import CipProcessingJob


class ValidationProvenanceBridge:
    """Orchestrate CIP-002 evidence layer after CIP-001 stage outputs."""

    def __init__(
        self,
        *,
        provenance: ProvenanceService | None = None,
        confidence: ConfidenceScoringService | None = None,
        validation: GraphValidationService | None = None,
        metrics: PipelineMetricsService | None = None,
        audit: AuditService | None = None,
    ) -> None:
        self._provenance = provenance or ProvenanceService()
        self._confidence = confidence or ConfidenceScoringService()
        self._validation = validation or GraphValidationService()
        self._metrics = metrics or PipelineMetricsService()
        self._audit = audit or AuditService()

    def after_parse(
        self,
        job: CipProcessingJob,
        structural: StructuralDocument,
        *,
        version_label: str = "",
    ) -> None:
        """Record parser-stage provenance for structural nodes."""
        self._provenance.replace_document_subjects(
            document_id=job.document_id,
            subject_kinds=(ProvenanceSubjectKind.STRUCTURAL_NODE.value,),
        )

        def walk(node) -> None:
            if node.kind.value != "document":
                self._provenance.record_structural_node(
                    node,
                    document_id=structural.document_id,
                    pipeline_job_id=job.job_id,
                    extraction_id=structural.extraction_id,
                    parse_id=structural.parse_id,
                    version_label=version_label,
                )
            for child in node.children:
                walk(child)

        walk(structural.root)

    def after_map(
        self,
        job: CipProcessingJob,
        curriculum_map: CurriculumMap,
        *,
        extraction_id: str,
        version_label: str = "",
    ) -> None:
        """Materialise entity provenance + confidence after mapping."""
        self._provenance.replace_document_subjects(
            document_id=job.document_id,
            subject_kinds=(ProvenanceSubjectKind.ENTITY.value,),
        )
        for entity in curriculum_map.entities:
            prov = self._provenance.record_entity(
                entity,
                pipeline_job_id=job.job_id,
                extraction_id=extraction_id,
                parse_id=curriculum_map.parse_id,
                map_id=curriculum_map.map_id,
                version_label=version_label or curriculum_map.version_label,
            )
            self._confidence.score_entity(
                entity,
                provenance_id=prov.provenance_id,
                document_id=curriculum_map.document_id,
            )
            self._audit.record(
                action=AuditAction.ENTITY_CREATED,
                actor_id="system",
                subject_kind=ProvenanceSubjectKind.ENTITY.value,
                subject_id=entity.entity_id,
                message=f"Mapped {entity.kind.value}: {entity.title}",
                document_id=job.document_id,
                pipeline_job_id=job.job_id,
                document_version=version_label or curriculum_map.version_label,
                workspace_id=job.workspace_id,
            )

    def after_graph(
        self,
        job: CipProcessingJob,
        graph: KnowledgeGraph,
        curriculum_map: CurriculumMap,
        *,
        extraction_id: str,
        version_label: str = "",
    ) -> None:
        """Relation provenance, confidence, validation, and metrics after graph."""
        self._provenance.replace_document_subjects(
            document_id=job.document_id,
            subject_kinds=(ProvenanceSubjectKind.RELATION.value,),
        )
        # Update entity provenance graph_id via fresh mapping records is already
        # done; relation records carry graph_id.
        for rel in graph.relations:
            prov = self._provenance.record_relation(
                rel,
                pipeline_job_id=job.job_id,
                extraction_id=extraction_id,
                parse_id=curriculum_map.parse_id,
                map_id=curriculum_map.map_id,
                graph_id=graph.graph_id,
                version_label=version_label or curriculum_map.version_label,
            )
            self._confidence.score_relation(
                rel,
                provenance_id=prov.provenance_id,
                document_id=graph.document_id,
            )
            self._audit.record(
                action=AuditAction.RELATION_CREATED,
                actor_id="system",
                subject_kind=ProvenanceSubjectKind.RELATION.value,
                subject_id=rel.relation_id,
                message=f"Created {rel.relation_type.value} edge",
                document_id=job.document_id,
                pipeline_job_id=job.job_id,
                document_version=version_label or curriculum_map.version_label,
                workspace_id=job.workspace_id,
            )

        report = self._validation.validate_document(
            document_id=job.document_id,
            graph=graph,
            pipeline_job_id=job.job_id,
        )
        self._audit.record(
            action=AuditAction.GRAPH_VALIDATED,
            actor_id="system",
            subject_kind="graph",
            subject_id=graph.graph_id,
            message=(
                f"Validation {'passed' if report.passed else 'failed'} "
                f"({report.error_count} errors, {report.warning_count} warnings)"
            ),
            document_id=job.document_id,
            pipeline_job_id=job.job_id,
            document_version=version_label or curriculum_map.version_label,
            workspace_id=job.workspace_id,
        )
        self._audit.record(
            action=AuditAction.GRAPH_REBUILT,
            actor_id="system",
            subject_kind="graph",
            subject_id=graph.graph_id,
            message=f"Knowledge graph rebuilt with {len(graph.relations)} relations",
            document_id=job.document_id,
            pipeline_job_id=job.job_id,
            document_version=version_label or curriculum_map.version_label,
            workspace_id=job.workspace_id,
        )
        metrics = self._metrics.record_for_job(
            document_id=job.document_id,
            pipeline_job_id=job.job_id,
            workspace_id=job.workspace_id,
            parse_id=curriculum_map.parse_id,
            map_id=curriculum_map.map_id,
            graph_id=graph.graph_id,
        )
        self._audit.record(
            action=AuditAction.METRICS_RECORDED,
            actor_id="system",
            subject_kind="metrics",
            subject_id=metrics.metrics_id,
            message="Pipeline quality metrics recorded",
            document_id=job.document_id,
            pipeline_job_id=job.job_id,
            document_version=version_label or curriculum_map.version_label,
            workspace_id=job.workspace_id,
        )

    def after_ready(
        self, job: CipProcessingJob, *, graph_id: str, version_label: str = ""
    ) -> None:
        """Audit pipeline completion (embeddings remain CIP-003)."""
        self._audit.record(
            action=AuditAction.PIPELINE_COMPLETED,
            actor_id="system",
            subject_kind="job",
            subject_id=job.job_id,
            message="Pipeline ready for embeddings extension",
            document_id=job.document_id,
            pipeline_job_id=job.job_id,
            document_version=version_label,
            workspace_id=job.workspace_id,
            attributes={"graph_id": graph_id or ""},
        )
