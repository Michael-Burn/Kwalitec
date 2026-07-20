"""Educational Decision domain enumerations.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Decision Status / Outcome / Readiness / Indicator / Constraint / Revision
"""

from __future__ import annotations

from enum import StrEnum


class DecisionStatus(StrEnum):
    """Lifecycle status of an EducationalDecision aggregate.

    Decision evaluates readiness for executing a planned intervention. It
    does not create strategies, diagnose deficiencies, or orchestrate
    sessions. PENDING holds an evaluated posture; APPROVED / DELAYED /
    REJECTED commit an outcome; RECONSIDERED reopens commitment.
    """

    PENDING = "pending"
    APPROVED = "approved"
    DELAYED = "delayed"
    REJECTED = "rejected"
    RECONSIDERED = "reconsidered"


class DecisionOutcome(StrEnum):
    """Educational execution outcomes of an EducationalDecision.

    Outcomes answer whether the planned intervention may proceed now, or
    what must happen first. They are not teaching strategies and not
    diagnoses.
    """

    TEACH_NOW = "teach_now"
    DELAY = "delay"
    REQUIRE_REMEDIATION = "require_remediation"
    REQUIRE_PREREQUISITE_WORK = "require_prerequisite_work"
    REQUIRE_ADDITIONAL_EVIDENCE = "require_additional_evidence"


class ReadinessBand(StrEnum):
    """Qualitative readiness of a planned intervention for execution.

    Readiness describes fitness to proceed now. It is not mastery, twin
    certainty, priority ranking, or strategy selection.
    """

    NOT_READY = "not_ready"
    PARTIALLY_READY = "partially_ready"
    READY = "ready"
    BLOCKED = "blocked"


class ReadinessIndicatorKind(StrEnum):
    """Kinds of readiness signals that warrant an execution decision.

    Indicators describe execution fitness — never diagnosis categories or
    teaching-strategy selection.
    """

    PREREQUISITE_SATISFIED = "prerequisite_satisfied"
    PREREQUISITE_MISSING = "prerequisite_missing"
    EVIDENCE_SUFFICIENT = "evidence_sufficient"
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"
    CAPACITY_ADEQUATE = "capacity_adequate"
    CAPACITY_INSUFFICIENT = "capacity_insufficient"
    INTENTION_ALIGNED = "intention_aligned"
    STRATEGY_APPLICABLE = "strategy_applicable"
    REMEDIATION_REQUIRED = "remediation_required"
    AFFECTIVE_BLOCK = "affective_block"
    SESSION_CONSTRAINT = "session_constraint"
    CONFLICTING_SIGNAL = "conflicting_signal"


class ExecutionConstraintKind(StrEnum):
    """Educational constraints that execution decisions must not contradict.

    Derived from Decision Points discipline (teach only when ready; protect
    prerequisites; require evidence; lawful deferral and remediation).
    """

    FORBID_TEACH_WITHOUT_PREREQUISITE = "forbid_teach_without_prerequisite"
    FORBID_TEACH_WITHOUT_EVIDENCE = "forbid_teach_without_evidence"
    REQUIRE_REMEDIATION_FIRST = "require_remediation_first"
    REQUIRE_MINIMUM_READINESS = "require_minimum_readiness"
    REQUIRE_MINIMUM_CONFIDENCE = "require_minimum_confidence"
    FORBID_APPROVAL_WHEN_BLOCKED = "forbid_approval_when_blocked"
    PROTECT_CAPACITY = "protect_capacity"
    REQUIRE_INDICATOR = "require_indicator"
    FORBID_INDICATOR = "forbid_indicator"
    FORBID_OUTCOME = "forbid_outcome"


class DecisionRevisionKind(StrEnum):
    """Lawful forms of educational-decision revision."""

    APPROVED = "approved"
    DELAYED = "delayed"
    REJECTED = "rejected"
    RECONSIDERED = "reconsidered"
    READINESS_AMENDED = "readiness_amended"
    CONSTRAINTS_REPLACED = "constraints_replaced"
    INDICATORS_REPLACED = "indicators_replaced"
    CONFIDENCE_AMENDED = "confidence_amended"
    GENERAL = "general"
