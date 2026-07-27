"""Founder-only Twin diagnostic HTTP endpoints (SDT-001)."""

from __future__ import annotations

from flask import jsonify, request
from flask_login import current_user

from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.founder.dashboard.access import founder_required
from app.presentation.student_digital_twin import twin_diagnostics_bp
from app.presentation.student_digital_twin.serializers import (
    gap_public,
    mastery_public,
    observation_public,
    prediction_public,
    reasoning_public,
    recommendation_public,
    twin_public,
)


def _twins() -> StudentDigitalTwinService:
    return StudentDigitalTwinService()


def _not_found(twin_id: str):
    return jsonify({"ok": False, "error": f"Twin {twin_id!r} not found"}), 404


@twin_diagnostics_bp.get("")
@twin_diagnostics_bp.get("/")
@founder_required
def twin_index():
    """List twins for a student_id query param, or create via POST body elsewhere."""
    student_id = (request.args.get("student_id") or "").strip()
    if not student_id:
        return jsonify(
            {
                "ok": False,
                "error": "student_id query parameter is required",
                "hint": (
                    "GET /founder/twin?student_id=... "
                    "or GET /founder/twin/<twin_id>"
                ),
            }
        ), 400
    twins = _twins().list_twins_for_student(student_id)
    return jsonify({"ok": True, "twins": [twin_public(t) for t in twins]})


@twin_diagnostics_bp.post("")
@twin_diagnostics_bp.post("/")
@founder_required
def twin_create():
    """Create (or return existing) Twin for a learner scope."""
    payload = request.get_json(silent=True) or {}
    student_id = str(payload.get("student_id") or "").strip()
    if not student_id:
        return jsonify({"ok": False, "error": "student_id is required"}), 400
    twin = _twins().create(
        student_id=student_id,
        display_name=str(payload.get("display_name") or ""),
        subject_code=str(payload.get("subject_code") or ""),
        workspace_id=str(payload.get("workspace_id") or ""),
        external_user_id=(
            str(payload["external_user_id"])
            if payload.get("external_user_id") is not None
            else None
        ),
    )
    return jsonify({"ok": True, "twin": twin_public(twin)}), 201


@twin_diagnostics_bp.get("/<twin_id>")
@founder_required
def twin_detail(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify({"ok": True, "twin": twin_public(twin)})


@twin_diagnostics_bp.get("/<twin_id>/history")
@founder_required
def twin_history(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    snapshots = TwinPersistenceService().list_state_snapshots(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "observations": [observation_public(o) for o in twin.observations],
            "learning_state_snapshots": [
                {
                    "snapshot_id": s.snapshot_id,
                    "knowledge": s.knowledge,
                    "confidence": s.confidence,
                    "retention": s.retention,
                    "consistency": s.consistency,
                    "momentum": s.momentum,
                    "exam_readiness": s.exam_readiness,
                    "evidence_count": s.evidence_count,
                    "reason": s.reason,
                    "computed_at": s.computed_at.isoformat() if s.computed_at else None,
                }
                for s in snapshots
            ],
            "reasoning": [reasoning_public(r) for r in twin.reasoning_history],
        }
    )


@twin_diagnostics_bp.get("/<twin_id>/mastery")
@founder_required
def twin_mastery(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "mastery": [mastery_public(r) for r in twin.mastery.records],
        }
    )


@twin_diagnostics_bp.get("/<twin_id>/gaps")
@founder_required
def twin_gaps(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "gaps": [gap_public(g) for g in twin.knowledge_gaps],
        }
    )


@twin_diagnostics_bp.get("/<twin_id>/recommendations")
@founder_required
def twin_recommendations(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "recommendations": [
                recommendation_public(r) for r in twin.recommendations
            ],
        }
    )


@twin_diagnostics_bp.get("/<twin_id>/predictions")
@founder_required
def twin_predictions(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "predictions": [prediction_public(p) for p in twin.predictions],
        }
    )


@twin_diagnostics_bp.get("/<twin_id>/reasoning")
@founder_required
def twin_reasoning(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    return jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "reasoning": [reasoning_public(r) for r in twin.reasoning_history],
        }
    )


@twin_diagnostics_bp.post("/<twin_id>/observations")
@founder_required
def twin_record_observation(twin_id: str):
    """Founder diagnostic: append an observation and optionally re-reason."""
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    payload = request.get_json(silent=True) or {}
    kind = str(payload.get("kind") or "").strip()
    if not kind:
        return jsonify({"ok": False, "error": "kind is required"}), 400
    twin, obs = ObservationService().record(
        twin,
        kind=kind,
        curriculum_entity_id=str(payload.get("curriculum_entity_id") or ""),
        curriculum_entity_kind=str(payload.get("curriculum_entity_kind") or ""),
        evidence_reference=str(payload.get("evidence_reference") or ""),
        provenance=str(
            payload.get("provenance")
            or f"founder:{getattr(current_user, 'email', 'unknown')}"
        ),
        metadata=(
            payload.get("metadata")
            if isinstance(payload.get("metadata"), dict)
            else {}
        ),
    )
    if payload.get("reason", True):
        twin = StudentReasoningService().reason(
            twin,
            triggered_by="founder_observation",
            observation_ids=(obs.observation_id,),
        )
    return jsonify(
        {
            "ok": True,
            "observation": observation_public(obs),
            "twin": twin_public(twin),
        }
    ), 201


@twin_diagnostics_bp.post("/<twin_id>/reason")
@founder_required
def twin_reason(twin_id: str):
    twin = _twins().get(twin_id)
    if twin is None:
        return _not_found(twin_id)
    twin = StudentReasoningService().reason(twin, triggered_by="founder_manual")
    return jsonify({"ok": True, "twin": twin_public(twin)})
