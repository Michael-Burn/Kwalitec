"""Advisory Decision Simulation package (P2-MS011).

Parallel simulation path for comparing production Runtime A recommendations
against advisory-informed structural simulations. Feature flag
``KWALITEC_DECISION_SIMULATION`` / ``ENABLE_DECISION_SIMULATION`` defaults OFF.

Never modifies production recommendations. Never writes educational state.
No Adaptive / Strategy / Recovery optimisation / AI coaching.
"""

from __future__ import annotations

from .contracts import (
    AUTHORITY_DECISION_SIMULATION,
    AUTHORITY_RUNTIME_A,
    INVALID_STATE,
    SIMULATION_ERROR_CODES,
    SIMULATION_VERSION,
    UNAVAILABLE,
    DecisionComparisonRecord,
    DecisionDifference,
    DecisionSimulationContext,
    DecisionSimulationResult,
    SimulatedRecommendation,
    serialize_canonical,
    snapshot_mapping,
    snapshot_mapping_tuple,
)
from .service import (
    ADVISORY_SOURCE_EVIDENCE,
    ADVISORY_SOURCE_RECOVERY,
    SERVICE_ID,
    SIMULATION_MODE_STRUCTURAL,
    SOURCE_SERVICE,
    DecisionSimulationService,
    build_decision_simulation_service,
    deterministic_comparison_id,
    deterministic_simulation_id,
)

__all__ = [
    "ADVISORY_SOURCE_EVIDENCE",
    "ADVISORY_SOURCE_RECOVERY",
    "AUTHORITY_DECISION_SIMULATION",
    "AUTHORITY_RUNTIME_A",
    "DecisionComparisonRecord",
    "DecisionDifference",
    "DecisionSimulationContext",
    "DecisionSimulationResult",
    "DecisionSimulationService",
    "INVALID_STATE",
    "SERVICE_ID",
    "SIMULATION_ERROR_CODES",
    "SIMULATION_MODE_STRUCTURAL",
    "SIMULATION_VERSION",
    "SOURCE_SERVICE",
    "SimulatedRecommendation",
    "UNAVAILABLE",
    "build_decision_simulation_service",
    "deterministic_comparison_id",
    "deterministic_simulation_id",
    "serialize_canonical",
    "snapshot_mapping",
    "snapshot_mapping_tuple",
]
