"""Advisory Outcome Measurement Service (P3-MS002).

Collects Controlled Advisory Activation rollout outcomes, aggregates
activation statistics, and correlates observed actions with activation.

Reports observations only. Never interprets educational success.
Never modifies Runtime A recommendations. Never influences ranking.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping, Sequence
from typing import Any

from .contracts import (
    ACTION_ACCEPTED,
    ACTION_NOT_OBSERVED,
    ACTIVATION_STATUS_ACTIVATED,
    ACTIVATION_STATUS_FAILED,
    ACTIVATION_STATUS_REJECTED,
    ACTIVATION_STATUS_ROLLED_BACK,
    AUTHORITY_ADVISORY_OUTCOME,
    AUTHORITY_CONTROLLED_ADVISORY,
    COHORT_EXCLUDED,
    COHORT_IN_ROLLOUT,
    COHORT_UNKNOWN,
    INTERACTION_ACTIONS,
    INVALID_STATE,
    OUTCOME_MEASUREMENT_VERSION,
    UNAVAILABLE,
    ActionCorrelation,
    ActivationStatistics,
    AdvisoryOutcome,
    AdvisoryOutcomeResult,
    OutcomeMeasurementSummary,
    RolloutMetrics,
    serialize_canonical,
)

logger = logging.getLogger(__name__)

SERVICE_ID = "advisory_outcome_measurement_service"
SOURCE_SERVICE = "advisory_outcome_measurement"

DEFAULT_OBSERVATION_WINDOW = "session"


def deterministic_outcome_id(
    *,
    recommendation_id: str = "",
    policy_version: str = "",
    advisory_field: str = "",
    activation_status: str = "",
    student_action_observed: str = "",
    observation_window: str = "",
    generated_at: str | None = None,
) -> str:
    """Deterministic outcome id from observation material."""
    material = {
        "activation_status": (activation_status or "").strip(),
        "advisory_field": (advisory_field or "").strip(),
        "generated_at": generated_at,
        "observation_window": (observation_window or "").strip(),
        "policy_version": (policy_version or "").strip(),
        "recommendation_id": (recommendation_id or "").strip(),
        "student_action_observed": (student_action_observed or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"advout-{digest}"


def deterministic_summary_id(
    *,
    outcome_ids: Sequence[str],
    generated_at: str | None = None,
) -> str:
    """Deterministic measurement summary id."""
    material = {
        "generated_at": generated_at,
        "outcome_ids": sorted(str(item) for item in outcome_ids),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"advoutsum-{digest}"


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if value is None:
        return {}
    if hasattr(value, "to_canonical_dict"):
        payload = value.to_canonical_dict()
        return payload if isinstance(payload, Mapping) else {}
    if isinstance(value, Mapping):
        return value
    return {}


def _increment(counts: dict[str, int], key: str) -> None:
    label = (key or "").strip() or "unknown"
    counts[label] = counts.get(label, 0) + 1


def resolve_activation_status(
    *,
    allowed: bool | None = None,
    activation_failed: bool = False,
    rolled_back: bool = False,
    activated: bool | None = None,
    status: str | None = None,
) -> str:
    """Map activation signals to an operational activation_status."""
    if status:
        return str(status).strip()
    if rolled_back:
        return ACTIVATION_STATUS_ROLLED_BACK
    if activation_failed:
        return ACTIVATION_STATUS_FAILED
    if activated is True or allowed is True:
        return ACTIVATION_STATUS_ACTIVATED
    if activated is False or allowed is False:
        return ACTIVATION_STATUS_REJECTED
    return ACTIVATION_STATUS_REJECTED


def resolve_rollout_cohort(
    *,
    in_rollout: bool | None = None,
    cohort: str | None = None,
) -> str:
    """Map rollout membership to an explainability cohort label."""
    if cohort:
        return str(cohort).strip()
    if in_rollout is True:
        return COHORT_IN_ROLLOUT
    if in_rollout is False:
        return COHORT_EXCLUDED
    return COHORT_UNKNOWN


class AdvisoryOutcomeMeasurementService:
    """Measure Controlled Advisory Activation rollout outcomes.

    Rules:
    - MAY collect AdvisoryOutcome observations
    - MAY aggregate ActivationStatistics / RolloutMetrics
    - MAY correlate observed actions with activation status
    - MUST NEVER modify production recommendation outputs
    - MUST NEVER interpret educational success or mastery
    - MUST NOT include personal identifiers on outcome artefacts
    """

    SERVICE_VERSION = "1.0.0-p3.ms002"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self._last_result: AdvisoryOutcomeResult | None = None
        self._outcomes: list[AdvisoryOutcome] = []

    @property
    def service_id(self) -> str:
        return SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def last_result(self) -> AdvisoryOutcomeResult | None:
        return self._last_result

    @property
    def outcomes(self) -> tuple[AdvisoryOutcome, ...]:
        """Operational outcomes accumulated this process (in-memory)."""
        return tuple(self._outcomes)

    def clear_outcomes(self) -> None:
        """Clear in-memory operational outcome buffer."""
        self._outcomes.clear()

    def record_outcome(
        self,
        *,
        policy_version: str = "",
        advisory_field: str = "",
        activation_status: str = ACTIVATION_STATUS_REJECTED,
        recommendation_id: str = "",
        student_action_observed: str = ACTION_NOT_OBSERVED,
        observation_window: str = DEFAULT_OBSERVATION_WINDOW,
        generated_at: str | None = None,
        rollout_cohort: str = COHORT_UNKNOWN,
        activation_decision: str = "",
        provenance: Mapping[str, Any] | None = None,
        outcome_id: str | None = None,
    ) -> AdvisoryOutcomeResult:
        """Collect one rollout outcome observation."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        try:
            outcome = self._build_outcome(
                policy_version=policy_version,
                advisory_field=advisory_field,
                activation_status=activation_status,
                recommendation_id=recommendation_id,
                student_action_observed=student_action_observed,
                observation_window=observation_window,
                generated_at=generated_at,
                rollout_cohort=rollout_cohort,
                activation_decision=activation_decision,
                provenance=provenance,
                outcome_id=outcome_id,
            )
        except Exception as exc:
            logger.warning(
                "advisory_outcome_record_failed error=%s",
                exc,
                exc_info=True,
            )
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=INVALID_STATE,
                message=str(exc) or "advisory outcome record failed",
            )
            self._last_result = result
            return result
        self._outcomes.append(outcome)
        result = AdvisoryOutcomeResult(ok=True, outcome=outcome)
        self._last_result = result
        logger.debug(
            "advisory_outcome_recorded outcome_id=%s status=%s action=%s",
            outcome.outcome_id,
            outcome.activation_status,
            outcome.student_action_observed,
        )
        return result

    def record_from_activation(
        self,
        activation: Any,
        *,
        recommendation_id: str = "",
        student_action_observed: str = ACTION_NOT_OBSERVED,
        observation_window: str = DEFAULT_OBSERVATION_WINDOW,
        generated_at: str | None = None,
        activation_failed: bool = False,
        rolled_back: bool = False,
        extra_provenance: Mapping[str, Any] | None = None,
    ) -> AdvisoryOutcomeResult:
        """Collect an outcome from an activation decision / explainability DTO."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        fields = _activation_record_fields(activation)
        status = resolve_activation_status(
            allowed=fields["allowed"],
            activated=fields["activated"],
            activation_failed=activation_failed,
            rolled_back=rolled_back,
        )
        decision = fields["activation_decision"]
        if rolled_back and not decision:
            decision = "controlled_advisory_rolled_back"
        if activation_failed and not decision:
            decision = "controlled_advisory_activation_failed"
        provenance = {
            **dict(fields["provenance"]),
            **dict(extra_provenance or {}),
            "activation_authority": fields["authority"]
            or AUTHORITY_CONTROLLED_ADVISORY,
            "measurement_version": OUTCOME_MEASUREMENT_VERSION,
            "service_id": self.service_id,
            "service_version": self.SERVICE_VERSION,
            "source_service": SOURCE_SERVICE,
        }
        return self.record_outcome(
            policy_version=fields["policy_version"],
            advisory_field=fields["advisory_field"],
            activation_status=status,
            recommendation_id=recommendation_id or fields["recommendation_id"],
            student_action_observed=student_action_observed,
            observation_window=observation_window,
            generated_at=generated_at or fields["generated_at"],
            rollout_cohort=resolve_rollout_cohort(in_rollout=fields["in_rollout"]),
            activation_decision=decision,
            provenance=provenance,
        )

    def aggregate_activation_statistics(
        self,
        outcomes: Sequence[AdvisoryOutcome] | None = None,
        *,
        generated_at: str | None = None,
    ) -> AdvisoryOutcomeResult:
        """Aggregate activation count statistics from outcomes."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(outcomes) if outcomes is not None else self.outcomes
        for item in cohort:
            if not isinstance(item, AdvisoryOutcome):
                result = AdvisoryOutcomeResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="outcomes must contain AdvisoryOutcome values",
                )
                self._last_result = result
                return result
        statistics = self._compute_activation_statistics(
            cohort, generated_at=generated_at
        )
        result = AdvisoryOutcomeResult(ok=True, activation_statistics=statistics)
        self._last_result = result
        return result

    def correlate_actions(
        self,
        outcomes: Sequence[AdvisoryOutcome] | None = None,
        *,
        generated_at: str | None = None,
    ) -> AdvisoryOutcomeResult:
        """Correlate observed actions with advisory activation status."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(outcomes) if outcomes is not None else self.outcomes
        for item in cohort:
            if not isinstance(item, AdvisoryOutcome):
                result = AdvisoryOutcomeResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="outcomes must contain AdvisoryOutcome values",
                )
                self._last_result = result
                return result
        correlation = self._compute_action_correlation(
            cohort, generated_at=generated_at
        )
        result = AdvisoryOutcomeResult(ok=True, action_correlation=correlation)
        self._last_result = result
        return result

    def aggregate_rollout_metrics(
        self,
        outcomes: Sequence[AdvisoryOutcome] | None = None,
        *,
        generated_at: str | None = None,
    ) -> AdvisoryOutcomeResult:
        """Aggregate operational RolloutMetrics from outcomes."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(outcomes) if outcomes is not None else self.outcomes
        for item in cohort:
            if not isinstance(item, AdvisoryOutcome):
                result = AdvisoryOutcomeResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="outcomes must contain AdvisoryOutcome values",
                )
                self._last_result = result
                return result
        metrics = self._compute_rollout_metrics(cohort, generated_at=generated_at)
        result = AdvisoryOutcomeResult(ok=True, metrics=metrics)
        self._last_result = result
        return result

    def generate_summary(
        self,
        outcomes: Sequence[AdvisoryOutcome] | None = None,
        *,
        generated_at: str | None = None,
        notes: Sequence[str] | None = None,
    ) -> AdvisoryOutcomeResult:
        """Generate an OutcomeMeasurementSummary with metrics and correlations."""
        if not self._enabled:
            result = AdvisoryOutcomeResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_OUTCOME_MEASUREMENT is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(outcomes) if outcomes is not None else self.outcomes
        for item in cohort:
            if not isinstance(item, AdvisoryOutcome):
                result = AdvisoryOutcomeResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="outcomes must contain AdvisoryOutcome values",
                )
                self._last_result = result
                return result
        metrics = self._compute_rollout_metrics(cohort, generated_at=generated_at)
        statistics = self._compute_activation_statistics(
            cohort, generated_at=generated_at
        )
        correlation = self._compute_action_correlation(
            cohort, generated_at=generated_at
        )
        summary_notes = tuple(str(item) for item in (notes or ()))
        if not summary_notes:
            summary_notes = (
                (
                    "Operational outcome measurement only — "
                    "Runtime A behaviour unchanged."
                ),
                "No personal identifiers included in outcome artefacts.",
                (
                    "Rates report behavioural observations; they do not infer "
                    "learning quality."
                ),
                (
                    "Await architecture review before expanding advisory influence "
                    "or enabling automatic optimisation."
                ),
            )
        summary = OutcomeMeasurementSummary(
            summary_id=deterministic_summary_id(
                outcome_ids=[item.outcome_id for item in cohort],
                generated_at=generated_at,
            ),
            metrics=metrics,
            activation_statistics=statistics,
            action_correlation=correlation,
            outcomes=cohort,
            notes=summary_notes,
            generated_at=generated_at,
            operational_only=True,
        )
        result = AdvisoryOutcomeResult(
            ok=True,
            metrics=metrics,
            activation_statistics=statistics,
            action_correlation=correlation,
            summary=summary,
        )
        self._last_result = result
        return result

    def _build_outcome(
        self,
        *,
        policy_version: str,
        advisory_field: str,
        activation_status: str,
        recommendation_id: str,
        student_action_observed: str,
        observation_window: str,
        generated_at: str | None,
        rollout_cohort: str,
        activation_decision: str,
        provenance: Mapping[str, Any] | None,
        outcome_id: str | None,
    ) -> AdvisoryOutcome:
        window = (observation_window or DEFAULT_OBSERVATION_WINDOW).strip()
        decision = (activation_decision or "").strip()
        if not decision:
            decision = f"status:{activation_status or ACTIVATION_STATUS_REJECTED}"
        base_provenance = {
            "measurement_version": OUTCOME_MEASUREMENT_VERSION,
            "service_id": self.service_id,
            "service_version": self.SERVICE_VERSION,
            "source_service": SOURCE_SERVICE,
            **dict(provenance or {}),
        }
        resolved_id = (outcome_id or "").strip() or deterministic_outcome_id(
            recommendation_id=recommendation_id,
            policy_version=policy_version,
            advisory_field=advisory_field,
            activation_status=activation_status,
            student_action_observed=student_action_observed,
            observation_window=window,
            generated_at=generated_at,
        )
        return AdvisoryOutcome(
            outcome_id=resolved_id,
            policy_version=policy_version,
            advisory_field=advisory_field,
            activation_status=activation_status,
            recommendation_id=recommendation_id,
            student_action_observed=student_action_observed,
            observation_window=window,
            generated_at=generated_at,
            rollout_cohort=rollout_cohort,
            activation_decision=decision,
            provenance=base_provenance,
            operational_only=True,
            authority=AUTHORITY_ADVISORY_OUTCOME,
            measurement_version=OUTCOME_MEASUREMENT_VERSION,
        )

    def _compute_activation_statistics(
        self,
        outcomes: Sequence[AdvisoryOutcome],
        *,
        generated_at: str | None = None,
    ) -> ActivationStatistics:
        by_field: dict[str, int] = {}
        by_policy: dict[str, int] = {}
        by_cohort: dict[str, int] = {}
        by_status: dict[str, int] = {}
        activated = rejected = failed = rolled_back = 0
        for item in outcomes:
            _increment(by_field, item.advisory_field)
            _increment(by_policy, item.policy_version)
            _increment(by_cohort, item.rollout_cohort)
            _increment(by_status, item.activation_status)
            if item.activation_status == ACTIVATION_STATUS_ACTIVATED:
                activated += 1
            elif item.activation_status == ACTIVATION_STATUS_REJECTED:
                rejected += 1
            elif item.activation_status == ACTIVATION_STATUS_FAILED:
                failed += 1
            elif item.activation_status == ACTIVATION_STATUS_ROLLED_BACK:
                rolled_back += 1
        return ActivationStatistics(
            total_outcomes=len(outcomes),
            activated_count=activated,
            rejected_count=rejected,
            failed_count=failed,
            rolled_back_count=rolled_back,
            by_advisory_field=by_field,
            by_policy_version=by_policy,
            by_rollout_cohort=by_cohort,
            by_activation_status=by_status,
            generated_at=generated_at,
            operational_only=True,
        )

    def _compute_action_correlation(
        self,
        outcomes: Sequence[AdvisoryOutcome],
        *,
        generated_at: str | None = None,
    ) -> ActionCorrelation:
        activated: dict[str, int] = {}
        rejected: dict[str, int] = {}
        failed: dict[str, int] = {}
        rolled_back: dict[str, int] = {}
        for item in outcomes:
            if item.activation_status == ACTIVATION_STATUS_ACTIVATED:
                _increment(activated, item.student_action_observed)
            elif item.activation_status == ACTIVATION_STATUS_REJECTED:
                _increment(rejected, item.student_action_observed)
            elif item.activation_status == ACTIVATION_STATUS_FAILED:
                _increment(failed, item.student_action_observed)
            elif item.activation_status == ACTIVATION_STATUS_ROLLED_BACK:
                _increment(rolled_back, item.student_action_observed)
        return ActionCorrelation(
            activated_action_counts=activated,
            rejected_action_counts=rejected,
            failed_action_counts=failed,
            rolled_back_action_counts=rolled_back,
            generated_at=generated_at,
            operational_only=True,
        )

    def _compute_rollout_metrics(
        self,
        outcomes: Sequence[AdvisoryOutcome],
        *,
        generated_at: str | None = None,
    ) -> RolloutMetrics:
        count = len(outcomes)
        if count == 0:
            return RolloutMetrics(
                outcome_count=0,
                activation_rate=0.0,
                acceptance_rate=0.0,
                recommendation_interaction_rate=0.0,
                rollback_count=0,
                activation_failures=0,
                rejection_count=0,
                generated_at=generated_at,
                operational_only=True,
            )
        status_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        activated_n = 0
        accepted_among_activated = 0
        interacted_among_activated = 0
        rollback_n = 0
        failed_n = 0
        rejected_n = 0
        for item in outcomes:
            _increment(status_counts, item.activation_status)
            _increment(action_counts, item.student_action_observed)
            if item.activation_status == ACTIVATION_STATUS_ACTIVATED:
                activated_n += 1
                if item.student_action_observed == ACTION_ACCEPTED:
                    accepted_among_activated += 1
                if item.student_action_observed in INTERACTION_ACTIONS:
                    interacted_among_activated += 1
            elif item.activation_status == ACTIVATION_STATUS_ROLLED_BACK:
                rollback_n += 1
            elif item.activation_status == ACTIVATION_STATUS_FAILED:
                failed_n += 1
            elif item.activation_status == ACTIVATION_STATUS_REJECTED:
                rejected_n += 1
        acceptance_rate = (
            accepted_among_activated / activated_n if activated_n else 0.0
        )
        interaction_rate = (
            interacted_among_activated / activated_n if activated_n else 0.0
        )
        return RolloutMetrics(
            outcome_count=count,
            activation_rate=activated_n / count,
            acceptance_rate=acceptance_rate,
            recommendation_interaction_rate=interaction_rate,
            rollback_count=rollback_n,
            activation_failures=failed_n,
            rejection_count=rejected_n,
            activation_status_counts=status_counts,
            action_counts=action_counts,
            generated_at=generated_at,
            operational_only=True,
        )


def _activation_record_fields(activation: Any) -> dict[str, Any]:
    """Extract explainability fields from activation decision / explainability DTOs."""
    payload = _as_mapping(activation)
    allowed = payload.get("allowed")
    activated = payload.get("activated")
    if activated is None and allowed is not None:
        activated = bool(allowed)
    if allowed is None and activated is not None:
        allowed = bool(activated)

    decision = str(
        payload.get("activation_decision")
        or payload.get("activation_reason")
        or payload.get("rejection_reason")
        or payload.get("reason")
        or ""
    ).strip()
    advisory_field = str(
        payload.get("advisory_field")
        or payload.get("advisory_field_used")
        or ""
    ).strip()
    policy_version = str(payload.get("policy_version") or "").strip()
    in_rollout = payload.get("in_rollout")
    if in_rollout is not None:
        in_rollout = bool(in_rollout)
    elif activated is True:
        in_rollout = True

    provenance = dict(payload.get("evidence_provenance") or {})
    nested = payload.get("provenance")
    if isinstance(nested, Mapping):
        provenance = {**provenance, **dict(nested)}
    for key in ("advisory_id", "policy_id", "activation_version"):
        if key in payload and payload[key] not in (None, ""):
            provenance.setdefault(key, payload[key])

    return {
        "activation_decision": decision,
        "activated": activated if activated is None else bool(activated),
        "advisory_field": advisory_field,
        "allowed": allowed if allowed is None else bool(allowed),
        "authority": str(payload.get("authority") or "").strip(),
        "generated_at": (
            str(payload["generated_at"])
            if payload.get("generated_at") is not None
            else None
        ),
        "in_rollout": in_rollout,
        "policy_version": policy_version,
        "provenance": provenance,
        "recommendation_id": str(payload.get("recommendation_id") or "").strip(),
    }


def build_advisory_outcome_measurement_service(
    *,
    enabled: bool,
) -> AdvisoryOutcomeMeasurementService | None:
    """DI helper — construct only when ENABLE_ADVISORY_OUTCOME_MEASUREMENT is ON."""
    if not enabled:
        return None
    return AdvisoryOutcomeMeasurementService(enabled=True)


__all__ = [
    "DEFAULT_OBSERVATION_WINDOW",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "AdvisoryOutcomeMeasurementService",
    "build_advisory_outcome_measurement_service",
    "deterministic_outcome_id",
    "deterministic_summary_id",
    "resolve_activation_status",
    "resolve_rollout_cohort",
]
