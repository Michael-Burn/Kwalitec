"""Controlled Advisory Activation applicator for Runtime A (P3-MS001).

Applies the single approved Evidence Advisory field to production
recommendations when the Runtime Policy Evaluator allows it.

Influence is intentionally minimal and fully explainable:

- Annotate recommendation ``reason`` with the factual
  ``consistency_summary`` observation.
- Never change priority, title, category, or ranking order.
- Record activation / rejection explainability on every evaluated path.

Simulation comparison remains available via DecisionSimulationService.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import datetime
from typing import Any

from .contracts import (
    APPROVED_ADVISORY_FIELD_CONSISTENCY,
    AUTHORITY_RUNTIME_A,
    CONTROLLED_ADVISORY_VERSION,
    DEFAULT_APPROVED_FIELD,
    DEFAULT_MAX_AGE_HOURS,
    DEFAULT_ROLLOUT_PERCENTAGE,
    REASON_FLAG_OFF,
    AdvisoryActivationDecision,
    AdvisoryPolicy,
    ControlledAdvisoryExplainability,
    build_default_advisory_policy,
)
from .policy_evaluator import ControlledAdvisoryPolicyEvaluator

logger = logging.getLogger(__name__)

SERVICE_ID = "controlled_advisory_activation"
SOURCE_SERVICE = "controlled_advisory"
ACTIVATION_KEY = "advisory_activation"


def _env_int(name: str, default: int, *, environ: Mapping[str, str] | None) -> int:
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return default


def resolve_controlled_advisory_policy(
    *,
    environ: Mapping[str, str] | None = None,
) -> AdvisoryPolicy:
    """Resolve AdvisoryPolicy from environment (safe defaults)."""
    rollout = _env_int(
        "KWALITEC_CONTROLLED_ADVISORY_ROLLOUT_PERCENTAGE",
        DEFAULT_ROLLOUT_PERCENTAGE,
        environ=environ,
    )
    max_age = _env_int(
        "KWALITEC_CONTROLLED_ADVISORY_MAX_AGE_HOURS",
        DEFAULT_MAX_AGE_HOURS,
        environ=environ,
    )
    env = environ if environ is not None else os.environ
    effective_from = (
        env.get("KWALITEC_CONTROLLED_ADVISORY_EFFECTIVE_FROM") or ""
    ).strip()
    return build_default_advisory_policy(
        rollout_percentage=rollout,
        effective_from=effective_from or None,
        max_age_hours=max_age,
        enabled_field=DEFAULT_APPROVED_FIELD,
    )


def _consistency_summary(advisory: Any) -> Mapping[str, Any] | None:
    if advisory is None:
        return None
    if hasattr(advisory, "consistency_summary"):
        summary = advisory.consistency_summary
        if hasattr(summary, "to_canonical_dict"):
            return summary.to_canonical_dict()
        if isinstance(summary, Mapping):
            return dict(summary)
        return None
    if isinstance(advisory, Mapping):
        raw = advisory.get("consistency_summary")
        if isinstance(raw, Mapping):
            return dict(raw)
    return None


def _annotate_reason(reason: str, consistency: Mapping[str, Any]) -> str:
    """Minimal factual annotation — no ranking / priority changes."""
    streak = consistency.get("active_streak", 0)
    try:
        streak_int = int(streak)
    except (TypeError, ValueError):
        streak_int = 0
    source = str(consistency.get("source_description") or "").strip()
    note = (
        "Evidence advisory (consistency_summary): observed active streak "
        f"of {streak_int} day(s)."
    )
    if source:
        note = f"{note} {source}"
    base = (reason or "").strip()
    return f"{base} | {note}".strip(" |") if base else note


def explainability_from_decision(
    decision: AdvisoryActivationDecision,
) -> ControlledAdvisoryExplainability:
    """Map an activation decision to a recommendation explainability record."""
    if decision.allowed:
        return ControlledAdvisoryExplainability(
            activated=True,
            advisory_field_used=decision.advisory_field,
            policy_version=decision.policy_version,
            activation_reason=decision.reason,
            evidence_provenance=dict(decision.evidence_provenance),
            advisory_id=decision.advisory_id,
            policy_id=decision.policy_id,
            authority=AUTHORITY_RUNTIME_A,
        )
    return ControlledAdvisoryExplainability(
        activated=False,
        policy_version=decision.policy_version,
        rejection_reason=decision.reason,
        evidence_provenance=dict(decision.evidence_provenance),
        advisory_id=decision.advisory_id,
        policy_id=decision.policy_id,
        authority=AUTHORITY_RUNTIME_A,
    )


class ControlledAdvisoryActivation:
    """Runtime A applicator for the single approved advisory field.

    Rules:
    - Consume only the policy-approved field when evaluator allows.
    - Ignore all other advisory inputs.
    - Influence must remain minimal (rationale annotation only).
    - Every activation / rejection must be explainable.
    - Disabling the feature flag restores prior Runtime A behaviour.
    """

    SERVICE_ID = SERVICE_ID
    SERVICE_VERSION = CONTROLLED_ADVISORY_VERSION
    APPROVED_FIELD = APPROVED_ADVISORY_FIELD_CONSISTENCY

    def __init__(
        self,
        *,
        enabled: bool = True,
        policy: AdvisoryPolicy | None = None,
        evaluator: ControlledAdvisoryPolicyEvaluator | None = None,
        now: datetime | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._policy = policy or build_default_advisory_policy()
        self._evaluator = evaluator or ControlledAdvisoryPolicyEvaluator(
            enabled=self._enabled,
            policy=self._policy,
            now=now,
        )
        self._last_decision: AdvisoryActivationDecision | None = None
        self._last_explainability: ControlledAdvisoryExplainability | None = None

    @property
    def service_id(self) -> str:
        return self.SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def policy(self) -> AdvisoryPolicy:
        return self._policy

    @property
    def evaluator(self) -> ControlledAdvisoryPolicyEvaluator:
        return self._evaluator

    @property
    def last_decision(self) -> AdvisoryActivationDecision | None:
        return self._last_decision

    @property
    def last_explainability(self) -> ControlledAdvisoryExplainability | None:
        return self._last_explainability

    def evaluate(
        self,
        student_id: str | int,
        *,
        advisory: Any | None = None,
    ) -> AdvisoryActivationDecision:
        """Evaluate whether activation is permitted (no recommendation I/O)."""
        if not self._enabled:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_FLAG_OFF,
                student_id=str(student_id).strip(),
                feature_flag_enabled=False,
                policy_id=self._policy.policy_id,
                policy_version=self._policy.policy_version,
            )
            self._last_decision = decision
            self._last_explainability = explainability_from_decision(decision)
            return decision
        decision = self._evaluator.evaluate(
            student_id=str(student_id),
            advisory=advisory,
            policy=self._policy,
            feature_flag_enabled=True,
        )
        self._last_decision = decision
        self._last_explainability = explainability_from_decision(decision)
        return decision

    def apply_to_recommendations(
        self,
        student_id: str | int,
        recommendations: Sequence[Mapping[str, Any]] | None,
        *,
        advisory: Any | None = None,
    ) -> list[dict[str, Any]]:
        """Apply controlled advisory influence when allowed.

        Returns a new list of recommendation dicts. Never mutates the input
        sequence. When denied or disabled, recommendations are returned
        unchanged except for optional explainability attachment when the
        service is enabled.
        """
        source = list(recommendations or ())
        copies: list[dict[str, Any]] = [deepcopy(dict(item)) for item in source]

        if not self._enabled:
            # Rollback path — identical student-facing payload, no metadata.
            return copies

        decision = self.evaluate(student_id, advisory=advisory)
        explainability = explainability_from_decision(decision)
        self._last_explainability = explainability
        payload = explainability.to_canonical_dict()

        if not decision.allowed:
            for item in copies:
                item[ACTIVATION_KEY] = dict(payload)
            logger.debug(
                "controlled_advisory_rejected student_id=%s reason=%s",
                str(student_id).strip(),
                decision.reason,
            )
            return copies

        consistency = _consistency_summary(advisory)
        if consistency is None:
            # Defensive: evaluator should have denied; treat as no-op annotate.
            for item in copies:
                item[ACTIVATION_KEY] = dict(payload)
            return copies

        for item in copies:
            reason = str(item.get("reason") or item.get("rationale") or "")
            item["reason"] = _annotate_reason(reason, consistency)
            item[ACTIVATION_KEY] = dict(payload)

        logger.debug(
            "controlled_advisory_activated student_id=%s field=%s "
            "policy_version=%s count=%s",
            str(student_id).strip(),
            decision.advisory_field,
            decision.policy_version,
            len(copies),
        )
        return copies


def build_controlled_advisory_activation(
    *,
    enabled: bool,
    policy: AdvisoryPolicy | None = None,
    evaluator: ControlledAdvisoryPolicyEvaluator | None = None,
    environ: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> ControlledAdvisoryActivation | None:
    """DI helper — construct activation only when ENABLE_CONTROLLED_ADVISORY is ON."""
    if not enabled:
        return None
    active_policy = policy or resolve_controlled_advisory_policy(environ=environ)
    active_evaluator = evaluator or ControlledAdvisoryPolicyEvaluator(
        enabled=True,
        policy=active_policy,
        now=now,
    )
    return ControlledAdvisoryActivation(
        enabled=True,
        policy=active_policy,
        evaluator=active_evaluator,
        now=now,
    )


__all__ = [
    "ACTIVATION_KEY",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "ControlledAdvisoryActivation",
    "build_controlled_advisory_activation",
    "explainability_from_decision",
    "resolve_controlled_advisory_policy",
]
