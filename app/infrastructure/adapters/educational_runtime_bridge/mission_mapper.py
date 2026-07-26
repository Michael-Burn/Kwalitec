"""Mission → Experience opaque session mapping (translator only)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.infrastructure.adapters.educational_runtime_bridge.contracts import (
    AUTHORITY_PLANNING_SERVICE,
    AUTHORITY_STUDY_SESSION_SERVICE,
)
from app.models.mission import Mission

# SQL Mission.status → Experience session status.
_STATUS_MAP: dict[str, str] = {
    "pending": "ready",
    "in progress": "in_progress",
    "completed": "completed",
}


def map_mission_status(sql_status: str | None) -> str:
    """Map Runtime A mission status to Experience session status."""
    key = (sql_status or "").strip().lower()
    return _STATUS_MAP.get(key, "ready")


def map_mission_tasks(mission: Mission) -> list[dict[str, Any]]:
    """Project MissionTask rows to opaque task dicts (no educational invention)."""
    tasks: list[dict[str, Any]] = []
    for task in list(mission.tasks or []):
        tasks.append(
            {
                "id": str(task.id),
                "title": str(task.title or ""),
                "description": (
                    None if task.description is None else str(task.description)
                ),
                "order": int(task.order or 0),
                "completed": bool(task.completed),
            }
        )
    return tasks


def map_mission_to_todays_session(
    mission: Mission,
    *,
    student_id: str,
    lifecycle_stage: str | None = None,
    topic_code: str | None = None,
    estimated_minutes: int | None = None,
) -> dict[str, Any]:
    """Translate a SQL Mission into the Experience ``todays_session`` shape.

    Field values are taken from Runtime A records only. This function does not
    choose topics, invent minutes, or alter educational behaviour.
    """
    mission_id = str(mission.id)
    return {
        "student_id": student_id.strip(),
        "mission_id": mission_id,
        "session_id": mission_id,
        "topic_code": (topic_code or "").strip(),
        "topic_title": str(mission.title or ""),
        "estimated_minutes": estimated_minutes,
        "status": map_mission_status(mission.status),
        "tasks": map_mission_tasks(mission),
        "lifecycle_stage": (lifecycle_stage or "").strip(),
        "authority": AUTHORITY_PLANNING_SERVICE,
        "next_action_authority": False,
    }


def map_mission_to_start_result(
    mission: Mission,
    *,
    student_id: str,
    session_id: str | None = None,
    estimated_minutes: int | None = None,
    started_at: str | None = None,
) -> dict[str, Any]:
    """Translate a started SQL Mission into the Experience start_session shape.

    Does not invent topics or educational state — values come from Runtime A.
    ``started_at`` is an observational timestamp for the UX handle only.
    """
    mission_key = str(mission.id)
    resolved_session = str(session_id or mission_key)
    stamp = started_at or (
        datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
    )
    return {
        "student_id": student_id.strip(),
        "mission_id": mission_key,
        "session_id": resolved_session,
        "experience_session_id": f"es-{resolved_session}",
        "topic_title": str(mission.title or ""),
        "estimated_minutes": estimated_minutes,
        "started_at": stamp,
        "status": "in_progress",
        "authority": AUTHORITY_STUDY_SESSION_SERVICE,
        "next_action_authority": False,
    }


def map_mission_to_resume_result(
    mission: Mission,
    *,
    student_id: str,
    session_id: str | None = None,
    estimated_minutes: int | None = None,
) -> dict[str, Any]:
    """Translate an active SQL Mission into the Experience resume shape.

    Preserves mission/session identity and Runtime A progress (tasks/status).
    Does not invent topics, start Pending missions, or alter learning state.
    """
    mission_key = str(mission.id)
    resolved_session = str(session_id or mission_key)
    return {
        "student_id": student_id.strip(),
        "mission_id": mission_key,
        "session_id": resolved_session,
        "experience_session_id": f"es-{resolved_session}",
        "topic_title": str(mission.title or ""),
        "estimated_minutes": estimated_minutes,
        "status": map_mission_status(getattr(mission, "status", None)),
        "tasks": map_mission_tasks(mission),
        "authority": AUTHORITY_STUDY_SESSION_SERVICE,
        "next_action_authority": False,
        "resumed": True,
    }


def map_mission_to_completion_result(
    mission: Mission,
    *,
    student_id: str,
    session_id: str | None = None,
    topic_title: str = "",
    estimated_minutes: int | None = None,
    completed_at: str | None = None,
    evidence_accepted: bool = False,
    mastery_updated: bool = False,
) -> dict[str, Any]:
    """Translate a completed SQL Mission into the Experience completion shape.

    Values come from Runtime A only. Does not invent topics or mastery.
    """
    mission_key = str(mission.id)
    resolved_session = str(session_id or mission_key)
    stamp = completed_at or (
        datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
    )
    title = topic_title or str(mission.title or "")
    return {
        "student_id": student_id.strip(),
        "mission_id": mission_key,
        "session_id": resolved_session,
        "experience_session_id": f"es-{resolved_session}",
        "topic_title": title,
        "estimated_minutes": estimated_minutes,
        "status": "completed",
        "completed_at": stamp,
        "educational_complete": True,
        "evidence_accepted": bool(evidence_accepted),
        "mastery_updated": bool(mastery_updated),
        "tasks": map_mission_tasks(mission),
        "authority": AUTHORITY_STUDY_SESSION_SERVICE,
        "next_action_authority": False,
    }
