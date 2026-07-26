"""Controlled Advisory Activation contracts (P3-MS001).

Immutable governance DTOs for permitting Runtime A to consume exactly one
approved Evidence Advisory field under explicit policy, feature-flag, and
freshness controls.

Activation answers: **"May Runtime A use this approved advisory field now?"**
Runtime A answers: **"What should the student do next?"** (sole authority).

The policy evaluator never produces recommendations.
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

ACTIVATION_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_CONTROLLED_ADVISORY = "controlled_advisory"
AUTHORITY_RUNTIME_A = "runtime_a"
AUTHORITY_EVIDENCE_PLATFORM = "evidence_platform"

CONTROLLED_ADVISORY_VERSION = "p3.ms001.1"

# Single approved field for P3-MS001 — additional fields require architecture review.
APPROVED_ADVISORY_FIELD_CONSISTENCY = "consistency_summary"
APPROVED_ADVISORY_FIELDS = frozenset({APPROVED_ADVISORY_FIELD_CONSISTENCY})
DEFAULT_APPROVED_FIELD = APPROVED_ADVISORY_FIELD_CONSISTENCY

DEFAULT_POLICY_ID = "controlled-advisory-p3-ms001"
DEFAULT_POLICY_VERSION = CONTROLLED_ADVISORY_VERSION
DEFAULT_MAX_AGE_HOURS = 168  # 7 days
DEFAULT_ROLLOUT_PERCENTAGE = 0
DEFAULT_ROLLOUT_SALT = "controlled-advisory-p3-ms001"

# Explicit allow / deny reasons (explainability).
REASON_ALLOWED = "policy_allows_approved_field"
REASON_FLAG_OFF = "controlled_advisory_flag_off"
REASON_POLICY_INVALID = "policy_invalid"
REASON_MULTIPLE_FIELDS = "multiple_advisory_fields_forbidden"
REASON_FIELD_NOT_APPROVED = "advisory_field_not_approved"
REASON_ROLLOUT_EXCLUDED = "rollout_percentage_excluded"
REASON_ADVISORY_MISSING = "advisory_unavailable"
REASON_ADVISORY_INVALID = "advisory_invalid"
REASON_ADVISORY_STALE = "advisory_stale"
REASON_ADVISORY_FIELD_MISSING = "approved_field_missing"
REASON_EFFECTIVE_FROM_FUTURE = "policy_not_yet_effective"
REASON_ACTIVATION_CONDITIONS = "activation_conditions_unmet"


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
        f"Unsupported controlled advisory contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class AdvisoryPolicy:
    """Immutable advisory activation policy (P3-MS001).

    Exactly one advisory field may be enabled. Additional fields require
    architecture review before policy expansion.
    """

    policy_id: str = DEFAULT_POLICY_ID
    enabled_advisory_fields: tuple[str, ...] = (DEFAULT_APPROVED_FIELD,)
    activation_conditions: Mapping[str, Any] = field(default_factory=dict)
    rollout_percentage: int = DEFAULT_ROLLOUT_PERCENTAGE
    policy_version: str = DEFAULT_POLICY_VERSION
    effective_from: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        fields = tuple(
            str(item).strip()
            for item in (self.enabled_advisory_fields or ())
            if str(item).strip()
        )
        object.__setattr__(self, "enabled_advisory_fields", fields)
        object.__setattr__(
            self, "activation_conditions", _freeze_mapping(self.activation_conditions)
        )
        try:
            percentage = int(self.rollout_percentage)
        except (TypeError, ValueError):
            percentage = DEFAULT_ROLLOUT_PERCENTAGE
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        object.__setattr__(self, "rollout_percentage", percentage)
        object.__setattr__(
            self,
            "policy_version",
            (self.policy_version or DEFAULT_POLICY_VERSION).strip(),
        )
        object.__setattr__(
            self, "effective_from", (self.effective_from or "").strip()
        )

    @property
    def enabled_field(self) -> str | None:
        """Return the single enabled field, or None when policy is empty."""
        if len(self.enabled_advisory_fields) != 1:
            return None
        return self.enabled_advisory_fields[0]

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_conditions": dict(self.activation_conditions),
            "effective_from": self.effective_from,
            "enabled_advisory_fields": list(self.enabled_advisory_fields),
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "rollout_percentage": self.rollout_percentage,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdvisoryActivationDecision:
    """Explicit allow/deny decision from the Runtime Policy Evaluator.

    Never contains recommendations. Evaluator authority only.
    """

    allowed: bool
    reason: str
    policy_id: str = ""
    policy_version: str = ""
    advisory_field: str = ""
    student_id: str = ""
    feature_flag_enabled: bool = False
    rollout_percentage: int = 0
    in_rollout: bool = False
    advisory_id: str = ""
    evidence_provenance: Mapping[str, Any] = field(default_factory=dict)
    authority: str = AUTHORITY_CONTROLLED_ADVISORY
    activation_version: str = CONTROLLED_ADVISORY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "advisory_id", (self.advisory_id or "").strip())
        object.__setattr__(
            self, "evidence_provenance", _freeze_mapping(self.evidence_provenance)
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_CONTROLLED_ADVISORY).strip(),
        )
        object.__setattr__(
            self,
            "activation_version",
            (self.activation_version or CONTROLLED_ADVISORY_VERSION).strip(),
        )
        try:
            percentage = int(self.rollout_percentage)
        except (TypeError, ValueError):
            percentage = 0
        object.__setattr__(self, "rollout_percentage", max(0, min(100, percentage)))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_version": self.activation_version,
            "advisory_field": self.advisory_field,
            "advisory_id": self.advisory_id,
            "allowed": self.allowed,
            "authority": self.authority,
            "evidence_provenance": dict(self.evidence_provenance),
            "feature_flag_enabled": self.feature_flag_enabled,
            "in_rollout": self.in_rollout,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "reason": self.reason,
            "rollout_percentage": self.rollout_percentage,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ControlledAdvisoryExplainability:
    """Explainability record for advisory influence on a recommendation.

    Attached to recommendations when controlled activation evaluates.
    """

    activated: bool
    advisory_field_used: str = ""
    policy_version: str = ""
    activation_reason: str = ""
    rejection_reason: str = ""
    evidence_provenance: Mapping[str, Any] = field(default_factory=dict)
    advisory_id: str = ""
    policy_id: str = ""
    authority: str = AUTHORITY_RUNTIME_A
    activation_version: str = CONTROLLED_ADVISORY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "advisory_field_used", (self.advisory_field_used or "").strip()
        )
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "activation_reason", (self.activation_reason or "").strip()
        )
        object.__setattr__(
            self, "rejection_reason", (self.rejection_reason or "").strip()
        )
        object.__setattr__(
            self, "evidence_provenance", _freeze_mapping(self.evidence_provenance)
        )
        object.__setattr__(self, "advisory_id", (self.advisory_id or "").strip())
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_RUNTIME_A).strip()
        )
        object.__setattr__(
            self,
            "activation_version",
            (self.activation_version or CONTROLLED_ADVISORY_VERSION).strip(),
        )
        # Binding: activated records must not carry a rejection reason and
        # rejected records must not claim a used field without reason.
        if self.activated:
            object.__setattr__(self, "rejection_reason", "")
        else:
            object.__setattr__(self, "advisory_field_used", "")
            object.__setattr__(self, "activation_reason", "")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activated": self.activated,
            "activation_reason": self.activation_reason,
            "activation_version": self.activation_version,
            "advisory_field_used": self.advisory_field_used,
            "advisory_id": self.advisory_id,
            "authority": self.authority,
            "evidence_provenance": dict(self.evidence_provenance),
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "rejection_reason": self.rejection_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def build_default_advisory_policy(
    *,
    rollout_percentage: int = DEFAULT_ROLLOUT_PERCENTAGE,
    effective_from: str | None = None,
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
    enabled_field: str = DEFAULT_APPROVED_FIELD,
    policy_id: str = DEFAULT_POLICY_ID,
    policy_version: str = DEFAULT_POLICY_VERSION,
    activation_conditions: Mapping[str, Any] | None = None,
) -> AdvisoryPolicy:
    """Construct the P3-MS001 default policy (single approved field)."""
    conditions: dict[str, Any] = {
        "max_age_hours": int(max_age_hours),
        "require_advisory_available": True,
        "require_approved_field_present": True,
        "rollout_salt": DEFAULT_ROLLOUT_SALT,
    }
    if activation_conditions:
        conditions.update(dict(activation_conditions))
    effective = (effective_from or "").strip()
    if not effective:
        effective = "1970-01-01T00:00:00+00:00"
    return AdvisoryPolicy(
        policy_id=policy_id,
        enabled_advisory_fields=(enabled_field,),
        activation_conditions=conditions,
        rollout_percentage=rollout_percentage,
        policy_version=policy_version,
        effective_from=effective,
    )


def validate_advisory_policy(policy: AdvisoryPolicy) -> str | None:
    """Return a denial reason when the policy is invalid; else None."""
    if not isinstance(policy, AdvisoryPolicy):
        return REASON_POLICY_INVALID
    if not policy.policy_id:
        return REASON_POLICY_INVALID
    if not policy.policy_version:
        return REASON_POLICY_INVALID
    if not policy.effective_from:
        return REASON_POLICY_INVALID
    if len(policy.enabled_advisory_fields) == 0:
        return REASON_POLICY_INVALID
    if len(policy.enabled_advisory_fields) > 1:
        return REASON_MULTIPLE_FIELDS
    field_name = policy.enabled_advisory_fields[0]
    if field_name not in APPROVED_ADVISORY_FIELDS:
        return REASON_FIELD_NOT_APPROVED
    return None


def snapshot_explainability_list(
    records: Sequence[ControlledAdvisoryExplainability] | None,
) -> tuple[Mapping[str, Any], ...]:
    """Freeze explainability records into canonical mappings."""
    if not records:
        return ()
    return tuple(item.to_canonical_dict() for item in records)


__all__ = [
    "ACTIVATION_ERROR_CODES",
    "APPROVED_ADVISORY_FIELDS",
    "APPROVED_ADVISORY_FIELD_CONSISTENCY",
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
    "UNAVAILABLE",
    "AdvisoryActivationDecision",
    "AdvisoryPolicy",
    "ControlledAdvisoryExplainability",
    "build_default_advisory_policy",
    "serialize_canonical",
    "snapshot_explainability_list",
    "validate_advisory_policy",
]
