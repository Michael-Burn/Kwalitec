"""Student Digital Twin Foundation (EP-001.1).

Canonical Runtime-A-grounded learner-state read model for subsystems.

Extends MS-004 collectors / TwinRuntimeEvidence / facet synthesis — does not
invent a parallel Twin domain, write Runtime A, estimate missing mastery, or
fabricate mock performance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.digital_twin.assembler import (
    TwinFacetAssembler,
    TwinFacetBundle,
    build_twin_facet_assembler,
)
from app.infrastructure.adapters.digital_twin.builders import (
    COMPLETED_MISSION_STATUSES,
    MISSED_MISSION_STATUSES,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    TwinSnapshot,
    serialize_canonical,
)
from app.infrastructure.adapters.digital_twin.evidence import TwinRuntimeEvidence
from app.infrastructure.adapters.digital_twin.provenance import (
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_STUDENT_GOALS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_TOPIC_PROGRESS,
)
from app.infrastructure.adapters.digital_twin.snapshot_builder import (
    TwinSnapshotBuilder,
    build_twin_snapshot_builder,
)

FOUNDATION_VERSION = "ep001.1.0"

REASON_FOUNDATION_FLAG_OFF = "foundation_flag_off"
REASON_INVALID_STUDENT_ID = "invalid_student_id"
REASON_MOCK_NOT_DISTINGUISHED = "mock_evidence_not_distinguished"
REASON_RUNTIME_A_UNAVAILABLE = "runtime_a_field_unavailable"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def _freeze_rows(
    value: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None,
) -> tuple[Mapping[str, Any], ...]:
    if not value:
        return ()
    return tuple(MappingProxyType(dict(row)) for row in value)


def _available_block(
    *,
    payload: Mapping[str, Any],
    evidence_refs: Sequence[str] = (),
    source_field: str = "",
) -> dict[str, Any]:
    return {
        "availability": AVAILABILITY_AVAILABLE,
        "unavailable_reason": "",
        "authority": AUTHORITY_RUNTIME_A,
        "source_field": source_field,
        "evidence_refs": list(evidence_refs),
        "payload": dict(payload),
    }


def _unavailable_block(*, reason: str, source_field: str = "") -> dict[str, Any]:
    return {
        "availability": AVAILABILITY_UNAVAILABLE,
        "unavailable_reason": reason,
        "authority": AUTHORITY_DIGITAL_TWIN,
        "source_field": source_field,
        "evidence_refs": [],
        "payload": {},
    }


@dataclass(frozen=True)
class CanonicalLearnerState:
    """Immutable canonical Student Digital Twin foundation state.

    Every material educational claim is Runtime A pass-through or an
    explicitly labelled MS-004 facet projection. Missing evidence stays
    unavailable — never estimated.
    """

    student_id: str
    as_of: str | None
    foundation_version: str
    twin_id: str
    study_state: Mapping[str, Any]
    topic_mastery: Mapping[str, Any]
    topic_progress: Mapping[str, Any]
    learning_evidence: Mapping[str, Any]
    practice_performance: Mapping[str, Any]
    mock_performance: Mapping[str, Any]
    study_behaviour: Mapping[str, Any]
    study_consistency: Mapping[str, Any]
    streaks: Mapping[str, Any]
    mission_completion: Mapping[str, Any]
    facet_labels: Mapping[str, str] = field(default_factory=dict)
    limitations_codes: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "study_state", _freeze_mapping(self.study_state))
        object.__setattr__(self, "topic_mastery", _freeze_mapping(self.topic_mastery))
        object.__setattr__(
            self, "topic_progress", _freeze_mapping(self.topic_progress)
        )
        object.__setattr__(
            self, "learning_evidence", _freeze_mapping(self.learning_evidence)
        )
        object.__setattr__(
            self,
            "practice_performance",
            _freeze_mapping(self.practice_performance),
        )
        object.__setattr__(
            self, "mock_performance", _freeze_mapping(self.mock_performance)
        )
        object.__setattr__(
            self, "study_behaviour", _freeze_mapping(self.study_behaviour)
        )
        object.__setattr__(
            self, "study_consistency", _freeze_mapping(self.study_consistency)
        )
        object.__setattr__(self, "streaks", _freeze_mapping(self.streaks))
        object.__setattr__(
            self, "mission_completion", _freeze_mapping(self.mission_completion)
        )
        object.__setattr__(self, "facet_labels", _freeze_mapping(self.facet_labels))
        object.__setattr__(
            self,
            "limitations_codes",
            tuple(str(item) for item in self.limitations_codes if item),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            tuple(str(item) for item in self.provenance_refs if item),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "facet_labels": dict(self.facet_labels),
            "foundation_version": self.foundation_version,
            "learning_evidence": dict(self.learning_evidence),
            "limitations_codes": list(self.limitations_codes),
            "mission_completion": dict(self.mission_completion),
            "mock_performance": dict(self.mock_performance),
            "practice_performance": dict(self.practice_performance),
            "provenance_refs": list(self.provenance_refs),
            "streaks": dict(self.streaks),
            "student_id": self.student_id,
            "study_behaviour": dict(self.study_behaviour),
            "study_consistency": dict(self.study_consistency),
            "study_state": dict(self.study_state),
            "topic_mastery": dict(self.topic_mastery),
            "topic_progress": dict(self.topic_progress),
            "twin_id": self.twin_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())

    def to_learner_summary_opaque(self) -> dict[str, Any]:
        """Opaque StudentTwinPort-compatible learner summary."""
        mastery_payload = dict(self.topic_mastery.get("payload") or {})
        progress_payload = dict(self.topic_progress.get("payload") or {})
        streaks_payload = dict(self.streaks.get("payload") or {})
        mission_payload = dict(self.mission_completion.get("payload") or {})
        study_payload = dict(self.study_state.get("payload") or {})
        mastered = int(mastery_payload.get("mastered_topic_count") or 0)
        return {
            "display_name": "",
            "examination_label": str(study_payload.get("examination_label") or ""),
            "exam_countdown_days": study_payload.get("exam_countdown_days"),
            "preferences": dict(study_payload.get("preferences") or {}),
            "goals": tuple(study_payload.get("goals") or ()),
            "account": {},
            "statistics": {
                "total_study_minutes": int(
                    study_payload.get("total_study_minutes") or 0
                ),
                "sessions_completed": int(
                    study_payload.get("sessions_completed") or 0
                ),
                "topics_mastered": mastered,
                "current_exam_readiness": study_payload.get("exam_readiness"),
                "study_streak_days": int(streaks_payload.get("current_streak") or 0),
            },
            "student_id": self.student_id,
            "twin_id": self.twin_id,
            "foundation_version": self.foundation_version,
            "canonical_state": {
                "topic_mastery": dict(self.topic_mastery),
                "topic_progress": dict(self.topic_progress),
                "learning_evidence": dict(self.learning_evidence),
                "practice_performance": dict(self.practice_performance),
                "mock_performance": dict(self.mock_performance),
                "study_behaviour": dict(self.study_behaviour),
                "study_consistency": dict(self.study_consistency),
                "streaks": dict(self.streaks),
                "mission_completion": dict(self.mission_completion),
                "study_state": dict(self.study_state),
            },
            "facet_labels": dict(self.facet_labels),
            "progress_summary": {
                "topic_count": int(progress_payload.get("topic_count") or 0),
                "completed_count": int(progress_payload.get("completed_count") or 0),
                "mastered_topic_count": mastered,
            },
            "mission_summary": {
                "completed_count": int(mission_payload.get("completed_count") or 0),
                "missed_count": int(mission_payload.get("missed_count") or 0),
                "history_count": int(mission_payload.get("history_count") or 0),
            },
            "provenance_refs": list(self.provenance_refs),
            "limitations_codes": list(self.limitations_codes),
            "availability": self.availability,
            "unavailable_reason": self.unavailable_reason,
            "authority": AUTHORITY_DIGITAL_TWIN,
        }

    def to_readiness_summary_opaque(self) -> dict[str, Any]:
        study_payload = dict(self.study_state.get("payload") or {})
        streaks_payload = dict(self.streaks.get("payload") or {})
        readiness = dict(study_payload.get("readiness_overall") or {})
        score = readiness.get("score")
        if score is None:
            score = readiness.get("readiness_score")
        return {
            "examination_label": str(study_payload.get("examination_label") or ""),
            "exam_countdown_days": study_payload.get("exam_countdown_days"),
            "exam_readiness": score,
            "readiness_score": score,
            "readiness_label": str(
                readiness.get("label") or readiness.get("readiness_label") or ""
            ),
            "current_streak": streaks_payload.get("current_streak"),
            "longest_streak": streaks_payload.get("longest_streak"),
            "availability": self.study_state.get("availability")
            or AVAILABILITY_UNAVAILABLE,
            "unavailable_reason": self.study_state.get("unavailable_reason") or "",
            "twin_id": self.twin_id,
            "provenance_refs": list(self.provenance_refs),
            "limitations_codes": list(self.limitations_codes),
            "authority": AUTHORITY_DIGITAL_TWIN,
        }

    def to_learning_insights_opaque(self) -> dict[str, Any]:
        study_payload = dict(self.study_state.get("payload") or {})
        mastery_payload = dict(self.topic_mastery.get("payload") or {})
        practice_payload = dict(self.practice_performance.get("payload") or {})
        return {
            "completed_sessions": (),
            "total_study_minutes": int(study_payload.get("total_study_minutes") or 0),
            "readiness_progression": (),
            "mastered_topics": tuple(mastery_payload.get("mastered_topic_ids") or ()),
            "revision_history": (),
            "recent_achievements": (),
            "sessions_completed": int(study_payload.get("sessions_completed") or 0),
            "topics_mastered": int(mastery_payload.get("mastered_topic_count") or 0),
            "practice_attempt_count": int(practice_payload.get("attempt_count") or 0),
            "canonical_state": self.to_canonical_dict(),
            "facet_labels": dict(self.facet_labels),
            "student_id": self.student_id,
            "twin_id": self.twin_id,
            "provenance_refs": list(self.provenance_refs),
            "limitations_codes": list(self.limitations_codes),
            "availability": self.availability,
            "unavailable_reason": self.unavailable_reason,
            "authority": AUTHORITY_DIGITAL_TWIN,
        }


class StudentDigitalTwinFoundation:
    """Assemble CanonicalLearnerState from Runtime A via MS-004 seams.

    Rules:
    - MAY read TwinRuntimeEvidence / TwinFacetBundle / TwinSnapshot
    - MUST NOT write Runtime A, invent mastery, or fabricate mocks
    - Identical evidence + as_of → identical serialize()
    """

    FOUNDATION_ID = "student_digital_twin_foundation"
    FOUNDATION_VERSION = FOUNDATION_VERSION

    def __init__(
        self,
        *,
        enabled: bool = True,
        facet_assembler: TwinFacetAssembler | None = None,
        snapshot_builder: TwinSnapshotBuilder | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._facet_assembler = facet_assembler or TwinFacetAssembler(enabled=True)
        self._snapshot_builder = snapshot_builder

    @property
    def foundation_id(self) -> str:
        return self.FOUNDATION_ID

    @property
    def foundation_version(self) -> str:
        return self.FOUNDATION_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def unavailable_state(
        self,
        *,
        student_id: str = "",
        as_of: str | None = None,
        reason: str = REASON_FOUNDATION_FLAG_OFF,
    ) -> CanonicalLearnerState:
        block = _unavailable_block(reason=reason)
        return CanonicalLearnerState(
            student_id=student_id,
            as_of=as_of,
            foundation_version=FOUNDATION_VERSION,
            twin_id="",
            study_state=block,
            topic_mastery=block,
            topic_progress=block,
            learning_evidence=block,
            practice_performance=block,
            mock_performance=_unavailable_block(
                reason=REASON_MOCK_NOT_DISTINGUISHED,
                source_field=FIELD_STUDY_ATTEMPTS,
            ),
            study_behaviour=block,
            study_consistency=block,
            streaks=block,
            mission_completion=block,
            limitations_codes=(reason,),
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
        )

    def assemble(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        evidence: TwinRuntimeEvidence | None = None,
        facet_bundle: TwinFacetBundle | None = None,
        snapshot: TwinSnapshot | None = None,
    ) -> CanonicalLearnerState:
        """Assemble canonical foundation state for a student.

        When ``evidence`` / ``facet_bundle`` are omitted, collects via the
        TwinFacetAssembler (Runtime A read-only).
        """
        if not self._enabled:
            return self.unavailable_state(
                student_id=student_id,
                as_of=as_of,
                reason=REASON_FOUNDATION_FLAG_OFF,
            )

        sid = (student_id or "").strip()
        if not sid:
            return self.unavailable_state(
                student_id="",
                as_of=as_of,
                reason=REASON_INVALID_STUDENT_ID,
            )

        runtime_evidence = evidence
        bundle = facet_bundle
        if runtime_evidence is None:
            runtime_evidence = self._facet_assembler.collect_evidence(
                sid, as_of=as_of
            )
        if bundle is None:
            bundle = self._facet_assembler.synthesise_from_evidence(
                runtime_evidence
            )

        resolved_snapshot = snapshot
        if resolved_snapshot is None and self._snapshot_builder is not None:
            try:
                resolved_snapshot = self._snapshot_builder.build_from_bundle(
                    bundle,
                    generated_at=as_of or runtime_evidence.as_of,
                )
            except Exception:  # noqa: BLE001
                resolved_snapshot = None

        return self._project_state(
            sid,
            as_of=as_of or getattr(runtime_evidence, "as_of", None),
            evidence=runtime_evidence,
            facet_bundle=bundle,
            snapshot=resolved_snapshot,
        )

    def _project_state(
        self,
        student_id: str,
        *,
        as_of: str | None,
        evidence: TwinRuntimeEvidence,
        facet_bundle: TwinFacetBundle | None,
        snapshot: TwinSnapshot | None,
    ) -> CanonicalLearnerState:
        limitations: list[str] = []
        provenance: list[str] = []

        topic_progress = self._topic_progress_block(evidence, limitations, provenance)
        topic_mastery = self._topic_mastery_block(evidence, limitations, provenance)
        learning_evidence = self._learning_evidence_block(
            evidence, limitations, provenance
        )
        practice_performance = self._practice_performance_block(
            evidence, limitations, provenance
        )
        mock_performance = _unavailable_block(
            reason=REASON_MOCK_NOT_DISTINGUISHED,
            source_field=FIELD_STUDY_ATTEMPTS,
        )
        limitations.append(REASON_MOCK_NOT_DISTINGUISHED)
        mission_completion = self._mission_completion_block(
            evidence, limitations, provenance
        )
        streaks = self._streaks_block(evidence, limitations, provenance)
        study_state = self._study_state_block(evidence, limitations, provenance)
        study_behaviour, study_consistency, facet_labels = self._behaviour_blocks(
            facet_bundle, limitations, provenance
        )

        twin_id = ""
        if snapshot is not None:
            twin_id = str(snapshot.twin_id or "")
            provenance.append(
                f"twin_snapshot:{twin_id}" if twin_id else "twin_snapshot"
            )
        if not twin_id:
            twin_id = f"twin-foundation-{student_id}"

        ordered_limitations = tuple(dict.fromkeys(limitations))
        ordered_provenance = tuple(dict.fromkeys(provenance))
        return CanonicalLearnerState(
            student_id=student_id,
            as_of=as_of,
            foundation_version=FOUNDATION_VERSION,
            twin_id=twin_id,
            study_state=study_state,
            topic_mastery=topic_mastery,
            topic_progress=topic_progress,
            learning_evidence=learning_evidence,
            practice_performance=practice_performance,
            mock_performance=mock_performance,
            study_behaviour=study_behaviour,
            study_consistency=study_consistency,
            streaks=streaks,
            mission_completion=mission_completion,
            facet_labels=facet_labels,
            limitations_codes=ordered_limitations,
            provenance_refs=ordered_provenance,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )

    def _topic_progress_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_TOPIC_PROGRESS):
            reason = evidence.unavailable_reason(FIELD_TOPIC_PROGRESS) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"topic_progress:{reason}")
            return _unavailable_block(
                reason=reason, source_field=FIELD_TOPIC_PROGRESS
            )
        rows = list(evidence.topic_progress)
        refs = [f"topic_progress:{row.get('topic_progress_id')}" for row in rows]
        provenance.extend(refs)
        provenance.append(FIELD_TOPIC_PROGRESS)
        completed = sum(1 for row in rows if bool(row.get("completed")))
        return _available_block(
            payload={
                "topics": [
                    {
                        "topic_id": str(row.get("topic_id") or ""),
                        "topic_name": str(row.get("topic_name") or ""),
                        "current_stage": str(row.get("current_stage") or ""),
                        "completed": bool(row.get("completed")),
                        "revision_count": int(row.get("revision_count") or 0),
                        "last_reviewed": row.get("last_reviewed"),
                        "next_review_date": row.get("next_review_date"),
                    }
                    for row in rows
                ],
                "topic_count": len(rows),
                "completed_count": completed,
            },
            evidence_refs=tuple(refs),
            source_field=FIELD_TOPIC_PROGRESS,
        )

    def _topic_mastery_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_TOPIC_PROGRESS):
            reason = evidence.unavailable_reason(FIELD_TOPIC_PROGRESS) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"topic_mastery:{reason}")
            return _unavailable_block(
                reason=reason, source_field=FIELD_TOPIC_PROGRESS
            )
        rows = list(evidence.topic_progress)
        mastered_ids = [
            str(row.get("topic_id") or "")
            for row in rows
            if str(row.get("current_stage") or "").lower() in {"mastered", "completed"}
            or bool(row.get("completed"))
        ]
        mastered_ids = [tid for tid in mastered_ids if tid]
        refs = [f"topic_progress:{row.get('topic_progress_id')}" for row in rows]
        provenance.append(FIELD_TOPIC_PROGRESS)
        return _available_block(
            payload={
                "topics": [
                    {
                        "topic_id": str(row.get("topic_id") or ""),
                        "mastery_score": row.get("mastery_score"),
                        "average_accuracy": row.get("average_accuracy"),
                        "confidence": str(row.get("confidence") or ""),
                        "current_stage": str(row.get("current_stage") or ""),
                    }
                    for row in rows
                ],
                "mastered_topic_ids": mastered_ids,
                "mastered_topic_count": len(dict.fromkeys(mastered_ids)),
            },
            evidence_refs=tuple(refs),
            source_field=FIELD_TOPIC_PROGRESS,
        )

    def _learning_evidence_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_STUDY_ATTEMPTS):
            reason = evidence.unavailable_reason(FIELD_STUDY_ATTEMPTS) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"learning_evidence:{reason}")
            return _unavailable_block(
                reason=reason, source_field=FIELD_STUDY_ATTEMPTS
            )
        attempts = list(evidence.study_attempts)
        refs = [f"attempt:{row.get('attempt_id')}" for row in attempts]
        provenance.append(FIELD_STUDY_ATTEMPTS)
        return _available_block(
            payload={
                "attempt_count": len(attempts),
                "attempt_ids": [str(row.get("attempt_id") or "") for row in attempts],
                "attempts": [
                    {
                        "attempt_id": str(row.get("attempt_id") or ""),
                        "mission_id": str(row.get("mission_id") or ""),
                        "topic_id": row.get("topic_id"),
                        "study_date": row.get("study_date"),
                        "duration_minutes": row.get("duration_minutes"),
                    }
                    for row in attempts
                ],
            },
            evidence_refs=tuple(refs),
            source_field=FIELD_STUDY_ATTEMPTS,
        )

    def _practice_performance_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_STUDY_ATTEMPTS):
            reason = evidence.unavailable_reason(FIELD_STUDY_ATTEMPTS) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"practice_performance:{reason}")
            return _unavailable_block(
                reason=reason, source_field=FIELD_STUDY_ATTEMPTS
            )
        attempts = list(evidence.study_attempts)
        scored = [
            row
            for row in attempts
            if row.get("accuracy_pct") is not None
            or row.get("questions_attempted") is not None
        ]
        refs = [f"attempt:{row.get('attempt_id')}" for row in scored]
        provenance.append(FIELD_STUDY_ATTEMPTS)
        accuracies = [
            float(row["accuracy_pct"])
            for row in scored
            if row.get("accuracy_pct") is not None
        ]
        mean_accuracy = (
            round(sum(accuracies) / len(accuracies), 4) if accuracies else None
        )
        return _available_block(
            payload={
                "attempt_count": len(scored),
                "mean_accuracy_pct": mean_accuracy,
                "attempts": [
                    {
                        "attempt_id": str(row.get("attempt_id") or ""),
                        "topic_id": row.get("topic_id"),
                        "questions_attempted": row.get("questions_attempted"),
                        "questions_correct": row.get("questions_correct"),
                        "accuracy_pct": row.get("accuracy_pct"),
                    }
                    for row in scored
                ],
            },
            evidence_refs=tuple(refs),
            source_field=FIELD_STUDY_ATTEMPTS,
        )

    def _mission_completion_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_MISSION):
            reason = evidence.unavailable_reason(FIELD_MISSION) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"mission_completion:{reason}")
            return _unavailable_block(reason=reason, source_field=FIELD_MISSION)
        mission = dict(evidence.mission)
        history = list(mission.get("history") or [])
        completed = [
            row
            for row in history
            if str(row.get("status") or "").lower() in COMPLETED_MISSION_STATUSES
        ]
        missed = [
            row
            for row in history
            if str(row.get("status") or "").lower() in MISSED_MISSION_STATUSES
        ]
        refs = [f"mission:{row.get('mission_id')}" for row in history]
        provenance.append(FIELD_MISSION)
        today = mission.get("today")
        return _available_block(
            payload={
                "today": None if today is None else dict(today),
                "history_count": int(mission.get("history_count") or len(history)),
                "completed_count": len(completed),
                "missed_count": len(missed),
                "completed_mission_ids": [
                    str(row.get("mission_id") or "") for row in completed
                ],
            },
            evidence_refs=tuple(refs),
            source_field=FIELD_MISSION,
        )

    def _streaks_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        if not evidence.is_available(FIELD_READINESS):
            reason = evidence.unavailable_reason(FIELD_READINESS) or (
                REASON_RUNTIME_A_UNAVAILABLE
            )
            limitations.append(f"streaks:{reason}")
            return _unavailable_block(reason=reason, source_field=FIELD_READINESS)
        readiness = dict(evidence.readiness)
        streaks = dict(readiness.get("streaks") or {})
        if not streaks and "current_streak" not in readiness:
            # Older readiness payloads without streak pass-through.
            limitations.append("streaks:not_present_in_readiness_payload")
            return _unavailable_block(
                reason="streaks_not_present_in_readiness_payload",
                source_field=FIELD_READINESS,
            )
        current = streaks.get("current_streak", readiness.get("current_streak"))
        longest = streaks.get("longest_streak", readiness.get("longest_streak"))
        provenance.append(FIELD_READINESS)
        return _available_block(
            payload={
                "current_streak": (
                    None if current is None else int(current)
                ),
                "longest_streak": (
                    None if longest is None else int(longest)
                ),
            },
            evidence_refs=(FIELD_READINESS,),
            source_field=FIELD_READINESS,
        )

    def _study_state_block(
        self,
        evidence: TwinRuntimeEvidence,
        limitations: list[str],
        provenance: list[str],
    ) -> dict[str, Any]:
        goals_available = evidence.is_available(FIELD_STUDENT_GOALS)
        readiness_available = evidence.is_available(FIELD_READINESS)
        attempts_available = evidence.is_available(FIELD_STUDY_ATTEMPTS)
        if not (goals_available or readiness_available or attempts_available):
            limitations.append("study_state:runtime_a_unavailable")
            return _unavailable_block(
                reason=REASON_RUNTIME_A_UNAVAILABLE,
                source_field=FIELD_STUDENT_GOALS,
            )

        goals = dict(evidence.student_goals) if goals_available else {}
        readiness = dict(evidence.readiness) if readiness_available else {}
        overall = dict(readiness.get("overall") or {})
        attempts = list(evidence.study_attempts) if attempts_available else []
        total_minutes = sum(
            int(row.get("duration_minutes") or 0)
            for row in attempts
            if row.get("duration_minutes") is not None
        )
        if goals_available:
            provenance.append(FIELD_STUDENT_GOALS)
        if readiness_available:
            provenance.append(FIELD_READINESS)
        if attempts_available:
            provenance.append(FIELD_STUDY_ATTEMPTS)

        goal_items = []
        if goals.get("target_exam_date") or goals.get("exam_date"):
            goal_items.append(
                {
                    "target_exam_date": goals.get("target_exam_date")
                    or goals.get("exam_date"),
                    "planned_weekly_hours": goals.get("planned_weekly_hours"),
                }
            )
        return _available_block(
            payload={
                "lifecycle_stage": evidence.lifecycle_stage,
                "examination_label": str(
                    goals.get("exam_name")
                    or goals.get("examination_label")
                    or evidence.curriculum.get("exam_name")
                    or ""
                ),
                "exam_countdown_days": goals.get("exam_countdown_days"),
                "exam_readiness": (
                    overall.get("score") or overall.get("readiness_score")
                ),
                "readiness_overall": overall,
                "goals": goal_items,
                "preferences": {
                    "preferred_session_minutes": goals.get("preferred_session_minutes"),
                    "planned_weekly_hours": goals.get("planned_weekly_hours"),
                },
                "sessions_completed": len(attempts),
                "total_study_minutes": total_minutes,
            },
            evidence_refs=tuple(
                r
                for r in (
                    FIELD_STUDENT_GOALS if goals_available else "",
                    FIELD_READINESS if readiness_available else "",
                    FIELD_STUDY_ATTEMPTS if attempts_available else "",
                )
                if r
            ),
            source_field=FIELD_STUDENT_GOALS,
        )

    def _behaviour_blocks(
        self,
        facet_bundle: TwinFacetBundle | None,
        limitations: list[str],
        provenance: list[str],
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
        labels: dict[str, str] = {}
        if facet_bundle is None:
            limitations.append("study_behaviour:facets_unavailable")
            block = _unavailable_block(reason="facets_unavailable")
            return block, block, labels

        profile = getattr(facet_bundle, "profile", None)
        if profile is None:
            limitations.append("study_behaviour:profile_unavailable")
            block = _unavailable_block(reason="profile_unavailable")
            return block, block, labels

        rhythm = getattr(profile, "learning_rhythm", None)
        habits = getattr(profile, "session_habits", None)
        consistency = getattr(profile, "consistency", None)
        persistence = getattr(profile, "persistence", None)

        def _facet_payload(facet: Any, note_attr: str) -> dict[str, Any]:
            if facet is None:
                return _unavailable_block(reason="facet_missing")
            availability = str(getattr(facet, "availability", "") or "")
            label = str(getattr(facet, "label", "") or "")
            if label:
                labels[str(getattr(facet, "facet_name", "") or note_attr)] = label
            if availability != AVAILABILITY_AVAILABLE:
                return _unavailable_block(
                    reason=str(
                        getattr(facet, "unavailable_reason", "") or "unavailable"
                    )
                )
            refs = tuple(getattr(facet, "evidence_refs", ()) or ())
            provenance.extend(str(r) for r in refs)
            return _available_block(
                payload={
                    "label": label,
                    "note": str(getattr(facet, note_attr, "") or ""),
                    "evidence_refs": list(refs),
                },
                evidence_refs=refs,
                source_field="twin_facet",
            )

        # Attach stable label keys from known facet names.
        for name, facet, note in (
            ("learning_rhythm", rhythm, "cadence_note"),
            ("session_habits", habits, "habits_note"),
            ("consistency", consistency, "adherence_note"),
            ("persistence", persistence, "continuity_note"),
        ):
            if facet is not None:
                label = str(getattr(facet, "label", "") or "")
                if label:
                    labels[name] = label

        behaviour = _available_block(
            payload={
                "learning_rhythm": _facet_payload(rhythm, "cadence_note"),
                "session_habits": _facet_payload(habits, "habits_note"),
                "persistence": _facet_payload(persistence, "continuity_note"),
            },
            evidence_refs=(),
            source_field="twin_facet",
        )
        consistency_block = _facet_payload(consistency, "adherence_note")
        provenance.append("twin_facet:behaviour")
        return behaviour, consistency_block, labels


def build_student_digital_twin_foundation(
    *,
    enabled: bool,
    facet_assembler: TwinFacetAssembler | None = None,
    snapshot_builder: TwinSnapshotBuilder | None = None,
) -> StudentDigitalTwinFoundation | None:
    """DI helper — construct Foundation only when Digital Twin is ON."""
    if not enabled:
        return None
    assembler = facet_assembler or build_twin_facet_assembler(enabled=True)
    builder = snapshot_builder
    if builder is None and assembler is not None:
        builder = build_twin_snapshot_builder(
            enabled=True, facet_assembler=assembler
        )
    return StudentDigitalTwinFoundation(
        enabled=True,
        facet_assembler=assembler,
        snapshot_builder=builder,
    )


__all__ = [
    "FOUNDATION_VERSION",
    "REASON_FOUNDATION_FLAG_OFF",
    "REASON_INVALID_STUDENT_ID",
    "REASON_MOCK_NOT_DISTINGUISHED",
    "REASON_RUNTIME_A_UNAVAILABLE",
    "CanonicalLearnerState",
    "StudentDigitalTwinFoundation",
    "build_student_digital_twin_foundation",
]
