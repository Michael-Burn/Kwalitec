"""DocumentMetadataPort — Curriculum Studio document persistence (Phase 1).

``DocumentUploadService`` never imports SQLAlchemy models directly —
infrastructure composition binds a concrete adapter via the process-local
registry below (mirrors ``student_experience.ports.commitment_port``).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass
class DocumentRecord:
    """Mutable mirror of one ``StudioFoundationDocument`` persistence row.

    Application code never touches the ORM directly — DocumentMetadataPort
    adapters translate to/from this shape.
    """

    workspace_id: str
    version_id: int
    kind: str
    reference: str
    title: str
    id: int | None = None
    uploaded_by: str = ""
    uploaded_at: datetime | None = None
    original_filename: str = ""
    content_type: str = ""
    byte_size: int = 0
    checksum_sha256: str = ""
    storage_key: str = ""
    version_number: int = 1
    is_active: bool = True
    processing_stage: str = ""


@runtime_checkable
class DocumentMetadataPort(Protocol):
    """Structural contract for Curriculum Studio document metadata persistence."""

    def find_active(self, workspace_id: str, kind: str) -> DocumentRecord | None:
        """Most recent active document for ``workspace_id`` + ``kind``."""

    def find_by_checksum(
        self, workspace_id: str, kind: str, checksum: str
    ) -> DocumentRecord | None:
        """Active document matching ``checksum`` for duplicate detection."""

    def get(self, document_id: int) -> DocumentRecord | None:
        """Fetch one document by id, or None."""

    def list_active(self, workspace_id: str) -> tuple[DocumentRecord, ...]:
        """All active documents for ``workspace_id``, ordered by kind then id."""

    def create(self, record: DocumentRecord) -> DocumentRecord:
        """Insert ``record`` and flush; returns the record with ``id`` assigned."""

    def deactivate(self, document_id: int) -> None:
        """Set ``is_active = False`` on a document and flush."""

    def update_stage(self, document_id: int, stage: str) -> None:
        """Update ``processing_stage`` on a document and flush."""

    def commit(self) -> None:
        """Commit the current unit of work."""


# Process-local port (bound by infrastructure composition / tests).
_document_metadata: DocumentMetadataPort | None = None


def bind_document_metadata_port(port: DocumentMetadataPort | None) -> None:
    """Bind the process-local DocumentMetadataPort."""
    global _document_metadata
    _document_metadata = port


def get_document_metadata_port() -> DocumentMetadataPort | None:
    """Return the bound DocumentMetadataPort, or None."""
    return _document_metadata
