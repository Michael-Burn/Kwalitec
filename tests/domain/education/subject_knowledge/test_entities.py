"""Tests for Subject Knowledge entities."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import (
    RepresentationKind,
    TeachingIntentionType,
    TeachingStrategyType,
    TransferLevel,
)
from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)
from domain.education.subject_knowledge import (
    ApplicationContext,
    ApplicationContextId,
    LearningObjective,
    MasteryIndicator,
    Misconception,
    Representation,
    RepresentationId,
    TransferContext,
    TransferContextId,
)
from tests.domain.education.subject_knowledge.conftest import (
    make_application_context,
    make_misconception,
    make_objective,
    make_representation,
    make_transfer_context,
)


class TestLearningObjective:
    def test_create_valid(self, concept_id: ConceptId) -> None:
        objective = make_objective(concept_id)
        assert objective.belongs_to(concept_id)
        assert objective.entity_id == objective.objective_id

    def test_rejects_empty_success_criteria(self, concept_id: ConceptId) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningObjective(
                objective_id=LearningObjectiveId("lo-x"),
                concept_id=concept_id,
                statement="Do something",
                success_criteria=(),
                mastery_indicators=(
                    MasteryIndicator(
                        description="a",
                        observable_signal="b",
                    ),
                ),
            )

    def test_rejects_empty_mastery_indicators(self, concept_id: ConceptId) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningObjective(
                objective_id=LearningObjectiveId("lo-x"),
                concept_id=concept_id,
                statement="Do something",
                success_criteria=("criterion",),
                mastery_indicators=(),
            )

    @pytest.mark.parametrize("raw", ["", "   "])
    def test_rejects_blank_statement(
        self, concept_id: ConceptId, raw: str
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningObjective(
                objective_id=LearningObjectiveId("lo-x"),
                concept_id=concept_id,
                statement=raw,
                success_criteria=("criterion",),
                mastery_indicators=(
                    MasteryIndicator(description="a", observable_signal="b"),
                ),
            )

    def test_identity_equality(self, concept_id: ConceptId) -> None:
        left = make_objective(concept_id, objective_id="lo-same")
        right = make_objective(
            concept_id,
            objective_id="lo-same",
            statement="Different statement still same identity",
        )
        assert left == right
        assert hash(left) == hash(right)

    def test_belongs_to_false_for_other(self, concept_id: ConceptId) -> None:
        objective = make_objective(concept_id)
        assert objective.belongs_to(ConceptId("other-concept")) is False

    def test_rejects_wrong_id_types(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningObjective(
                objective_id="lo-x",  # type: ignore[arg-type]
                concept_id=ConceptId("c1"),
                statement="ok",
                success_criteria=("c",),
                mastery_indicators=(
                    MasteryIndicator(description="a", observable_signal="b"),
                ),
            )


class TestMisconception:
    def test_create_valid(self, concept_id: ConceptId) -> None:
        misc = make_misconception(concept_id)
        assert misc.belongs_to(concept_id)
        assert misc.entity_id == misc.misconception_id

    @pytest.mark.parametrize(
        "field",
        [
            "description",
            "incorrect_reasoning",
        ],
    )
    def test_rejects_blank_text(
        self, concept_id: ConceptId, field: str
    ) -> None:
        kwargs = {
            "misconception_id": MisconceptionId("m1"),
            "concept_id": concept_id,
            "description": "ok",
            "incorrect_reasoning": "ok",
            "likely_causes": ("cause",),
            "observable_evidence": ("evidence",),
            "recommended_teaching_intentions": (
                TeachingIntentionType.REPAIR_MISCONCEPTION,
            ),
            "recommended_strategies": (TeachingStrategyType.COUNTEREXAMPLE,),
            "repair_evidence": ("repair",),
            field: "  ",
        }
        with pytest.raises(EducationalInvariantViolation):
            Misconception(**kwargs)

    @pytest.mark.parametrize(
        "field",
        [
            "likely_causes",
            "observable_evidence",
            "repair_evidence",
            "recommended_teaching_intentions",
            "recommended_strategies",
        ],
    )
    def test_rejects_empty_collections(
        self, concept_id: ConceptId, field: str
    ) -> None:
        kwargs = {
            "misconception_id": MisconceptionId("m1"),
            "concept_id": concept_id,
            "description": "ok",
            "incorrect_reasoning": "ok",
            "likely_causes": ("cause",),
            "observable_evidence": ("evidence",),
            "recommended_teaching_intentions": (
                TeachingIntentionType.REPAIR_MISCONCEPTION,
            ),
            "recommended_strategies": (TeachingStrategyType.COUNTEREXAMPLE,),
            "repair_evidence": ("repair",),
            field: (),
        }
        with pytest.raises(EducationalInvariantViolation):
            Misconception(**kwargs)

    def test_identity_equality(self, concept_id: ConceptId) -> None:
        left = make_misconception(concept_id, misconception_id="m-same")
        right = make_misconception(concept_id, misconception_id="m-same")
        assert left == right


class TestRepresentation:
    def test_create_valid(self, concept_id: ConceptId) -> None:
        rep = make_representation(concept_id)
        assert rep.kind is RepresentationKind.SYMBOLIC
        assert rep.belongs_to(concept_id)

    @pytest.mark.parametrize("kind", list(RepresentationKind))
    def test_all_kinds_accepted(
        self, concept_id: ConceptId, kind: RepresentationKind
    ) -> None:
        rep = make_representation(
            concept_id,
            representation_id=f"rep-{kind.value}",
            kind=kind,
        )
        assert rep.kind is kind

    def test_rejects_invalid_kind(self, concept_id: ConceptId) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Representation(
                representation_id=RepresentationId("r1"),
                concept_id=concept_id,
                kind="decorative",  # type: ignore[arg-type]
                description="ok",
                educational_purpose="ok",
            )

    @pytest.mark.parametrize("field", ["description", "educational_purpose"])
    def test_rejects_blank(self, concept_id: ConceptId, field: str) -> None:
        kwargs = {
            "representation_id": RepresentationId("r1"),
            "concept_id": concept_id,
            "kind": RepresentationKind.VERBAL,
            "description": "ok",
            "educational_purpose": "ok",
            field: "",
        }
        with pytest.raises(EducationalInvariantViolation):
            Representation(**kwargs)

    def test_representation_id_rejects_whitespace(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RepresentationId("bad id")


class TestApplicationContext:
    def test_create_valid(self, concept_id: ConceptId) -> None:
        ctx = make_application_context(concept_id)
        assert ctx.belongs_to(concept_id)

    def test_optional_fields(self, concept_id: ConceptId) -> None:
        ctx = ApplicationContext(
            context_id=ApplicationContextId("app-min"),
            concept_id=concept_id,
            description="use situation",
            task_demand="compute",
        )
        assert ctx.assumptions is None
        assert ctx.constraints is None

    @pytest.mark.parametrize("field", ["description", "task_demand"])
    def test_rejects_blank(self, concept_id: ConceptId, field: str) -> None:
        kwargs = {
            "context_id": ApplicationContextId("app-x"),
            "concept_id": concept_id,
            "description": "ok",
            "task_demand": "ok",
            field: " ",
        }
        with pytest.raises(EducationalInvariantViolation):
            ApplicationContext(**kwargs)

    def test_rejects_blank_optional_when_provided(
        self, concept_id: ConceptId
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ApplicationContext(
                context_id=ApplicationContextId("app-x"),
                concept_id=concept_id,
                description="ok",
                task_demand="ok",
                assumptions="  ",
            )


class TestTransferContext:
    def test_create_valid(self, concept_id: ConceptId) -> None:
        ctx = make_transfer_context(concept_id)
        assert ctx.transfer_level is TransferLevel.NEAR

    def test_rejects_none_transfer_level(self, concept_id: ConceptId) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            TransferContext(
                context_id=TransferContextId("t1"),
                concept_id=concept_id,
                description="clone",
                surface_variation="none",
                underlying_demand="same",
                transfer_level=TransferLevel.NONE,
            )
        assert exc_info.value.invariant == "TransferContext.transfer_level.not_none"

    @pytest.mark.parametrize("level", [TransferLevel.NEAR, TransferLevel.FAR])
    def test_accepts_near_and_far(
        self, concept_id: ConceptId, level: TransferLevel
    ) -> None:
        ctx = make_transfer_context(concept_id, level=level)
        assert ctx.transfer_level is level

    def test_with_base_application_context(self, concept_id: ConceptId) -> None:
        base = ApplicationContextId("app-001")
        ctx = make_transfer_context(concept_id, base=base)
        assert ctx.base_application_context_id == base

    @pytest.mark.parametrize(
        "field",
        ["description", "surface_variation", "underlying_demand"],
    )
    def test_rejects_blank(self, concept_id: ConceptId, field: str) -> None:
        kwargs = {
            "context_id": TransferContextId("t1"),
            "concept_id": concept_id,
            "description": "ok",
            "surface_variation": "ok",
            "underlying_demand": "ok",
            "transfer_level": TransferLevel.FAR,
            field: "",
        }
        with pytest.raises(EducationalInvariantViolation):
            TransferContext(**kwargs)
