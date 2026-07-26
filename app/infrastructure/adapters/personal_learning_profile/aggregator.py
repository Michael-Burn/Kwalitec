"""Aggregate Learning Feedback evidence into Personal Learning Profile (EP-004.1).

Derived indicators are labelled as such. Attributes without lawful evidence
are marked unsupported / unavailable — never invented.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from app.infrastructure.adapters.learning_feedback.contracts import (
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
    FEEDBACK_EVENT_RECOVERY_APPLIED,
    FEEDBACK_EVENT_REVISION_ADHERED,
    FEEDBACK_EVENT_REVISION_DEFERRED,
    FEEDBACK_EVENT_SESSION_MISSED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    LearningFeedbackEvent,
)
from app.infrastructure.adapters.personal_learning_profile.contracts import (
    ATTR_CONSISTENCY_TREND,
    ATTR_PLANNING_COMPLETION_RATE,
    ATTR_PREFERRED_SESSION_DURATION,
    ATTR_PREFERRED_STUDY_WINDOWS,
    ATTR_RECOMMENDATION_RESPONSIVENESS,
    ATTR_RECOVERY_EFFECTIVENESS,
    ATTR_REVISION_ADHERENCE,
    CLAIM_BEHAVIOUR_SUMMARY,
    CLAIM_HABIT_SUMMARY,
    CLAIM_PREFERENCE_SUMMARY,
    CLAIM_UNSUPPORTED,
    CONTRACT_VERSION,
    KIND_DERIVED_INDICATOR,
    KIND_OBSERVED_FACT,
    KIND_UNSUPPORTED,
    PROFILE_ATTRIBUTE_KEYS,
    STATUS_AVAILABLE,
    STATUS_UNAVAILABLE,
    STATUS_UNSUPPORTED,
    PersonalLearningProfile,
    ProfileAttribute,
    ProfileEvidenceRef,
    confidence_from_sample_size,
    deterministic_profile_id,
    serialize_canonical,
)

logger = logging.getLogger(__name__)

_LIMITATION_NO_DURATION_EVIDENCE = (
    "Learning Feedback events do not carry study-session duration; "
    "preferred duration remains unsupported unless declared minutes are supplied"
)
_LIMITATION_NO_WINDOW_EVIDENCE = (
    "Event wall-clock timestamps are not treated as student preferred "
    "study windows; attribute remains unsupported"
)
_LIMITATION_RECOVERY_PROXY = (
    "Recovery effectiveness is a behavioural follow-through rate after "
    "recovery_applied observations — not proof that recovery fixed a deficit"
)
_LIMITATION_COMPLETION_RATE = (
    "Planning completion rate uses plan_completed vs session_missed counts "
    "as a behavioural proxy — not mastery or plan quality"
)


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _as_events(events: Sequence[Any] | None) -> list[LearningFeedbackEvent]:
    out: list[LearningFeedbackEvent] = []
    for item in events or ():
        if isinstance(item, LearningFeedbackEvent):
            out.append(item)
    return out


def _refs_for(
    events: Sequence[LearningFeedbackEvent],
    *,
    limit: int = 20,
) -> tuple[ProfileEvidenceRef, ...]:
    refs: list[ProfileEvidenceRef] = []
    for event in events[-limit:]:
        refs.append(
            ProfileEvidenceRef(
                feedback_id=event.feedback_id,
                event_type=event.event_type,
                source_authority=event.source_authority,
                timestamp=event.timestamp,
            )
        )
    return tuple(refs)


def _fingerprint(events: Sequence[LearningFeedbackEvent]) -> str:
    material = [
        {
            "feedback_id": e.feedback_id,
            "event_type": e.event_type,
            "timestamp": e.timestamp,
            "payload": dict(e.payload),
        }
        for e in events
    ]
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return digest[:40]


def _unsupported(
    key: str,
    *,
    explanation: str,
    limitations: tuple[str, ...] = (),
) -> ProfileAttribute:
    return ProfileAttribute(
        key=key,
        kind=KIND_UNSUPPORTED,
        status=STATUS_UNSUPPORTED,
        claim_boundary=CLAIM_UNSUPPORTED,
        value=None,
        confidence=0.0,
        sample_size=0,
        explanation=explanation,
        evidence_refs=(),
        limitations=limitations,
    )


def _unavailable(
    key: str,
    *,
    kind: str,
    claim_boundary: str,
    explanation: str,
    limitations: tuple[str, ...] = (),
) -> ProfileAttribute:
    return ProfileAttribute(
        key=key,
        kind=kind,
        status=STATUS_UNAVAILABLE,
        claim_boundary=claim_boundary,
        value=None,
        confidence=0.0,
        sample_size=0,
        explanation=explanation,
        evidence_refs=(),
        limitations=limitations,
    )


def _build_preferred_session_duration(
    *,
    declared_session_minutes: int | None,
) -> ProfileAttribute:
    if declared_session_minutes is None:
        return _unsupported(
            ATTR_PREFERRED_SESSION_DURATION,
            explanation=(
                "No observed session-duration evidence and no declared "
                "preferred session minutes supplied"
            ),
            limitations=(_LIMITATION_NO_DURATION_EVIDENCE,),
        )
    minutes = max(0, int(declared_session_minutes))
    return ProfileAttribute(
        key=ATTR_PREFERRED_SESSION_DURATION,
        kind=KIND_OBSERVED_FACT,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_PREFERENCE_SUMMARY,
        value={"declared_session_minutes": minutes},
        confidence=1.0 if minutes > 0 else 0.0,
        sample_size=1 if minutes > 0 else 0,
        explanation=(
            "Declared preferred session minutes from student settings "
            "(observed preference declaration, not inferred mastery)"
        ),
        evidence_refs=(),
        limitations=(
            "Value is a declared preference, not measured session length",
        ),
    )


def _build_consistency_trend(
    events: Sequence[LearningFeedbackEvent],
) -> ProfileAttribute:
    consistency = [
        e for e in events if e.event_type == FEEDBACK_EVENT_STUDY_CONSISTENCY
    ]
    if not consistency:
        return _unavailable(
            ATTR_CONSISTENCY_TREND,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_HABIT_SUMMARY,
            explanation="No study_consistency_observed events available",
        )
    streaks: list[int] = []
    for event in consistency:
        raw = event.payload.get("current_streak")
        try:
            streaks.append(max(0, int(raw)))
        except (TypeError, ValueError):
            continue
    if not streaks:
        return _unavailable(
            ATTR_CONSISTENCY_TREND,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_HABIT_SUMMARY,
            explanation=(
                "Consistency events present but current_streak payloads "
                "were not parseable"
            ),
        )
    latest = streaks[-1]
    prior = streaks[-2] if len(streaks) >= 2 else latest
    if latest > prior:
        direction = "increasing"
    elif latest < prior:
        direction = "decreasing"
    else:
        direction = "stable"
    sample = len(streaks)
    return ProfileAttribute(
        key=ATTR_CONSISTENCY_TREND,
        kind=KIND_DERIVED_INDICATOR,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_HABIT_SUMMARY,
        value={
            "direction": direction,
            "latest_streak": latest,
            "observation_count": sample,
        },
        confidence=confidence_from_sample_size(sample),
        sample_size=sample,
        explanation=(
            f"Derived from {sample} study_consistency_observed streak "
            f"signal(s); latest={latest}, direction={direction}"
        ),
        evidence_refs=_refs_for(consistency),
        limitations=(
            "Streak integers are habit signals, not learning-quality proof",
        ),
    )


def _build_recovery_effectiveness(
    events: Sequence[LearningFeedbackEvent],
) -> ProfileAttribute:
    recoveries = [
        e for e in events if e.event_type == FEEDBACK_EVENT_RECOVERY_APPLIED
    ]
    completions = [
        e for e in events if e.event_type == FEEDBACK_EVENT_PLAN_COMPLETED
    ]
    if not recoveries:
        return _unavailable(
            ATTR_RECOVERY_EFFECTIVENESS,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
            explanation="No recovery_applied observations available",
            limitations=(_LIMITATION_RECOVERY_PROXY,),
        )
    # Behavioural proxy: share of recovery events followed later by at least
    # one plan_completed (same student event stream order).
    followed = 0
    for recovery in recoveries:
        for completion in completions:
            if completion.timestamp >= recovery.timestamp:
                followed += 1
                break
    rate = round(followed / len(recoveries), 4)
    sample = len(recoveries)
    return ProfileAttribute(
        key=ATTR_RECOVERY_EFFECTIVENESS,
        kind=KIND_DERIVED_INDICATOR,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
        value={
            "recovery_count": sample,
            "followed_by_completion_count": followed,
            "follow_through_rate": rate,
        },
        confidence=confidence_from_sample_size(sample),
        sample_size=sample,
        explanation=(
            f"Derived follow-through rate {rate} from {sample} "
            "recovery_applied observation(s)"
        ),
        evidence_refs=_refs_for(list(recoveries) + list(completions)),
        limitations=(_LIMITATION_RECOVERY_PROXY,),
    )


def _build_revision_adherence(
    events: Sequence[LearningFeedbackEvent],
) -> ProfileAttribute:
    adhered = [
        e for e in events if e.event_type == FEEDBACK_EVENT_REVISION_ADHERED
    ]
    deferred = [
        e for e in events if e.event_type == FEEDBACK_EVENT_REVISION_DEFERRED
    ]
    total = len(adhered) + len(deferred)
    if total == 0:
        return _unavailable(
            ATTR_REVISION_ADHERENCE,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
            explanation="No revision_adhered / revision_deferred observations",
        )
    rate = round(len(adhered) / total, 4)
    return ProfileAttribute(
        key=ATTR_REVISION_ADHERENCE,
        kind=KIND_DERIVED_INDICATOR,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
        value={
            "adhered_count": len(adhered),
            "deferred_count": len(deferred),
            "adherence_rate": rate,
        },
        confidence=confidence_from_sample_size(total),
        sample_size=total,
        explanation=(
            f"Derived revision adherence rate {rate} from {total} "
            "revision interaction observation(s)"
        ),
        evidence_refs=_refs_for(list(adhered) + list(deferred)),
        limitations=(
            "Revision adherence is plan-interaction evidence, not mastery",
        ),
    )


def _build_recommendation_responsiveness(
    events: Sequence[LearningFeedbackEvent],
) -> ProfileAttribute:
    accepted = [
        e
        for e in events
        if e.event_type == FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED
    ]
    dismissed = [
        e
        for e in events
        if e.event_type == FEEDBACK_EVENT_RECOMMENDATION_DISMISSED
    ]
    total = len(accepted) + len(dismissed)
    if total == 0:
        return _unavailable(
            ATTR_RECOMMENDATION_RESPONSIVENESS,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_PREFERENCE_SUMMARY,
            explanation=(
                "No recommendation_accepted / recommendation_dismissed "
                "preference-journal observations"
            ),
        )
    rate = round(len(accepted) / total, 4)
    return ProfileAttribute(
        key=ATTR_RECOMMENDATION_RESPONSIVENESS,
        kind=KIND_DERIVED_INDICATOR,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_PREFERENCE_SUMMARY,
        value={
            "accepted_count": len(accepted),
            "dismissed_count": len(dismissed),
            "accept_rate": rate,
        },
        confidence=confidence_from_sample_size(total),
        sample_size=total,
        explanation=(
            f"Derived preference-journal accept rate {rate} from {total} "
            "recommendation decision observation(s)"
        ),
        evidence_refs=_refs_for(list(accepted) + list(dismissed)),
        limitations=(
            "Accept/dismiss is preference history, never mastery evidence",
        ),
    )


def _build_planning_completion_rate(
    events: Sequence[LearningFeedbackEvent],
) -> ProfileAttribute:
    completed = [
        e for e in events if e.event_type == FEEDBACK_EVENT_PLAN_COMPLETED
    ]
    missed = [
        e for e in events if e.event_type == FEEDBACK_EVENT_SESSION_MISSED
    ]
    if not completed and not missed:
        return _unavailable(
            ATTR_PLANNING_COMPLETION_RATE,
            kind=KIND_DERIVED_INDICATOR,
            claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
            explanation=(
                "No plan_completed or session_missed observations available"
            ),
            limitations=(_LIMITATION_COMPLETION_RATE,),
        )
    # Observed fact counts plus derived rate when both sides exist.
    completed_n = len(completed)
    missed_signal = 0
    for event in missed:
        raw = event.payload.get("mission_missed_count", 1)
        try:
            missed_signal += max(0, int(raw))
        except (TypeError, ValueError):
            missed_signal += 1
    denominator = completed_n + missed_signal
    rate = (
        round(completed_n / denominator, 4) if denominator > 0 else None
    )
    sample = completed_n + len(missed)
    value: dict[str, Any] = {
        "plan_completed_count": completed_n,
        "session_missed_event_count": len(missed),
        "session_missed_signal_sum": missed_signal,
    }
    if rate is not None:
        value["completion_rate"] = rate
    return ProfileAttribute(
        key=ATTR_PLANNING_COMPLETION_RATE,
        kind=KIND_DERIVED_INDICATOR if rate is not None else KIND_OBSERVED_FACT,
        status=STATUS_AVAILABLE,
        claim_boundary=CLAIM_BEHAVIOUR_SUMMARY,
        value=value,
        confidence=confidence_from_sample_size(sample),
        sample_size=sample,
        explanation=(
            f"Planning completion behavioural summary from {sample} "
            "plan/miss observation(s)"
            + (f"; rate={rate}" if rate is not None else "")
        ),
        evidence_refs=_refs_for(list(completed) + list(missed)),
        limitations=(_LIMITATION_COMPLETION_RATE,),
    )


def _build_preferred_study_windows() -> ProfileAttribute:
    return _unsupported(
        ATTR_PREFERRED_STUDY_WINDOWS,
        explanation=(
            "Preferred study windows are not supported by lawful evidence "
            "in the current Learning Feedback event model"
        ),
        limitations=(_LIMITATION_NO_WINDOW_EVIDENCE,),
    )


class PersonalLearningProfileAggregator:
    """Build immutable PersonalLearningProfile snapshots from evidence.

    Responsibilities: aggregate, label epistemic kind, record confidence,
    preserve provenance. Non-responsibilities: ranking, readiness, planning,
    Twin writes, educational conclusions.
    """

    AGGREGATOR_ID = "personal_learning_profile_aggregator"
    AGGREGATOR_VERSION = "1.0.0-ep004.1"

    def aggregate(
        self,
        *,
        student_id: str | int,
        events: Sequence[Any] | None = None,
        declared_session_minutes: int | None = None,
        as_of: str | None = None,
        provenance: Mapping[str, Any] | None = None,
    ) -> PersonalLearningProfile:
        """Aggregate observed events into a full attribute profile."""
        sid = str(student_id).strip()
        if not sid:
            raise ValueError("student_id is required")
        filtered = [
            e for e in _as_events(events) if e.student_id == sid
        ]
        filtered.sort(key=lambda e: (e.timestamp, e.feedback_id))
        stamp = (as_of or "").strip() or _now_iso()
        fingerprint = _fingerprint(filtered)

        attributes = {
            ATTR_PREFERRED_SESSION_DURATION: _build_preferred_session_duration(
                declared_session_minutes=declared_session_minutes
            ),
            ATTR_CONSISTENCY_TREND: _build_consistency_trend(filtered),
            ATTR_RECOVERY_EFFECTIVENESS: _build_recovery_effectiveness(
                filtered
            ),
            ATTR_REVISION_ADHERENCE: _build_revision_adherence(filtered),
            ATTR_RECOMMENDATION_RESPONSIVENESS: (
                _build_recommendation_responsiveness(filtered)
            ),
            ATTR_PLANNING_COMPLETION_RATE: _build_planning_completion_rate(
                filtered
            ),
            ATTR_PREFERRED_STUDY_WINDOWS: _build_preferred_study_windows(),
        }
        assert frozenset(attributes) == PROFILE_ATTRIBUTE_KEYS

        limitations = (
            "Profile summarises Learning Feedback observations only",
            "Profile is not an educational decision authority",
            "Unavailable / unsupported attributes must not be invented by consumers",
        )
        profile_id = deterministic_profile_id(
            student_id=sid,
            as_of=stamp,
            evidence_fingerprint=fingerprint,
            contract_version=CONTRACT_VERSION,
        )
        prov = {
            "aggregator_id": self.AGGREGATOR_ID,
            "aggregator_version": self.AGGREGATOR_VERSION,
            "source": "learning_feedback",
            "event_count": len(filtered),
            **dict(provenance or {}),
        }
        return PersonalLearningProfile(
            profile_id=profile_id,
            student_id=sid,
            as_of=stamp,
            attributes=attributes,
            evidence_fingerprint=fingerprint,
            evidence_event_count=len(filtered),
            provenance=prov,
            limitations=limitations,
        )


def build_personal_learning_profile_aggregator() -> (
    PersonalLearningProfileAggregator
):
    """DI helper for the profile aggregator."""
    return PersonalLearningProfileAggregator()
