"""SQLAlchemy adapter for Curriculum Studio DocumentMetadataPort."""

from __future__ import annotations

from app.application.curriculum_studio.ports.document_metadata_port import (
    DocumentRecord,
)
from app.extensions import db
from app.models.curriculum_studio_foundation import StudioFoundationDocument


def _to_record(row: StudioFoundationDocument) -> DocumentRecord:
    return DocumentRecord(
        id=row.id,
        workspace_id=row.workspace_id or "",
        version_id=int(row.version_id or 0),
        kind=row.kind or "",
        reference=row.reference or "",
        title=row.title or "",
        uploaded_by=row.uploaded_by or "",
        uploaded_at=row.uploaded_at,
        original_filename=row.original_filename or "",
        content_type=row.content_type or "",
        byte_size=int(row.byte_size or 0),
        checksum_sha256=row.checksum_sha256 or "",
        storage_key=row.storage_key or "",
        version_number=int(row.version_number or 1),
        is_active=bool(row.is_active),
        processing_stage=row.processing_stage or "",
    )


class SqlAlchemyDocumentMetadataAdapter:
    """Persist StudioFoundationDocument rows for DocumentUploadService."""

    def find_active(self, workspace_id: str, kind: str) -> DocumentRecord | None:
        row = (
            StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, kind=kind, is_active=True
            )
            .order_by(StudioFoundationDocument.version_number.desc())
            .first()
        )
        return _to_record(row) if row is not None else None

    def find_by_checksum(
        self, workspace_id: str, kind: str, checksum: str
    ) -> DocumentRecord | None:
        row = StudioFoundationDocument.query.filter_by(
            workspace_id=workspace_id,
            kind=kind,
            checksum_sha256=checksum,
            is_active=True,
        ).first()
        return _to_record(row) if row is not None else None

    def get(self, document_id: int) -> DocumentRecord | None:
        row = db.session.get(StudioFoundationDocument, document_id)
        return _to_record(row) if row is not None else None

    def list_active(self, workspace_id: str) -> tuple[DocumentRecord, ...]:
        rows = (
            StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, is_active=True
            )
            .order_by(
                StudioFoundationDocument.kind,
                StudioFoundationDocument.id,
            )
            .all()
        )
        return tuple(_to_record(row) for row in rows)

    def create(self, record: DocumentRecord) -> DocumentRecord:
        row = StudioFoundationDocument(
            version_id=record.version_id,
            kind=record.kind,
            reference=record.reference,
            title=record.title,
            uploaded_by=record.uploaded_by,
            uploaded_at=record.uploaded_at,
            workspace_id=record.workspace_id,
            original_filename=record.original_filename,
            content_type=record.content_type,
            byte_size=record.byte_size,
            checksum_sha256=record.checksum_sha256,
            storage_key=record.storage_key,
            version_number=record.version_number,
            is_active=record.is_active,
            processing_stage=record.processing_stage,
        )
        db.session.add(row)
        db.session.flush()
        return _to_record(row)

    def deactivate(self, document_id: int) -> None:
        row = db.session.get(StudioFoundationDocument, document_id)
        if row is None:
            return
        row.is_active = False
        db.session.flush()

    def update_stage(self, document_id: int, stage: str) -> None:
        row = db.session.get(StudioFoundationDocument, document_id)
        if row is None:
            return
        row.processing_stage = stage
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()
