"""Advisory Outcome Measurement package (P3-MS002).

Measures the behavioural impact of Controlled Advisory Activation during
rollout. Feature flag ``KWALITEC_ADVISORY_OUTCOME_MEASUREMENT`` /
``ENABLE_ADVISORY_OUTCOME_MEASUREMENT`` defaults OFF.

Reports operational observations only. Never modifies Runtime A behaviour.
Never interprets educational success. No Adaptive / Strategy / Recovery /
automatic optimisation.
"""

from __future__ import annotations

from .contracts import (
    ACTION_ACCEPTED,
    ACTION_DISMISSED,
    ACTION_IGNORED,
    ACTION_INTERACTED,
    ACTION_NOT_OBSERVED,
    ACTION_VIEWED,
    ACTIVATION_STATUS_ACTIVATED,
    ACTIVATION_STATUS_FAILED,
    ACTIVATION_STATUS_REJECTED,
    ACTIVATION_STATUS_ROLLED_BACK,
    ACTIVATION_STATUSES,
    AUTHORITY_ADVISORY_OUTCOME,
    AUTHORITY_CONTROLLED_ADVISORY,
    AUTHORITY_RUNTIME_A,
    COHORT_EXCLUDED,
    COHORT_IN_ROLLOUT,
    COHORT_UNKNOWN,
    INTERACTION_ACTIONS,
    INVALID_STATE,
    OUTCOME_ERROR_CODES,
    OUTCOME_MEASUREMENT_VERSION,
    ROLLOUT_COHORTS,
    STUDENT_ACTIONS,
    UNAVAILABLE,
    ActionCorrelation,
    ActivationStatistics,
    AdvisoryOutcome,
    AdvisoryOutcomeResult,
    OutcomeMeasurementSummary,
    RolloutMetrics,
    explainability_fields_present,
    serialize_canonical,
    snapshot_mapping,
)
from .service import (
    DEFAULT_OBSERVATION_WINDOW,
    SERVICE_ID,
    SOURCE_SERVICE,
    AdvisoryOutcomeMeasurementService,
    build_advisory_outcome_measurement_service,
    deterministic_outcome_id,
    deterministic_summary_id,
    resolve_activation_status,
    resolve_rollout_cohort,
)

__all__ = [
    "ACTION_ACCEPTED",
    "ACTION_DISMISSED",
    "ACTION_IGNORED",
    "ACTION_INTERACTED",
    "ACTION_NOT_OBSERVED",
    "ACTION_VIEWED",
    "ACTIVATION_STATUSES",
    "ACTIVATION_STATUS_ACTIVATED",
    "ACTIVATION_STATUS_FAILED",
    "ACTIVATION_STATUS_REJECTED",
    "ACTIVATION_STATUS_ROLLED_BACK",
    "AUTHORITY_ADVISORY_OUTCOME",
    "AUTHORITY_CONTROLLED_ADVISORY",
    "AUTHORITY_RUNTIME_A",
    "COHORT_EXCLUDED",
    "COHORT_IN_ROLLOUT",
    "COHORT_UNKNOWN",
    "DEFAULT_OBSERVATION_WINDOW",
    "INTERACTION_ACTIONS",
    "INVALID_STATE",
    "OUTCOME_ERROR_CODES",
    "OUTCOME_MEASUREMENT_VERSION",
    "ROLLOUT_COHORTS",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "STUDENT_ACTIONS",
    "UNAVAILABLE",
    "ActionCorrelation",
    "ActivationStatistics",
    "AdvisoryOutcome",
    "AdvisoryOutcomeMeasurementService",
    "AdvisoryOutcomeResult",
    "OutcomeMeasurementSummary",
    "RolloutMetrics",
    "build_advisory_outcome_measurement_service",
    "deterministic_outcome_id",
    "deterministic_summary_id",
    "explainability_fields_present",
    "resolve_activation_status",
    "resolve_rollout_cohort",
    "serialize_canonical",
    "snapshot_mapping",
]
