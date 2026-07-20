"""HTTP routes for Curriculum Studio (V2-016C).

Thin Flask layer: founder auth → views → templates.
Publication / validation authority stay on Management / Studio services.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, url_for

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
from app.presentation.curriculum_studio.view_models import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.curriculum_studio.views import (
    actor_id,
    load_dashboard,
    load_workspace,
    service,
)

logger = logging.getLogger(__name__)


def _workspace_redirect(workspace_id: str):
    return redirect(
        url_for("curriculum_studio.workspace", workspace_id=workspace_id)
    )


@studio_bp.get("/")
@founder_required
def index():
    """Curriculum Studio founder dashboard."""
    page = load_dashboard()
    return render_template(
        "curriculum_studio/dashboard.html",
        title="Curriculum Studio",
        page=page,
        create_subject_form=CreateSubjectForm(),
        create_workspace_form=CreateWorkspaceForm(),
    )


@studio_bp.post("/subjects")
@founder_required
def create_subject():
    form = CreateSubjectForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["subject_create"], "warning")
        return redirect(url_for("curriculum_studio.index"))
    try:
        service().create_subject(
            form.subject_code.data.strip(),
            title=(form.title.data or "").strip(),
        )
        flash(FLASH_SUCCESS["subject_created"], "success")
    except Exception as exc:
        logger.warning("Create subject failed: %s", exc)
        flash(FLASH_WARNING["subject_create"], "warning")
    return redirect(url_for("curriculum_studio.index"))


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
        flash(FLASH_WARNING["workspace_open"], "warning")
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
    return render_template(
        "curriculum_studio/workspace.html",
        title=f"Workspace · {page.workspace.subject_code}",
        page=page,
        advance_form=advance,
        validate_form=validate,
        preview_form=preview,
        approve_form=approve,
        publish_form=publish,
        version_form=version,
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
        flash(FLASH_WARNING["advance"], "warning")
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
    except Exception as exc:
        logger.warning("Validation failed: %s", exc)
        flash(FLASH_WARNING["validate"], "warning")
    return _workspace_redirect(workspace_id)


@studio_bp.post("/workspaces/<workspace_id>/preview")
@founder_required
def preview(workspace_id: str):
    form = PreviewWorkspaceForm()
    if not form.validate_on_submit():
        flash(FLASH_WARNING["preview"], "warning")
        return _workspace_redirect(workspace_id)
    try:
        service().preview.preview(workspace_id)
        flash(FLASH_SUCCESS["preview_ok"], "success")
    except Exception as exc:
        logger.warning("Preview failed: %s", exc)
        flash(FLASH_WARNING["preview"], "warning")
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
    except Exception as exc:
        logger.warning("Approve failed: %s", exc)
        flash(FLASH_WARNING["approve"], "warning")
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
    except Exception as exc:
        logger.warning("Publish failed: %s", exc)
        flash(FLASH_WARNING["publish"], "warning")
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
        flash(FLASH_WARNING["version"], "warning")
    return _workspace_redirect(workspace_id)
