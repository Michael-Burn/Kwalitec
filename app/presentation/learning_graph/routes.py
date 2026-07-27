"""Founder-only Learning Graph diagnostic HTTP endpoints (SDT-003)."""

from __future__ import annotations

from flask import jsonify, request

from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.learning_graph.learning_graph_traversal_service import (
    LearningGraphTraversalService,
)
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.founder.dashboard.access import founder_required
from app.presentation.learning_graph import learning_graph_diagnostics_bp


def _graphs() -> LearningGraphService:
    return LearningGraphService()


def _traversal() -> LearningGraphTraversalService:
    return LearningGraphTraversalService()


@learning_graph_diagnostics_bp.get("/")
@founder_required
def learning_graph_index():
    """List Learning Graphs for an optional student_id query param."""
    student_id = (request.args.get("student_id") or "").strip()
    if not student_id:
        return jsonify(
            {
                "ok": True,
                "message": (
                    "Provide student_id to list graphs, or use "
                    "/founder/learning-graph/<student>"
                ),
            }
        )
    graphs = _graphs().list_for_student(student_id)
    return jsonify(
        {
            "ok": True,
            "student_id": student_id,
            "graphs": [_graphs().as_dict(g) for g in graphs],
        }
    )


@learning_graph_diagnostics_bp.post("/traverse")
@learning_graph_diagnostics_bp.get("/traverse")
@founder_required
def learning_graph_traverse():
    """Traverse connected concepts (diagnostic)."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    concept_id = str(
        payload.get("concept_id") or request.args.get("concept_id") or ""
    ).strip()
    kind = str(payload.get("kind") or request.args.get("kind") or "connected").strip()
    max_depth = int(payload.get("max_depth") or request.args.get("max_depth") or 4)

    if not twin_id or not concept_id:
        return jsonify(
            {"ok": False, "error": "twin_id and concept_id are required"}
        ), 400

    graph = _graphs().get_for_twin(twin_id)
    if graph is None:
        return jsonify(
            {"ok": False, "error": f"Learning Graph for twin {twin_id!r} not found"}
        ), 404

    trav = _traversal()
    if kind == "prerequisites":
        result = trav.prerequisites(graph, concept_id, max_depth=max_depth)
    elif kind == "dependencies":
        result = trav.dependencies(graph, concept_id, max_depth=max_depth)
    elif kind == "learning_path":
        path = trav.learning_path(graph, concept_id, max_depth=max_depth)
        return jsonify(
            {
                "ok": True,
                "kind": "learning_path",
                "result": trav.learning_path_as_dict(path),
            }
        )
    elif kind == "recovery":
        path = trav.recovery_path(graph, concept_id, max_depth=max_depth)
        return jsonify(
            {
                "ok": True,
                "kind": "recovery",
                "result": trav.recovery_as_dict(path),
            }
        )
    elif kind == "impact":
        analysis = trav.impact(graph, concept_id, max_depth=max_depth)
        return jsonify(
            {
                "ok": True,
                "kind": "impact",
                "result": trav.impact_as_dict(analysis),
            }
        )
    else:
        result = trav.connected(graph, concept_id, max_depth=max_depth)

    return jsonify(
        {
            "ok": True,
            "kind": result.kind,
            "result": trav.traversal_as_dict(result),
        }
    )


@learning_graph_diagnostics_bp.get("/prerequisites")
@learning_graph_diagnostics_bp.post("/prerequisites")
@founder_required
def learning_graph_prerequisites():
    """Prerequisite traversal diagnostic."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    concept_id = str(
        payload.get("concept_id") or request.args.get("concept_id") or ""
    ).strip()
    max_depth = int(payload.get("max_depth") or request.args.get("max_depth") or 8)
    if not twin_id or not concept_id:
        return jsonify(
            {"ok": False, "error": "twin_id and concept_id are required"}
        ), 400
    graph = _graphs().get_for_twin(twin_id)
    if graph is None:
        return jsonify(
            {"ok": False, "error": f"Learning Graph for twin {twin_id!r} not found"}
        ), 404
    trav = _traversal()
    result = trav.prerequisites(graph, concept_id, max_depth=max_depth)
    recovery = trav.recovery_path(graph, concept_id, max_depth=max_depth)
    return jsonify(
        {
            "ok": True,
            "prerequisites": trav.traversal_as_dict(result),
            "recovery_path": trav.recovery_as_dict(recovery),
        }
    )


@learning_graph_diagnostics_bp.get("/dependencies")
@learning_graph_diagnostics_bp.post("/dependencies")
@founder_required
def learning_graph_dependencies():
    """Dependency / impact traversal diagnostic."""
    payload = request.get_json(silent=True) or {}
    twin_id = str(
        payload.get("twin_id") or request.args.get("twin_id") or ""
    ).strip()
    concept_id = str(
        payload.get("concept_id") or request.args.get("concept_id") or ""
    ).strip()
    max_depth = int(payload.get("max_depth") or request.args.get("max_depth") or 8)
    if not twin_id or not concept_id:
        return jsonify(
            {"ok": False, "error": "twin_id and concept_id are required"}
        ), 400
    graph = _graphs().get_for_twin(twin_id)
    if graph is None:
        return jsonify(
            {"ok": False, "error": f"Learning Graph for twin {twin_id!r} not found"}
        ), 404
    trav = _traversal()
    result = trav.dependencies(graph, concept_id, max_depth=max_depth)
    impact = trav.impact(graph, concept_id, max_depth=max_depth)
    return jsonify(
        {
            "ok": True,
            "dependencies": trav.traversal_as_dict(result),
            "impact": trav.impact_as_dict(impact),
        }
    )


@learning_graph_diagnostics_bp.get("/<student_id>")
@founder_required
def learning_graph_for_student(student_id: str):
    """Return Learning Graphs for a student (diagnostic).

    Registered after static paths so /traverse, /prerequisites, /dependencies
    are not captured by this parameter route.
    """
    twin_id = (request.args.get("twin_id") or "").strip()
    svc = _graphs()
    if twin_id:
        graph = svc.get_for_twin(twin_id)
        if graph is None:
            return jsonify(
                {
                    "ok": False,
                    "error": f"Learning Graph for twin {twin_id!r} not found",
                }
            ), 404
        return jsonify(
            {"ok": True, "student_id": student_id, "graph": svc.as_dict(graph)}
        )

    twins = StudentDigitalTwinService().list_twins_for_student(student_id)
    graphs = []
    for twin in twins:
        graph = svc.get_or_create_for_twin(twin, persist=True)
        graphs.append(svc.as_dict(graph))
    return jsonify({"ok": True, "student_id": student_id, "graphs": graphs})
