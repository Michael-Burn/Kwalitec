"""ProgressService — in-session progress projection."""

from __future__ import annotations

from typing import Any

from app.application.session_experience._snapshots import progress_snapshot
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.exceptions import PortUnavailable, ProgressError
from app.application.session_experience.ports.activity_engine_port import (
    ActivityEnginePort,
)
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.domain.session_experience.session_progress import SessionProgress


class ProgressService:
    """Project session progress from Runtime / Activity Engine ports.

    Projection only — does not calculate educational progress law.
    """

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        activity_engine: ActivityEnginePort | None = None,
    ) -> None:
        self._runtime = session_runtime
        self._activity = activity_engine

    def progress(self, student_id: str, *, session_id: str) -> ProgressSnapshot:
        """Build the progress projection for ``session_id``."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        activity_doc = {}
        if self._activity is not None and self._activity.is_available():
            activity_doc = (
                self._activity.get_activity_progress(sid, session_id=sess) or {}
            )
        runtime_doc = {}
        if self._runtime is not None and self._runtime.is_available():
            runtime_doc = (
                self._runtime.get_runtime_snapshot(sid, session_id=sess) or {}
            )
        if not activity_doc and not runtime_doc:
            if self._runtime is None and self._activity is None:
                raise PortUnavailable(
                    "session_runtime and activity_engine ports unavailable"
                )
            raise ProgressError("no progress facts available from ports")
        try:
            domain = SessionProgress.create(
                sess,
                activities_completed=int(
                    activity_doc.get("activities_completed")
                    or runtime_doc.get("activities_completed")
                    or 0
                ),
                activities_remaining=int(
                    activity_doc.get("activities_remaining")
                    or runtime_doc.get("activities_remaining")
                    or 0
                ),
                activities_total=_optional_int(
                    activity_doc.get("activities_total")
                    or runtime_doc.get("activities_total")
                ),
                estimated_remaining_minutes=_optional_int(
                    activity_doc.get("estimated_remaining_minutes")
                    or runtime_doc.get("estimated_remaining_minutes")
                ),
                current_topic=str(
                    activity_doc.get("current_topic")
                    or runtime_doc.get("current_topic")
                    or runtime_doc.get("topic_title")
                    or ""
                ),
                overall_progress=_optional_float(
                    activity_doc.get("overall_progress")
                    or runtime_doc.get("overall_progress")
                ),
            )
        except ValueError as exc:
            raise ProgressError(str(exc)) from exc
        return progress_snapshot(domain)


def _require_id(value: str, field: str = "student_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProgressError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
