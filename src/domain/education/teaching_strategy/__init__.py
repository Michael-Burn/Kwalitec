"""Teaching Strategy bounded context — pure educational domain model.

IMP-010 implementation of Teaching Strategy architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

This domain converts Teaching Intentions into instructional strategies.
It answers only: how does the tutor intend to produce the desired educational
change? It does not enact learning episodes, score twins, or prescribe
prompts/screens.
"""

from __future__ import annotations

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy.aggregates.teaching_strategy import (
    TeachingStrategy,
)
from domain.education.teaching_strategy.entities.strategy_constraint import (
    StrategyConstraint,
    StrategyConstraintId,
)
from domain.education.teaching_strategy.entities.strategy_goal import (
    StrategyGoal,
    StrategyGoalId,
)
from domain.education.teaching_strategy.entities.strategy_rationale import (
    StrategyRationale,
    StrategyRationaleId,
)
from domain.education.teaching_strategy.entities.strategy_reference import (
    DiagnosisReference,
    HypothesisReference,
    IntentionReference,
    SecondaryStrategyReference,
)
from domain.education.teaching_strategy.enums import (
    ComplexityLevel,
    CompositionPattern,
    EffectivenessLevel,
    StrategyConstraintKind,
    StrategyRevisionKind,
    StrategyStatus,
)
from domain.education.teaching_strategy.events.strategy_revised import (
    TeachingStrategyRevised,
)
from domain.education.teaching_strategy.events.strategy_selected import (
    TeachingStrategySelected,
)
from domain.education.teaching_strategy.policies.strategy_composition_policy import (
    StrategyCompositionPolicy,
)
from domain.education.teaching_strategy.policies.strategy_selection_policy import (
    StrategySelectionPolicy,
)
from domain.education.teaching_strategy.policies.strategy_validation_policy import (
    StrategyValidationPolicy,
)
from domain.education.teaching_strategy.specifications.strategy_is_applicable import (
    StrategyIsApplicableSpecification,
)
from domain.education.teaching_strategy.specifications.strategy_is_composable import (
    StrategyIsComposableSpecification,
)
from domain.education.teaching_strategy.value_objects.instructional_complexity import (
    InstructionalComplexity,
)
from domain.education.teaching_strategy.value_objects.strategy_effectiveness import (
    StrategyEffectiveness,
)

__all__ = [
    # Aggregate
    "TeachingStrategy",
    # Entities
    "StrategyGoal",
    "StrategyGoalId",
    "StrategyRationale",
    "StrategyRationaleId",
    "StrategyConstraint",
    "StrategyConstraintId",
    "IntentionReference",
    "DiagnosisReference",
    "HypothesisReference",
    "SecondaryStrategyReference",
    # Value objects / identity
    "StrategyEffectiveness",
    "InstructionalComplexity",
    "TeachingStrategyId",
    "TeachingStrategyType",
    # Enums
    "StrategyStatus",
    "EffectivenessLevel",
    "ComplexityLevel",
    "StrategyConstraintKind",
    "StrategyRevisionKind",
    "CompositionPattern",
    # Policies
    "StrategyValidationPolicy",
    "StrategySelectionPolicy",
    "StrategyCompositionPolicy",
    # Specifications
    "StrategyIsApplicableSpecification",
    "StrategyIsComposableSpecification",
    # Events
    "TeachingStrategySelected",
    "TeachingStrategyRevised",
]
