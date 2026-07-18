"""PreviewService — assemble a read-only ingestion preview snapshot."""

from __future__ import annotations

from app.application.curriculum_ingestion._snapshots import ingestion_snapshot
from app.application.curriculum_ingestion.dto.ingestion_snapshot import (
    CurriculumPackagePreview,
    IngestionSnapshot,
)
from app.application.curriculum_ingestion.exceptions import PreviewError
from app.application.curriculum_ingestion.mapping_service import MappingService
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_state import IngestionState


class PreviewService:
    """Produce immutable previews of normalised ingestion output.

    Never mutates the job. Never generates educational content.
    """

    def __init__(self, mapper: MappingService | None = None) -> None:
        self._mapper = mapper or MappingService()

    def preview(self, job: IngestionJob) -> IngestionSnapshot:
        """Build a preview snapshot from the current job artefacts."""
        if job.normalization is None:
            raise PreviewError(
                f"Job {job.job_id} has no normalisation result to preview"
            )
        if job.state in {
            IngestionState.RECEIVED,
            IngestionState.CLASSIFIED,
            IngestionState.EXTRACTED,
        }:
            raise PreviewError(
                f"Job {job.job_id} is not ready for preview (state={job.state.value})"
            )
        package = self._mapper.map_package(
            job, job.normalization, job.report
        )
        return ingestion_snapshot(job, package=package)

    def package_preview(self, job: IngestionJob) -> CurriculumPackagePreview:
        """Return only the package preview portion."""
        snap = self.preview(job)
        assert snap.package is not None
        return snap.package
