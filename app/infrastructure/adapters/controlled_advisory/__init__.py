"""Controlled Advisory Activation package (P3-MS001).

Permits Runtime A to consume exactly one approved Evidence Advisory field
under policy, feature-flag, freshness, and rollout governance.

Feature flag ``KWALITEC_CONTROLLED_ADVISORY`` /
``ENABLE_CONTROLLED_ADVISORY`` defaults OFF.

Influence is intentionally minimal (rationale annotation only), fully
explainable, and immediately reversible by disabling the flag.
"""

from __future__ import annotations

from .activation import (
    ACTIVATION_KEY,
    SERVICE_ID,
    SOURCE_SERVICE,
    ControlledAdvisoryActivation,
    build_controlled_advisory_activation,
    explainability_from_decision,
    resolve_controlled_advisory_policy,
)
from .contracts import (
    ACTIVATION_ERROR_CODES,
    APPROVED_ADVISORY_FIELD_CONSISTENCY,
    APPROVED_ADVISORY_FIELDS,
    AUTHORITY_CONTROLLED_ADVISORY,
    AUTHORITY_EVIDENCE_PLATFORM,
    AUTHORITY_RUNTIME_A,
    CONTROLLED_ADVISORY_VERSION,
    DEFAULT_APPROVED_FIELD,
    DEFAULT_MAX_AGE_HOURS,
    DEFAULT_POLICY_ID,
    DEFAULT_POLICY_VERSION,
    DEFAULT_ROLLOUT_PERCENTAGE,
    DEFAULT_ROLLOUT_SALT,
    INVALID_STATE,
    REASON_ACTIVATION_CONDITIONS,
    REASON_ADVISORY_FIELD_MISSING,
    REASON_ADVISORY_INVALID,
    REASON_ADVISORY_MISSING,
    REASON_ADVISORY_STALE,
    REASON_ALLOWED,
    REASON_EFFECTIVE_FROM_FUTURE,
    REASON_FIELD_NOT_APPROVED,
    REASON_FLAG_OFF,
    REASON_MULTIPLE_FIELDS,
    REASON_POLICY_INVALID,
    REASON_ROLLOUT_EXCLUDED,
    UNAVAILABLE,
    AdvisoryActivationDecision,
    AdvisoryPolicy,
    ControlledAdvisoryExplainability,
    build_default_advisory_policy,
    serialize_canonical,
    snapshot_explainability_list,
    validate_advisory_policy,
)
from .policy_evaluator import (
    EVALUATOR_ID,
    EVALUATOR_VERSION,
    ControlledAdvisoryPolicyEvaluator,
    build_controlled_advisory_policy_evaluator,
    student_in_rollout,
)

__all__ = [
    "ACTIVATION_ERROR_CODES",
    "ACTIVATION_KEY",
    "APPROVED_ADVISORY_FIELD_CONSISTENCY",
    "APPROVED_ADVISORY_FIELDS",
    "AUTHORITY_CONTROLLED_ADVISORY",
    "AUTHORITY_EVIDENCE_PLATFORM",
    "AUTHORITY_RUNTIME_A",
    "CONTROLLED_ADVISORY_VERSION",
    "DEFAULT_APPROVED_FIELD",
    "DEFAULT_MAX_AGE_HOURS",
    "DEFAULT_POLICY_ID",
    "DEFAULT_POLICY_VERSION",
    "DEFAULT_ROLLOUT_PERCENTAGE",
    "DEFAULT_ROLLOUT_SALT",
    "EVALUATOR_ID",
    "EVALUATOR_VERSION",
    "INVALID_STATE",
    "REASON_ACTIVATION_CONDITIONS",
    "REASON_ADVISORY_FIELD_MISSING",
    "REASON_ADVISORY_INVALID",
    "REASON_ADVISORY_MISSING",
    "REASON_ADVISORY_STALE",
    "REASON_ALLOWED",
    "REASON_EFFECTIVE_FROM_FUTURE",
    "REASON_FIELD_NOT_APPROVED",
    "REASON_FLAG_OFF",
    "REASON_MULTIPLE_FIELDS",
    "REASON_POLICY_INVALID",
    "REASON_ROLLOUT_EXCLUDED",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "UNAVAILABLE",
    "AdvisoryActivationDecision",
    "AdvisoryPolicy",
    "ControlledAdvisoryActivation",
    "ControlledAdvisoryExplainability",
    "ControlledAdvisoryPolicyEvaluator",
    "build_controlled_advisory_activation",
    "build_controlled_advisory_policy_evaluator",
    "build_default_advisory_policy",
    "explainability_from_decision",
    "resolve_controlled_advisory_policy",
    "serialize_canonical",
    "snapshot_explainability_list",
    "student_in_rollout",
    "validate_advisory_policy",
]
