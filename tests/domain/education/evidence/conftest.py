"""Shared factories for Evidence domain tests."""

from __future__ import annotations

import pytest

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
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
    LearningObjectiveId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
CONCEPT_ULTIMATE = ConceptId("concept-ultimate-mortality")
EPISODE_001 = LearningEpisodeId("episode-001")
EPISODE_002 = LearningEpisodeId("episode-002")
KNOWN_CONCEPTS = frozenset({CONCEPT_SELECT, CONCEPT_ULTIMATE})
KNOWN_EPISODES = frozenset({EPISODE_001, EPISODE_002})


@pytest.fixture
def evidence_id() -> EvidenceId:
    return EvidenceId("evidence-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_timestamp(
    *,
    year: int = 2026,
    month: int = 7,
    day: int = 19,
    hour: int = 10,
    minute: int = 0,
) -> EvidenceTimestamp:
    return EvidenceTimestamp.from_utc_components(year, month, day, hour, minute)


def make_confidence(
    level: ConfidenceLevel = ConfidenceLevel.HIGH,
    *,
    ratio: float | None = 0.85,
) -> ConfidenceMeasure:
    return ConfidenceMeasure.of(level, ratio=ratio)


def make_strength(*, level: str = "strong") -> EvidenceStrength:
    factories = {
        "weak": EvidenceStrength.weak,
        "moderate": EvidenceStrength.moderate,
        "strong": EvidenceStrength.strong,
        "very_strong": EvidenceStrength.very_strong,
    }
    return factories[level]()


def make_item(
    *,
    item_id: str = "item-001",
    kind: EvidenceItemKind = EvidenceItemKind.QUESTION_RESPONSE,
    observation: str = "Correctly discriminated select vs ultimate ages",
    concept_id: ConceptId | None = CONCEPT_SELECT,
    learning_episode_id: LearningEpisodeId | None = EPISODE_001,
) -> EvidenceItem:
    return EvidenceItem(
        item_id=EvidenceItemId(item_id),
        kind=kind,
        observation=observation,
        concept_id=concept_id,
        learning_episode_id=learning_episode_id,
    )


def make_source(
    *,
    source_id: str = "source-001",
    kind: EvidenceSourceKind = EvidenceSourceKind.ASSESSMENT,
    label: str = "Quiz probe on select mortality",
    channel: str | None = "learning_episode",
) -> EvidenceSource:
    return EvidenceSource(
        source_id=EvidenceSourceId(source_id),
        kind=kind,
        label=label,
        channel=channel,
    )


def make_context(
    *,
    context_id: str = "ctx-001",
    situation: str = "Post-explanation retrieval probe",
    dimension: LearningDimension | None = LearningDimension.UNDERSTANDING,
    concepts: tuple[ConceptReference, ...] | None = None,
    episodes: tuple[LearningEpisodeId, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
) -> EvidenceContext:
    return EvidenceContext(
        context_id=EvidenceContextId(context_id),
        situation=situation,
        learning_dimension=dimension,
        concept_references=concepts
        if concepts is not None
        else (ConceptReference(concept_id=CONCEPT_SELECT, label="Select mortality"),),
        learning_objective_references=objectives
        if objectives is not None
        else (
            LearningObjectiveReference(
                objective_id=LearningObjectiveId("lo-select-ultimate"),
                label="Interpret select mortality tables",
            ),
        ),
        learning_episode_ids=episodes if episodes is not None else (EPISODE_001,),
    )


def make_record(
    *,
    evidence_id: str = "evidence-001",
    student_id: str = "student-ada",
    items: list[EvidenceItem] | None = None,
    source: EvidenceSource | None = None,
    context: EvidenceContext | None = None,
    confidence: ConfidenceMeasure | None = None,
    strength: EvidenceStrength | None = None,
    timestamp: EvidenceTimestamp | None = None,
    known_concepts: frozenset[ConceptId] | None = KNOWN_CONCEPTS,
    known_episodes: frozenset[LearningEpisodeId] | None = KNOWN_EPISODES,
    concept_references: list[ConceptReference] | None = None,
    learning_episode_ids: list[LearningEpisodeId] | None = None,
) -> EvidenceRecord:
    return EvidenceRecord.record(
        evidence_id=EvidenceId(evidence_id),
        student_id=student_id,
        items=items or [make_item()],
        source=source or make_source(),
        context=context or make_context(),
        confidence=confidence or make_confidence(),
        strength=strength or make_strength(),
        timestamp=timestamp or make_timestamp(),
        known_concept_ids=known_concepts,
        known_episode_ids=known_episodes,
        concept_references=concept_references
        or [ConceptReference(concept_id=CONCEPT_SELECT)],
        learning_episode_ids=learning_episode_ids or [EPISODE_001],
    )
