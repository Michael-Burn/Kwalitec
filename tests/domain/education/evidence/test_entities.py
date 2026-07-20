"""Entity tests for Evidence domain."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    EvidenceContext,
    EvidenceContextId,
    EvidenceItem,
    EvidenceItemId,
    EvidenceItemKind,
    EvidenceSource,
    EvidenceSourceId,
    EvidenceSourceKind,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    LearningObjectiveId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from tests.domain.education.evidence.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    make_context,
    make_item,
    make_source,
)


class TestEvidenceItem:
    def test_valid_construction(self) -> None:
        item = make_item()
        assert item.entity_id == EvidenceItemId("item-001")
        assert item.kind is EvidenceItemKind.QUESTION_RESPONSE

    @pytest.mark.parametrize("kind", list(EvidenceItemKind))
    def test_all_kinds(self, kind: EvidenceItemKind) -> None:
        item = make_item(kind=kind, observation=f"Observation for {kind.value}")
        assert item.kind is kind

    def test_blank_observation_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_item(observation="   ")

    def test_blank_id_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceItemId("  ")

    def test_identity_equality(self) -> None:
        a = make_item(item_id="same", observation="first")
        b = make_item(item_id="same", observation="second")
        assert a == b
        assert hash(a) == hash(b)

    def test_signature_casefold(self) -> None:
        a = make_item(observation="Correct Answer")
        b = make_item(item_id="item-002", observation="correct answer")
        assert a.observational_signature() == b.observational_signature()

    def test_with_observation(self) -> None:
        item = make_item()
        amended = item.with_observation("Amended observational text")
        assert amended.observation == "Amended observational text"
        assert amended.item_id == item.item_id

    def test_bad_kind_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceItem(
                item_id=EvidenceItemId("i1"),
                kind="question_response",  # type: ignore[arg-type]
                observation="x",
            )


class TestEvidenceSource:
    def test_valid(self) -> None:
        source = make_source()
        assert source.is_assessment()
        assert not source.is_reflection_capture()

    @pytest.mark.parametrize("kind", list(EvidenceSourceKind))
    def test_all_source_kinds(self, kind: EvidenceSourceKind) -> None:
        source = make_source(kind=kind, label=f"Source {kind.value}")
        assert source.kind is kind

    def test_blank_label_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_source(label="")

    def test_blank_channel_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_source(channel="  ")

    def test_channel_optional(self) -> None:
        source = EvidenceSource(
            source_id=EvidenceSourceId("s1"),
            kind=EvidenceSourceKind.STUDENT_ACTION,
            label="Attempt",
        )
        assert source.channel is None

    def test_identity_equality(self) -> None:
        a = make_source(source_id="src", label="A")
        b = make_source(source_id="src", label="B")
        assert a == b

    def test_predicates(self) -> None:
        assert make_source(kind=EvidenceSourceKind.STUDENT_ACTION).is_student_action()
        assert make_source(
            kind=EvidenceSourceKind.REFLECTION_CAPTURE
        ).is_reflection_capture()


class TestEvidenceContext:
    def test_valid(self) -> None:
        ctx = make_context()
        assert CONCEPT_SELECT in ctx.concept_ids()
        assert EPISODE_001 in ctx.episode_ids()

    def test_blank_situation_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_context(situation="")

    def test_duplicate_concept_refs_rejected(self) -> None:
        ref = ConceptReference(concept_id=CONCEPT_SELECT)
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                context_id=EvidenceContextId("c1"),
                situation="Probe",
                concept_references=(ref, ref),
            )

    def test_duplicate_episode_ids_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                context_id=EvidenceContextId("c1"),
                situation="Probe",
                learning_episode_ids=(EPISODE_001, EPISODE_001),
            )

    def test_duplicate_objectives_rejected(self) -> None:
        obj = LearningObjectiveReference(
            objective_id=LearningObjectiveId("lo-1"), label="LO"
        )
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                context_id=EvidenceContextId("c1"),
                situation="Probe",
                learning_objective_references=(obj, obj),
            )

    def test_with_concept_reference(self) -> None:
        ctx = make_context(concepts=())
        updated = ctx.with_concept_reference(
            ConceptReference(concept_id=CONCEPT_ULTIMATE, label="Ultimate")
        )
        assert CONCEPT_ULTIMATE in updated.concept_ids()

    def test_with_concept_duplicate(self) -> None:
        ctx = make_context()
        with pytest.raises(EducationalInvariantViolation):
            ctx.with_concept_reference(ConceptReference(concept_id=CONCEPT_SELECT))

    def test_with_learning_episode(self) -> None:
        ctx = make_context(episodes=())
        updated = ctx.with_learning_episode(EPISODE_002)
        assert EPISODE_002 in updated.episode_ids()

    def test_with_episode_duplicate(self) -> None:
        ctx = make_context()
        with pytest.raises(EducationalInvariantViolation):
            ctx.with_learning_episode(EPISODE_001)

    def test_bad_dimension_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContext(
                context_id=EvidenceContextId("c1"),
                situation="Probe",
                learning_dimension="understanding",  # type: ignore[arg-type]
            )

    def test_identity_equality(self) -> None:
        a = make_context(context_id="same", situation="A")
        b = make_context(context_id="same", situation="B")
        assert a == b

    def test_minimal_context(self) -> None:
        ctx = EvidenceContext(
            context_id=EvidenceContextId("minimal"),
            situation="Bare educational situation",
        )
        assert ctx.learning_dimension is None
        assert ctx.concept_references == ()
        assert isinstance(LearningDimension.APPLICATION, LearningDimension)
