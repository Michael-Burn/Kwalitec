"""Dashboard API routes — HTTP orchestration over dashboard read models."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from web.blueprints.dashboard.schemas import (
    parse_get_dashboard,
    parse_get_progress,
    parse_get_recommendations,
    parse_get_timeline,
    parse_get_todays_mission,
    serialize_read_model,
)
from web.lifecycle import get_services

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
def get_dashboard() -> tuple[Any, int]:
    query = parse_get_dashboard(request.args)
    read_model = get_services().dashboard.get_dashboard(query)
    return jsonify(serialize_read_model(read_model)), 200


@dashboard_bp.get("/dashboard/today")
def get_today() -> tuple[Any, int]:
    query = parse_get_todays_mission(request.args)
    read_model = get_services().dashboard.get_todays_mission(query)
    return jsonify(serialize_read_model(read_model)), 200


@dashboard_bp.get("/dashboard/progress")
def get_progress() -> tuple[Any, int]:
    query = parse_get_progress(request.args)
    read_model = get_services().dashboard.get_progress(query)
    return jsonify(serialize_read_model(read_model)), 200


@dashboard_bp.get("/dashboard/recommendations")
def get_recommendations() -> tuple[Any, int]:
    query = parse_get_recommendations(request.args)
    read_model = get_services().dashboard.get_recommendations(query)
    return jsonify(serialize_read_model(read_model)), 200


@dashboard_bp.get("/dashboard/timeline")
def get_timeline() -> tuple[Any, int]:
    query = parse_get_timeline(request.args)
    read_model = get_services().dashboard.get_timeline(query)
    return jsonify(serialize_read_model(read_model)), 200
