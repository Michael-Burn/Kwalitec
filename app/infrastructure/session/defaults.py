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
        # CQ-005: humble default — composition threads recommendation why.
        "why_studying": "This Session is today's recommended next step.",
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
    student_id: str,
    *,
    session_id: str,
    topic_title: str = "Core methods",
) -> dict[str, Any]:
    """Opaque reflection guidance facts."""
    topic = (topic_title or "today's topic").strip() or "today's topic"
    return {
        "student_id": student_id,
        "session_id": session_id,
        "key_insight": f"Focused practice on {topic} strengthens recall",
        "concept_confidence": f"Growing comfort with {topic}",
        "suggested_improvement": (
            f"Revisit borderline cases in {topic} next session"
        ),
        "reflection_prompt": f"What still feels unclear about {topic}?",
        "topic_title": topic,
        "next_action_label": "Continue to Summary",
        "student_note": "",
        "authority": "learning_session_runtime",
    }


def default_completion_summary(
    student_id: str,
    *,
    session_id: str,
    topic_title: str = "Core methods",
) -> dict[str, Any]:
    """Opaque session completion / summary facts."""
    topic = (topic_title or "Core methods").strip() or "Core methods"
    return {
        "student_id": student_id,
        "session_id": session_id,
        "topics_completed": (topic,),
        "time_studied_minutes": 28,
        "activities_completed": 3,
        "learning_insights": (
            f"Completing practice on {topic} builds exam-ready recall",
        ),
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
    topic_title: str = "Core methods",
    why_studying: str = "",
) -> dict[str, Any]:
    """Opaque current activity facts.

    Topic-threaded prompts keep the activity coherent with today's Mission
    without inventing new educational content (CQ-004). CQ-005 echoes the
    mission why into context when already present on the overview.
    """
    topic = (topic_title or "today's topic").strip() or "today's topic"
    why = (why_studying or "").strip()
    is_final = index >= total
    prompts = (
        f"In your own words, explain one key idea from {topic}.",
        f"Describe a situation where {topic} applies — what would you do first?",
        f"What still feels unclear about {topic}, and how would you check it?",
    )
    question = prompts[(index - 1) % len(prompts)]
    if why:
        context = f"You're practising {topic} because {why}"
    else:
        context = f"Focused practice on {topic}"
    return {
        "student_id": student_id,
        "session_id": session_id,
        "activity_id": f"act-{index}",
        "question": question,
        "context": context,
        "supporting_material": (
            f"Review the core definition for {topic} and one worked example"
        ),
        "hints": (f"Start from the definition of {topic}",),
        "activity_index": index,
        "activities_total": total,
        "topic_title": topic,
        "phase": "ready",
        "answer_prompt": "Your answer",
        "next_action_label": (
            "Continue to Reflection" if is_final else "Continue"
        ),
        "authority": "learning_activity_engine",
    }


def default_activity_progress(
    student_id: str,
    *,
    session_id: str,
    completed: int = 0,
    total: int = 3,
    topic_title: str = "Core methods",
) -> dict[str, Any]:
    """Opaque activity sequence progress facts."""
    remaining = max(0, total - completed)
    topic = (topic_title or "Core methods").strip() or "Core methods"
    return {
        "student_id": student_id,
        "session_id": session_id,
        "activities_completed": completed,
        "activities_remaining": remaining,
        "activities_total": total,
        "estimated_remaining_minutes": remaining * 8,
        "current_topic": topic,
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
