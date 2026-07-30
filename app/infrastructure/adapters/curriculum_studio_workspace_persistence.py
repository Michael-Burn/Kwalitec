"""FV-001A — Durable Curriculum Studio workspace projection persistence.

Serialises CurriculumWorkspace (stage + facts + structure) to
``studio_workspace_projections`` so Founder workflow survives restarts.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from app.domain.curriculum_studio.curriculum_workspace import (
    CurriculumWorkspace,
    WorkspaceStatus,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.studio_workflow import (
    StudioWorkflow,
    WorkflowTransitionRecord,
)
from app.domain.curriculum_studio.workflow_stage import WorkflowStage

logger = logging.getLogger(__name__)


def workspace_to_projection_payload(
    workspace: CurriculumWorkspace,
) -> dict[str, Any]:
    """Flatten a workspace aggregate into ORM column values."""
    wf = workspace.workflow
    facts = workspace.facts
    history = []
    if wf is not None:
        for record in wf.history:
            history.append(
                {
                    "from_stage": record.from_stage.value,
                    "to_stage": record.to_stage.value,
                    "event": record.event.value,
                    "occurred_at": record.occurred_at,
                    "actor_id": record.actor_id,
                    "reason": record.reason,
                }
            )
    structure = {
        "section_ids": list(workspace.section_ids),
        "topic_ids": list(workspace.topic_ids),
        "objective_ids": list(workspace.objective_ids),
        "prerequisite_edges": [list(edge) for edge in workspace.prerequisite_edges],
    }
    metadata = {k: v for k, v in workspace.metadata}
    return {
        "workspace_id": workspace.workspace_id,
        "subject_code": workspace.subject_code,
        "subject_title": workspace.subject_title,
        "version_label": workspace.version_label,
        "version_id": workspace.version_id,
        "status": workspace.status.value,
        "current_stage": (
            wf.current_stage.value if wf is not None else WorkflowStage.SUBJECT.value
        ),
        "highest_stage_reached": (
            wf.highest_stage_reached.value
            if wf is not None
            else WorkflowStage.SUBJECT.value
        ),
        "facts_json": json.dumps(
            {
                "cmp_uploaded": facts.cmp_uploaded,
                "official_syllabus_uploaded": facts.official_syllabus_uploaded,
                "validation_passed": facts.validation_passed,
                "blueprint_assigned": facts.blueprint_assigned,
                "preview_built": facts.preview_built,
                "preview_approved": facts.preview_approved,
                "version_assigned": facts.version_assigned,
                "rollback_snapshot_created": facts.rollback_snapshot_created,
                "intelligence_certified": facts.intelligence_certified,
                "calibration_applied": facts.calibration_applied,
                "legacy_publish_fallback": facts.legacy_publish_fallback,
            },
            separators=(",", ":"),
        ),
        "structure_json": json.dumps(structure, separators=(",", ":")),
        "workflow_history_json": json.dumps(history, separators=(",", ":")),
        "metadata_json": json.dumps(metadata, separators=(",", ":")),
        "active_chain_id": metadata.get("ei_chain_id") or None,
        "certified_snapshot_id": metadata.get("ei_certified_snapshot_id") or None,
        "calibration_profile_id": metadata.get("ei_calibration_profile_id") or None,
        "certification_status": metadata.get("ei_certification_status") or None,
        "review_pack_ref": metadata.get("ei_review_pack_ref") or None,
        "estimated_workload_hours": workspace.estimated_workload_hours,
        "notes": workspace.notes,
    }


def projection_row_to_workspace(row: Any) -> CurriculumWorkspace:
    """Rebuild a CurriculumWorkspace from a projection ORM row."""
    facts_raw = _loads(row.facts_json, {})
    structure = _loads(row.structure_json, {})
    history_raw = _loads(row.workflow_history_json, [])
    metadata_raw = _loads(row.metadata_json, {})
    history = tuple(
        WorkflowTransitionRecord.create(
            item.get("from_stage") or WorkflowStage.SUBJECT.value,
            item.get("to_stage") or WorkflowStage.SUBJECT.value,
            item.get("event") or "advance",
            occurred_at=str(item.get("occurred_at") or ""),
            actor_id=item.get("actor_id"),
            reason=str(item.get("reason") or ""),
        )
        for item in history_raw
        if isinstance(item, dict)
    )
    workflow = StudioWorkflow.create(
        f"wf-{row.workspace_id}",
        row.workspace_id,
        current_stage=row.current_stage or WorkflowStage.SUBJECT.value,
        history=history,
        highest_stage_reached=(
            row.highest_stage_reached
            or row.current_stage
            or WorkflowStage.SUBJECT.value
        ),
    )
    facts = WorkspacePublicationFacts.create(
        cmp_uploaded=bool(facts_raw.get("cmp_uploaded")),
        official_syllabus_uploaded=bool(facts_raw.get("official_syllabus_uploaded")),
        validation_passed=bool(facts_raw.get("validation_passed")),
        blueprint_assigned=bool(facts_raw.get("blueprint_assigned")),
        preview_built=bool(facts_raw.get("preview_built")),
        preview_approved=bool(facts_raw.get("preview_approved")),
        version_assigned=bool(facts_raw.get("version_assigned")),
        rollback_snapshot_created=bool(facts_raw.get("rollback_snapshot_created")),
        intelligence_certified=bool(facts_raw.get("intelligence_certified")),
        calibration_applied=bool(facts_raw.get("calibration_applied")),
        legacy_publish_fallback=bool(facts_raw.get("legacy_publish_fallback")),
    )
    edges = tuple(
        (str(a), str(b))
        for a, b in (structure.get("prerequisite_edges") or ())
        if a is not None and b is not None
    )
    return CurriculumWorkspace.create(
        row.workspace_id,
        row.subject_code or "",
        subject_title=row.subject_title or "",
        version_label=row.version_label or "",
        version_id=row.version_id,
        status=row.status or WorkspaceStatus.ACTIVE.value,
        workflow=workflow,
        facts=facts,
        section_ids=tuple(str(x) for x in (structure.get("section_ids") or ())),
        topic_ids=tuple(str(x) for x in (structure.get("topic_ids") or ())),
        objective_ids=tuple(str(x) for x in (structure.get("objective_ids") or ())),
        prerequisite_edges=edges,
        metadata=tuple((str(k), str(v)) for k, v in metadata_raw.items()),
        estimated_workload_hours=row.estimated_workload_hours,
        notes=row.notes or "",
    )


def persist_workspace(workspace: CurriculumWorkspace) -> None:
    """Upsert durable projection; no-op outside app/DB context."""
    try:
        from flask import has_app_context

        if not has_app_context():
            return
        from app.extensions import db
        from app.models.curriculum_studio_foundation import (
            StudioWorkspaceProjection,
        )

        payload = workspace_to_projection_payload(workspace)
        row = db.session.get(StudioWorkspaceProjection, workspace.workspace_id)
        if row is None:
            row = StudioWorkspaceProjection(workspace_id=workspace.workspace_id)
            db.session.add(row)
        for key, value in payload.items():
            if key == "workspace_id":
                continue
            setattr(row, key, value)
        db.session.commit()
    except Exception:  # noqa: BLE001 — persistence must not break unit paths
        logger.warning(
            "Failed to persist workspace projection %s",
            workspace.workspace_id,
            exc_info=True,
        )
        try:
            from app.extensions import db

            db.session.rollback()
        except Exception:  # noqa: BLE001
            pass


def load_workspace(workspace_id: str) -> CurriculumWorkspace | None:
    """Load a workspace projection from DB, or None."""
    try:
        from flask import has_app_context

        if not has_app_context():
            return None
        from app.extensions import db
        from app.models.curriculum_studio_foundation import (
            StudioWorkspaceProjection,
        )

        row = db.session.get(StudioWorkspaceProjection, workspace_id)
        if row is None:
            return None
        return projection_row_to_workspace(row)
    except Exception:  # noqa: BLE001
        logger.warning(
            "Failed to load workspace projection %s",
            workspace_id,
            exc_info=True,
        )
        return None


def load_all_workspaces() -> tuple[CurriculumWorkspace, ...]:
    """Load every durable workspace projection."""
    try:
        from flask import has_app_context

        if not has_app_context():
            return ()
        from app.models.curriculum_studio_foundation import (
            StudioWorkspaceProjection,
        )

        rows = StudioWorkspaceProjection.query.order_by(
            StudioWorkspaceProjection.created_at.asc()
        ).all()
        return tuple(projection_row_to_workspace(row) for row in rows)
    except Exception:  # noqa: BLE001
        logger.warning("Failed to list workspace projections", exc_info=True)
        return ()


def delete_workspace_projection(workspace_id: str) -> None:
    """Remove durable projection for a workspace id."""
    try:
        from flask import has_app_context

        if not has_app_context():
            return
        from app.extensions import db
        from app.models.curriculum_studio_foundation import (
            StudioWorkspaceProjection,
        )

        row = db.session.get(StudioWorkspaceProjection, workspace_id)
        if row is None:
            return
        db.session.delete(row)
        db.session.commit()
    except Exception:  # noqa: BLE001
        logger.warning(
            "Failed to delete workspace projection %s",
            workspace_id,
            exc_info=True,
        )
        try:
            from app.extensions import db

            db.session.rollback()
        except Exception:  # noqa: BLE001
            pass


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default
