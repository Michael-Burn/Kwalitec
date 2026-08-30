"""Founder-only Intelligent Tutor diagnostic HTTP endpoints (TUTOR-001).

ADR-027 Phase 2 Stage 3: labelled legacy SDT sandbox. Tutor diagnostics consume
SDT Twin state for Epic-2 experiments; not student-facing Estimated Knowledge
(see app.presentation.stack_c_sandbox).
"""

from __future__ import annotations

from datetime import datetime

from flask import jsonify, request

from app.application.intelligent_tutor.intelligent_tutor_service import (
    IntelligentTutorService,
)
from app.application.intelligent_tutor.persistence import (
    IntelligentTutorPersistenceService,
)
from app.extensions import db
from app.founder.dashboard.access import founder_required
from app.presentation.intelligent_tutor import intelligent_tutor_diagnostics_bp
from app.presentation.stack_c_sandbox import sandbox_jsonify


def _tutor() -> IntelligentTutorService:
    return IntelligentTutorService()


@intelligent_tutor_diagnostics_bp.get("/sessions")
@founder_required
def tutor_sessions():
    """List Tutor sessions for a twin_id query param."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return sandbox_jsonify(
            {
                "ok": True,
                "message": "Provide twin_id to list Tutor sessions.",
                "engine_version": IntelligentTutorService.ENGINE_VERSION,
            }
        )
    service = _tutor()
    sessions = service.list_sessions(twin_id)
    return sandbox_jsonify(
        {
            "ok": True,
            "twin_id": twin_id,
            "sessions": [service.session_as_dict(s) for s in sessions],
        }
    )


@intelligent_tutor_diagnostics_bp.get("/context")
@intelligent_tutor_diagnostics_bp.post("/context")
@founder_required
def tutor_context():
    """Build Tutor context for a twin + sample question (diagnostic)."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    text = str(
        payload.get("text")
        or request.args.get("text")
        or "Why is today's mission the right focus?"
    ).strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400

    from app.application.student_digital_twin.student_digital_twin_service import (
        StudentDigitalTwinService,
    )
    from app.domain.intelligent_tutor.tutor_question import (
        TutorQuestion,
        classify_question,
    )

    twin = StudentDigitalTwinService().get(twin_id)
    if twin is None:
        return jsonify({"ok": False, "error": f"twin {twin_id!r} not found"}), 404

    service = _tutor()
    question = TutorQuestion(
        question_id="diag-q",
        twin_id=twin_id,
        text=text,
        kind=classify_question(text),
    )
    context = service.build_context(
        twin, question, enrich_evidence=True
    )
    return sandbox_jsonify(
        {
            "ok": True,
            "context": {
                "context_id": context.context_id,
                "twin_id": context.twin_id,
                "question_kind": context.question_kind,
                "primary_concept_id": context.primary_concept_id,
                "active_mission_id": context.active_mission_id,
                "active_mission_goal": context.active_mission_goal,
                "recommendation_summaries": list(context.recommendation_summaries),
                "knowledge_gap_summaries": list(context.knowledge_gap_summaries),
                "recovery_path": list(context.recovery_path),
                "prerequisite_ids": list(context.prerequisite_ids),
                "curriculum_excerpts": list(context.curriculum_excerpts),
                "reasoning_run_id": context.reasoning_run_id,
                "learning_state_summary": context.learning_state_summary,
            },
        }
    )


@intelligent_tutor_diagnostics_bp.get("/evidence")
@intelligent_tutor_diagnostics_bp.post("/evidence")
@founder_required
def tutor_evidence():
    """Assemble structured Tutor evidence for a twin + question."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    text = str(
        payload.get("text")
        or request.args.get("text")
        or "Explain my knowledge gaps"
    ).strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400

    from app.application.student_digital_twin.student_digital_twin_service import (
        StudentDigitalTwinService,
    )
    from app.domain.intelligent_tutor.response_evidence import assemble_evidence
    from app.domain.intelligent_tutor.tutor_question import (
        TutorQuestion,
        classify_question,
    )

    twin = StudentDigitalTwinService().get(twin_id)
    if twin is None:
        return jsonify({"ok": False, "error": f"twin {twin_id!r} not found"}), 404

    service = _tutor()
    kind = classify_question(text)
    question = TutorQuestion(
        question_id="diag-ev-q",
        twin_id=twin_id,
        text=text,
        kind=kind,
    )
    context = service.build_context(twin, question, enrich_evidence=True)
    evidence = assemble_evidence(
        context, assembly_id="diag-asm", question_kind=kind
    )
    return sandbox_jsonify(
        {
            "ok": True,
            "assembly_id": evidence.assembly_id,
            "primary_concept_id": evidence.primary_concept_id,
            "counts": {
                "curriculum": evidence.curriculum_count,
                "student": evidence.student_count,
                "learning_graph": evidence.graph_count,
                "reasoning": evidence.reasoning_count,
                "observation": evidence.observation_count,
                "total": len(evidence.items),
            },
            "items": [
                {
                    "evidence_id": i.evidence_id,
                    "category": i.category.value,
                    "summary": i.summary,
                    "source_id": i.source_id,
                    "concept_id": i.concept_id,
                }
                for i in evidence.items
            ],
        }
    )


@intelligent_tutor_diagnostics_bp.get("/explanations")
@founder_required
def tutor_explanations():
    """List persisted Tutor explanations for a twin."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400
    rows = IntelligentTutorPersistenceService().list_explanations(twin_id)
    return sandbox_jsonify({"ok": True, "twin_id": twin_id, "explanations": rows})


@intelligent_tutor_diagnostics_bp.post("/ask")
@intelligent_tutor_diagnostics_bp.get("/ask")
@founder_required
def tutor_ask():
    """Run the full Tutor pipeline for a twin (diagnostic)."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    text = str(
        payload.get("text")
        or request.args.get("text")
        or "Why is today's mission the right focus?"
    ).strip()
    session_id = str(
        payload.get("session_id") or request.args.get("session_id") or ""
    ).strip() or None
    if not twin_id:
        return jsonify({"ok": False, "error": "twin_id is required"}), 400

    service = _tutor()
    try:
        response = service.ask(
            twin_id,
            text,
            session_id=session_id,
            persist=True,
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    return sandbox_jsonify({"ok": True, "response": service.as_dict(response)})


@intelligent_tutor_diagnostics_bp.get("/diagnostics")
@founder_required
def tutor_diagnostics():
    """Founder diagnostics for Intelligent Tutor state."""
    twin_id = (request.args.get("twin_id") or "").strip()
    if not twin_id:
        return sandbox_jsonify(
            {
                "ok": True,
                "engine_version": IntelligentTutorService.ENGINE_VERSION,
                "message": "Provide twin_id for Twin-scoped diagnostics.",
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }
        )
    return sandbox_jsonify(_tutor().diagnostics_for_twin(twin_id))


@intelligent_tutor_diagnostics_bp.post("/feedback")
@founder_required
def tutor_feedback():
    """Record diagnostic feedback on a Tutor response."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(payload.get("twin_id") or "").strip()
    session_id = str(payload.get("session_id") or "").strip()
    response_id = str(payload.get("response_id") or "").strip()
    if not twin_id or not session_id or not response_id:
        return jsonify(
            {
                "ok": False,
                "error": "twin_id, session_id, and response_id are required",
            }
        ), 400
    rating = int(payload.get("rating") or 0)
    comment = str(payload.get("comment") or "")
    helpful = payload.get("helpful")
    row = IntelligentTutorPersistenceService().save_feedback(
        twin_id=twin_id,
        session_id=session_id,
        response_id=response_id,
        rating=rating,
        comment=comment,
        helpful=bool(helpful) if helpful is not None else None,
    )
    db.session.commit()
    return sandbox_jsonify(
        {
            "ok": True,
            "feedback_id": row.feedback_id,
            "rating": row.rating,
        }
    )
