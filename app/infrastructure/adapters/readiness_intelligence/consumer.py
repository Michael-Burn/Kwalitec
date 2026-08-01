"""Canonical Learner State → Readiness Intelligence inputs (EP-001.3).

Read-only projection. Does not write Runtime A, invent mastery, recompute
streaks, or fabricate mock performance. Does not plan missions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    CanonicalLearnerState,
)
from app.infrastructure.adapters.readiness_intelligence.contracts import (
    REASON_INVALID_STUDENT_ID,
    REASON_PLANNER_UNAVAILABLE,
    REASON_STATE_UNAVAILABLE,
    REASON_TWIN_FLAG_OFF,
    ReadinessIntelligenceInputs,
    TopicArea,
)

_WEAK_THRESHOLD = 60.0
_STRONG_THRESHOLD = 70.0


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


def _topic_areas_from_state(state: CanonicalLearnerState) -> tuple[TopicArea, ...]:
    mastery_payload = _payload(state.topic_mastery)
    rows = mastery_payload.get("topics") or ()
    areas: list[TopicArea] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        tid = str(row.get("topic_id") or "").strip()
        if not tid:
            continue
        score = _as_float(row.get("mastery_score"))
        name = str(row.get("topic_name") or f"Topic {tid}")
        if score is None:
            reason = "Mastery score unavailable on Canonical topic row"
        elif score < _WEAK_THRESHOLD:
            reason = f"Mastery {score:.0f}% — limiting area"
        elif score >= _STRONG_THRESHOLD:
            reason = f"Mastery {score:.0f}% — supporting area"
        else:
            reason = f"Mastery {score:.0f}% — developing area"
        areas.append(
            TopicArea(
                topic_id=tid,
                topic_name=name,
                mastery_score=score,
                reason=reason,
            )
        )
    areas.sort(
        key=lambda a: (
            a.mastery_score is None,
            -(a.mastery_score or 0.0),
            a.topic_id,
        )
    )
    return tuple(areas)


def _compose_score_from_cls(
    *,
    coverage_pct: float | None,
    avg_mastery: float | None,
    review_discipline: float | None,
) -> float | None:
    """Same 50/30/20 weights as ReadinessService.get_overall_readiness."""
    if coverage_pct is None and avg_mastery is None and review_discipline is None:
        return None
    coverage = float(coverage_pct or 0.0)
    mastery = float(avg_mastery or 0.0)
    review = float(review_discipline or 0.0)
    return round((coverage * 0.50) + (mastery * 0.30) + (review * 0.20), 1)


def _mission_review_discipline(
    completed: int, missed: int, history_hint: int | None = None
) -> float | None:
    total = completed + missed
    if history_hint is not None and history_hint > total:
        total = history_hint
    if total <= 0:
        return None
    return round((completed / total) * 100.0, 1)


class CanonicalReadinessConsumer:
    """Project CanonicalLearnerState (+ optional planner dict) into inputs.

    Rules:
    - MAY read CanonicalLearnerState and planner projection dicts only
    - MUST NOT write Runtime A, invent mastery, or recompute streaks
    - MUST NOT call ReadinessService getters (avoids collector recursion)
    - Identical serialize() for identical CanonicalLearnerState.serialize()
      and identical planner payload
    """

    CONSUMER_ID = "canonical_readiness_consumer"
    CONSUMER_VERSION = "1.0.0"

    def unavailable_inputs(
        self,
        *,
        student_id: str = "",
        as_of: str | None = None,
        reason: str = REASON_STATE_UNAVAILABLE,
    ) -> ReadinessIntelligenceInputs:
        return ReadinessIntelligenceInputs(
            student_id=student_id,
            as_of=as_of,
            foundation_version="",
            twin_id="",
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
            lifecycle_stage="",
            examination_label="",
            exam_countdown_days=None,
            readiness_score=None,
            coverage_pct=None,
            avg_mastery=None,
            review_discipline=None,
            topics_started=None,
            topics_mastered=None,
            total_topics=None,
            current_streak=None,
            longest_streak=None,
            consistency_label="",
            behaviour_labels={},
            evidence_attempt_count=0,
            practice_mean_accuracy_pct=None,
            mission_completed_count=0,
            mission_missed_count=0,
            topic_areas=(),
            planner_missions=(),
            planner_revision_priorities=(),
            planner_available=False,
            provenance_refs=(),
            limitations_codes=(reason,),
        )

    def project(
        self,
        state: CanonicalLearnerState,
        *,
        daily_plan: Mapping[str, Any] | None = None,
    ) -> ReadinessIntelligenceInputs:
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
        mastery = _payload(state.topic_mastery)
        progress = _payload(state.topic_progress)

        overall = dict(study.get("readiness_overall") or {})
        readiness_score = _as_float(overall.get("score"))
        if readiness_score is None:
            readiness_score = _as_float(overall.get("readiness_score"))
        if readiness_score is None:
            readiness_score = _as_float(study.get("exam_readiness"))

        coverage_pct = _as_float(overall.get("coverage_pct"))
        avg_mastery = _as_float(overall.get("avg_mastery"))
        review_discipline = _as_float(overall.get("review_discipline"))
        topics_started = _as_int(overall.get("topics_started"))
        topics_mastered = _as_int(overall.get("topics_mastered"))
        total_topics = _as_int(overall.get("total_topics"))

        # Fallbacks from CLS dimension payloads when overall is thin.
        if avg_mastery is None:
            scores = [
                _as_float(row.get("mastery_score"))
                for row in (mastery.get("topics") or ())
                if isinstance(row, Mapping)
            ]
            present = [s for s in scores if s is not None]
            if present:
                avg_mastery = round(sum(present) / len(present), 1)

        if topics_mastered is None:
            topics_mastered = _as_int(mastery.get("mastered_topic_count"))

        if topics_started is None:
            topics_started = _as_int(progress.get("completed_count"))
            if topics_started is None:
                # Study Progress authority: completed topics only (not revision_count).
                started_rows = [
                    row
                    for row in (progress.get("topics") or ())
                    if isinstance(row, Mapping) and bool(row.get("completed"))
                ]
                topics_started = len(started_rows) if started_rows else None

        if total_topics is None:
            total_topics = _as_int(progress.get("topic_count"))
            if total_topics is None:
                rows = progress.get("topics") or mastery.get("topics") or ()
                total_topics = len(rows) if rows else None

        if coverage_pct is None and total_topics and topics_started is not None:
            coverage_pct = round((topics_started / total_topics) * 100.0, 1)

        completed = int(mission.get("completed_count") or 0)
        missed = int(mission.get("missed_count") or 0)
        history = _as_int(mission.get("history_count"))
        if review_discipline is None:
            review_discipline = _mission_review_discipline(
                completed, missed, history_hint=history
            )

        if readiness_score is None:
            readiness_score = _compose_score_from_cls(
                coverage_pct=coverage_pct,
                avg_mastery=avg_mastery,
                review_discipline=review_discipline,
            )

        behaviour_labels: dict[str, str] = {}
        for key in ("learning_rhythm", "session_habits", "persistence"):
            facet = behaviour.get(key)
            if isinstance(facet, Mapping):
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

        planner_missions: tuple[Mapping[str, Any], ...] = ()
        planner_revisions: tuple[Mapping[str, Any], ...] = ()
        planner_available = False
        limitations = list(state.limitations_codes)
        if daily_plan and isinstance(daily_plan, Mapping):
            plan_availability = str(
                daily_plan.get("availability") or AVAILABILITY_AVAILABLE
            )
            if plan_availability == AVAILABILITY_AVAILABLE:
                missions = daily_plan.get("today_missions") or ()
                revisions = daily_plan.get("revision_priorities") or ()
                if isinstance(missions, Sequence):
                    planner_missions = tuple(
                        dict(row) for row in missions if isinstance(row, Mapping)
                    )
                if isinstance(revisions, Sequence):
                    planner_revisions = tuple(
                        dict(row) for row in revisions if isinstance(row, Mapping)
                    )
                planner_available = bool(planner_missions or planner_revisions)
            if not planner_available:
                limitations.append(REASON_PLANNER_UNAVAILABLE)
        else:
            limitations.append(REASON_PLANNER_UNAVAILABLE)

        return ReadinessIntelligenceInputs(
            student_id=sid,
            as_of=state.as_of,
            foundation_version=state.foundation_version,
            twin_id=state.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            lifecycle_stage=str(study.get("lifecycle_stage") or ""),
            examination_label=str(study.get("examination_label") or ""),
            exam_countdown_days=_as_int(study.get("exam_countdown_days")),
            readiness_score=readiness_score,
            coverage_pct=coverage_pct,
            avg_mastery=avg_mastery,
            review_discipline=review_discipline,
            topics_started=topics_started,
            topics_mastered=topics_mastered,
            total_topics=total_topics,
            current_streak=_as_int(streaks.get("current_streak")),
            longest_streak=_as_int(streaks.get("longest_streak")),
            consistency_label=consistency_label,
            behaviour_labels=behaviour_labels,
            evidence_attempt_count=int(evidence.get("attempt_count") or 0),
            practice_mean_accuracy_pct=_as_float(
                practice.get("mean_accuracy_pct")
            ),
            mission_completed_count=completed,
            mission_missed_count=missed,
            topic_areas=_topic_areas_from_state(state),
            planner_missions=planner_missions,
            planner_revision_priorities=planner_revisions,
            planner_available=planner_available,
            provenance_refs=tuple(state.provenance_refs),
            limitations_codes=tuple(dict.fromkeys(limitations)),
        )


def build_canonical_readiness_consumer() -> CanonicalReadinessConsumer:
    return CanonicalReadinessConsumer()


__all__ = [
    "CanonicalReadinessConsumer",
    "REASON_TWIN_FLAG_OFF",
    "build_canonical_readiness_consumer",
]
