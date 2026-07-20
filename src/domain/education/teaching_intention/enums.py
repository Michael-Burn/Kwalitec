"""Teaching Intention domain enumerations.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Status / Strength / Scope / Constraint / Revision
"""

from __future__ import annotations

from enum import StrEnum


class IntentionStatus(StrEnum):
    """Lifecycle status of a TeachingIntention aggregate.

    Teaching Intention states the educational change sought. It does not
    select teaching strategies or construct learning episodes. DRAFT allows
    intention-type amendment; ACTIVE locks the type; RETIRED is terminal.
    """

    DRAFT = "draft"
    ACTIVE = "active"
    REVISED = "revised"
    RETIRED = "retired"


class IntentionStrengthLevel(StrEnum):
    """Commitment strength of a teaching intention.

    Strength expresses how firmly the tutor commits to seeking this
    educational change. It is not priority score, diagnosis confidence,
    hypothesis plausibility, or a mastery claim.
    """

    TENTATIVE = "tentative"
    MODERATE = "moderate"
    FIRM = "firm"
    COMMITTED = "committed"


class IntentionScopeKind(StrEnum):
    """Grain of instructional scope for a teaching intention."""

    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    LEARNING_DIMENSION = "learning_dimension"
    MISCONCEPTION = "misconception"
    PREREQUISITE_CHAIN = "prerequisite_chain"
    CROSS_CONCEPT = "cross_concept"
    EXAM_HORIZON = "exam_horizon"
    TRANSFER_CONTEXT = "transfer_context"


class IntentionConstraintKind(StrEnum):
    """Educational constraints that a teaching intention must not contradict.

    Derived from Teaching Intention Model governing constraints and
    Educational Reasoning Invariants (intention precedes strategy; no
    mastery claim as episode outcome; atomicity; priority alignment).
    """

    REQUIRE_PRIORITY_REFERENCE = "require_priority_reference"
    REQUIRE_DIAGNOSIS_ALIGNMENT = "require_diagnosis_alignment"
    FORBID_MASTERY_CLAIM = "forbid_mastery_claim"
    FORBID_STRATEGY_SELECTION = "forbid_strategy_selection"
    REQUIRE_EVALUABLE_OUTCOME = "require_evaluable_outcome"
    PROTECT_ATOMICITY = "protect_atomicity"
    PROTECT_CONCEPTUAL_HONESTY_OVER_EXAM = "protect_conceptual_honesty_over_exam"
    CAP_STRENGTH = "cap_strength"
    FORBID_INTENTION_TYPE = "forbid_intention_type"
    REQUIRE_HYPOTHESIS_REFERENCE = "require_hypothesis_reference"


class IntentionRevisionKind(StrEnum):
    """Lawful forms of teaching-intention revision."""

    GOAL_AMENDED = "goal_amended"
    OUTCOME_AMENDED = "outcome_amended"
    SCOPE_AMENDED = "scope_amended"
    CONSTRAINTS_REPLACED = "constraints_replaced"
    REFERENCES_UPDATED = "references_updated"
    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    ACTIVATED = "activated"
    RETIRED = "retired"
    GENERAL = "general"
