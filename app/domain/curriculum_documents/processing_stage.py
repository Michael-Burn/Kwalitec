"""Document processing pipeline stages (CS-DOC-001 + CIP-001).

CS-DOC-001 ends at QUEUED after a successful store.
CIP-001 advances documents through verify → extract → … → ready_for_embeddings.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.curriculum_intelligence.pipeline_stage import (
    FOUNDER_STAGE_LABELS as CIP_FOUNDER_LABELS,
)
from app.domain.curriculum_intelligence.pipeline_stage import (
    PipelineStage,
)
from app.domain.curriculum_intelligence.pipeline_stage import (
    founder_label as cip_founder_label,
)


class DocumentProcessingStage(StrEnum):
    """Authoritative processing stages for curriculum documents.

    Values align with CIP ``PipelineStage`` so Founder UI and workers share
    one vocabulary. Legacy aliases ``processing`` / ``ready`` remain readable
    via ``founder_label``.
    """

    UPLOADED = PipelineStage.UPLOADED.value
    STORED = PipelineStage.STORED.value
    QUEUED = PipelineStage.QUEUED.value
    VERIFIED = PipelineStage.VERIFIED.value
    EXTRACTED = PipelineStage.EXTRACTED.value
    NORMALIZED = PipelineStage.NORMALIZED.value
    PARSED = PipelineStage.PARSED.value
    MAPPED = PipelineStage.MAPPED.value
    GRAPH_BUILT = PipelineStage.GRAPH_BUILT.value
    READY_FOR_EMBEDDINGS = PipelineStage.READY_FOR_EMBEDDINGS.value
    FAILED = PipelineStage.FAILED.value
    CANCELLED = PipelineStage.CANCELLED.value
    # Legacy CS-DOC-001 tokens (still accepted in reads).
    PROCESSING = "processing"
    READY = "ready"


FOUNDER_STAGE_LABELS: dict[DocumentProcessingStage, str] = {
    DocumentProcessingStage.UPLOADED: "Uploaded",
    DocumentProcessingStage.STORED: "Stored",
    DocumentProcessingStage.QUEUED: "Processing",
    DocumentProcessingStage.VERIFIED: "Verified",
    DocumentProcessingStage.EXTRACTED: "Extracted",
    DocumentProcessingStage.NORMALIZED: "Normalized",
    DocumentProcessingStage.PARSED: "Parsed",
    DocumentProcessingStage.MAPPED: "Mapped",
    DocumentProcessingStage.GRAPH_BUILT: "Knowledge Graph Built",
    DocumentProcessingStage.READY_FOR_EMBEDDINGS: "Ready",
    DocumentProcessingStage.FAILED: "Failed",
    DocumentProcessingStage.CANCELLED: "Cancelled",
    DocumentProcessingStage.PROCESSING: "Processing",
    DocumentProcessingStage.READY: "Ready",
}


def founder_label(stage: DocumentProcessingStage | str) -> str:
    """Return Founder-facing label for a processing stage."""
    raw = str(stage).strip().lower()
    try:
        resolved = DocumentProcessingStage(raw)
        return FOUNDER_STAGE_LABELS.get(resolved, resolved.value.title())
    except ValueError:
        return cip_founder_label(raw)


# Re-export CIP labels for callers that want the pipeline milestone set.
__all__ = [
    "CIP_FOUNDER_LABELS",
    "DocumentProcessingStage",
    "FOUNDER_STAGE_LABELS",
    "founder_label",
]
