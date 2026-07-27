"""DocumentProcessingPort — async pipeline extension point.

Phase 1 only enqueues work (marks QUEUED). Later phases run OCR, extract,
chunk, embed, and knowledge-graph updates.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessingJobHandle:
    """Opaque handle returned when a document is enqueued for processing."""

    job_id: str
    document_id: int
    stage: str


class DocumentProcessingPort(ABC):
    """Enqueue curriculum documents for background AI / extraction work."""

    @abstractmethod
    def enqueue(
        self,
        *,
        document_id: int,
        kind: str,
        storage_key: str,
        workspace_id: str,
        subject_code: str,
    ) -> ProcessingJobHandle:
        """Queue a document for future processing. Must be idempotent-safe."""
