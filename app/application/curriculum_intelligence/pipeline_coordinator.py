"""PipelineCoordinator — run CIP stages with retry/resume/cancel support."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.curriculum_mapping_service import (
    CurriculumMappingService,
)
from app.application.curriculum_intelligence.document_extraction_service import (
    DocumentExtractionService,
)
from app.application.curriculum_intelligence.document_normalization_service import (
    DocumentNormalizationService,
)
from app.application.curriculum_intelligence.exceptions import (
    CurriculumIntelligenceError,
    PipelineCancelledError,
)
from app.application.curriculum_intelligence.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)
from app.application.curriculum_intelligence.persistence import CipPersistenceService
from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    EmbeddingExtensionPort,
    PdfExtractionPort,
    get_default_embedding_extension_port,
)
from app.application.curriculum_intelligence.processing_job_service import (
    ProcessingJobService,
)
from app.application.curriculum_intelligence.structural_parser_service import (
    StructuralParserService,
)
from app.application.curriculum_intelligence.validation_provenance_bridge import (
    ValidationProvenanceBridge,
)
from app.application.curriculum_studio.ports.document_storage_port import (
    DocumentStoragePort,
)
from app.domain.curriculum_intelligence.pipeline_stage import (
    PIPELINE_ORDER,
    PipelineStage,
    has_reached,
    pipeline_index,
    resolve_pipeline_stage,
)
from app.extensions import db
from app.models.curriculum_intelligence import CipProcessingJob
from app.models.curriculum_studio_foundation import StudioFoundationDocument

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class PipelineCoordinator:
    """Orchestrate CIP stages. Single entry for run / retry / resume."""

    def __init__(
        self,
        *,
        storage: DocumentStoragePort,
        extractor_port: PdfExtractionPort,
        jobs: ProcessingJobService | None = None,
        extraction: DocumentExtractionService | None = None,
        normalizer: DocumentNormalizationService | None = None,
        parser: StructuralParserService | None = None,
        mapper: CurriculumMappingService | None = None,
        graph_builder: KnowledgeGraphBuilder | None = None,
        persistence: CipPersistenceService | None = None,
        embeddings: EmbeddingExtensionPort | None = None,
        validation_bridge: ValidationProvenanceBridge | None = None,
    ) -> None:
        self._storage = storage
        self._jobs = jobs or ProcessingJobService()
        self._extraction = extraction or DocumentExtractionService(extractor_port)
        self._normalizer = normalizer or DocumentNormalizationService()
        self._parser = parser or StructuralParserService()
        self._mapper = mapper or CurriculumMappingService()
        self._graph = graph_builder or KnowledgeGraphBuilder()
        self._persistence = persistence or CipPersistenceService()
        self._embeddings = (
            embeddings if embeddings is not None
            else get_default_embedding_extension_port()
        )
        self._validation_bridge = validation_bridge or ValidationProvenanceBridge()

    def run_job(self, job_id: str) -> CipProcessingJob:
        """Run or continue a job from its current checkpoint to terminal state."""
        job = self._jobs.get_job(job_id)
        if job.cancel_requested:
            self._jobs.mark_failed(
                job,
                stage=job.status,
                error="Cancelled",
            )
            job.status = PipelineStage.CANCELLED.value
            db.session.commit()
            return job

        job.attempt_count = int(job.attempt_count or 0) + (
            0 if job.attempt_count else 1
        )
        if not job.started_at:
            job.started_at = _utc_now()
        db.session.flush()

        try:
            self._execute(job)
            db.session.commit()
        except PipelineCancelledError:
            db.session.rollback()
            job = self._jobs.get_job(job_id)
            job.cancel_requested = True
            job.status = PipelineStage.CANCELLED.value
            job.finished_at = _utc_now()
            self._jobs._sync_document_stage(job.document_id, PipelineStage.CANCELLED)
            db.session.commit()
        except CurriculumIntelligenceError as exc:
            db.session.rollback()
            job = self._jobs.get_job(job_id)
            self._jobs.mark_failed(job, stage=job.status, error=str(exc))
            db.session.commit()
            logger.warning("CIP job %s failed: %s", job_id, exc)
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            job = self._jobs.get_job(job_id)
            self._jobs.mark_failed(job, stage=job.status, error=str(exc))
            db.session.commit()
            logger.exception("CIP job %s crashed", job_id)
        return self._jobs.get_job(job_id)

    def retry(self, job_id: str, *, from_scratch: bool = False) -> CipProcessingJob:
        """Retry a failed/cancelled job then run."""
        self._jobs.prepare_retry(job_id, resume=not from_scratch)
        db.session.commit()
        return self.run_job(job_id)

    def _execute(self, job: CipProcessingJob) -> None:
        current = resolve_pipeline_stage(job.status)
        # If resuming from a successful checkpoint, start at the *next* stage.
        start_idx = pipeline_index(current)
        if current is PipelineStage.QUEUED:
            stages = list(
                PIPELINE_ORDER[PIPELINE_ORDER.index(PipelineStage.VERIFIED) :]
            )
        elif has_reached(current, PipelineStage.READY_FOR_EMBEDDINGS):
            return
        elif start_idx >= 0:
            # Re-run from the stage after checkpoint when status==checkpoint
            next_idx = start_idx + 1
            if next_idx >= len(PIPELINE_ORDER):
                return
            stages = list(PIPELINE_ORDER[next_idx:])
        else:
            stages = list(
                PIPELINE_ORDER[PIPELINE_ORDER.index(PipelineStage.VERIFIED) :]
            )

        context: dict = {}
        for stage in stages:
            self._ensure_not_cancelled(job)
            started = _utc_now()
            if stage is PipelineStage.VERIFIED:
                self._verify(job, context)
            elif stage is PipelineStage.EXTRACTED:
                self._extract(job, context)
            elif stage is PipelineStage.NORMALIZED:
                self._normalize(job, context)
            elif stage is PipelineStage.PARSED:
                self._parse(job, context)
            elif stage is PipelineStage.MAPPED:
                self._map(job, context)
            elif stage is PipelineStage.GRAPH_BUILT:
                self._build_graph(job, context)
            elif stage is PipelineStage.READY_FOR_EMBEDDINGS:
                self._ready(job, context)
            else:
                continue
            duration = int((_utc_now() - started).total_seconds() * 1000)
            self._jobs.mark_stage(
                job,
                stage,
                message=f"Completed {stage.value}",
                diagnostics={"duration_ms": duration},
                duration_ms=duration,
                started_at=started,
            )

    def _ensure_not_cancelled(self, job: CipProcessingJob) -> None:
        db.session.refresh(job)
        if job.cancel_requested:
            raise PipelineCancelledError()

    def _verify(self, job: CipProcessingJob, context: dict) -> None:
        doc = db.session.get(StudioFoundationDocument, job.document_id)
        if doc is None:
            raise CurriculumIntelligenceError(
                "Foundation document missing.",
                code="document_missing",
            )
        if not job.storage_key and not doc.storage_key:
            raise CurriculumIntelligenceError(
                "Document has no storage key.",
                code="no_storage_key",
            )
        key = job.storage_key or doc.storage_key or ""
        try:
            payload = self._storage.get(key)
        except FileNotFoundError as exc:
            raise CurriculumIntelligenceError(
                "Stored PDF could not be read.",
                code="blob_missing",
            ) from exc
        if not payload.startswith(b"%PDF"):
            raise CurriculumIntelligenceError(
                "Stored file is not a valid PDF.",
                code="invalid_pdf",
            )
        if doc.byte_size and abs(len(payload) - int(doc.byte_size)) > 0:
            # Soft check — allow small variance but flag in diagnostics
            context["size_mismatch"] = True
        context["pdf_bytes"] = payload
        context["version_label"] = ""
        if doc.version is not None:
            context["version_label"] = doc.version.version_label

    def _extract(self, job: CipProcessingJob, context: dict) -> None:
        pdf_bytes = context.get("pdf_bytes")
        if pdf_bytes is None:
            self._verify(job, context)
            pdf_bytes = context["pdf_bytes"]
        extraction_id = f"ext-{uuid4().hex[:12]}"
        extracted = self._extraction.extract(
            pdf_bytes,
            extraction_id=extraction_id,
            document_id=job.document_id,
        )
        self._persistence.replace_extraction(extracted, job_id=job.job_id)
        context["extracted"] = extracted

    def _normalize(self, job: CipProcessingJob, context: dict) -> None:
        extracted = context.get("extracted")
        if extracted is None:
            raise CurriculumIntelligenceError(
                "Missing extraction for normalize.",
                code="missing_extraction",
            )
        normalized = self._normalizer.normalize(extracted)
        # Keep same extraction_id; overwrite stored extraction with normalised text.
        self._persistence.replace_extraction(normalized, job_id=job.job_id)
        context["extracted"] = normalized

    def _parse(self, job: CipProcessingJob, context: dict) -> None:
        extracted = context.get("extracted")
        if extracted is None:
            raise CurriculumIntelligenceError(
                "Missing extraction for parse.",
                code="missing_extraction",
            )
        structural = self._parser.parse(extracted)
        self._persistence.replace_structural(structural)
        context["structural"] = structural
        self._validation_bridge.after_parse(
            job,
            structural,
            version_label=context.get("version_label") or "",
        )

    def _map(self, job: CipProcessingJob, context: dict) -> None:
        structural = context.get("structural")
        if structural is None:
            raise CurriculumIntelligenceError(
                "Missing structural parse for mapping.",
                code="missing_parse",
            )
        curriculum_map = self._mapper.map(
            structural,
            subject_code=job.subject_code,
            version_label=context.get("version_label") or "",
        )
        self._persistence.replace_curriculum_map(curriculum_map)
        context["map"] = curriculum_map
        extraction_id = getattr(structural, "extraction_id", "") or ""
        extracted = context.get("extracted")
        if extracted is not None:
            extraction_id = extracted.extraction_id
        self._validation_bridge.after_map(
            job,
            curriculum_map,
            extraction_id=extraction_id,
            version_label=context.get("version_label") or "",
        )

    def _build_graph(self, job: CipProcessingJob, context: dict) -> None:
        curriculum_map = context.get("map")
        if curriculum_map is None:
            raise CurriculumIntelligenceError(
                "Missing curriculum map for graph build.",
                code="missing_map",
            )
        graph = self._graph.build(curriculum_map)
        self._persistence.replace_knowledge_graph(graph)
        context["graph"] = graph
        structural = context.get("structural")
        extracted = context.get("extracted")
        extraction_id = ""
        if extracted is not None:
            extraction_id = extracted.extraction_id
        elif structural is not None:
            extraction_id = structural.extraction_id
        self._validation_bridge.after_graph(
            job,
            graph,
            curriculum_map,
            extraction_id=extraction_id,
            version_label=context.get("version_label") or "",
        )

    def _ready(self, job: CipProcessingJob, context: dict) -> None:
        graph = context.get("graph")
        graph_id = graph.graph_id if graph is not None else ""
        self._validation_bridge.after_ready(
            job,
            graph_id=graph_id,
            version_label=context.get("version_label") or "",
        )
        self._embeddings.on_ready_for_embeddings(
            document_id=job.document_id,
            job_id=job.job_id,
            graph_id=graph_id,
        )
