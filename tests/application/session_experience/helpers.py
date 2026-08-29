"""Shared helpers / fake ports for Learning Session Experience application tests."""

from __future__ import annotations

from typing import Any

from app.application.session_experience.facade import SessionExperienceService


class FakeSessionRuntimePort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self.begin_calls: list[tuple] = []
        self.response_calls: list[tuple] = []
        self.complete_calls: list[str] = []
        self.reflection_note_calls: list[tuple] = []

    @property
    def component_id(self) -> str:
        return "session_runtime"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_session_overview(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {
            "objective": "Strengthen equity method recall",
            "learning_goal": "Explain influence vs control",
            "why_studying": "This Session is today's recommended next step.",
            "estimated_minutes": 30,
            "activity_count": 3,
            "topics": ("Equity method", "Associates"),
            "expected_readiness_improvement": 0.03,
            "status": "overview",
            "mission_id": "m1",
        }

    def begin_session(self, student_id: str, *, session_id: str) -> dict[str, Any]:
        self.begin_calls.append((student_id, session_id))
        return {"session_id": session_id, "status": "in_progress"}

    def pause_session(self, student_id: str, *, session_id: str) -> dict[str, Any]:
        return {"session_id": session_id, "status": "paused", "phase": "paused"}

    def resume_session(self, student_id: str, *, session_id: str) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "status": "in_progress",
            "phase": "active",
            "active_surface": "activity",
        }

    def request_finish(self, student_id: str, *, session_id: str) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "status": "ready_to_finish",
            "phase": "ready_to_finish",
            "finish_review_required": True,
        }

    def get_runtime_snapshot(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {
            "activities_completed": 1,
            "activities_remaining": 2,
            "activities_total": 3,
            "estimated_remaining_minutes": 20,
            "current_topic": "Equity method",
            "overall_progress": 1 / 3,
            "active_surface": "activity",
            "checklist": [
                {"id": "read", "label": "Read today's topic", "done": False},
            ],
        }

    def record_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
        scored_correct: bool | None = None,
        structured: bool = False,
        score_payload: dict | None = None,
    ) -> dict[str, Any]:
        self.response_calls.append(
            (student_id, session_id, activity_id, response, scored_correct)
        )
        return {
            "recorded": True,
            "activity_id": activity_id,
            "scored_correct": scored_correct,
        }

    def update_checklist(
        self,
        student_id: str,
        *,
        session_id: str,
        item_id: str,
        done: bool,
    ) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "student_id": student_id,
            "item_id": item_id,
            "done": done,
        }

    def save_surface(
        self,
        student_id: str,
        *,
        session_id: str,
        surface: str,
    ) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "student_id": student_id,
            "active_surface": surface,
        }

    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str,
        finish_verdict: str | None = None,
        finish_notes: str | None = None,
    ) -> dict[str, Any]:
        self.complete_calls.append(session_id)
        return {
            "session_id": session_id,
            "status": "completed",
            "mission_completed": False,
            "finish_review": (
                {"verdict": finish_verdict, "notes": finish_notes or ""}
                if finish_verdict
                else None
            ),
        }

    def get_reflection(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {
            "key_insight": "Influence drives equity accounting",
            "concept_confidence": "Growing comfort with ownership thresholds",
            "suggested_improvement": "Practice borderline influence cases",
            "reflection_prompt": "What still feels unclear about influence?",
            "topic_title": "Equity method",
        }

    def record_reflection_note(
        self,
        student_id: str,
        *,
        session_id: str,
        note: str,
        confidence_rating: int | None = None,
    ) -> dict[str, Any]:
        self.reflection_note_calls.append(
            (student_id, session_id, note, confidence_rating)
        )
        return {
            "recorded": True,
            "session_id": session_id,
            "confidence_rating": confidence_rating,
        }

    def get_completion_summary(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {
            "topics_completed": ("Equity method",),
            "time_studied_minutes": 28,
            "activities_completed": 3,
            "learning_insights": ("Influence thresholds matter",),
            "exam_readiness_change": 0.03,
        }


class FakeActivityEnginePort:
    def __init__(self, *, available: bool = True, activities: int = 3) -> None:
        self._available = available
        self._activities = max(1, activities)
        self._index = 1
        self.submit_calls: list[tuple] = []

    @property
    def component_id(self) -> str:
        return "activity_engine"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_current_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {
            "activity_id": f"act-{self._index}",
            "question": f"Question {self._index}: explain equity method use",
            "context": "Associate investment scenario",
            "supporting_material": "Ownership between 20% and 50%",
            "hints": ("Consider significant influence",),
            "activity_index": self._index,
            "activities_total": self._activities,
            "topic_title": "Equity method",
            "phase": "ready",
        }

    def submit_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        self.submit_calls.append((student_id, session_id, activity_id, response))
        return {
            "activity_id": activity_id,
            "explanation": "Significant influence usually indicates equity method.",
            "phase": "explained",
            "activity_index": self._index,
            "activities_total": self._activities,
            "question": f"Question {self._index}",
            "next_action_label": "Continue",
        }

    def advance_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        if self._index >= self._activities:
            return None
        self._index += 1
        return self.get_current_activity(student_id, session_id=session_id)

    def get_activity_progress(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        completed = self._index - 1
        remaining = self._activities - completed
        return {
            "activities_completed": completed,
            "activities_remaining": remaining,
            "activities_total": self._activities,
            "estimated_remaining_minutes": remaining * 8,
            "current_topic": "Equity method",
            "overall_progress": completed / self._activities,
        }


class FakeMissionPort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available

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
            "estimated_minutes": 30,
            "status": "ready",
            "objective": "Strengthen equity method recall",
            "topics": ("Equity method",),
        }

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        return {"session_id": session_id, "status": "ready", "mission_id": "m1"}


class FakeTwinPort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available

    @property
    def component_id(self) -> str:
        return "student_twin"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        return {"exam_readiness": 0.65, "examination_label": "CPA"}

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        return {"recent_insights": ("Consistent practice helps retention",)}


class FakeAdaptivePort:
    def __init__(self, *, available: bool = True) -> None:
        self._available = available

    @property
    def component_id(self) -> str:
        return "adaptive_decision"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def get_todays_recommendation(self, student_id: str) -> dict[str, Any] | None:
        return {
            "title": "Revise consolidations",
            "topic_title": "Consolidations",
            "estimated_minutes": 25,
        }


def make_session_experience(**kwargs) -> SessionExperienceService:
    return SessionExperienceService(
        session_runtime=kwargs.pop("session_runtime", FakeSessionRuntimePort()),
        activity_engine=kwargs.pop("activity_engine", FakeActivityEnginePort()),
        mission=kwargs.pop("mission", FakeMissionPort()),
        student_twin=kwargs.pop("student_twin", FakeTwinPort()),
        adaptive_decision=kwargs.pop("adaptive_decision", FakeAdaptivePort()),
        **kwargs,
    )
