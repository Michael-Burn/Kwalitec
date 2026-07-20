"""Unit tests for educational foundation reference value objects."""

from __future__ import annotations

import pytest

from domain.education.foundation import (
    ApplicationContextReference,
    ConceptId,
    ConceptReference,
    DependencyKind,
    DependencyReference,
    EducationalInvariantViolation,
    LearningObjectiveId,
    LearningObjectiveReference,
    MisconceptionId,
    MisconceptionReference,
    RepresentationKind,
    RepresentationReference,
    TransferContextReference,
    TransferLevel,
)


def test_learning_objective_reference_equality_and_immutability() -> None:
    ref_a = LearningObjectiveReference(
        LearningObjectiveId("lo-1"),
        label="Explain select vs ultimate",
    )
    ref_b = LearningObjectiveReference(
        LearningObjectiveId("lo-1"),
        label="Explain select vs ultimate",
    )
    assert ref_a == ref_b
    assert hash(ref_a) == hash(ref_b)
    with pytest.raises(AttributeError):
        ref_a.label = "mutated"  # type: ignore[misc]


def test_concept_reference_requires_concept_id() -> None:
    ref = ConceptReference(ConceptId("force-of-mortality"), label="μₓ")
    assert ref.concept_id.value == "force-of-mortality"
    with pytest.raises(EducationalInvariantViolation):
        ConceptReference("not-an-id")  # type: ignore[arg-type]


def test_misconception_reference_optional_related_concept() -> None:
    bare = MisconceptionReference(MisconceptionId("misc-1"))
    linked = MisconceptionReference(
        MisconceptionId("misc-1"),
        related_concept_id=ConceptId("annuity-due"),
        label="Ultimate from age 0",
    )
    assert bare.related_concept_id is None
    assert linked.related_concept_id == ConceptId("annuity-due")


def test_representation_reference_validation() -> None:
    ref = RepresentationReference(
        representation_id="rep-timeline-1",
        kind=RepresentationKind.TIMELINE,
        concept_id=ConceptId("annuity-due"),
    )
    assert ref.kind is RepresentationKind.TIMELINE
    with pytest.raises(EducationalInvariantViolation):
        RepresentationReference(
            representation_id="",
            kind=RepresentationKind.SYMBOLIC,
        )


def test_dependency_reference_rejects_self_edge() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        DependencyReference(
            source_id="concept-a",
            target_id="concept-a",
            kind=DependencyKind.REQUIRED_PREREQUISITE,
        )
    assert exc_info.value.invariant == "DependencyReference.no_self_dependency"


def test_dependency_reference_valid() -> None:
    dep = DependencyReference(
        source_id="present-value",
        target_id="net-premium",
        kind=DependencyKind.REQUIRED_PREREQUISITE,
        label="PV before equivalence premium",
    )
    assert dep.source_id == "present-value"
    assert dep.kind is DependencyKind.REQUIRED_PREREQUISITE


def test_transfer_context_rejects_none_level() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        TransferContextReference(
            context_id="tx-1",
            transfer_level=TransferLevel.NONE,
        )
    assert (
        exc_info.value.invariant
        == "TransferContextReference.transfer_level.not_none"
    )


def test_transfer_context_near_and_far() -> None:
    near = TransferContextReference(
        context_id="tx-near",
        transfer_level=TransferLevel.NEAR,
        base_application_context_id="app-1",
    )
    far = TransferContextReference(
        context_id="tx-far",
        transfer_level=TransferLevel.FAR,
    )
    assert near.transfer_level is TransferLevel.NEAR
    assert far.base_application_context_id is None


def test_application_context_requires_task_demand() -> None:
    ctx = ApplicationContextReference(
        context_id="app-epv",
        task_demand="compute",
        label="Standard EPV valuation",
    )
    assert ctx.task_demand == "compute"
    with pytest.raises(EducationalInvariantViolation):
        ApplicationContextReference(context_id="app-1", task_demand="  ")


def test_blank_optional_label_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        LearningObjectiveReference(
            LearningObjectiveId("lo-1"),
            label="   ",
        )
