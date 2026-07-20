"""Policy governing educational dependency integrity.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md / SUBJECT_INVARIANTS.md
Concept
    Dependency Policy
"""

from __future__ import annotations

from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge.value_objects.dependency import Dependency

_PREREQUISITE_KINDS = frozenset(
    {
        DependencyKind.REQUIRED_PREREQUISITE,
        DependencyKind.HELPFUL_PREREQUISITE,
    }
)


class DependencyPolicy:
    """Enforces typed dependency law for a concept aggregate."""

    @staticmethod
    def assert_valid_kind(kind: DependencyKind) -> None:
        """Require ``kind`` to be a recognised educational DependencyKind."""
        if not isinstance(kind, DependencyKind):
            raise EducationalInvariantViolation(
                "dependency kind must be a valid DependencyKind",
                invariant="DependencyPolicy.kind.valid",
            )

    @staticmethod
    def assert_no_self_dependency(
        owner_concept_id: ConceptId,
        dependency: Dependency,
    ) -> None:
        """Forbid a concept depending on itself (educational nonsense)."""
        dependency.assert_not_self(owner_concept_id)

    @staticmethod
    def assert_not_duplicate(
        existing: tuple[Dependency, ...] | list[Dependency],
        candidate: Dependency,
    ) -> None:
        """Forbid duplicate (target, kind) dependency edges."""
        for edge in existing:
            if edge.same_edge(candidate):
                raise EducationalInvariantViolation(
                    "duplicate dependency is not allowed",
                    invariant="DependencyPolicy.no_duplicate",
                )

    @staticmethod
    def assert_can_add(
        owner_concept_id: ConceptId,
        existing: tuple[Dependency, ...] | list[Dependency],
        candidate: Dependency,
    ) -> None:
        """Run full admission checks for a new dependency."""
        DependencyPolicy.assert_valid_kind(candidate.kind)
        DependencyPolicy.assert_no_self_dependency(owner_concept_id, candidate)
        DependencyPolicy.assert_not_duplicate(existing, candidate)

    @staticmethod
    def is_prerequisite_kind(kind: DependencyKind) -> bool:
        """True for required or helpful prerequisite kinds."""
        return kind in _PREREQUISITE_KINDS

    @staticmethod
    def is_extension_kind(kind: DependencyKind) -> bool:
        """True when the dependency marks extension knowledge (K16)."""
        return kind is DependencyKind.EXTENSION

    @staticmethod
    def find_edge(
        existing: tuple[Dependency, ...] | list[Dependency],
        target_concept_id: ConceptId,
        kind: DependencyKind | None = None,
    ) -> Dependency | None:
        """Locate a dependency by target, optionally filtered by kind."""
        for edge in existing:
            if edge.target_concept_id != target_concept_id:
                continue
            if kind is not None and edge.kind is not kind:
                continue
            return edge
        return None
