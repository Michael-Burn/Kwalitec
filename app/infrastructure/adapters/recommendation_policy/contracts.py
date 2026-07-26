"""Recommendation Policy Framework contracts (P3-MS003 / P3-MS004).

Immutable, versioned DTOs that declare when and how approved advisory
information may influence Runtime A recommendations.

Policy answers: **"Which advisory / weighting rules are applicable now?"**
Runtime A answers: **"What should the student do next?"** (sole authority).

P3-MS004 permits Runtime A to apply exactly one approved, bounded weighting
rule (``consistency_summary`` only) under ``ENABLE_POLICY_WEIGHTING``.
The policy engine resolves an immutable ``WeightApplication``; Runtime A
retains final recommendation authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

POLICY_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_RECOMMENDATION_POLICY = "recommendation_policy"
AUTHORITY_RUNTIME_A = "runtime_a"

RECOMMENDATION_POLICY_VERSION = "p3.ms003.1"
POLICY_WEIGHT_APPLICATION_VERSION = "p3.ms004.1"

DEFAULT_POLICY_ID = "recommendation-policy-p3-ms003"
DEFAULT_POLICY_VERSION = RECOMMENDATION_POLICY_VERSION
DEFAULT_WEIGHTING_POLICY_ID = "recommendation-policy-p3-ms004"
DEFAULT_WEIGHTING_POLICY_VERSION = POLICY_WEIGHT_APPLICATION_VERSION

# Rule kinds exposed on resolutions.
RULE_KIND_ADVISORY = "advisory"
RULE_KIND_WEIGHTING = "weighting"
RULE_KINDS = frozenset({RULE_KIND_ADVISORY, RULE_KIND_WEIGHTING})

# Advisory influence modes (declarative only — Runtime A decides application).
INFLUENCE_ANNOTATE = "annotate"
INFLUENCE_PERMIT = "permit"
INFLUENCE_MODES = frozenset({INFLUENCE_ANNOTATE, INFLUENCE_PERMIT})

# Default advisory field aligned with Controlled Advisory (P3-MS001).
# P3-MS004: only this field may influence recommendation weight.
DEFAULT_ADVISORY_FIELD = "consistency_summary"
APPROVED_WEIGHT_ADVISORY_FIELDS = frozenset({DEFAULT_ADVISORY_FIELD})
DEFAULT_ADVISORY_RULE_ID = "adv-consistency-annotate"
DEFAULT_WEIGHTING_RULE_ID = "wgt-reserved-unapplied"
DEFAULT_APPLIED_WEIGHTING_RULE_ID = "wgt-consistency-bounded"

# Bounded adjustment defaults (policy-configurable).
DEFAULT_MAX_WEIGHT_ADJUSTMENT = 0.05  # ±5%
DEFAULT_WEIGHT_BASE = 1.0
DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE = 0
DEFAULT_WEIGHT_MAX_AGE_HOURS = 168
DEFAULT_WEIGHT_ROLLOUT_SALT = "policy-weighting-p3-ms004"
DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE = 0.001
DEFAULT_STREAK_SCALE = 7  # days → full ±max_adjustment

# Explicit resolution / validation reasons (explainability).
REASON_RULES_RESOLVED = "applicable_rules_resolved"
REASON_FLAG_OFF = "recommendation_policy_flag_off"
REASON_WEIGHTING_FLAG_OFF = "policy_weighting_flag_off"
REASON_POLICY_INVALID = "policy_invalid"
REASON_POLICY_MISSING = "policy_missing"
REASON_EFFECTIVE_FROM_FUTURE = "policy_not_yet_effective"
REASON_NO_RULES_APPLICABLE = "no_rules_applicable"
REASON_ACTIVATION_CONSTRAINTS = "activation_constraints_unmet"
REASON_DUPLICATE_RULE_ID = "duplicate_rule_id"
REASON_UNKNOWN_INFLUENCE_MODE = "unknown_influence_mode"
REASON_EMPTY_RULE_ID = "empty_rule_id"
REASON_WEIGHTING_NOT_APPLIED = "weighting_rules_resolved_not_applied"
REASON_WEIGHT_APPLIED = "policy_weight_applied"
REASON_WEIGHT_DENIED = "policy_weight_denied"
REASON_WEIGHT_ROLLOUT_EXCLUDED = "weight_rollout_percentage_excluded"
REASON_WEIGHT_ADVISORY_MISSING = "weight_advisory_unavailable"
REASON_WEIGHT_ADVISORY_STALE = "weight_advisory_stale"
REASON_WEIGHT_ADVISORY_FIELD_MISSING = "weight_advisory_field_missing"
REASON_WEIGHT_FIELD_NOT_APPROVED = "weight_advisory_field_not_approved"
REASON_WEIGHT_NO_RULE = "no_approved_weighting_rule"
REASON_WEIGHT_BOUNDS_INVALID = "weight_adjustment_bounds_invalid"
REASON_WEIGHT_SIMULATION_DIVERGENCE = "weight_simulation_divergence"

# Explainability attachment keys on Runtime A recommendation dicts.
POLICY_EXPLAINABILITY_KEY = "recommendation_policy"
WEIGHT_EXPLAINABILITY_KEY = "policy_weight_application"

# Priority → base scoring weight (Runtime A authority surface).
PRIORITY_BASE_WEIGHTS: Mapping[str, float] = MappingProxyType(
    {
        "Critical": 1.00,
        "High": 0.75,
        "Medium": 0.50,
        "Low": 0.25,
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
        f"Unsupported recommendation policy contract value type: {type(value)!r}"
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
class AdvisoryRule:
    """Immutable advisory influence rule declared by policy.

    States when an advisory field may influence Runtime A. Does not itself
    generate or rank recommendations.
    """

    rule_id: str
    advisory_field: str
    influence_mode: str = INFLUENCE_ANNOTATE
    enabled: bool = True
    rationale: str = ""
    conditions: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", (self.rule_id or "").strip())
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        mode = (self.influence_mode or INFLUENCE_ANNOTATE).strip()
        object.__setattr__(self, "influence_mode", mode)
        object.__setattr__(self, "enabled", bool(self.enabled))
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "conditions", _freeze_mapping(self.conditions))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_field": self.advisory_field,
            "conditions": dict(self.conditions),
            "enabled": self.enabled,
            "influence_mode": self.influence_mode,
            "rationale": self.rationale,
            "rule_id": self.rule_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class WeightingRule:
    """Immutable weighting rule declared by policy.

    P3-MS003: resolved and exposed for explainability.
    P3-MS004: at most one enabled rule with ``apply_to_ranking=True`` and
    ``advisory_field=consistency_summary`` may produce a bounded
    ``WeightApplication`` under ``ENABLE_POLICY_WEIGHTING``.
    """

    rule_id: str
    factor: str
    weight: float = DEFAULT_WEIGHT_BASE
    enabled: bool = True
    rationale: str = ""
    conditions: Mapping[str, Any] = field(default_factory=dict)
    advisory_field: str = DEFAULT_ADVISORY_FIELD
    max_adjustment: float = DEFAULT_MAX_WEIGHT_ADJUSTMENT
    apply_to_ranking: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", (self.rule_id or "").strip())
        object.__setattr__(self, "factor", (self.factor or "").strip())
        try:
            weight = float(self.weight)
        except (TypeError, ValueError):
            weight = DEFAULT_WEIGHT_BASE
        object.__setattr__(self, "weight", weight)
        object.__setattr__(self, "enabled", bool(self.enabled))
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "conditions", _freeze_mapping(self.conditions))
        object.__setattr__(
            self,
            "advisory_field",
            (self.advisory_field or DEFAULT_ADVISORY_FIELD).strip(),
        )
        try:
            max_adj = abs(float(self.max_adjustment))
        except (TypeError, ValueError):
            max_adj = DEFAULT_MAX_WEIGHT_ADJUSTMENT
        object.__setattr__(self, "max_adjustment", max_adj)
        object.__setattr__(self, "apply_to_ranking", bool(self.apply_to_ranking))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_field": self.advisory_field,
            "apply_to_ranking": self.apply_to_ranking,
            "conditions": dict(self.conditions),
            "enabled": self.enabled,
            "factor": self.factor,
            "max_adjustment": self.max_adjustment,
            "rationale": self.rationale,
            "rule_id": self.rule_id,
            "weight": self.weight,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class WeightApplication:
    """Immutable weight adjustment resolved for Runtime A (P3-MS004).

    The policy engine returns this artefact only — Runtime A decides whether
    and how to apply it to recommendation scoring / ordering.
    """

    application_id: str
    policy_version: str
    rule_id: str
    advisory_field: str
    base_weight: float
    adjusted_weight: float
    adjustment_reason: str
    provenance: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str = ""
    applied: bool = False
    max_adjustment: float = DEFAULT_MAX_WEIGHT_ADJUSTMENT
    policy_id: str = ""
    student_id: str = ""
    authority: str = AUTHORITY_RECOMMENDATION_POLICY
    contract_version: str = POLICY_WEIGHT_APPLICATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "application_id", (self.application_id or "").strip()
        )
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(self, "rule_id", (self.rule_id or "").strip())
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        try:
            base = float(self.base_weight)
        except (TypeError, ValueError):
            base = DEFAULT_WEIGHT_BASE
        try:
            adjusted = float(self.adjusted_weight)
        except (TypeError, ValueError):
            adjusted = base
        object.__setattr__(self, "base_weight", base)
        object.__setattr__(self, "adjusted_weight", adjusted)
        object.__setattr__(
            self, "adjustment_reason", (self.adjustment_reason or "").strip()
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self, "generated_at", (self.generated_at or "").strip()
        )
        object.__setattr__(self, "applied", bool(self.applied))
        try:
            max_adj = abs(float(self.max_adjustment))
        except (TypeError, ValueError):
            max_adj = DEFAULT_MAX_WEIGHT_ADJUSTMENT
        object.__setattr__(self, "max_adjustment", max_adj)
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_RECOMMENDATION_POLICY).strip(),
        )
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or POLICY_WEIGHT_APPLICATION_VERSION).strip(),
        )

    @property
    def delta(self) -> float:
        return self.adjusted_weight - self.base_weight

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adjusted_weight": self.adjusted_weight,
            "adjustment_reason": self.adjustment_reason,
            "application_id": self.application_id,
            "applied": self.applied,
            "authority": self.authority,
            "advisory_field": self.advisory_field,
            "base_weight": self.base_weight,
            "contract_version": self.contract_version,
            "delta": self.delta,
            "generated_at": self.generated_at,
            "max_adjustment": self.max_adjustment,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "rule_id": self.rule_id,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def deterministic_weight_application_id(
    *,
    student_id: str,
    policy_version: str,
    rule_id: str,
    base_weight: float,
    adjusted_weight: float,
    generated_at: str,
) -> str:
    """Deterministic WeightApplication id from material inputs."""
    material = {
        "adjusted_weight": adjusted_weight,
        "base_weight": base_weight,
        "generated_at": (generated_at or "").strip(),
        "policy_version": (policy_version or "").strip(),
        "rule_id": (rule_id or "").strip(),
        "student_id": (student_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"wgtapp-{digest}"


def clamp_weight_adjustment(
    *,
    base_weight: float,
    proposed_delta: float,
    max_adjustment: float,
) -> float:
    """Clamp a proposed delta into ±max_adjustment and return adjusted weight."""
    bound = abs(float(max_adjustment))
    delta = max(-bound, min(bound, float(proposed_delta)))
    return float(base_weight) + delta


def compute_consistency_weight_delta(
    *,
    active_streak: int,
    max_adjustment: float = DEFAULT_MAX_WEIGHT_ADJUSTMENT,
    streak_scale: int = DEFAULT_STREAK_SCALE,
) -> float:
    """Deterministic bounded delta from consistency_summary.active_streak.

    Maps streak into [-max_adjustment, +max_adjustment] using streak_scale
    as the full-positive reference (default 7 days). Streak 0 → 0 delta.
    """
    bound = abs(float(max_adjustment))
    scale = max(1, int(streak_scale))
    streak = max(0, int(active_streak))
    if streak <= 0:
        return 0.0
    raw = (streak / scale) * bound
    return max(-bound, min(bound, raw))


def priority_base_weight(priority: str | None) -> float:
    """Map Runtime A priority label to a base scoring weight."""
    key = (priority or "").strip()
    return float(PRIORITY_BASE_WEIGHTS.get(key, 0.0))

@dataclass(frozen=True)
class RecommendationPolicy:
    """Immutable, versioned recommendation policy (P3-MS003).

    Declares advisory and weighting governance external to recommendation
    logic. Policies are independently versioned via ``version``.
    """

    policy_id: str = DEFAULT_POLICY_ID
    version: str = DEFAULT_POLICY_VERSION
    effective_from: str = ""
    advisory_rules: tuple[AdvisoryRule, ...] = ()
    weighting_rules: tuple[WeightingRule, ...] = ()
    activation_constraints: Mapping[str, Any] = field(default_factory=dict)
    explainability_requirements: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(
            self,
            "version",
            (self.version or DEFAULT_POLICY_VERSION).strip(),
        )
        object.__setattr__(
            self, "effective_from", (self.effective_from or "").strip()
        )
        advisory = tuple(
            rule
            for rule in (self.advisory_rules or ())
            if isinstance(rule, AdvisoryRule)
        )
        weighting = tuple(
            rule
            for rule in (self.weighting_rules or ())
            if isinstance(rule, WeightingRule)
        )
        object.__setattr__(self, "advisory_rules", advisory)
        object.__setattr__(self, "weighting_rules", weighting)
        object.__setattr__(
            self,
            "activation_constraints",
            _freeze_mapping(self.activation_constraints),
        )
        object.__setattr__(
            self,
            "explainability_requirements",
            _freeze_mapping(self.explainability_requirements),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "activation_constraints": dict(self.activation_constraints),
            "advisory_rules": [r.to_canonical_dict() for r in self.advisory_rules],
            "effective_from": self.effective_from,
            "explainability_requirements": dict(self.explainability_requirements),
            "policy_id": self.policy_id,
            "version": self.version,
            "weighting_rules": [
                r.to_canonical_dict() for r in self.weighting_rules
            ],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PolicyRuleResolution:
    """Resolution of a single declared rule for a request context."""

    rule_id: str
    rule_kind: str
    applicable: bool
    rationale: str = ""
    advisory_field: str = ""
    influence_mode: str = ""
    factor: str = ""
    weight: float = 0.0
    applied_to_ranking: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", (self.rule_id or "").strip())
        kind = (self.rule_kind or "").strip()
        if kind not in RULE_KINDS:
            kind = RULE_KIND_ADVISORY
        object.__setattr__(self, "rule_kind", kind)
        object.__setattr__(self, "applicable", bool(self.applicable))
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        object.__setattr__(
            self, "influence_mode", (self.influence_mode or "").strip()
        )
        object.__setattr__(self, "factor", (self.factor or "").strip())
        try:
            weight = float(self.weight)
        except (TypeError, ValueError):
            weight = 0.0
        object.__setattr__(self, "weight", weight)
        object.__setattr__(
            self, "applied_to_ranking", bool(self.applied_to_ranking)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_field": self.advisory_field,
            "applicable": self.applicable,
            "applied_to_ranking": self.applied_to_ranking,
            "factor": self.factor,
            "influence_mode": self.influence_mode,
            "rationale": self.rationale,
            "rule_id": self.rule_id,
            "rule_kind": self.rule_kind,
            "weight": self.weight,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PolicyDecision:
    """Policy decision exposed to Runtime A.

    Advisory only. Never contains recommendations. Runtime A retains final
    educational authority.
    """

    applicable: bool
    reason: str
    policy_id: str = ""
    policy_version: str = ""
    feature_flag_enabled: bool = False
    advisory_rules_applicable: tuple[PolicyRuleResolution, ...] = ()
    weighting_rules_applicable: tuple[PolicyRuleResolution, ...] = ()
    advisory_inputs_considered: Mapping[str, Any] = field(default_factory=dict)
    rationale: str = ""
    student_id: str = ""
    authority: str = AUTHORITY_RECOMMENDATION_POLICY
    policy_framework_version: str = RECOMMENDATION_POLICY_VERSION
    weighting_applied: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "applicable", bool(self.applicable))
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "feature_flag_enabled", bool(self.feature_flag_enabled)
        )
        object.__setattr__(
            self,
            "advisory_rules_applicable",
            tuple(self.advisory_rules_applicable or ()),
        )
        object.__setattr__(
            self,
            "weighting_rules_applicable",
            tuple(self.weighting_rules_applicable or ()),
        )
        object.__setattr__(
            self,
            "advisory_inputs_considered",
            _freeze_mapping(self.advisory_inputs_considered),
        )
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_RECOMMENDATION_POLICY).strip(),
        )
        object.__setattr__(
            self,
            "policy_framework_version",
            (self.policy_framework_version or RECOMMENDATION_POLICY_VERSION).strip(),
        )
        object.__setattr__(self, "weighting_applied", bool(self.weighting_applied))

    @property
    def applicable_rule_ids(self) -> tuple[str, ...]:
        ids: list[str] = []
        for rule in self.advisory_rules_applicable:
            if rule.applicable and rule.rule_id:
                ids.append(rule.rule_id)
        for rule in self.weighting_rules_applicable:
            if rule.applicable and rule.rule_id:
                ids.append(rule.rule_id)
        return tuple(ids)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_inputs_considered": dict(self.advisory_inputs_considered),
            "advisory_rules_applicable": [
                r.to_canonical_dict() for r in self.advisory_rules_applicable
            ],
            "applicable": self.applicable,
            "authority": self.authority,
            "feature_flag_enabled": self.feature_flag_enabled,
            "policy_framework_version": self.policy_framework_version,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "rationale": self.rationale,
            "reason": self.reason,
            "student_id": self.student_id,
            "weighting_applied": self.weighting_applied,
            "weighting_rules_applicable": [
                r.to_canonical_dict() for r in self.weighting_rules_applicable
            ],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RecommendationPolicyExplainability:
    """Explainability record when policy influences a recommendation path.

    Attached to Runtime A recommendations when the policy engine is consulted.
    """

    policy_version: str
    rule_identifiers: tuple[str, ...] = ()
    advisory_inputs_considered: Mapping[str, Any] = field(default_factory=dict)
    rationale: str = ""
    policy_id: str = ""
    reason: str = ""
    applicable: bool = False
    weighting_applied: bool = False
    authority: str = AUTHORITY_RUNTIME_A
    policy_framework_version: str = RECOMMENDATION_POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        ids = tuple(
            str(item).strip()
            for item in (self.rule_identifiers or ())
            if str(item).strip()
        )
        object.__setattr__(self, "rule_identifiers", ids)
        object.__setattr__(
            self,
            "advisory_inputs_considered",
            _freeze_mapping(self.advisory_inputs_considered),
        )
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "applicable", bool(self.applicable))
        object.__setattr__(self, "weighting_applied", bool(self.weighting_applied))
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_RUNTIME_A).strip()
        )
        object.__setattr__(
            self,
            "policy_framework_version",
            (self.policy_framework_version or RECOMMENDATION_POLICY_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_inputs_considered": dict(self.advisory_inputs_considered),
            "applicable": self.applicable,
            "authority": self.authority,
            "policy_framework_version": self.policy_framework_version,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "rationale": self.rationale,
            "reason": self.reason,
            "rule_identifiers": list(self.rule_identifiers),
            "weighting_applied": self.weighting_applied,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def build_default_recommendation_policy(
    *,
    policy_id: str = DEFAULT_POLICY_ID,
    version: str = DEFAULT_POLICY_VERSION,
    effective_from: str | None = None,
    advisory_rules: Sequence[AdvisoryRule] | None = None,
    weighting_rules: Sequence[WeightingRule] | None = None,
    activation_constraints: Mapping[str, Any] | None = None,
    explainability_requirements: Mapping[str, Any] | None = None,
) -> RecommendationPolicy:
    """Construct the P3-MS003 default policy (framework scaffolding).

    Default weighting rule remains disabled / not applied so MS003 behaviour
    is preserved when only ``ENABLE_RECOMMENDATION_POLICY`` is ON.
    """
    if advisory_rules is None:
        advisory_rules = (
            AdvisoryRule(
                rule_id=DEFAULT_ADVISORY_RULE_ID,
                advisory_field=DEFAULT_ADVISORY_FIELD,
                influence_mode=INFLUENCE_ANNOTATE,
                enabled=True,
                rationale=(
                    "Permit Runtime A to consider consistency_summary under "
                    "Controlled Advisory governance (annotate only)."
                ),
                conditions={"require_controlled_advisory_alignment": True},
            ),
        )
    if weighting_rules is None:
        weighting_rules = (
            WeightingRule(
                rule_id=DEFAULT_WEIGHTING_RULE_ID,
                factor="reserved",
                weight=0.0,
                enabled=False,
                apply_to_ranking=False,
                advisory_field=DEFAULT_ADVISORY_FIELD,
                max_adjustment=DEFAULT_MAX_WEIGHT_ADJUSTMENT,
                rationale=(
                    "Reserved weighting placeholder — enable via "
                    "ENABLE_POLICY_WEIGHTING / P3-MS004 default weighting policy."
                ),
                conditions={"apply_to_ranking": False},
            ),
        )
    constraints: dict[str, Any] = {
        "require_feature_flag": True,
        "require_effective_from": True,
    }
    if activation_constraints:
        constraints.update(dict(activation_constraints))
    requirements: dict[str, Any] = {
        "require_policy_version": True,
        "require_rule_identifiers": True,
        "require_advisory_inputs_considered": True,
        "require_rationale": True,
    }
    if explainability_requirements:
        requirements.update(dict(explainability_requirements))
    effective = (effective_from or "").strip()
    if not effective:
        effective = "1970-01-01T00:00:00+00:00"
    return RecommendationPolicy(
        policy_id=policy_id,
        version=version,
        effective_from=effective,
        advisory_rules=tuple(advisory_rules),
        weighting_rules=tuple(weighting_rules),
        activation_constraints=constraints,
        explainability_requirements=requirements,
    )


def build_default_weighting_policy(
    *,
    policy_id: str = DEFAULT_WEIGHTING_POLICY_ID,
    version: str = DEFAULT_WEIGHTING_POLICY_VERSION,
    effective_from: str | None = None,
    rollout_percentage: int = DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE,
    max_age_hours: int = DEFAULT_WEIGHT_MAX_AGE_HOURS,
    max_adjustment: float = DEFAULT_MAX_WEIGHT_ADJUSTMENT,
    divergence_tolerance: float = DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE,
    advisory_rules: Sequence[AdvisoryRule] | None = None,
    weighting_rules: Sequence[WeightingRule] | None = None,
) -> RecommendationPolicy:
    """Construct the P3-MS004 default policy with one bounded weighting rule."""
    if weighting_rules is None:
        weighting_rules = (
            WeightingRule(
                rule_id=DEFAULT_APPLIED_WEIGHTING_RULE_ID,
                factor="consistency_summary.active_streak",
                weight=DEFAULT_WEIGHT_BASE,
                enabled=True,
                apply_to_ranking=True,
                advisory_field=DEFAULT_ADVISORY_FIELD,
                max_adjustment=max_adjustment,
                rationale=(
                    "Bounded policy weight from consistency_summary "
                    f"(±{max_adjustment:.0%} max) under P3-MS004 governance."
                ),
                conditions={
                    "require_advisory_present": True,
                    "require_advisory_field_present": True,
                    "apply_to_ranking": True,
                },
            ),
        )
    constraints: dict[str, Any] = {
        "require_feature_flag": True,
        "require_effective_from": True,
        "require_advisory_freshness": True,
        "rollout_percentage": max(0, min(100, int(rollout_percentage))),
        "max_age_hours": max(0, int(max_age_hours)),
        "rollout_salt": DEFAULT_WEIGHT_ROLLOUT_SALT,
        "weight_divergence_tolerance": float(divergence_tolerance),
        "approved_advisory_fields": [DEFAULT_ADVISORY_FIELD],
        "max_weight_adjustment": float(max_adjustment),
    }
    return build_default_recommendation_policy(
        policy_id=policy_id,
        version=version,
        effective_from=effective_from,
        advisory_rules=advisory_rules,
        weighting_rules=weighting_rules,
        activation_constraints=constraints,
        explainability_requirements={
            "require_policy_version": True,
            "require_rule_identifiers": True,
            "require_advisory_inputs_considered": True,
            "require_rationale": True,
            "require_original_weight": True,
            "require_adjusted_weight": True,
            "require_advisory_provenance": True,
        },
    )


def validate_recommendation_policy(policy: RecommendationPolicy) -> str | None:
    """Return a denial reason when the policy is invalid; else None."""
    if not isinstance(policy, RecommendationPolicy):
        return REASON_POLICY_INVALID
    if not policy.policy_id:
        return REASON_POLICY_INVALID
    if not policy.version:
        return REASON_POLICY_INVALID
    if not policy.effective_from:
        return REASON_POLICY_INVALID

    seen_ids: set[str] = set()
    for rule in policy.advisory_rules:
        if not rule.rule_id:
            return REASON_EMPTY_RULE_ID
        if rule.rule_id in seen_ids:
            return REASON_DUPLICATE_RULE_ID
        seen_ids.add(rule.rule_id)
        if rule.influence_mode not in INFLUENCE_MODES:
            return REASON_UNKNOWN_INFLUENCE_MODE
        if not rule.advisory_field:
            return REASON_POLICY_INVALID

    ranking_weight_rules = 0
    for rule in policy.weighting_rules:
        if not rule.rule_id:
            return REASON_EMPTY_RULE_ID
        if rule.rule_id in seen_ids:
            return REASON_DUPLICATE_RULE_ID
        seen_ids.add(rule.rule_id)
        if not rule.factor:
            return REASON_POLICY_INVALID
        if rule.apply_to_ranking and rule.enabled:
            ranking_weight_rules += 1
            if rule.advisory_field not in APPROVED_WEIGHT_ADVISORY_FIELDS:
                return REASON_WEIGHT_FIELD_NOT_APPROVED
            if rule.max_adjustment < 0:
                return REASON_WEIGHT_BOUNDS_INVALID
            # Hard safety bound: never allow > ±25% even if misconfigured.
            if rule.max_adjustment > 0.25:
                return REASON_WEIGHT_BOUNDS_INVALID
    if ranking_weight_rules > 1:
        return REASON_POLICY_INVALID

    return None


def explainability_from_decision(
    decision: PolicyDecision,
) -> RecommendationPolicyExplainability:
    """Map a policy decision to a recommendation explainability record."""
    return RecommendationPolicyExplainability(
        policy_version=decision.policy_version,
        rule_identifiers=decision.applicable_rule_ids,
        advisory_inputs_considered=dict(decision.advisory_inputs_considered),
        rationale=decision.rationale or decision.reason,
        policy_id=decision.policy_id,
        reason=decision.reason,
        applicable=decision.applicable,
        weighting_applied=decision.weighting_applied,
        authority=AUTHORITY_RUNTIME_A,
    )


def explainability_from_weight_application(
    application: WeightApplication,
) -> dict[str, Any]:
    """Build Runtime A weight explainability payload from a WeightApplication."""
    return {
        "adjusted_weight": application.adjusted_weight,
        "adjustment_reason": application.adjustment_reason,
        "advisory_field": application.advisory_field,
        "advisory_provenance": dict(application.provenance),
        "application_id": application.application_id,
        "applied": application.applied,
        "authority": AUTHORITY_RUNTIME_A,
        "base_weight": application.base_weight,
        "contract_version": application.contract_version,
        "delta": application.delta,
        "generated_at": application.generated_at,
        "max_adjustment": application.max_adjustment,
        "original_weight": application.base_weight,
        "policy_id": application.policy_id,
        "policy_version": application.policy_version,
        "rule_id": application.rule_id,
        "rule_identifier": application.rule_id,
    }


def explainability_fields_present(
    record: RecommendationPolicyExplainability | Mapping[str, Any],
) -> bool:
    """Return True when required explainability fields are present."""
    if isinstance(record, RecommendationPolicyExplainability):
        payload = record.to_canonical_dict()
    else:
        payload = dict(record)
    version = str(payload.get("policy_version") or "").strip()
    rationale = str(payload.get("rationale") or "").strip()
    rule_ids = payload.get("rule_identifiers") or ()
    inputs = payload.get("advisory_inputs_considered")
    if not version or not rationale:
        return False
    if not isinstance(rule_ids, list | tuple):
        return False
    if inputs is None or not isinstance(inputs, Mapping):
        return False
    return True


def weight_explainability_fields_present(payload: Mapping[str, Any]) -> bool:
    """Return True when required weight explainability fields are present."""
    required = (
        "original_weight",
        "adjusted_weight",
        "policy_version",
        "rule_identifier",
        "advisory_provenance",
        "adjustment_reason",
    )
    for key in required:
        if key not in payload:
            return False
    if not str(payload.get("policy_version") or "").strip():
        return False
    if not str(payload.get("rule_identifier") or payload.get("rule_id") or "").strip():
        return False
    if not str(payload.get("adjustment_reason") or "").strip():
        return False
    if not isinstance(payload.get("advisory_provenance"), Mapping):
        return False
    return True


def snapshot_explainability_list(
    records: Sequence[RecommendationPolicyExplainability] | None,
) -> tuple[Mapping[str, Any], ...]:
    """Freeze explainability records into canonical mappings."""
    if not records:
        return ()
    return tuple(item.to_canonical_dict() for item in records)


__all__ = [
    "APPROVED_WEIGHT_ADVISORY_FIELDS",
    "AUTHORITY_RECOMMENDATION_POLICY",
    "AUTHORITY_RUNTIME_A",
    "DEFAULT_ADVISORY_FIELD",
    "DEFAULT_ADVISORY_RULE_ID",
    "DEFAULT_APPLIED_WEIGHTING_RULE_ID",
    "DEFAULT_MAX_WEIGHT_ADJUSTMENT",
    "DEFAULT_POLICY_ID",
    "DEFAULT_POLICY_VERSION",
    "DEFAULT_STREAK_SCALE",
    "DEFAULT_WEIGHTING_POLICY_ID",
    "DEFAULT_WEIGHTING_POLICY_VERSION",
    "DEFAULT_WEIGHTING_RULE_ID",
    "DEFAULT_WEIGHT_BASE",
    "DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE",
    "DEFAULT_WEIGHT_MAX_AGE_HOURS",
    "DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE",
    "DEFAULT_WEIGHT_ROLLOUT_SALT",
    "INFLUENCE_ANNOTATE",
    "INFLUENCE_MODES",
    "INFLUENCE_PERMIT",
    "INVALID_STATE",
    "POLICY_ERROR_CODES",
    "POLICY_EXPLAINABILITY_KEY",
    "POLICY_WEIGHT_APPLICATION_VERSION",
    "PRIORITY_BASE_WEIGHTS",
    "REASON_ACTIVATION_CONSTRAINTS",
    "REASON_DUPLICATE_RULE_ID",
    "REASON_EMPTY_RULE_ID",
    "REASON_EFFECTIVE_FROM_FUTURE",
    "REASON_FLAG_OFF",
    "REASON_NO_RULES_APPLICABLE",
    "REASON_POLICY_INVALID",
    "REASON_POLICY_MISSING",
    "REASON_RULES_RESOLVED",
    "REASON_UNKNOWN_INFLUENCE_MODE",
    "REASON_WEIGHTING_FLAG_OFF",
    "REASON_WEIGHTING_NOT_APPLIED",
    "REASON_WEIGHT_ADVISORY_FIELD_MISSING",
    "REASON_WEIGHT_ADVISORY_MISSING",
    "REASON_WEIGHT_ADVISORY_STALE",
    "REASON_WEIGHT_APPLIED",
    "REASON_WEIGHT_BOUNDS_INVALID",
    "REASON_WEIGHT_DENIED",
    "REASON_WEIGHT_FIELD_NOT_APPROVED",
    "REASON_WEIGHT_NO_RULE",
    "REASON_WEIGHT_ROLLOUT_EXCLUDED",
    "REASON_WEIGHT_SIMULATION_DIVERGENCE",
    "RECOMMENDATION_POLICY_VERSION",
    "RULE_KIND_ADVISORY",
    "RULE_KIND_WEIGHTING",
    "RULE_KINDS",
    "UNAVAILABLE",
    "WEIGHT_EXPLAINABILITY_KEY",
    "AdvisoryRule",
    "PolicyDecision",
    "PolicyRuleResolution",
    "RecommendationPolicy",
    "RecommendationPolicyExplainability",
    "WeightApplication",
    "WeightingRule",
    "build_default_recommendation_policy",
    "build_default_weighting_policy",
    "clamp_weight_adjustment",
    "compute_consistency_weight_delta",
    "deterministic_weight_application_id",
    "explainability_fields_present",
    "explainability_from_decision",
    "explainability_from_weight_application",
    "priority_base_weight",
    "serialize_canonical",
    "snapshot_explainability_list",
    "snapshot_mapping",
    "validate_recommendation_policy",
    "weight_explainability_fields_present",
]
