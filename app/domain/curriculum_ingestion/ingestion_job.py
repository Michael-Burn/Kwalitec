"""Ingestion job — lifecycle carrier for a curriculum ingestion run."""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentKind,
)
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult
from app.domain.curriculum_ingestion.ingestion_report import IngestionReport
from app.domain.curriculum_ingestion.ingestion_state import (
    IngestionState,
    IngestionTransitionEvent,
    next_ingestion_state,
)
from app.domain.curriculum_ingestion.normalization_result import NormalizationResult


@dataclass(frozen=True)
class IngestionJob:
    """Single deterministic ingestion run over abstract curriculum documents.

    Does not teach. Does not generate activities, sessions, or missions.
    Does not persist — callers own any storage.
    """

    job_id: str
    documents: tuple[CurriculumDocument, ...]
    state: IngestionState = IngestionState.RECEIVED
    classified_kinds: tuple[tuple[str, DocumentKind], ...] = field(
        default_factory=tuple
    )
    extraction: ExtractionResult | None = None
    normalization: NormalizationResult | None = None
    report: IngestionReport | None = None
    failure_reason: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        job_id: str,
        documents: list[CurriculumDocument] | tuple[CurriculumDocument, ...],
        *,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> IngestionJob:
        """Construct an IngestionJob in RECEIVED state."""
        jid = _require_non_empty(job_id, "job_id")
        docs = tuple(documents)
        if not docs:
            raise ValueError("documents must not be empty")
        seen: set[str] = set()
        for doc in docs:
            if doc.document_id in seen:
                raise ValueError(f"duplicate document_id: {doc.document_id!r}")
            seen.add(doc.document_id)
        return cls(
            job_id=jid,
            documents=docs,
            state=IngestionState.RECEIVED,
            metadata=tuple(metadata or ()),
        )

    @property
    def document_count(self) -> int:
        """Number of source documents."""
        return len(self.documents)

    def document_by_id(self, document_id: str) -> CurriculumDocument | None:
        """Return a document by identity, or None."""
        token = (document_id or "").strip()
        for doc in self.documents:
            if doc.document_id == token:
                return doc
        return None

    def kind_for(self, document_id: str) -> DocumentKind | None:
        """Return classified kind for ``document_id``, if recorded."""
        token = (document_id or "").strip()
        for did, kind in self.classified_kinds:
            if did == token:
                return kind
        return None

    def transition(
        self,
        event: IngestionTransitionEvent | str,
        *,
        reason: str | None = None,
    ) -> IngestionJob:
        """Return a job advanced by a lawful lifecycle event."""
        new_state = next_ingestion_state(self.state, event)
        failure = self.failure_reason
        if new_state is IngestionState.FAILED:
            failure = (reason or "ingestion_failed").strip() or "ingestion_failed"
        elif new_state is IngestionState.RECEIVED:
            failure = None
        return replace(self, state=new_state, failure_reason=failure)

    def with_classification(
        self, classified_kinds: list[tuple[str, DocumentKind]]
        | tuple[tuple[str, DocumentKind], ...]
    ) -> IngestionJob:
        """Attach classification results and advance to CLASSIFIED."""
        kinds = tuple(classified_kinds)
        job = replace(self, classified_kinds=kinds)
        if job.state is IngestionState.RECEIVED:
            job = job.transition(IngestionTransitionEvent.MARK_CLASSIFIED)
        return job

    def with_extraction(self, extraction: ExtractionResult) -> IngestionJob:
        """Attach extraction result and advance to EXTRACTED."""
        job = replace(self, extraction=extraction)
        if job.state is IngestionState.CLASSIFIED:
            job = job.transition(IngestionTransitionEvent.MARK_EXTRACTED)
        return job

    def with_normalization(
        self, normalization: NormalizationResult
    ) -> IngestionJob:
        """Attach normalisation result and advance to NORMALIZED."""
        job = replace(self, normalization=normalization)
        if job.state is IngestionState.EXTRACTED:
            job = job.transition(IngestionTransitionEvent.MARK_NORMALIZED)
        return job

    def with_report(self, report: IngestionReport) -> IngestionJob:
        """Attach validation report and advance to VALIDATED when allowed."""
        job = replace(self, report=report)
        if job.state is IngestionState.NORMALIZED:
            job = job.transition(IngestionTransitionEvent.MARK_VALIDATED)
        return job

    def mark_preview_ready(self) -> IngestionJob:
        """Advance VALIDATED → PREVIEW_READY."""
        return self.transition(IngestionTransitionEvent.MARK_PREVIEW_READY)

    def mark_completed(self) -> IngestionJob:
        """Advance PREVIEW_READY → COMPLETED."""
        return self.transition(IngestionTransitionEvent.MARK_COMPLETED)

    def mark_failed(self, reason: str) -> IngestionJob:
        """Advance to FAILED with a reason."""
        return self.transition(
            IngestionTransitionEvent.MARK_FAILED,
            reason=reason,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
