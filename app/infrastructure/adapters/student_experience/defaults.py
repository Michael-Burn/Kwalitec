"""Default opaque projections provisioned into production stores.

These documents represent educational-platform projection shapes expected by
Student Experience ports. Values originate from store provisioning (or injected
engines) — adapters never invent readiness or recommendation math.
"""

from __future__ import annotations

from typing import Any


def default_twin_document(student_id: str) -> dict[str, Any]:
    """Opaque Twin projection for Experience StudentTwinPort."""
    return {
        "student_id": student_id,
        "display_name": "",
        "examination_label": "",
        "exam_countdown_days": None,
        "preferences": {
            "preferred_session_minutes": 45,
            "preferred_study_days": (),
            "reminder_enabled": False,
            "quiet_hours_label": "",
        },
        "goals": (),
        "account": {
            "email": "",
            "notifications_enabled": True,
            "locale": "en",
            "timezone": "UTC",
        },
        "statistics": {
            "total_study_minutes": 0,
            "sessions_completed": 0,
            "topics_mastered": 0,
            "current_exam_readiness": None,
            "study_streak_days": 0,
        },
        "readiness": {
            "examination_label": "",
            "exam_countdown_days": None,
            "exam_readiness": None,
            "readiness_score": None,
            "readiness_label": "",
        },
        "insights": {
            "completed_sessions": (),
            "total_study_minutes": 0,
            "readiness_progression": (),
            "mastered_topics": (),
            "revision_history": (),
            "recent_achievements": (),
            "sessions_completed": 0,
            "topics_mastered": 0,
        },
        "authority": "student_twin",
    }


def default_adaptive_document(student_id: str) -> dict[str, Any]:
    """Opaque Adaptive Decision projection for Experience AdaptiveDecisionPort."""
    return {
        "student_id": student_id,
        "recommendation": None,
        "revision_options": (),
        "explanations": {},
        "authority": "adaptive_decision_engine",
        "next_action_authority": True,
    }


def default_journey_document(student_id: str) -> dict[str, Any]:
    """Opaque Journey projection for Experience LearningJourneyPort."""
    return {
        "student_id": student_id,
        "progress": {
            "overall_progress_ratio": 0.0,
            "estimated_completion_label": "",
            "examination_label": "",
            "current_topic_id": "",
            "current_topic_title": "",
        },
        "topics": (),
        "authority": "learning_journey",
    }


def default_mission_document(student_id: str) -> dict[str, Any]:
    """Opaque Mission projection for Experience MissionPort."""
    return {
        "student_id": student_id,
        "todays_session": None,
        "sessions": {},
        "authority": "mission_engine",
        "next_action_authority": False,
    }


def default_activity_document(student_id: str) -> dict[str, Any]:
    """Opaque Orchestrator activity projection."""
    return {
        "student_id": student_id,
        "status": "idle",
        "status_label": "Ready for today's session",
        "acknowledged": {},
        "authority": "learning_orchestrator",
    }


def seeded_demo_twin(student_id: str) -> dict[str, Any]:
    """Provisioned Twin projection used when engines seed a learner."""
    doc = default_twin_document(student_id)
    doc.update(
        {
            "display_name": "Learner",
            "examination_label": "Professional Examination",
            "exam_countdown_days": 64,
            "preferences": {
                "preferred_session_minutes": 45,
                "preferred_study_days": ("Mon", "Wed", "Fri"),
                "reminder_enabled": True,
                "quiet_hours_label": "22:00–07:00",
            },
            "goals": (
                {
                    "goal_id": "g1",
                    "title": "Reach exam readiness",
                    "target_label": "Exam sitting",
                    "progress_ratio": 0.4,
                },
            ),
            "account": {
                "email": "",
                "notifications_enabled": True,
                "locale": "en",
                "timezone": "UTC",
            },
            "statistics": {
                "total_study_minutes": 320,
                "sessions_completed": 12,
                "topics_mastered": 4,
                "current_exam_readiness": 0.58,
                "study_streak_days": 0,
            },
            "readiness": {
                "examination_label": "Professional Examination",
                "exam_countdown_days": 64,
                "exam_readiness": 0.58,
                "readiness_score": 0.58,
                "readiness_label": "Building",
            },
            "insights": {
                "completed_sessions": (
                    {
                        "session_id": "s1",
                        "topic_title": "Foundations",
                        "completed_at": "2026-07-10",
                        "study_minutes": 40,
                    },
                    {
                        "session_id": "s2",
                        "topic_title": "Core methods",
                        "completed_at": "2026-07-15",
                        "study_minutes": 35,
                    },
                ),
                "total_study_minutes": 320,
                "readiness_progression": (
                    {"recorded_at": "2026-06-01", "exam_readiness": 0.35},
                    {"recorded_at": "2026-07-01", "exam_readiness": 0.58},
                ),
                "mastered_topics": ("Foundations", "Core methods"),
                "revision_history": ("Ethics review", "Methods refresh"),
                "recent_achievements": (
                    {
                        "achievement_id": "a1",
                        "title": "Completed Foundations",
                        "earned_at": "2026-07-10",
                        "description": "Finished the foundations block",
                    },
                ),
                "sessions_completed": 12,
                "topics_mastered": 2,
            },
        }
    )
    return doc


def seeded_demo_adaptive(student_id: str) -> dict[str, Any]:
    """Provisioned Adaptive projection (engine output shape)."""
    explanation = {
        "topic_title": "Core methods",
        "reason_codes": ("high_roi", "exam_proximity"),
        "evidence_points": (
            "Recent practice showed soft recall on this topic",
            "This topic appears frequently in the examination",
        ),
        "expected_benefit": "Strengthen exam readiness",
        "priority_band": "high",
        "confidence": "strong",
    }
    recommendation = {
        "decision_id": "d1",
        "title": "Strengthen core methods",
        "topic_title": "Core methods",
        "summary": "Focused practice where readiness gains are strongest today.",
        "estimated_minutes": 30,
        "expected_readiness_improvement": 0.03,
        "priority_band": "high",
        "mission_id": "m1",
        "explanation": explanation,
    }
    revisions = (
        {
            "option_id": "r1",
            "topic_title": "Core methods",
            "priority_label": "High priority",
            "estimated_minutes": 25,
            "expected_benefit": "Protect weak recall before the exam",
            "mission_id": "m1",
            "explanation": {
                "topic_title": "Core methods",
                "reason_codes": ("low_retention",),
                "evidence_points": ("Recall soft on this topic",),
                "expected_benefit": "Protect weak recall",
            },
        },
        {
            "option_id": "r2",
            "topic_title": "Ethics",
            "priority_label": "Medium priority",
            "estimated_minutes": 20,
            "expected_benefit": "Steady progress on a supporting topic",
        },
    )
    return {
        "student_id": student_id,
        "recommendation": recommendation,
        "revision_options": revisions,
        "explanations": {"d1": explanation},
        "authority": "adaptive_decision_engine",
        "next_action_authority": True,
    }


def seeded_demo_journey(student_id: str) -> dict[str, Any]:
    """Provisioned Journey projection (engine output shape)."""
    return {
        "student_id": student_id,
        "progress": {
            "overall_progress_ratio": 0.42,
            "estimated_completion_label": "About 10 weeks",
            "examination_label": "Professional Examination",
            "current_topic_id": "t2",
            "current_topic_title": "Core methods",
        },
        "topics": (
            {
                "topic_id": "t1",
                "title": "Foundations",
                "status": "completed",
                "status_label": "Completed",
            },
            {
                "topic_id": "t2",
                "title": "Core methods",
                "status": "current",
                "status_label": "Current",
                "prerequisite_note": "Build on Foundations",
            },
            {
                "topic_id": "t3",
                "title": "Advanced applications",
                "status": "upcoming",
                "status_label": "Upcoming",
                "prerequisite_note": "Finish Core methods first",
            },
        ),
        "authority": "learning_journey",
    }


def seeded_demo_mission(student_id: str) -> dict[str, Any]:
    """Provisioned Mission projection (engine output shape)."""
    session = {
        "mission_id": "m1",
        "session_id": "sess-1",
        "topic_title": "Core methods",
        "estimated_minutes": 30,
        "status": "ready",
    }
    return {
        "student_id": student_id,
        "todays_session": session,
        "sessions": {"sess-1": dict(session)},
        "authority": "mission_engine",
        "next_action_authority": False,
    }


def seeded_demo_activity(student_id: str) -> dict[str, Any]:
    """Provisioned Orchestrator activity projection."""
    doc = default_activity_document(student_id)
    doc["status_label"] = "Ready for today's session"
    return doc
