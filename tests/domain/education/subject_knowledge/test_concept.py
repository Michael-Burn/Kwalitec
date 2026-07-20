"""Tests for the Concept aggregate root and educational invariants."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import DependencyKind, RepresentationKind
from domain.education.foundation.ids import ConceptId, LearningObjectiveId
from domain.education.subject_knowledge import (
    Concept,
    ConceptBoundary,
    ConceptCreated,
    Dependency,
    DependencyAdded,
    MisconceptionRegistered,
)
from tests.domain.education.subject_knowledge.conftest import (
    make_application_context,
    make_concept,
    make_dependency,
    make_misconception,
    make_objective,
    make_representation,
    make_transfer_context,
)


class TestConceptCreation:
    def test_create_requires_learning_objective(
        self, concept_id: ConceptId, boundary: ConceptBoundary
    ) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            Concept(
                concept_id=concept_id,
                canonical_name="Force of mortality",
                core_meaning="instantaneous mortality rate",
                boundary=boundary,
                learning_objectives=[],
            )
        assert exc_info.value.invariant == "Concept.learning_objectives.min_one"

    def test_create_emits_concept_created(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        events = concept.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], ConceptCreated)
        assert events[0].concept_id == concept_id
        assert concept.pull_events() == []

    def test_must_have_identity(self, boundary: ConceptBoundary) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Concept(
                concept_id="not-an-id",  # type: ignore[arg-type]
                canonical_name="Name",
                core_meaning="meaning",
                boundary=boundary,
                learning_objectives=[make_objective(ConceptId("c1"))],
            )

    def test_must_have_canonical_name(
        self, concept_id: ConceptId, boundary: ConceptBoundary
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Concept(
                concept_id=concept_id,
                canonical_name="  ",
                core_meaning="meaning",
                boundary=boundary,
                learning_objectives=[make_objective(concept_id)],
            )

    def test_must_have_core_meaning(
        self, concept_id: ConceptId, boundary: ConceptBoundary
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Concept(
                concept_id=concept_id,
                canonical_name="Name",
                core_meaning="",
                boundary=boundary,
                learning_objectives=[make_objective(concept_id)],
            )

    def test_objective_must_belong(
        self, concept_id: ConceptId, boundary: ConceptBoundary
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Concept(
                concept_id=concept_id,
                canonical_name="Name",
                core_meaning="meaning",
                boundary=boundary,
                learning_objectives=[make_objective(ConceptId("other"))],
            )

    def test_no_public_setters_for_collections(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(AttributeError):
            concept.canonical_name = "mutated"  # type: ignore[misc]

    def test_identity_equality(self) -> None:
        left = make_concept(ConceptId("same"), name="A")
        right = make_concept(ConceptId("same"), name="B")
        assert left == right
        assert hash(left) == hash(right)


class TestLearningObjectiveBehaviour:
    def test_add_learning_objective(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.add_learning_objective(
            make_objective(concept_id, objective_id="lo-002")
        )
        assert len(concept.learning_objectives) == 2
        assert concept.has_learning_objective(LearningObjectiveId("lo-002"))

    def test_duplicate_learning_objective_rejected(
        self, concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id, objective_id="lo-001")
        with pytest.raises(EducationalInvariantViolation):
            concept.add_learning_objective(
                make_objective(concept_id, objective_id="lo-001")
            )

    def test_cannot_remove_final_learning_objective(
        self, concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id, objective_id="lo-001")
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            concept.remove_learning_objective(LearningObjectiveId("lo-001"))
        assert (
            exc_info.value.invariant
            == "Concept.learning_objectives.cannot_remove_final"
        )

    def test_can_remove_non_final(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id, objective_id="lo-001")
        concept.add_learning_objective(
            make_objective(concept_id, objective_id="lo-002")
        )
        concept.remove_learning_objective(LearningObjectiveId("lo-001"))
        assert len(concept.learning_objectives) == 1
        assert concept.has_learning_objective(LearningObjectiveId("lo-002"))

    def test_remove_unknown_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.add_learning_objective(
            make_objective(concept_id, objective_id="lo-002")
        )
        with pytest.raises(EducationalInvariantViolation):
            concept.remove_learning_objective(LearningObjectiveId("missing"))

    def test_foreign_objective_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.add_learning_objective(
                make_objective(ConceptId("foreign"), objective_id="lo-x")
            )


class TestRepresentationBehaviour:
    def test_register_representation(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.register_representation(make_representation(concept_id))
        assert len(concept.representations) == 1
        assert concept.has_representation_kind(RepresentationKind.SYMBOLIC)

    def test_duplicate_representation_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.register_representation(make_representation(concept_id))
        with pytest.raises(EducationalInvariantViolation):
            concept.register_representation(make_representation(concept_id))

    def test_representation_kinds_unique(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.register_representation(
            make_representation(
                concept_id,
                representation_id="rep-1",
                kind=RepresentationKind.SYMBOLIC,
            )
        )
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            concept.register_representation(
                make_representation(
                    concept_id,
                    representation_id="rep-2",
                    kind=RepresentationKind.SYMBOLIC,
                )
            )
        assert exc_info.value.invariant == "RepresentationPolicy.kind.unique"

    def test_different_kinds_allowed(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.register_representation(
            make_representation(
                concept_id,
                representation_id="rep-1",
                kind=RepresentationKind.SYMBOLIC,
            )
        )
        concept.register_representation(
            make_representation(
                concept_id,
                representation_id="rep-2",
                kind=RepresentationKind.TIMELINE,
            )
        )
        assert len(concept.representations) == 2

    def test_foreign_representation_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.register_representation(
                make_representation(ConceptId("foreign"))
            )


class TestMisconceptionBehaviour:
    def test_register_misconception_emits_event(
        self, concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.pull_events()
        misc = make_misconception(concept_id)
        concept.register_misconception(misc)
        events = concept.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], MisconceptionRegistered)
        assert concept.has_misconception(misc.misconception_id)

    def test_duplicate_misconception_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        concept.register_misconception(make_misconception(concept_id))
        with pytest.raises(EducationalInvariantViolation):
            concept.register_misconception(make_misconception(concept_id))

    def test_foreign_misconception_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.register_misconception(make_misconception(ConceptId("foreign")))


class TestDependencyBehaviour:
    def test_add_dependency_emits_event(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.pull_events()
        dep = make_dependency(other_concept_id)
        concept.add_dependency(dep)
        events = concept.pull_events()
        assert isinstance(events[0], DependencyAdded)
        assert concept.dependencies == (dep,)

    def test_self_dependency_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            concept.add_dependency(make_dependency(concept_id))
        assert "self" in (exc_info.value.invariant or "")

    def test_duplicate_dependency_rejected(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(make_dependency(other_concept_id))
        with pytest.raises(EducationalInvariantViolation):
            concept.add_dependency(make_dependency(other_concept_id))

    def test_same_target_different_kind_allowed(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(
            make_dependency(
                other_concept_id, kind=DependencyKind.REQUIRED_PREREQUISITE
            )
        )
        concept.add_dependency(
            make_dependency(other_concept_id, kind=DependencyKind.EXTENSION)
        )
        assert len(concept.dependencies) == 2

    @pytest.mark.parametrize("kind", list(DependencyKind))
    def test_all_dependency_kinds_accepted(
        self,
        concept_id: ConceptId,
        other_concept_id: ConceptId,
        kind: DependencyKind,
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(make_dependency(other_concept_id, kind=kind))
        assert concept.dependencies[0].kind is kind

    def test_remove_dependency(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(make_dependency(other_concept_id))
        concept.remove_dependency(other_concept_id)
        assert concept.dependencies == ()

    def test_remove_dependency_by_kind(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(
            make_dependency(
                other_concept_id, kind=DependencyKind.REQUIRED_PREREQUISITE
            )
        )
        concept.add_dependency(
            make_dependency(other_concept_id, kind=DependencyKind.PARALLEL)
        )
        concept.remove_dependency(
            other_concept_id, kind=DependencyKind.REQUIRED_PREREQUISITE
        )
        assert len(concept.dependencies) == 1
        assert concept.dependencies[0].kind is DependencyKind.PARALLEL

    def test_remove_missing_dependency_rejected(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.remove_dependency(other_concept_id)

    def test_prerequisites_and_extensions_queries(
        self, concept_id: ConceptId, other_concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_dependency(
            make_dependency(
                other_concept_id, kind=DependencyKind.REQUIRED_PREREQUISITE
            )
        )
        concept.add_dependency(
            Dependency(
                target_concept_id=ConceptId("concept-extension"),
                kind=DependencyKind.EXTENSION,
                description="extension",
            )
        )
        assert len(concept.prerequisites()) == 1
        assert len(concept.extensions()) == 1


class TestApplicationAndTransferBehaviour:
    def test_add_application_context(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        ctx = make_application_context(concept_id)
        concept.add_application_context(ctx)
        assert concept.has_application_context(ctx.context_id)

    def test_duplicate_application_context_rejected(
        self, concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_application_context(make_application_context(concept_id))
        with pytest.raises(EducationalInvariantViolation):
            concept.add_application_context(make_application_context(concept_id))

    def test_add_transfer_context(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        app = make_application_context(concept_id)
        concept.add_application_context(app)
        xfer = make_transfer_context(concept_id, base=app.context_id)
        concept.add_transfer_context(xfer)
        assert concept.has_transfer_context(xfer.context_id)

    def test_duplicate_transfer_context_rejected(
        self, concept_id: ConceptId
    ) -> None:
        concept = make_concept(concept_id)
        concept.add_transfer_context(make_transfer_context(concept_id))
        with pytest.raises(EducationalInvariantViolation):
            concept.add_transfer_context(make_transfer_context(concept_id))

    def test_transfer_base_must_be_owned(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        from domain.education.subject_knowledge import ApplicationContextId

        with pytest.raises(EducationalInvariantViolation) as exc_info:
            concept.add_transfer_context(
                make_transfer_context(
                    concept_id, base=ApplicationContextId("missing-app")
                )
            )
        assert exc_info.value.invariant == "Concept.transfer_context.base_owned"

    def test_foreign_application_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.add_application_context(
                make_application_context(ConceptId("foreign"))
            )

    def test_foreign_transfer_rejected(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        with pytest.raises(EducationalInvariantViolation):
            concept.add_transfer_context(
                make_transfer_context(ConceptId("foreign"))
            )


class TestConceptReadModels:
    def test_collections_are_tuples(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id)
        assert isinstance(concept.learning_objectives, tuple)
        assert isinstance(concept.representations, tuple)
        assert isinstance(concept.misconceptions, tuple)
        assert isinstance(concept.application_contexts, tuple)
        assert isinstance(concept.transfer_contexts, tuple)
        assert isinstance(concept.dependencies, tuple)

    def test_repr_contains_name(self, concept_id: ConceptId) -> None:
        concept = make_concept(concept_id, name="Force of mortality")
        assert "Force of mortality" in repr(concept)
