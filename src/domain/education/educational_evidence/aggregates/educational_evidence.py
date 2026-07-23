"""EducationalEvidence aggregate — the Educational Evidence Engine's product.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model, Evidence rules,
    Twin Lifecycle)
Concept
    Educational Evidence

Every meaningful student interaction is transformed into one immutable,
deterministic ``EducationalEvidence`` instance through a ``record_*``
factory on this class. Evidence describes educational meaning — never a
UI event, a diagnosis, or a recommendation.
"""

from __future__ import annotations

from datetime import datetime

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import (
    CheckpointId,
    CompetencyId,
    EvidenceId,
    MissionId,
    SubjectId,
)
from domain.education.educational_evidence.policies.evidence_normalisation_policy import (  # noqa: E501
    EvidenceNormalisationPolicy,
)
from domain.education.educational_evidence.policies.evidence_validation_policy import (
    EvidenceValidationPolicy,
)
from domain.education.educational_evidence.value_objects.evidence_context import (
    EvidenceContext,
)
from domain.education.educational_evidence.value_objects.evidence_metadata import (
    EvidenceMetadata,
    Primitive,
)
from domain.education.educational_evidence.value_objects.evidence_snapshot import (
    EvidenceSnapshot,
)
from domain.education.educational_evidence.value_objects.evidence_source import (
    EvidenceSource,
)
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.educational_evidence.value_objects.evidence_weight import (
    EvidenceWeight,
)
from domain.education.educational_evidence.value_objects.learning_context import (
    LearningContext,
)
from domain.education.educational_evidence.value_objects.learning_environment import (
    LearningEnvironment,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId

# Deterministic default epistemic weight per evidence type. Callers may
# always override via the ``weight`` keyword argument on a ``record_*``
# factory. No randomness; no wall-clock or estimation involved.
_DEFAULT_WEIGHT_MAGNITUDE: dict[EvidenceType, float] = {
    EvidenceType.QUESTION_ANSWERED: 0.55,
    EvidenceType.QUESTION_INCORRECT: 0.50,
    EvidenceType.REFLECTION_RECORDED: 0.20,
    EvidenceType.MISSION_COMPLETED: 0.40,
    EvidenceType.MISSION_ABANDONED: 0.30,
    EvidenceType.STUDY_SESSION_STARTED: 0.10,
    EvidenceType.STUDY_SESSION_COMPLETED: 0.30,
    EvidenceType.HINT_REQUESTED: 0.15,
    EvidenceType.REVIEW_COMPLETED: 0.45,
    EvidenceType.CHECKPOINT_REACHED: 0.50,
    EvidenceType.CONFIDENCE_REPORTED: 0.25,
    EvidenceType.GOAL_ACHIEVED: 0.50,
    EvidenceType.TIME_INVESTED: 0.10,
    EvidenceType.SUBJECT_VISITED: 0.10,
    EvidenceType.COMPETENCY_PRACTISED: 0.35,
}


def _coerce_subject_id(value: SubjectId | str) -> SubjectId:
    return value if isinstance(value, SubjectId) else SubjectId(value)


def _coerce_competency_id(value: CompetencyId | str) -> CompetencyId:
    return value if isinstance(value, CompetencyId) else CompetencyId(value)


def _coerce_mission_id(value: MissionId | str) -> MissionId:
    return value if isinstance(value, MissionId) else MissionId(value)


def _coerce_checkpoint_id(value: CheckpointId | str) -> CheckpointId:
    return value if isinstance(value, CheckpointId) else CheckpointId(value)


def _coerce_episode_id(value: LearningEpisodeId | str) -> LearningEpisodeId:
    return value if isinstance(value, LearningEpisodeId) else LearningEpisodeId(value)


def _coerce_timestamp(value: EvidenceTimestamp | datetime) -> EvidenceTimestamp:
    if isinstance(value, EvidenceTimestamp):
        return value
    return EvidenceTimestamp.of(value)


def _resolve_weight(
    evidence_type: EvidenceType, weight: EvidenceWeight | float | None
) -> EvidenceWeight:
    if weight is None:
        return EvidenceWeight.of(_DEFAULT_WEIGHT_MAGNITUDE[evidence_type])
    if isinstance(weight, EvidenceWeight):
        return weight
    if isinstance(weight, bool) or not isinstance(weight, int | float):
        raise EducationalInvariantViolation(
            "weight must be an EvidenceWeight or a real number",
            invariant="EducationalEvidence.weight.type",
        )
    return EvidenceWeight.of(float(weight))


def _build_context(
    *,
    learning_environment: LearningEnvironment,
    subject_id: SubjectId | str | None = None,
    competency_id: CompetencyId | str | None = None,
    mission_id: MissionId | str | None = None,
    checkpoint_id: CheckpointId | str | None = None,
    learning_episode_id: LearningEpisodeId | str | None = None,
) -> EvidenceContext:
    return EvidenceContext(
        learning_context=LearningContext(
            subject_id=(
                _coerce_subject_id(subject_id) if subject_id is not None else None
            ),
            competency_id=(
                _coerce_competency_id(competency_id)
                if competency_id is not None
                else None
            ),
            mission_id=(
                _coerce_mission_id(mission_id) if mission_id is not None else None
            ),
            checkpoint_id=(
                _coerce_checkpoint_id(checkpoint_id)
                if checkpoint_id is not None
                else None
            ),
            learning_episode_id=(
                _coerce_episode_id(learning_episode_id)
                if learning_episode_id is not None
                else None
            ),
        ),
        learning_environment=learning_environment,
    )


def _merge_metadata(
    required: dict[str, Primitive], extra_metadata: dict[str, Primitive] | None
) -> EvidenceMetadata:
    if extra_metadata:
        overlap = sorted(set(required) & set(extra_metadata))
        if overlap:
            raise EducationalInvariantViolation(
                f"metadata keys {overlap} are derived from this evidence "
                "factory and cannot be overridden",
                invariant="EducationalEvidence.metadata.reserved_key",
            )
        merged: dict[str, Primitive] = {**required, **extra_metadata}
    else:
        merged = dict(required)
    return EvidenceMetadata.of(**merged)


class EducationalEvidence:
    """Immutable educational evidence — the Twin's evidence spine.

    Every instance describes one meaningful student interaction in
    educational terms. Instances never mutate after construction; a
    correction is recorded as new evidence, never a silent edit.

    This aggregate does not estimate mastery, update
    ``StudentEducationalState``, update an ``EducationalDigitalTwin``, run
    recommendation logic, or perform any persistence. It only produces
    deterministic, internally-consistent evidence from explicit inputs.
    """

    def __init__(
        self,
        evidence_id: EvidenceId,
        student_id: str,
        evidence_type: EvidenceType,
        occurred_at: EvidenceTimestamp,
        source: EvidenceSource,
        context: EvidenceContext,
        weight: EvidenceWeight,
        metadata: EvidenceMetadata | None = None,
    ) -> None:
        self._evidence_id = EvidenceValidationPolicy.assert_identity(evidence_id)
        self._student_id = EvidenceValidationPolicy.assert_student_id(student_id)
        self._evidence_type = EvidenceValidationPolicy.assert_evidence_type(
            evidence_type
        )
        self._occurred_at = EvidenceValidationPolicy.assert_timestamp(occurred_at)
        self._source = EvidenceValidationPolicy.assert_source(source)
        self._context = EvidenceValidationPolicy.assert_context(context)
        self._weight = EvidenceValidationPolicy.assert_weight(weight)
        self._metadata = EvidenceValidationPolicy.assert_metadata(
            metadata if metadata is not None else EvidenceMetadata.empty()
        )
        EvidenceValidationPolicy.assert_context_matches_type(
            self._evidence_type, self._context
        )
        EvidenceValidationPolicy.assert_metadata_matches_type(
            self._evidence_type, self._metadata
        )

    # --- identity / read models (no setters; evidence is immutable) ---

    @property
    def evidence_id(self) -> EvidenceId:
        return self._evidence_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def evidence_type(self) -> EvidenceType:
        return self._evidence_type

    @property
    def occurred_at(self) -> EvidenceTimestamp:
        return self._occurred_at

    @property
    def source(self) -> EvidenceSource:
        return self._source

    @property
    def context(self) -> EvidenceContext:
        return self._context

    @property
    def weight(self) -> EvidenceWeight:
        return self._weight

    @property
    def metadata(self) -> EvidenceMetadata:
        return self._metadata

    def is_type(self, evidence_type: EvidenceType) -> bool:
        return self._evidence_type is evidence_type

    def references_subject(self, subject_id: SubjectId | str) -> bool:
        return self._context.learning_context.subject_id == _coerce_subject_id(
            subject_id
        )

    def references_competency(self, competency_id: CompetencyId | str) -> bool:
        return self._context.learning_context.competency_id == _coerce_competency_id(
            competency_id
        )

    def references_mission(self, mission_id: MissionId | str) -> bool:
        return self._context.learning_context.mission_id == _coerce_mission_id(
            mission_id
        )

    def references_checkpoint(self, checkpoint_id: CheckpointId | str) -> bool:
        return self._context.learning_context.checkpoint_id == _coerce_checkpoint_id(
            checkpoint_id
        )

    def references_learning_episode(
        self, learning_episode_id: LearningEpisodeId | str
    ) -> bool:
        return self._context.learning_context.learning_episode_id == _coerce_episode_id(
            learning_episode_id
        )

    # --- normalisation / snapshot ---

    def normalise(self) -> EducationalEvidence:
        """Return a canonically normalised copy of this evidence.

        Construction already enforces normalisation (metadata keys are
        always stored sorted; weight magnitude is always rounded with a
        band derived from it), so this is idempotent: calling it repeatedly
        never changes the result. It exists so callers can explicitly
        request and verify canonical form without depending on the
        constructor's internal shape.
        """
        return EducationalEvidence(
            evidence_id=self._evidence_id,
            student_id=self._student_id,
            evidence_type=self._evidence_type,
            occurred_at=self._occurred_at,
            source=self._source,
            context=self._context,
            weight=EvidenceNormalisationPolicy.normalise_weight(self._weight),
            metadata=EvidenceNormalisationPolicy.normalise_metadata(self._metadata),
        )

    def is_normalised(self) -> bool:
        """True when this evidence already equals its normalised form."""
        return self == self.normalise()

    def produce_snapshot(self) -> EvidenceSnapshot:
        """Produce an immutable, accurate read model of this evidence."""
        return EvidenceSnapshot(
            evidence_id=self._evidence_id,
            student_id=self._student_id,
            evidence_type=self._evidence_type,
            occurred_at=self._occurred_at,
            source=self._source,
            context=self._context,
            weight=self._weight,
            metadata=self._metadata,
        )

    # --- behaviour: the Educational Evidence Engine's factories ---

    @classmethod
    def record_question_answer(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        competency_id: CompetencyId | str,
        is_correct: bool,
        subject_id: SubjectId | str | None = None,
        mission_id: MissionId | str | None = None,
        learning_episode_id: LearningEpisodeId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a single answered question into evidence.

        Produces ``QUESTION_ANSWERED`` when ``is_correct`` is ``True``, or
        ``QUESTION_INCORRECT`` otherwise. The two outcomes are mutually
        exclusive by construction — a single call can never produce
        contradictory evidence.
        """
        evidence_type = (
            EvidenceType.QUESTION_ANSWERED
            if is_correct
            else EvidenceType.QUESTION_INCORRECT
        )
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
            learning_episode_id=learning_episode_id,
        )
        metadata = _merge_metadata({"is_correct": is_correct}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_reflection(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        reflection_text: str,
        subject_id: SubjectId | str | None = None,
        competency_id: CompetencyId | str | None = None,
        mission_id: MissionId | str | None = None,
        learning_episode_id: LearningEpisodeId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a recorded student reflection into evidence."""
        evidence_type = EvidenceType.REFLECTION_RECORDED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
            learning_episode_id=learning_episode_id,
        )
        metadata = _merge_metadata(
            {"reflection_text": reflection_text}, extra_metadata
        )
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_session_start(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        learning_episode_id: LearningEpisodeId | str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform the start of a study session into evidence."""
        evidence_type = EvidenceType.STUDY_SESSION_STARTED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            learning_episode_id=learning_episode_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_session_completion(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        learning_episode_id: LearningEpisodeId | str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform the completion of a study session into evidence."""
        evidence_type = EvidenceType.STUDY_SESSION_COMPLETED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            learning_episode_id=learning_episode_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_mission_completion(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        mission_id: MissionId | str,
        completed: bool,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a finished mission into evidence.

        Produces ``MISSION_COMPLETED`` when ``completed`` is ``True``, or
        ``MISSION_ABANDONED`` otherwise — mutually exclusive by
        construction.
        """
        evidence_type = (
            EvidenceType.MISSION_COMPLETED
            if completed
            else EvidenceType.MISSION_ABANDONED
        )
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            mission_id=mission_id,
        )
        metadata = _merge_metadata({"completed": completed}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_hint_request(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        competency_id: CompetencyId | str,
        hint_count: int = 1,
        subject_id: SubjectId | str | None = None,
        mission_id: MissionId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a requested hint into evidence."""
        evidence_type = EvidenceType.HINT_REQUESTED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
        )
        metadata = _merge_metadata({"hint_count": hint_count}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_checkpoint(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        checkpoint_id: CheckpointId | str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a reached checkpoint into evidence."""
        evidence_type = EvidenceType.CHECKPOINT_REACHED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            checkpoint_id=checkpoint_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_confidence(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        confidence_level: str,
        subject_id: SubjectId | str | None = None,
        competency_id: CompetencyId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a self-reported confidence rating into evidence.

        Requires at least one of ``subject_id`` or ``competency_id`` — a
        confidence report must target something.
        """
        evidence_type = EvidenceType.CONFIDENCE_REPORTED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
        )
        metadata = _merge_metadata(
            {"confidence_level": confidence_level}, extra_metadata
        )
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_time_invested(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        duration_seconds: float,
        subject_id: SubjectId | str | None = None,
        competency_id: CompetencyId | str | None = None,
        mission_id: MissionId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform invested study time into evidence."""
        evidence_type = EvidenceType.TIME_INVESTED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
        )
        metadata = _merge_metadata(
            {"duration_seconds": duration_seconds}, extra_metadata
        )
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_review_completion(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        competency_id: CompetencyId | str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a completed spaced-review pass into evidence."""
        evidence_type = EvidenceType.REVIEW_COMPLETED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_goal_achievement(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        goal_id: str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform an achieved goal into evidence.

        ``goal_id`` is carried as metadata rather than a typed reference
        because no Goals bounded context exists yet in this codebase.
        """
        evidence_type = EvidenceType.GOAL_ACHIEVED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
        )
        metadata = _merge_metadata({"goal_id": goal_id}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_subject_visit(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        subject_id: SubjectId | str,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform a subject visit into evidence."""
        evidence_type = EvidenceType.SUBJECT_VISITED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    @classmethod
    def record_competency_practice(
        cls,
        evidence_id: EvidenceId,
        student_id: str,
        occurred_at: EvidenceTimestamp | datetime,
        source: EvidenceSource,
        *,
        learning_environment: LearningEnvironment,
        competency_id: CompetencyId | str,
        subject_id: SubjectId | str | None = None,
        weight: EvidenceWeight | float | None = None,
        extra_metadata: dict[str, Primitive] | None = None,
    ) -> EducationalEvidence:
        """Transform deliberate competency practice into evidence."""
        evidence_type = EvidenceType.COMPETENCY_PRACTISED
        context = _build_context(
            learning_environment=learning_environment,
            subject_id=subject_id,
            competency_id=competency_id,
        )
        metadata = _merge_metadata({}, extra_metadata)
        return cls(
            evidence_id=evidence_id,
            student_id=student_id,
            evidence_type=evidence_type,
            occurred_at=_coerce_timestamp(occurred_at),
            source=source,
            context=context,
            weight=_resolve_weight(evidence_type, weight),
            metadata=metadata,
        )

    # --- structural equality (evidence is compared by content, not just
    #     identity, so normalisation can be verified meaningfully) ---

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalEvidence):
            return NotImplemented
        return (
            self._evidence_id == other._evidence_id
            and self._student_id == other._student_id
            and self._evidence_type == other._evidence_type
            and self._occurred_at == other._occurred_at
            and self._source == other._source
            and self._context == other._context
            and self._weight == other._weight
            and self._metadata == other._metadata
        )

    def __hash__(self) -> int:
        return hash((type(self), self._evidence_id))

    def __repr__(self) -> str:
        return (
            f"EducationalEvidence(evidence_id={self._evidence_id!r}, "
            f"evidence_type={self._evidence_type!r}, "
            f"student_id={self._student_id!r})"
        )
