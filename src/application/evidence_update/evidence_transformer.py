"""EvidenceTransformer — CapturedEvidence → EvidenceRecord.

Deterministic mapping of observational session facts into Educational OS
evidence objects. Never diagnoses, recommends, plans study, or invokes AI.
"""

from __future__ import annotations

from datetime import UTC, datetime

from application.errors import ApplicationError
from application.evidence_capture.captured_evidence import CapturedEvidence
from application.evidence_capture.learning_session_outcome import (
    LearningSessionOutcome,
)
from application.evidence_update.evidence_update_request import (
    EvidenceUpdateRequest,
)
from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceContext,
    EvidenceContextId,
    EvidenceItem,
    EvidenceItemId,
    EvidenceItemKind,
    EvidenceRecord,
    EvidenceSource,
    EvidenceSourceId,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceTimestamp,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference


class EvidenceTransformError(ApplicationError):
    """Raised when captured evidence cannot become a valid EvidenceRecord."""


class EvidenceTransformer:
    """Transform captured session evidence into an ``EvidenceRecord``.

    Student self-report fields become ``REFLECTION`` observation items.
    Recording confidence and epistemic strength describe observational warrant
    of the capture — not mastery or diagnosis of the learner.
    """

    @classmethod
    def transform(cls, request: EvidenceUpdateRequest) -> EvidenceRecord:
        """Build an ``EvidenceRecord`` from an ``EvidenceUpdateRequest``.

        Args:
            request: Validated update request containing ``CapturedEvidence``.

        Returns:
            Domain ``EvidenceRecord`` ready for repository storage.

        Raises:
            EvidenceTransformError: When required facts are missing or invalid.
        """
        if request is None or not isinstance(request, EvidenceUpdateRequest):
            raise EvidenceTransformError("request must be an EvidenceUpdateRequest")
        return cls.from_captured(
            request.captured,
            concept_ids=request.concept_ids,
            learning_episode_ids=request.learning_episode_ids,
        )

    @classmethod
    def from_captured(
        cls,
        captured: CapturedEvidence,
        *,
        concept_ids: tuple[str, ...] = (),
        learning_episode_ids: tuple[str, ...] = (),
    ) -> EvidenceRecord:
        """Map ``CapturedEvidence`` into a domain ``EvidenceRecord``."""
        if not isinstance(captured, CapturedEvidence):
            raise EvidenceTransformError("captured must be a CapturedEvidence")

        outcome = captured.outcome
        student_id = (outcome.student_id or "").strip()
        if not student_id:
            raise EvidenceTransformError("student_id is required on captured evidence")

        occurred_at = cls._resolve_occurred_at(captured, outcome)
        items = cls._build_items(captured, outcome)
        if not items:
            raise EvidenceTransformError(
                "captured evidence produced no observational items"
            )

        concept_id_objs = tuple(ConceptId(cid) for cid in concept_ids)
        episode_id_objs = tuple(
            LearningEpisodeId(eid) for eid in learning_episode_ids
        )
        concept_refs = tuple(
            ConceptReference(concept_id=cid) for cid in concept_id_objs
        )

        try:
            return EvidenceRecord.record(
                evidence_id=EvidenceId(captured.evidence_id),
                student_id=student_id,
                items=items,
                source=cls._build_source(captured),
                context=cls._build_context(
                    captured,
                    outcome,
                    concept_refs=concept_refs,
                    episode_ids=episode_id_objs,
                ),
                confidence=cls._recording_confidence(outcome),
                strength=EvidenceStrength.weak(),
                timestamp=EvidenceTimestamp(occurred_at=occurred_at),
                known_concept_ids=(
                    frozenset(concept_id_objs) if concept_id_objs else None
                ),
                known_episode_ids=(
                    frozenset(episode_id_objs) if episode_id_objs else None
                ),
                concept_references=list(concept_refs),
                learning_episode_ids=list(episode_id_objs),
            )
        except EducationalDomainError as exc:
            raise EvidenceTransformError(str(exc)) from exc

    @classmethod
    def _resolve_occurred_at(
        cls,
        captured: CapturedEvidence,
        outcome: LearningSessionOutcome,
    ) -> datetime:
        stamp = captured.captured_at
        if not isinstance(stamp, datetime):
            raise EvidenceTransformError("captured_at must be a datetime")
        if stamp.tzinfo is None:
            raise EvidenceTransformError(
                "captured_at must be timezone-aware"
            )
        # Prefer capture stamp; session_completed is already folded into capture.
        _ = outcome  # retained for explicit coupling to session facts
        return stamp.astimezone(UTC)

    @classmethod
    def _build_source(cls, captured: CapturedEvidence) -> EvidenceSource:
        provenance = (captured.provenance or "").strip() or "study_session_reflection"
        return EvidenceSource(
            source_id=EvidenceSourceId(f"source:{captured.evidence_id}"),
            kind=EvidenceSourceKind.REFLECTION_CAPTURE,
            label="Study session reflection",
            channel=provenance,
        )

    @classmethod
    def _build_context(
        cls,
        captured: CapturedEvidence,
        outcome: LearningSessionOutcome,
        *,
        concept_refs: tuple[ConceptReference, ...],
        episode_ids: tuple[LearningEpisodeId, ...],
    ) -> EvidenceContext:
        title = (outcome.mission_title or "").strip()
        mission = (outcome.mission_id or "").strip()
        session = (outcome.session_id or "").strip()
        parts = [
            "Study session reflection",
            f"mission={mission}" if mission else "",
            f"session={session}" if session else "",
            f"title={title}" if title else "",
            f"completion={outcome.completion_status.value}",
        ]
        situation = "; ".join(part for part in parts if part)
        return EvidenceContext(
            context_id=EvidenceContextId(f"ctx:{captured.evidence_id}"),
            situation=situation,
            learning_dimension=LearningDimension.UNDERSTANDING,
            concept_references=concept_refs,
            learning_episode_ids=episode_ids,
        )

    @classmethod
    def _recording_confidence(
        cls, outcome: LearningSessionOutcome
    ) -> ConfidenceMeasure:
        """Observational recording certainty — not student self-confidence."""
        filled = sum(
            1
            for value in (
                outcome.confidence,
                outcome.difficulty,
                outcome.weak_concept,
                outcome.student_notes,
                outcome.reflection_summary,
            )
            if (value or "").strip()
        )
        if filled >= 3:
            return ConfidenceMeasure.of(ConfidenceLevel.MEDIUM)
        if filled >= 1:
            return ConfidenceMeasure.of(ConfidenceLevel.LOW)
        return ConfidenceMeasure.of(ConfidenceLevel.VERY_LOW)

    @classmethod
    def _build_items(
        cls,
        captured: CapturedEvidence,
        outcome: LearningSessionOutcome,
    ) -> list[EvidenceItem]:
        items: list[EvidenceItem] = []
        index = 1

        def add(observation: str) -> None:
            nonlocal index
            text = (observation or "").strip()
            if not text:
                return
            items.append(
                EvidenceItem(
                    item_id=EvidenceItemId(
                        f"item:{captured.evidence_id}:{index:02d}"
                    ),
                    kind=EvidenceItemKind.REFLECTION,
                    observation=text,
                )
            )
            index += 1

        duration = outcome.actual_duration_seconds
        duration_part = (
            f"; duration_seconds={duration}" if duration is not None else ""
        )
        add(
            "session_completion="
            f"{outcome.completion_status.value}{duration_part}"
        )
        if (outcome.confidence or "").strip():
            add(f"student_reported_confidence={outcome.confidence.strip()}")
        if (outcome.difficulty or "").strip():
            add(f"student_reported_difficulty={outcome.difficulty.strip()}")
        if (outcome.weak_concept or "").strip():
            add(f"student_noted_weak_concept={outcome.weak_concept.strip()}")
        if (outcome.student_notes or "").strip():
            add(f"student_notes={outcome.student_notes.strip()}")
        if (outcome.reflection_summary or "").strip():
            add(f"reflection_summary={outcome.reflection_summary.strip()}")
        return items
