"""Advisory Outcome Measurement contracts (P3-MS002).

Immutable DTOs for measuring the behavioural impact of Controlled Advisory
Activation during rollout.

Measurement answers: **"What operational outcomes followed advisory
activation decisions?"**
Runtime A answers: **"What should the student do next?"** (unchanged).

All artefacts are operational / observation-only. No personal identifiers.
No educational scoring. No recommendation ranking. No Runtime A mutation.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

OUTCOME_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_ADVISORY_OUTCOME = "advisory_outcome_measurement"
AUTHORITY_CONTROLLED_ADVISORY = "controlled_advisory"
AUTHORITY_RUNTIME_A = "runtime_a"

OUTCOME_MEASUREMENT_VERSION = "p3.ms002.1"

# Activation statuses — operational only (no educational interpretation).
ACTIVATION_STATUS_ACTIVATED = "activated"
ACTIVATION_STATUS_REJECTED = "rejected"
ACTIVATION_STATUS_FAILED = "failed"
ACTIVATION_STATUS_ROLLED_BACK = "rolled_back"

ACTIVATION_STATUSES = frozenset(
    {
        ACTIVATION_STATUS_ACTIVATED,
        ACTIVATION_STATUS_REJECTED,
        ACTIVATION_STATUS_FAILED,
        ACTIVATION_STATUS_ROLLED_BACK,
    }
)

# Observed student actions — behavioural observation only (no mastery scores).
ACTION_NOT_OBSERVED = "not_observed"
ACTION_VIEWED = "viewed"
ACTION_ACCEPTED = "accepted"
ACTION_INTERACTED = "interacted"
ACTION_IGNORED = "ignored"
ACTION_DISMISSED = "dismissed"

STUDENT_ACTIONS = frozenset(
    {
        ACTION_NOT_OBSERVED,
        ACTION_VIEWED,
        ACTION_ACCEPTED,
        ACTION_INTERACTED,
        ACTION_IGNORED,
        ACTION_DISMISSED,
    }
)

# Engagement actions counted toward recommendation interaction rate.
INTERACTION_ACTIONS = frozenset(
    {
        ACTION_VIEWED,
        ACTION_ACCEPTED,
        ACTION_INTERACTED,
    }
)

# Rollout cohort labels (explainability).
COHORT_IN_ROLLOUT = "in_rollout"
COHORT_EXCLUDED = "excluded"
COHORT_UNKNOWN = "unknown"

ROLLOUT_COHORTS = frozenset(
    {
        COHORT_IN_ROLLOUT,
        COHORT_EXCLUDED,
        COHORT_UNKNOWN,
    }
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    frozen: dict[str, Any] = {}
    for key, item in dict(value).items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


def _canonical(value: Any) -> Any:
    """Recursively convert values into JSON-stable plain data."""
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {
            str(k): _canonical(v)
            for k, v in sorted(value.items(), key=lambda i: str(i[0]))
        }
    if isinstance(value, list | tuple):
        return [_canonical(item) for item in value]
    if hasattr(value, "to_canonical_dict"):
        return value.to_canonical_dict()
    raise TypeError(
        f"Unsupported advisory outcome contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def snapshot_mapping(value: Any | None) -> Mapping[str, Any] | None:
    """Freeze a DTO or mapping into a canonical snapshot."""
    if value is None:
        return None
    if hasattr(value, "to_canonical_dict"):
        return _freeze_mapping(value.to_canonical_dict())
    if isinstance(value, Mapping):
        return _freeze_mapping(value)
    raise TypeError("value must be a Mapping, DTO with to_canonical_dict, or None")


@dataclass(frozen=True)
class AdvisoryOutcome:
    """Immutable advisory rollout outcome observation (P3-MS002).

    Operational measurement artefact only. No personal identifiers. No
    educational scoring. Does not interpret learning quality.
    """

    outcome_id: str = ""
    policy_version: str = ""
    advisory_field: str = ""
    activation_status: str = ACTIVATION_STATUS_REJECTED
    recommendation_id: str = ""
    student_action_observed: str = ACTION_NOT_OBSERVED
    observation_window: str = ""
    generated_at: str | None = None
    rollout_cohort: str = COHORT_UNKNOWN
    activation_decision: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_OUTCOME
    measurement_version: str = OUTCOME_MEASUREMENT_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "outcome_id", (self.outcome_id or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        object.__setattr__(
            self, "recommendation_id", (self.recommendation_id or "").strip()
        )
        object.__setattr__(
            self, "observation_window", (self.observation_window or "").strip()
        )
        object.__setattr__(
            self, "activation_decision", (self.activation_decision or "").strip()
        )

        status = (self.activation_status or ACTIVATION_STATUS_REJECTED).strip()
        if status not in ACTIVATION_STATUSES:
            status = ACTIVATION_STATUS_FAILED
        object.__setattr__(self, "activation_status", status)

        action = (self.student_action_observed or ACTION_NOT_OBSERVED).strip()
        if action not in STUDENT_ACTIONS:
            action = ACTION_NOT_OBSERVED
        object.__setattr__(self, "student_action_observed", action)

        cohort = (self.rollout_cohort or COHORT_UNKNOWN).strip()
        if cohort not in ROLLOUT_COHORTS:
            cohort = COHORT_UNKNOWN
        object.__setattr__(self, "rollout_cohort", cohort)

        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_OUTCOME).strip(),
        )
        object.__setattr__(
            self,
            "measurement_version",
            (self.measurement_version or OUTCOME_MEASUREMENT_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_decision": self.activation_decision,
            "activation_status": self.activation_status,
            "advisory_field": self.advisory_field,
            "authority": self.authority,
            "generated_at": self.generated_at,
            "measurement_version": self.measurement_version,
            "observation_window": self.observation_window,
            "operational_only": self.operational_only,
            "outcome_id": self.outcome_id,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "recommendation_id": self.recommendation_id,
            "rollout_cohort": self.rollout_cohort,
            "student_action_observed": self.student_action_observed,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ActivationStatistics:
    """Immutable activation count aggregates (P3-MS002).

    Reports observations only — never interprets educational success.
    """

    total_outcomes: int = 0
    activated_count: int = 0
    rejected_count: int = 0
    failed_count: int = 0
    rolled_back_count: int = 0
    by_advisory_field: Mapping[str, int] = field(default_factory=dict)
    by_policy_version: Mapping[str, int] = field(default_factory=dict)
    by_rollout_cohort: Mapping[str, int] = field(default_factory=dict)
    by_activation_status: Mapping[str, int] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_OUTCOME
    measurement_version: str = OUTCOME_MEASUREMENT_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "total_outcomes", max(0, int(self.total_outcomes or 0))
        )
        object.__setattr__(
            self, "activated_count", max(0, int(self.activated_count or 0))
        )
        object.__setattr__(
            self, "rejected_count", max(0, int(self.rejected_count or 0))
        )
        object.__setattr__(self, "failed_count", max(0, int(self.failed_count or 0)))
        object.__setattr__(
            self, "rolled_back_count", max(0, int(self.rolled_back_count or 0))
        )

        def _int_map(value: Mapping[str, Any] | None) -> Mapping[str, int]:
            return _freeze_mapping(
                {str(k): int(v) for k, v in dict(value or {}).items()}
            )

        object.__setattr__(
            self, "by_advisory_field", _int_map(self.by_advisory_field)
        )
        object.__setattr__(
            self, "by_policy_version", _int_map(self.by_policy_version)
        )
        object.__setattr__(
            self, "by_rollout_cohort", _int_map(self.by_rollout_cohort)
        )
        object.__setattr__(
            self, "by_activation_status", _int_map(self.by_activation_status)
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_OUTCOME).strip(),
        )
        object.__setattr__(
            self,
            "measurement_version",
            (self.measurement_version or OUTCOME_MEASUREMENT_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activated_count": self.activated_count,
            "authority": self.authority,
            "by_activation_status": dict(self.by_activation_status),
            "by_advisory_field": dict(self.by_advisory_field),
            "by_policy_version": dict(self.by_policy_version),
            "by_rollout_cohort": dict(self.by_rollout_cohort),
            "failed_count": self.failed_count,
            "generated_at": self.generated_at,
            "measurement_version": self.measurement_version,
            "operational_only": self.operational_only,
            "rejected_count": self.rejected_count,
            "rolled_back_count": self.rolled_back_count,
            "total_outcomes": self.total_outcomes,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ActionCorrelation:
    """Immutable correlation of observed actions with activation (P3-MS002).

    Operational co-occurrence only — does not claim causal educational impact.
    """

    activated_action_counts: Mapping[str, int] = field(default_factory=dict)
    rejected_action_counts: Mapping[str, int] = field(default_factory=dict)
    failed_action_counts: Mapping[str, int] = field(default_factory=dict)
    rolled_back_action_counts: Mapping[str, int] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_OUTCOME
    measurement_version: str = OUTCOME_MEASUREMENT_VERSION

    def __post_init__(self) -> None:
        def _int_map(value: Mapping[str, Any] | None) -> Mapping[str, int]:
            return _freeze_mapping(
                {str(k): int(v) for k, v in dict(value or {}).items()}
            )

        object.__setattr__(
            self, "activated_action_counts", _int_map(self.activated_action_counts)
        )
        object.__setattr__(
            self, "rejected_action_counts", _int_map(self.rejected_action_counts)
        )
        object.__setattr__(
            self, "failed_action_counts", _int_map(self.failed_action_counts)
        )
        object.__setattr__(
            self,
            "rolled_back_action_counts",
            _int_map(self.rolled_back_action_counts),
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_OUTCOME).strip(),
        )
        object.__setattr__(
            self,
            "measurement_version",
            (self.measurement_version or OUTCOME_MEASUREMENT_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activated_action_counts": dict(self.activated_action_counts),
            "authority": self.authority,
            "failed_action_counts": dict(self.failed_action_counts),
            "generated_at": self.generated_at,
            "measurement_version": self.measurement_version,
            "operational_only": self.operational_only,
            "rejected_action_counts": dict(self.rejected_action_counts),
            "rolled_back_action_counts": dict(self.rolled_back_action_counts),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RolloutMetrics:
    """Immutable operational rollout metrics (P3-MS002).

    Rates are floats in ``[0.0, 1.0]``. Empty cohorts yield ``0.0`` rates.
    Does not infer learning quality.
    """

    outcome_count: int = 0
    activation_rate: float = 0.0
    acceptance_rate: float = 0.0
    recommendation_interaction_rate: float = 0.0
    rollback_count: int = 0
    activation_failures: int = 0
    rejection_count: int = 0
    activation_status_counts: Mapping[str, int] = field(default_factory=dict)
    action_counts: Mapping[str, int] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_OUTCOME
    measurement_version: str = OUTCOME_MEASUREMENT_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "outcome_count", max(0, int(self.outcome_count or 0))
        )
        object.__setattr__(
            self, "rollback_count", max(0, int(self.rollback_count or 0))
        )
        object.__setattr__(
            self, "activation_failures", max(0, int(self.activation_failures or 0))
        )
        object.__setattr__(
            self, "rejection_count", max(0, int(self.rejection_count or 0))
        )

        def _clamp_rate(value: float) -> float:
            try:
                number = float(value)
            except (TypeError, ValueError):
                return 0.0
            if number < 0.0:
                return 0.0
            if number > 1.0:
                return 1.0
            return number

        object.__setattr__(self, "activation_rate", _clamp_rate(self.activation_rate))
        object.__setattr__(self, "acceptance_rate", _clamp_rate(self.acceptance_rate))
        object.__setattr__(
            self,
            "recommendation_interaction_rate",
            _clamp_rate(self.recommendation_interaction_rate),
        )
        object.__setattr__(
            self,
            "activation_status_counts",
            _freeze_mapping(
                {
                    str(k): int(v)
                    for k, v in dict(self.activation_status_counts or {}).items()
                }
            ),
        )
        object.__setattr__(
            self,
            "action_counts",
            _freeze_mapping(
                {str(k): int(v) for k, v in dict(self.action_counts or {}).items()}
            ),
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_OUTCOME).strip(),
        )
        object.__setattr__(
            self,
            "measurement_version",
            (self.measurement_version or OUTCOME_MEASUREMENT_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "acceptance_rate": self.acceptance_rate,
            "action_counts": dict(self.action_counts),
            "activation_failures": self.activation_failures,
            "activation_rate": self.activation_rate,
            "activation_status_counts": dict(self.activation_status_counts),
            "authority": self.authority,
            "generated_at": self.generated_at,
            "measurement_version": self.measurement_version,
            "operational_only": self.operational_only,
            "outcome_count": self.outcome_count,
            "recommendation_interaction_rate": self.recommendation_interaction_rate,
            "rejection_count": self.rejection_count,
            "rollback_count": self.rollback_count,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class OutcomeMeasurementSummary:
    """Immutable outcome measurement summary for ops review (P3-MS002)."""

    summary_id: str = ""
    metrics: RolloutMetrics | None = None
    activation_statistics: ActivationStatistics | None = None
    action_correlation: ActionCorrelation | None = None
    outcomes: tuple[AdvisoryOutcome, ...] = ()
    notes: tuple[str, ...] = ()
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_OUTCOME
    measurement_version: str = OUTCOME_MEASUREMENT_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary_id", (self.summary_id or "").strip())
        if self.metrics is not None and not isinstance(self.metrics, RolloutMetrics):
            raise TypeError("metrics must be RolloutMetrics or None")
        if self.activation_statistics is not None and not isinstance(
            self.activation_statistics, ActivationStatistics
        ):
            raise TypeError(
                "activation_statistics must be ActivationStatistics or None"
            )
        if self.action_correlation is not None and not isinstance(
            self.action_correlation, ActionCorrelation
        ):
            raise TypeError("action_correlation must be ActionCorrelation or None")
        object.__setattr__(self, "outcomes", tuple(self.outcomes or ()))
        for item in self.outcomes:
            if not isinstance(item, AdvisoryOutcome):
                raise TypeError("outcomes must contain AdvisoryOutcome values")
        object.__setattr__(
            self, "notes", tuple(str(item) for item in (self.notes or ()))
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_OUTCOME).strip(),
        )
        object.__setattr__(
            self,
            "measurement_version",
            (self.measurement_version or OUTCOME_MEASUREMENT_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "action_correlation": (
                None
                if self.action_correlation is None
                else self.action_correlation.to_canonical_dict()
            ),
            "activation_statistics": (
                None
                if self.activation_statistics is None
                else self.activation_statistics.to_canonical_dict()
            ),
            "authority": self.authority,
            "generated_at": self.generated_at,
            "measurement_version": self.measurement_version,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "notes": list(self.notes),
            "operational_only": self.operational_only,
            "outcomes": [item.to_canonical_dict() for item in self.outcomes],
            "summary_id": self.summary_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdvisoryOutcomeResult:
    """Result envelope for AdvisoryOutcomeMeasurementService calls."""

    ok: bool
    outcome: AdvisoryOutcome | None = None
    metrics: RolloutMetrics | None = None
    activation_statistics: ActivationStatistics | None = None
    action_correlation: ActionCorrelation | None = None
    summary: OutcomeMeasurementSummary | None = None
    error_code: str | None = None
    message: str | None = None

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "action_correlation": (
                None
                if self.action_correlation is None
                else self.action_correlation.to_canonical_dict()
            ),
            "activation_statistics": (
                None
                if self.activation_statistics is None
                else self.activation_statistics.to_canonical_dict()
            ),
            "error_code": self.error_code,
            "message": self.message,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "ok": self.ok,
            "outcome": (
                None if self.outcome is None else self.outcome.to_canonical_dict()
            ),
            "summary": (
                None if self.summary is None else self.summary.to_canonical_dict()
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def explainability_fields_present(outcome: AdvisoryOutcome) -> bool:
    """Return True when required explainability fields are populated."""
    if not isinstance(outcome, AdvisoryOutcome):
        return False
    return bool(
        outcome.policy_version
        and outcome.advisory_field
        and outcome.rollout_cohort
        and outcome.activation_decision
        and outcome.provenance
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
    "INTERACTION_ACTIONS",
    "INVALID_STATE",
    "OUTCOME_ERROR_CODES",
    "OUTCOME_MEASUREMENT_VERSION",
    "ROLLOUT_COHORTS",
    "STUDENT_ACTIONS",
    "UNAVAILABLE",
    "ActionCorrelation",
    "ActivationStatistics",
    "AdvisoryOutcome",
    "AdvisoryOutcomeResult",
    "OutcomeMeasurementSummary",
    "RolloutMetrics",
    "explainability_fields_present",
    "serialize_canonical",
    "snapshot_mapping",
]
