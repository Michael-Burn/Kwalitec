"""MappingService — map normalised structures to a package preview."""

from __future__ import annotations

from app.application.curriculum_ingestion.dto.ingestion_snapshot import (
    CurriculumPackagePreview,
)
from app.application.curriculum_ingestion.exceptions import MappingError
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_report import IngestionReport
from app.domain.curriculum_ingestion.normalization_result import NormalizationResult


class MappingService:
    """Map normalised curriculum structures into a package preview.

    Produces handoff-shaped identifiers only. Does not write to
    Curriculum Management. Does not generate sessions, activities, or missions.
    """

    def map_package(
        self,
        job: IngestionJob,
        normalization: NormalizationResult,
        report: IngestionReport | None,
        *,
        package_id: str | None = None,
    ) -> CurriculumPackagePreview:
        """Build an immutable CurriculumPackagePreview."""
        if normalization is None:
            raise MappingError("Normalization result is required for mapping")
        pid = (package_id or f"pkg-{job.job_id}").strip()
        if not pid:
            raise MappingError("package_id must be non-empty")

        refs: list[tuple[str, str, str]] = []
        for doc in job.documents:
            kind = job.kind_for(doc.document_id) or doc.declared_kind
            kind_token = kind.value if kind is not None else "unknown"
            refs.append((doc.document_id, doc.source_ref, kind_token))

        ready = report.passed if report is not None else False
        return CurriculumPackagePreview(
            package_id=pid,
            job_id=job.job_id,
            document_refs=tuple(refs),
            section_ids=tuple(s.section_id for s in normalization.sections),
            topic_ids=tuple(t.topic_id for t in normalization.topics),
            objective_ids=tuple(o.objective_id for o in normalization.objectives),
            prerequisite_edges=normalization.prerequisite_edges,
            metadata=normalization.metadata,
            ready=ready,
        )
