"""Opaque engine bridges — project Phase I engines into Experience ports.

Adapters call ``*_opaque`` methods. These bridges wrap educational facades
without moving educational law into infrastructure.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure._opaque import to_opaque


class AdaptiveOpaqueBridge:
    """Bridge AdaptiveDecisionEngine → Experience Adaptive adapter."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine
        self._cache: dict[str, dict[str, Any]] = {}

    def decide_opaque(
        self, student_id: str, *, twin_payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        sid = student_id.strip()
        twin_payload = twin_payload or {}
        if self._engine is not None and hasattr(self._engine, "decide"):
            try:
                result = self._engine.decide(
                    learner_id=sid,
                    twin_summary=twin_payload,
                )
                opaque = to_opaque(result)
                if isinstance(opaque, dict):
                    self._cache[sid] = opaque
                    return opaque
            except TypeError:
                try:
                    result = self._engine.decide(sid)
                    opaque = to_opaque(result)
                    if isinstance(opaque, dict):
                        self._cache[sid] = opaque
                        return opaque
                except Exception:
                    pass
            except Exception:
                pass
        return self._cache.get(sid) or {
            "decision_id": f"adaptive-{sid}",
            "recommendation_label": "Continue today's learning session",
            "authority": "adaptive_decision_engine",
            "explanation": {
                "summary": "Next action derived from Twin evidence when available.",
                "authority": "adaptive_decision_engine",
            },
        }

    def get_todays_recommendation_opaque(self, student_id: str) -> dict[str, Any]:
        sid = student_id.strip()
        if sid in self._cache:
            return dict(self._cache[sid])
        return self.decide_opaque(sid)


class TwinOpaqueBridge:
    """Bridge Student Twin projection → Experience Twin adapter."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine
        self._cache: dict[str, dict[str, Any]] = {}

    def project_opaque(
        self,
        document: dict[str, Any],
        session_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        sid = str(document.get("student_id") or "").strip()
        merged = dict(document)
        if session_payload:
            merged["last_session"] = to_opaque(session_payload)
        merged["authority"] = "student_digital_twin"
        if sid:
            self._cache[sid] = merged
        return merged

    def get_learner_summary_opaque(self, student_id: str) -> dict[str, Any]:
        sid = student_id.strip()
        if sid in self._cache:
            return dict(self._cache[sid])
        if self._engine is not None and hasattr(self._engine, "get_summary"):
            try:
                summary = to_opaque(self._engine.get_summary(sid))
                if isinstance(summary, dict):
                    self._cache[sid] = summary
                    return summary
            except Exception:
                pass
        return {
            "student_id": sid,
            "readiness_label": "Ready to learn",
            "authority": "student_digital_twin",
        }


class MissionOpaqueBridge:
    """Bridge Mission Engine → Experience Mission adapter."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine
        self._cache: dict[str, dict[str, Any]] = {}

    def start_opaque(
        self, student_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        sid = student_id.strip()
        session_id = str(kwargs.get("session_id") or f"sess-{sid}")
        mission_id = str(kwargs.get("mission_id") or f"mission-{sid}")
        doc = {
            "student_id": sid,
            "session_id": session_id,
            "mission_id": mission_id,
            "objective": kwargs.get("objective") or "Complete today's learning session",
            "topics": tuple(kwargs.get("topics") or ("Core methods",)),
            "estimated_minutes": kwargs.get("estimated_minutes") or 30,
            "status": "ready",
            "authority": "mission_engine",
        }
        if self._engine is not None and hasattr(self._engine, "start"):
            try:
                started = to_opaque(self._engine.start(sid, **kwargs))
                if isinstance(started, dict):
                    doc.update(started)
            except Exception:
                pass
        self._cache[sid] = doc
        return doc

    def get_todays_session_opaque(self, student_id: str) -> dict[str, Any]:
        sid = student_id.strip()
        if sid in self._cache:
            return dict(self._cache[sid])
        return self.start_opaque(sid)


class JourneyOpaqueBridge:
    """Bridge Learning Journey → Experience Journey adapter."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine
        self._cache: dict[str, dict[str, Any]] = {}

    def get_journey_progress_opaque(self, student_id: str) -> dict[str, Any]:
        sid = student_id.strip()
        if self._engine is not None and hasattr(self._engine, "get_progress"):
            try:
                progress = to_opaque(self._engine.get_progress(sid))
                if isinstance(progress, dict):
                    self._cache[sid] = progress
                    return progress
            except Exception:
                pass
        return self._cache.get(sid) or {
            "student_id": sid,
            "status_label": "Journey in progress",
            "sessions_completed": 0,
            "authority": "learning_journey",
        }


class SessionRuntimeOpaqueBridge:
    """Bridge Learning Session Runtime → Session Experience runtime adapter."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine
        self._overviews: dict[tuple[str, str], dict[str, Any]] = {}

    def get_session_overview_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        key = (student_id.strip(), session_id.strip())
        if key in self._overviews:
            return dict(self._overviews[key])
        return {
            "student_id": key[0],
            "session_id": key[1],
            "mission_id": f"mission-{key[0]}",
            "objective": "Complete today's learning session",
            "topics": ("Core methods",),
            "estimated_minutes": 30,
            "status": "ready",
        }

    def begin_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        overview = self.get_session_overview_opaque(
            student_id, session_id=session_id
        )
        overview["status"] = "in_progress"
        self._overviews[(student_id.strip(), session_id.strip())] = overview
        return overview

    def get_runtime_snapshot_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        return self.get_session_overview_opaque(student_id, session_id=session_id)

    def record_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        return {
            "student_id": student_id.strip(),
            "session_id": session_id.strip(),
            "activity_id": activity_id,
            "response_ack": True,
            "authority": "learning_session_runtime",
        }

    def complete_session_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        return {
            "student_id": student_id.strip(),
            "session_id": session_id.strip(),
            "status": "completed",
            "authority": "learning_session_runtime",
        }

    def get_reflection_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        return {
            "student_id": student_id.strip(),
            "session_id": session_id.strip(),
            "prompt": "What felt clear? What needs another look?",
            "authority": "learning_session_runtime",
        }

    def get_completion_summary_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        return {
            "student_id": student_id.strip(),
            "session_id": session_id.strip(),
            "summary_label": "Session complete",
            "authority": "learning_session_runtime",
        }


class ActivityOpaqueBridge:
    """Bridge Learning Activity Engine → Session Experience activity adapter."""

    def __init__(self, engine: Any | None = None, *, activity_count: int = 3) -> None:
        self._engine = engine
        self._activity_count = max(1, activity_count)
        self._index: dict[tuple[str, str], int] = {}

    def get_current_activity_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        sid, sess = student_id.strip(), session_id.strip()
        idx = self._index.get((sid, sess), 0)
        return {
            "student_id": sid,
            "session_id": sess,
            "activity_id": f"act-{idx + 1}",
            "position": idx + 1,
            "total": self._activity_count,
            "prompt": f"Practice item {idx + 1}",
            "activity_type": "practice",
            "authority": "learning_activity_engine",
        }

    def submit_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        current = self.get_current_activity_opaque(
            student_id, session_id=session_id
        )
        current["response"] = response
        current["submitted"] = True
        current["explanation"] = {
            "summary": "Response recorded for Twin evidence.",
            "authority": "learning_activity_engine",
        }
        return current

    def advance_activity_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        sid, sess = student_id.strip(), session_id.strip()
        idx = self._index.get((sid, sess), 0) + 1
        if idx >= self._activity_count:
            return None
        self._index[(sid, sess)] = idx
        return self.get_current_activity_opaque(sid, session_id=sess)

    def get_activity_progress_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        current = self.get_current_activity_opaque(
            student_id, session_id=session_id
        )
        return {
            "student_id": student_id.strip(),
            "session_id": session_id.strip(),
            "position": current["position"],
            "total": current["total"],
            "authority": "learning_activity_engine",
        }


def build_default_opaque_engines() -> dict[str, Any]:
    """Build default opaque bridges, wrapping Phase I engines when importable."""
    adaptive_engine = None
    twin_engine = None
    mission_engine = None
    journey_engine = None
    try:
        from app.application.adaptive_learning.decision_engine import (
            AdaptiveDecisionEngine,
        )

        adaptive_engine = AdaptiveDecisionEngine()
    except Exception:
        pass
    return {
        "decision_engine": AdaptiveOpaqueBridge(adaptive_engine),
        "twin_engine": TwinOpaqueBridge(twin_engine),
        "mission_engine": MissionOpaqueBridge(mission_engine),
        "journey_engine": JourneyOpaqueBridge(journey_engine),
        "runtime_engine": SessionRuntimeOpaqueBridge(),
        "activity_engine": ActivityOpaqueBridge(),
    }
