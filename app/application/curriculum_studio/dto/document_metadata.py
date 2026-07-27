"""Founder-facing document metadata DTOs (never expose ref:// or storage keys)."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DocumentMetadataView:
    """Safe metadata projected to the Founder UI / JSON API."""

    document_id: int
    kind: str
    label: str
    filename: str
    content_type: str
    byte_size: int
    version_number: int
    uploaded_by: str
    uploaded_at: str
    processing_stage: str
    processing_label: str
    is_active: bool
    is_duplicate: bool = False
    job_id: str | None = None
    last_error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class WorkspaceDocumentsStatus:
    """Workspace-level document status for the Content Sources UI."""

    workspace_id: str
    documents: tuple[DocumentMetadataView, ...]
    required_kinds: tuple[str, ...]
    ready_kinds: tuple[str, ...]
    all_required_uploaded: bool
    cta_state: str  # upload | replace | uploaded
    pipeline_jobs: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return {
            "workspace_id": self.workspace_id,
            "documents": [d.to_dict() for d in self.documents],
            "required_kinds": list(self.required_kinds),
            "ready_kinds": list(self.ready_kinds),
            "all_required_uploaded": self.all_required_uploaded,
            "cta_state": self.cta_state,
            "pipeline_jobs": list(self.pipeline_jobs),
        }
