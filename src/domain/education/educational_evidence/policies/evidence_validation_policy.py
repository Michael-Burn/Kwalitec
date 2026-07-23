"""Policy validating EducationalEvidence shapes and outcome consistency.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model, Evidence rules)
Concept
    Evidence Validation Policy
"""

from __future__ import annotations

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_context import (
    EvidenceContext,
)
from domain.education.educational_evidence.value_objects.evidence_metadata import (
    EvidenceMetadata,
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
from domain.education.foundation.base import require_identity_value
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

# Curriculum/journey coordinates that must be present on LearningContext for
# a given evidence type. Field names are attributes of LearningContext.
_REQUIRED_CONTEXT_FIELDS: dict[EvidenceType, tuple[str, ...]] = {
    EvidenceType.QUESTION_ANSWERED: ("competency_id",),
    EvidenceType.QUESTION_INCORRECT: ("competency_id",),
    EvidenceType.MISSION_COMPLETED: ("mission_id",),
    EvidenceType.MISSION_ABANDONED: ("mission_id",),
    EvidenceType.STUDY_SESSION_STARTED: ("learning_episode_id",),
    EvidenceType.STUDY_SESSION_COMPLETED: ("learning_episode_id",),
    EvidenceType.HINT_REQUESTED: ("competency_id",),
    EvidenceType.REVIEW_COMPLETED: ("competency_id",),
    EvidenceType.CHECKPOINT_REACHED: ("checkpoint_id",),
    EvidenceType.SUBJECT_VISITED: ("subject_id",),
    EvidenceType.COMPETENCY_PRACTISED: ("competency_id",),
}

# Metadata keys that must be present for a given evidence type.
_REQUIRED_METADATA_KEYS: dict[EvidenceType, tuple[str, ...]] = {
    EvidenceType.QUESTION_ANSWERED: ("is_correct",),
    EvidenceType.QUESTION_INCORRECT: ("is_correct",),
    EvidenceType.MISSION_COMPLETED: ("completed",),
    EvidenceType.MISSION_ABANDONED: ("completed",),
    EvidenceType.REFLECTION_RECORDED: ("reflection_text",),
    EvidenceType.CONFIDENCE_REPORTED: ("confidence_level",),
    EvidenceType.GOAL_ACHIEVED: ("goal_id",),
    EvidenceType.TIME_INVESTED: ("duration_seconds",),
    EvidenceType.HINT_REQUESTED: ("hint_count",),
}

_KNOWN_CONFIDENCE_LEVELS = frozenset(
    level.value for level in ConfidenceLevel if level is not ConfidenceLevel.UNKNOWN
)

# Evidence types whose metadata "is_correct" boolean must equal this value.
_EXPECTED_IS_CORRECT: dict[EvidenceType, bool] = {
    EvidenceType.QUESTION_ANSWERED: True,
    EvidenceType.QUESTION_INCORRECT: False,
}

# Evidence types whose metadata "completed" boolean must equal this value.
_EXPECTED_COMPLETED: dict[EvidenceType, bool] = {
    EvidenceType.MISSION_COMPLETED: True,
    EvidenceType.MISSION_ABANDONED: False,
}


class EvidenceValidationPolicy:
    """Validates EducationalEvidence shapes and outcome consistency.

    This policy ensures invalid or self-contradictory evidence cannot be
    constructed. It performs no diagnosis, mastery estimation, or
    recommendation reasoning.
    """

    @staticmethod
    def assert_identity(evidence_id: EvidenceId) -> EvidenceId:
        if not isinstance(evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence must possess an EvidenceId identity",
                invariant="EducationalEvidence.identity.required",
            )
        return evidence_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_evidence_type(evidence_type: EvidenceType) -> EvidenceType:
        if not isinstance(evidence_type, EvidenceType):
            raise EducationalInvariantViolation(
                "evidence must possess an EvidenceType",
                invariant="EducationalEvidence.evidence_type.required",
            )
        return evidence_type

    @staticmethod
    def assert_timestamp(timestamp: EvidenceTimestamp) -> EvidenceTimestamp:
        if not isinstance(timestamp, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "evidence must possess an EvidenceTimestamp",
                invariant="EducationalEvidence.timestamp.required",
            )
        return timestamp

    @staticmethod
    def assert_source(source: EvidenceSource) -> EvidenceSource:
        if not isinstance(source, EvidenceSource):
            raise EducationalInvariantViolation(
                "evidence must identify its source",
                invariant="EducationalEvidence.source.required",
            )
        return source

    @staticmethod
    def assert_context(context: EvidenceContext) -> EvidenceContext:
        if not isinstance(context, EvidenceContext):
            raise EducationalInvariantViolation(
                "evidence must identify its educational context",
                invariant="EducationalEvidence.context.required",
            )
        return context

    @staticmethod
    def assert_weight(weight: EvidenceWeight) -> EvidenceWeight:
        if not isinstance(weight, EvidenceWeight):
            raise EducationalInvariantViolation(
                "evidence must possess an EvidenceWeight",
                invariant="EducationalEvidence.weight.required",
            )
        return weight

    @staticmethod
    def assert_metadata(metadata: EvidenceMetadata) -> EvidenceMetadata:
        if not isinstance(metadata, EvidenceMetadata):
            raise EducationalInvariantViolation(
                "evidence must possess EvidenceMetadata",
                invariant="EducationalEvidence.metadata.required",
            )
        return metadata

    @staticmethod
    def assert_context_matches_type(
        evidence_type: EvidenceType, context: EvidenceContext
    ) -> None:
        """Every evidence type that scopes to curriculum coordinates must
        carry those coordinates — evidence never invents its own scope."""
        learning_context = context.learning_context
        for field_name in _REQUIRED_CONTEXT_FIELDS.get(evidence_type, ()):
            if getattr(learning_context, field_name) is None:
                raise EducationalInvariantViolation(
                    f"{evidence_type.value} evidence requires "
                    f"learning_context.{field_name}",
                    invariant=f"EducationalEvidence.context.{field_name}.required",
                )
        if evidence_type is EvidenceType.CONFIDENCE_REPORTED:
            if (
                learning_context.subject_id is None
                and learning_context.competency_id is None
            ):
                raise EducationalInvariantViolation(
                    "confidence_reported evidence requires a subject_id or "
                    "competency_id",
                    invariant=(
                        "EducationalEvidence.context.confidence_target.required"
                    ),
                )

    @staticmethod
    def assert_metadata_matches_type(
        evidence_type: EvidenceType, metadata: EvidenceMetadata
    ) -> None:
        """Every evidence type's required metadata must be present, well
        typed, and consistent with the educational outcome the type asserts.

        This is where contradictory educational outcomes are rejected — for
        example, ``QUESTION_ANSWERED`` evidence claiming ``is_correct`` is
        ``False`` can never be constructed.
        """
        for key in _REQUIRED_METADATA_KEYS.get(evidence_type, ()):
            if not metadata.has(key):
                raise EducationalInvariantViolation(
                    f"{evidence_type.value} evidence requires metadata key "
                    f"'{key}'",
                    invariant=f"EducationalEvidence.metadata.{key}.required",
                )

        if evidence_type in _EXPECTED_IS_CORRECT:
            is_correct = metadata.get("is_correct")
            if not isinstance(is_correct, bool):
                raise EducationalInvariantViolation(
                    "is_correct metadata must be a boolean",
                    invariant="EducationalEvidence.metadata.is_correct.type",
                )
            if is_correct is not _EXPECTED_IS_CORRECT[evidence_type]:
                raise EducationalInvariantViolation(
                    "is_correct metadata contradicts the evidence_type "
                    "outcome",
                    invariant=(
                        "EducationalEvidence.metadata.is_correct.contradiction"
                    ),
                )

        if evidence_type in _EXPECTED_COMPLETED:
            completed = metadata.get("completed")
            if not isinstance(completed, bool):
                raise EducationalInvariantViolation(
                    "completed metadata must be a boolean",
                    invariant="EducationalEvidence.metadata.completed.type",
                )
            if completed is not _EXPECTED_COMPLETED[evidence_type]:
                raise EducationalInvariantViolation(
                    "completed metadata contradicts the evidence_type outcome",
                    invariant=(
                        "EducationalEvidence.metadata.completed.contradiction"
                    ),
                )

        if evidence_type is EvidenceType.TIME_INVESTED:
            duration = metadata.get("duration_seconds")
            if isinstance(duration, bool) or not isinstance(duration, int | float):
                raise EducationalInvariantViolation(
                    "duration_seconds metadata must be a real number",
                    invariant=(
                        "EducationalEvidence.metadata.duration_seconds.type"
                    ),
                )
            if duration <= 0:
                raise EducationalInvariantViolation(
                    "duration_seconds metadata must be positive",
                    invariant=(
                        "EducationalEvidence.metadata.duration_seconds.range"
                    ),
                )

        if evidence_type is EvidenceType.HINT_REQUESTED:
            hint_count = metadata.get("hint_count")
            if isinstance(hint_count, bool) or not isinstance(hint_count, int):
                raise EducationalInvariantViolation(
                    "hint_count metadata must be an integer",
                    invariant="EducationalEvidence.metadata.hint_count.type",
                )
            if hint_count < 1:
                raise EducationalInvariantViolation(
                    "hint_count metadata must be at least 1",
                    invariant="EducationalEvidence.metadata.hint_count.range",
                )

        if evidence_type is EvidenceType.CONFIDENCE_REPORTED:
            level = metadata.get("confidence_level")
            if not isinstance(level, str) or level not in _KNOWN_CONFIDENCE_LEVELS:
                raise EducationalInvariantViolation(
                    "confidence_level metadata must be a known confidence "
                    "level",
                    invariant=(
                        "EducationalEvidence.metadata.confidence_level.type"
                    ),
                )

        if evidence_type is EvidenceType.GOAL_ACHIEVED:
            goal_id = metadata.get("goal_id")
            if not isinstance(goal_id, str) or not goal_id.strip():
                raise EducationalInvariantViolation(
                    "goal_id metadata must be a non-empty string",
                    invariant="EducationalEvidence.metadata.goal_id.required",
                )

        if evidence_type is EvidenceType.REFLECTION_RECORDED:
            text = metadata.get("reflection_text")
            if not isinstance(text, str) or not text.strip():
                raise EducationalInvariantViolation(
                    "reflection_text metadata must be a non-empty string",
                    invariant=(
                        "EducationalEvidence.metadata.reflection_text.required"
                    ),
                )
