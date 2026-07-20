"""Educational Priority domain enumerations.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Status / Factor Kind / Urgency / Impact / Constraint / Revision
"""

from __future__ import annotations

from enum import StrEnum


class PriorityStatus(StrEnum):
    """Lifecycle status of an EducationalPriority aggregate.

    Priority orders diagnosed educational work. It does not diagnose, explain,
    or select teaching strategies. STABILISED locks the current ordering until
    an explicit recalculation.
    """

    ASSIGNED = "assigned"
    REVISED = "revised"
    STABILISED = "stabilised"


class PriorityFactorKind(StrEnum):
    """Catalogue of educational priority factors (Priority Model).

    Factors contribute to instructional ordering. They are not severity of
    learner condition and not teaching-strategy selectors.
    """

    PREREQUISITE_IMPORTANCE = "prerequisite_importance"
    TRANSFER_BLOCKING = "transfer_blocking"
    EXAM_RELEVANCE = "exam_relevance"
    CONCEPT_CENTRALITY = "concept_centrality"
    LEARNING_DEPENDENCY_DEPTH = "learning_dependency_depth"
    MISCONCEPTION_PERSISTENCE = "misconception_persistence"
    EDUCATIONAL_LEVERAGE = "educational_leverage"
    CONFIDENCE_IN_DIAGNOSIS = "confidence_in_diagnosis"


class PriorityScoreBand(StrEnum):
    """Qualitative instructional-ordering band.

    Distinct from diagnosis severity. Severity describes learner condition;
    priority score describes what the tutor should address first.
    """

    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UrgencyLevel(StrEnum):
    """Temporal pressure on instructional ordering.

    Urgency may rise near examinations without abolishing higher gates
    (Priority Model §7). It never invents educational need.
    """

    DEFERRED = "deferred"
    ROUTINE = "routine"
    ELEVATED = "elevated"
    IMMEDIATE = "immediate"
    CRITICAL = "critical"


class InstructionalImpactLevel(StrEnum):
    """Expected instructional consequence of addressing this priority first."""

    MARGINAL = "marginal"
    MATERIAL = "material"
    SUBSTANTIAL = "substantial"
    TRANSFORMATIONAL = "transformational"


class PriorityScopeKind(StrEnum):
    """Grain of educational scope for a priority decision."""

    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    LEARNING_EPISODE = "learning_episode"
    LEARNING_DIMENSION = "learning_dimension"
    CROSS_CONCEPT = "cross_concept"
    PREREQUISITE_CHAIN = "prerequisite_chain"
    SESSION_WINDOW = "session_window"
    COMPETING_DIAGNOSES = "competing_diagnoses"


class PriorityConstraintKind(StrEnum):
    """Educational constraints that priority ordering must not contradict.

    Derived from Priority Model principles P1–P8 and exam-horizon policy.
    """

    PROTECT_PREREQUISITE_OVER_EXTENSION = "protect_prerequisite_over_extension"
    PROTECT_MISCONCEPTION_OVER_PRACTICE = "protect_misconception_over_practice"
    PROTECT_UNDERSTANDING_OVER_SPEED = "protect_understanding_over_speed"
    PROTECT_DURABLE_LEARNING_OVER_THEATRE = "protect_durable_learning_over_theatre"
    EXAM_MUST_NOT_SKIP_CONCEPTUAL_REPAIR = "exam_must_not_skip_conceptual_repair"
    FORBID_ENGAGEMENT_ORDERING = "forbid_engagement_ordering"
    CAP_URGENCY = "cap_urgency"
    CAP_SCORE = "cap_score"
    REQUIRE_FACTOR = "require_factor"
    FORBID_FACTOR = "forbid_factor"


class PriorityRevisionKind(StrEnum):
    """Lawful forms of priority revision."""

    RECALCULATED = "recalculated"
    PROMOTED = "promoted"
    DEMOTED = "demoted"
    STABILISED = "stabilised"
    FACTORS_REPLACED = "factors_replaced"
