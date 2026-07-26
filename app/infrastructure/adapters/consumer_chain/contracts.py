"""EP-002.1 consumer-chain observability contracts.

Operational outcome categories for Twin-gated ``build_*`` APIs.
Does not encode educational judgements.
"""

from __future__ import annotations

# Outcome categories (binding for telemetry payloads).
OUTCOME_SUCCESS = "success"
OUTCOME_UNAVAILABLE = "unavailable"
OUTCOME_LIMITATION = "limitation"
OUTCOME_EXCEPTION = "exception"

OUTCOME_CATEGORIES: tuple[str, ...] = (
    OUTCOME_SUCCESS,
    OUTCOME_UNAVAILABLE,
    OUTCOME_LIMITATION,
    OUTCOME_EXCEPTION,
)

# Host service / API names (stable identifiers for ops).
SERVICE_PLANNING = "PlanningService"
SERVICE_READINESS = "ReadinessService"
SERVICE_RECOMMENDATION = "RecommendationService"

API_BUILD_DAILY_STUDY_PLAN = "build_daily_study_plan"
API_BUILD_READINESS_INTELLIGENCE = "build_readiness_intelligence"
API_BUILD_STUDY_INSIGHTS = "build_study_insights"

CONSUMER_CHAIN_APIS: tuple[str, ...] = (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
)

LOG_CONSUMER_CHAIN_INVOKED = "consumer_chain.invoked"
LOG_CONSUMER_CHAIN_COMPLETED = "consumer_chain.completed"
LOG_CONSUMER_CHAIN_FAILED = "consumer_chain.failed"
LOG_CONSUMER_CHAIN_DUAL_RUN = "consumer_chain.dual_run"
LOG_CONSUMER_CHAIN_CUTOVER = "consumer_chain.cutover"
LOG_FOUNDATION_ASSEMBLE = "consumer_chain.foundation_assemble"
