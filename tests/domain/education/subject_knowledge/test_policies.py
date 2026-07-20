"""Tests for Subject Knowledge policies."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import DependencyKind, RepresentationKind
from domain.education.foundation.ids import ConceptId, LearningObjectiveId
from domain.education.subject_knowledge import (
    ConceptBoundary,
    ConceptValidationPolicy,
    Dependency,
    DependencyPolicy,
    RepresentationPolicy,
)
from tests.domain.education.subject_knowledge.conftest import (
    make_application_context,
    make_misconception,
    make_objective,
    make_representation,
    make_transfer_context,
)


class TestDependencyPolicy:
    def test_valid_kind(self) -> None:
        DependencyPolicy.assert_valid_kind(DependencyKind.PARALLEL)

    def test_invalid_kind(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            DependencyPolicy.assert_valid_kind("related")  # type: ignore[arg-type]

    def test_no_self_dependency(self) -> None:
        owner = ConceptId("c1")
        dep = Dependency(
            target_concept_id=owner,
            kind=DependencyKind.REQUIRED_PREREQUISITE,
            description="self",
        )
        with pytest.raises(EducationalInvariantViolation):
            DependencyPolicy.assert_no_self_dependency(owner, dep)

    def test_duplicate_rejected(self) -> None:
        target = ConceptId("c2")
        existing = (
            Dependency(
                target_concept_id=target,
                kind=DependencyKind.EXTENSION,
                description="one",
            ),
        )
        candidate = Dependency(
            target_concept_id=target,
            kind=DependencyKind.EXTENSION,
            description="two",
        )
        with pytest.raises(EducationalInvariantViolation):
            DependencyPolicy.assert_not_duplicate(existing, candidate)

    def test_can_add_happy_path(self) -> None:
        DependencyPolicy.assert_can_add(
            ConceptId("c1"),
            (),
            Dependency(
                target_concept_id=ConceptId("c2"),
                kind=DependencyKind.HELPFUL_PREREQUISITE,
                description="helps",
            ),
        )

    @pytest.mark.parametrize(
        ("kind", "expected"),
        [
            (DependencyKind.REQUIRED_PREREQUISITE, True),
            (DependencyKind.HELPFUL_PREREQUISITE, True),
            (DependencyKind.PARALLEL, False),
            (DependencyKind.EXTENSION, False),
            (DependencyKind.REMEDIATION, False),
        ],
    )
    def test_is_prerequisite_kind(
        self, kind: DependencyKind, expected: bool
    ) -> None:
        assert DependencyPolicy.is_prerequisite_kind(kind) is expected

    def test_is_extension_kind(self) -> None:
        assert DependencyPolicy.is_extension_kind(DependencyKind.EXTENSION) is True
        assert (
            DependencyPolicy.is_extension_kind(DependencyKind.PARALLEL) is False
        )

    def test_find_edge(self) -> None:
        target = ConceptId("c2")
        edge = Dependency(
            target_concept_id=target,
            kind=DependencyKind.PARALLEL,
            description="parallel",
        )
        found = DependencyPolicy.find_edge(
            (edge,), target, DependencyKind.PARALLEL
        )
        assert found is edge
        missing = DependencyPolicy.find_edge(
            (edge,), target, DependencyKind.EXTENSION
        )
        assert missing is None


class TestRepresentationPolicy:
    def test_duplicate_identity(self, concept_id: ConceptId) -> None:
        existing = (make_representation(concept_id),)
        with pytest.raises(EducationalInvariantViolation):
            RepresentationPolicy.assert_not_duplicate_identity(
                existing, make_representation(concept_id)
            )

    def test_kind_unique(self, concept_id: ConceptId) -> None:
        existing = (
            make_representation(
                concept_id,
                representation_id="rep-a",
                kind=RepresentationKind.SYMBOLIC,
            ),
        )
        candidate = make_representation(
            concept_id,
            representation_id="rep-b",
            kind=RepresentationKind.SYMBOLIC,
        )
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            RepresentationPolicy.assert_kind_unique(existing, candidate)
        assert exc_info.value.invariant == "RepresentationPolicy.kind.unique"

    def test_can_register_different_kinds(self, concept_id: ConceptId) -> None:
        existing = (
            make_representation(
                concept_id,
                representation_id="rep-a",
                kind=RepresentationKind.SYMBOLIC,
            ),
        )
        candidate = make_representation(
            concept_id,
            representation_id="rep-b",
            kind=RepresentationKind.TABULAR,
        )
        RepresentationPolicy.assert_can_register(existing, candidate)


class TestConceptValidationPolicy:
    def test_identity_and_name(self) -> None:
        cid = ConceptValidationPolicy.assert_identity(ConceptId("c1"))
        assert cid.value == "c1"
        assert ConceptValidationPolicy.assert_canonical_name("  Name  ") == "Name"

    def test_rejects_blank_name(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_canonical_name(" ")

    def test_boundary_required(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_boundary("not-boundary")  # type: ignore[arg-type]
        boundary = ConceptBoundary(inclusion="in", exclusion="out")
        assert ConceptValidationPolicy.assert_boundary(boundary) is boundary

    def test_requires_learning_objective(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_has_learning_objective(())

    def test_cannot_remove_final(self, concept_id: ConceptId) -> None:
        objective = make_objective(concept_id)
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            ConceptValidationPolicy.assert_can_remove_learning_objective(
                (objective,), objective.objective_id
            )
        assert (
            exc_info.value.invariant
            == "Concept.learning_objectives.cannot_remove_final"
        )

    def test_remove_unknown_objective(self, concept_id: ConceptId) -> None:
        objective = make_objective(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_can_remove_learning_objective(
                (objective,), LearningObjectiveId("missing")
            )

    def test_can_remove_when_multiple(self, concept_id: ConceptId) -> None:
        first = make_objective(concept_id, objective_id="lo-1")
        second = make_objective(concept_id, objective_id="lo-2")
        removed = ConceptValidationPolicy.assert_can_remove_learning_objective(
            (first, second), first.objective_id
        )
        assert removed == first

    def test_ownership_checks(self, concept_id: ConceptId) -> None:
        other = ConceptId("other")
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_objective_belongs(
                concept_id, make_objective(other)
            )
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_misconception_belongs(
                concept_id, make_misconception(other)
            )
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_application_context_belongs(
                concept_id, make_application_context(other)
            )
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_transfer_context_belongs(
                concept_id, make_transfer_context(other)
            )

    def test_duplicate_checks(self, concept_id: ConceptId) -> None:
        objectives = (make_objective(concept_id),)
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_objective_not_duplicate(
                objectives, make_objective(concept_id)
            )
        miscs = (make_misconception(concept_id),)
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_misconception_not_duplicate(
                miscs, make_misconception(concept_id)
            )
        apps = (make_application_context(concept_id),)
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_application_context_not_duplicate(
                apps, make_application_context(concept_id)
            )
        xfers = (make_transfer_context(concept_id),)
        with pytest.raises(EducationalInvariantViolation):
            ConceptValidationPolicy.assert_transfer_context_not_duplicate(
                xfers, make_transfer_context(concept_id)
            )
