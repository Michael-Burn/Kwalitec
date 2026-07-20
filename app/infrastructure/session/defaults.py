"""Default opaque session documents for Session Experience adapters.

Adapters provision these shapes when engines are absent. Values are
structural presentation facts — adapters never invent readiness or
recommendation math.
"""

from __future__ import annotations

from typing import Any


def default_session_overview(
    student_id: str, *, session_id: str, mission_id: str = "m1"
) -> dict[str, Any]:
    """Opaque Session Runtime overview facts."""
    return {
        "student_id": student_id,
        "session_id": session_id,
        "mission_id": mission_id,
        "experience_session_id": f"es-{session_id}",
        "objective": "Strengthen today's focus topic",
        "learning_goal": "Build confident recall for the examination",
        "why_studying": "High value for exam readiness",
        "estimated_minutes": 30,
        "activity_count": 3,
        "topics": ("Core methods",),
        "expected_readiness_improvement": 0.03,
        "status": "overview",
        "authority": "learning_session_runtime",
    }


def default_runtime_snapshot(
    student_id: str, *, session_id: str
) -> dict[str, Any]:
    """Opaque runtime progress facts."""
    return {
        "student_id": student_id,
        "session_id": session_id,
        "activities_completed": 0,
        "activities_remaining": 3,
        "activities_total": 3,
        "estimated_remaining_minutes": 30,
        "current_topic": "Core methods",
        "overall_progress": 0.0,
        "authority": "learning_session_runtime",
    }


def default_reflection(
    student_id: str, *, session_id: str
) -> dict[str, Any]:
    """Opaque reflection guidance facts."""
    return {
        "student_id": student_id,
        "session_id": session_id,
        "key_insight": "Focused practice strengthens recall",
        "concept_confidence": "Growing comfort with today's topic",
        "suggested_improvement": "Revisit borderline cases next session",
        "reflection_prompt": "What still feels unclear about today's topic?",
        "topic_title": "Core methods",
        "next_action_label": "Continue to Summary",
        "authority": "learning_session_runtime",
    }


def default_completion_summary(
    student_id: str, *, session_id: str
) -> dict[str, Any]:
    """Opaque session completion / summary facts."""
    return {
        "student_id": student_id,
        "session_id": session_id,
        "topics_completed": ("Core methods",),
        "time_studied_minutes": 28,
        "activities_completed": 3,
        "learning_insights": ("Consistent practice helps retention",),
        "exam_readiness_change": 0.03,
        "exam_readiness_change_label": "",
        "authority": "learning_session_runtime",
    }


def default_activity(
    student_id: str,
    *,
    session_id: str,
    index: int = 1,
    total: int = 3,
) -> dict[str, Any]:
    """Opaque current activity facts."""
    return {
        "student_id": student_id,
        "session_id": session_id,
        "activity_id": f"act-{index}",
        "question": f"Question {index}: explain a key idea from today's topic",
        "context": "Focused practice item",
        "supporting_material": "Review the core definition and one worked example",
        "hints": ("Start from the definition",),
        "activity_index": index,
        "activities_total": total,
        "topic_title": "Core methods",
        "phase": "ready",
        "answer_prompt": "Your answer",
        "next_action_label": "Continue",
        "authority": "learning_activity_engine",
    }


def default_activity_progress(
    student_id: str,
    *,
    session_id: str,
    completed: int = 0,
    total: int = 3,
) -> dict[str, Any]:
    """Opaque activity sequence progress facts."""
    remaining = max(0, total - completed)
    return {
        "student_id": student_id,
        "session_id": session_id,
        "activities_completed": completed,
        "activities_remaining": remaining,
        "activities_total": total,
        "estimated_remaining_minutes": remaining * 8,
        "current_topic": "Core methods",
        "overall_progress": (completed / total) if total else 0.0,
        "authority": "learning_activity_engine",
    }


def default_mission_session(
    student_id: str, *, session_id: str = "sess-1", mission_id: str = "m1"
) -> dict[str, Any]:
    """Opaque today's session / mission summary."""
    return {
        "student_id": student_id,
        "mission_id": mission_id,
        "session_id": session_id,
        "topic_title": "Core methods",
        "estimated_minutes": 30,
        "status": "ready",
        "objective": "Strengthen today's focus topic",
        "topics": ("Core methods",),
        "authority": "mission_engine",
        "next_action_authority": False,
    }
