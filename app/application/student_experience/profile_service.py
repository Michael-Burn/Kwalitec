"""ProfileService — Profile experience projection."""

from __future__ import annotations

from typing import Any

from app.application.educational_state import EducationalStateService
from app.application.student_experience._snapshots import profile_snapshot
from app.application.student_experience.dto.profile_snapshot import ProfileSnapshot
from app.application.student_experience.exceptions import (
    PortUnavailable,
    ProfileError,
)
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.domain.student_experience.profile_projection import (
    AccountSettings,
    LearningGoal,
    LearningStatistics,
    ProfileProjection,
    StudyPreferences,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)


class ProfileService:
    """Project the Profile surface from shared Educational State.

    Prefer EducationalStateService so Settings/Profile share the same Twin
    learner / readiness / insights snapshot as Dashboard and Analytics.
    Account settings remain presentation flags only — no auth/persistence.
    """

    def __init__(
        self,
        *,
        student_twin: StudentTwinPort | None = None,
        educational_state: EducationalStateService | None = None,
    ) -> None:
        self._twin = student_twin
        self._educational_state = educational_state

    def profile(self, student_id: str) -> ProfileSnapshot:
        """Build the Profile projection for ``student_id``."""
        sid = _require_id(student_id)
        learner, readiness, insights = self._facts_for(sid)

        prefs_raw = learner.get("preferences") or {}
        account_raw = learner.get("account") or {}
        goals_raw = learner.get("goals") or ()
        stats_raw = learner.get("statistics") or insights

        try:
            preferences = StudyPreferences.create(
                preferred_session_minutes=_optional_int(
                    prefs_raw.get("preferred_session_minutes")
                ),
                preferred_study_days=tuple(
                    str(d) for d in (prefs_raw.get("preferred_study_days") or ())
                ),
                reminder_enabled=bool(prefs_raw.get("reminder_enabled", False)),
                quiet_hours_label=str(prefs_raw.get("quiet_hours_label") or ""),
            )
            statistics = LearningStatistics.create(
                total_study_minutes=int(stats_raw.get("total_study_minutes") or 0),
                sessions_completed=int(stats_raw.get("sessions_completed") or 0),
                topics_mastered=int(
                    stats_raw.get("topics_mastered")
                    or len(insights.get("mastered_topics") or ())
                ),
                current_exam_readiness=_optional_float(
                    readiness.get("exam_readiness")
                    or readiness.get("readiness_score")
                    or stats_raw.get("current_exam_readiness")
                ),
                study_streak_days=int(stats_raw.get("study_streak_days") or 0),
            )
            goals = tuple(
                LearningGoal.create(
                    str(g.get("goal_id") or g.get("id") or f"g-{i}"),
                    translate_to_student_language(
                        str(g.get("title") or "Goal")
                    ),
                    target_label=translate_to_student_language(
                        str(g.get("target_label") or "")
                    ),
                    progress_ratio=float(g.get("progress_ratio") or 0.0),
                )
                for i, g in enumerate(goals_raw)
            )
            account = AccountSettings.create(
                email=str(account_raw.get("email") or learner.get("email") or ""),
                notifications_enabled=bool(
                    account_raw.get("notifications_enabled", True)
                ),
                locale=str(account_raw.get("locale") or ""),
                timezone=str(account_raw.get("timezone") or ""),
            )
            projection = ProfileProjection.create(
                sid,
                display_name=str(learner.get("display_name") or ""),
                examination_label=str(
                    learner.get("examination_label")
                    or readiness.get("examination_label")
                    or ""
                ),
                preferences=preferences,
                statistics=statistics,
                goals=goals,
                account=account,
            )
        except ValueError as exc:
            raise ProfileError(str(exc)) from exc
        return profile_snapshot(projection)

    def _facts_for(
        self, student_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        if self._educational_state is not None:
            state = self._educational_state.load(student_id)
            if not state.twin_available:
                raise PortUnavailable("student_twin port unavailable")
            return (
                dict(state.learner_summary),
                dict(state.readiness_summary),
                dict(state.learning_insights),
            )
        twin = self._require_twin()
        return (
            dict(twin.get_learner_summary(student_id) or {}),
            dict(twin.get_readiness_summary(student_id) or {}),
            dict(twin.get_learning_insights(student_id) or {}),
        )

    def _require_twin(self) -> StudentTwinPort:
        if self._twin is None or not self._twin.is_available():
            raise PortUnavailable("student_twin port unavailable")
        return self._twin


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProfileError("student_id must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
