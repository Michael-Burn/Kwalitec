"""Policy selecting Teaching Strategies that serve Teaching Intentions.

Architecture Source
    TEACHING_STRATEGY_CATALOGUE.md §4
    STRATEGY_SELECTION_MODEL.md
Concept
    Strategy Selection Policy
"""

from __future__ import annotations

from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.entities.strategy_reference import (
    DiagnosisReference,
    IntentionReference,
)

# Catalogue §4 — illustrative primary affinities (not exclusive).
_AFFINITY: dict[TeachingIntentionType, frozenset[TeachingStrategyType]] = {
    TeachingIntentionType.REPAIR_MISCONCEPTION: frozenset(
        {
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.ERROR_LED_TEACHING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
        }
    ),
    TeachingIntentionType.BUILD_INTUITION: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.ANALOGY,
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.WORKED_EXAMPLE,
        }
    ),
    TeachingIntentionType.STRENGTHEN_PREREQUISITE: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    TeachingIntentionType.IMPROVE_TRANSFER: frozenset(
        {
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.GUIDED_DISCOVERY,
        }
    ),
    TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingIntentionType.CONSOLIDATE_UNDERSTANDING: frozenset(
        {
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.DUAL_REPRESENTATION,
        }
    ),
    TeachingIntentionType.RECOVER_CONFIDENCE: frozenset(
        {
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.RETRIEVAL_FIRST,
        }
    ),
    TeachingIntentionType.PREPARE_FOR_EXAMINATION: frozenset(
        {
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    TeachingIntentionType.IMPROVE_RETENTION: frozenset(
        {
            TeachingStrategyType.RETRIEVAL_FIRST,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
        }
    ),
    TeachingIntentionType.CALIBRATE_CONFIDENCE_DOWNWARD: frozenset(
        {
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.ERROR_LED_TEACHING,
        }
    ),
    TeachingIntentionType.CONNECT_FRAGMENTED_KNOWLEDGE: frozenset(
        {
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.DUAL_REPRESENTATION,
        }
    ),
    TeachingIntentionType.STRENGTHEN_APPLICATION: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
        }
    ),
    TeachingIntentionType.COMPLETE_MISSING_FACETS: frozenset(
        {
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.DIRECT_EXPLANATION,
        }
    ),
}

# Hard contradictions — primary strategy unlawful for intention
# (Selection R-S1/R-S4, S14).
_FORBIDDEN_PRIMARY: dict[TeachingIntentionType, frozenset[TeachingStrategyType]] = {
    TeachingIntentionType.REPAIR_MISCONCEPTION: frozenset(
        {
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.RETRIEVAL_FIRST,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
        }
    ),
    TeachingIntentionType.BUILD_INTUITION: frozenset(
        {
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
    TeachingIntentionType.STRENGTHEN_PREREQUISITE: frozenset(
        {
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
}

# Diagnosis family → preferred method families (Selection Model R-S2).
_DIAGNOSIS_FAMILIES: dict[DiagnosisType, frozenset[TeachingStrategyType]] = {
    DiagnosisType.MISCONCEPTION: frozenset(
        {
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.ERROR_LED_TEACHING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
        }
    ),
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.ANALOGY,
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.DUAL_REPRESENTATION,
        }
    ),
    DiagnosisType.INCOMPLETE_UNDERSTANDING: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.ANALOGY,
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.CONCEPT_MAPPING,
        }
    ),
    DiagnosisType.PREREQUISITE_GAP: frozenset(
        {
            TeachingStrategyType.DIRECT_EXPLANATION,
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    DiagnosisType.PROCEDURAL_WEAKNESS: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
        }
    ),
    DiagnosisType.APPLICATION_WEAKNESS: frozenset(
        {
            TeachingStrategyType.WORKED_EXAMPLE,
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
            TeachingStrategyType.DELIBERATE_PRACTICE,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
        }
    ),
    DiagnosisType.WEAK_RETENTION: frozenset(
        {
            TeachingStrategyType.RETRIEVAL_FIRST,
            TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
            TeachingStrategyType.SPACED_REINFORCEMENT,
        }
    ),
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: frozenset(
        {
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.CONCEPT_MAPPING,
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.DUAL_REPRESENTATION,
        }
    ),
    DiagnosisType.TRANSFER_WEAKNESS: frozenset(
        {
            TeachingStrategyType.INTERLEAVING,
            TeachingStrategyType.DUAL_REPRESENTATION,
            TeachingStrategyType.GUIDED_DISCOVERY,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.EXAM_SIMULATION,
        }
    ),
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: frozenset(
        {
            TeachingStrategyType.EXAM_SIMULATION,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
            TeachingStrategyType.INTERLEAVING,
        }
    ),
    DiagnosisType.LOW_CONFIDENCE: frozenset(
        {
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.THINK_ALOUD_MODELLING,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.RETRIEVAL_FIRST,
        }
    ),
    DiagnosisType.FALSE_CONFIDENCE: frozenset(
        {
            TeachingStrategyType.COUNTEREXAMPLE,
            TeachingStrategyType.SOCRATIC_QUESTIONING,
            TeachingStrategyType.CONCEPT_COMPARISON,
            TeachingStrategyType.ERROR_LED_TEACHING,
        }
    ),
}

_MISCONCEPTION_FAMILY = frozenset(
    {
        TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
        TeachingStrategyType.COUNTEREXAMPLE,
        TeachingStrategyType.ERROR_LED_TEACHING,
        TeachingStrategyType.CONCEPT_COMPARISON,
        TeachingStrategyType.SOCRATIC_QUESTIONING,
    }
)

_CATALOGUE: frozenset[TeachingStrategyType] = frozenset(TeachingStrategyType)


class StrategySelectionPolicy:
    """Ensures strategy selection serves intention and respects diagnosis.

    Selection answers whether a catalogue strategy is a lawful *how* for the
    named Teaching Intention. It does not execute episodes or score twins.
    """

    @staticmethod
    def catalogue() -> frozenset[TeachingStrategyType]:
        """Return the full Teaching Strategy Catalogue (no invented types)."""
        return _CATALOGUE

    @staticmethod
    def preferred_for_intention(
        intention_type: TeachingIntentionType,
    ) -> frozenset[TeachingStrategyType]:
        if not isinstance(intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="StrategySelectionPolicy.intention_type.type",
            )
        return _AFFINITY[intention_type]

    @staticmethod
    def preferred_for_diagnosis(
        diagnosis_type: DiagnosisType,
    ) -> frozenset[TeachingStrategyType]:
        if not isinstance(diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="StrategySelectionPolicy.diagnosis_type.type",
            )
        return _DIAGNOSIS_FAMILIES[diagnosis_type]

    @staticmethod
    def is_catalogue_strategy(strategy_type: TeachingStrategyType) -> bool:
        return strategy_type in _CATALOGUE

    @staticmethod
    def is_preferred_for_intention(
        strategy_type: TeachingStrategyType,
        intention_type: TeachingIntentionType,
    ) -> bool:
        return strategy_type in StrategySelectionPolicy.preferred_for_intention(
            intention_type
        )

    @staticmethod
    def is_forbidden_primary(
        strategy_type: TeachingStrategyType,
        intention_type: TeachingIntentionType,
    ) -> bool:
        forbidden = _FORBIDDEN_PRIMARY.get(intention_type, frozenset())
        return strategy_type in forbidden

    @staticmethod
    def is_lawful_for_intention(
        strategy_type: TeachingStrategyType,
        intention_type: TeachingIntentionType,
    ) -> bool:
        """Lawful when catalogue-named and not a hard contradiction."""
        if not StrategySelectionPolicy.is_catalogue_strategy(strategy_type):
            return False
        return not StrategySelectionPolicy.is_forbidden_primary(
            strategy_type, intention_type
        )

    @staticmethod
    def assert_serves_intention(
        strategy_type: TeachingStrategyType,
        intention_references: tuple[IntentionReference, ...]
        | list[IntentionReference],
        *,
        require_affinity: bool = False,
    ) -> None:
        if not intention_references:
            raise EducationalInvariantViolation(
                "strategy must reference Teaching Intention",
                invariant="StrategySelectionPolicy.intention_references.min_one",
            )
        primary_intention = intention_references[0].intention_type
        if not StrategySelectionPolicy.is_lawful_for_intention(
            strategy_type, primary_intention
        ):
            raise EducationalInvariantViolation(
                f"strategy {strategy_type.value} contradicts Teaching Intention "
                f"{primary_intention.value}",
                invariant="StrategySelectionPolicy.intention_contradiction",
            )
        if require_affinity and not StrategySelectionPolicy.is_preferred_for_intention(
            strategy_type, primary_intention
        ):
            raise EducationalInvariantViolation(
                f"strategy {strategy_type.value} lacks affinity with intention "
                f"{primary_intention.value}",
                invariant="StrategySelectionPolicy.intention_affinity",
            )

    @staticmethod
    def assert_misconception_duty(
        strategy_type: TeachingStrategyType,
        intention_references: tuple[IntentionReference, ...]
        | list[IntentionReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> None:
        """S14 — stable misconception diagnosis requires explicit repair strategy."""
        intention_types = {ref.intention_type for ref in intention_references}
        diagnosis_types = {ref.diagnosis_type for ref in diagnosis_references}
        if (
            TeachingIntentionType.REPAIR_MISCONCEPTION in intention_types
            or DiagnosisType.MISCONCEPTION in diagnosis_types
        ):
            if strategy_type not in _MISCONCEPTION_FAMILY:
                raise EducationalInvariantViolation(
                    "misconception diagnosis requires an explicit confrontation "
                    "or displacement strategy",
                    invariant="StrategySelectionPolicy.misconception_duty",
                )

    @staticmethod
    def assert_not_exam_over_misconception(
        strategy_type: TeachingStrategyType,
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> None:
        """S18 — exam tactics must not erase conceptual duties."""
        diagnosis_types = {ref.diagnosis_type for ref in diagnosis_references}
        if (
            DiagnosisType.MISCONCEPTION in diagnosis_types
            and strategy_type is TeachingStrategyType.EXAM_SIMULATION
        ):
            raise EducationalInvariantViolation(
                "exam simulation must not skip misconception repair",
                invariant="StrategySelectionPolicy.forbid_exam_over_misconception",
            )
