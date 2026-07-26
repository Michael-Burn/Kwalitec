"""Runtime Policy Evaluator for Controlled Advisory Activation (P3-MS001).

Decides whether Runtime A is permitted to consume the single approved
Evidence Advisory field. Responsibilities:

- validate policy
- validate feature flags
- validate advisory freshness
- return explicit allow/deny decision

The evaluator must never produce recommendations.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from .contracts import (
    APPROVED_ADVISORY_FIELDS,
    AUTHORITY_CONTROLLED_ADVISORY,
    CONTROLLED_ADVISORY_VERSION,
    DEFAULT_MAX_AGE_HOURS,
    DEFAULT_ROLLOUT_SALT,
    REASON_ADVISORY_FIELD_MISSING,
    REASON_ADVISORY_INVALID,
    REASON_ADVISORY_MISSING,
    REASON_ADVISORY_STALE,
    REASON_ALLOWED,
    REASON_EFFECTIVE_FROM_FUTURE,
    REASON_FLAG_OFF,
    REASON_POLICY_INVALID,
    REASON_ROLLOUT_EXCLUDED,
    AdvisoryActivationDecision,
    AdvisoryPolicy,
    validate_advisory_policy,
)

logger = logging.getLogger(__name__)

EVALUATOR_ID = "controlled_advisory_policy_evaluator"
EVALUATOR_VERSION = CONTROLLED_ADVISORY_VERSION


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


def student_in_rollout(
    student_id: str,
    *,
    rollout_percentage: int,
    salt: str = DEFAULT_ROLLOUT_SALT,
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


def _advisory_provenance(advisory: Any) -> dict[str, Any]:
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
    if isinstance(advisory, dict):
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


def _field_present(advisory: Any, field_name: str) -> bool:
    if advisory is None:
        return False
    if hasattr(advisory, field_name):
        value = getattr(advisory, field_name)
        return value is not None
    if isinstance(advisory, dict):
        return field_name in advisory and advisory[field_name] is not None
    return False


class ControlledAdvisoryPolicyEvaluator:
    """Allow/deny evaluator for controlled advisory consumption.

    Never ranks topics, never builds recommendations, never writes state.
    """

    EVALUATOR_ID = EVALUATOR_ID
    EVALUATOR_VERSION = EVALUATOR_VERSION

    def __init__(
        self,
        *,
        enabled: bool = True,
        policy: AdvisoryPolicy | None = None,
        now: datetime | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._policy = policy
        self._now = now
        self._last_decision: AdvisoryActivationDecision | None = None

    @property
    def evaluator_id(self) -> str:
        return self.EVALUATOR_ID

    @property
    def evaluator_version(self) -> str:
        return self.EVALUATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def policy(self) -> AdvisoryPolicy | None:
        return self._policy

    @property
    def last_decision(self) -> AdvisoryActivationDecision | None:
        return self._last_decision

    def _clock(self) -> datetime:
        if self._now is not None:
            return self._now if self._now.tzinfo else self._now.replace(
                tzinfo=UTC
            )
        return datetime.now(UTC)

    def evaluate(
        self,
        *,
        student_id: str,
        advisory: Any | None = None,
        policy: AdvisoryPolicy | None = None,
        feature_flag_enabled: bool | None = None,
    ) -> AdvisoryActivationDecision:
        """Return an explicit allow/deny decision.

        Args:
            student_id: Runtime A student / user id.
            advisory: EvidenceAdvisory DTO or mapping (optional).
            policy: Policy override; defaults to evaluator policy.
            feature_flag_enabled: Override for ENABLE_CONTROLLED_ADVISORY.
                Defaults to ``self.is_enabled()``.
        """
        sid = (student_id or "").strip()
        flag_on = (
            self._enabled
            if feature_flag_enabled is None
            else bool(feature_flag_enabled)
        )
        active_policy = policy if policy is not None else self._policy

        if not flag_on:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_FLAG_OFF,
                student_id=sid,
                feature_flag_enabled=False,
            )
            self._last_decision = decision
            return decision

        if active_policy is None:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_POLICY_INVALID,
                student_id=sid,
                feature_flag_enabled=True,
            )
            self._last_decision = decision
            return decision

        policy_error = validate_advisory_policy(active_policy)
        if policy_error is not None:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=policy_error,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
            )
            self._last_decision = decision
            return decision

        field_name = active_policy.enabled_field or ""
        assert field_name in APPROVED_ADVISORY_FIELDS

        effective_from = _parse_iso(active_policy.effective_from)
        now = self._clock()
        if effective_from is not None and now < effective_from:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_EFFECTIVE_FROM_FUTURE,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
            )
            self._last_decision = decision
            return decision

        conditions = dict(active_policy.activation_conditions or {})
        salt = str(conditions.get("rollout_salt") or DEFAULT_ROLLOUT_SALT)
        in_rollout = student_in_rollout(
            sid,
            rollout_percentage=active_policy.rollout_percentage,
            salt=salt,
        )
        if not in_rollout:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ROLLOUT_EXCLUDED,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=False,
            )
            self._last_decision = decision
            return decision

        require_advisory = bool(conditions.get("require_advisory_available", True))
        if advisory is None:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_MISSING,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
            )
            self._last_decision = decision
            return decision

        provenance = _advisory_provenance(advisory)
        advisory_id = str(provenance.get("advisory_id") or "")
        availability = getattr(advisory, "availability", None)
        if availability is None and isinstance(advisory, dict):
            availability = advisory.get("availability")
        if availability is not None and str(availability).strip().lower() not in (
            "",
            "available",
        ):
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_INVALID,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
                advisory_id=advisory_id,
                evidence_provenance=provenance,
            )
            self._last_decision = decision
            return decision

        generated_at = provenance.get("generated_at")
        if hasattr(advisory, "generated_at") and not generated_at:
            generated_at = getattr(advisory, "generated_at", None)
        max_age_hours = conditions.get("max_age_hours", DEFAULT_MAX_AGE_HOURS)
        try:
            max_age = int(max_age_hours)
        except (TypeError, ValueError):
            max_age = DEFAULT_MAX_AGE_HOURS
        if max_age < 0:
            max_age = DEFAULT_MAX_AGE_HOURS

        parsed_generated = _parse_iso(
            generated_at if isinstance(generated_at, str) else None
        )
        if parsed_generated is None:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_STALE,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
                advisory_id=advisory_id,
                evidence_provenance=provenance,
            )
            self._last_decision = decision
            return decision
        if now - parsed_generated > timedelta(hours=max_age):
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_STALE,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
                advisory_id=advisory_id,
                evidence_provenance=provenance,
            )
            self._last_decision = decision
            return decision

        require_field = bool(conditions.get("require_approved_field_present", True))
        if require_field and not _field_present(advisory, field_name):
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_FIELD_MISSING,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
                advisory_id=advisory_id,
                evidence_provenance=provenance,
            )
            self._last_decision = decision
            return decision

        if require_advisory and not advisory_id:
            decision = AdvisoryActivationDecision(
                allowed=False,
                reason=REASON_ADVISORY_INVALID,
                policy_id=active_policy.policy_id,
                policy_version=active_policy.policy_version,
                advisory_field=field_name,
                student_id=sid,
                feature_flag_enabled=True,
                rollout_percentage=active_policy.rollout_percentage,
                in_rollout=True,
                evidence_provenance=provenance,
            )
            self._last_decision = decision
            return decision

        decision = AdvisoryActivationDecision(
            allowed=True,
            reason=REASON_ALLOWED,
            policy_id=active_policy.policy_id,
            policy_version=active_policy.policy_version,
            advisory_field=field_name,
            student_id=sid,
            feature_flag_enabled=True,
            rollout_percentage=active_policy.rollout_percentage,
            in_rollout=True,
            advisory_id=advisory_id,
            evidence_provenance=provenance,
            authority=AUTHORITY_CONTROLLED_ADVISORY,
        )
        self._last_decision = decision
        logger.debug(
            "controlled_advisory_allowed student_id=%s field=%s policy=%s",
            sid,
            field_name,
            active_policy.policy_version,
        )
        return decision


def build_controlled_advisory_policy_evaluator(
    *,
    enabled: bool,
    policy: AdvisoryPolicy | None = None,
    now: datetime | None = None,
) -> ControlledAdvisoryPolicyEvaluator | None:
    """DI helper — construct evaluator only when ENABLE_CONTROLLED_ADVISORY is ON."""
    if not enabled:
        return None
    return ControlledAdvisoryPolicyEvaluator(
        enabled=True,
        policy=policy,
        now=now,
    )


__all__ = [
    "EVALUATOR_ID",
    "EVALUATOR_VERSION",
    "ControlledAdvisoryPolicyEvaluator",
    "build_controlled_advisory_policy_evaluator",
    "student_in_rollout",
]
