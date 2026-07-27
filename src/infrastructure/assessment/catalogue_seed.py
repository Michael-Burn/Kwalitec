"""Seeded formative instrument catalogue for AP-002B delivery demos / tests."""

from __future__ import annotations

from application.assessment.delivery.question_content import (
    ChoiceOption,
    QuestionContent,
)
from application.assessment.ports.repositories import (
    AssessmentInstrumentRepository,
    QuestionContentRepository,
)
from domain.assessment.enums import (
    AssessmentPurpose,
    AssessmentType,
    DifficultyBand,
    ItemType,
    KnowledgeLevel,
)
from domain.assessment.factories import AssessmentInstrumentFactory
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.ids import InstrumentId, QuestionId
from domain.assessment.value_objects.levels import DifficultyLevel
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)
from domain.education.foundation.ids import LearningObjectiveId

DEFAULT_INSTRUMENT_ID = "inst-checkpoint-force-mortality"


def seed_delivery_catalogue(
    instruments: AssessmentInstrumentRepository,
    question_content: QuestionContentRepository,
) -> str:
    """Seed a short formative checkpoint and return its instrument id."""
    objective = LearningObjectiveReference(
        objective_id=LearningObjectiveId("lo-force-mortality"),
        label="Force of mortality",
    )
    questions = [
        QuestionReference(
            question_id=QuestionId("q-mc-force"),
            item_type=ItemType.MULTIPLE_CHOICE,
            version="1",
            learning_objective=objective,
            curriculum_entity_id="topic-cm1-01",
            knowledge_level=KnowledgeLevel.UNDERSTANDING,
            difficulty=DifficultyLevel(band=DifficultyBand.STANDARD),
            estimated_time_seconds=90,
        ),
        QuestionReference(
            question_id=QuestionId("q-numeric-mu"),
            item_type=ItemType.NUMERIC,
            version="1",
            learning_objective=objective,
            knowledge_level=KnowledgeLevel.APPLICATION,
            difficulty=DifficultyLevel(band=DifficultyBand.STANDARD),
            estimated_time_seconds=60,
        ),
        QuestionReference(
            question_id=QuestionId("q-confidence-mu"),
            item_type=ItemType.CONFIDENCE_RATING,
            version="1",
            learning_objective=objective,
            estimated_time_seconds=30,
        ),
        QuestionReference(
            question_id=QuestionId("q-reflection-mu"),
            item_type=ItemType.REFLECTION,
            version="1",
            learning_objective=objective,
            estimated_time_seconds=60,
        ),
    ]
    instrument = AssessmentInstrumentFactory.create(
        instrument_id=InstrumentId(DEFAULT_INSTRUMENT_ID),
        assessment_type=AssessmentType.MIXED,
        purpose=AssessmentPurpose.FORMATIVE_CHECKPOINT,
        questions=questions,
        learning_objectives=[objective],
        metadata=AssessmentMetadata(
            version="1",
            title="Checkpoint — force of mortality",
            description=(
                "A short learning check. No grades — just clearer next steps."
            ),
            tags=("checkpoint", "formative"),
        ),
        configuration=AssessmentConfiguration(
            allow_pause=True,
            invite_confidence=True,
            require_confidence=False,
            one_item_at_a_time=True,
        ),
    )
    instruments.save(instrument)

    contents = [
        QuestionContent(
            question_id="q-mc-force",
            item_type=ItemType.MULTIPLE_CHOICE,
            stem=(
                "Which statement best describes the force of mortality at age x?"
            ),
            options=(
                ChoiceOption(
                    "a",
                    "The instantaneous rate of mortality at exact age x",
                ),
                ChoiceOption(
                    "b",
                    "The probability of surviving from age x to x+1",
                ),
                ChoiceOption(
                    "c",
                    "The expected curtate future lifetime",
                ),
                ChoiceOption(
                    "d",
                    "The present value of a unit assurance",
                ),
            ),
            hints=(
                "Think about an instantaneous rate, not a one-year probability.",
            ),
        ),
        QuestionContent(
            question_id="q-numeric-mu",
            item_type=ItemType.NUMERIC,
            stem=(
                "If μ_x = 0.02 constantly, what is the approximate one-year "
                "mortality probability q_x under a constant force assumption? "
                "(Enter a decimal, e.g. 0.02)"
            ),
            placeholder="0.02",
            hints=("Under constant force, q_x ≈ 1 − e^{−μ}.",),
        ),
        QuestionContent(
            question_id="q-confidence-mu",
            item_type=ItemType.CONFIDENCE_RATING,
            stem=(
                "How confident do you feel about the force of mortality idea "
                "right now? (1 = not sure, 5 = very sure)"
            ),
        ),
        QuestionContent(
            question_id="q-reflection-mu",
            item_type=ItemType.REFLECTION,
            stem=(
                "In a sentence, what still feels unclear about force of mortality?"
            ),
            placeholder="Share a brief reflection",
        ),
    ]
    for content in contents:
        question_content.save(content)

    return DEFAULT_INSTRUMENT_ID
