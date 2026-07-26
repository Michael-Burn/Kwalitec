"""Canonical Learner State → Adaptive Study Planner inputs (EP-001.2).

Read-only projection. Does not write Runtime A, invent mastery, recompute
streaks, or fabricate mock performance.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.adaptive_study_planner.contracts import (
    REASON_INVALID_STUDENT_ID,
    REASON_STATE_UNAVAILABLE,
    REASON_TWIN_FLAG_OFF,
    AdaptivePlannerInputs,
    TopicPlanRow,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    CanonicalLearnerState,
)


def _payload(block: Mapping[str, Any] | None) -> dict[str, Any]:
    if not block:
        return {}
    return dict(block.get("payload") or {})


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _topic_rows_from_state(state: CanonicalLearnerState) -> tuple[TopicPlanRow, ...]:
    mastery_payload = _payload(state.topic_mastery)
    progress_payload = _payload(state.topic_progress)

    mastery_by_id: dict[str, Mapping[str, Any]] = {}
    for row in mastery_payload.get("topics") or ():
        if isinstance(row, Mapping):
            tid = str(row.get("topic_id") or "").strip()
            if tid:
                mastery_by_id[tid] = row

    progress_rows = progress_payload.get("topics") or ()
    # Foundation may expose topic lists under alternate keys — merge both.
    if not progress_rows:
        progress_rows = progress_payload.get("topic_rows") or ()

    rows: list[TopicPlanRow] = []
    seen: set[str] = set()

    for row in progress_rows:
        if not isinstance(row, Mapping):
            continue
        tid = str(row.get("topic_id") or "").strip()
        if not tid or tid in seen:
            continue
        seen.add(tid)
        mastery = mastery_by_id.get(tid, {})
        score = _as_float(mastery.get("mastery_score"))
        if score is None:
            score = _as_float(row.get("mastery_score"))
        accuracy = _as_float(mastery.get("average_accuracy"))
        if accuracy is None:
            accuracy = _as_float(row.get("average_accuracy"))
        rows.append(
            TopicPlanRow(
                topic_id=tid,
                topic_name=str(
                    row.get("topic_name")
                    or mastery.get("topic_name")
                    or f"Topic {tid}"
                ),
                mastery_score=score,
                average_accuracy=accuracy,
                current_stage=str(
                    row.get("current_stage")
                    or mastery.get("current_stage")
                    or ""
                ),
                completed=bool(row.get("completed")),
                next_review_date=(
                    str(row["next_review_date"])
                    if row.get("next_review_date")
                    else None
                ),
                revision_count=int(row.get("revision_count") or 0),
            )
        )

    # Mastery-only topics not present in progress list.
    for tid, mastery in mastery_by_id.items():
        if tid in seen:
            continue
        rows.append(
            TopicPlanRow(
                topic_id=tid,
                topic_name=str(mastery.get("topic_name") or f"Topic {tid}"),
                mastery_score=_as_float(mastery.get("mastery_score")),
                average_accuracy=_as_float(mastery.get("average_accuracy")),
                current_stage=str(mastery.get("current_stage") or ""),
                completed=bool(mastery.get("completed")),
                next_review_date=(
                    str(mastery["next_review_date"])
                    if mastery.get("next_review_date")
                    else None
                ),
                revision_count=int(mastery.get("revision_count") or 0),
            )
        )

    # Deterministic order: incomplete first (syllabus progress), then by topic_id.
    rows.sort(key=lambda r: (r.completed, r.topic_id))
    return tuple(rows)


class CanonicalPlannerConsumer:
    """Project CanonicalLearnerState into AdaptivePlannerInputs.

    Rules:
    - MAY read CanonicalLearnerState only
    - MUST NOT write Runtime A, invent mastery, or recompute streaks
    - Identical serialize() for identical CanonicalLearnerState.serialize()
    """

    CONSUMER_ID = "canonical_planner_consumer"
    CONSUMER_VERSION = "1.0.0"

    def unavailable_inputs(
        self,
        *,
        student_id: str = "",
        as_of: str | None = None,
        reason: str = REASON_STATE_UNAVAILABLE,
    ) -> AdaptivePlannerInputs:
        return AdaptivePlannerInputs(
            student_id=student_id,
            as_of=as_of,
            foundation_version="",
            twin_id="",
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
            lifecycle_stage="",
            examination_label="",
            exam_countdown_days=None,
            planned_weekly_hours=None,
            preferred_session_minutes=None,
            current_streak=None,
            longest_streak=None,
            consistency_label="",
            behaviour_labels={},
            topics=(),
            evidence_attempt_count=0,
            practice_mean_accuracy_pct=None,
            mission_completed_count=0,
            mission_missed_count=0,
            provenance_refs=(),
            limitations_codes=(reason,),
        )

    def project(self, state: CanonicalLearnerState) -> AdaptivePlannerInputs:
        if not isinstance(state, CanonicalLearnerState):
            raise TypeError("state must be a CanonicalLearnerState")

        sid = (state.student_id or "").strip()
        if not sid:
            return self.unavailable_inputs(reason=REASON_INVALID_STUDENT_ID)

        if state.availability != AVAILABILITY_AVAILABLE:
            return self.unavailable_inputs(
                student_id=sid,
                as_of=state.as_of,
                reason=state.unavailable_reason or REASON_STATE_UNAVAILABLE,
            )

        study = _payload(state.study_state)
        streaks = _payload(state.streaks)
        evidence = _payload(state.learning_evidence)
        practice = _payload(state.practice_performance)
        mission = _payload(state.mission_completion)
        consistency = _payload(state.study_consistency)
        behaviour = _payload(state.study_behaviour)
        preferences = dict(study.get("preferences") or {})

        behaviour_labels: dict[str, str] = {}
        for key in ("learning_rhythm", "session_habits", "persistence"):
            facet = behaviour.get(key)
            if isinstance(facet, Mapping):
                # Foundation nests facet claims as availability envelopes.
                inner = facet.get("payload") if "payload" in facet else facet
                if not isinstance(inner, Mapping):
                    inner = {}
                label = str(
                    inner.get("label")
                    or facet.get("label")
                    or facet.get("facet_label")
                    or ""
                )
                if label:
                    behaviour_labels[key] = label
            if key not in behaviour_labels and key in state.facet_labels:
                behaviour_labels[key] = str(state.facet_labels[key])

        consistency_label = str(
            consistency.get("label")
            or consistency.get("facet_label")
            or state.facet_labels.get("consistency")
            or ""
        )

        return AdaptivePlannerInputs(
            student_id=sid,
            as_of=state.as_of,
            foundation_version=state.foundation_version,
            twin_id=state.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            lifecycle_stage=str(study.get("lifecycle_stage") or ""),
            examination_label=str(study.get("examination_label") or ""),
            exam_countdown_days=_as_int(study.get("exam_countdown_days")),
            planned_weekly_hours=_as_float(preferences.get("planned_weekly_hours")),
            preferred_session_minutes=_as_int(
                preferences.get("preferred_session_minutes")
            ),
            current_streak=_as_int(streaks.get("current_streak")),
            longest_streak=_as_int(streaks.get("longest_streak")),
            consistency_label=consistency_label,
            behaviour_labels=behaviour_labels,
            topics=_topic_rows_from_state(state),
            evidence_attempt_count=int(evidence.get("attempt_count") or 0),
            practice_mean_accuracy_pct=_as_float(
                practice.get("mean_accuracy_pct")
            ),
            mission_completed_count=int(mission.get("completed_count") or 0),
            mission_missed_count=int(mission.get("missed_count") or 0),
            provenance_refs=tuple(state.provenance_refs),
            limitations_codes=tuple(state.limitations_codes),
        )


def build_canonical_planner_consumer() -> CanonicalPlannerConsumer:
    return CanonicalPlannerConsumer()


# Re-export reason used when Twin flag is off for callers.
__all__ = [
    "CanonicalPlannerConsumer",
    "REASON_TWIN_FLAG_OFF",
    "build_canonical_planner_consumer",
]
