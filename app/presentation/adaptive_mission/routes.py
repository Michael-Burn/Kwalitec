"""Founder-only Adaptive Mission Engine diagnostic HTTP endpoints (AME-001).

ADR-027 Phase 2 Stage 3: labelled legacy SDT sandbox. Adaptive mission
generation here is Twin-first Epic-2 diagnostics, not student Home authority
(see app.presentation.stack_c_sandbox).
"""

from __future__ import annotations

from datetime import date, datetime

from flask import jsonify, request

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)
from app.founder.dashboard.access import founder_required
from app.presentation.adaptive_mission import adaptive_mission_diagnostics_bp
from app.presentation.stack_c_sandbox import sandbox_jsonify


def _missions() -> AdaptiveMissionService:
    return AdaptiveMissionService()


@adaptive_mission_diagnostics_bp.get("/")
@founder_required
def missions_index():
    """List adaptive missions for a twin_id query param."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return sandbox_jsonify(
            {
                "ok": True,
                "message": (
                    "Provide twin_id to list missions, or POST "
                    "/founder/missions/generate"
                ),
                "engine_version": AdaptiveMissionService.ENGINE_VERSION,
            }
        )
    missions = _missions().list_for_twin(twin_id)
    active = _missions().get_active(twin_id)
    return sandbox_jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "active_mission_id": active.mission_id if active else None,
            "missions": [_missions().as_dict(m) for m in missions],
        }
    )


@adaptive_mission_diagnostics_bp.post("/generate")
@adaptive_mission_diagnostics_bp.get("/generate")
@founder_required
def missions_generate():
    """Generate today's adaptive mission from Twin educational decisions."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400

    mission_date_raw = payload.get("mission_date") or request.args.get("mission_date")
    mission_date = None
    if mission_date_raw:
        mission_date = date.fromisoformat(str(mission_date_raw))

    available_minutes = int(
        payload.get("available_minutes")
        or request.args.get("available_minutes")
        or 45
    )
    activate = str(
        payload.get("activate", request.args.get("activate", "true"))
    ).lower() not in {"0", "false", "no"}

    try:
        mission = _missions().generate_for_twin(
            twin_id,
            mission_date=mission_date,
            available_minutes=available_minutes,
            activate=activate,
            persist=True,
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    return sandbox_jsonify(
        {
            "ok": True,
            "mission": _missions().as_dict(mission),
            "mission_card": mission.as_mission_card(),
        }
    )


@adaptive_mission_diagnostics_bp.get("/history")
@founder_required
def missions_history():
    """Append-only adaptive mission history for a twin."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400
    history = _missions().history_for_twin(twin_id)
    return sandbox_jsonify({"ok": True, "twin_id": twin_id, "history": history})


@adaptive_mission_diagnostics_bp.post("/validate")
@adaptive_mission_diagnostics_bp.get("/validate")
@founder_required
def missions_validate():
    """Validate an existing adaptive mission or a dry-run generation."""
    payload = request.get_json(silent=True) or {}
    mission_id = str(
        payload.get("mission_id") or request.args.get("mission_id") or ""
    ).strip()
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()

    service = _missions()
    if mission_id:
        mission = service.get(mission_id)
        if mission is None:
            return jsonify(
                {"ok": False, "error": f"mission {mission_id!r} not found"}
            ), 404
        result = service.validate(mission, check_active_duplicate=False)
        return sandbox_jsonify(
            {
                "ok": True,
                "mission_id": mission_id,
                "passed": result.passed,
                "summary": result.summary,
                "issues": [
                    {
                        "code": i.code,
                        "severity": i.severity.value,
                        "message": i.message,
                    }
                    for i in result.issues
                ],
            }
        )

    if not twin_id:
        return jsonify(
            {"ok": False, "error": "mission_id or twin_id is required"}
        ), 400

    try:
        mission = service.generate_for_twin(
            twin_id,
            activate=False,
            persist=False,
            enrich_evidence=False,
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc), "passed": False}), 400

    result = service.validate(mission, check_active_duplicate=True)
    return sandbox_jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "dry_run_mission_id": mission.mission_id,
            "passed": result.passed,
            "summary": result.summary,
            "issues": [
                {
                    "code": i.code,
                    "severity": i.severity.value,
                    "message": i.message,
                }
                for i in result.issues
            ],
            "mission": service.as_dict(mission),
        }
    )


@adaptive_mission_diagnostics_bp.get("/diagnostics")
@founder_required
def missions_diagnostics():
    """Founder diagnostics for Adaptive Mission Engine state."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return sandbox_jsonify(
            {
                "ok": True,
                "engine_version": AdaptiveMissionService.ENGINE_VERSION,
                "message": "Provide twin_id for Twin-scoped diagnostics.",
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }
        )
    return sandbox_jsonify(_missions().diagnostics_for_twin(twin_id))
