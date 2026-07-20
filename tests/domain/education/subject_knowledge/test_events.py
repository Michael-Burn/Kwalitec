"""Tests for Subject Knowledge domain events."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)
from domain.education.subject_knowledge import (
    ConceptCreated,
    DependencyAdded,
    MisconceptionRegistered,
)


class TestConceptCreated:
    def test_valid_event(self) -> None:
        event = ConceptCreated(
            concept_id=ConceptId("c1"),
            canonical_name="Force of mortality",
            initial_objective_id=LearningObjectiveId("lo-1"),
        )
        assert event.canonical_name == "Force of mortality"

    def test_rejects_blank_name(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCreated(
                concept_id=ConceptId("c1"),
                canonical_name=" ",
                initial_objective_id=LearningObjectiveId("lo-1"),
            )

    def test_frozen(self) -> None:
        event = ConceptCreated(
            concept_id=ConceptId("c1"),
            canonical_name="Name",
            initial_objective_id=LearningObjectiveId("lo-1"),
        )
        with pytest.raises(AttributeError):
            event.canonical_name = "x"  # type: ignore[misc]

    def test_equality(self) -> None:
        left = ConceptCreated(
            concept_id=ConceptId("c1"),
            canonical_name="Name",
            initial_objective_id=LearningObjectiveId("lo-1"),
        )
        right = ConceptCreated(
            concept_id=ConceptId("c1"),
            canonical_name="Name",
            initial_objective_id=LearningObjectiveId("lo-1"),
        )
        assert left == right


class TestMisconceptionRegistered:
    def test_valid_event(self) -> None:
        event = MisconceptionRegistered(
            concept_id=ConceptId("c1"),
            misconception_id=MisconceptionId("m1"),
        )
        assert event.misconception_id.value == "m1"

    def test_rejects_bad_concept_id(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MisconceptionRegistered(
                concept_id="c1",  # type: ignore[arg-type]
                misconception_id=MisconceptionId("m1"),
            )

    def test_frozen(self) -> None:
        event = MisconceptionRegistered(
            concept_id=ConceptId("c1"),
            misconception_id=MisconceptionId("m1"),
        )
        with pytest.raises(AttributeError):
            event.concept_id = ConceptId("c2")  # type: ignore[misc]


class TestDependencyAdded:
    def test_valid_event(self) -> None:
        event = DependencyAdded(
            concept_id=ConceptId("c1"),
            target_concept_id=ConceptId("c2"),
            kind=DependencyKind.REQUIRED_PREREQUISITE,
        )
        assert event.kind is DependencyKind.REQUIRED_PREREQUISITE

    def test_rejects_self_dependency_event(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            DependencyAdded(
                concept_id=ConceptId("c1"),
                target_concept_id=ConceptId("c1"),
                kind=DependencyKind.PARALLEL,
            )
        assert exc_info.value.invariant == "DependencyAdded.no_self_dependency"

    @pytest.mark.parametrize("kind", list(DependencyKind))
    def test_all_kinds(self, kind: DependencyKind) -> None:
        event = DependencyAdded(
            concept_id=ConceptId("c1"),
            target_concept_id=ConceptId("c2"),
            kind=kind,
        )
        assert event.kind is kind
