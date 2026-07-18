"""HomeService — Student Home projection (what next, and why)."""

from __future__ import annotations

from typing import Any

from app.application.student_experience._snapshots import home_snapshot
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.exceptions import HomeError, PortUnavailable
from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.domain.student_experience.experience_session import StartSessionAction
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)
from app.domain.student_experience.student_home import StudentHome


class HomeService:
    """Project the Student Home surface from Twin / Adaptive / Mission ports.

    Projection only. No educational ownership.
    """

    def __init__(
        self,
        *,
        student_twin: StudentTwinPort | None = None,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        mission: MissionPort | None = None,
        explanation: ExplanationService | None = None,
    ) -> None:
        self._twin = student_twin
        self._adaptive = adaptive_decision
        self._mission = mission
        self._explanation = explanation or ExplanationService(
            adaptive_decision=adaptive_decision
        )

    def home(self, student_id: str) -> HomeSnapshot:
        """Build the Student Home projection for ``student_id``."""
        sid = _require_id(student_id)
        twin = self._require_twin()
        adaptive = self._require_adaptive()
        learner = twin.get_learner_summary(sid) or {}
        readiness = twin.get_readiness_summary(sid) or {}
        recommendation = adaptive.get_todays_recommendation(sid) or {}
        session = (
            self._mission.get_todays_session(sid)
            if self._mission is not None and self._mission.is_available()
            else None
        ) or {}

        try:
            explanation = None
            if recommendation:
                decision_id = recommendation.get("decision_id")
                explanation = self._explanation.from_opaque(
                    recommendation.get("explanation")
                    or adaptive.get_decision_explanation(
                        sid,
                        decision_id=(
                            None if decision_id is None else str(decision_id)
                        ),
                    )
                    or recommendation
                )
            home = StudentHome.create(
                sid,
                display_name=str(learner.get("display_name") or ""),
                examination_label=str(
                    learner.get("examination_label")
                    or readiness.get("examination_label")
                    or ""
                ),
                exam_countdown_days=_first_present_int(
                    readiness.get("exam_countdown_days"),
                    learner.get("exam_countdown_days"),
                ),
                exam_readiness=_first_present_float(
                    readiness.get("exam_readiness"),
                    readiness.get("readiness_score"),
                ),
                recommendation_title=translate_to_student_language(
                    str(
                        recommendation.get("title")
                        or recommendation.get("topic_title")
                        or ""
                    )
                ),
                recommendation_summary=translate_to_student_language(
                    str(
                        recommendation.get("summary")
                        or recommendation.get("rationale")
                        or ""
                    )
                ),
                estimated_study_minutes=_first_present_int(
                    recommendation.get("estimated_minutes"),
                    session.get("estimated_minutes"),
                ),
                expected_readiness_improvement=_first_present_float(
                    recommendation.get("expected_readiness_improvement"),
                    recommendation.get("expected_benefit_delta"),
                ),
                explanation=explanation,
                start_session=_start_action(session, recommendation),
            )
        except ValueError as exc:
            raise HomeError(str(exc)) from exc
        return home_snapshot(home)

    def _require_twin(self) -> StudentTwinPort:
        if self._twin is None or not self._twin.is_available():
            raise PortUnavailable("student_twin port unavailable")
        return self._twin

    def _require_adaptive(self) -> AdaptiveDecisionPort:
        if self._adaptive is None or not self._adaptive.is_available():
            raise PortUnavailable("adaptive_decision port unavailable")
        return self._adaptive


def _start_action(
    session: dict[str, Any], recommendation: dict[str, Any]
) -> StartSessionAction | None:
    mission_id = session.get("mission_id") or recommendation.get("mission_id")
    session_id = session.get("session_id")
    if not mission_id and not session_id:
        return StartSessionAction.create(enabled=False)
    return StartSessionAction.create(
        enabled=str(session.get("status") or "ready").lower()
        in {"ready", "in_progress", ""},
        mission_id=None if mission_id is None else str(mission_id),
        session_id=None if session_id is None else str(session_id),
        estimated_minutes=_optional_int(session.get("estimated_minutes")),
        topic_title=translate_to_student_language(
            str(session.get("topic_title") or recommendation.get("topic_title") or "")
        ),
    )


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HomeError("student_id must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _first_present_int(*values: Any) -> int | None:
    for value in values:
        if value is None or value == "":
            continue
        return int(value)
    return None


def _first_present_float(*values: Any) -> float | None:
    for value in values:
        if value is None or value == "":
            continue
        return float(value)
    return None
