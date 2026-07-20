"""Shared helpers for Session Experience production adapter tests."""

from __future__ import annotations

from typing import Any

from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.adaptive_adapter import SessionAdaptiveAdapter
from app.infrastructure.session.composition import (
    SessionExperienceComposition,
    build_production_session_experience,
)
from app.infrastructure.session.mission_adapter import SessionMissionAdapter
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.twin_adapter import SessionTwinAdapter

LEARNERS = tuple(f"sess-L{i}" for i in range(10))
SESSIONS = tuple(f"sess-{i}" for i in range(8))
ADAPTER_OPS = ("overview", "begin", "activity", "progress", "complete")


class RecordingRuntimeEngine:
    """Test double engine exposing opaque runtime methods."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []

    def get_session_overview_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("overview", (student_id,), {"session_id": session_id}))
        return {
            "objective": "Engine objective",
            "learning_goal": "Engine goal",
            "why_studying": "Engine rationale",
            "estimated_minutes": 25,
            "activity_count": 2,
            "topics": ("Engine topic",),
            "expected_readiness_improvement": 0.02,
            "status": "overview",
            "mission_id": "engine-m1",
            "session_id": session_id,
        }

    def begin_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("begin", (student_id,), {"session_id": session_id}))
        return {"session_id": session_id, "status": "in_progress", "engine": True}

    def get_runtime_snapshot_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("snapshot", (student_id,), {"session_id": session_id}))
        return {
            "activities_completed": 1,
            "activities_remaining": 1,
            "activities_total": 2,
            "estimated_remaining_minutes": 12,
            "current_topic": "Engine topic",
            "overall_progress": 0.5,
        }

    def record_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        self.calls.append(
            (
                "record",
                (student_id,),
                {
                    "session_id": session_id,
                    "activity_id": activity_id,
                    "response": response,
                },
            )
        )
        return {"recorded": True, "activity_id": activity_id, "engine": True}

    def complete_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("complete", (student_id,), {"session_id": session_id}))
        return {"session_id": session_id, "status": "completed", "engine": True}

    def get_reflection_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("reflection", (student_id,), {"session_id": session_id}))
        return {
            "key_insight": "Engine insight",
            "concept_confidence": "Steady",
            "suggested_improvement": "Revisit edge cases",
            "reflection_prompt": "What remains unclear?",
            "topic_title": "Engine topic",
        }

    def get_completion_summary_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append(("summary", (student_id,), {"session_id": session_id}))
        return {
            "topics_completed": ("Engine topic",),
            "time_studied_minutes": 22,
            "activities_completed": 2,
            "learning_insights": ("Engine insight",),
            "exam_readiness_change": 0.02,
        }


class RecordingActivityEngine:
    """Test double engine exposing opaque activity methods."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self._index = 1
        self._total = 2

    def get_current_activity_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append("current")
        return {
            "activity_id": f"eng-{self._index}",
            "question": f"Engine Q{self._index}",
            "context": "Engine context",
            "supporting_material": "Engine material",
            "hints": ("hint",),
            "activity_index": self._index,
            "activities_total": self._total,
            "topic_title": "Engine topic",
            "phase": "ready",
        }

    def submit_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        self.calls.append("submit")
        return {
            "activity_id": activity_id,
            "explanation": "Engine explanation",
            "phase": "explained",
            "activity_index": self._index,
            "activities_total": self._total,
            "next_action_label": "Continue",
        }

    def advance_activity_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self.calls.append("advance")
        if self._index >= self._total:
            return None
        self._index += 1
        return self.get_current_activity_opaque(student_id, session_id=session_id)

    def get_activity_progress_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        self.calls.append("progress")
        completed = self._index - 1
        return {
            "activities_completed": completed,
            "activities_remaining": self._total - completed,
            "activities_total": self._total,
            "estimated_remaining_minutes": (self._total - completed) * 8,
            "current_topic": "Engine topic",
            "overall_progress": completed / self._total,
        }


def make_composition(**kwargs) -> SessionExperienceComposition:
    return SessionExperienceComposition(**kwargs)


def make_seeded_service(student_id: str = "stu-1"):
    composition, service = build_production_session_experience(
        seed_demo_learners=False
    )
    composition.seed_learner(student_id, demo=True)
    return composition, service


def make_all_adapters(**kwargs):
    composition = make_composition(seed_demo_learners=False, **kwargs)
    return (
        composition.runtime,
        composition.activity,
        composition.mission,
        composition.twin,
        composition.adaptive,
    )


ADAPTER_TYPES = (
    (SessionRuntimeAdapter, "session_runtime"),
    (SessionActivityAdapter, "session_activity"),
    (SessionMissionAdapter, "session_mission"),
    (SessionTwinAdapter, "session_twin"),
    (SessionAdaptiveAdapter, "session_adaptive"),
)
