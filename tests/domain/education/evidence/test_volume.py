"""High-volume matrices exercising Evidence domain surface area."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceConsistencyPolicy,
    EvidenceIsConsistentSpecification,
    EvidenceIsSufficientSpecification,
    EvidenceItemKind,
    EvidenceRecordStatus,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceStrengthLevel,
    EvidenceValidationPolicy,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence.conftest import (
    KNOWN_CONCEPTS,
    KNOWN_EPISODES,
    make_confidence,
    make_context,
    make_item,
    make_record,
    make_source,
    make_timestamp,
)

ITEM_KINDS = list(EvidenceItemKind)
SOURCE_KINDS = list(EvidenceSourceKind)
STRENGTH_LEVELS = list(EvidenceStrengthLevel)
CONFIDENCE_LEVELS = [
    ConfidenceLevel.VERY_LOW,
    ConfidenceLevel.LOW,
    ConfidenceLevel.MEDIUM,
    ConfidenceLevel.HIGH,
    ConfidenceLevel.VERY_HIGH,
]
DIMENSIONS = list(LearningDimension)
STUDENTS = tuple(f"student-{i}" for i in range(1, 8))
HOURS = tuple(range(0, 24))


def _compatible_source(kind: EvidenceItemKind) -> EvidenceSourceKind:
    mapping = {
        EvidenceItemKind.REFLECTION: EvidenceSourceKind.REFLECTION_CAPTURE,
        EvidenceItemKind.HINT_USAGE: EvidenceSourceKind.SYSTEM_OBSERVATION,
        EvidenceItemKind.QUESTION_RESPONSE: EvidenceSourceKind.ASSESSMENT,
        EvidenceItemKind.WORKED_EXAMPLE_OUTCOME: EvidenceSourceKind.LEARNING_EPISODE,
        EvidenceItemKind.RETRIEVAL_ATTEMPT: EvidenceSourceKind.STUDENT_ACTION,
        EvidenceItemKind.TRANSFER_ATTEMPT: EvidenceSourceKind.ASSESSMENT,
    }
    return mapping[kind]


def _compatible_strength(kind: EvidenceItemKind) -> EvidenceStrength:
    if kind in {EvidenceItemKind.REFLECTION, EvidenceItemKind.HINT_USAGE}:
        return EvidenceStrength.weak()
    return EvidenceStrength.strong()


def _compatible_confidence(strength: EvidenceStrength) -> ConfidenceMeasure:
    floors = {
        EvidenceStrengthLevel.WEAK: ConfidenceLevel.LOW,
        EvidenceStrengthLevel.MODERATE: ConfidenceLevel.MEDIUM,
        EvidenceStrengthLevel.STRONG: ConfidenceLevel.HIGH,
        EvidenceStrengthLevel.VERY_STRONG: ConfidenceLevel.VERY_HIGH,
    }
    return ConfidenceMeasure.of(floors[strength.level])


@pytest.mark.parametrize("kind", ITEM_KINDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_record_per_item_kind_and_student(
    kind: EvidenceItemKind, student: str
) -> None:
    strength = _compatible_strength(kind)
    record = make_record(
        evidence_id=f"ev-{kind.value}-{student}",
        student_id=student,
        items=[
            make_item(
                item_id=f"item-{kind.value}",
                kind=kind,
                observation=f"{kind.value} observation for {student}",
            )
        ],
        source=make_source(
            source_id=f"src-{kind.value}",
            kind=_compatible_source(kind),
            label=f"Source for {kind.value}",
        ),
        strength=strength,
        confidence=_compatible_confidence(strength),
    )
    assert record.student_id == student
    assert record.items[0].kind is kind
    assert EvidenceIsSufficientSpecification().is_satisfied_by(record)
    assert EvidenceIsConsistentSpecification().is_satisfied_by(record)


@pytest.mark.parametrize("level", STRENGTH_LEVELS)
@pytest.mark.parametrize("quality", [0, 1, 2, 3, 4])
def test_strength_quality_and_predicates(
    level: EvidenceStrengthLevel, quality: int
) -> None:
    strength = EvidenceStrength(level=level)
    from_quality = EvidenceStrength.from_quality_level(quality)
    assert isinstance(from_quality.level, EvidenceStrengthLevel)
    assert strength.at_least(EvidenceStrength.weak())
    assert str(strength) == level.value


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("ratio", [None, 0.0, 0.25, 0.5, 0.75, 1.0])
def test_confidence_matrix(level: ConfidenceLevel, ratio: float | None) -> None:
    measure = ConfidenceMeasure.of(level, ratio=ratio)
    assert measure.level is level
    assert measure.is_at_least(ConfidenceLevel.VERY_LOW)


@pytest.mark.parametrize("hour", HOURS)
def test_timestamp_hours(hour: int) -> None:
    ts = make_timestamp(hour=hour)
    assert ts.occurred_at.hour == hour
    later = make_timestamp(hour=min(hour + 1, 23))
    if hour < 23:
        assert ts.is_before(later)


@pytest.mark.parametrize("dimension", DIMENSIONS)
@pytest.mark.parametrize("source_kind", SOURCE_KINDS)
def test_context_dimension_with_source_label(
    dimension: LearningDimension, source_kind: EvidenceSourceKind
) -> None:
    # Use assessment-compatible item unless reflection source.
    if source_kind is EvidenceSourceKind.REFLECTION_CAPTURE:
        kind = EvidenceItemKind.REFLECTION
        strength = EvidenceStrength.weak()
        confidence = make_confidence(ConfidenceLevel.LOW)
    else:
        kind = EvidenceItemKind.QUESTION_RESPONSE
        if source_kind is EvidenceSourceKind.SYSTEM_OBSERVATION:
            # question response allowed for system observation
            pass
        strength = EvidenceStrength.moderate()
        confidence = make_confidence(ConfidenceLevel.MEDIUM)

    if source_kind is EvidenceSourceKind.REFLECTION_CAPTURE:
        items = [
            make_item(
                kind=kind,
                observation=f"Reflection in {dimension.value}",
            )
        ]
    elif source_kind is EvidenceSourceKind.SYSTEM_OBSERVATION:
        items = [
            make_item(
                kind=EvidenceItemKind.HINT_USAGE,
                observation=f"Hint in {dimension.value}",
            )
        ]
        strength = EvidenceStrength.weak()
        confidence = make_confidence(ConfidenceLevel.LOW)
    else:
        items = [
            make_item(
                kind=EvidenceItemKind.QUESTION_RESPONSE,
                observation=f"Response in {dimension.value}",
            )
        ]
        strength = EvidenceStrength.strong()
        confidence = make_confidence(ConfidenceLevel.HIGH)

    record = make_record(
        evidence_id=f"ev-{dimension.value}-{source_kind.value}",
        items=items,
        source=make_source(
            source_id=f"src-{source_kind.value}-{dimension.value}",
            kind=source_kind,
            label=f"{source_kind.value}-{dimension.value}",
        ),
        context=make_context(
            context_id=f"ctx-{dimension.value}-{source_kind.value}",
            situation=f"Situation {dimension.value}",
            dimension=dimension,
        ),
        strength=strength,
        confidence=confidence,
    )
    assert record.context.learning_dimension is dimension


@pytest.mark.parametrize(
    "status_action",
    ["amend", "invalidate", "attach_context", "add_item"],
)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_mutation_matrix(status_action: str, student: str) -> None:
    record = make_record(
        evidence_id=f"ev-mut-{status_action}-{student}",
        student_id=student,
    )
    record.pull_events()
    if status_action == "amend":
        record.amend(
            items=[
                make_item(
                    item_id="amended",
                    observation=f"Amended for {student}",
                )
            ]
        )
        assert record.is_amended()
    elif status_action == "invalidate":
        record.invalidate(f"void-{student}")
        assert record.is_invalidated()
    elif status_action == "attach_context":
        record.attach_context(
            make_context(
                context_id=f"ctx-{student}",
                situation=f"Attached for {student}",
            )
        )
        assert record.context.situation.startswith("Attached")
    elif status_action == "add_item":
        record.add_item(
            make_item(
                item_id=f"extra-{student}",
                observation=f"Extra observation {student}",
            )
        )
        assert record.item_count() == 2


@pytest.mark.parametrize("concept_value", [c.value for c in KNOWN_CONCEPTS])
@pytest.mark.parametrize("episode_value", [e.value for e in KNOWN_EPISODES])
def test_known_reference_matrix(concept_value: str, episode_value: str) -> None:
    concept_id = ConceptId(concept_value)
    episode_id = LearningEpisodeId(episode_value)
    EvidenceValidationPolicy.assert_known_concepts(KNOWN_CONCEPTS, {concept_id})
    EvidenceValidationPolicy.assert_known_episodes(KNOWN_EPISODES, {episode_id})
    record = make_record(
        evidence_id=f"ev-{concept_value}-{episode_value}",
        items=[
            make_item(
                item_id=f"item-{concept_value}-{episode_value}",
                observation=f"Obs {concept_value} {episode_value}",
                concept_id=concept_id,
                learning_episode_id=episode_id,
            )
        ],
        context=make_context(
            context_id=f"ctx-{concept_value}-{episode_value}",
            concepts=(ConceptReference(concept_id=concept_id),),
            episodes=(episode_id,),
        ),
        concept_references=[ConceptReference(concept_id=concept_id)],
        learning_episode_ids=[episode_id],
    )
    assert record.has_concept(concept_id)
    assert record.has_learning_episode(episode_id)


@pytest.mark.parametrize("kind", ITEM_KINDS)
def test_duplicate_signature_rejected_per_kind(kind: EvidenceItemKind) -> None:
    strength = _compatible_strength(kind)
    source_kind = _compatible_source(kind)
    with pytest.raises(EducationalInvariantViolation):
        make_record(
            items=[
                make_item(
                    item_id="a",
                    kind=kind,
                    observation="Identical observation text",
                ),
                make_item(
                    item_id="b",
                    kind=kind,
                    observation="Identical observation text",
                ),
            ],
            source=make_source(kind=source_kind, label=f"dup-{kind.value}"),
            strength=strength,
            confidence=_compatible_confidence(strength),
        )


@pytest.mark.parametrize("kind", ITEM_KINDS)
def test_soft_ceiling_enforced_when_applicable(kind: EvidenceItemKind) -> None:
    if kind not in {EvidenceItemKind.REFLECTION, EvidenceItemKind.HINT_USAGE}:
        EvidenceConsistencyPolicy.assert_strength_consistent_with_items(
            EvidenceStrength.very_strong(),
            (make_item(kind=kind, observation=f"Hard {kind.value}"),),
        )
        return
    with pytest.raises(EducationalInvariantViolation):
        EvidenceConsistencyPolicy.assert_strength_consistent_with_items(
            EvidenceStrength.very_strong(),
            (make_item(kind=kind, observation=f"Soft {kind.value}"),),
        )


@pytest.mark.parametrize("level", STRENGTH_LEVELS)
def test_status_enum_and_strength_coexist(level: EvidenceStrengthLevel) -> None:
    assert EvidenceRecordStatus.ACTIVE.value == "active"
    assert EvidenceStrength(level=level).level is level
    assert EvidenceId(f"ev-{level.value}").value == f"ev-{level.value}"


@pytest.mark.parametrize("i", range(20))
def test_merge_distinct_observations(i: int) -> None:
    primary = make_record(evidence_id=f"primary-{i}")
    other = make_record(
        evidence_id=f"other-{i}",
        items=[
            make_item(
                item_id=f"other-item-{i}",
                observation=f"Distinct merge observation {i}",
            )
        ],
    )
    primary.merge(other)
    assert primary.item_count() == 2
    assert other.status is EvidenceRecordStatus.MERGED
