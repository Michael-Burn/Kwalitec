"""Founder-only Assessment Pipeline diagnostic HTTP endpoints (AP-001)."""

from __future__ import annotations

from flask import jsonify, request

from app.application.assessment_pipeline.assessment_pipeline_service import (
    AssessmentPipelineService,
)
from app.domain.assessment_pipeline.assessment_event import AssessmentEventType
from app.founder.dashboard.access import founder_required
from app.presentation.assessment_pipeline import assessment_pipeline_diagnostics_bp


def _pipeline() -> AssessmentPipelineService:
    return AssessmentPipelineService()


@assessment_pipeline_diagnostics_bp.get("/events")
@founder_required
def assessment_events():
    """List assessment events for a twin_id query param."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify(
            {
                "ok": True,
                "message": "Provide twin_id to list assessment events.",
                "engine_version": AssessmentPipelineService.ENGINE_VERSION,
            }
        )
    service = _pipeline()
    events = service.list_events(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "events": [service.event_as_dict(e) for e in events],
        }
    )


@assessment_pipeline_diagnostics_bp.get("/results")
@founder_required
def assessment_results():
    """List assessment results for a twin."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400
    service = _pipeline()
    results = service.list_results(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "results": [service.result_as_dict(r) for r in results],
        }
    )


@assessment_pipeline_diagnostics_bp.get("/feedback")
@founder_required
def assessment_feedback():
    """List learning feedback for a twin."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400
    service = _pipeline()
    feedback = service.list_feedback(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "feedback": [service.feedback_as_dict(f) for f in feedback],
        }
    )


@assessment_pipeline_diagnostics_bp.post("/pipeline")
@assessment_pipeline_diagnostics_bp.get("/pipeline")
@founder_required
def assessment_pipeline_run():
    """Ingest an activity (POST) or describe the pipeline (GET)."""
    if request.method == "GET":
        return jsonify(
            {
                "ok": True,
                "engine_version": AssessmentPipelineService.ENGINE_VERSION,
                "pipeline": [
                    "Learner Activity",
                    "Validation",
                    "Assessment Event",
                    "Observation Creation",
                    "StudentReasoningService",
                    "Student Digital Twin Update",
                    "Learning Feedback",
                    "Mission Refresh Trigger",
                ],
                "event_types": [t.value for t in AssessmentEventType],
                "message": (
                    "POST JSON with twin_id + event_type to run the pipeline."
                ),
            }
        )

    payload = request.get_json(silent=True) or {}
    twin_id = str(payload.get("twin_id") or "").strip()
    event_type = str(payload.get("event_type") or "").strip()
    if not twin_id or not event_type:
        return jsonify(
            {"ok": False, "error": "twin_id and event_type are required"}
        ), 400

    try:
        run = _pipeline().ingest(
            twin_id=twin_id,
            event_type=event_type,
            activity_id=str(payload.get("activity_id") or ""),
            curriculum_entity_id=str(payload.get("curriculum_entity_id") or ""),
            curriculum_entity_kind=str(payload.get("curriculum_entity_kind") or ""),
            concept_ids=payload.get("concept_ids") or [],
            mission_id=str(payload.get("mission_id") or ""),
            step_id=str(payload.get("step_id") or ""),
            source=str(payload.get("source") or "founder_diagnostics"),
            score=payload.get("score"),
            correct=payload.get("correct"),
            duration_seconds=payload.get("duration_seconds"),
            metadata=payload.get("metadata") or {},
            persist=True,
            reason=str(payload.get("reason", "true")).lower()
            not in {"0", "false", "no"},
            refresh_mission=str(payload.get("refresh_mission", "false")).lower()
            in {"1", "true", "yes"},
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    service = _pipeline()
    return jsonify(
        {
            "ok": run.ok,
            "validation": {
                "passed": run.validation.passed,
                "summary": run.validation.summary,
                "issues": [
                    {"code": i.code, "message": i.message, "severity": i.severity.value}
                    for i in run.validation.issues
                ],
            },
            "event": service.event_as_dict(run.event),
            "observation_id": (
                run.observation.observation_id if run.observation else None
            ),
            "result": service.result_as_dict(run.result) if run.result else None,
            "feedback": (
                service.feedback_as_dict(run.feedback) if run.feedback else None
            ),
            "twin_id": run.twin.twin_id if run.twin else twin_id,
            "mission_refresh_triggered": run.mission_refresh_triggered,
            "refreshed_mission_id": run.refreshed_mission_id,
        }
    )


@assessment_pipeline_diagnostics_bp.get("/diagnostics")
@founder_required
def assessment_diagnostics():
    """Founder diagnostics summary for assessment pipeline state."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400
    return jsonify(_pipeline().diagnostics_for_twin(twin_id))
