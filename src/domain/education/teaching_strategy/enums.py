"""Teaching Strategy domain enumerations.

Architecture Source
    TEACHING_STRATEGY_CATALOGUE.md
    STRATEGY_COMPOSITION_MODEL.md
    STRATEGY_INVARIANTS.md
Concept
    Strategy Status / Effectiveness / Complexity / Constraint / Revision / Composition
"""

from __future__ import annotations

from enum import StrEnum


class StrategyStatus(StrEnum):
    """Lifecycle status of a TeachingStrategy aggregate.

    Teaching Strategy states *how* the tutor intends to teach. DRAFT allows
    primary-type amendment; SELECTED locks the primary commitment; RETIRED
    is terminal and forbids further revision.
    """

    DRAFT = "draft"
    SELECTED = "selected"
    REVISED = "revised"
    RETIRED = "retired"


class EffectivenessLevel(StrEnum):
    """Expected educational effectiveness of a selected strategy.

    Effectiveness is an educational estimate, not a mastery score, twin
    metric, or implementation KPI.
    """

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    UNCERTAIN = "uncertain"


class ComplexityLevel(StrEnum):
    """Instructional complexity / cognitive demand of a strategy.

    Used to cap ambition under load (Strategy Selection Model R-S11).
    """

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class StrategyConstraintKind(StrEnum):
    """Educational constraints that a teaching strategy must not contradict.

    Derived from Strategy Invariants (S1–S20), Selection Model, and
    Composition Model governing rules.
    """

    REQUIRE_INTENTION_REFERENCE = "require_intention_reference"
    REQUIRE_DIAGNOSIS_REFERENCE = "require_diagnosis_reference"
    REQUIRE_RATIONALE = "require_rationale"
    REQUIRE_EFFECTIVENESS = "require_effectiveness"
    REQUIRE_INTENTION_AFFINITY = "require_intention_affinity"
    FORBID_MASTERY_CLAIM = "forbid_mastery_claim"
    FORBID_COEQUAL_PRIMARIES = "forbid_coequal_primaries"
    PROTECT_ATOMICITY = "protect_atomicity"
    FORBID_STRATEGY_TYPE = "forbid_strategy_type"
    CAP_COMPLEXITY = "cap_complexity"
    REQUIRE_MISCONCEPTION_STRATEGY = "require_misconception_strategy"
    FORBID_EXAM_OVER_MISCONCEPTION = "forbid_exam_over_misconception"
    REQUIRE_HYPOTHESIS_REFERENCE = "require_hypothesis_reference"


class StrategyRevisionKind(StrEnum):
    """Lawful forms of teaching-strategy revision."""

    PRIMARY_CHANGED = "primary_changed"
    SECONDARIES_COMPOSED = "secondaries_composed"
    SECONDARIES_DECOMPOSED = "secondaries_decomposed"
    RATIONALE_AMENDED = "rationale_amended"
    EFFECTIVENESS_AMENDED = "effectiveness_amended"
    GOAL_AMENDED = "goal_amended"
    COMPLEXITY_AMENDED = "complexity_amended"
    CONSTRAINTS_REPLACED = "constraints_replaced"
    REFERENCES_UPDATED = "references_updated"
    SELECTED = "selected"
    RETIRED = "retired"
    GENERAL = "general"


class CompositionPattern(StrEnum):
    """Canonical composition arcs from Strategy Composition Model §6."""

    ANALOGY_TO_GUIDED_PRACTICE = "analogy_to_guided_practice"
    MISCONCEPTION_REPAIR_ARC = "misconception_repair_arc"
    MODELLING_TO_INDEPENDENCE = "modelling_to_independence"
    RETENTION_ARC = "retention_arc"
    DISCRIMINATION_TO_EXAM = "discrimination_to_exam"
    DISCOVERY_DEEPENING = "discovery_deepening"
    INTUITION_TO_FORM = "intuition_to_form"
    CUSTOM = "custom"
