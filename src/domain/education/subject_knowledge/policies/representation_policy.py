"""Policy governing representation uniqueness within a concept.

Architecture Source
    REPRESENTATION_MODEL.md / SUBJECT_INVARIANTS.md
Concept
    Representation Policy
"""

from __future__ import annotations

from domain.education.foundation.enums import RepresentationKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.subject_knowledge.entities.representation import Representation


class RepresentationPolicy:
    """Enforces unique representation identity and unique kinds per concept."""

    @staticmethod
    def assert_valid_kind(kind: RepresentationKind) -> None:
        """Require a recognised RepresentationKind."""
        if not isinstance(kind, RepresentationKind):
            raise EducationalInvariantViolation(
                "representation kind must be a valid RepresentationKind",
                invariant="RepresentationPolicy.kind.valid",
            )

    @staticmethod
    def assert_not_duplicate_identity(
        existing: tuple[Representation, ...] | list[Representation],
        candidate: Representation,
    ) -> None:
        """Forbid registering the same representation identity twice."""
        for item in existing:
            if item.representation_id == candidate.representation_id:
                raise EducationalInvariantViolation(
                    "duplicate representation is not allowed",
                    invariant="RepresentationPolicy.no_duplicate_identity",
                )

    @staticmethod
    def assert_kind_unique(
        existing: tuple[Representation, ...] | list[Representation],
        candidate: Representation,
    ) -> None:
        """Forbid two representations of the same kind on one concept."""
        for item in existing:
            if item.kind is candidate.kind:
                raise EducationalInvariantViolation(
                    "representation kinds must be unique within a concept",
                    invariant="RepresentationPolicy.kind.unique",
                )

    @staticmethod
    def assert_can_register(
        existing: tuple[Representation, ...] | list[Representation],
        candidate: Representation,
    ) -> None:
        """Run full admission checks for a new representation."""
        RepresentationPolicy.assert_valid_kind(candidate.kind)
        RepresentationPolicy.assert_not_duplicate_identity(existing, candidate)
        RepresentationPolicy.assert_kind_unique(existing, candidate)
