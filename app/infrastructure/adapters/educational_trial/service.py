"""Educational Effectiveness Trial Service (P4-MS001).

Configures controlled trials, assigns deterministic cohorts, collects
operational metrics, and produces immutable trial summaries for educational
review.

Compares baseline recommendations with policy-weighted recommendations under
controlled rollout. Does not expand advisory fields, infer mastery, mutate
Adaptive / Recovery / Strategy, or autonomously update policy.
"""

from __future__ import annotations

import hashlib
import logging
import os
from collections.abc import Mapping, Sequence
from typing import Any

from .cohort import assign_cohort
from .contracts import (
    APPROVED_ADVISORY_FIELD,
    AUTHORITY_EDUCATIONAL_TRIAL,
    COHORT_BASELINE,
    COHORT_TREATMENT,
    COHORT_UNASSIGNED,
    DEFAULT_POLICY_VERSION,
    DEFAULT_ROLLOUT_SALT,
    DEFAULT_SUCCESS_METRICS,
    DEFAULT_TRIAL_ID,
    EDUCATIONAL_TRIAL_VERSION,
    INVALID_STATE,
    METRIC_MISSION_COMPLETION,
    METRIC_POLICY_ACTIVATION,
    METRIC_RECOMMENDATION_ACCEPTANCE,
    METRIC_REFLECTION_COMPLETION,
    METRIC_STUDY_SESSION_COMPLETION,
    OPERATIONAL_SUCCESS_METRICS,
    TRIAL_STATUS_ACTIVE,
    TRIAL_STATUS_DRAFT,
    UNAVAILABLE,
    ActivationStatistics,
    CohortAssignment,
    CohortStatistics,
    EducationalTrial,
    EducationalTrialResult,
    TrialMetricObservation,
    TrialMetrics,
    TrialSummary,
    serialize_canonical,
    validate_educational_trial,
)

logger = logging.getLogger(__name__)

SERVICE_ID = "educational_trial_service"
SOURCE_SERVICE = "educational_trial"

DEFAULT_OBSERVATION_WINDOW = "trial_window"


def _env_int(
    name: str,
    default: int,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    env = environ if environ is not None else os.environ
    raw = env.get(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return default


def resolve_default_trial(
    *,
    environ: Mapping[str, str] | None = None,
) -> EducationalTrial:
    """Resolve default EducationalTrial configuration from environment."""
    env = environ if environ is not None else os.environ
    status = (env.get("KWALITEC_EDUCATIONAL_TRIAL_STATUS") or "").strip()
    if not status:
        status = TRIAL_STATUS_ACTIVE
    return EducationalTrial(
        trial_id=(
            env.get("KWALITEC_EDUCATIONAL_TRIAL_ID") or DEFAULT_TRIAL_ID
        ).strip(),
        policy_version=(
            env.get("KWALITEC_EDUCATIONAL_TRIAL_POLICY_VERSION")
            or DEFAULT_POLICY_VERSION
        ).strip(),
        rollout_percentage=_env_int(
            "KWALITEC_EDUCATIONAL_TRIAL_ROLLOUT_PERCENTAGE",
            0,
            environ=environ,
        ),
        advisory_field=APPROVED_ADVISORY_FIELD,
        start_date=(
            env.get("KWALITEC_EDUCATIONAL_TRIAL_START_DATE") or ""
        ).strip(),
        end_date=(env.get("KWALITEC_EDUCATIONAL_TRIAL_END_DATE") or "").strip(),
        success_metrics=DEFAULT_SUCCESS_METRICS,
        status=status if status else TRIAL_STATUS_DRAFT,
        rollout_salt=(
            env.get("KWALITEC_EDUCATIONAL_TRIAL_ROLLOUT_SALT")
            or DEFAULT_ROLLOUT_SALT
        ).strip(),
        provenance={
            "source": "environment",
            "service_id": SERVICE_ID,
        },
    )


def deterministic_observation_id(
    *,
    trial_id: str = "",
    metric_name: str = "",
    cohort: str = "",
    recommendation_id: str = "",
    observation_window: str = "",
    generated_at: str | None = None,
    occurred: bool = False,
) -> str:
    """Deterministic observation id from metric material."""
    material = {
        "cohort": (cohort or "").strip(),
        "generated_at": generated_at,
        "metric_name": (metric_name or "").strip(),
        "observation_window": (observation_window or "").strip(),
        "occurred": bool(occurred),
        "recommendation_id": (recommendation_id or "").strip(),
        "trial_id": (trial_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"edtrialobs-{digest}"


def deterministic_summary_id(
    *,
    trial_id: str,
    observation_ids: Sequence[str],
    generated_at: str | None = None,
) -> str:
    """Deterministic trial summary id."""
    material = {
        "generated_at": generated_at,
        "observation_ids": sorted(str(item) for item in observation_ids),
        "trial_id": (trial_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"edtrialsum-{digest}"


def _increment(counts: dict[str, int], key: str, amount: int = 1) -> None:
    label = (key or "").strip() or "unknown"
    counts[label] = counts.get(label, 0) + max(0, int(amount))


class EducationalTrialService:
    """Operate a Controlled Educational Effectiveness Trial.

    Rules:
    - MAY configure an immutable EducationalTrial
    - MAY assign deterministic baseline / treatment cohorts
    - MAY authorise policy weighting only for treatment cohorts
    - MAY collect operational metrics (no mastery inference)
    - MAY produce immutable TrialSummary artefacts
    - MUST NEVER expand advisory fields beyond consistency_summary
    - MUST NEVER modify Adaptive / Recovery / Strategy / AI coaching
    - MUST leave Runtime A as sole educational authority
    """

    SERVICE_VERSION = "1.0.0-p4.ms001"

    def __init__(
        self,
        *,
        enabled: bool = True,
        trial: EducationalTrial | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._trial = trial if trial is not None else resolve_default_trial(
            environ=environ
        )
        self._last_result: EducationalTrialResult | None = None
        self._observations: list[TrialMetricObservation] = []
        self._assignments: list[CohortAssignment] = []

    @property
    def service_id(self) -> str:
        return SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def trial(self) -> EducationalTrial:
        return self._trial

    @property
    def last_result(self) -> EducationalTrialResult | None:
        return self._last_result

    @property
    def observations(self) -> tuple[TrialMetricObservation, ...]:
        return tuple(self._observations)

    @property
    def assignments(self) -> tuple[CohortAssignment, ...]:
        return tuple(self._assignments)

    def clear_buffers(self) -> None:
        """Clear in-memory observation / assignment buffers."""
        self._observations.clear()
        self._assignments.clear()

    def configure_trial(self, trial: EducationalTrial) -> EducationalTrialResult:
        """Replace the active immutable trial configuration."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        ok, detail = validate_educational_trial(trial)
        if not ok:
            result = EducationalTrialResult(
                ok=False,
                error_code=INVALID_STATE,
                message=detail,
            )
            self._last_result = result
            return result
        self._trial = trial
        result = EducationalTrialResult(ok=True, trial=trial)
        self._last_result = result
        return result

    def assign_cohort(
        self,
        student_id: str,
        *,
        trial: EducationalTrial | None = None,
        generated_at: str | None = None,
        record: bool = True,
    ) -> EducationalTrialResult:
        """Deterministically assign a student to baseline or treatment."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        active = trial if trial is not None else self._trial
        ok, detail = validate_educational_trial(active)
        if not ok:
            result = EducationalTrialResult(
                ok=False,
                error_code=INVALID_STATE,
                message=detail,
            )
            self._last_result = result
            return result
        assignment = assign_cohort(
            str(student_id),
            active,
            generated_at=generated_at,
            provenance={
                "service_id": self.service_id,
                "service_version": self.SERVICE_VERSION,
                "source_service": SOURCE_SERVICE,
            },
        )
        if record:
            self._assignments.append(assignment)
        result = EducationalTrialResult(
            ok=True, trial=active, assignment=assignment
        )
        self._last_result = result
        return result

    def authorises_policy_weighting(
        self,
        student_id: str,
        *,
        trial: EducationalTrial | None = None,
    ) -> bool:
        """Return True only when trial gate authorises treatment weighting.

        When the service is disabled, returns True so existing policy-weighting
        rollout behaviour is undisturbed (trial gate not interposed).
        """
        if not self._enabled:
            return True
        active = trial if trial is not None else self._trial
        if not active.is_active:
            return False
        assignment = assign_cohort(str(student_id), active)
        return bool(assignment.authorised_for_weighting)

    def record_metric(
        self,
        *,
        metric_name: str,
        cohort: str = COHORT_UNASSIGNED,
        occurred: bool = True,
        count: int = 1,
        recommendation_id: str = "",
        observation_window: str = DEFAULT_OBSERVATION_WINDOW,
        generated_at: str | None = None,
        policy_activated: bool = False,
        provenance: Mapping[str, Any] | None = None,
        observation_id: str | None = None,
        trial: EducationalTrial | None = None,
    ) -> EducationalTrialResult:
        """Collect one operational trial metric observation."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        active = trial if trial is not None else self._trial
        label = (metric_name or "").strip()
        if label not in OPERATIONAL_SUCCESS_METRICS:
            result = EducationalTrialResult(
                ok=False,
                error_code=INVALID_STATE,
                message="metric_name_not_operational",
            )
            self._last_result = result
            return result
        window = (observation_window or DEFAULT_OBSERVATION_WINDOW).strip()
        resolved_id = (observation_id or "").strip() or deterministic_observation_id(
            trial_id=active.trial_id,
            metric_name=label,
            cohort=cohort,
            recommendation_id=recommendation_id,
            observation_window=window,
            generated_at=generated_at,
            occurred=occurred,
        )
        observation = TrialMetricObservation(
            observation_id=resolved_id,
            trial_id=active.trial_id,
            metric_name=label,
            cohort=cohort,
            occurred=occurred,
            count=count,
            recommendation_id=recommendation_id,
            observation_window=window,
            generated_at=generated_at,
            policy_version=active.policy_version,
            policy_activated=policy_activated
            or label == METRIC_POLICY_ACTIVATION,
            provenance={
                "service_id": self.service_id,
                "service_version": self.SERVICE_VERSION,
                "source_service": SOURCE_SERVICE,
                "measurement_version": EDUCATIONAL_TRIAL_VERSION,
                **dict(provenance or {}),
            },
            operational_only=True,
            authority=AUTHORITY_EDUCATIONAL_TRIAL,
            trial_version=EDUCATIONAL_TRIAL_VERSION,
        )
        self._observations.append(observation)
        result = EducationalTrialResult(
            ok=True, trial=active, observation=observation
        )
        self._last_result = result
        logger.debug(
            "educational_trial_metric_recorded trial_id=%s metric=%s cohort=%s",
            active.trial_id,
            label,
            observation.cohort,
        )
        return result

    def record_policy_activation(
        self,
        student_id: str,
        *,
        recommendation_id: str = "",
        generated_at: str | None = None,
        activated: bool = True,
    ) -> EducationalTrialResult:
        """Record whether policy weighting activated for an authorised cohort."""
        assignment_result = self.assign_cohort(
            student_id, generated_at=generated_at, record=True
        )
        if not assignment_result.ok or assignment_result.assignment is None:
            return assignment_result
        assignment = assignment_result.assignment
        return self.record_metric(
            metric_name=METRIC_POLICY_ACTIVATION,
            cohort=assignment.cohort,
            occurred=bool(activated and assignment.authorised_for_weighting),
            recommendation_id=recommendation_id,
            generated_at=generated_at,
            policy_activated=bool(activated and assignment.authorised_for_weighting),
            provenance={
                "student_key": assignment.student_key,
                "authorised_for_weighting": assignment.authorised_for_weighting,
            },
        )

    def aggregate_cohort_statistics(
        self,
        assignments: Sequence[CohortAssignment] | None = None,
        *,
        generated_at: str | None = None,
    ) -> EducationalTrialResult:
        """Aggregate cohort membership statistics."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(assignments) if assignments is not None else self.assignments
        for item in cohort:
            if not isinstance(item, CohortAssignment):
                result = EducationalTrialResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="assignments must contain CohortAssignment values",
                )
                self._last_result = result
                return result
        statistics = self._compute_cohort_statistics(
            cohort, generated_at=generated_at
        )
        result = EducationalTrialResult(
            ok=True, trial=self._trial, cohort_statistics=statistics
        )
        self._last_result = result
        return result

    def aggregate_activation_statistics(
        self,
        observations: Sequence[TrialMetricObservation] | None = None,
        *,
        generated_at: str | None = None,
    ) -> EducationalTrialResult:
        """Aggregate policy activation / metric count statistics."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        cohort = (
            tuple(observations) if observations is not None else self.observations
        )
        for item in cohort:
            if not isinstance(item, TrialMetricObservation):
                result = EducationalTrialResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="observations must contain TrialMetricObservation values",
                )
                self._last_result = result
                return result
        statistics = self._compute_activation_statistics(
            cohort, generated_at=generated_at
        )
        result = EducationalTrialResult(
            ok=True, trial=self._trial, activation_statistics=statistics
        )
        self._last_result = result
        return result

    def aggregate_metrics(
        self,
        observations: Sequence[TrialMetricObservation] | None = None,
        *,
        generated_at: str | None = None,
    ) -> EducationalTrialResult:
        """Aggregate operational TrialMetrics from observations."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        cohort = (
            tuple(observations) if observations is not None else self.observations
        )
        for item in cohort:
            if not isinstance(item, TrialMetricObservation):
                result = EducationalTrialResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="observations must contain TrialMetricObservation values",
                )
                self._last_result = result
                return result
        metrics = self._compute_trial_metrics(cohort, generated_at=generated_at)
        result = EducationalTrialResult(
            ok=True, trial=self._trial, metrics=metrics
        )
        self._last_result = result
        return result

    def generate_summary(
        self,
        *,
        observations: Sequence[TrialMetricObservation] | None = None,
        assignments: Sequence[CohortAssignment] | None = None,
        generated_at: str | None = None,
        notes: Sequence[str] | None = None,
        trial: EducationalTrial | None = None,
    ) -> EducationalTrialResult:
        """Generate an immutable TrialSummary for educational review."""
        if not self._enabled:
            result = EducationalTrialResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_EDUCATIONAL_TRIALS is OFF",
            )
            self._last_result = result
            return result
        active = trial if trial is not None else self._trial
        obs = tuple(observations) if observations is not None else self.observations
        assigns = (
            tuple(assignments) if assignments is not None else self.assignments
        )
        for item in obs:
            if not isinstance(item, TrialMetricObservation):
                result = EducationalTrialResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="observations must contain TrialMetricObservation values",
                )
                self._last_result = result
                return result
        for item in assigns:
            if not isinstance(item, CohortAssignment):
                result = EducationalTrialResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="assignments must contain CohortAssignment values",
                )
                self._last_result = result
                return result

        metrics = self._compute_trial_metrics(obs, generated_at=generated_at)
        activation = self._compute_activation_statistics(
            obs, generated_at=generated_at
        )
        cohort_stats = self._compute_cohort_statistics(
            assigns, generated_at=generated_at
        )
        summary_notes = tuple(str(item) for item in (notes or ()))
        if not summary_notes:
            summary_notes = (
                (
                    "Operational educational effectiveness trial only — "
                    "Runtime A remains sole educational authority."
                ),
                "No mastery or examination success inferred.",
                "Advisory field locked to consistency_summary.",
                (
                    "Await architecture review before expanding advisory "
                    "influence beyond consistency_summary."
                ),
            )
        summary = TrialSummary(
            summary_id=deterministic_summary_id(
                trial_id=active.trial_id,
                observation_ids=[item.observation_id for item in obs],
                generated_at=generated_at,
            ),
            trial=active,
            cohort_statistics=cohort_stats,
            activation_statistics=activation,
            metrics=metrics,
            observations=obs,
            observation_period_start=active.start_date,
            observation_period_end=active.end_date,
            notes=summary_notes,
            generated_at=generated_at,
            operational_only=True,
        )
        result = EducationalTrialResult(
            ok=True,
            trial=active,
            cohort_statistics=cohort_stats,
            activation_statistics=activation,
            metrics=metrics,
            summary=summary,
        )
        self._last_result = result
        return result

    def _compute_cohort_statistics(
        self,
        assignments: Sequence[CohortAssignment],
        *,
        generated_at: str | None = None,
    ) -> CohortStatistics:
        by_cohort: dict[str, int] = {}
        baseline = treatment = unassigned = 0
        for item in assignments:
            _increment(by_cohort, item.cohort)
            if item.cohort == COHORT_BASELINE:
                baseline += 1
            elif item.cohort == COHORT_TREATMENT:
                treatment += 1
            else:
                unassigned += 1
        return CohortStatistics(
            baseline_count=baseline,
            treatment_count=treatment,
            unassigned_count=unassigned,
            total_assignments=len(assignments),
            by_cohort=by_cohort,
            generated_at=generated_at,
            operational_only=True,
        )

    def _compute_activation_statistics(
        self,
        observations: Sequence[TrialMetricObservation],
        *,
        generated_at: str | None = None,
    ) -> ActivationStatistics:
        activation_by_cohort: dict[str, int] = {}
        metric_counts: dict[str, int] = {}
        metric_by_cohort: dict[str, dict[str, int]] = {}
        policy_activation_count = 0
        for item in observations:
            amount = item.count if item.occurred else 0
            _increment(metric_counts, item.metric_name, amount)
            cohort_bucket = metric_by_cohort.setdefault(item.cohort, {})
            _increment(cohort_bucket, item.metric_name, amount)
            if item.policy_activated or (
                item.metric_name == METRIC_POLICY_ACTIVATION and item.occurred
            ):
                policy_activation_count += max(1, amount)
                _increment(activation_by_cohort, item.cohort, max(1, amount))
        return ActivationStatistics(
            total_observations=len(observations),
            policy_activation_count=policy_activation_count,
            activation_by_cohort=activation_by_cohort,
            metric_counts=metric_counts,
            metric_counts_by_cohort=metric_by_cohort,
            generated_at=generated_at,
            operational_only=True,
        )

    def _compute_trial_metrics(
        self,
        observations: Sequence[TrialMetricObservation],
        *,
        generated_at: str | None = None,
    ) -> TrialMetrics:
        count = len(observations)
        if count == 0:
            return TrialMetrics(
                observation_count=0,
                generated_at=generated_at,
                operational_only=True,
            )

        def _rate(metric: str, cohort: str | None = None) -> float:
            relevant = [
                item
                for item in observations
                if item.metric_name == metric
                and (cohort is None or item.cohort == cohort)
            ]
            if not relevant:
                return 0.0
            hits = sum(1 for item in relevant if item.occurred)
            return hits / len(relevant)

        rates_by_cohort: dict[str, dict[str, float]] = {}
        for cohort in (COHORT_BASELINE, COHORT_TREATMENT, COHORT_UNASSIGNED):
            if any(item.cohort == cohort for item in observations):
                rates_by_cohort[cohort] = {
                    METRIC_RECOMMENDATION_ACCEPTANCE: _rate(
                        METRIC_RECOMMENDATION_ACCEPTANCE, cohort
                    ),
                    METRIC_MISSION_COMPLETION: _rate(
                        METRIC_MISSION_COMPLETION, cohort
                    ),
                    METRIC_STUDY_SESSION_COMPLETION: _rate(
                        METRIC_STUDY_SESSION_COMPLETION, cohort
                    ),
                    METRIC_REFLECTION_COMPLETION: _rate(
                        METRIC_REFLECTION_COMPLETION, cohort
                    ),
                    METRIC_POLICY_ACTIVATION: _rate(
                        METRIC_POLICY_ACTIVATION, cohort
                    ),
                }

        return TrialMetrics(
            observation_count=count,
            recommendation_acceptance_rate=_rate(METRIC_RECOMMENDATION_ACCEPTANCE),
            mission_completion_rate=_rate(METRIC_MISSION_COMPLETION),
            study_session_completion_rate=_rate(METRIC_STUDY_SESSION_COMPLETION),
            reflection_completion_rate=_rate(METRIC_REFLECTION_COMPLETION),
            policy_activation_frequency=_rate(METRIC_POLICY_ACTIVATION),
            rates_by_cohort=rates_by_cohort,
            generated_at=generated_at,
            operational_only=True,
        )


def build_educational_trial_service(
    *,
    enabled: bool,
    trial: EducationalTrial | None = None,
    environ: Mapping[str, str] | None = None,
) -> EducationalTrialService | None:
    """DI helper — construct only when ENABLE_EDUCATIONAL_TRIALS is ON."""
    if not enabled:
        return None
    return EducationalTrialService(
        enabled=True,
        trial=trial,
        environ=environ,
    )


__all__ = [
    "DEFAULT_OBSERVATION_WINDOW",
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "EducationalTrialService",
    "build_educational_trial_service",
    "deterministic_observation_id",
    "deterministic_summary_id",
    "resolve_default_trial",
]
