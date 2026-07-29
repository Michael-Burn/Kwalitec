"""HTTP routes for Curriculum Studio (V2-016C).

Thin Flask layer: founder auth → views → templates / JSON.
Publication / validation authority stay on Management / Studio services.
Document bytes are handled only via DocumentUploadService.
"""

from __future__ import annotations

import logging
from io import BytesIO

from flask import flash, jsonify, redirect, render_template, request, send_file, url_for

from app.application.curriculum_studio.document_upload_exceptions import (
    DocumentNotFoundError,
    DocumentUploadError,
    DocumentValidationError,
    DuplicateDocumentError,
)
from app.founder.dashboard.access import founder_required
from app.presentation.curriculum_studio import studio_bp
from app.presentation.curriculum_studio.forms import (
    AdvanceWorkflowForm,
    ApproveWorkspaceForm,
    AssignVersionForm,
    CreateSubjectForm,
    CreateWorkspaceForm,
    PreviewWorkspaceForm,
    PublishWorkspaceForm,
    ValidateWorkspaceForm,
)
from app.presentation.curriculum_studio.operator_guidance import recover_flash
from app.presentation.curriculum_studio.view_models import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.curriculum_studio.views import (
    actor_id,
    document_upload_service,
    load_dashboard,
    load_workspace,
    service,
)

logger = logging.getLogger(__name__)


def _workspace_redirect(workspace_id: str):
    return redirect(url_for("curriculum_studio.workspace", workspace_id=workspace_id))


def _auto_advance_when_ready(workspace_id: str) -> bool:
    """Advance one stage when readiness gates already pass (FV-001A)."""
    try:
        snap = service().workflow.get_workflow(workspace_id)
        if not snap.can_advance:
            return False
        service().workflow.advance(workspace_id)
        return True
    except Exception as exc:  # noqa: BLE001 — never block the parent action
        logger.info("Auto-advance skipped for %s: %s", workspace_id, exc)
        return False


def _json_error(exc: Exception, *, status: int = 400):
    if isinstance(exc, DocumentUploadError):
        return jsonify({"ok": False, "error": exc.message, "code": exc.code}), status
    return jsonify({"ok": False, "error": str(exc), "code": "error"}), status


@studio_bp.get("/")
@founder_required
def index():
    """Curriculum Studio — workspace execution index (not a subject catalogue)."""
    page = load_dashboard()
    return render_template(
        "curriculum_studio/dashboard.html",
        title="Curriculum Studio",
        page=page,
        create_workspace_form=CreateWorkspaceForm(),
        hub="studio",
    )


@studio_bp.get("/subjects")
@founder_required
def subjects_hub():
    """Subjects catalogue — DX-004B Catalogue First."""
    from app.founder.dashboard.services.founder_subjects_service import (
        FounderSubjectsService,
    )

    subjects = FounderSubjectsService().build_page(
        query=request.args.get("q", ""),
        status=request.args.get("status", "all"),
        sort=request.args.get("sort", "recent_active"),
        create=request.args.get("create", "") in {"1", "true", "yes"},
    )
    return render_template(
        "curriculum_studio/subjects.html",
        title="Subjects",
        subjects=subjects,
        create_subject_form=CreateSubjectForm(),
    )


def _subjects_filter_redirect(*, status: str = "all"):
    """Collapse legacy hub catalogues into Subjects filter presets."""
    return redirect(url_for("curriculum_studio.subjects_hub", status=status))


@studio_bp.get("/review-queue")
@founder_required
def review_hub():
    """Legacy Review Queue hub → Subjects Validation filter."""
    return _subjects_filter_redirect(status="validation")


@studio_bp.get("/publishing")
@founder_required
def publishing_hub():
    """Legacy Publishing hub → Subjects Ready to publish filter."""
    return _subjects_filter_redirect(status="ready_to_publish")


@studio_bp.get("/versions")
@founder_required
def versions_hub():
    """Legacy Versions hub → Subjects catalogue."""
    return redirect(url_for("curriculum_studio.subjects_hub"))


@studio_bp.get("/quality")
@founder_required
def quality_hub():
    """Legacy Quality hub → Subjects Validation filter."""
    return _subjects_filter_redirect(status="validation")


@studio_bp.post("/subjects")
@founder_required
def create_subject():
    form = CreateSubjectForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["subject_create"], "warning")
        return redirect(url_for("curriculum_studio.subjects_hub", create=1))
    try:
        code = form.subject_code.data.strip().upper()
        title = (form.title.data or "").strip()
        service().create_subject(code, title=title)
        workspace_id = f"ws-{code.lower()}"
        try:
            ws = service().create_workspace(
                workspace_id, code, subject_title=title
            )
        except Exception as open_exc:  # noqa: BLE001
            logger.info("Create workspace after subject: %s", open_exc)
            existing = [
                w
                for w in service().list_workspaces()
                if (w.subject_code or "").strip().upper() == code
            ]
            if not existing:
                flash(FLASH_SUCCESS["subject_created"], "success")
                return redirect(url_for("curriculum_studio.subjects_hub"))
            flash(FLASH_SUCCESS["subject_created"], "success")
            return redirect(
                url_for(
                    "curriculum_studio.workspace",
                    workspace_id=existing[0].workspace_id,
                )
            )
        flash(FLASH_SUCCESS["subject_created"], "success")
        return redirect(
            url_for("curriculum_studio.workspace", workspace_id=ws.workspace_id)
        )
    except Exception as exc:
        logger.warning("Create subject failed: %s", exc)
        flash(recover_flash(exc, "subject_create"), "warning")
        return redirect(url_for("curriculum_studio.subjects_hub", create=1))


@studio_bp.post("/workspaces")
@founder_required
def create_workspace():
    form = CreateWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["workspace_open"], "warning")
        return redirect(url_for("curriculum_studio.index"))
    try:
        code = form.subject_code.data.strip().upper()
        workspace_id = f"ws-{code.lower()}"
        ws = service().create_workspace(workspace_id, code)
        flash(FLASH_SUCCESS["workspace_opened"], "success")
        return redirect(
            url_for("curriculum_studio.workspace", workspace_id=ws.workspace_id)
        )
    except Exception as exc:
        logger.warning("Create workspace failed: %s", exc)
        flash(recover_flash(exc, "workspace_open"), "warning")
        return redirect(url_for("curriculum_studio.index"))


@studio_bp.get("/workspaces/<workspace_id>")
@founder_required
def workspace(workspace_id: str):
    try:
        page = load_workspace(workspace_id)
    except LookupError:
        flash(FLASH_WARNING["workspace_missing"], "warning")
        return redirect(url_for("curriculum_studio.index"))
    advance = AdvanceWorkflowForm()
    advance.workspace_id.data = workspace_id
    validate = ValidateWorkspaceForm()
    validate.workspace_id.data = workspace_id
    preview = PreviewWorkspaceForm()
    preview.workspace_id.data = workspace_id
    approve = ApproveWorkspaceForm()
    approve.workspace_id.data = workspace_id
    publish = PublishWorkspaceForm()
    publish.workspace_id.data = workspace_id
    version = AssignVersionForm()
    version.workspace_id.data = workspace_id
    upload_svc = document_upload_service()
    try:
        doc_status = upload_svc.status(workspace_id)
    except Exception:
        logger.warning(
            "Document status unavailable for %s",
            workspace_id,
            exc_info=True,
        )
        from app.application.curriculum_studio.dto.document_metadata import (
            WorkspaceDocumentsStatus,
        )
        doc_status = WorkspaceDocumentsStatus(
            workspace_id=workspace_id,
            documents=(),
            required_kinds=("cmp", "syllabus"),
            ready_kinds=(),
            all_required_uploaded=False,
            cta_state="upload",
        )
    return render_template(
        "curriculum_studio/workspace.html",
        title=page.subject_name,
        page=page,
        advance_form=advance,
        validate_form=validate,
        preview_form=preview,
        approve_form=approve,
        publish_form=publish,
        version_form=version,
        document_slots=upload_svc.upload_slots(),
        document_status=doc_status,
        documents_by_kind={d.kind: d for d in doc_status.documents},
    )


@studio_bp.post("/workspaces/<workspace_id>/advance")
@founder_required
def advance(workspace_id: str):
    form = AdvanceWorkflowForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["advance"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().workflow.advance(workspace_id)
        flash(FLASH_SUCCESS["workflow_advanced"], "success")
    except Exception as exc:
        logger.warning("Advance workflow failed: %s", exc)
        flash(recover_flash(exc, "advance"), "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/validate")
@founder_required
def validate(workspace_id: str):
    form = ValidateWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["validate"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().validation.validate_curriculum(workspace_id)
        flash(FLASH_SUCCESS["validation_ok"], "success")
        _auto_advance_when_ready(workspace_id)
        # Prefer landing on Preview after successful validation.
        try:
            snap = service().preview.build_for_review(workspace_id)
            flash(
                FLASH_SUCCESS["preview_ok"].format(count=snap.node_count),
                "success",
            )
            _auto_advance_when_ready(workspace_id)
        except Exception as preview_exc:
            logger.info(
                "Preview not ready after validation for %s: %s",
                workspace_id,
                preview_exc,
            )
    except Exception as exc:
        logger.warning("Validation failed: %s", exc)
        flash(recover_flash(exc, "validate"), "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/preview")
@founder_required
def preview(workspace_id: str):
    form = PreviewWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["preview"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        snap = service().preview.build_for_review(workspace_id)
        readiness = (snap.readiness or "").strip().lower()
        # PI-002R: never claim Preview Ready when validation has not passed.
        if readiness in {"ready_for_review", "approved"} and snap.validation_passed:
            flash(
                FLASH_SUCCESS["preview_ok"].format(count=snap.node_count),
                "success",
            )
        else:
            flash(
                f"We've loaded {snap.node_count} curriculum topic(s). "
                "Validate the curriculum before preview is ready for review.",
                "warning",
            )
        _auto_advance_when_ready(workspace_id)
    except Exception as exc:
        logger.warning("Preview failed: %s", exc)
        flash(recover_flash(exc, "preview"), "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/approve")
@founder_required
def approve(workspace_id: str):
    form = ApproveWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["approve"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().publication.approve(
            workspace_id,
            actor_id=actor_id(),
            reason=(form.reason.data or "").strip(),
        )
        flash(FLASH_SUCCESS["approved"], "success")
        # FV-001A: structure approved → enable Publish path automatically.
        _auto_advance_when_ready(workspace_id)
        _auto_advance_when_ready(workspace_id)
    except Exception as exc:
        logger.warning("Approve failed: %s", exc)
        flash(recover_flash(exc, "approve"), "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/publish")
@founder_required
def publish(workspace_id: str):
    form = PublishWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["publish"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().publication.publish(
            workspace_id,
            actor_id=actor_id(),
        )
        flash(FLASH_SUCCESS["published"], "success")
        # DX-004C: successful Publish exits to Home → Recent Publications.
        return redirect(url_for("founder_dashboard.index"))
    except Exception as exc:
        logger.warning("Publish failed: %s", exc)
        flash(recover_flash(exc, "publish"), "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/version")
@founder_required
def assign_version(workspace_id: str):
    form = AssignVersionForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["version"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().versions.assign_version(
            workspace_id,
            form.version_label.data.strip(),
        )
        flash(FLASH_SUCCESS["version_assigned"], "success")
    except Exception as exc:
        logger.warning("Assign version failed: %s", exc)
        flash(recover_flash(exc, "version"), "warning")
    return _workspace_redirect(workspace_id)


# ------------------------------------------------------------------ documents


@studio_bp.post("/workspaces/<workspace_id>/documents")
@founder_required
def upload_document(workspace_id: str):
    """Upload a curriculum PDF (multipart). Returns metadata JSON only."""
    kind = (request.form.get("kind") or "").strip()
    file = request.files.get("file")
    if not kind or file is None or not file.filename:
        return _json_error(
            DocumentValidationError(
                "Choose a PDF document to upload.",
                code="missing_file",
            )
        )
    try:
        payload = file.read()
        view = document_upload_service().upload(
            workspace_id,
            kind=kind,
            filename=file.filename,
            data=payload,
            content_type=file.mimetype or "application/pdf",
            actor_id=actor_id(),
        )
        status = document_upload_service().status(workspace_id)
        return jsonify(
            {
                "ok": True,
                "document": view.to_dict(),
                "status": status.to_dict(),
                "message": "Document uploaded successfully.",
            }
        )
    except DuplicateDocumentError as exc:
        return _json_error(exc, status=409)
    except DocumentValidationError as exc:
        return _json_error(exc, status=400)
    except DocumentUploadError as exc:
        return _json_error(exc, status=400)
    except Exception as exc:
        logger.warning("Document upload failed: %s", exc)
        return _json_error(
            DocumentUploadError(
                "We couldn't upload this document. Please try again.",
            ),
            status=500,
        )


@studio_bp.post("/workspaces/<workspace_id>/documents/<int:document_id>/replace")
@founder_required
def replace_document(workspace_id: str, document_id: int):
    file = request.files.get("file")
    if file is None or not file.filename:
        return _json_error(
            DocumentValidationError(
                "Choose a PDF document to replace the current file.",
                code="missing_file",
            )
        )
    try:
        view = document_upload_service().replace(
            workspace_id,
            document_id,
            filename=file.filename,
            data=file.read(),
            content_type=file.mimetype or "application/pdf",
            actor_id=actor_id(),
        )
        status = document_upload_service().status(workspace_id)
        return jsonify(
            {
                "ok": True,
                "document": view.to_dict(),
                "status": status.to_dict(),
                "message": "Document replaced successfully.",
            }
        )
    except DuplicateDocumentError as exc:
        return _json_error(exc, status=409)
    except DocumentNotFoundError as exc:
        return _json_error(exc, status=404)
    except DocumentValidationError as exc:
        return _json_error(exc, status=400)
    except DocumentUploadError as exc:
        return _json_error(exc, status=400)
    except Exception as exc:
        logger.warning("Document replace failed: %s", exc)
        return _json_error(
            DocumentUploadError(
                "We couldn't replace this document. Please try again.",
            ),
            status=500,
        )


@studio_bp.get("/workspaces/<workspace_id>/documents/<int:document_id>/download")
@founder_required
def download_document(workspace_id: str, document_id: int):
    try:
        payload, filename, content_type = document_upload_service().download(
            workspace_id, document_id
        )
        return send_file(
            BytesIO(payload),
            mimetype=content_type,
            as_attachment=True,
            download_name=filename,
        )
    except DocumentNotFoundError as exc:
        flash(exc.message, "warning")
        return _workspace_redirect(workspace_id)
    except Exception as exc:
        logger.warning("Document download failed: %s", exc)
        flash("We couldn't download this document.", "warning")
        return _workspace_redirect(workspace_id)


@studio_bp.delete("/workspaces/<workspace_id>/documents/<int:document_id>")
@founder_required
def remove_document(workspace_id: str, document_id: int):
    try:
        view = document_upload_service().remove(workspace_id, document_id)
        status = document_upload_service().status(workspace_id)
        return jsonify(
            {
                "ok": True,
                "document": view.to_dict(),
                "status": status.to_dict(),
                "message": "Document removed from the active workspace.",
            }
        )
    except DocumentNotFoundError as exc:
        return _json_error(exc, status=404)
    except DocumentUploadError as exc:
        return _json_error(exc, status=400)
    except Exception as exc:
        logger.warning("Document remove failed: %s", exc)
        return _json_error(
            DocumentUploadError(
                "We couldn't remove this document. Please try again.",
            ),
            status=500,
        )


@studio_bp.get("/workspaces/<workspace_id>/documents/status")
@founder_required
def documents_status(workspace_id: str):
    try:
        status = document_upload_service().status(workspace_id)
        return jsonify({"ok": True, "status": status.to_dict()})
    except DocumentUploadError as exc:
        return _json_error(exc, status=404)
    except Exception as exc:
        logger.warning("Document status failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't load document status."),
            status=500,
        )


@studio_bp.get("/workspaces/<workspace_id>/documents/<int:document_id>/pipeline")
@founder_required
def document_pipeline(workspace_id: str, document_id: int):
    """Inspect CIP processing job for a document."""
    from app.application.curriculum_intelligence.exceptions import JobNotFoundError
    from app.application.curriculum_intelligence.processing_job_service import (
        ProcessingJobService,
    )

    try:
        document_upload_service()._require_document(document_id, workspace_id)
        job = ProcessingJobService().get_latest_for_document(document_id)
        if job is None:
            return _json_error(
                DocumentUploadError(
                    "No processing job found for this document.",
                    code="no_job",
                ),
                status=404,
            )
        return jsonify(
            {"ok": True, "job": ProcessingJobService().to_view(job).to_dict()}
        )
    except DocumentNotFoundError as exc:
        return _json_error(exc, status=404)
    except JobNotFoundError as exc:
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=404)
    except Exception as exc:
        logger.warning("Pipeline inspect failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't load processing details."),
            status=500,
        )


@studio_bp.post("/workspaces/<workspace_id>/documents/<int:document_id>/pipeline/retry")
@founder_required
def document_pipeline_retry(workspace_id: str, document_id: int):
    """Retry a failed CIP job for a document."""
    from app.application.curriculum_intelligence.exceptions import (
        CurriculumIntelligenceError,
    )
    from app.application.curriculum_intelligence.pipeline_coordinator import (
        PipelineCoordinator,
    )
    from app.application.curriculum_intelligence.processing_job_service import (
        ProcessingJobService,
    )
    from app.infrastructure.adapters.curriculum_intelligence.pypdf_extractor import (
        PyPdfExtractionAdapter,
    )
    from app.presentation.curriculum_studio.factory import get_document_upload_service

    try:
        document_upload_service()._require_document(document_id, workspace_id)
        jobs = ProcessingJobService()
        job = jobs.get_latest_for_document(document_id)
        if job is None:
            return _json_error(
                DocumentUploadError(
                    "No processing job found for this document.",
                    code="no_job",
                ),
                status=404,
            )
        upload_svc = get_document_upload_service()
        coordinator = PipelineCoordinator(
            storage=upload_svc._storage,
            extractor_port=PyPdfExtractionAdapter(),
            jobs=jobs,
        )
        from_scratch = (request.json or {}).get("from_scratch") is True
        updated = coordinator.retry(job.job_id, from_scratch=from_scratch)
        status = document_upload_service().status(workspace_id)
        return jsonify(
            {
                "ok": True,
                "job": jobs.to_view(updated).to_dict(),
                "status": status.to_dict(),
                "message": "Processing retry started.",
            }
        )
    except DocumentNotFoundError as exc:
        return _json_error(exc, status=404)
    except CurriculumIntelligenceError as exc:
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=400)
    except Exception as exc:
        logger.warning("Pipeline retry failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't retry processing."),
            status=500,
        )


@studio_bp.post(
    "/workspaces/<workspace_id>/documents/<int:document_id>/pipeline/cancel"
)
@founder_required
def document_pipeline_cancel(workspace_id: str, document_id: int):
    """Cancel an in-flight CIP job."""
    from app.application.curriculum_intelligence.exceptions import (
        CurriculumIntelligenceError,
    )
    from app.application.curriculum_intelligence.processing_job_service import (
        ProcessingJobService,
    )

    try:
        document_upload_service()._require_document(document_id, workspace_id)
        jobs = ProcessingJobService()
        job = jobs.get_latest_for_document(document_id)
        if job is None:
            return _json_error(
                DocumentUploadError(
                    "No processing job found for this document.",
                    code="no_job",
                ),
                status=404,
            )
        updated = jobs.request_cancel(job.job_id)
        status = document_upload_service().status(workspace_id)
        return jsonify(
            {
                "ok": True,
                "job": jobs.to_view(updated).to_dict(),
                "status": status.to_dict(),
                "message": "Processing cancelled.",
            }
        )
    except DocumentNotFoundError as exc:
        return _json_error(exc, status=404)
    except CurriculumIntelligenceError as exc:
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=400)
    except Exception as exc:
        logger.warning("Pipeline cancel failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't cancel processing."),
            status=500,
        )


# ---------------------------------------------------------------------------
# CIP-002 — Validation, provenance, review, metrics APIs
# ---------------------------------------------------------------------------


@studio_bp.get("/workspaces/<workspace_id>/intelligence/overview")
@founder_required
def intelligence_overview(workspace_id: str):
    """Founder overview of CIP validation & provenance for a workspace."""
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )
    from app.application.curriculum_intelligence.graph_validation_service import (
        GraphValidationService,
    )
    from app.application.curriculum_intelligence.pipeline_metrics_service import (
        PipelineMetricsService,
    )
    from app.models.curriculum_intelligence import CipCurriculumEntity
    from app.models.curriculum_studio_foundation import StudioFoundationDocument

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    docs = StudioFoundationDocument.query.filter_by(workspace_id=workspace_id).all()
    doc_ids = [d.id for d in docs]
    entity_count = 0
    if doc_ids:
        entity_count = CipCurriculumEntity.query.filter(
            CipCurriculumEntity.document_id.in_(doc_ids)
        ).count()
    queue = FounderReviewService().review_queue(workspace_id=workspace_id)
    metrics = PipelineMetricsService().workspace_summary(workspace_id)
    reports = GraphValidationService().latest_for_workspace(workspace_id)
    return jsonify(
        {
            "ok": True,
            "overview": {
                "document_count": len(docs),
                "entity_count": entity_count,
                "review_queue_count": len(queue),
                "validation_reports": len(reports),
                "validation_errors": sum(r.error_count for r in reports),
                "metrics": metrics,
            },
        }
    )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/validation")
@founder_required
def intelligence_validation(workspace_id: str):
    from app.application.curriculum_intelligence.graph_validation_service import (
        GraphValidationService,
    )
    from app.presentation.curriculum_studio.intelligence_serializers import (
        validation_report_public,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    reports = GraphValidationService().latest_for_workspace(workspace_id)
    return jsonify(
        {
            "ok": True,
            "reports": [validation_report_public(r) for r in reports],
        }
    )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/review-queue")
@founder_required
def intelligence_review_queue(workspace_id: str):
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    items = FounderReviewService().review_queue(workspace_id=workspace_id)
    return jsonify({"ok": True, "items": items})


@studio_bp.post(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/approve"
)
@founder_required
def intelligence_approve_entity(workspace_id: str, entity_id: str):
    from app.application.curriculum_intelligence.exceptions import (
        CurriculumIntelligenceError,
    )
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )
    from app.extensions import db

    try:
        service().get_workspace(workspace_id)
        payload = request.get_json(silent=True) or {}
        record = FounderReviewService().approve(
            entity_id=entity_id,
            actor_id=actor_id(),
            workspace_id=workspace_id,
            reason=str(payload.get("reason") or ""),
        )
        db.session.commit()
        return jsonify(
            {
                "ok": True,
                "review_id": record.review_id,
                "status": record.review_status.value,
                "message": "Entity approved.",
            }
        )
    except CurriculumIntelligenceError as exc:
        db.session.rollback()
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=400)
    except Exception as exc:
        db.session.rollback()
        logger.warning("Approve entity failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't approve this entity."),
            status=500,
        )


@studio_bp.post(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/reject"
)
@founder_required
def intelligence_reject_entity(workspace_id: str, entity_id: str):
    from app.application.curriculum_intelligence.exceptions import (
        CurriculumIntelligenceError,
    )
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )
    from app.extensions import db

    try:
        service().get_workspace(workspace_id)
        payload = request.get_json(silent=True) or {}
        record = FounderReviewService().reject(
            entity_id=entity_id,
            actor_id=actor_id(),
            workspace_id=workspace_id,
            reason=str(payload.get("reason") or ""),
        )
        db.session.commit()
        return jsonify(
            {
                "ok": True,
                "review_id": record.review_id,
                "status": record.review_status.value,
                "message": "Entity rejected.",
            }
        )
    except CurriculumIntelligenceError as exc:
        db.session.rollback()
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=400)
    except Exception as exc:
        db.session.rollback()
        logger.warning("Reject entity failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't reject this entity."),
            status=500,
        )


@studio_bp.post(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/remap"
)
@founder_required
def intelligence_remap_entity(workspace_id: str, entity_id: str):
    from app.application.curriculum_intelligence.exceptions import (
        CurriculumIntelligenceError,
    )
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )
    from app.extensions import db

    try:
        service().get_workspace(workspace_id)
        payload = request.get_json(silent=True) or {}
        record = FounderReviewService().remap(
            entity_id=entity_id,
            actor_id=actor_id(),
            workspace_id=workspace_id,
            remap_target_id=str(payload.get("remap_target_id") or ""),
            reason=str(payload.get("reason") or ""),
            suggested_learning_objective=str(
                payload.get("suggested_learning_objective") or ""
            ),
        )
        db.session.commit()
        return jsonify(
            {
                "ok": True,
                "review_id": record.review_id,
                "status": record.review_status.value,
                "message": "Entity remapped.",
            }
        )
    except CurriculumIntelligenceError as exc:
        db.session.rollback()
        return _json_error(DocumentUploadError(str(exc), code=exc.code), status=400)
    except Exception as exc:
        db.session.rollback()
        logger.warning("Remap entity failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't remap this entity."),
            status=500,
        )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/entities/<entity_id>")
@founder_required
def intelligence_entity_details(workspace_id: str, entity_id: str):
    from app.application.curriculum_intelligence.founder_review_service import (
        FounderReviewService,
    )
    from app.extensions import db
    from app.models.curriculum_studio_foundation import StudioFoundationDocument

    try:
        service().get_workspace(workspace_id)
        details = FounderReviewService().entity_details(entity_id)
        if details is None:
            return _json_error(
                DocumentUploadError("Entity not found.", code="entity_not_found"),
                status=404,
            )
        doc = db.session.get(StudioFoundationDocument, details["document_id"])
        if doc is None or doc.workspace_id != workspace_id:
            return _json_error(
                DocumentUploadError("Entity not found.", code="entity_not_found"),
                status=404,
            )
        return jsonify({"ok": True, "entity": details})
    except Exception as exc:
        logger.warning("Entity details failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't load entity details."),
            status=500,
        )


@studio_bp.get(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/provenance"
)
@founder_required
def intelligence_entity_provenance(workspace_id: str, entity_id: str):
    from app.application.curriculum_intelligence.provenance_service import (
        ProvenanceService,
    )
    from app.domain.curriculum_intelligence.provenance import ProvenanceSubjectKind
    from app.extensions import db
    from app.models.curriculum_intelligence import CipCurriculumEntity
    from app.models.curriculum_studio_foundation import StudioFoundationDocument
    from app.presentation.curriculum_studio.intelligence_serializers import (
        provenance_public,
    )

    try:
        service().get_workspace(workspace_id)
        entity = CipCurriculumEntity.query.filter_by(entity_id=entity_id).first()
        if entity is None:
            return _json_error(
                DocumentUploadError("Entity not found.", code="entity_not_found"),
                status=404,
            )
        doc = db.session.get(StudioFoundationDocument, entity.document_id)
        if doc is None or doc.workspace_id != workspace_id:
            return _json_error(
                DocumentUploadError("Entity not found.", code="entity_not_found"),
                status=404,
            )
        prov = ProvenanceService().get_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        if prov is None:
            return _json_error(
                DocumentUploadError(
                    "No provenance recorded for this entity.",
                    code="provenance_missing",
                ),
                status=404,
            )
        payload = provenance_public(prov)
        payload["chain"] = ProvenanceService().chain_for_entity(entity_id)
        return jsonify({"ok": True, "provenance": payload})
    except Exception as exc:
        logger.warning("Entity provenance failed: %s", exc)
        return _json_error(
            DocumentUploadError("We couldn't load provenance."),
            status=500,
        )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/audit")
@founder_required
def intelligence_audit(workspace_id: str):
    from app.application.curriculum_intelligence.audit_service import AuditService
    from app.presentation.curriculum_studio.intelligence_serializers import (
        audit_event_public,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    limit = 100
    try:
        limit = int(request.args.get("limit") or 100)
    except ValueError:
        limit = 100
    events = AuditService().history_for_workspace(
        workspace_id=workspace_id, limit=limit
    )
    return jsonify(
        {"ok": True, "events": [audit_event_public(e) for e in events]}
    )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/metrics")
@founder_required
def intelligence_metrics(workspace_id: str):
    from app.application.curriculum_intelligence.pipeline_metrics_service import (
        PipelineMetricsService,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    summary = PipelineMetricsService().workspace_summary(workspace_id)
    return jsonify({"ok": True, "metrics": summary})


@studio_bp.get("/workspaces/<workspace_id>/intelligence/knowledge-graph")
@founder_required
def intelligence_knowledge_graph(workspace_id: str):
    """Educational graph projection for the Knowledge Graph tab."""
    from app.models.curriculum_intelligence import (
        CipCurriculumEntity,
        CipKnowledgeRelation,
    )
    from app.models.curriculum_studio_foundation import StudioFoundationDocument

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    docs = StudioFoundationDocument.query.filter_by(workspace_id=workspace_id).all()
    doc_ids = [d.id for d in docs]
    if not doc_ids:
        return jsonify({"ok": True, "nodes": [], "edges": []})
    entities = CipCurriculumEntity.query.filter(
        CipCurriculumEntity.document_id.in_(doc_ids)
    ).all()
    relations = CipKnowledgeRelation.query.filter(
        CipKnowledgeRelation.document_id.in_(doc_ids)
    ).all()
    return jsonify(
        {
            "ok": True,
            "nodes": [
                {
                    "entity_id": e.entity_id,
                    "kind": e.kind,
                    "title": e.title,
                    "confidence": e.confidence,
                    "needs_review": e.needs_review,
                    "document_id": e.document_id,
                    "version_label": e.version_label,
                }
                for e in entities
            ],
            "edges": [
                {
                    "relation_id": r.relation_id,
                    "type": r.relation_type,
                    "from_entity_id": r.from_entity_id,
                    "to_entity_id": r.to_entity_id,
                    "confidence": r.confidence,
                    "needs_review": r.needs_review,
                }
                for r in relations
            ],
        }
    )


@studio_bp.get("/workspaces/<workspace_id>/intelligence/evidence/search")
@founder_required
def intelligence_evidence_search(workspace_id: str):
    """Concept / evidence search via CurriculumRetrievalService."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )
    from app.domain.curriculum_retrieval.profile import RetrievalProfile
    from app.domain.curriculum_retrieval.query import RetrievalQuery
    from app.presentation.curriculum_studio.intelligence_serializers import (
        retrieval_result_public,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    text = (request.args.get("q") or "").strip()
    if not text:
        return _json_error(
            DocumentUploadError("Query text is required.", code="query_required"),
            status=400,
        )
    profile_raw = (request.args.get("profile") or "founder_explorer").strip()
    try:
        profile = RetrievalProfile(profile_raw)
    except ValueError:
        profile = RetrievalProfile.FOUNDER_EXPLORER
    limit = min(50, max(1, request.args.get("limit", 10, type=int) or 10))
    result = CurriculumRetrievalService().retrieve(
        RetrievalQuery(
            text=text,
            workspace_id=workspace_id,
            profile=profile,
            limit=limit,
            include_diagnostics=True,
        )
    )
    from app.extensions import db

    db.session.commit()
    return jsonify({"ok": True, "retrieval": retrieval_result_public(result)})


@studio_bp.get("/workspaces/<workspace_id>/intelligence/evidence/retrieve")
@founder_required
def intelligence_evidence_retrieve(workspace_id: str):
    """Full evidence retrieval with optional filters (Founder / diagnostics)."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )
    from app.domain.curriculum_retrieval.intent import QueryIntent
    from app.domain.curriculum_retrieval.profile import RetrievalProfile
    from app.domain.curriculum_retrieval.query import RetrievalQuery
    from app.presentation.curriculum_studio.intelligence_serializers import (
        retrieval_result_public,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    text = (request.args.get("q") or "").strip()
    if not text:
        return _json_error(
            DocumentUploadError("Query text is required.", code="query_required"),
            status=400,
        )
    profile_raw = (request.args.get("profile") or "founder_explorer").strip()
    try:
        profile = RetrievalProfile(profile_raw)
    except ValueError:
        profile = RetrievalProfile.FOUNDER_EXPLORER
    intent = None
    intent_raw = (request.args.get("intent") or "").strip()
    if intent_raw:
        try:
            intent = QueryIntent(intent_raw)
        except ValueError:
            intent = None
    kinds_raw = (request.args.get("kinds") or "").strip()
    kinds = tuple(k.strip() for k in kinds_raw.split(",") if k.strip())
    limit = min(50, max(1, request.args.get("limit", 10, type=int) or 10))
    document_id = request.args.get("document_id", type=int)
    require_verified = (request.args.get("verified") or "").lower() in {
        "1",
        "true",
        "yes",
    }
    result = CurriculumRetrievalService().retrieve(
        RetrievalQuery(
            text=text,
            workspace_id=workspace_id,
            profile=profile,
            intent=intent,
            document_id=document_id,
            entity_kinds=kinds,
            require_verified=require_verified,
            limit=limit,
            include_diagnostics=True,
        )
    )
    from app.extensions import db

    db.session.commit()
    return jsonify({"ok": True, "retrieval": retrieval_result_public(result)})


@studio_bp.get(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/neighbours"
)
@founder_required
def intelligence_entity_neighbours(workspace_id: str, entity_id: str):
    """Knowledge graph neighbours for an entity."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )
    from app.models.curriculum_intelligence import CipCurriculumEntity
    from app.models.curriculum_studio_foundation import StudioFoundationDocument

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    doc_ids = {
        d.id
        for d in StudioFoundationDocument.query.filter_by(
            workspace_id=workspace_id
        ).all()
    }
    entity = CipCurriculumEntity.query.filter_by(entity_id=entity_id).first()
    if entity is None or entity.document_id not in doc_ids:
        return _json_error(
            DocumentUploadError("Entity not found.", code="entity_missing"),
            status=404,
        )
    hops = min(3, max(1, request.args.get("hops", 1, type=int) or 1))
    neighbours = CurriculumRetrievalService().neighbours(
        entity_id, workspace_id=workspace_id, max_hops=hops
    )
    return jsonify({"ok": True, "entity_id": entity_id, "neighbours": neighbours})


@studio_bp.get(
    "/workspaces/<workspace_id>/intelligence/entities/<entity_id>/related"
)
@founder_required
def intelligence_entity_related(workspace_id: str, entity_id: str):
    """Related concepts for an entity."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )
    from app.models.curriculum_intelligence import CipCurriculumEntity
    from app.models.curriculum_studio_foundation import StudioFoundationDocument

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    doc_ids = {
        d.id
        for d in StudioFoundationDocument.query.filter_by(
            workspace_id=workspace_id
        ).all()
    }
    entity = CipCurriculumEntity.query.filter_by(entity_id=entity_id).first()
    if entity is None or entity.document_id not in doc_ids:
        return _json_error(
            DocumentUploadError("Entity not found.", code="entity_missing"),
            status=404,
        )
    related = CurriculumRetrievalService().related_concepts(
        entity_id, workspace_id=workspace_id
    )
    return jsonify({"ok": True, "entity_id": entity_id, "related": related})


@studio_bp.get("/workspaces/<workspace_id>/intelligence/embeddings/status")
@founder_required
def intelligence_embedding_status(workspace_id: str):
    """Embedding index status for the workspace (no vector payloads)."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    status = CurriculumRetrievalService().embedding_status(workspace_id)
    return jsonify({"ok": True, "status": status})


@studio_bp.get("/workspaces/<workspace_id>/intelligence/retrieval/diagnostics")
@founder_required
def intelligence_retrieval_diagnostics(workspace_id: str):
    """Retrieval diagnostics for Evidence Explorer ranking inspection."""
    from app.application.curriculum_retrieval.curriculum_retrieval_service import (
        CurriculumRetrievalService,
    )
    from app.domain.curriculum_retrieval.profile import RetrievalProfile
    from app.domain.curriculum_retrieval.query import RetrievalQuery
    from app.presentation.curriculum_studio.intelligence_serializers import (
        retrieval_result_public,
    )

    try:
        service().get_workspace(workspace_id)
    except Exception:
        return _json_error(
            DocumentUploadError("Workspace not found.", code="workspace_missing"),
            status=404,
        )
    text = (request.args.get("q") or "").strip()
    if not text:
        return _json_error(
            DocumentUploadError("Query text is required.", code="query_required"),
            status=400,
        )
    profile_raw = (request.args.get("profile") or "founder_explorer").strip()
    try:
        profile = RetrievalProfile(profile_raw)
    except ValueError:
        profile = RetrievalProfile.FOUNDER_EXPLORER
    result = CurriculumRetrievalService().diagnostics_for_query(
        RetrievalQuery(
            text=text,
            workspace_id=workspace_id,
            profile=profile,
            limit=min(20, max(1, request.args.get("limit", 10, type=int) or 10)),
            seed_entity_id=(request.args.get("seed") or "").strip() or None,
        )
    )
    from app.extensions import db

    db.session.commit()
    return jsonify({"ok": True, "retrieval": retrieval_result_public(result)})

