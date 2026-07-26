"""HistoryService — History experience projection (no raw event logs)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from app.application.educational_state import (
    EducationalStateService,
    EducationalStateSnapshot,
)
from app.application.student_experience._snapshots import history_snapshot
from app.application.student_experience.dto.history_snapshot import HistorySnapshot
from app.application.student_experience.exceptions import (
    HistoryError,
    PortUnavailable,
)
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_HISTORY_HEADER,
    RecommendationCommitmentService,
)
from app.domain.student_experience.history_projection import (
    AchievementCard,
    CompletedSessionCard,
    HistoryProjection,
    ReadinessPoint,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)
from app.domain.student_experience.student_home import readiness_band_label


class HistoryService:
    """Project Analytics/History from Runtime A History Bridge or Twin insights.

    Never surfaces raw event logs. Never recomputes mastery independently.
    When ``history_read`` is wired, projects exclusively from Runtime A.
    """

    def __init__(
        self,
        *,
        student_twin: StudentTwinPort | None = None,
        educational_state: EducationalStateService | None = None,
        history_read: Any | None = None,
    ) -> None:
        self._twin = student_twin
        self._educational_state = educational_state
        self._history_read = history_read

    def history(
        self,
        student_id: str,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> HistorySnapshot:
        """Build the History projection for ``student_id``."""
        sid = _require_id(student_id)
        if self._history_read is not None:
            snap = self._history_from_bridge(sid, limit=limit, offset=offset)
        else:
            snap = self._history_from_insights(sid)
        return self._with_recommendation_narrative(sid, snap)

    def _history_from_insights(self, sid: str) -> HistorySnapshot:
        insights = dict(self._insights_for(sid))
        # Reject raw event dumps if an adapter mistakenly supplies them.
        if "events" in insights or "raw_events" in insights or "event_log" in insights:
            insights = {
                k: v
                for k, v in insights.items()
                if k not in {"events", "raw_events", "event_log"}
            }

        sessions = tuple(
            CompletedSessionCard.create(
                str(s.get("session_id") or s.get("id") or f"s-{i}"),
                translate_to_student_language(
                    str(s.get("topic_title") or s.get("title") or "Session")
                ),
                completed_at=str(s.get("completed_at") or ""),
                study_minutes=int(s.get("study_minutes") or 0),
            )
            for i, s in enumerate(insights.get("completed_sessions") or ())
        )
        progression = tuple(
            ReadinessPoint.create(
                str(p.get("recorded_at") or p.get("at") or f"t-{i}"),
                float(
                    p.get("exam_readiness")
                    if p.get("exam_readiness") is not None
                    else p.get("readiness_score") or 0.0
                ),
                label=str(
                    p.get("label")
                    or readiness_band_label(
                        float(
                            p.get("exam_readiness")
                            if p.get("exam_readiness") is not None
                            else p.get("readiness_score") or 0.0
                        )
                    )
                ),
            )
            for i, p in enumerate(insights.get("readiness_progression") or ())
        )
        achievements = tuple(
            AchievementCard.create(
                str(a.get("achievement_id") or a.get("id") or f"a-{i}"),
                translate_to_student_language(
                    str(a.get("title") or "Achievement")
                ),
                earned_at=str(a.get("earned_at") or ""),
                description=translate_to_student_language(
                    str(a.get("description") or "")
                ),
            )
            for i, a in enumerate(insights.get("recent_achievements") or ())
        )
        try:
            projection = HistoryProjection.create(
                sid,
                completed_sessions=sessions,
                total_study_minutes=_optional_int(
                    insights.get("total_study_minutes")
                ),
                readiness_progression=progression,
                mastered_topics=tuple(
                    translate_to_student_language(str(t))
                    for t in (insights.get("mastered_topics") or ())
                ),
                revision_history=tuple(
                    translate_to_student_language(str(r))
                    for r in (insights.get("revision_history") or ())
                ),
                recent_achievements=achievements,
            )
        except ValueError as exc:
            raise HistoryError(str(exc)) from exc
        return history_snapshot(projection)

    def _history_from_bridge(
        self,
        student_id: str,
        *,
        limit: int,
        offset: int,
    ) -> HistorySnapshot:
        """History Read Bridge path — Runtime A only; never Twin demo."""
        bridge = self._history_read
        result = bridge.project_history(
            student_id, limit=limit, offset=offset
        )
        payload = getattr(result, "value", None)
        if not isinstance(payload, dict):
            payload = {}
        # Strip forbidden raw event keys if present.
        insights = {
            k: v
            for k, v in payload.items()
            if k not in {"events", "raw_events", "event_log"}
        }

        sessions = tuple(
            CompletedSessionCard.create(
                str(s.get("session_id") or s.get("mission_id") or f"s-{i}"),
                translate_to_student_language(
                    str(s.get("topic_title") or s.get("title") or "Session")
                ),
                completed_at=str(s.get("completed_at") or ""),
                study_minutes=int(s.get("study_minutes") or 0),
            )
            for i, s in enumerate(insights.get("completed_sessions") or ())
        )
        # Explicit null readiness series → empty progression (never fabricate).
        readiness_raw = insights.get("readiness_progression")
        progression = tuple(
            ReadinessPoint.create(
                str(p.get("recorded_at") or p.get("at") or f"t-{i}"),
                float(
                    p.get("exam_readiness")
                    if p.get("exam_readiness") is not None
                    else p.get("readiness_score") or 0.0
                ),
                label=str(
                    p.get("label")
                    or readiness_band_label(
                        float(
                            p.get("exam_readiness")
                            if p.get("exam_readiness") is not None
                            else p.get("readiness_score") or 0.0
                        )
                    )
                ),
            )
            for i, p in enumerate(readiness_raw or ())
        )
        achievements = tuple(
            AchievementCard.create(
                str(a.get("achievement_id") or a.get("id") or f"a-{i}"),
                translate_to_student_language(
                    str(a.get("title") or "Achievement")
                ),
                earned_at=str(a.get("earned_at") or ""),
                description=translate_to_student_language(
                    str(a.get("description") or "")
                ),
            )
            for i, a in enumerate(insights.get("recent_achievements") or ())
        )
        try:
            projection = HistoryProjection.create(
                student_id,
                completed_sessions=sessions,
                total_study_minutes=_optional_int(
                    insights.get("total_study_minutes")
                ),
                readiness_progression=progression,
                mastered_topics=tuple(
                    translate_to_student_language(str(t))
                    for t in (insights.get("mastered_topics") or ())
                ),
                revision_history=tuple(
                    translate_to_student_language(str(r))
                    for r in (insights.get("revision_history") or ())
                ),
                recent_achievements=achievements,
            )
        except ValueError as exc:
            raise HistoryError(str(exc)) from exc
        return history_snapshot(projection)

    def _with_recommendation_narrative(
        self, student_id: str, snap: HistorySnapshot
    ) -> HistorySnapshot:
        """Attach EP-008.3 educational narrative (fail-open)."""
        try:
            uid = int(student_id)
        except (TypeError, ValueError):
            return snap
        try:
            entries = RecommendationCommitmentService.narrative_entries(uid)
            if not entries:
                return snap
            return replace(
                snap,
                recommendation_narrative=entries,
                recommendation_narrative_header=CONTINUITY_HISTORY_HEADER,
            )
        except Exception:  # noqa: BLE001 — presentation fail-open
            return snap

    def _insights_for(self, student_id: str) -> dict[str, Any]:
        if self._educational_state is not None:
            state = self._educational_state.load(student_id)
            if not state.twin_available:
                raise PortUnavailable("student_twin port unavailable")
            return state.learning_insights
        twin = self._require_twin()
        return twin.get_learning_insights(student_id) or {}

    def _require_twin(self) -> StudentTwinPort:
        if self._twin is None or not self._twin.is_available():
            raise PortUnavailable("student_twin port unavailable")
        return self._twin

    # Retained for type checkers / tests that introspect Twin wiring.
    def _state_snapshot(self, student_id: str) -> EducationalStateSnapshot | None:
        if self._educational_state is None:
            return None
        return self._educational_state.load(student_id)


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HistoryError("student_id must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
