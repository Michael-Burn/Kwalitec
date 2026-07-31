"""Build a sitting Evidence Package from session candidates (EV-001B).

LearningSessionRuntime / adapters emit candidates. This builder assembles
one package for EducationalEvidenceAuthority validation. It does not decide
sufficiency.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    SessionEvidencePackage,
)
from app.application.learning_session.dto.finish_review import FinishReviewVerdict
from app.application.learning_session.educational_flow import EducationalStage

_STAGE_TO_COMPLETED_TYPE: dict[str, RuntimeEvidenceType] = {
    EducationalStage.READ.value: RuntimeEvidenceType.READING_COMPLETED,
    EducationalStage.WORKED_EXAMPLE.value: RuntimeEvidenceType.WORKED_EXAMPLE_COMPLETED,
    EducationalStage.PRACTICE.value: RuntimeEvidenceType.PRACTICE_ATTEMPTED,
}


class EvidencePackageBuilder:
    """Assemble a Generated Evidence Package for one sitting."""

    def __init__(self, *, id_factory=None, clock=None) -> None:
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._clock = clock or (lambda: datetime.now(tz=UTC))

    def emit(
        self,
        *,
        type_id: RuntimeEvidenceType | str,
        student_id: str,
        session_id: str,
        topic_id: str = "",
        mission_instance_id: str = "",
        stage: str = "",
        activity_id: str = "",
        payload: dict[str, Any] | None = None,
    ) -> CandidateObservation:
        """Create one Generated candidate observation."""
        return CandidateObservation.create(
            observation_id=f"obs-{self._id_factory()}",
            type_id=type_id,
            student_id=student_id,
            session_id=session_id,
            recorded_at=self._clock(),
            topic_id=topic_id,
            mission_instance_id=mission_instance_id,
            stage=stage,
            activity_id=activity_id,
            payload=payload,
        )

    def observation_for_stage_response(
        self,
        *,
        stage: str,
        student_id: str,
        session_id: str,
        topic_id: str = "",
        mission_instance_id: str = "",
        activity_id: str = "",
        response: str = "",
        scored_correct: bool | None = None,
        structured: bool = False,
        score_payload: dict[str, Any] | None = None,
    ) -> CandidateObservation:
        """Map an activity stage response to the EV-001A type catalogue.

        When ``structured`` is True and the practice attempt was scored,
        emit EV-RT-40 (structured question results). Otherwise scored
        practice maps to EV-RT-07 / EV-RT-08.
        """
        stage_key = (stage or "").strip().lower()
        extra = dict(score_payload or {})
        if stage_key == EducationalStage.PRACTICE.value:
            if structured and scored_correct is not None:
                type_id = RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS
            elif scored_correct is True:
                type_id = RuntimeEvidenceType.PRACTICE_CORRECT
            elif scored_correct is False:
                type_id = RuntimeEvidenceType.PRACTICE_INCORRECT
            elif (response or "").strip():
                type_id = RuntimeEvidenceType.PRACTICE_ATTEMPTED
            else:
                type_id = RuntimeEvidenceType.PRACTICE_PARTIAL_UNSCORED
        else:
            type_id = _STAGE_TO_COMPLETED_TYPE.get(
                stage_key, RuntimeEvidenceType.PRACTICE_ATTEMPTED
            )
        payload: dict[str, Any] = {
            "response_length": len((response or "").strip()),
            "scored_correct": scored_correct,
            **extra,
        }
        if type_id is RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS:
            if "accuracy" not in payload and scored_correct is not None:
                payload["accuracy"] = 1.0 if scored_correct else 0.0
            if "outcome" not in payload and scored_correct is not None:
                payload["outcome"] = "correct" if scored_correct else "incorrect"
        return self.emit(
            type_id=type_id,
            student_id=student_id,
            session_id=session_id,
            topic_id=topic_id,
            mission_instance_id=mission_instance_id,
            stage=stage_key,
            activity_id=activity_id,
            payload=payload,
        )

    def observation_for_finish_review(
        self,
        *,
        verdict: str,
        student_id: str,
        session_id: str,
        topic_id: str = "",
        mission_instance_id: str = "",
        notes: str | None = None,
    ) -> CandidateObservation:
        mapping = {
            FinishReviewVerdict.YES.value: RuntimeEvidenceType.FINISH_REVIEW_YES,
            FinishReviewVerdict.PARTIALLY.value: (
                RuntimeEvidenceType.FINISH_REVIEW_PARTIALLY
            ),
            FinishReviewVerdict.NO.value: RuntimeEvidenceType.FINISH_REVIEW_NO,
        }
        key = (verdict or "").strip().lower()
        type_id = mapping.get(key, RuntimeEvidenceType.FINISH_REVIEW_YES)
        return self.emit(
            type_id=type_id,
            student_id=student_id,
            session_id=session_id,
            topic_id=topic_id,
            mission_instance_id=mission_instance_id,
            stage="finish_review",
            payload={"verdict": key, "notes": notes or ""},
        )

    def build(
        self,
        *,
        student_id: str,
        session_id: str,
        observations: list[CandidateObservation] | tuple[CandidateObservation, ...],
        mission_instance_id: str = "",
        topic_id: str = "",
        topic_title: str = "",
        curriculum_identity: str = "",
        learning_objectives: tuple[str, ...] | list[str] = (),
        finish_review_verdict: str | None = None,
        finish_review_notes: str | None = None,
        session_metadata: dict[str, Any] | None = None,
    ) -> SessionEvidencePackage:
        """Assemble one Generated package for Authority validation."""
        return SessionEvidencePackage.create(
            package_id=f"evp-{self._id_factory()}",
            student_id=student_id,
            session_id=session_id,
            mission_instance_id=mission_instance_id,
            topic_id=topic_id,
            topic_title=topic_title,
            curriculum_identity=curriculum_identity,
            learning_objectives=learning_objectives,
            observations=observations,
            finish_review_verdict=finish_review_verdict,
            finish_review_notes=finish_review_notes,
            session_metadata=session_metadata,
            provenance="learning_session_runtime",
            created_at=self._clock(),
        )
