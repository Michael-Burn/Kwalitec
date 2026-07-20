"""Learning API routes — HTTP orchestration over application services."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from web.blueprints.learning.schemas import (
    parse_complete_learning_episode,
    parse_get_learner_state,
    parse_get_learning_trajectory,
    parse_record_evidence,
    parse_start_learning_session,
    serialize_dto,
)
from web.lifecycle import get_services

learning_bp = Blueprint("learning", __name__, url_prefix="/learning")


@learning_bp.post("/session/start")
def start_session() -> tuple[Any, int]:
    command = parse_start_learning_session(request.get_json(silent=True))
    dto = get_services().learning.start_learning_session(command)
    return jsonify(serialize_dto(dto)), 200


@learning_bp.post("/episode/complete")
def complete_episode() -> tuple[Any, int]:
    command = parse_complete_learning_episode(request.get_json(silent=True))
    dto = get_services().learning.complete_learning_episode(command)
    return jsonify(serialize_dto(dto)), 200


@learning_bp.post("/evidence")
def record_evidence() -> tuple[Any, int]:
    command = parse_record_evidence(request.get_json(silent=True))
    dto = get_services().assessment.record_evidence(command)
    return jsonify(serialize_dto(dto)), 201


@learning_bp.get("/state/<student_id>")
def get_state(student_id: str) -> tuple[Any, int]:
    query = parse_get_learner_state(student_id)
    dto = get_services().twin.get_learner_state(query)
    return jsonify(serialize_dto(dto)), 200


@learning_bp.get("/trajectory/<student_id>")
def get_trajectory(student_id: str) -> tuple[Any, int]:
    query = parse_get_learning_trajectory(student_id)
    dto = get_services().twin.get_learning_trajectory(query)
    return jsonify(serialize_dto(dto)), 200
