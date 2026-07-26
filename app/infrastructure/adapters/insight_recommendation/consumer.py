"""Project Twin + Planner + Readiness into insight inputs (EP-001.4).

Communication-layer projection only. Never invents mastery, readiness scores,
or mission plans.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import CanonicalLearnerState
from app.infrastructure.adapters.insight_recommendation.contracts import (
    REASON_INVALID_STUDENT_ID,
    REASON_PLANNER_UNAVAILABLE,
    REASON_READINESS_UNAVAILABLE,
    REASON_STATE_UNAVAILABLE,
    StudyInsightInputs,
)


def _payload(block: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if not isinstance(block, Mapping):
        return {}
    payload = block.get("payload")
    return payload if isinstance(payload, Mapping) else {}


def _available(block: Mapping[str, Any] | None) -> bool:
    if not isinstance(block, Mapping):
        return False
    return block.get("availability") == AVAILABILITY_AVAILABLE


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _rows(value: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        return ()
    rows: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, Mapping):
            rows.append(dict(item))
    return tuple(rows)


def _unavailable_inputs(
    *,
    student_id: str,
    reason: str,
    foundation_version: str = "",
    twin_id: str = "",
    as_of: str | None = None,
) -> StudyInsightInputs:
    return StudyInsightInputs(
        student_id=student_id,
        as_of=as_of,
        foundation_version=foundation_version,
        twin_id=twin_id,
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason=reason,
        lifecycle_stage="",
        examination_label="",
        exam_countdown_days=None,
        current_streak=None,
        longest_streak=None,
        consistency_label="",
        mission_completed_count=0,
        mission_missed_count=0,
        evidence_attempt_count=0,
        topics_started=None,
        topics_mastered=None,
        total_topics=None,
        planner_available=False,
        readiness_available=False,
        planner_missions=(),
        planner_revision_priorities=(),
        recommended_workload={},
        readiness_score=None,
        confidence_level="",
        strongest_areas=(),
        weakest_areas=(),
        readiness_drivers=(),
        recommended_next_actions=(),
        provenance_refs=(),
        limitations_codes=(reason,),
    )


class CanonicalInsightConsumer:
    """Maps CanonicalLearnerState (+ optional planner/readiness) → insight inputs."""

    def project(
        self,
        state: CanonicalLearnerState | None,
        *,
        daily_plan: Mapping[str, Any] | None = None,
        readiness_intelligence: Mapping[str, Any] | None = None,
    ) -> StudyInsightInputs:
        if state is None:
            return _unavailable_inputs(
                student_id="",
                reason=REASON_STATE_UNAVAILABLE,
            )
        student_id = (state.student_id or "").strip()
        if not student_id:
            return _unavailable_inputs(
                student_id="",
                reason=REASON_INVALID_STUDENT_ID,
                foundation_version=state.foundation_version,
                twin_id=state.twin_id,
                as_of=state.as_of,
            )
        if state.availability != AVAILABILITY_AVAILABLE:
            return _unavailable_inputs(
                student_id=student_id,
                reason=state.unavailable_reason or REASON_STATE_UNAVAILABLE,
                foundation_version=state.foundation_version,
                twin_id=state.twin_id,
                as_of=state.as_of,
            )

        study = _payload(state.study_state) if _available(state.study_state) else {}
        readiness_overall = study.get("readiness_overall")
        if not isinstance(readiness_overall, Mapping):
            readiness_overall = {}

        streaks = _payload(state.streaks) if _available(state.streaks) else {}
        consistency = (
            _payload(state.study_consistency)
            if _available(state.study_consistency)
            else {}
        )
        missions = (
            _payload(state.mission_completion)
            if _available(state.mission_completion)
            else {}
        )
        evidence = (
            _payload(state.learning_evidence)
            if _available(state.learning_evidence)
            else {}
        )

        limitations: list[str] = list(state.limitations_codes or ())
        planner_available = False
        planner_missions: tuple[dict[str, Any], ...] = ()
        planner_revisions: tuple[dict[str, Any], ...] = ()
        workload: dict[str, Any] = {}

        if isinstance(daily_plan, Mapping) and daily_plan.get(
            "availability"
        ) == AVAILABILITY_AVAILABLE:
            planner_available = True
            planner_missions = _rows(daily_plan.get("today_missions"))
            planner_revisions = _rows(daily_plan.get("revision_priorities"))
            raw_workload = daily_plan.get("recommended_workload")
            if isinstance(raw_workload, Mapping):
                workload = dict(raw_workload)
        else:
            limitations.append(REASON_PLANNER_UNAVAILABLE)

        readiness_available = False
        readiness_score: float | None = None
        confidence_level = ""
        strongest: tuple[dict[str, Any], ...] = ()
        weakest: tuple[dict[str, Any], ...] = ()
        drivers: tuple[dict[str, Any], ...] = ()
        next_actions: tuple[dict[str, Any], ...] = ()

        if isinstance(readiness_intelligence, Mapping) and readiness_intelligence.get(
            "availability"
        ) == AVAILABILITY_AVAILABLE:
            readiness_available = True
            readiness_score = _as_float(readiness_intelligence.get("readiness_score"))
            confidence_level = str(
                readiness_intelligence.get("confidence_level") or ""
            ).strip()
            strongest = _rows(readiness_intelligence.get("strongest_areas"))
            weakest = _rows(readiness_intelligence.get("weakest_areas"))
            drivers = _rows(readiness_intelligence.get("readiness_drivers"))
            next_actions = _rows(
                readiness_intelligence.get("recommended_next_actions")
            )
        else:
            limitations.append(REASON_READINESS_UNAVAILABLE)
            # Prefer CLS readiness pass-through for score context only when
            # intelligence package is unavailable — never invent confidence.
            readiness_score = _as_float(readiness_overall.get("score"))

        provenance = list(state.provenance_refs or ())
        provenance.extend(
            [
                "insight_recommendation",
                "canonical_learner_state",
            ]
        )
        if planner_available:
            provenance.append("adaptive_study_planner")
        if readiness_available:
            provenance.append("readiness_intelligence")

        # Preserve order, drop empties / duplicates.
        seen: set[str] = set()
        provenance_refs: list[str] = []
        for item in provenance:
            key = str(item).strip()
            if key and key not in seen:
                seen.add(key)
                provenance_refs.append(key)

        return StudyInsightInputs(
            student_id=student_id,
            as_of=state.as_of,
            foundation_version=state.foundation_version,
            twin_id=state.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            lifecycle_stage=str(study.get("lifecycle_stage") or "").strip(),
            examination_label=str(study.get("examination_label") or "").strip(),
            exam_countdown_days=(
                _as_int(study["exam_countdown_days"])
                if "exam_countdown_days" in study
                and study.get("exam_countdown_days") is not None
                else None
            ),
            current_streak=(
                _as_int(streaks.get("current_streak"))
                if streaks.get("current_streak") is not None
                else None
            ),
            longest_streak=(
                _as_int(streaks.get("longest_streak"))
                if streaks.get("longest_streak") is not None
                else None
            ),
            consistency_label=str(consistency.get("label") or "").strip(),
            mission_completed_count=_as_int(missions.get("completed_count")),
            mission_missed_count=_as_int(missions.get("missed_count")),
            evidence_attempt_count=_as_int(evidence.get("attempt_count")),
            topics_started=(
                _as_int(readiness_overall.get("topics_started"))
                if readiness_overall.get("topics_started") is not None
                else None
            ),
            topics_mastered=(
                _as_int(readiness_overall.get("topics_mastered"))
                if readiness_overall.get("topics_mastered") is not None
                else None
            ),
            total_topics=(
                _as_int(readiness_overall.get("total_topics"))
                if readiness_overall.get("total_topics") is not None
                else None
            ),
            planner_available=planner_available,
            readiness_available=readiness_available,
            planner_missions=planner_missions,
            planner_revision_priorities=planner_revisions,
            recommended_workload=workload,
            readiness_score=readiness_score,
            confidence_level=confidence_level,
            strongest_areas=strongest,
            weakest_areas=weakest,
            readiness_drivers=drivers,
            recommended_next_actions=next_actions,
            provenance_refs=tuple(provenance_refs),
            limitations_codes=tuple(dict.fromkeys(limitations)),
        )


def build_canonical_insight_consumer() -> CanonicalInsightConsumer:
    return CanonicalInsightConsumer()


__all__ = [
    "CanonicalInsightConsumer",
    "build_canonical_insight_consumer",
]
