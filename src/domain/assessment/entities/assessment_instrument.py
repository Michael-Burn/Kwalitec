"""AssessmentInstrument — catalogue instrument for evidence collection.

Architecture Source
    knowledge/product/AP-002/QUESTION_MODEL.md
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md §2.3
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.assessment.entities.assessment_attempt import AssessmentQuestionReference
from domain.assessment.enums import AssessmentPurpose, AssessmentType
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.validation.instrument_validation import (
    assert_learning_objectives,
    assert_question_references,
)
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.ids import InstrumentId
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)


class AssessmentInstrument:
    """Published assessment instrument: ordered items + educational metadata.

    Published content versions are immutable; edits create a new instrument
    version via factory (AP-002B+). This foundation holds the domain shape.
    """

    def __init__(
        self,
        instrument_id: InstrumentId,
        assessment_type: AssessmentType,
        purpose: AssessmentPurpose,
        questions: Sequence[QuestionReference],
        learning_objectives: Sequence[LearningObjectiveReference],
        metadata: AssessmentMetadata,
        *,
        configuration: AssessmentConfiguration | None = None,
    ) -> None:
        if not isinstance(instrument_id, InstrumentId):
            raise AssessmentInvariantViolation(
                "instrument_id must be an InstrumentId",
                invariant="AssessmentInstrument.instrument_id.type",
            )
        if not isinstance(assessment_type, AssessmentType):
            raise AssessmentInvariantViolation(
                "assessment_type must be an AssessmentType",
                invariant="AssessmentInstrument.assessment_type.type",
            )
        if not isinstance(purpose, AssessmentPurpose):
            raise AssessmentInvariantViolation(
                "purpose must be an AssessmentPurpose",
                invariant="AssessmentInstrument.purpose.type",
            )
        if not isinstance(metadata, AssessmentMetadata):
            raise AssessmentInvariantViolation(
                "metadata must be an AssessmentMetadata",
                invariant="AssessmentInstrument.metadata.type",
            )
        refs = assert_question_references(questions)
        objectives = assert_learning_objectives(learning_objectives)
        self._instrument_id = instrument_id
        self._assessment_type = assessment_type
        self._purpose = purpose
        self._questions = tuple(
            AssessmentQuestionReference(reference=ref, sequence_index=index)
            for index, ref in enumerate(refs)
        )
        self._learning_objectives = objectives
        self._metadata = metadata
        self._configuration = configuration or AssessmentConfiguration()
        if not isinstance(self._configuration, AssessmentConfiguration):
            raise AssessmentInvariantViolation(
                "configuration must be an AssessmentConfiguration",
                invariant="AssessmentInstrument.configuration.type",
            )

    @property
    def instrument_id(self) -> InstrumentId:
        return self._instrument_id

    @property
    def assessment_type(self) -> AssessmentType:
        return self._assessment_type

    @property
    def purpose(self) -> AssessmentPurpose:
        return self._purpose

    @property
    def questions(self) -> tuple[AssessmentQuestionReference, ...]:
        return self._questions

    @property
    def question_references(self) -> tuple[QuestionReference, ...]:
        return tuple(item.reference for item in self._questions)

    @property
    def learning_objectives(self) -> tuple[LearningObjectiveReference, ...]:
        return self._learning_objectives

    @property
    def metadata(self) -> AssessmentMetadata:
        return self._metadata

    @property
    def configuration(self) -> AssessmentConfiguration:
        return self._configuration

    def question_count(self) -> int:
        return len(self._questions)
