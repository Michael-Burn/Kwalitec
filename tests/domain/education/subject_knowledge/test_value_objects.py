"""Tests for Subject Knowledge value objects."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import DependencyKind, LearningDimension
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge import (
    ConceptBoundary,
    Dependency,
    MasteryIndicator,
)


class TestConceptBoundary:
    def test_accepts_valid_boundary(self) -> None:
        boundary = ConceptBoundary(
            inclusion="inside",
            exclusion="outside",
            key_contrast="A vs B",
        )
        assert boundary.inclusion == "inside"
        assert boundary.marks_contrast() is True

    def test_contrast_optional(self) -> None:
        boundary = ConceptBoundary(inclusion="in", exclusion="out")
        assert boundary.key_contrast is None
        assert boundary.marks_contrast() is False

    @pytest.mark.parametrize("field", ["inclusion", "exclusion"])
    @pytest.mark.parametrize("raw", ["", "   ", None])
    def test_rejects_blank_required_fields(
        self, field: str, raw: str | None
    ) -> None:
        kwargs = {"inclusion": "in", "exclusion": "out", field: raw}
        with pytest.raises(EducationalInvariantViolation):
            ConceptBoundary(**kwargs)  # type: ignore[arg-type]

    def test_rejects_blank_contrast(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptBoundary(inclusion="in", exclusion="out", key_contrast="  ")

    def test_strips_whitespace(self) -> None:
        boundary = ConceptBoundary(
            inclusion="  in  ",
            exclusion="  out  ",
            key_contrast="  contrast  ",
        )
        assert boundary.inclusion == "in"
        assert boundary.exclusion == "out"
        assert boundary.key_contrast == "contrast"

    def test_frozen(self) -> None:
        boundary = ConceptBoundary(inclusion="in", exclusion="out")
        with pytest.raises(AttributeError):
            boundary.inclusion = "mutated"  # type: ignore[misc]

    def test_equality(self) -> None:
        left = ConceptBoundary(inclusion="in", exclusion="out")
        right = ConceptBoundary(inclusion="in", exclusion="out")
        assert left == right


class TestMasteryIndicator:
    def test_accepts_valid_indicator(self) -> None:
        indicator = MasteryIndicator(
            description="explains why",
            observable_signal="states conditions",
            dimension=LearningDimension.APPLICATION,
        )
        assert indicator.dimension is LearningDimension.APPLICATION

    def test_dimension_optional(self) -> None:
        indicator = MasteryIndicator(
            description="explains why",
            observable_signal="states conditions",
        )
        assert indicator.dimension is None

    @pytest.mark.parametrize("field", ["description", "observable_signal"])
    @pytest.mark.parametrize("raw", ["", "   "])
    def test_rejects_blank(self, field: str, raw: str) -> None:
        kwargs = {
            "description": "ok",
            "observable_signal": "ok",
            field: raw,
        }
        with pytest.raises(EducationalInvariantViolation):
            MasteryIndicator(**kwargs)

    def test_rejects_invalid_dimension(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryIndicator(
                description="ok",
                observable_signal="ok",
                dimension="not-a-dimension",  # type: ignore[arg-type]
            )

    def test_frozen(self) -> None:
        indicator = MasteryIndicator(
            description="ok",
            observable_signal="ok",
        )
        with pytest.raises(AttributeError):
            indicator.description = "x"  # type: ignore[misc]

    def test_equality(self) -> None:
        left = MasteryIndicator(description="a", observable_signal="b")
        right = MasteryIndicator(description="a", observable_signal="b")
        assert left == right


class TestDependency:
    def test_accepts_valid_dependency(self) -> None:
        dep = Dependency(
            target_concept_id=ConceptId("concept-a"),
            kind=DependencyKind.REQUIRED_PREREQUISITE,
            description="foundation required",
        )
        assert dep.kind is DependencyKind.REQUIRED_PREREQUISITE

    @pytest.mark.parametrize("kind", list(DependencyKind))
    def test_all_dependency_kinds_valid(self, kind: DependencyKind) -> None:
        dep = Dependency(
            target_concept_id=ConceptId("concept-a"),
            kind=kind,
            description=f"edge of kind {kind}",
        )
        assert dep.kind is kind

    def test_rejects_invalid_kind(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Dependency(
                target_concept_id=ConceptId("concept-a"),
                kind="related_to",  # type: ignore[arg-type]
                description="vague",
            )

    def test_rejects_invalid_target_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Dependency(
                target_concept_id="concept-a",  # type: ignore[arg-type]
                kind=DependencyKind.PARALLEL,
                description="ok",
            )

    @pytest.mark.parametrize("raw", ["", "   "])
    def test_rejects_blank_description(self, raw: str) -> None:
        with pytest.raises(EducationalInvariantViolation):
            Dependency(
                target_concept_id=ConceptId("concept-a"),
                kind=DependencyKind.EXTENSION,
                description=raw,
            )

    def test_assert_not_self_rejects_self(self) -> None:
        owner = ConceptId("concept-a")
        dep = Dependency(
            target_concept_id=owner,
            kind=DependencyKind.HELPFUL_PREREQUISITE,
            description="illegal self",
        )
        with pytest.raises(EducationalInvariantViolation) as exc_info:
            dep.assert_not_self(owner)
        assert exc_info.value.invariant == "Dependency.no_self_dependency"

    def test_assert_not_self_allows_other(self) -> None:
        dep = Dependency(
            target_concept_id=ConceptId("concept-b"),
            kind=DependencyKind.REQUIRED_PREREQUISITE,
            description="ok",
        )
        dep.assert_not_self(ConceptId("concept-a"))

    def test_same_edge(self) -> None:
        target = ConceptId("concept-b")
        left = Dependency(
            target_concept_id=target,
            kind=DependencyKind.EXTENSION,
            description="one",
        )
        right = Dependency(
            target_concept_id=target,
            kind=DependencyKind.EXTENSION,
            description="two",
        )
        other = Dependency(
            target_concept_id=target,
            kind=DependencyKind.PARALLEL,
            description="different kind",
        )
        assert left.same_edge(right) is True
        assert left.same_edge(other) is False

    def test_frozen(self) -> None:
        dep = Dependency(
            target_concept_id=ConceptId("concept-a"),
            kind=DependencyKind.REMEDIATION,
            description="repair first",
        )
        with pytest.raises(AttributeError):
            dep.description = "x"  # type: ignore[misc]
