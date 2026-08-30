"""Founder-only Educational Reasoning diagnostic HTTP endpoints (SDT-002).

ADR-027 Phase 2 Stage 3: this surface exercises the Epic-2 reasoning engine
against SDT SQL. It is an explicitly labelled legacy diagnostic sandbox, not
student-facing Estimated Knowledge (see app.presentation.stack_c_sandbox).
"""

from __future__ import annotations

from typing import Any

from flask import jsonify, request

from app.application.educational_reasoning.educational_reasoning_service import (
    EducationalReasoningService,
)
from app.application.educational_reasoning.persistence import (
    ReasoningPersistenceService,
)
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.founder.dashboard.access import founder_required
from app.presentation.educational_reasoning import reasoning_diagnostics_bp
from app.presentation.stack_c_sandbox import with_stack_c_sandbox_label
from app.presentation.student_digital_twin.serializers import twin_public


def _reasoning() -> EducationalReasoningService:
    return EducationalReasoningService()


def _persistence() -> ReasoningPersistenceService:
    return ReasoningPersistenceService()


def _sandbox(payload: dict[str, Any]):
    return jsonify(with_stack_c_sandbox_label(payload))


@reasoning_diagnostics_bp.post("/run")
@founder_required
def reasoning_run():
    """Run the Educational Reasoning Engine for a Twin (diagnostic)."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(payload.get("twin_id") or request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400

    twin = StudentDigitalTwinService().get(twin_id)
    if twin is None:
        return jsonify({"ok": False, "error": f"Twin {twin_id!r} not found"}), 404

    triggered_by = str(payload.get("triggered_by") or "founder_reasoning_run")
    twin = StudentReasoningService().reason(twin, triggered_by=triggered_by)
    runs = _persistence().list_runs_for_twin(twin_id, limit=1)
    run_payload = _persistence().run_as_dict(runs[0]) if runs else None
    return _sandbox(
        {
            "ok": True,
            "twin": twin_public(twin),
            "reasoning_run": run_payload,
        }
    )


@reasoning_diagnostics_bp.get("/history")
@founder_required
def reasoning_history():
    """List immutable reasoning runs for a twin_id query param."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify(
            {"ok": False, "error": "twin_id query parameter is required"}
        ), 400
    limit = min(int(request.args.get("limit") or 50), 200)
    runs = _persistence().list_runs_for_twin(twin_id, limit=limit)
    return _sandbox(
        {
            "ok": True,
            "twin_id": twin_id,
            "runs": [_persistence().run_as_dict(r) for r in runs],
        }
    )


@reasoning_diagnostics_bp.get("/rules")
@founder_required
def reasoning_rules():
    """List registered educational reasoning rules."""
    rules = _reasoning().list_rules()
    return _sandbox(
        {
            "ok": True,
            "engine_version": EducationalReasoningService.engine_version(),
            "rules": list(rules),
        }
    )


@reasoning_diagnostics_bp.get("/explanations")
@founder_required
def reasoning_explanations():
    """List reasoning explanations (optional twin_id / run_id filters)."""
    twin_id = (request.args.get("twin_id") or "").strip() or None
    run_id = (request.args.get("run_id") or "").strip() or None
    limit = min(int(request.args.get("limit") or 100), 500)
    rows = _persistence().list_explanations(
        twin_id=twin_id, run_id=run_id, limit=limit
    )
    return _sandbox(
        {
            "ok": True,
            "explanations": [_persistence().explanation_as_dict(r) for r in rows],
        }
    )


@reasoning_diagnostics_bp.get("/decision/<decision_id>")
@founder_required
def reasoning_decision(decision_id: str):
    """Fetch one educational decision record by id."""
    row = _persistence().get_decision(decision_id)
    if row is None:
        return jsonify(
            {"ok": False, "error": f"Decision {decision_id!r} not found"}
        ), 404
    return _sandbox(
        {"ok": True, "decision": _persistence().decision_as_dict(row)}
    )
