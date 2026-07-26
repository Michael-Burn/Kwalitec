"""Twin facet builders (MS-004 T1).

Each builder derives one immutable facet directly from Runtime A evidence.
Builders must not consume other derived facets, Adaptive outputs, or invent
missing values.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import median
from typing import Any, Protocol

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_COGNITIVE_LOAD,
    FACET_CONFIDENCE_TREND,
    FACET_CONSISTENCY,
    FACET_LEARNING_RHYTHM,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_SESSION_HABITS,
    CognitiveLoadIndicatorsFacet,
    ConfidenceTrendFacet,
    ConsistencyFacet,
    LearningRhythmFacet,
    PersistenceFacet,
    RevisionBehaviourFacet,
    SessionHabitsFacet,
    TwinProvenance,
)
from app.infrastructure.adapters.digital_twin.evidence import TwinRuntimeEvidence
from app.infrastructure.adapters.digital_twin.provenance import (
    FIELD_LIFECYCLE_STAGE,
    FIELD_MISSION,
    FIELD_STUDENT_GOALS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_TOPIC_PROGRESS,
    KIND_RUNTIME_A_DERIVED,
    REASON_INSUFFICIENT_DURATION_EVIDENCE,
    REASON_NO_CONFIDENCE_EVIDENCE,
    REASON_UNAVAILABLE,
    SOURCE_SERVICE_TWIN_FACET,
    available_facet_provenance,
    unavailable_facet_provenance,
)
from app.infrastructure.adapters.digital_twin.validation import (
    validate_unavailable_facet_empty,
)

# Structural count postures (observed counts only — not scored estimates).
LABEL_NONE = "none"
LABEL_SPARSE = "sparse"
LABEL_REGULAR = "regular"
LABEL_OBSERVED = "observed"

COMPLETED_MISSION_STATUSES = frozenset({"completed", "complete", "done"})
MISSED_MISSION_STATUSES = frozenset({"missed", "skipped", "abandoned", "cancelled"})


@dataclass(frozen=True)
class FacetBuildResult:
    """One synthesised facet plus its provenance."""

    facet_name: str
    facet: Any
    provenance: TwinProvenance


class FacetBuilder(Protocol):
    """Protocol for a single Runtime-A-derived facet builder."""

    facet_name: str
    source_fields: frozenset[str]

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        """Derive an immutable facet from Runtime A evidence."""


def _count_posture(count: int) -> str:
    if count <= 0:
        return LABEL_NONE
    if count == 1:
        return LABEL_SPARSE
    return LABEL_REGULAR


def _evidence_ref(kind: str, entity_id: str) -> str:
    return f"{kind}:{entity_id}"


def _attempt_refs(attempts: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    refs: list[str] = []
    for row in attempts:
        attempt_id = str(row.get("attempt_id") or "").strip()
        if attempt_id:
            refs.append(_evidence_ref("attempt", attempt_id))
    return tuple(refs)


def _mission_refs(history: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    refs: list[str] = []
    for row in history:
        mission_id = str(row.get("mission_id") or "").strip()
        if mission_id:
            refs.append(_evidence_ref("mission", mission_id))
    return tuple(refs)


def _progress_refs(rows: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    refs: list[str] = []
    for row in rows:
        progress_id = str(row.get("topic_progress_id") or "").strip()
        if progress_id:
            refs.append(_evidence_ref("topic_progress", progress_id))
    return tuple(refs)


def _source_unavailable(
    evidence: TwinRuntimeEvidence,
    field_names: frozenset[str],
) -> tuple[str, str, str] | None:
    """Return (reason, source_service, source_entity) if any required field is down."""
    for name in sorted(field_names):
        if evidence.is_available(name):
            continue
        reason = evidence.unavailable_reason(name) or REASON_UNAVAILABLE
        return (
            reason,
            evidence.source_service(name, default=SOURCE_SERVICE_TWIN_FACET),
            evidence.source_entity(name, default=name),
        )
    return None


def _unavailable_result(
    *,
    facet_name: str,
    facet: Any,
    collected_at: str | None,
    reason: str,
    source_service: str,
    source_entity: str,
) -> FacetBuildResult:
    validate_unavailable_facet_empty(
        facet_name=facet_name,
        availability=AVAILABILITY_UNAVAILABLE,
        evidence_refs=getattr(facet, "evidence_refs", ()),
        material_values={
            "label": getattr(facet, "label", ""),
            "note": (
                getattr(facet, "cadence_note", None)
                or getattr(facet, "adherence_note", None)
                or getattr(facet, "continuity_note", None)
                or getattr(facet, "revision_note", None)
                or getattr(facet, "trend_note", None)
                or getattr(facet, "habits_note", None)
                or getattr(facet, "load_note", None)
                or ""
            ),
            "typical_session_minutes": getattr(
                facet, "typical_session_minutes", None
            ),
        },
    )
    return FacetBuildResult(
        facet_name=facet_name,
        facet=facet,
        provenance=unavailable_facet_provenance(
            source_service=source_service,
            source_entity=source_entity,
            collected_at=collected_at,
            reason=reason,
            kind=KIND_RUNTIME_A_DERIVED,
        ),
    )


class LearningRhythmBuilder:
    """Derive Learning Rhythm from study attempt durations and dates."""

    facet_name = FACET_LEARNING_RHYTHM
    source_fields = frozenset({FIELD_STUDY_ATTEMPTS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = LearningRhythmFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        attempts = list(evidence.study_attempts)
        durations = [
            float(row["duration_minutes"])
            for row in attempts
            if row.get("duration_minutes") is not None
        ]
        dates = sorted(
            {
                str(row.get("study_date") or "").strip()
                for row in attempts
                if str(row.get("study_date") or "").strip()
            }
        )
        typical = round(float(median(durations)), 4) if durations else None
        label = _count_posture(len(attempts))
        cadence_parts = [f"attempt_count={len(attempts)}"]
        if dates:
            cadence_parts.append(f"distinct_days={len(dates)}")
            cadence_parts.append(f"first_date={dates[0]}")
            cadence_parts.append(f"last_date={dates[-1]}")
        if typical is not None:
            cadence_parts.append(f"median_duration_minutes={typical}")
        facet = LearningRhythmFacet(
            label=label,
            typical_session_minutes=typical,
            cadence_note=";".join(cadence_parts),
            evidence_refs=_attempt_refs(attempts),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_STUDY_ATTEMPTS, default="StudyAttempt"
                ),
                collected_at=collected_at,
            ),
        )


class ConsistencyBuilder:
    """Derive Consistency from Mission completion / miss structure."""

    facet_name = FACET_CONSISTENCY
    source_fields = frozenset({FIELD_MISSION})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = ConsistencyFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        history = list(evidence.mission.get("history") or [])
        completed = 0
        missed = 0
        for row in history:
            status = str(row.get("status") or "").strip().lower()
            if status in COMPLETED_MISSION_STATUSES:
                completed += 1
            elif status in MISSED_MISSION_STATUSES:
                missed += 1
        label = _count_posture(completed)
        note = (
            f"mission_count={len(history)};"
            f"completed={completed};"
            f"missed={missed}"
        )
        facet = ConsistencyFacet(
            label=label,
            adherence_note=note,
            evidence_refs=_mission_refs(history),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_MISSION, default="mission_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_MISSION, default="Mission"
                ),
                collected_at=collected_at,
            ),
        )


class PersistenceBuilder:
    """Derive Persistence from TopicProgress continuity fields."""

    facet_name = FACET_PERSISTENCE
    source_fields = frozenset({FIELD_TOPIC_PROGRESS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = PersistenceFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        rows = list(evidence.topic_progress)
        completed = sum(1 for row in rows if bool(row.get("completed")))
        reviewed = sum(
            1 for row in rows if str(row.get("last_reviewed") or "").strip()
        )
        label = _count_posture(len(rows))
        note = (
            f"topic_progress_count={len(rows)};"
            f"completed={completed};"
            f"reviewed={reviewed}"
        )
        facet = PersistenceFacet(
            label=label,
            continuity_note=note,
            evidence_refs=_progress_refs(rows),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_TOPIC_PROGRESS, default="adaptive_learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_TOPIC_PROGRESS, default="TopicProgress"
                ),
                collected_at=collected_at,
            ),
        )


class RevisionBehaviourBuilder:
    """Derive Revision Behaviour from TopicProgress revision counts + lifecycle.

    Lifecycle stage is optional enrichment when the collector is available.
    """

    facet_name = FACET_REVISION_BEHAVIOUR
    source_fields = frozenset({FIELD_TOPIC_PROGRESS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = RevisionBehaviourFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        rows = list(evidence.topic_progress)
        revised_topics = [
            row
            for row in rows
            if int(row.get("revision_count") or 0) > 0
        ]
        total_revisions = sum(int(row.get("revision_count") or 0) for row in rows)
        if evidence.is_available(FIELD_LIFECYCLE_STAGE) and evidence.lifecycle_stage:
            stage = evidence.lifecycle_stage
        else:
            stage = "unknown"
        label = _count_posture(len(revised_topics))
        note = (
            f"lifecycle_stage={stage};"
            f"topics_with_revision={len(revised_topics)};"
            f"total_revision_count={total_revisions}"
        )
        facet = RevisionBehaviourFacet(
            label=label,
            revision_note=note,
            evidence_refs=_progress_refs(revised_topics or rows),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_TOPIC_PROGRESS, default="adaptive_learning_service"
                ),
                source_entity="TopicProgress+LifecycleStage",
                collected_at=collected_at,
            ),
        )


class ConfidenceTrendBuilder:
    """Derive Confidence Trend from study attempt confidence before/after.

    Requires observed confidence fields. Never invents a trend from accuracy.
    """

    facet_name = FACET_CONFIDENCE_TREND
    source_fields = frozenset({FIELD_STUDY_ATTEMPTS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = ConfidenceTrendFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        attempts = list(evidence.study_attempts)
        paired = [
            row
            for row in attempts
            if str(row.get("confidence_before") or "").strip()
            and str(row.get("confidence_after") or "").strip()
        ]
        if not paired:
            facet = ConfidenceTrendFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_NO_CONFIDENCE_EVIDENCE,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=REASON_NO_CONFIDENCE_EVIDENCE,
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_STUDY_ATTEMPTS, default="StudyAttempt"
                ),
            )

        transitions = [
            (
                f"{str(row.get('confidence_before')).strip()}"
                f"->{str(row.get('confidence_after')).strip()}"
            )
            for row in paired
        ]
        # Deterministic frequency summary of observed transitions only.
        counts: dict[str, int] = {}
        for item in transitions:
            counts[item] = counts.get(item, 0) + 1
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        summary = ",".join(f"{name}:{count}" for name, count in ordered)
        facet = ConfidenceTrendFacet(
            label=LABEL_OBSERVED if paired else LABEL_NONE,
            trend_note=(
                f"paired_confidence_attempts={len(paired)};"
                f"transitions={summary}"
            ),
            evidence_refs=_attempt_refs(paired),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_STUDY_ATTEMPTS, default="StudyAttempt"
                ),
                collected_at=collected_at,
            ),
        )


class SessionHabitsBuilder:
    """Derive Session Habits from mission dates + study attempt durations."""

    facet_name = FACET_SESSION_HABITS
    source_fields = frozenset({FIELD_MISSION, FIELD_STUDY_ATTEMPTS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        blocked = _source_unavailable(evidence, self.source_fields)
        if blocked is not None:
            reason, source_service, source_entity = blocked
            facet = SessionHabitsFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=source_service,
                source_entity=source_entity,
            )

        history = list(evidence.mission.get("history") or [])
        attempts = list(evidence.study_attempts)
        mission_days = sorted(
            {
                str(row.get("mission_date") or "").strip()
                for row in history
                if str(row.get("mission_date") or "").strip()
            }
        )
        attempt_days = sorted(
            {
                str(row.get("study_date") or "").strip()
                for row in attempts
                if str(row.get("study_date") or "").strip()
            }
        )
        durations = [
            int(row["duration_minutes"])
            for row in attempts
            if row.get("duration_minutes") is not None
        ]
        label = _count_posture(max(len(history), len(attempts)))
        note_parts = [
            f"mission_days={len(mission_days)}",
            f"attempt_days={len(attempt_days)}",
            f"duration_observations={len(durations)}",
        ]
        if durations:
            note_parts.append(f"min_duration_minutes={min(durations)}")
            note_parts.append(f"max_duration_minutes={max(durations)}")
        refs = list(_mission_refs(history)) + list(_attempt_refs(attempts))
        facet = SessionHabitsFacet(
            label=label,
            habits_note=";".join(note_parts),
            evidence_refs=tuple(refs),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=SOURCE_SERVICE_TWIN_FACET,
                source_entity="Mission+StudyAttempt",
                collected_at=collected_at,
            ),
        )


class CognitiveLoadBuilder:
    """Derive Cognitive Load Indicators from durations vs preferred minutes.

    Structural comparison only. Never invents burnout or load scores.
    Unavailable when no observed durations exist.
    """

    facet_name = FACET_COGNITIVE_LOAD
    source_fields = frozenset({FIELD_STUDY_ATTEMPTS})

    def build(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None,
    ) -> FacetBuildResult:
        # Prefer study attempts; goals preferred minutes are optional enrichment.
        if not evidence.is_available(FIELD_STUDY_ATTEMPTS):
            reason = (
                evidence.unavailable_reason(FIELD_STUDY_ATTEMPTS)
                or REASON_UNAVAILABLE
            )
            facet = CognitiveLoadIndicatorsFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=reason,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=reason,
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_STUDY_ATTEMPTS, default="StudyAttempt"
                ),
            )

        attempts = list(evidence.study_attempts)
        durations = [
            float(row["duration_minutes"])
            for row in attempts
            if row.get("duration_minutes") is not None
        ]
        if not durations:
            facet = CognitiveLoadIndicatorsFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INSUFFICIENT_DURATION_EVIDENCE,
            )
            return _unavailable_result(
                facet_name=self.facet_name,
                facet=facet,
                collected_at=collected_at,
                reason=REASON_INSUFFICIENT_DURATION_EVIDENCE,
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity=evidence.source_entity(
                    FIELD_STUDY_ATTEMPTS, default="StudyAttempt"
                ),
            )

        questions = [
            int(row["questions_attempted"])
            for row in attempts
            if row.get("questions_attempted") is not None
        ]
        preferred = None
        if evidence.is_available(FIELD_STUDENT_GOALS):
            raw = evidence.student_goals.get("preferred_session_minutes")
            if raw is not None and str(raw).strip() != "":
                preferred = int(raw)
        median_duration = round(float(median(durations)), 4)
        note_parts = [
            f"duration_observations={len(durations)}",
            f"median_duration_minutes={median_duration}",
        ]
        if preferred is not None and preferred > 0:
            note_parts.append(f"preferred_session_minutes={preferred}")
            note_parts.append(
                "vs_preferred="
                + (
                    "above"
                    if median_duration > preferred
                    else "at_or_below"
                )
            )
        if questions:
            note_parts.append(
                f"median_questions_attempted={round(float(median(questions)), 4)}"
            )
        facet = CognitiveLoadIndicatorsFacet(
            label=LABEL_OBSERVED,
            load_note=";".join(note_parts),
            evidence_refs=_attempt_refs(
                [row for row in attempts if row.get("duration_minutes") is not None]
            ),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        return FacetBuildResult(
            facet_name=self.facet_name,
            facet=facet,
            provenance=available_facet_provenance(
                source_service=evidence.source_service(
                    FIELD_STUDY_ATTEMPTS, default="learning_service"
                ),
                source_entity="StudyAttempt+StudentGoals",
                collected_at=collected_at,
            ),
        )


def default_facet_builders() -> tuple[FacetBuilder, ...]:
    """Return the canonical ordered set of Twin facet builders."""
    return (
        LearningRhythmBuilder(),
        ConsistencyBuilder(),
        PersistenceBuilder(),
        RevisionBehaviourBuilder(),
        ConfidenceTrendBuilder(),
        SessionHabitsBuilder(),
        CognitiveLoadBuilder(),
    )
