"""CurriculumStudioFoundationService — durable Founder onboarding lifecycle.

Implements:
  Create Subject → Upload CMP → Upload Syllabus → Extract → Parse
  → Validate → Founder Review → Publish Curriculum Version

Uses Curriculum Ingestion for extract/parse/validate. Persists durable
state and append-only audit events. Students consume only published
packages via PublishedCurriculumAuthority.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict
from typing import Any
from uuid import uuid4

from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentEntryPayload,
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.ingestion_engine import (
    CurriculumIngestionEngine,
)
from app.application.curriculum_studio_foundation.dto import (
    AuditEventSnapshot,
    DocumentSnapshot,
    ParsedCurriculumSnapshot,
    ProcessingSnapshot,
    PublishedPackageSnapshot,
    SubjectSnapshot,
    ValidationSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio_foundation.exceptions import (
    IllegalStageTransition,
    PublicationError,
    SubjectAlreadyExists,
    SubjectNotFound,
    ValidationBlocked,
    VersionAlreadyExists,
    VersionNotFound,
)
from app.domain.curriculum_studio_foundation.lifecycle import (
    FoundationPublicationState,
    FoundationStage,
    is_student_consumable,
)
from app.extensions import db
from app.models.curriculum_studio_foundation import (
    PublishedCurriculumPackage,
    StudioFoundationAuditEvent,
    StudioFoundationDocument,
    StudioFoundationSubject,
    StudioFoundationVersion,
    _utc_now,
)

logger = logging.getLogger(__name__)

_VERSION_LABEL_RE = re.compile(r"^\d{4}\.\d+$")
_PDF_MARKERS = ("%PDF", "data:application/pdf", "data:application/")


class CurriculumStudioFoundationService:
    """Durable foundation orchestrator for subject-agnostic curriculum onboarding."""

    SERVICE_ID = "curriculum_studio_foundation"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        ingestion: CurriculumIngestionEngine | None = None,
    ) -> None:
        self._ingestion = ingestion or CurriculumIngestionEngine()

    # ------------------------------------------------------------------ subjects

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        actor_id: str = "",
    ) -> SubjectSnapshot:
        """Create Subject — register a new educational product."""
        code = self._normalize_code(subject_code)
        existing = StudioFoundationSubject.query.filter_by(subject_code=code).first()
        if existing is not None:
            raise SubjectAlreadyExists(f"Subject already exists: {code}")
        subject = StudioFoundationSubject(
            subject_code=code,
            title=(title or code).strip() or code,
            created_by=(actor_id or "").strip(),
        )
        db.session.add(subject)
        db.session.flush()
        self._audit(
            subject_code=code,
            version_id=None,
            stage=FoundationStage.CREATE_SUBJECT,
            event_type="subject_created",
            actor_id=actor_id,
            message=f"Created subject {code}",
            payload={"title": subject.title},
        )
        db.session.commit()
        return self._subject_snapshot(subject)

    def get_subject(self, subject_code: str) -> SubjectSnapshot:
        """Return a subject snapshot."""
        return self._subject_snapshot(self._require_subject(subject_code))

    def list_subjects(self) -> tuple[SubjectSnapshot, ...]:
        """List all foundation subjects ordered by code."""
        rows = StudioFoundationSubject.query.order_by(
            StudioFoundationSubject.subject_code
        ).all()
        return tuple(self._subject_snapshot(s) for s in rows)

    # ------------------------------------------------------------------ versions

    def create_version(
        self,
        subject_code: str,
        version_label: str,
        *,
        actor_id: str = "",
    ) -> VersionSnapshot:
        """Create a draft curriculum version for a subject."""
        subject = self._require_subject(subject_code)
        label = self._normalize_version_label(version_label)
        dup = StudioFoundationVersion.query.filter_by(
            subject_id=subject.id, version_label=label
        ).first()
        if dup is not None:
            raise VersionAlreadyExists(
                f"Version {label} already exists for {subject.subject_code}"
            )
        version = StudioFoundationVersion(
            subject_id=subject.id,
            version_label=label,
            stage=FoundationStage.CREATE_SUBJECT.value,
            publication_state=FoundationPublicationState.DRAFT.value,
        )
        db.session.add(version)
        db.session.flush()
        self._audit(
            subject_code=subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.CREATE_SUBJECT,
            event_type="version_created",
            actor_id=actor_id,
            message=f"Created draft version {label}",
            payload={"version_label": label},
        )
        db.session.commit()
        return self._version_snapshot(version)

    def get_version(self, version_id: int) -> VersionSnapshot:
        """Return a version snapshot."""
        return self._version_snapshot(self._require_version(version_id))

    def list_versions(self, subject_code: str) -> tuple[VersionSnapshot, ...]:
        """List versions for a subject."""
        subject = self._require_subject(subject_code)
        rows = (
            StudioFoundationVersion.query.filter_by(subject_id=subject.id)
            .order_by(StudioFoundationVersion.version_label)
            .all()
        )
        return tuple(self._version_snapshot(v) for v in rows)

    # ------------------------------------------------------------------ upload

    def upload_document(
        self,
        version_id: int,
        *,
        kind: str,
        reference: str,
        title: str = "",
        structure: dict[str, Any] | list[dict[str, Any]] | None = None,
        actor_id: str = "",
    ) -> VersionSnapshot:
        """Upload CMP or syllabus (reference + optional abstract structure)."""
        version = self._require_version(version_id)
        if is_student_consumable(version.publication_state):
            raise IllegalStageTransition("Cannot mutate a published version")
        resolved_kind = self._normalize_kind(kind)
        ref = self._reject_embedded_bytes((reference or "").strip())
        if not ref:
            raise IllegalStageTransition("Document reference is required")
        doc = StudioFoundationDocument(
            version_id=version.id,
            kind=resolved_kind,
            reference=ref,
            title=(title or resolved_kind).strip() or resolved_kind,
            structure_json=(
                json.dumps(structure, default=str, sort_keys=True)
                if structure is not None
                else None
            ),
            uploaded_by=(actor_id or "").strip(),
        )
        db.session.add(doc)
        stage = (
            FoundationStage.UPLOAD_CMP
            if resolved_kind == "cmp"
            else FoundationStage.UPLOAD_SYLLABUS
            if resolved_kind == "syllabus"
            else FoundationStage.UPLOAD_SYLLABUS
        )
        version.stage = stage.value
        version.publication_state = FoundationPublicationState.DRAFT.value
        version.updated_at = _utc_now()
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=stage,
            event_type="document_uploaded",
            actor_id=actor_id,
            message=f"Uploaded {resolved_kind} reference",
            payload={"kind": resolved_kind, "reference": ref},
        )
        db.session.commit()
        return self._version_snapshot(version)

    # ------------------------------------------------------------------ pipeline

    def process_curriculum(
        self,
        version_id: int,
        *,
        actor_id: str = "",
    ) -> ProcessingSnapshot:
        """Run Extract → Parse (normalise) via Curriculum Ingestion."""
        version = self._require_version(version_id)
        if is_student_consumable(version.publication_state):
            raise IllegalStageTransition("Cannot process a published version")
        docs = list(version.documents)
        if not docs:
            raise IllegalStageTransition(
                "Upload CMP and/or syllabus before processing"
            )
        version.publication_state = FoundationPublicationState.PROCESSING.value
        version.stage = FoundationStage.EXTRACT.value
        version.processing_state = "received"
        version.updated_at = _utc_now()
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.EXTRACT,
            event_type="processing_started",
            actor_id=actor_id,
            message="Started extract/parse pipeline",
            payload={"document_count": len(docs)},
        )
        db.session.flush()

        job_id = f"job-{uuid4().hex[:12]}"
        payloads = tuple(self._document_payload_from_row(d) for d in docs)
        request = IngestionRequest(
            job_id=job_id,
            documents=payloads,
            metadata=(
                ("subject_code", version.subject.subject_code),
                ("version_label", version.version_label),
            ),
            require_pass=False,
        )
        snapshot = self._ingestion.ingest(request)
        structure = self._structure_from_ingestion(snapshot)
        report = asdict(snapshot.validation) if snapshot.validation else {}
        version.ingestion_job_id = job_id
        version.parsed_structure_json = json.dumps(
            structure, default=str, sort_keys=True
        )
        version.validation_report_json = json.dumps(
            report, default=str, sort_keys=True
        )
        version.processing_state = snapshot.state
        version.stage = FoundationStage.PARSE.value
        version.publication_state = FoundationPublicationState.PROCESSING.value
        version.updated_at = _utc_now()
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.PARSE,
            event_type="processing_completed",
            actor_id=actor_id,
            message=f"Pipeline reached state={snapshot.state}",
            payload={
                "ingestion_job_id": job_id,
                "state": snapshot.state,
                "section_count": structure.get("section_count", 0),
                "topic_count": structure.get("topic_count", 0),
            },
        )
        db.session.commit()
        return self.get_processing_state(version.id)

    def get_processing_state(self, version_id: int) -> ProcessingSnapshot:
        """Track processing state for a curriculum version."""
        version = self._require_version(version_id)
        structure = self._load_json(version.parsed_structure_json) or {}
        report = self._load_json(version.validation_report_json) or {}
        passed = report.get("passed")
        if passed is None and "blocks_ingestion" in report:
            passed = not bool(report.get("blocks_ingestion"))
        return ProcessingSnapshot(
            version_id=version.id,
            processing_state=version.processing_state,
            ingestion_job_id=version.ingestion_job_id,
            stage=version.stage,
            publication_state=version.publication_state,
            section_count=int(structure.get("section_count") or 0),
            topic_count=int(structure.get("topic_count") or 0),
            objective_count=int(structure.get("objective_count") or 0),
            validation_passed=None if passed is None else bool(passed),
            validation_summary=str(report.get("summary") or ""),
        )

    def review_parsed_curriculum(self, version_id: int) -> ParsedCurriculumSnapshot:
        """Founder review projection of the parsed/normalised curriculum."""
        version = self._require_version(version_id)
        structure = self._load_json(version.parsed_structure_json) or {}
        return ParsedCurriculumSnapshot(
            version_id=version.id,
            subject_code=version.subject.subject_code,
            version_label=version.version_label,
            sections=tuple(structure.get("sections") or ()),
            topics=tuple(structure.get("topics") or ()),
            objectives=tuple(structure.get("objectives") or ()),
            processing_state=version.processing_state,
        )

    def validate_curriculum(
        self,
        version_id: int,
        *,
        actor_id: str = "",
        require_pass: bool = True,
    ) -> ValidationSnapshot:
        """Validate curriculum — gate before founder review."""
        version = self._require_version(version_id)
        if not version.parsed_structure_json:
            raise IllegalStageTransition(
                "Process curriculum (extract/parse) before validation"
            )
        report = self._load_json(version.validation_report_json) or {}
        # Re-run ingestion validation if we have documents, to refresh the report.
        if version.documents:
            payloads = tuple(
                self._document_payload_from_row(d) for d in version.documents
            )
            job_id = version.ingestion_job_id or f"job-{uuid4().hex[:12]}"
            snapshot = self._ingestion.ingest(
                IngestionRequest(
                    job_id=job_id,
                    documents=payloads,
                    metadata=(
                        ("subject_code", version.subject.subject_code),
                        ("version_label", version.version_label),
                    ),
                    require_pass=False,
                )
            )
            report = asdict(snapshot.validation) if snapshot.validation else {}
            structure = self._structure_from_ingestion(snapshot)
            version.parsed_structure_json = json.dumps(
                structure, default=str, sort_keys=True
            )
            version.validation_report_json = json.dumps(
                report, default=str, sort_keys=True
            )
            version.processing_state = snapshot.state
            version.ingestion_job_id = job_id

        passed = bool(report.get("passed"))
        if "blocks_ingestion" in report and "passed" not in report:
            passed = not bool(report.get("blocks_ingestion"))
        issues = tuple(report.get("issues") or ())
        version.stage = FoundationStage.VALIDATE.value
        version.updated_at = _utc_now()
        if passed:
            version.publication_state = (
                FoundationPublicationState.READY_FOR_REVIEW.value
            )
        else:
            version.publication_state = FoundationPublicationState.FAILED.value
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.VALIDATE,
            event_type="validation_completed",
            actor_id=actor_id,
            message=f"Validation {'passed' if passed else 'failed'}",
            payload={"passed": passed, "issue_count": len(issues)},
        )
        db.session.commit()
        result = ValidationSnapshot(
            version_id=version.id,
            passed=passed,
            summary=str(report.get("summary") or ("passed" if passed else "failed")),
            issue_count=len(issues),
            issues=tuple(
                i if isinstance(i, dict) else {"detail": str(i)} for i in issues
            ),
        )
        if require_pass and not passed:
            raise ValidationBlocked(result.summary)
        return result

    def founder_review(
        self,
        version_id: int,
        *,
        actor_id: str = "",
        notes: str = "",
        approve: bool = True,
    ) -> VersionSnapshot:
        """Founder Review — approve or reject a validated curriculum."""
        version = self._require_version(version_id)
        if version.publication_state not in {
            FoundationPublicationState.READY_FOR_REVIEW.value,
            FoundationPublicationState.APPROVED.value,
        }:
            raise IllegalStageTransition(
                "Validate curriculum successfully before founder review"
            )
        version.stage = FoundationStage.FOUNDER_REVIEW.value
        version.review_notes = (notes or "").strip() or None
        version.reviewed_by = (actor_id or "").strip() or None
        version.reviewed_at = _utc_now()
        version.updated_at = _utc_now()
        if approve:
            version.publication_state = FoundationPublicationState.APPROVED.value
            event_type = "founder_approved"
            message = "Founder approved curriculum for publication"
        else:
            version.publication_state = FoundationPublicationState.DRAFT.value
            event_type = "founder_rejected"
            message = "Founder rejected curriculum; returned to draft"
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.FOUNDER_REVIEW,
            event_type=event_type,
            actor_id=actor_id,
            message=message,
            payload={"approve": approve, "notes": notes or ""},
        )
        db.session.commit()
        return self._version_snapshot(version)

    def publish_curriculum(
        self,
        version_id: int,
        *,
        actor_id: str = "",
        activate: bool = True,
    ) -> PublishedPackageSnapshot:
        """Publish Curriculum Version — materialise student-facing SSOT package."""
        version = self._require_version(version_id)
        if version.publication_state != FoundationPublicationState.APPROVED.value:
            raise PublicationError(
                "Publish requires founder approval; "
                f"got {version.publication_state}"
            )
        structure = self._load_json(version.parsed_structure_json)
        if not structure:
            raise PublicationError("Cannot publish without a parsed curriculum")
        package = {
            "subject_code": version.subject.subject_code,
            "version_label": version.version_label,
            "foundation_version_id": version.id,
            "ingestion_job_id": version.ingestion_job_id,
            "structure": structure,
            "documents": [
                {
                    "kind": d.kind,
                    "reference": d.reference,
                    "title": d.title,
                }
                for d in version.documents
            ],
        }
        # EI-002A: surface certification provenance for Student Runtime.
        certification = {}
        if isinstance(structure, dict):
            if structure.get("ei_chain_id"):
                certification["chain_id"] = structure["ei_chain_id"]
            if structure.get("ei_certified_snapshot_id"):
                certification["snapshot_id"] = structure[
                    "ei_certified_snapshot_id"
                ]
            if structure.get("ei_certification_status"):
                certification["status"] = structure["ei_certification_status"]
            if structure.get("curriculum_authority"):
                certification["authority"] = structure["curriculum_authority"]
        if certification:
            package["certification"] = certification
        else:
            # Legacy packages without EI binding remain readable during migration.
            package["certification"] = {
                "authority": "legacy_or_unspecified",
            }
        if activate:
            (
                PublishedCurriculumPackage.query.filter_by(
                    subject_code=version.subject.subject_code,
                    is_active=True,
                ).update({"is_active": False})
            )
        existing = (
            PublishedCurriculumPackage.query.filter_by(
                subject_code=version.subject.subject_code,
                version_label=version.version_label,
            ).one_or_none()
        )
        package_json = json.dumps(package, default=str, sort_keys=True)
        if existing is not None:
            existing.version_id = version.id
            existing.package_json = package_json
            existing.is_active = activate
            existing.published_by = (actor_id or "").strip()
            existing.source_ingestion_job_id = version.ingestion_job_id
            published = existing
        else:
            published = PublishedCurriculumPackage(
                subject_code=version.subject.subject_code,
                version_id=version.id,
                version_label=version.version_label,
                package_json=package_json,
                is_active=activate,
                published_by=(actor_id or "").strip(),
                source_ingestion_job_id=version.ingestion_job_id,
            )
            db.session.add(published)
        version.stage = FoundationStage.PUBLISH.value
        version.publication_state = FoundationPublicationState.PUBLISHED.value
        version.updated_at = _utc_now()
        self._audit(
            subject_code=version.subject.subject_code,
            version_id=version.id,
            stage=FoundationStage.PUBLISH,
            event_type="curriculum_published",
            actor_id=actor_id,
            message=f"Published {version.subject.subject_code} {version.version_label}",
            payload={"activate": activate, "package_keys": sorted(package.keys())},
        )
        db.session.commit()
        return self._published_snapshot(published)

    # -------------------------------------------------------------- audit

    def list_audit_events(
        self,
        *,
        subject_code: str | None = None,
        version_id: int | None = None,
        limit: int = 100,
    ) -> tuple[AuditEventSnapshot, ...]:
        """Return append-only audit events newest-first."""
        q = StudioFoundationAuditEvent.query
        if subject_code:
            q = q.filter_by(subject_code=self._normalize_code(subject_code))
        if version_id is not None:
            q = q.filter_by(version_id=version_id)
        rows = (
            q.order_by(StudioFoundationAuditEvent.created_at.desc())
            .limit(max(1, limit))
            .all()
        )
        return tuple(
            AuditEventSnapshot(
                event_id=r.event_id,
                subject_code=r.subject_code,
                version_id=r.version_id,
                stage=r.stage,
                event_type=r.event_type,
                actor_id=r.actor_id,
                message=r.message,
                created_at=r.created_at.isoformat() if r.created_at else "",
            )
            for r in rows
        )

    # ------------------------------------------------------------------ helpers

    def _require_subject(self, subject_code: str) -> StudioFoundationSubject:
        code = self._normalize_code(subject_code)
        subject = StudioFoundationSubject.query.filter_by(subject_code=code).first()
        if subject is None:
            raise SubjectNotFound(f"Subject not found: {code}")
        return subject

    def _require_version(self, version_id: int) -> StudioFoundationVersion:
        version = StudioFoundationVersion.query.filter_by(id=version_id).one_or_none()
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id}")
        return version

    def _subject_snapshot(self, subject: StudioFoundationSubject) -> SubjectSnapshot:
        return SubjectSnapshot(
            subject_id=subject.id,
            subject_code=subject.subject_code,
            title=subject.title,
            version_count=len(subject.versions),
            created_at=subject.created_at.isoformat() if subject.created_at else "",
        )

    def _version_snapshot(self, version: StudioFoundationVersion) -> VersionSnapshot:
        docs = tuple(
            DocumentSnapshot(
                document_id=d.id,
                kind=d.kind,
                reference=d.reference,
                title=d.title,
                uploaded_at=d.uploaded_at.isoformat() if d.uploaded_at else "",
            )
            for d in version.documents
        )
        kinds = {d.kind for d in docs}
        report = self._load_json(version.validation_report_json) or {}
        passed = report.get("passed")
        if passed is None and "blocks_ingestion" in report:
            passed = not bool(report.get("blocks_ingestion"))
        return VersionSnapshot(
            version_id=version.id,
            subject_code=version.subject.subject_code,
            version_label=version.version_label,
            stage=version.stage,
            publication_state=version.publication_state,
            processing_state=version.processing_state,
            ingestion_job_id=version.ingestion_job_id,
            has_cmp="cmp" in kinds,
            has_syllabus="syllabus" in kinds,
            validation_passed=None if passed is None else bool(passed),
            reviewed_by=version.reviewed_by,
            documents=docs,
            updated_at=version.updated_at.isoformat() if version.updated_at else "",
        )

    def _published_snapshot(
        self, row: PublishedCurriculumPackage
    ) -> PublishedPackageSnapshot:
        return PublishedPackageSnapshot(
            package_id=row.id,
            subject_code=row.subject_code,
            version_id=row.version_id,
            version_label=row.version_label,
            is_active=row.is_active,
            published_by=row.published_by,
            published_at=row.published_at.isoformat() if row.published_at else "",
            package=self._load_json(row.package_json) or {},
        )

    def _audit(
        self,
        *,
        subject_code: str,
        version_id: int | None,
        stage: FoundationStage,
        event_type: str,
        actor_id: str,
        message: str,
        payload: dict[str, Any],
    ) -> StudioFoundationAuditEvent:
        event = StudioFoundationAuditEvent(
            event_id=f"evt-{uuid4().hex[:16]}",
            subject_code=subject_code,
            version_id=version_id,
            stage=stage.value,
            event_type=event_type,
            actor_id=(actor_id or "").strip(),
            message=(message or "")[:512],
            payload_json=json.dumps(payload, default=str, sort_keys=True),
        )
        db.session.add(event)
        return event

    @staticmethod
    def _normalize_code(subject_code: str) -> str:
        code = (subject_code or "").strip().upper()
        if not code:
            raise SubjectNotFound("Subject code is required")
        return code

    @staticmethod
    def _normalize_version_label(version_label: str) -> str:
        label = (version_label or "").strip()
        if not _VERSION_LABEL_RE.match(label):
            raise IllegalStageTransition(
                f"version_label must match YYYY.N (e.g. 2026.1); got {version_label!r}"
            )
        return label

    @staticmethod
    def _normalize_kind(kind: str) -> str:
        from app.domain.curriculum_documents.document_type_registry import (
            default_document_type_registry,
        )

        registry = default_document_type_registry()
        try:
            return registry.require(kind).kind
        except ValueError as exc:
            raise IllegalStageTransition(f"Unsupported document kind: {kind!r}") from exc

    @staticmethod
    def _reject_embedded_bytes(reference: str) -> str:
        lowered = reference.lower()
        for marker in _PDF_MARKERS:
            if marker.lower() in lowered:
                raise IllegalStageTransition(
                    "Embedded PDF / data-URI payloads are not allowed; "
                    "store references only"
                )
        return reference

    @staticmethod
    def _load_json(raw: str | None) -> Any:
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON payload in foundation store")
            return None

    def _document_payload_from_row(
        self, doc: StudioFoundationDocument
    ) -> DocumentPayload:
        structure = self._load_json(doc.structure_json)
        entries: list[DocumentEntryPayload] = []
        if isinstance(structure, dict) and structure.get("entries"):
            for i, e in enumerate(structure["entries"]):
                attributes = tuple(
                    (str(k).strip(), str(v).strip())
                    for k, v in (e.get("attributes") or {}).items()
                    if str(k).strip() and str(v).strip()
                )
                entries.append(
                    DocumentEntryPayload(
                        entry_id=str(e.get("entry_id") or f"e-{i}"),
                        entry_type=str(e.get("entry_type") or "topic"),
                        text=str(e.get("text") or e.get("title") or "entry"),
                        number=e.get("number"),
                        parent_ref=e.get("parent_ref"),
                        attributes=attributes,
                    )
                )
        elif isinstance(structure, list):
            for i, e in enumerate(structure):
                if isinstance(e, dict):
                    attributes = tuple(
                        (str(k).strip(), str(v).strip())
                        for k, v in (e.get("attributes") or {}).items()
                        if str(k).strip() and str(v).strip()
                    )
                    entries.append(
                        DocumentEntryPayload(
                            entry_id=str(e.get("entry_id") or f"e-{i}"),
                            entry_type=str(e.get("entry_type") or "topic"),
                            text=str(e.get("text") or e.get("title") or "entry"),
                            number=e.get("number"),
                            parent_ref=e.get("parent_ref"),
                            attributes=attributes,
                        )
                    )
        if not entries:
            entries = [
                DocumentEntryPayload(
                    entry_id="e-1",
                    entry_type="section",
                    text=doc.title or doc.kind,
                    number="1",
                ),
                DocumentEntryPayload(
                    entry_id="e-2",
                    entry_type="topic",
                    text=f"{doc.kind} topic",
                    number="1.1",
                    parent_ref="e-1",
                ),
                DocumentEntryPayload(
                    entry_id="e-3",
                    entry_type="objective",
                    text=f"Understand {doc.kind}",
                    number="1",
                    parent_ref="e-2",
                ),
            ]
        return DocumentPayload(
            document_id=f"doc-{doc.id}",
            source_ref=doc.reference,
            title=doc.title or doc.kind,
            entries=tuple(entries),
            declared_kind=doc.kind,
            metadata=(("subject_code", doc.version.subject.subject_code),),
        )

    @staticmethod
    def _structure_from_ingestion(snapshot: Any) -> dict[str, Any]:
        norm = snapshot.normalization
        if norm is None:
            return {
                "section_count": 0,
                "topic_count": 0,
                "objective_count": 0,
                "sections": [],
                "topics": [],
                "objectives": [],
            }
        sections = [
            {
                "section_id": s.section_id,
                "code": s.number,
                "title": s.title,
                "number": s.number,
                "order_index": s.order_index + 1,
                "source_ids": list(s.source_ids),
            }
            for s in (norm.sections or ())
        ]
        topics = [
            {
                "topic_id": t.topic_id,
                "code": t.number,
                "title": t.title,
                "section_ref": t.section_id,
                "number": t.number,
                "order_index": t.order_index + 1,
                "prerequisite_ids": list(t.prerequisite_ids),
                "source_ids": list(t.source_ids),
            }
            for t in (norm.topics or ())
        ]
        objectives = [
            {
                "objective_id": o.objective_id,
                "code": o.number,
                "text": o.text,
                "topic_ref": o.topic_id,
                "number": o.number,
                "order_index": o.order_index + 1,
                "estimated_minutes": 20,
                "learning_type": "concept",
                "cognitive_level": "understand",
                "source_ids": list(o.source_ids),
            }
            for o in (norm.objectives or ())
        ]
        return {
            "section_count": len(sections),
            "topic_count": len(topics),
            "objective_count": len(objectives),
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": list(norm.prerequisite_edges or ()),
            "metadata": list(norm.metadata or ()),
            "state": snapshot.state,
        }
