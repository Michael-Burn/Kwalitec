"""Shared helpers for Student Experience application tests."""

from __future__ import annotations

from typing import Any

from app.application.student_experience.student_experience_service import (
    StudentExperienceService,
)


class FakeTwinPort:
    def __init__(self, *, available: bool = True, student_id: str = "stu-1") -> None:
        self._available = available
        self.student_id = student_id
        self.calls: list[str] = []

    @property
    def component_id(self) -> str:
        return "student_twin"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        self.calls.append(f"learner:{student_id}")
        if student_id != self.student_id and student_id != "stu-1":
            return {
                "display_name": "Alex",
                "examination_label": "CPA",
                "preferences": {
                    "preferred_session_minutes": 45,
                    "preferred_study_days": ("Mon", "Wed"),
                    "reminder_enabled": True,
                },
                "goals": (
                    {"goal_id": "g1", "title": "Pass exam", "progress_ratio": 0.4},
                ),
                "account": {"email": "alex@example.com", "locale": "en"},
                "statistics": {
                    "total_study_minutes": 120,
                    "sessions_completed": 4,
                    "topics_mastered": 2,
                    "study_streak_days": 3,
                },
            }
        return {
            "display_name": "Alex",
            "examination_label": "CPA",
            "preferences": {
                "preferred_session_minutes": 45,
                "preferred_study_days": ("Mon", "Wed"),
                "reminder_enabled": True,
            },
            "goals": (
                {"goal_id": "g1", "title": "Pass exam", "progress_ratio": 0.4},
            ),
            "account": {"email": "alex@example.com", "locale": "en"},
            "statistics": {
                "total_study_minutes": 120,
                "sessions_completed": 4,
                "topics_mastered": 2,
                "study_streak_days": 3,
            },
        }

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        self.calls.append(f"readiness:{student_id}")
        return {
            "examination_label": "CPA",
            "exam_countdown_days": 42,
            "exam_readiness": 0.62,
            "readiness_score": 0.62,
        }

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        self.calls.append(f"insights:{student_id}")
        return {
            "completed_sessions": (
                {
                    "session_id": "s1",
                    "topic_title": "Tax basics",
                    "completed_at": "2026-07-01",
                    "study_minutes": 30,
                },
            ),
            "total_study_minutes": 120,
            "readiness_progression": (
                {"recorded_at": "2026-06-01", "exam_readiness": 0.4},
                {"recorded_at": "2026-07-01", "exam_readiness": 0.62},
            ),
            "mastered_topics": ("Intro",),
            "revision_history": ("Ethics review",),
            "recent_achievements": (
                {
                    "achievement_id": "a1",
                    "title": "First week streak",
                    "earned_at": "2026-07-01",
                },
            ),
            "sessions_completed": 4,
            "topics_mastered": 1,
            "study_streak_days": 3,
        }


class FakeAdaptivePort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self.calls: list[str] = []

    @property
    def component_id(self) -> str:
        return "adaptive_decision"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_todays_recommendation(self, student_id: str) -> dict[str, Any] | None:
        self.calls.append(f"recommend:{student_id}")
        return {
            "decision_id": "d1",
            "title": "Revise equity method",
            "topic_title": "Equity method",
            "summary": "High value for exam readiness",
            "estimated_minutes": 25,
            "expected_readiness_improvement": 0.03,
            "priority_band": "high",
            "mission_id": "m1",
            "explanation": {
                "topic_title": "Equity method",
                "reason_codes": ("high_roi", "exam_proximity"),
                "evidence_points": ("Recent practice scores dipped",),
                "expected_benefit": "Strengthen exam readiness",
                "priority_band": "high",
                "confidence": "strong",
            },
        }

    def get_revision_options(self, student_id: str) -> tuple[dict[str, Any], ...]:
        self.calls.append(f"revision:{student_id}")
        return (
            {
                "option_id": "r1",
                "topic_title": "Equity method",
                "priority_label": "high",
                "estimated_minutes": 25,
                "expected_benefit": "Protect weak recall",
                "explanation": {
                    "topic_title": "Equity method",
                    "reason_codes": ("low_retention",),
                    "evidence_points": ("Recall soft on this topic",),
                    "expected_benefit": "Protect weak recall",
                },
            },
            {
                "option_id": "r2",
                "topic_title": "Leases",
                "priority_label": "medium",
                "estimated_minutes": 20,
                "expected_benefit": "Steady progress",
            },
        )

    def get_decision_explanation(
        self, student_id: str, *, decision_id: str | None = None
    ) -> dict[str, Any] | None:
        self.calls.append(f"explain:{student_id}:{decision_id}")
        return {
            "topic_title": "Equity method",
            "reason_codes": ("high_roi",),
            "evidence_points": ("Strong educational return for time invested",),
            "expected_benefit": "Improve exam readiness",
            "priority_band": "high",
            "confidence": "strong",
        }


class FakeMissionPort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self.start_calls: list[tuple] = []

    @property
    def component_id(self) -> str:
        return "mission"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_todays_session(self, student_id: str) -> dict[str, Any] | None:
        return {
            "mission_id": "m1",
            "session_id": "sess-1",
            "topic_title": "Equity method",
            "estimated_minutes": 25,
            "status": "ready",
        }

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        self.start_calls.append((student_id, mission_id, session_id))
        return {
            "experience_session_id": "es-1",
            "mission_id": mission_id or "m1",
            "session_id": session_id or "sess-1",
            "topic_title": "Equity method",
            "estimated_minutes": 25,
            "started_at": "2026-07-18T10:00:00Z",
            "status": "in_progress",
        }

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {"session_id": session_id, "status": "in_progress"}


class FakeJourneyPort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available

    @property
    def component_id(self) -> str:
        return "learning_journey"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_journey_progress(self, student_id: str) -> dict[str, Any] | None:
        return {
            "overall_progress_ratio": 0.35,
            "estimated_completion_label": "About 8 weeks",
            "examination_label": "CPA",
            "current_topic_id": "t2",
            "current_topic_title": "Equity method",
        }

    def get_topic_list(self, student_id: str) -> tuple[dict[str, Any], ...]:
        return (
            {
                "topic_id": "t1",
                "title": "Intro",
                "status": "completed",
                "status_label": "Completed",
            },
            {
                "topic_id": "t2",
                "title": "Equity method",
                "status": "current",
                "status_label": "Current",
                "prerequisite_note": "Complete Intro first",
            },
            {
                "topic_id": "t3",
                "title": "Consolidations",
                "status": "upcoming",
                "status_label": "Upcoming",
                "prerequisite_note": "Finish Equity method first",
            },
        )


class FakeOrchestratorPort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self.acks: list[tuple] = []

    @property
    def component_id(self) -> str:
        return "learning_orchestrator"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_activity_status(self, student_id: str) -> dict[str, Any] | None:
        return {"status": "idle", "status_label": "No active learning activity"}

    def acknowledge_activity(
        self, student_id: str, *, activity_id: str
    ) -> dict[str, Any]:
        self.acks.append((student_id, activity_id))
        return {"activity_id": activity_id, "acknowledged": True}


def make_experience(**kwargs) -> StudentExperienceService:
    twin = kwargs.pop("student_twin", FakeTwinPort())
    adaptive = kwargs.pop("adaptive_decision", FakeAdaptivePort())
    mission = kwargs.pop("mission", FakeMissionPort())
    journey = kwargs.pop("learning_journey", FakeJourneyPort())
    orch = kwargs.pop("learning_orchestrator", FakeOrchestratorPort())
    return StudentExperienceService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
        learning_journey=journey,
        learning_orchestrator=orch,
        **kwargs,
    )
