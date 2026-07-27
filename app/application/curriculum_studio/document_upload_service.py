"""DocumentUploadService — Founder PDF upload orchestration (Phase 1).

Validates PDFs, stores bytes via DocumentStoragePort, persists metadata,
mints opaque internal references, links the Studio workspace checklist,
and enqueues future processing. Controllers must not own this logic.
"""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import UTC, datetime
from typing import BinaryIO
from uuid import uuid4

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.application.curriculum_studio.document_upload_exceptions import (
    DocumentNotFoundError,
    DocumentUploadError,
    DocumentValidationError,
    DuplicateDocumentError,
)
from app.application.curriculum_studio.dto.document_metadata import (
    DocumentMetadataView,
    WorkspaceDocumentsStatus,
)
from app.application.curriculum_studio.exceptions import WorkspaceNotFound
from app.application.curriculum_studio.ports.document_processing_port import (
    DocumentProcessingPort,
)
from app.application.curriculum_studio.ports.document_storage_port import (
    DocumentStoragePort,
)
from app.application.curriculum_studio_foundation.exceptions import (
    SubjectAlreadyExists,
    VersionAlreadyExists,
)
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.domain.curriculum_documents.document_type_registry import (
    DocumentTypeRegistry,
    default_document_type_registry,
)
from app.domain.curriculum_documents.processing_stage import (
    DocumentProcessingStage,
    founder_label,
)
from app.extensions import db
from app.models.curriculum_studio_foundation import (
    StudioFoundationDocument,
    StudioFoundationSubject,
    StudioFoundationVersion,
    _utc_now,
)

logger = logging.getLogger(__name__)

_PDF_MAGIC = b"%PDF"
_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")
_DEFAULT_MAX_BYTES = 25 * 1024 * 1024


class DocumentUploadService:
    """Orchestrate curriculum document upload for Curriculum Studio."""

    def __init__(
        self,
        *,
        studio: CurriculumStudioService,
        storage: DocumentStoragePort,
        processing: DocumentProcessingPort,
        foundation: CurriculumStudioFoundationService | None = None,
        registry: DocumentTypeRegistry | None = None,
        max_bytes: int = _DEFAULT_MAX_BYTES,
    ) -> None:
        self._studio = studio
        self._storage = storage
        self._processing = processing
        self._foundation = foundation or CurriculumStudioFoundationService()
        self._registry = registry or default_document_type_registry()
        self._max_bytes = max(1, int(max_bytes))

    # ------------------------------------------------------------------ public

    def upload(
        self,
        workspace_id: str,
        *,
        kind: str,
        filename: str,
        data: bytes | BinaryIO,
        content_type: str = "application/pdf",
        actor_id: str = "",
        replace_document_id: int | None = None,
    ) -> DocumentMetadataView:
        """Validate, store, persist metadata, link workspace, enqueue processing."""
        type_def = self._registry.require(kind)
        payload = self._read_bytes(data)
        self._validate_pdf(payload, filename=filename, content_type=content_type)

        checksum = hashlib.sha256(payload).hexdigest()
        workspace = self._require_workspace(workspace_id)
        self._ensure_workspace_version(workspace_id)
        workspace = self._require_workspace(workspace_id)
        foundation_version = self._ensure_foundation_version(
            subject_code=workspace.subject_code,
            version_label=workspace.version_label or self._default_version_label(),
            actor_id=actor_id,
        )

        if replace_document_id is None:
            self._reject_duplicate(
                workspace_id=workspace_id,
                kind=type_def.kind,
                checksum=checksum,
            )

        next_version = 1
        if replace_document_id is not None:
            prior = self._require_document(replace_document_id, workspace_id)
            if prior.kind != type_def.kind:
                raise DocumentValidationError(
                    "Replacement must use the same document type.",
                    code="kind_mismatch",
                )
            next_version = int(prior.version_number or 1) + 1
            prior.is_active = False
            db.session.flush()
        else:
            active = self._active_document(workspace_id, type_def.kind)
            if active is not None:
                next_version = int(active.version_number or 1) + 1
                active.is_active = False
                db.session.flush()

        storage_key = self._build_storage_key(
            subject_code=workspace.subject_code,
            kind=type_def.kind,
            version_number=next_version,
            checksum=checksum,
        )
        stored = self._storage.put(
            storage_key=storage_key,
            data=payload,
            content_type="application/pdf",
        )
        opaque_ref = self._mint_reference(
            kind=type_def.kind,
            subject_code=workspace.subject_code,
            version_label=workspace.version_label or foundation_version.version_label,
            version_number=next_version,
        )

        doc = StudioFoundationDocument(
            version_id=foundation_version.id,
            kind=type_def.kind,
            reference=opaque_ref,
            title=type_def.label,
            uploaded_by=(actor_id or "").strip(),
            uploaded_at=_utc_now(),
            workspace_id=workspace_id,
            original_filename=self._safe_filename(filename),
            content_type=stored.content_type,
            byte_size=stored.byte_size,
            checksum_sha256=stored.checksum_sha256,
            storage_key=stored.storage_key,
            version_number=next_version,
            is_active=True,
            processing_stage=DocumentProcessingStage.UPLOADED.value,
        )
        db.session.add(doc)
        db.session.flush()

        doc.processing_stage = DocumentProcessingStage.STORED.value
        db.session.flush()

        self._link_workspace_sources(
            workspace_id,
            kind=type_def.kind,
            reference=opaque_ref,
        )

        handle = self._processing.enqueue(
            document_id=doc.id,
            kind=type_def.kind,
            storage_key=stored.storage_key,
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
        )
        doc.processing_stage = handle.stage or DocumentProcessingStage.QUEUED.value
        db.session.commit()

        logger.info(
            "Document uploaded workspace=%s kind=%s id=%s version=%s job=%s",
            workspace_id,
            type_def.kind,
            doc.id,
            next_version,
            handle.job_id,
        )
        return self._metadata_view(doc, label=type_def.label)

    def replace(
        self,
        workspace_id: str,
        document_id: int,
        *,
        filename: str,
        data: bytes | BinaryIO,
        content_type: str = "application/pdf",
        actor_id: str = "",
    ) -> DocumentMetadataView:
        """Archive the active document and upload a new version."""
        prior = self._require_document(document_id, workspace_id)
        return self.upload(
            workspace_id,
            kind=prior.kind,
            filename=filename,
            data=data,
            content_type=content_type,
            actor_id=actor_id,
            replace_document_id=document_id,
        )

    def remove(self, workspace_id: str, document_id: int) -> DocumentMetadataView:
        """Deactivate an active document (archive). Bytes are retained."""
        doc = self._require_document(document_id, workspace_id)
        if not doc.is_active:
            raise DocumentValidationError(
                "This document is already archived.",
                code="already_archived",
            )
        doc.is_active = False
        db.session.commit()
        self._refresh_workspace_checklist(workspace_id)
        type_def = self._registry.get(doc.kind)
        label = type_def.label if type_def else doc.kind
        return self._metadata_view(doc, label=label)

    def download(
        self, workspace_id: str, document_id: int
    ) -> tuple[bytes, str, str]:
        """Return (bytes, filename, content_type) for download."""
        doc = self._require_document(document_id, workspace_id)
        if not doc.storage_key:
            raise DocumentNotFoundError(
                "This document has no downloadable file.",
                code="no_file",
            )
        try:
            payload = self._storage.get(doc.storage_key)
        except FileNotFoundError as exc:
            raise DocumentNotFoundError(
                "The document file could not be found.",
                code="blob_missing",
            ) from exc
        filename = doc.original_filename or f"{doc.kind}.pdf"
        content_type = doc.content_type or "application/pdf"
        return payload, filename, content_type

    def status(self, workspace_id: str) -> WorkspaceDocumentsStatus:
        """Return Founder-safe status for all active workspace documents."""
        self._require_workspace(workspace_id)
        rows = (
            StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, is_active=True
            )
            .order_by(StudioFoundationDocument.kind, StudioFoundationDocument.id)
            .all()
        )
        views = []
        pipeline_jobs: list[dict] = []
        for row in rows:
            type_def = self._registry.get(row.kind)
            label = type_def.label if type_def else row.kind
            job_view = self._pipeline_job_view(row.id)
            views.append(
                self._metadata_view(
                    row,
                    label=label,
                    job_id=job_view.job_id if job_view else None,
                    last_error=job_view.last_error if job_view else None,
                )
            )
            if job_view is not None:
                pipeline_jobs.append(job_view.to_dict())

        required = tuple(d.kind for d in self._registry.publish_required())
        ready = tuple(sorted({v.kind for v in views if v.kind in required}))
        all_ready = all(k in ready for k in required)
        if all_ready:
            cta = "uploaded"
        elif views:
            cta = "replace"
        else:
            cta = "upload"

        return WorkspaceDocumentsStatus(
            workspace_id=workspace_id,
            documents=tuple(views),
            required_kinds=required,
            ready_kinds=ready,
            all_required_uploaded=all_ready,
            cta_state=cta,
            pipeline_jobs=tuple(pipeline_jobs),
        )

    def upload_slots(self) -> tuple[dict, ...]:
        """Phase 1 Founder upload cards (registry-driven; publish-required)."""
        return tuple(
            {
                "kind": d.kind,
                "label": d.label,
                "description": d.description,
                "required_for_publish": d.required_for_publish,
                "accept": d.accept,
            }
            for d in self._registry.publish_required()
        )

    # ------------------------------------------------------------------ helpers
    def _link_workspace_sources(
        self, workspace_id: str, *, kind: str, reference: str
    ) -> None:
        kwargs: dict[str, str] = {}
        if kind == "cmp":
            kwargs["cmp_reference"] = reference
        elif kind == "syllabus":
            kwargs["syllabus_reference"] = reference
        else:
            # Non-checklist kinds still store metadata; checklist unchanged.
            return
        try:
            self._studio.workspaces.upload_sources(
                workspace_id,
                start_ingestion=True,
                **kwargs,
            )
        except Exception as exc:
            logger.warning(
                "Workspace source link failed workspace=%s kind=%s: %s",
                workspace_id,
                kind,
                exc,
            )
            raise DocumentUploadError(
                "We saved the document but could not update the workspace. "
                "Please try again.",
                code="workspace_link_failed",
            ) from exc

    def _refresh_workspace_checklist(self, workspace_id: str) -> None:
        """Recompute CMP/syllabus checklist facts from active documents."""
        from app.domain.curriculum_studio.curriculum_workspace import (
            CurriculumWorkspace,
        )
        from app.domain.curriculum_studio.publication_checklist import (
            WorkspacePublicationFacts,
        )

        entity = self._studio.registry.get_workspace(workspace_id)
        if entity is None:
            return
        active = {
            d.kind
            for d in StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, is_active=True
            ).all()
        }
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded="cmp" in active,
            official_syllabus_uploaded="syllabus" in active,
            validation_passed=entity.facts.validation_passed,
            blueprint_assigned=entity.facts.blueprint_assigned,
            preview_approved=entity.facts.preview_approved,
            version_assigned=entity.facts.version_assigned,
            rollback_snapshot_created=entity.facts.rollback_snapshot_created,
        )
        updated = CurriculumWorkspace.create(
            entity.workspace_id,
            entity.subject_code,
            subject_title=entity.subject_title,
            version_label=entity.version_label,
            version_id=entity.version_id,
            status=entity.status,
            workflow=entity.workflow,
            facts=facts,
            section_ids=entity.section_ids,
            topic_ids=entity.topic_ids,
            objective_ids=entity.objective_ids,
            prerequisite_edges=entity.prerequisite_edges,
            metadata=entity.metadata,
            estimated_workload_hours=entity.estimated_workload_hours,
            notes=entity.notes,
        )
        self._studio.registry.put_workspace(updated)

    def _ensure_workspace_version(self, workspace_id: str) -> str:
        from app.application.curriculum_studio.exceptions import (
            SubjectAlreadyExists,
            SubjectNotFound,
        )

        workspace = self._require_workspace(workspace_id)
        if workspace.version_id:
            return workspace.version_id
        label = workspace.version_label or self._default_version_label()
        try:
            self._studio.subjects.get_subject(workspace.subject_code)
        except SubjectNotFound:
            try:
                self._studio.create_subject(
                    workspace.subject_code,
                    title=workspace.subject_title or workspace.subject_code,
                )
            except SubjectAlreadyExists:
                pass
        except Exception:
            pass
        try:
            record = self._studio.versions.assign_version(workspace_id, label)
            return record.version_id
        except Exception as exc:
            raise DocumentUploadError(
                "We couldn't prepare a curriculum version for this upload. "
                "Create the subject, then try uploading again.",
                code="version_required",
            ) from exc

    def _ensure_foundation_version(
        self,
        *,
        subject_code: str,
        version_label: str,
        actor_id: str,
    ) -> StudioFoundationVersion:
        code = subject_code.strip().upper()
        label = self._foundation_version_label(version_label)
        subject = StudioFoundationSubject.query.filter_by(subject_code=code).first()
        if subject is None:
            try:
                self._foundation.create_subject(
                    code, title=code, actor_id=actor_id
                )
            except SubjectAlreadyExists:
                pass
            subject = StudioFoundationSubject.query.filter_by(subject_code=code).first()
        if subject is None:
            raise DocumentUploadError(
                "We couldn't prepare this subject for document storage.",
                code="subject_missing",
            )
        version = StudioFoundationVersion.query.filter_by(
            subject_id=subject.id, version_label=label
        ).first()
        if version is None:
            try:
                snap = self._foundation.create_version(
                    code, label, actor_id=actor_id
                )
                version = db.session.get(StudioFoundationVersion, snap.version_id)
            except VersionAlreadyExists:
                version = StudioFoundationVersion.query.filter_by(
                    subject_id=subject.id, version_label=label
                ).first()
        if version is None:
            raise DocumentUploadError(
                "We couldn't prepare a curriculum version for this upload.",
                code="version_missing",
            )
        return version

    def _reject_duplicate(
        self, *, workspace_id: str, kind: str, checksum: str
    ) -> None:
        existing = (
            StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id,
                kind=kind,
                checksum_sha256=checksum,
                is_active=True,
            ).first()
        )
        if existing is not None:
            raise DuplicateDocumentError(
                "This file is already uploaded for this document type. "
                "Choose Replace Document if you intend to upload a new version.",
            )

    def _active_document(
        self, workspace_id: str, kind: str
    ) -> StudioFoundationDocument | None:
        return (
            StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, kind=kind, is_active=True
            )
            .order_by(StudioFoundationDocument.version_number.desc())
            .first()
        )

    def _require_document(
        self, document_id: int, workspace_id: str
    ) -> StudioFoundationDocument:
        doc = db.session.get(StudioFoundationDocument, document_id)
        if doc is None or doc.workspace_id != workspace_id:
            raise DocumentNotFoundError("Document not found.")
        return doc

    def _require_workspace(self, workspace_id: str):
        try:
            return self._studio.get_workspace(workspace_id)
        except WorkspaceNotFound as exc:
            raise DocumentUploadError(
                "Workspace not found.",
                code="workspace_missing",
            ) from exc

    def _validate_pdf(
        self, payload: bytes, *, filename: str, content_type: str
    ) -> None:
        if not payload:
            raise DocumentValidationError(
                "The selected file is empty. Choose a valid PDF, then try again.",
                code="empty_file",
            )
        if len(payload) > self._max_bytes:
            mb = self._max_bytes // (1024 * 1024)
            raise DocumentValidationError(
                f"This file is too large. Maximum size is {mb} MB.",
                code="too_large",
            )
        name = (filename or "").lower()
        ctype = (content_type or "").lower()
        if name and not name.endswith(".pdf"):
            raise DocumentValidationError(
                "Only PDF documents are accepted.",
                code="not_pdf",
            )
        if ctype and "pdf" not in ctype and ctype not in {
            "application/octet-stream",
            "",
        }:
            raise DocumentValidationError(
                "Only PDF documents are accepted.",
                code="not_pdf",
            )
        if not payload.startswith(_PDF_MAGIC):
            raise DocumentValidationError(
                "This file does not look like a valid PDF. "
                "Choose the official PDF, then try again.",
                code="corrupt_pdf",
            )
        # Lightweight corruption check: PDFs normally contain an EOF marker.
        if b"%%EOF" not in payload[-2048:]:
            raise DocumentValidationError(
                "This PDF appears incomplete or corrupted. "
                "Re-export the official file, then try again.",
                code="corrupt_pdf",
            )

    @staticmethod
    def _read_bytes(data: bytes | BinaryIO) -> bytes:
        if isinstance(data, bytes | bytearray | memoryview):
            return bytes(data)
        return data.read()

    @staticmethod
    def _safe_filename(filename: str) -> str:
        raw = (filename or "document.pdf").strip() or "document.pdf"
        base = raw.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        cleaned = _SAFE_FILENAME_RE.sub("_", base).strip("._") or "document.pdf"
        if not cleaned.lower().endswith(".pdf"):
            cleaned = f"{cleaned}.pdf"
        return cleaned[:500]

    @staticmethod
    def _build_storage_key(
        *,
        subject_code: str,
        kind: str,
        version_number: int,
        checksum: str,
    ) -> str:
        code = subject_code.strip().lower()
        stamp = uuid4().hex[:8]
        return (
            f"{code}/{kind}/v{version_number}/"
            f"{checksum[:16]}-{stamp}.pdf"
        )

    @staticmethod
    def _mint_reference(
        *,
        kind: str,
        subject_code: str,
        version_label: str,
        version_number: int,
    ) -> str:
        code = subject_code.strip().lower().replace(" ", "-")
        label = (version_label or "draft").strip().lower().replace(" ", "-")
        return f"ref://{kind}/{code}-{label}-v{version_number}"

    @staticmethod
    def _default_version_label() -> str:
        return f"{datetime.now(UTC).year}.1"

    @staticmethod
    def _foundation_version_label(version_label: str) -> str:
        label = (version_label or "").strip()
        if re.match(r"^\d{4}\.\d+$", label):
            return label
        return DocumentUploadService._default_version_label()

    @staticmethod
    def _pipeline_job_view(document_id: int):
        """Best-effort CIP job projection (None when CIP tables unused)."""
        try:
            from app.application.curriculum_intelligence.processing_job_service import (
                ProcessingJobService,
            )

            job = ProcessingJobService().get_latest_for_document(document_id)
            if job is None:
                return None
            return ProcessingJobService().to_view(job)
        except Exception:  # noqa: BLE001 — status must not fail on CIP absence
            return None

    @staticmethod
    def _metadata_view(
        doc: StudioFoundationDocument,
        *,
        label: str,
        job_id: str | None = None,
        last_error: str | None = None,
    ) -> DocumentMetadataView:
        stage = doc.processing_stage or DocumentProcessingStage.UPLOADED.value
        return DocumentMetadataView(
            document_id=doc.id,
            kind=doc.kind,
            label=label,
            filename=doc.original_filename or "",
            content_type=doc.content_type or "application/pdf",
            byte_size=int(doc.byte_size or 0),
            version_number=int(doc.version_number or 1),
            uploaded_by=doc.uploaded_by or "",
            uploaded_at=doc.uploaded_at.isoformat() if doc.uploaded_at else "",
            processing_stage=stage,
            processing_label=founder_label(stage),
            is_active=bool(doc.is_active),
            job_id=job_id,
            last_error=last_error,
        )
