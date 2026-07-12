"""Stable readiness factor identities and posture vocabulary.

Structural catalogue only — no scoring weights or composite formulas.
"""

from __future__ import annotations

from enum import StrEnum


class FactorId(StrEnum):
    """Canonical readiness factor identities (architecture §2 / plan §6)."""

    CURRICULUM_COVERAGE = "curriculum_coverage"
    KNOWLEDGE_STRENGTH = "knowledge_strength"
    MEMORY_STABILITY = "memory_stability"
    BEHAVIOUR_RELIABILITY = "behaviour_reliability"
    ASSESSMENT_PERFORMANCE = "assessment_performance"
    TIME_GOAL_PRESSURE = "time_goal_pressure"
    EVIDENCE_WARRANT = "evidence_warrant"


# Ordered catalogue — every ReadinessState must include all of these.
FACTOR_CATALOGUE: tuple[FactorId, ...] = (
    FactorId.CURRICULUM_COVERAGE,
    FactorId.KNOWLEDGE_STRENGTH,
    FactorId.MEMORY_STABILITY,
    FactorId.BEHAVIOUR_RELIABILITY,
    FactorId.ASSESSMENT_PERFORMANCE,
    FactorId.TIME_GOAL_PRESSURE,
    FactorId.EVIDENCE_WARRANT,
)


class FactorPosture(StrEnum):
    """Educational posture for one readiness factor.

    Opacity is forbidden. Mid/High cold-start fabrication is forbidden —
    use UNKNOWN or LOW_WARRANT when evidence is absent or thin.
    """

    UNKNOWN = "unknown"
    LOW_WARRANT = "low_warrant"
    RISK_ELEVATING = "risk_elevating"
    SUPPORTIVE = "supportive"
    NOT_APPLICABLE = "not_applicable"


class WarrantPosture(StrEnum):
    """Evidence Warrant denseness for a factor or overall judgement."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class OverallPosture(StrEnum):
    """Overall readiness posture for a derivation.

    Never Mid or High fabrication under cold start. Supportive overall claims
    are deferred until numeric scoring ships; structural v1 stays honest.
    """

    NOT_YET_KNOWABLE = "not_yet_knowable"
    UNKNOWN = "unknown"
    FRAGILE = "fragile"
    MIXED = "mixed"


# Critical sitting-relevant factors that constrain overall warrant assertiveness.
CRITICAL_SITTING_FACTORS: frozenset[FactorId] = frozenset(
    {
        FactorId.KNOWLEDGE_STRENGTH,
        FactorId.MEMORY_STABILITY,
        FactorId.ASSESSMENT_PERFORMANCE,
    }
)

# Twin domain attribution tags used in FactorAttribution.twin_domains.
TWIN_DOMAIN_KNOWLEDGE = "knowledge"
TWIN_DOMAIN_MEMORY = "memory"
TWIN_DOMAIN_BEHAVIOUR = "behaviour"
TWIN_DOMAIN_PERFORMANCE = "performance"
TWIN_DOMAIN_GOALS = "goals"
TWIN_DOMAIN_IDENTITY = "identity"
TWIN_DOMAIN_CURRICULUM = "curriculum"
