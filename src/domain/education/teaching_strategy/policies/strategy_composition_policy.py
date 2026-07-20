"""Policy composing Teaching Strategies across instructional arcs.

Architecture Source
    STRATEGY_COMPOSITION_MODEL.md
Concept
    Strategy Composition Policy
"""

from __future__ import annotations

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.entities.strategy_reference import (
    SecondaryStrategyReference,
)
from domain.education.teaching_strategy.enums import CompositionPattern

# Canonical ordered arcs (Composition Model §6) — primary first, then secondaries.
_CANONICAL_ARCS: dict[CompositionPattern, tuple[TeachingStrategyType, ...]] = {
    CompositionPattern.ANALOGY_TO_GUIDED_PRACTICE: (
        TeachingStrategyType.ANALOGY,
        TeachingStrategyType.WORKED_EXAMPLE,
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
    ),
    CompositionPattern.MISCONCEPTION_REPAIR_ARC: (
        TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
        TeachingStrategyType.COUNTEREXAMPLE,
        TeachingStrategyType.ERROR_LED_TEACHING,
    ),
    CompositionPattern.MODELLING_TO_INDEPENDENCE: (
        TeachingStrategyType.WORKED_EXAMPLE,
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
        TeachingStrategyType.FADED_GUIDANCE,
    ),
    CompositionPattern.RETENTION_ARC: (
        TeachingStrategyType.RETRIEVAL_FIRST,
        TeachingStrategyType.DIRECT_EXPLANATION,
        TeachingStrategyType.SPACED_REINFORCEMENT,
    ),
    CompositionPattern.DISCRIMINATION_TO_EXAM: (
        TeachingStrategyType.CONCEPT_COMPARISON,
        TeachingStrategyType.INTERLEAVING,
        TeachingStrategyType.EXAM_SIMULATION,
    ),
    CompositionPattern.DISCOVERY_DEEPENING: (
        TeachingStrategyType.GUIDED_DISCOVERY,
        TeachingStrategyType.SOCRATIC_QUESTIONING,
        TeachingStrategyType.CONCEPT_MAPPING,
        TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
    ),
    CompositionPattern.INTUITION_TO_FORM: (
        TeachingStrategyType.ANALOGY,
        TeachingStrategyType.DUAL_REPRESENTATION,
        TeachingStrategyType.DIRECT_EXPLANATION,
        TeachingStrategyType.CONCEPT_COMPARISON,
    ),
}

# Lawful next-stage candidates after a primary (defeasible ordering).
_COMPATIBLE_FOLLOW_ONS: dict[TeachingStrategyType, frozenset[TeachingStrategyType]] = {
    TeachingStrategyType.ANALOGY: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.GUIDED_DISCOVERY,
        }
    ),
    TeachingStrategyType.DIRECT_EXPLANATION: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
        }
    ),
    TeachingStrategyType.WORKED_EXAMPLE: frozenset(
        {
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
        }
    ),
    TeachingStrategyType.GUIDED_DISCOVERY: frozenset(
        {
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.CONCEPT_COMPARISON,
        }
    ),
    TeachingStrategyType.SOCRATIC_QUESTIONING: frozenset(
        {
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.ERROR_LED_TEACHING,
        }
    ),
    TeachingStrategyType.MISCONCEPTION_CONFRONTATION: frozenset(
        {
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.ERROR_LED_TEACHING,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingStrategyType.COUNTEREXAMPLE: frozenset(
        {
            TeachingStrategyType.ERROR_LED_TEACHING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.CONCEPT_COMPARISON,
        }
    ),
    TeachingStrategyType.ERROR_LED_TEACHING: frozenset(
        {
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    TeachingStrategyType.PROGRESSIVE_SCAFFOLDING: frozenset(
        {
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingStrategyType.FADED_GUIDANCE: frozenset(
        {
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
    TeachingStrategyType.RETRIEVAL_FIRST: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.ERROR_LED_TEACHING,
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION: frozenset(
        {
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
    TeachingStrategyType.CONCEPT_COMPARISON: frozenset(
        {
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.DUAL_REPRESENTATION,
        }
    ),
    TeachingStrategyType.CONCEPT_MAPPING: frozenset(
        {
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.CONCEPT_COMPARISON,
        }
    ),
    TeachingStrategyType.INTERLEAVING: frozenset(
        {
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    TeachingStrategyType.THINK_ALOUD_MODELLING: frozenset(
        {
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.WORKED_EXAMPLE,
        }
    ),
    TeachingStrategyType.DUAL_REPRESENTATION: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingStrategyType.DELIBERATE_PRACTICE: frozenset(
        {
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.SPACED_REINFORCEMENT,
        }
    ),
    TeachingStrategyType.SPACED_REINFORCEMENT: frozenset(
        {
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
    TeachingStrategyType.EXAM_SIMULATION: frozenset(
        {
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
        }
    ),
}

# Anti-pattern: these must never be co-composed as secondary to the primary.
_INCOMPATIBLE_PAIRS: frozenset[
    tuple[TeachingStrategyType, TeachingStrategyType]
] = frozenset(
    {
        (
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            TeachingStrategyType.EXAM_SIMULATION,
        ),
        (
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            TeachingStrategyType.INTERLEAVING,
        ),
        (
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
        ),
        (
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.EXAM_SIMULATION,
        ),
        (TeachingStrategyType.ANALOGY, TeachingStrategyType.EXAM_SIMULATION),
        (
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.EXAM_SIMULATION,
        ),
        (
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
        ),
        (
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
        ),
    }
)

_MAX_SECONDARIES = 3


class StrategyCompositionPolicy:
    """Enforces composition rules without executing episodes.

    Composition sequences strategies across episodes under one primary per
    episode. It forbids kitchen-sink co-equal strategies and duplicate
    members in an arc.
    """

    @staticmethod
    def canonical_arc(
        pattern: CompositionPattern,
    ) -> tuple[TeachingStrategyType, ...]:
        if pattern is CompositionPattern.CUSTOM:
            raise EducationalInvariantViolation(
                "CUSTOM composition has no fixed canonical arc",
                invariant="StrategyCompositionPolicy.canonical.custom",
            )
        if pattern not in _CANONICAL_ARCS:
            raise EducationalInvariantViolation(
                f"unknown composition pattern {pattern}",
                invariant="StrategyCompositionPolicy.canonical.unknown",
            )
        return _CANONICAL_ARCS[pattern]

    @staticmethod
    def compatible_follow_ons(
        primary: TeachingStrategyType,
    ) -> frozenset[TeachingStrategyType]:
        if not isinstance(primary, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "primary must be a TeachingStrategyType",
                invariant="StrategyCompositionPolicy.primary.type",
            )
        return _COMPATIBLE_FOLLOW_ONS.get(primary, frozenset())

    @staticmethod
    def is_compatible(
        primary: TeachingStrategyType,
        secondary: TeachingStrategyType,
    ) -> bool:
        if primary is secondary:
            return False
        if (primary, secondary) in _INCOMPATIBLE_PAIRS:
            return False
        follow_ons = StrategyCompositionPolicy.compatible_follow_ons(primary)
        if not follow_ons:
            return True
        return secondary in follow_ons

    @staticmethod
    def matches_canonical_prefix(
        primary: TeachingStrategyType,
        secondaries: tuple[TeachingStrategyType, ...] | list[TeachingStrategyType],
    ) -> CompositionPattern | None:
        sequence = (primary, *tuple(secondaries))
        for pattern, arc in _CANONICAL_ARCS.items():
            if sequence == arc[: len(sequence)] and len(sequence) <= len(arc):
                return pattern
        return None

    @staticmethod
    def _pair_forbidden(
        left: TeachingStrategyType,
        right: TeachingStrategyType,
    ) -> bool:
        return (left, right) in _INCOMPATIBLE_PAIRS

    @staticmethod
    def assert_secondaries(
        primary: TeachingStrategyType,
        secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference],
    ) -> tuple[SecondaryStrategyReference, ...]:
        collected = tuple(secondaries)
        if len(collected) > _MAX_SECONDARIES:
            raise EducationalInvariantViolation(
                f"composition may include at most {_MAX_SECONDARIES} secondary "
                "strategies",
                invariant="StrategyCompositionPolicy.secondaries.max",
            )
        seen_types: set[TeachingStrategyType] = {primary}
        seen_orders: set[int] = set()
        for ref in collected:
            if not isinstance(ref, SecondaryStrategyReference):
                raise EducationalInvariantViolation(
                    "secondaries must be SecondaryStrategyReference values",
                    invariant="StrategyCompositionPolicy.secondaries.type",
                )
            if ref.strategy_type in seen_types:
                raise EducationalInvariantViolation(
                    "cannot duplicate composed strategies",
                    invariant="StrategyCompositionPolicy.secondaries.no_duplicate",
                )
            if ref.sequence_order in seen_orders:
                raise EducationalInvariantViolation(
                    "secondary sequence_order values must be unique",
                    invariant="StrategyCompositionPolicy.secondaries.order_unique",
                )
            if StrategyCompositionPolicy._pair_forbidden(
                primary, ref.strategy_type
            ):
                raise EducationalInvariantViolation(
                    f"strategy {ref.strategy_type.value} is incompatible with "
                    f"primary {primary.value}",
                    invariant="StrategyCompositionPolicy.compatibility",
                )
            seen_types.add(ref.strategy_type)
            seen_orders.add(ref.sequence_order)

        ordered = tuple(sorted(collected, key=lambda r: r.sequence_order))
        expected_orders = tuple(range(1, len(ordered) + 1))
        actual_orders = tuple(ref.sequence_order for ref in ordered)
        if actual_orders != expected_orders:
            raise EducationalInvariantViolation(
                "secondary sequence_order must be contiguous starting at 1",
                invariant="StrategyCompositionPolicy.secondaries.order_contiguous",
            )

        secondary_types = tuple(ref.strategy_type for ref in ordered)
        if StrategyCompositionPolicy.matches_canonical_prefix(
            primary, secondary_types
        ):
            return ordered

        previous = primary
        for strategy_type in secondary_types:
            if not StrategyCompositionPolicy.is_compatible(previous, strategy_type):
                raise EducationalInvariantViolation(
                    f"strategy {strategy_type.value} is not composable "
                    f"after {previous.value}",
                    invariant="StrategyCompositionPolicy.compatibility",
                )
            previous = strategy_type
        return ordered

    @staticmethod
    def assert_compose_types(
        primary: TeachingStrategyType,
        secondary_types: tuple[TeachingStrategyType, ...]
        | list[TeachingStrategyType],
    ) -> tuple[SecondaryStrategyReference, ...]:
        refs = [
            SecondaryStrategyReference(
                strategy_type=strategy_type,
                sequence_order=index,
            )
            for index, strategy_type in enumerate(secondary_types, start=1)
        ]
        return StrategyCompositionPolicy.assert_secondaries(primary, refs)

    @staticmethod
    def assert_no_coequal_primaries(
        primary: TeachingStrategyType,
        secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference],
    ) -> None:
        """C1 / S11 — exactly one primary; secondaries remain subordinate."""
        if not secondaries:
            return
        for ref in secondaries:
            if ref.strategy_type is primary:
                raise EducationalInvariantViolation(
                    "secondary strategies must not duplicate the primary",
                    invariant="StrategyCompositionPolicy.no_coequal_primaries",
                )
