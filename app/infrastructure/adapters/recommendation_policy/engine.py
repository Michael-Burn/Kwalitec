"""Recommendation Policy Engine (P3-MS003 / P3-MS004).

Validates policies, resolves applicable rules, and exposes policy decisions
to Runtime A. Never generates recommendations.

P3-MS004 adds a policy weight resolver that returns at most one immutable
``WeightApplication`` (bounded, single advisory field). Runtime A applies
the adjustment and retains final recommendation authority.
"""

from __future__ import annotations

import hashlib
import logging
import os
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from typing import Any

from .contracts import (
    APPROVED_WEIGHT_ADVISORY_FIELDS,
    AUTHORITY_RUNTIME_A,
    DEFAULT_ADVISORY_FIELD,
    DEFAULT_MAX_WEIGHT_ADJUSTMENT,
    DEFAULT_STREAK_SCALE,
    DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE,
    DEFAULT_WEIGHT_MAX_AGE_HOURS,
    DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE,
    DEFAULT_WEIGHT_ROLLOUT_SALT,
    POLICY_EXPLAINABILITY_KEY,
    REASON_EFFECTIVE_FROM_FUTURE,
    REASON_FLAG_OFF,
    REASON_NO_RULES_APPLICABLE,
    REASON_POLICY_MISSING,
    REASON_RULES_RESOLVED,
    REASON_WEIGHT_ADVISORY_FIELD_MISSING,
    REASON_WEIGHT_ADVISORY_MISSING,
    REASON_WEIGHT_ADVISORY_STALE,
    REASON_WEIGHT_APPLIED,
    REASON_WEIGHT_FIELD_NOT_APPROVED,
    REASON_WEIGHT_NO_RULE,
    REASON_WEIGHT_ROLLOUT_EXCLUDED,
    REASON_WEIGHT_SIMULATION_DIVERGENCE,
    REASON_WEIGHTING_FLAG_OFF,
    REASON_WEIGHTING_NOT_APPLIED,
    RECOMMENDATION_POLICY_VERSION,
    RULE_KIND_ADVISORY,
    RULE_KIND_WEIGHTING,
    WEIGHT_EXPLAINABILITY_KEY,
    AdvisoryRule,
    PolicyDecision,
    PolicyRuleResolution,
    RecommendationPolicy,
    WeightApplication,
    WeightingRule,
    build_default_recommendation_policy,
    build_default_weighting_policy,
    clamp_weight_adjustment,
    compute_consistency_weight_delta,
    deterministic_weight_application_id,
    explainability_from_decision,
    explainability_from_weight_application,
    priority_base_weight,
    validate_recommendation_policy,
)

logger = logging.getLogger(__name__)

ENGINE_ID = "recommendation_policy_engine"
ENGINE_VERSION = RECOMMENDATION_POLICY_VERSION
SERVICE_ID = "recommendation_policy"
SOURCE_SERVICE = "recommendation_policy"


def _parse_iso(value: str | None) -> datetime | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _env_int(name: str, default: int, *, environ: Mapping[str, str] | None) -> int:
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return default


def _env_float(
    name: str, default: float, *, environ: Mapping[str, str] | None
) -> float:
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return float(str(raw).strip())
    except (TypeError, ValueError):
        return default


def student_in_weight_rollout(
    student_id: str,
    *,
    rollout_percentage: int,
    salt: str = DEFAULT_WEIGHT_ROLLOUT_SALT,
) -> bool:
    """Deterministic percentage rollout gate from student identity."""
    percentage = max(0, min(100, int(rollout_percentage)))
    if percentage <= 0:
        return False
    if percentage >= 100:
        return True
    sid = (student_id or "").strip()
    if not sid:
        return False
    material = f"{salt}:{sid}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 100
    return bucket < percentage


def resolve_recommendation_policy(
    *,
    environ: Mapping[str, str] | None = None,
) -> RecommendationPolicy:
    """Resolve RecommendationPolicy from environment (safe defaults)."""
    env = environ if environ is not None else os.environ
    effective_from = (
        env.get("KWALITEC_RECOMMENDATION_POLICY_EFFECTIVE_FROM") or ""
    ).strip()
    policy_id = (env.get("KWALITEC_RECOMMENDATION_POLICY_ID") or "").strip()
    version = (env.get("KWALITEC_RECOMMENDATION_POLICY_VERSION") or "").strip()
    kwargs: dict[str, Any] = {"effective_from": effective_from or None}
    if policy_id:
        kwargs["policy_id"] = policy_id
    if version:
        kwargs["version"] = version
    return build_default_recommendation_policy(**kwargs)


def resolve_weighting_policy(
    *,
    environ: Mapping[str, str] | None = None,
) -> RecommendationPolicy:
    """Resolve P3-MS004 weighting policy from environment (safe defaults)."""
    env = environ if environ is not None else os.environ
    effective_from = (
        env.get("KWALITEC_POLICY_WEIGHTING_EFFECTIVE_FROM")
        or env.get("KWALITEC_RECOMMENDATION_POLICY_EFFECTIVE_FROM")
        or ""
    ).strip()
    policy_id = (env.get("KWALITEC_POLICY_WEIGHTING_POLICY_ID") or "").strip()
    version = (env.get("KWALITEC_POLICY_WEIGHTING_POLICY_VERSION") or "").strip()
    rollout = _env_int(
        "KWALITEC_POLICY_WEIGHTING_ROLLOUT_PERCENTAGE",
        DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE,
        environ=environ,
    )
    max_age = _env_int(
        "KWALITEC_POLICY_WEIGHTING_MAX_AGE_HOURS",
        DEFAULT_WEIGHT_MAX_AGE_HOURS,
        environ=environ,
    )
    max_adj = _env_float(
        "KWALITEC_POLICY_WEIGHTING_MAX_ADJUSTMENT",
        DEFAULT_MAX_WEIGHT_ADJUSTMENT,
        environ=environ,
    )
    tolerance = _env_float(
        "KWALITEC_POLICY_WEIGHTING_DIVERGENCE_TOLERANCE",
        DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE,
        environ=environ,
    )
    kwargs: dict[str, Any] = {
        "effective_from": effective_from or None,
        "rollout_percentage": rollout,
        "max_age_hours": max_age,
        "max_adjustment": max_adj,
        "divergence_tolerance": tolerance,
    }
    if policy_id:
        kwargs["policy_id"] = policy_id
    if version:
        kwargs["version"] = version
    return build_default_weighting_policy(**kwargs)


def _advisory_inputs_snapshot(advisory: Any | None) -> dict[str, Any]:
    """Capture advisory inputs considered (factual metadata only)."""
    if advisory is None:
        return {"advisory_present": False}
    if hasattr(advisory, "to_canonical_dict"):
        canonical = advisory.to_canonical_dict()
        return {
            "advisory_present": True,
            "advisory_id": str(canonical.get("advisory_id") or ""),
            "evidence_summary_id": str(
                canonical.get("evidence_summary_id") or ""
            ),
            "availability": str(canonical.get("availability") or ""),
            "generated_at": canonical.get("generated_at"),
            "fields_present": sorted(
                key
                for key in (
                    "consistency_summary",
                    "engagement_summary",
                    "observed_patterns",
                    "factual_constraints",
                )
                if canonical.get(key) is not None
            ),
        }
    if isinstance(advisory, Mapping):
        return {
            "advisory_present": True,
            "advisory_id": str(advisory.get("advisory_id") or ""),
            "evidence_summary_id": str(
                advisory.get("evidence_summary_id") or ""
            ),
            "availability": str(advisory.get("availability") or ""),
            "generated_at": advisory.get("generated_at"),
            "fields_present": sorted(
                key
                for key in (
                    "consistency_summary",
                    "engagement_summary",
                    "observed_patterns",
                    "factual_constraints",
                )
                if advisory.get(key) is not None
            ),
        }
    return {"advisory_present": True, "advisory_type": type(advisory).__name__}


def _advisory_provenance(advisory: Any | None) -> dict[str, Any]:
    if advisory is None:
        return {}
    if hasattr(advisory, "to_canonical_dict"):
        canonical = advisory.to_canonical_dict()
        return {
            "advisory_id": canonical.get("advisory_id", ""),
            "evidence_summary_id": canonical.get("evidence_summary_id", ""),
            "evidence_refs": list(canonical.get("evidence_refs") or []),
            "provenance": dict(canonical.get("provenance") or {}),
            "authority": canonical.get("authority", ""),
            "generated_at": canonical.get("generated_at"),
            "consistency_summary": dict(
                canonical.get("consistency_summary") or {}
            ),
        }
    if isinstance(advisory, Mapping):
        return {
            "advisory_id": str(advisory.get("advisory_id") or ""),
            "evidence_summary_id": str(advisory.get("evidence_summary_id") or ""),
            "evidence_refs": list(advisory.get("evidence_refs") or []),
            "provenance": dict(advisory.get("provenance") or {}),
            "authority": str(advisory.get("authority") or ""),
            "generated_at": advisory.get("generated_at"),
            "consistency_summary": dict(
                advisory.get("consistency_summary") or {}
            ),
        }
    return {}


def _consistency_active_streak(advisory: Any | None) -> int | None:
    if advisory is None:
        return None
    summary = None
    if hasattr(advisory, "consistency_summary"):
        summary = advisory.consistency_summary
    elif isinstance(advisory, Mapping):
        summary = advisory.get("consistency_summary")
    if summary is None:
        return None
    if hasattr(summary, "active_streak"):
        try:
            return int(summary.active_streak)
        except (TypeError, ValueError):
            return None
    if isinstance(summary, Mapping) and "active_streak" in summary:
        try:
            return int(summary["active_streak"])
        except (TypeError, ValueError):
            return None
    return None


def _condition_met(
    conditions: Mapping[str, Any],
    *,
    advisory: Any | None,
    advisory_field: str = "",
) -> tuple[bool, str]:
    """Evaluate simple declarative conditions (no educational scoring)."""
    if not conditions:
        return True, ""
    require_advisory = bool(conditions.get("require_advisory_present", False))
    if require_advisory and advisory is None:
        return False, "advisory_absent"
    require_field = bool(conditions.get("require_advisory_field_present", False))
    if require_field and advisory_field:
        present = False
        if advisory is not None:
            if hasattr(advisory, advisory_field):
                present = getattr(advisory, advisory_field) is not None
            elif isinstance(advisory, Mapping):
                present = (
                    advisory_field in advisory
                    and advisory[advisory_field] is not None
                )
        if not present:
            return False, f"advisory_field_absent:{advisory_field}"
    return True, ""


def _resolve_advisory_rule(
    rule: AdvisoryRule,
    *,
    advisory: Any | None,
) -> PolicyRuleResolution:
    if not rule.enabled:
        return PolicyRuleResolution(
            rule_id=rule.rule_id,
            rule_kind=RULE_KIND_ADVISORY,
            applicable=False,
            rationale="rule_disabled",
            advisory_field=rule.advisory_field,
            influence_mode=rule.influence_mode,
        )
    ok, detail = _condition_met(
        rule.conditions,
        advisory=advisory,
        advisory_field=rule.advisory_field,
    )
    if not ok:
        return PolicyRuleResolution(
            rule_id=rule.rule_id,
            rule_kind=RULE_KIND_ADVISORY,
            applicable=False,
            rationale=detail or "conditions_unmet",
            advisory_field=rule.advisory_field,
            influence_mode=rule.influence_mode,
        )
    rationale = rule.rationale or "advisory_rule_applicable"
    return PolicyRuleResolution(
        rule_id=rule.rule_id,
        rule_kind=RULE_KIND_ADVISORY,
        applicable=True,
        rationale=rationale,
        advisory_field=rule.advisory_field,
        influence_mode=rule.influence_mode,
        applied_to_ranking=False,
    )


def _resolve_weighting_rule(
    rule: WeightingRule,
    *,
    advisory: Any | None,
    weighting_enabled: bool,
) -> PolicyRuleResolution:
    """Resolve weighting rules; ranking apply only when weighting flag is ON."""
    if not rule.enabled:
        return PolicyRuleResolution(
            rule_id=rule.rule_id,
            rule_kind=RULE_KIND_WEIGHTING,
            applicable=False,
            rationale="rule_disabled",
            factor=rule.factor,
            weight=rule.weight,
            applied_to_ranking=False,
            advisory_field=rule.advisory_field,
        )
    ok, detail = _condition_met(
        rule.conditions,
        advisory=advisory,
        advisory_field=rule.advisory_field,
    )
    if not ok:
        return PolicyRuleResolution(
            rule_id=rule.rule_id,
            rule_kind=RULE_KIND_WEIGHTING,
            applicable=False,
            rationale=detail or "conditions_unmet",
            factor=rule.factor,
            weight=rule.weight,
            applied_to_ranking=False,
            advisory_field=rule.advisory_field,
        )
    may_apply = bool(weighting_enabled and rule.apply_to_ranking)
    if may_apply:
        rationale = rule.rationale or REASON_WEIGHT_APPLIED
    else:
        rationale = (
            f"{REASON_WEIGHTING_NOT_APPLIED}: "
            f"{rule.rationale or 'weighting_rule_resolved'}"
        )
    return PolicyRuleResolution(
        rule_id=rule.rule_id,
        rule_kind=RULE_KIND_WEIGHTING,
        applicable=True,
        rationale=rationale,
        factor=rule.factor,
        weight=rule.weight,
        applied_to_ranking=may_apply,
        advisory_field=rule.advisory_field,
    )


def _denied_weight_application(
    *,
    reason: str,
    student_id: str,
    policy: RecommendationPolicy | None,
    provenance: Mapping[str, Any] | None = None,
    generated_at: str = "",
    rule_id: str = "",
    advisory_field: str = DEFAULT_ADVISORY_FIELD,
    base_weight: float = 1.0,
    max_adjustment: float = DEFAULT_MAX_WEIGHT_ADJUSTMENT,
) -> WeightApplication:
    policy_version = policy.version if policy else ""
    policy_id = policy.policy_id if policy else ""
    app_id = deterministic_weight_application_id(
        student_id=student_id,
        policy_version=policy_version,
        rule_id=rule_id or reason,
        base_weight=base_weight,
        adjusted_weight=base_weight,
        generated_at=generated_at,
    )
    return WeightApplication(
        application_id=app_id,
        policy_version=policy_version,
        rule_id=rule_id,
        advisory_field=advisory_field,
        base_weight=base_weight,
        adjusted_weight=base_weight,
        adjustment_reason=reason,
        provenance=dict(provenance or {}),
        generated_at=generated_at,
        applied=False,
        max_adjustment=max_adjustment,
        policy_id=policy_id,
        student_id=student_id,
    )


class RecommendationPolicyEngine:
    """Validate policies, resolve rules, expose decisions to Runtime A.

    Never ranks topics, never builds recommendations, never writes educational
    state. When ``weighting_enabled`` is True, may resolve a single bounded
    ``WeightApplication`` for Runtime A to apply.
    """

    ENGINE_ID = ENGINE_ID
    ENGINE_VERSION = ENGINE_VERSION

    def __init__(
        self,
        *,
        enabled: bool = True,
        weighting_enabled: bool = False,
        policy: RecommendationPolicy | None = None,
        now: datetime | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._weighting_enabled = bool(weighting_enabled)
        self._policy = policy
        self._now = now
        self._last_decision: PolicyDecision | None = None
        self._last_weight_application: WeightApplication | None = None
        self._last_simulation_divergence: dict[str, Any] | None = None

    @property
    def engine_id(self) -> str:
        return self.ENGINE_ID

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def is_weighting_enabled(self) -> bool:
        return self._weighting_enabled

    @property
    def policy(self) -> RecommendationPolicy | None:
        return self._policy

    @property
    def last_decision(self) -> PolicyDecision | None:
        return self._last_decision

    @property
    def last_weight_application(self) -> WeightApplication | None:
        return self._last_weight_application

    @property
    def last_simulation_divergence(self) -> dict[str, Any] | None:
        return self._last_simulation_divergence

    def _clock(self) -> datetime:
        if self._now is not None:
            return (
                self._now
                if self._now.tzinfo
                else self._now.replace(tzinfo=UTC)
            )
        return datetime.now(UTC)

    def validate(
        self,
        policy: RecommendationPolicy | None = None,
    ) -> str | None:
        """Validate a policy; return denial reason or None when valid."""
        active = policy if policy is not None else self._policy
        if active is None:
            return REASON_POLICY_MISSING
        return validate_recommendation_policy(active)

    def resolve(
        self,
        *,
        student_id: str,
        advisory: Any | None = None,
        policy: RecommendationPolicy | None = None,
        feature_flag_enabled: bool | None = None,
    ) -> PolicyDecision:
        """Resolve applicable rules and return a PolicyDecision.

        Never generates recommendations. Weighting resolutions set
        ``applied_to_ranking`` only when ``weighting_enabled`` is True and the
        rule permits ranking application.
        """
        sid = (student_id or "").strip()
        flag_on = (
            self._enabled
            if feature_flag_enabled is None
            else bool(feature_flag_enabled)
        )
        active_policy = policy if policy is not None else self._policy
        inputs = _advisory_inputs_snapshot(advisory)

        if not flag_on:
            decision = PolicyDecision(
                applicable=False,
                reason=REASON_FLAG_OFF,
                policy_id=active_policy.policy_id if active_policy else "",
                policy_version=active_policy.version if active_policy else "",
                feature_flag_enabled=False,
                advisory_inputs_considered=inputs,
                rationale="Recommendation policy feature flag is OFF.",
                student_id=sid,
            )
            self._last_decision = decision
            return decision

        if active_policy is None:
            decision = PolicyDecision(
                applicable=False,
                reason=REASON_POLICY_MISSING,
                feature_flag_enabled=True,
                advisory_inputs_considered=inputs,
                rationale="No recommendation policy configured.",
                student_id=sid,
            )
            self._last_decision = decision
            return decision

        invalid = validate_recommendation_policy(active_policy)
        if invalid is not None:
            decision = PolicyDecision(
                applicable=False,
                reason=invalid,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.version,
                feature_flag_enabled=True,
                advisory_inputs_considered=inputs,
                rationale=f"Policy validation failed: {invalid}.",
                student_id=sid,
            )
            self._last_decision = decision
            return decision

        constraints = active_policy.activation_constraints
        require_effective = bool(constraints.get("require_effective_from", True))
        if require_effective:
            effective = _parse_iso(active_policy.effective_from)
            if effective is not None and effective > self._clock():
                decision = PolicyDecision(
                    applicable=False,
                    reason=REASON_EFFECTIVE_FROM_FUTURE,
                    policy_id=active_policy.policy_id,
                    policy_version=active_policy.version,
                    feature_flag_enabled=True,
                    advisory_inputs_considered=inputs,
                    rationale=(
                        "Policy effective_from is in the future; rules not "
                        "applicable."
                    ),
                    student_id=sid,
                )
                self._last_decision = decision
                return decision

        advisory_resolutions = tuple(
            _resolve_advisory_rule(rule, advisory=advisory)
            for rule in active_policy.advisory_rules
        )
        weighting_resolutions = tuple(
            _resolve_weighting_rule(
                rule,
                advisory=advisory,
                weighting_enabled=self._weighting_enabled,
            )
            for rule in active_policy.weighting_rules
        )

        any_applicable = any(r.applicable for r in advisory_resolutions) or any(
            r.applicable for r in weighting_resolutions
        )
        if not any_applicable:
            decision = PolicyDecision(
                applicable=False,
                reason=REASON_NO_RULES_APPLICABLE,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.version,
                feature_flag_enabled=True,
                advisory_rules_applicable=advisory_resolutions,
                weighting_rules_applicable=weighting_resolutions,
                advisory_inputs_considered=inputs,
                rationale="No advisory or weighting rules were applicable.",
                student_id=sid,
            )
            self._last_decision = decision
            return decision

        applicable_ids = [
            r.rule_id
            for r in (*advisory_resolutions, *weighting_resolutions)
            if r.applicable
        ]
        weighting_applied = any(
            r.applicable and r.applied_to_ranking for r in weighting_resolutions
        )
        if weighting_applied:
            weight_note = "Weighting eligible for Runtime A application (P3-MS004)."
        else:
            weight_note = "Weighting not applied to ranking (policy / flag)."
        decision = PolicyDecision(
            applicable=True,
            reason=REASON_RULES_RESOLVED,
            policy_id=active_policy.policy_id,
            policy_version=active_policy.version,
            feature_flag_enabled=True,
            advisory_rules_applicable=advisory_resolutions,
            weighting_rules_applicable=weighting_resolutions,
            advisory_inputs_considered=inputs,
            rationale=(
                "Policy rules resolved for Runtime A consideration: "
                + ", ".join(applicable_ids)
                + f". {weight_note}"
            ),
            student_id=sid,
            weighting_applied=weighting_applied,
        )
        self._last_decision = decision
        return decision

    def resolve_for_recommendation(
        self,
        student_id: str | int,
        *,
        advisory: Any | None = None,
        policy: RecommendationPolicy | None = None,
    ) -> PolicyDecision:
        """Runtime A entry: resolve applicable policy before recommending."""
        return self.resolve(
            student_id=str(student_id),
            advisory=advisory,
            policy=policy,
        )

    def resolve_weight_application(
        self,
        *,
        student_id: str,
        advisory: Any | None = None,
        policy: RecommendationPolicy | None = None,
        feature_flag_enabled: bool | None = None,
    ) -> WeightApplication:
        """Resolve one approved bounded weight adjustment (P3-MS004).

        Validates policy, rollout, and advisory freshness. Returns an
        immutable ``WeightApplication`` only — never mutates recommendations.
        """
        sid = (student_id or "").strip()
        flag_on = (
            self._weighting_enabled
            if feature_flag_enabled is None
            else bool(feature_flag_enabled)
        )
        active_policy = policy if policy is not None else self._policy
        now = self._clock()
        generated_at = now.isoformat()
        provenance = _advisory_provenance(advisory)

        if not flag_on:
            application = _denied_weight_application(
                reason=REASON_WEIGHTING_FLAG_OFF,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        if active_policy is None:
            application = _denied_weight_application(
                reason=REASON_POLICY_MISSING,
                student_id=sid,
                policy=None,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        invalid = validate_recommendation_policy(active_policy)
        if invalid is not None:
            application = _denied_weight_application(
                reason=invalid,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        constraints = dict(active_policy.activation_constraints or {})
        require_effective = bool(constraints.get("require_effective_from", True))
        if require_effective:
            effective = _parse_iso(active_policy.effective_from)
            if effective is not None and effective > now:
                application = _denied_weight_application(
                    reason=REASON_EFFECTIVE_FROM_FUTURE,
                    student_id=sid,
                    policy=active_policy,
                    provenance=provenance,
                    generated_at=generated_at,
                )
                self._last_weight_application = application
                return application

        rollout = int(
            constraints.get(
                "rollout_percentage", DEFAULT_WEIGHT_ROLLOUT_PERCENTAGE
            )
        )
        salt = str(constraints.get("rollout_salt") or DEFAULT_WEIGHT_ROLLOUT_SALT)
        if not student_in_weight_rollout(
            sid, rollout_percentage=rollout, salt=salt
        ):
            application = _denied_weight_application(
                reason=REASON_WEIGHT_ROLLOUT_EXCLUDED,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        if advisory is None:
            application = _denied_weight_application(
                reason=REASON_WEIGHT_ADVISORY_MISSING,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        max_age = int(constraints.get("max_age_hours", DEFAULT_WEIGHT_MAX_AGE_HOURS))
        if max_age < 0:
            max_age = DEFAULT_WEIGHT_MAX_AGE_HOURS
        generated_raw = provenance.get("generated_at")
        parsed_generated = _parse_iso(
            generated_raw if isinstance(generated_raw, str) else None
        )
        if parsed_generated is None:
            application = _denied_weight_application(
                reason=REASON_WEIGHT_ADVISORY_STALE,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application
        if now - parsed_generated > timedelta(hours=max_age):
            application = _denied_weight_application(
                reason=REASON_WEIGHT_ADVISORY_STALE,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        candidates = [
            rule
            for rule in active_policy.weighting_rules
            if rule.enabled and rule.apply_to_ranking
        ]
        if not candidates:
            application = _denied_weight_application(
                reason=REASON_WEIGHT_NO_RULE,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
            )
            self._last_weight_application = application
            return application

        # Exactly one approved ranking weight rule (validated by policy).
        rule = candidates[0]
        if rule.advisory_field not in APPROVED_WEIGHT_ADVISORY_FIELDS:
            application = _denied_weight_application(
                reason=REASON_WEIGHT_FIELD_NOT_APPROVED,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
                rule_id=rule.rule_id,
                advisory_field=rule.advisory_field,
                base_weight=rule.weight,
                max_adjustment=rule.max_adjustment,
            )
            self._last_weight_application = application
            return application

        ok, detail = _condition_met(
            rule.conditions,
            advisory=advisory,
            advisory_field=rule.advisory_field,
        )
        if not ok:
            application = _denied_weight_application(
                reason=detail or REASON_WEIGHT_ADVISORY_FIELD_MISSING,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
                rule_id=rule.rule_id,
                advisory_field=rule.advisory_field,
                base_weight=rule.weight,
                max_adjustment=rule.max_adjustment,
            )
            self._last_weight_application = application
            return application

        streak = _consistency_active_streak(advisory)
        if streak is None:
            application = _denied_weight_application(
                reason=REASON_WEIGHT_ADVISORY_FIELD_MISSING,
                student_id=sid,
                policy=active_policy,
                provenance=provenance,
                generated_at=generated_at,
                rule_id=rule.rule_id,
                advisory_field=rule.advisory_field,
                base_weight=rule.weight,
                max_adjustment=rule.max_adjustment,
            )
            self._last_weight_application = application
            return application

        max_adj = float(rule.max_adjustment)
        if "max_weight_adjustment" in constraints:
            try:
                max_adj = min(max_adj, abs(float(constraints["max_weight_adjustment"])))
            except (TypeError, ValueError):
                pass
        proposed = compute_consistency_weight_delta(
            active_streak=streak,
            max_adjustment=max_adj,
            streak_scale=DEFAULT_STREAK_SCALE,
        )
        adjusted = clamp_weight_adjustment(
            base_weight=rule.weight,
            proposed_delta=proposed,
            max_adjustment=max_adj,
        )
        reason = (
            f"{REASON_WEIGHT_APPLIED}: consistency_summary.active_streak={streak} "
            f"delta={adjusted - rule.weight:+.4f} bounded_by=±{max_adj}"
        )
        app_id = deterministic_weight_application_id(
            student_id=sid,
            policy_version=active_policy.version,
            rule_id=rule.rule_id,
            base_weight=rule.weight,
            adjusted_weight=adjusted,
            generated_at=generated_at,
        )
        application = WeightApplication(
            application_id=app_id,
            policy_version=active_policy.version,
            rule_id=rule.rule_id,
            advisory_field=rule.advisory_field,
            base_weight=rule.weight,
            adjusted_weight=adjusted,
            adjustment_reason=reason,
            provenance=provenance,
            generated_at=generated_at,
            applied=True,
            max_adjustment=max_adj,
            policy_id=active_policy.policy_id,
            student_id=sid,
        )
        self._last_weight_application = application
        return application

    def attach_explainability(
        self,
        recommendations: list[dict],
        decision: PolicyDecision | None = None,
    ) -> list[dict]:
        """Attach policy explainability to recommendations without reordering.

        Runtime A remains responsible for the recommendation content. This
        helper only records policy version, rule ids, advisory inputs, and
        rationale on each recommendation dict.
        """
        active = decision if decision is not None else self._last_decision
        if active is None:
            return recommendations
        record = explainability_from_decision(active)
        payload = record.to_canonical_dict()
        annotated: list[dict] = []
        for item in recommendations:
            copy = deepcopy(item) if isinstance(item, dict) else {"value": item}
            if isinstance(copy, dict):
                copy[POLICY_EXPLAINABILITY_KEY] = dict(payload)
                copy.setdefault("authority", AUTHORITY_RUNTIME_A)
            annotated.append(copy)
        return annotated

    def apply_weight_to_recommendations(
        self,
        student_id: str | int,
        recommendations: Sequence[Mapping[str, Any]] | None,
        *,
        advisory: Any | None = None,
        policy: RecommendationPolicy | None = None,
        reorder: bool = True,
    ) -> list[dict[str, Any]]:
        """Apply exactly one approved weight adjustment under Runtime A.

        When weighting is denied / disabled, recommendations are returned with
        explainability recording why no adjustment occurred. When applied,
        each recommendation receives a scoring weight; optional reorder uses
        adjusted scores while Runtime A remains the producing authority.
        """
        source = list(recommendations or ())
        copies: list[dict[str, Any]] = [deepcopy(dict(item)) for item in source]

        if not self._weighting_enabled:
            application = self.resolve_weight_application(
                student_id=str(student_id),
                advisory=advisory,
                policy=policy,
                feature_flag_enabled=False,
            )
            # Immediate rollback: leave student-facing payload untouched.
            _ = application
            return copies

        application = self.resolve_weight_application(
            student_id=str(student_id),
            advisory=advisory,
            policy=policy,
        )
        explain = explainability_from_weight_application(application)

        if not application.applied:
            for item in copies:
                item[WEIGHT_EXPLAINABILITY_KEY] = {
                    **explain,
                    "scoring_weight_original": priority_base_weight(
                        str(item.get("priority") or "")
                    ),
                    "scoring_weight_adjusted": priority_base_weight(
                        str(item.get("priority") or "")
                    ),
                    "weight_adjusted": False,
                }
                item.setdefault("authority", AUTHORITY_RUNTIME_A)
            logger.debug(
                "policy_weight_denied student_id=%s reason=%s",
                str(student_id).strip(),
                application.adjustment_reason,
            )
            return copies

        factor = (
            application.adjusted_weight / application.base_weight
            if application.base_weight
            else application.adjusted_weight
        )
        for item in copies:
            original = priority_base_weight(str(item.get("priority") or ""))
            adjusted_score = original * factor
            item["scoring_weight"] = adjusted_score
            item[WEIGHT_EXPLAINABILITY_KEY] = {
                **explain,
                "scoring_weight_original": original,
                "scoring_weight_adjusted": adjusted_score,
                "weight_adjusted": True,
                "original_weight": application.base_weight,
                "adjusted_weight": application.adjusted_weight,
            }
            item.setdefault("authority", AUTHORITY_RUNTIME_A)

        if reorder and copies:
            copies.sort(
                key=lambda r: (
                    -float(r.get("scoring_weight") or 0.0),
                    str(r.get("title") or ""),
                )
            )

        logger.debug(
            "policy_weight_applied student_id=%s rule=%s delta=%s count=%s",
            str(student_id).strip(),
            application.rule_id,
            application.delta,
            len(copies),
        )
        return copies

    def compare_weight_simulation(
        self,
        production: Sequence[Mapping[str, Any]] | None,
        simulated: Sequence[Mapping[str, Any]] | None,
        *,
        tolerance: float | None = None,
    ) -> dict[str, Any]:
        """Compare production vs simulation weights after application.

        Flags divergence beyond configured tolerance. Operational only —
        never mutates recommendations.
        """
        active_policy = self._policy
        if tolerance is None:
            if active_policy is not None:
                raw = active_policy.activation_constraints.get(
                    "weight_divergence_tolerance",
                    DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE,
                )
                try:
                    tolerance = float(raw)
                except (TypeError, ValueError):
                    tolerance = DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE
            else:
                tolerance = DEFAULT_WEIGHT_DIVERGENCE_TOLERANCE
        bound = abs(float(tolerance))

        prod = list(production or ())
        sim = list(simulated or ())
        divergences: list[dict[str, Any]] = []
        limit = max(len(prod), len(sim))
        for index in range(limit):
            p = prod[index] if index < len(prod) else {}
            s = sim[index] if index < len(sim) else {}
            p_w = p.get("scoring_weight")
            s_w = s.get("scoring_weight")
            if p_w is None and s_w is None:
                continue
            try:
                p_val = float(p_w) if p_w is not None else 0.0
                s_val = float(s_w) if s_w is not None else 0.0
            except (TypeError, ValueError):
                divergences.append(
                    {
                        "index": index,
                        "title": str(p.get("title") or s.get("title") or ""),
                        "production_weight": p_w,
                        "simulated_weight": s_w,
                        "delta": None,
                        "reason": "non_numeric_weight",
                    }
                )
                continue
            delta = abs(p_val - s_val)
            if delta > bound:
                divergences.append(
                    {
                        "index": index,
                        "title": str(p.get("title") or s.get("title") or ""),
                        "production_weight": p_val,
                        "simulated_weight": s_val,
                        "delta": delta,
                        "tolerance": bound,
                        "reason": REASON_WEIGHT_SIMULATION_DIVERGENCE,
                    }
                )

        result = {
            "diverged": bool(divergences),
            "divergence_count": len(divergences),
            "tolerance": bound,
            "divergences": divergences,
            "reason": (
                REASON_WEIGHT_SIMULATION_DIVERGENCE
                if divergences
                else "weight_simulation_consistent"
            ),
        }
        self._last_simulation_divergence = result
        if divergences:
            logger.warning(
                "policy_weight_simulation_divergence count=%s tolerance=%s",
                len(divergences),
                bound,
            )
        return result

    def apply_to_recommendations(
        self,
        student_id: str | int,
        recommendations: list[dict],
        *,
        advisory: Any | None = None,
        policy: RecommendationPolicy | None = None,
    ) -> list[dict]:
        """Consult policy and attach explainability; optionally apply weight.

        Ranking remains unchanged unless ``weighting_enabled`` and a weight
        application is resolved. When the policy feature flag is OFF,
        student-facing output is left untouched.
        """
        if not self._enabled and not self._weighting_enabled:
            self.resolve(
                student_id=str(student_id),
                advisory=advisory,
                policy=policy,
                feature_flag_enabled=False,
            )
            return recommendations

        result = list(recommendations)
        if self._enabled:
            decision = self.resolve_for_recommendation(
                student_id, advisory=advisory, policy=policy
            )
            result = self.attach_explainability(result, decision)

        if self._weighting_enabled:
            result = self.apply_weight_to_recommendations(
                student_id,
                result,
                advisory=advisory,
                policy=policy,
            )
        return result


def build_recommendation_policy_engine(
    *,
    enabled: bool,
    weighting_enabled: bool = False,
    policy: RecommendationPolicy | None = None,
    now: datetime | None = None,
    environ: Mapping[str, str] | None = None,
) -> RecommendationPolicyEngine | None:
    """DI helper — construct engine when policy and/or weighting is ON."""
    if not enabled and not weighting_enabled:
        return None
    if policy is not None:
        active_policy = policy
    elif weighting_enabled:
        active_policy = resolve_weighting_policy(environ=environ)
    else:
        active_policy = resolve_recommendation_policy(environ=environ)
    return RecommendationPolicyEngine(
        enabled=bool(enabled) or bool(weighting_enabled),
        weighting_enabled=bool(weighting_enabled),
        policy=active_policy,
        now=now,
    )


__all__ = [
    "ENGINE_ID",
    "ENGINE_VERSION",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "RecommendationPolicyEngine",
    "build_recommendation_policy_engine",
    "resolve_recommendation_policy",
    "resolve_weighting_policy",
    "student_in_weight_rollout",
]
