"""Study Recovery Planner package (P2-MS010).

Architectural Recovery Planning capability for Runtime A. Feature flag
``KWALITEC_RECOVERY_PLANNER`` / ``ENABLE_RECOVERY_PLANNER`` defaults OFF.

No recovery algorithms, schedule optimisation, recommendation changes,
Runtime A behavioural changes, Adaptive / Strategy / Twin mutation, or
Evidence scoring.
"""

from __future__ import annotations

from .adapter import (
    ADAPTER_ID,
    PLACEHOLDER_RATIONALE,
    PORT_ID,
    SOURCE_SERVICE,
    StudyRecoveryPlannerAdapter,
    build_study_recovery_planner_adapter,
    deterministic_candidate_id,
    deterministic_recovery_id,
)
from .contracts import (
    AUTHORITY_RECOVERY_PLANNER,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    AVAILABILITY_VALUES,
    FORBIDDEN,
    INVALID_STATE,
    NOT_FOUND,
    RECOVERY_ERROR_CODES,
    RECOVERY_VERSION,
    STRATEGY_STRUCTURAL_PLACEHOLDER,
    STRATEGY_TYPES,
    UNAVAILABLE,
    DisruptionSummary,
    MissedSessionFact,
    RecoveryContext,
    RecoveryPlanCandidate,
    RecoveryPlannerPort,
    RecoveryResult,
    StudyCapacityFact,
    serialize_canonical,
)

__all__ = [
    "ADAPTER_ID",
    "AUTHORITY_RECOVERY_PLANNER",
    "AUTHORITY_RUNTIME_A",
    "AVAILABILITY_AVAILABLE",
    "AVAILABILITY_UNAVAILABLE",
    "AVAILABILITY_VALUES",
    "DisruptionSummary",
    "FORBIDDEN",
    "INVALID_STATE",
    "MissedSessionFact",
    "NOT_FOUND",
    "PLACEHOLDER_RATIONALE",
    "PORT_ID",
    "RECOVERY_ERROR_CODES",
    "RECOVERY_VERSION",
    "RecoveryContext",
    "RecoveryPlanCandidate",
    "RecoveryPlannerPort",
    "RecoveryResult",
    "SOURCE_SERVICE",
    "STRATEGY_STRUCTURAL_PLACEHOLDER",
    "STRATEGY_TYPES",
    "StudyCapacityFact",
    "StudyRecoveryPlannerAdapter",
    "UNAVAILABLE",
    "build_study_recovery_planner_adapter",
    "deterministic_candidate_id",
    "deterministic_recovery_id",
    "serialize_canonical",
]
