"""Controlled Educational Effectiveness Trial contracts (P4-MS001).

Immutable DTOs for configuring trials that compare baseline recommendations
with policy-weighted recommendations under controlled rollout.

Trial answers: **"Did authorised policy weighting produce measurable
operational educational-effectiveness signals?"**
Runtime A answers: **"What should the student do next?"** (unchanged authority).

No additional advisory fields. No mastery / examination inference.
No autonomous policy updates. No Adaptive / Recovery / AI coaching.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

TRIAL_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_EDUCATIONAL_TRIAL = "educational_trial"
AUTHORITY_RUNTIME_A = "runtime_a"
AUTHORITY_POLICY_WEIGHTING = "policy_weighting"

EDUCATIONAL_TRIAL_VERSION = "p4.ms001.1"

# Approved advisory field — locked to P3-MS004 surface (no expansion).
APPROVED_ADVISORY_FIELD = "consistency_summary"
APPROVED_ADVISORY_FIELDS = frozenset({APPROVED_ADVISORY_FIELD})

# Trial lifecycle statuses.
TRIAL_STATUS_DRAFT = "draft"
TRIAL_STATUS_ACTIVE = "active"
TRIAL_STATUS_PAUSED = "paused"
TRIAL_STATUS_COMPLETED = "completed"
TRIAL_STATUS_CANCELLED = "cancelled"

TRIAL_STATUSES = frozenset(
    {
        TRIAL_STATUS_DRAFT,
        TRIAL_STATUS_ACTIVE,
        TRIAL_STATUS_PAUSED,
        TRIAL_STATUS_COMPLETED,
        TRIAL_STATUS_CANCELLED,
    }
)

# Deterministic cohort labels.
COHORT_BASELINE = "baseline"
COHORT_TREATMENT = "treatment"
COHORT_UNASSIGNED = "unassigned"

TRIAL_COHORTS = frozenset(
    {
        COHORT_BASELINE,
        COHORT_TREATMENT,
        COHORT_UNASSIGNED,
    }
)

# Operational success / observation metrics (no mastery inference).
METRIC_RECOMMENDATION_ACCEPTANCE = "recommendation_acceptance"
METRIC_MISSION_COMPLETION = "mission_completion"
METRIC_STUDY_SESSION_COMPLETION = "study_session_completion"
METRIC_REFLECTION_COMPLETION = "reflection_completion"
METRIC_POLICY_ACTIVATION = "policy_activation"

OPERATIONAL_SUCCESS_METRICS = frozenset(
    {
        METRIC_RECOMMENDATION_ACCEPTANCE,
        METRIC_MISSION_COMPLETION,
        METRIC_STUDY_SESSION_COMPLETION,
        METRIC_REFLECTION_COMPLETION,
        METRIC_POLICY_ACTIVATION,
    }
)

DEFAULT_SUCCESS_METRICS: tuple[str, ...] = (
    METRIC_RECOMMENDATION_ACCEPTANCE,
    METRIC_MISSION_COMPLETION,
    METRIC_STUDY_SESSION_COMPLETION,
    METRIC_REFLECTION_COMPLETION,
    METRIC_POLICY_ACTIVATION,
)

DEFAULT_ROLLOUT_SALT = "kwalitec-educational-trial-p4-ms001"
DEFAULT_TRIAL_ID = "educational-trial-p4-ms001"
DEFAULT_POLICY_VERSION = "p3.ms004.1"


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
        f"Unsupported educational trial contract value type: {type(value)!r}"
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


def _normalise_success_metrics(value: Sequence[str] | None) -> tuple[str, ...]:
    if not value:
        return DEFAULT_SUCCESS_METRICS
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in value:
        label = str(item or "").strip()
        if not label or label in seen:
            continue
        if label not in OPERATIONAL_SUCCESS_METRICS:
            continue
        seen.add(label)
        cleaned.append(label)
    return tuple(cleaned) if cleaned else DEFAULT_SUCCESS_METRICS


@dataclass(frozen=True)
class EducationalTrial:
    """Immutable educational effectiveness trial configuration (P4-MS001).

    Declares the comparison between baseline recommendations and
    policy-weighted recommendations for a controlled rollout window.
    Does not expand advisory fields or educational authority.
    """

    trial_id: str = DEFAULT_TRIAL_ID
    policy_version: str = DEFAULT_POLICY_VERSION
    rollout_percentage: int = 0
    advisory_field: str = APPROVED_ADVISORY_FIELD
    start_date: str = ""
    end_date: str = ""
    success_metrics: tuple[str, ...] = DEFAULT_SUCCESS_METRICS
    status: str = TRIAL_STATUS_DRAFT
    rollout_salt: str = DEFAULT_ROLLOUT_SALT
    provenance: Mapping[str, Any] = field(default_factory=dict)
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "trial_id", (self.trial_id or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self,
            "advisory_field",
            (self.advisory_field or APPROVED_ADVISORY_FIELD).strip(),
        )
        if self.advisory_field not in APPROVED_ADVISORY_FIELDS:
            object.__setattr__(self, "advisory_field", APPROVED_ADVISORY_FIELD)

        percentage = int(self.rollout_percentage or 0)
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        object.__setattr__(self, "rollout_percentage", percentage)

        object.__setattr__(self, "start_date", (self.start_date or "").strip())
        object.__setattr__(self, "end_date", (self.end_date or "").strip())
        object.__setattr__(
            self, "success_metrics", _normalise_success_metrics(self.success_metrics)
        )

        status = (self.status or TRIAL_STATUS_DRAFT).strip()
        if status not in TRIAL_STATUSES:
            status = TRIAL_STATUS_DRAFT
        object.__setattr__(self, "status", status)

        object.__setattr__(
            self,
            "rollout_salt",
            (self.rollout_salt or DEFAULT_ROLLOUT_SALT).strip(),
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    @property
    def is_active(self) -> bool:
        return self.status == TRIAL_STATUS_ACTIVE

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_field": self.advisory_field,
            "authority": self.authority,
            "end_date": self.end_date,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "rollout_percentage": self.rollout_percentage,
            "rollout_salt": self.rollout_salt,
            "start_date": self.start_date,
            "status": self.status,
            "success_metrics": list(self.success_metrics),
            "trial_id": self.trial_id,
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class CohortAssignment:
    """Immutable deterministic cohort assignment for a trial."""

    trial_id: str = ""
    student_key: str = ""
    cohort: str = COHORT_UNASSIGNED
    rollout_percentage: int = 0
    bucket: int = -1
    policy_version: str = ""
    authorised_for_weighting: bool = False
    assignment_mechanism: str = "stable_hash"
    generated_at: str | None = None
    provenance: Mapping[str, Any] = field(default_factory=dict)
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "trial_id", (self.trial_id or "").strip())
        object.__setattr__(self, "student_key", (self.student_key or "").strip())
        cohort = (self.cohort or COHORT_UNASSIGNED).strip()
        if cohort not in TRIAL_COHORTS:
            cohort = COHORT_UNASSIGNED
        object.__setattr__(self, "cohort", cohort)
        percentage = int(self.rollout_percentage or 0)
        object.__setattr__(
            self, "rollout_percentage", max(0, min(100, percentage))
        )
        object.__setattr__(self, "bucket", int(self.bucket))
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "authorised_for_weighting", bool(self.authorised_for_weighting)
        )
        object.__setattr__(
            self,
            "assignment_mechanism",
            (self.assignment_mechanism or "stable_hash").strip(),
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "assignment_mechanism": self.assignment_mechanism,
            "authorised_for_weighting": self.authorised_for_weighting,
            "authority": self.authority,
            "bucket": self.bucket,
            "cohort": self.cohort,
            "generated_at": self.generated_at,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "rollout_percentage": self.rollout_percentage,
            "student_key": self.student_key,
            "trial_id": self.trial_id,
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TrialMetricObservation:
    """Immutable operational trial metric observation (P4-MS001).

    No personal identifiers. No mastery / examination scores.
    """

    observation_id: str = ""
    trial_id: str = ""
    metric_name: str = ""
    cohort: str = COHORT_UNASSIGNED
    occurred: bool = False
    count: int = 1
    recommendation_id: str = ""
    observation_window: str = ""
    generated_at: str | None = None
    policy_version: str = ""
    policy_activated: bool = False
    provenance: Mapping[str, Any] = field(default_factory=dict)
    operational_only: bool = True
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "observation_id", (self.observation_id or "").strip()
        )
        object.__setattr__(self, "trial_id", (self.trial_id or "").strip())
        metric = (self.metric_name or "").strip()
        if metric not in OPERATIONAL_SUCCESS_METRICS:
            metric = ""
        object.__setattr__(self, "metric_name", metric)
        cohort = (self.cohort or COHORT_UNASSIGNED).strip()
        if cohort not in TRIAL_COHORTS:
            cohort = COHORT_UNASSIGNED
        object.__setattr__(self, "cohort", cohort)
        object.__setattr__(self, "occurred", bool(self.occurred))
        object.__setattr__(self, "count", max(0, int(self.count or 0)))
        object.__setattr__(
            self, "recommendation_id", (self.recommendation_id or "").strip()
        )
        object.__setattr__(
            self, "observation_window", (self.observation_window or "").strip()
        )
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(self, "policy_activated", bool(self.policy_activated))
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "cohort": self.cohort,
            "count": self.count,
            "generated_at": self.generated_at,
            "metric_name": self.metric_name,
            "observation_id": self.observation_id,
            "observation_window": self.observation_window,
            "occurred": self.occurred,
            "operational_only": self.operational_only,
            "policy_activated": self.policy_activated,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "recommendation_id": self.recommendation_id,
            "trial_id": self.trial_id,
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class CohortStatistics:
    """Immutable cohort membership / observation statistics."""

    baseline_count: int = 0
    treatment_count: int = 0
    unassigned_count: int = 0
    total_assignments: int = 0
    by_cohort: Mapping[str, int] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "baseline_count", max(0, int(self.baseline_count or 0))
        )
        object.__setattr__(
            self, "treatment_count", max(0, int(self.treatment_count or 0))
        )
        object.__setattr__(
            self, "unassigned_count", max(0, int(self.unassigned_count or 0))
        )
        object.__setattr__(
            self, "total_assignments", max(0, int(self.total_assignments or 0))
        )
        object.__setattr__(
            self,
            "by_cohort",
            _freeze_mapping(
                {str(k): int(v) for k, v in dict(self.by_cohort or {}).items()}
            ),
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "baseline_count": self.baseline_count,
            "by_cohort": dict(self.by_cohort),
            "generated_at": self.generated_at,
            "operational_only": self.operational_only,
            "total_assignments": self.total_assignments,
            "treatment_count": self.treatment_count,
            "trial_version": self.trial_version,
            "unassigned_count": self.unassigned_count,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ActivationStatistics:
    """Immutable policy-activation statistics for educational review."""

    total_observations: int = 0
    policy_activation_count: int = 0
    activation_by_cohort: Mapping[str, int] = field(default_factory=dict)
    metric_counts: Mapping[str, int] = field(default_factory=dict)
    metric_counts_by_cohort: Mapping[str, Mapping[str, int]] = field(
        default_factory=dict
    )
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "total_observations", max(0, int(self.total_observations or 0))
        )
        object.__setattr__(
            self,
            "policy_activation_count",
            max(0, int(self.policy_activation_count or 0)),
        )
        object.__setattr__(
            self,
            "activation_by_cohort",
            _freeze_mapping(
                {
                    str(k): int(v)
                    for k, v in dict(self.activation_by_cohort or {}).items()
                }
            ),
        )
        object.__setattr__(
            self,
            "metric_counts",
            _freeze_mapping(
                {str(k): int(v) for k, v in dict(self.metric_counts or {}).items()}
            ),
        )
        nested: dict[str, Mapping[str, int]] = {}
        for cohort, counts in dict(self.metric_counts_by_cohort or {}).items():
            nested[str(cohort)] = MappingProxyType(
                {str(k): int(v) for k, v in dict(counts or {}).items()}
            )
        object.__setattr__(
            self, "metric_counts_by_cohort", MappingProxyType(nested)
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_by_cohort": dict(self.activation_by_cohort),
            "authority": self.authority,
            "generated_at": self.generated_at,
            "metric_counts": dict(self.metric_counts),
            "metric_counts_by_cohort": {
                cohort: dict(counts)
                for cohort, counts in self.metric_counts_by_cohort.items()
            },
            "operational_only": self.operational_only,
            "policy_activation_count": self.policy_activation_count,
            "total_observations": self.total_observations,
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TrialMetrics:
    """Immutable operational trial metric rates (P4-MS001).

    Rates are floats in ``[0.0, 1.0]``. Empty cohorts yield ``0.0``.
    Does not infer mastery or examination success.
    """

    observation_count: int = 0
    recommendation_acceptance_rate: float = 0.0
    mission_completion_rate: float = 0.0
    study_session_completion_rate: float = 0.0
    reflection_completion_rate: float = 0.0
    policy_activation_frequency: float = 0.0
    rates_by_cohort: Mapping[str, Mapping[str, float]] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "observation_count", max(0, int(self.observation_count or 0))
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

        object.__setattr__(
            self,
            "recommendation_acceptance_rate",
            _clamp_rate(self.recommendation_acceptance_rate),
        )
        object.__setattr__(
            self,
            "mission_completion_rate",
            _clamp_rate(self.mission_completion_rate),
        )
        object.__setattr__(
            self,
            "study_session_completion_rate",
            _clamp_rate(self.study_session_completion_rate),
        )
        object.__setattr__(
            self,
            "reflection_completion_rate",
            _clamp_rate(self.reflection_completion_rate),
        )
        object.__setattr__(
            self,
            "policy_activation_frequency",
            _clamp_rate(self.policy_activation_frequency),
        )
        nested: dict[str, Mapping[str, float]] = {}
        for cohort, rates in dict(self.rates_by_cohort or {}).items():
            nested[str(cohort)] = MappingProxyType(
                {
                    str(k): _clamp_rate(v)
                    for k, v in dict(rates or {}).items()
                }
            )
        object.__setattr__(self, "rates_by_cohort", MappingProxyType(nested))
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "generated_at": self.generated_at,
            "mission_completion_rate": self.mission_completion_rate,
            "observation_count": self.observation_count,
            "operational_only": self.operational_only,
            "policy_activation_frequency": self.policy_activation_frequency,
            "rates_by_cohort": {
                cohort: dict(rates) for cohort, rates in self.rates_by_cohort.items()
            },
            "recommendation_acceptance_rate": self.recommendation_acceptance_rate,
            "reflection_completion_rate": self.reflection_completion_rate,
            "study_session_completion_rate": self.study_session_completion_rate,
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TrialSummary:
    """Immutable educational trial summary for review (P4-MS001)."""

    summary_id: str = ""
    trial: EducationalTrial | None = None
    cohort_statistics: CohortStatistics | None = None
    activation_statistics: ActivationStatistics | None = None
    metrics: TrialMetrics | None = None
    observations: tuple[TrialMetricObservation, ...] = ()
    observation_period_start: str = ""
    observation_period_end: str = ""
    notes: tuple[str, ...] = ()
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_EDUCATIONAL_TRIAL
    trial_version: str = EDUCATIONAL_TRIAL_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary_id", (self.summary_id or "").strip())
        if self.trial is not None and not isinstance(self.trial, EducationalTrial):
            raise TypeError("trial must be EducationalTrial or None")
        if self.cohort_statistics is not None and not isinstance(
            self.cohort_statistics, CohortStatistics
        ):
            raise TypeError("cohort_statistics must be CohortStatistics or None")
        if self.activation_statistics is not None and not isinstance(
            self.activation_statistics, ActivationStatistics
        ):
            raise TypeError(
                "activation_statistics must be ActivationStatistics or None"
            )
        if self.metrics is not None and not isinstance(self.metrics, TrialMetrics):
            raise TypeError("metrics must be TrialMetrics or None")
        object.__setattr__(self, "observations", tuple(self.observations or ()))
        for item in self.observations:
            if not isinstance(item, TrialMetricObservation):
                raise TypeError(
                    "observations must contain TrialMetricObservation values"
                )
        object.__setattr__(
            self,
            "observation_period_start",
            (self.observation_period_start or "").strip(),
        )
        object.__setattr__(
            self,
            "observation_period_end",
            (self.observation_period_end or "").strip(),
        )
        object.__setattr__(
            self, "notes", tuple(str(item) for item in (self.notes or ()))
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EDUCATIONAL_TRIAL).strip(),
        )
        object.__setattr__(
            self,
            "trial_version",
            (self.trial_version or EDUCATIONAL_TRIAL_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_statistics": (
                None
                if self.activation_statistics is None
                else self.activation_statistics.to_canonical_dict()
            ),
            "authority": self.authority,
            "cohort_statistics": (
                None
                if self.cohort_statistics is None
                else self.cohort_statistics.to_canonical_dict()
            ),
            "generated_at": self.generated_at,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "notes": list(self.notes),
            "observation_period_end": self.observation_period_end,
            "observation_period_start": self.observation_period_start,
            "observations": [item.to_canonical_dict() for item in self.observations],
            "operational_only": self.operational_only,
            "summary_id": self.summary_id,
            "trial": None if self.trial is None else self.trial.to_canonical_dict(),
            "trial_version": self.trial_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EducationalTrialResult:
    """Result envelope for EducationalTrialService calls."""

    ok: bool
    trial: EducationalTrial | None = None
    assignment: CohortAssignment | None = None
    observation: TrialMetricObservation | None = None
    cohort_statistics: CohortStatistics | None = None
    activation_statistics: ActivationStatistics | None = None
    metrics: TrialMetrics | None = None
    summary: TrialSummary | None = None
    error_code: str | None = None
    message: str | None = None

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_statistics": (
                None
                if self.activation_statistics is None
                else self.activation_statistics.to_canonical_dict()
            ),
            "assignment": (
                None
                if self.assignment is None
                else self.assignment.to_canonical_dict()
            ),
            "cohort_statistics": (
                None
                if self.cohort_statistics is None
                else self.cohort_statistics.to_canonical_dict()
            ),
            "error_code": self.error_code,
            "message": self.message,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "observation": (
                None
                if self.observation is None
                else self.observation.to_canonical_dict()
            ),
            "ok": self.ok,
            "summary": (
                None if self.summary is None else self.summary.to_canonical_dict()
            ),
            "trial": None if self.trial is None else self.trial.to_canonical_dict(),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def validate_educational_trial(trial: EducationalTrial) -> tuple[bool, str]:
    """Validate trial configuration for operational use."""
    if not isinstance(trial, EducationalTrial):
        return False, "trial_must_be_educational_trial"
    if not trial.trial_id:
        return False, "trial_id_required"
    if not trial.policy_version:
        return False, "policy_version_required"
    if trial.advisory_field not in APPROVED_ADVISORY_FIELDS:
        return False, "advisory_field_not_approved"
    if trial.rollout_percentage < 0 or trial.rollout_percentage > 100:
        return False, "rollout_percentage_out_of_range"
    if trial.status not in TRIAL_STATUSES:
        return False, "status_invalid"
    if not trial.success_metrics:
        return False, "success_metrics_required"
    return True, "ok"


__all__ = [
    "APPROVED_ADVISORY_FIELD",
    "APPROVED_ADVISORY_FIELDS",
    "AUTHORITY_EDUCATIONAL_TRIAL",
    "AUTHORITY_POLICY_WEIGHTING",
    "AUTHORITY_RUNTIME_A",
    "COHORT_BASELINE",
    "COHORT_TREATMENT",
    "COHORT_UNASSIGNED",
    "DEFAULT_POLICY_VERSION",
    "DEFAULT_ROLLOUT_SALT",
    "DEFAULT_SUCCESS_METRICS",
    "DEFAULT_TRIAL_ID",
    "EDUCATIONAL_TRIAL_VERSION",
    "INVALID_STATE",
    "METRIC_MISSION_COMPLETION",
    "METRIC_POLICY_ACTIVATION",
    "METRIC_RECOMMENDATION_ACCEPTANCE",
    "METRIC_REFLECTION_COMPLETION",
    "METRIC_STUDY_SESSION_COMPLETION",
    "OPERATIONAL_SUCCESS_METRICS",
    "TRIAL_COHORTS",
    "TRIAL_ERROR_CODES",
    "TRIAL_STATUSES",
    "TRIAL_STATUS_ACTIVE",
    "TRIAL_STATUS_CANCELLED",
    "TRIAL_STATUS_COMPLETED",
    "TRIAL_STATUS_DRAFT",
    "TRIAL_STATUS_PAUSED",
    "UNAVAILABLE",
    "ActivationStatistics",
    "CohortAssignment",
    "CohortStatistics",
    "EducationalTrial",
    "EducationalTrialResult",
    "TrialMetricObservation",
    "TrialMetrics",
    "TrialSummary",
    "serialize_canonical",
    "snapshot_mapping",
    "validate_educational_trial",
]
