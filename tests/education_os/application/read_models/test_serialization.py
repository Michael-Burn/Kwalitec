"""Serialization tests for application read models (WEB-003)."""

from __future__ import annotations

import json

import pytest

from application.read_models import (
    DashboardProjectionBuilder,
    DashboardReadModel,
    MissionTaskReadModel,
    ProgressSummaryReadModel,
    RecommendationReadModel,
    TimelineEventReadModel,
    TimelineReadModel,
    TodaysMissionReadModel,
    to_dashboard_json,
)


def test_to_dashboard_json_rejects_non_dataclass() -> None:
    with pytest.raises(TypeError):
        to_dashboard_json({"student_id": "x"})


def test_recommendation_serializes_to_plain_dict() -> None:
    model = RecommendationReadModel(
        title="Continue studying",
        subtitle="Next useful step",
        primary_action="Start Session",
        reason_summary="Stay on plan",
        estimated_minutes=30,
        can_start=True,
        decision_id="dec-1",
        recommendation_id="rec-1",
    )
    payload = to_dashboard_json(model)
    assert payload == {
        "title": "Continue studying",
        "subtitle": "Next useful step",
        "primary_action": "Start Session",
        "reason_summary": "Stay on plan",
        "estimated_minutes": 30,
        "can_start": True,
        "decision_id": "dec-1",
        "recommendation_id": "rec-1",
    }
    json.dumps(payload)


def test_dashboard_serializes_nested_sections() -> None:
    dashboard = DashboardProjectionBuilder.build(
        student_id="student-ada",
        recommendation=RecommendationReadModel(
            title="Continue studying",
            subtitle=None,
            primary_action=None,
            reason_summary=None,
            estimated_minutes=None,
            can_start=False,
        ),
        todays_mission=TodaysMissionReadModel(
            title="Today's Session",
            summary="1 task",
            task_count=1,
            tasks=(
                MissionTaskReadModel(
                    task_id="step-1",
                    headline="Explanation",
                    sequence_index=0,
                    status="pending",
                ),
            ),
            estimated_minutes=20,
            can_open=True,
            episode_id="episode-001",
        ),
        progress=ProgressSummaryReadModel(
            student_id="student-ada",
            activity_status="engaged",
            twin_status="active",
            concept_count=1,
            evidence_count=2,
            intervention_count=0,
            progress_cues=("activity:engaged",),
            twin_id="twin-001",
        ),
        timeline=TimelineReadModel(
            student_id="student-ada",
            events=(
                TimelineEventReadModel(
                    sequence=0,
                    kind="created",
                    label="Twin created",
                ),
            ),
            twin_id="twin-001",
        ),
        warnings=("thin_warrant",),
        empty_states=(),
        composed_at="2026-07-20T10:00:00+00:00",
    )
    payload = to_dashboard_json(dashboard)
    assert isinstance(payload, dict)
    assert payload["student_id"] == "student-ada"
    assert payload["recommendation"]["title"] == "Continue studying"
    assert payload["todays_mission"]["tasks"][0]["headline"] == "Explanation"
    assert payload["progress"]["concept_count"] == 1
    assert payload["timeline"]["events"][0]["kind"] == "created"
    assert payload["warnings"] == ["thin_warrant"]
    json.dumps(payload)


def test_sparse_dashboard_serializes_null_sections() -> None:
    dashboard = DashboardReadModel(
        student_id="student-ada",
        recommendation=None,
        todays_mission=None,
        progress=None,
        timeline=None,
    )
    payload = to_dashboard_json(dashboard)
    assert payload["recommendation"] is None
    assert payload["todays_mission"] is None
    assert payload["progress"] is None
    assert payload["timeline"] is None
    json.dumps(payload)
