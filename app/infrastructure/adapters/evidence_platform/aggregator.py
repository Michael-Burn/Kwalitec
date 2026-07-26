"""Deterministic analytics aggregation (MS-006 E4).

Aggregates immutable PolicyEvaluation, ExperimentObservation, and
EvidenceRecord inputs into AnalyticsSummary drafts. Never mutates inputs,
never promotes policies, never changes educational behaviour.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    ANALYTICS_AUDIENCE_GOVERNANCE,
    ANALYTICS_AUDIENCES,
    ANALYTICS_GRAINS,
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    CLAIM_LEARNING_DEPTH,
    CLAIM_LEARNING_SIGNAL,
    CLAIM_ORGANISATION,
    EVIDENCE_VERSION_E4,
    GATE_FAILED,
    GATE_INELIGIBLE,
    GATE_PASSED,
    GRAIN_SYSTEM,
    TREND_DIRECTION_NOT_ESTIMABLE,
    AnalyticsSummary,
    ConfidenceSummaryProjection,
    EvidenceRecord,
    ExperimentObservation,
    ExperimentSummaryProjection,
    MetricPoint,
    MetricSeries,
    PolicyEvaluation,
    PolicySummaryProjection,
    ScorecardSlice,
    TrendMetadata,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.provenance import (
    SOURCE_SERVICE_EVIDENCE,
    block_provenance,
)

NARRATIVE_CONSTRAINTS: tuple[str, ...] = (
    "Do not describe organisation metrics as learning improvement.",
    "Do not treat analytics PASS as Adaptive or Strategy Authority flip.",
    "Do not invent causation from ambiguous delivery→outcome linkage.",
    "Empty authentic / low N preferred over imputed healthy composites.",
)

SOURCE_SERVICE_ANALYTICS = "analytics_engine"
SOURCE_SERVICE_POLICY_EVALUATION = "policy_evaluation"
SOURCE_SERVICE_EXPERIMENT = "experiment_framework"


class AnalyticsValidationError(ValueError):
    """Raised when analytics aggregation inputs are invalid."""


class AnalyticsAggregator:
    """Deterministic observational analytics aggregator (E4).

    Identical PolicyEvaluation / ExperimentObservation / EvidenceRecord
    inputs → identical AnalyticsSummary material every execution.
    """

    AGGREGATOR_ID = "analytics_aggregator"
    AGGREGATOR_VERSION = "1.0.0-e4"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def aggregator_id(self) -> str:
        return self.AGGREGATOR_ID

    @property
    def aggregator_version(self) -> str:
        return self.AGGREGATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def aggregate(
        self,
        *,
        evaluations: Sequence[PolicyEvaluation] = (),
        observations: Sequence[ExperimentObservation] = (),
        evidence_records: Sequence[EvidenceRecord] = (),
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
        period: Mapping[str, Any] | None = None,
    ) -> AnalyticsSummary:
        """Aggregate immutable observational inputs into AnalyticsSummary.

        Does not mutate evaluations, observations, or evidence_records.
        """
        self._ensure_enabled()
        resolved_audience = self._normalize_audience(audience)
        evals = self._validate_evaluations(evaluations)
        obs = self._validate_observations(observations)
        records = self._validate_evidence_records(evidence_records)

        if not evals and not obs and not records:
            return AnalyticsSummary(
                audience=resolved_audience,
                as_of=as_of,
                period=dict(period or {}),
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason="empty_authentic",
                limitations=("empty_authentic",),
                narrative_constraints=NARRATIVE_CONSTRAINTS,
                trend_metadata=TrendMetadata(
                    grain=GRAIN_SYSTEM,
                    comparable=False,
                    direction=TREND_DIRECTION_NOT_ESTIMABLE,
                    limitations=("empty_authentic",),
                ),
                provenance={
                    "analytics": block_provenance(
                        available=False,
                        source_service=SOURCE_SERVICE_ANALYTICS,
                        source_entity="AnalyticsSummary",
                        collected_at=as_of,
                        unavailable_reason="empty_authentic",
                    )
                },
            )

        policy_summaries = self._policy_summaries(evals)
        experiment_summaries = self._experiment_summaries(obs)
        confidence = self._confidence_summary(evals)
        claim_mix = self._claim_boundary_mix(evals, records)
        metric_series = self._metric_series(evals, claim_mix, as_of=as_of)
        scorecard = self._scorecard_slice(
            claim_mix=claim_mix,
            confidence=confidence,
            evaluations=evals,
            as_of=as_of,
            period=period,
        )
        limitations = self._limitations(evals, obs, records, claim_mix)
        evidence_refs = self._evidence_refs(evals, obs, records)
        experiment_refs = self._experiment_refs(evals, obs)
        evaluation_ids = tuple(
            sorted({e.evaluation_id for e in evals if e.evaluation_id})
        )
        student_ids = self._student_ids(obs, records)
        resolved_as_of = as_of or _deterministic_as_of(evals, obs, records)
        resolved_period = dict(period or {})
        if not resolved_period:
            resolved_period = {
                "grain": GRAIN_SYSTEM,
                "as_of": resolved_as_of or "",
            }

        draft = AnalyticsSummary(
            summary_version=EVIDENCE_VERSION_E4,
            engine_version=EVIDENCE_VERSION_E4,
            as_of=resolved_as_of,
            period=resolved_period,
            audience=resolved_audience,
            evidence_count=len(evidence_refs),
            observation_count=len(obs),
            evaluation_count=len(evals),
            student_count=len(student_ids),
            experiment_count=len(experiment_refs),
            policy_summaries=policy_summaries,
            experiment_summaries=experiment_summaries,
            confidence_summary=confidence,
            metric_series=metric_series,
            scorecard_slice=scorecard,
            trend_metadata=TrendMetadata(
                grain=GRAIN_SYSTEM,
                comparable=False,
                direction=TREND_DIRECTION_NOT_ESTIMABLE,
                limitations=("no_prior_period", "single_freeze"),
            ),
            claim_boundary_mix=claim_mix,
            limitations=limitations,
            narrative_constraints=NARRATIVE_CONSTRAINTS,
            provenance=self._provenance(evals, obs, records, resolved_as_of),
            evaluation_ids=evaluation_ids,
            experiment_refs=experiment_refs,
            evidence_refs=evidence_refs,
            authority=AUTHORITY_EVIDENCE_PLATFORM,
            availability=AVAILABILITY_AVAILABLE,
        )
        return replace(draft, contents_ref=_contents_ref(draft))

    def _ensure_enabled(self) -> None:
        if not self._enabled:
            raise AnalyticsValidationError(
                "AnalyticsAggregator is disabled (feature flag OFF)"
            )

    def _normalize_audience(self, audience: str) -> str:
        resolved = (audience or "").strip().lower() or ANALYTICS_AUDIENCE_GOVERNANCE
        if resolved not in ANALYTICS_AUDIENCES or not resolved:
            allowed = sorted(k for k in ANALYTICS_AUDIENCES if k)
            raise AnalyticsValidationError(
                f"audience must be one of {allowed}"
            )
        if resolved == "student_coaching":
            raise AnalyticsValidationError(
                "student_coaching is a forbidden analytics audience"
            )
        return resolved

    def _validate_evaluations(
        self, evaluations: Sequence[PolicyEvaluation]
    ) -> tuple[PolicyEvaluation, ...]:
        items = tuple(evaluations or ())
        for item in items:
            if not isinstance(item, PolicyEvaluation):
                raise AnalyticsValidationError(
                    "evaluations must contain PolicyEvaluation values"
                )
        return tuple(sorted(items, key=lambda e: (e.evaluation_id, e.policy_id)))

    def _validate_observations(
        self, observations: Sequence[ExperimentObservation]
    ) -> tuple[ExperimentObservation, ...]:
        items = tuple(observations or ())
        for item in items:
            if not isinstance(item, ExperimentObservation):
                raise AnalyticsValidationError(
                    "observations must contain ExperimentObservation values"
                )
        return tuple(
            sorted(items, key=lambda o: (o.observation_id, o.experiment_id))
        )

    def _validate_evidence_records(
        self, evidence_records: Sequence[EvidenceRecord]
    ) -> tuple[EvidenceRecord, ...]:
        items = tuple(evidence_records or ())
        for item in items:
            if not isinstance(item, EvidenceRecord):
                raise AnalyticsValidationError(
                    "evidence_records must contain EvidenceRecord values"
                )
        return tuple(sorted(items, key=lambda r: (r.evidence_id, r.student_id)))

    def _policy_summaries(
        self, evaluations: Sequence[PolicyEvaluation]
    ) -> tuple[PolicySummaryProjection, ...]:
        summaries: list[PolicySummaryProjection] = []
        for evaluation in evaluations:
            kind = ""
            if isinstance(evaluation.statistical_summary, Mapping):
                kind = str(evaluation.statistical_summary.get("design") or "")
            claim = ""
            for metric in evaluation.outcome_metrics:
                if metric.claim_boundary:
                    claim = metric.claim_boundary
                    break
            if not claim and isinstance(evaluation.explanation.confidence, Mapping):
                claim = str(
                    evaluation.explanation.confidence.get("claim_boundary") or ""
                )
            observation_count = 0
            if isinstance(evaluation.statistical_summary, Mapping):
                raw = evaluation.statistical_summary.get("observation_count")
                if isinstance(raw, int):
                    observation_count = raw
                else:
                    observation_count = len(evaluation.evidence_refs)
            summaries.append(
                PolicySummaryProjection(
                    policy_id=evaluation.policy_id,
                    policy_version=evaluation.policy_version,
                    evaluation_id=evaluation.evaluation_id,
                    evaluation_kind=kind,
                    gate_result=evaluation.gate_result,
                    recommendation=evaluation.recommendation,
                    confidence_band=evaluation.confidence_band,
                    claim_boundary_intent=claim,
                    observation_count=observation_count,
                    experiment_refs=evaluation.experiment_refs,
                    evidence_refs=evaluation.evidence_refs,
                    limitations=evaluation.limitations,
                )
            )
        return tuple(summaries)

    def _experiment_summaries(
        self, observations: Sequence[ExperimentObservation]
    ) -> tuple[ExperimentSummaryProjection, ...]:
        by_experiment: dict[str, list[ExperimentObservation]] = {}
        for obs in observations:
            key = obs.experiment_id or ""
            by_experiment.setdefault(key, []).append(obs)
        summaries: list[ExperimentSummaryProjection] = []
        for experiment_id in sorted(by_experiment.keys()):
            group = by_experiment[experiment_id]
            arm_counts = Counter(o.arm_id for o in group if o.arm_id)
            cohort_counts = Counter(o.cohort for o in group if o.cohort)
            mechanisms = tuple(
                sorted(
                    {
                        o.assignment_mechanism
                        for o in group
                        if o.assignment_mechanism
                    }
                )
            )
            versions = sorted(
                {o.experiment_version for o in group if o.experiment_version}
            )
            summaries.append(
                ExperimentSummaryProjection(
                    experiment_id=experiment_id,
                    experiment_version=versions[0] if versions else "",
                    arm_distribution={k: arm_counts[k] for k in sorted(arm_counts)},
                    observation_count=len(group),
                    student_count=len({o.student_id for o in group if o.student_id}),
                    evidence_count=len({o.evidence_id for o in group if o.evidence_id}),
                    cohort_distribution={
                        k: cohort_counts[k] for k in sorted(cohort_counts)
                    },
                    assignment_mechanisms=mechanisms,
                    limitations=(),
                )
            )
        return tuple(summaries)

    def _confidence_summary(
        self, evaluations: Sequence[PolicyEvaluation]
    ) -> ConfidenceSummaryProjection:
        bands = Counter(
            e.confidence_band for e in evaluations if e.confidence_band
        )
        gate_passed = sum(1 for e in evaluations if e.gate_result == GATE_PASSED)
        gate_failed = sum(1 for e in evaluations if e.gate_result == GATE_FAILED)
        gate_ineligible = sum(
            1 for e in evaluations if e.gate_result == GATE_INELIGIBLE
        )
        dominant = ""
        if bands:
            # Deterministic: highest count, then lexicographic band.
            dominant = sorted(
                bands.items(), key=lambda item: (-item[1], item[0])
            )[0][0]
        not_proven: list[str] = []
        for evaluation in evaluations:
            if evaluation.confidence_band in {"low", "insufficient", ""}:
                not_proven.append(
                    f"{evaluation.evaluation_id or evaluation.policy_id}:"
                    f"{evaluation.confidence_band or 'missing'}"
                )
            for limitation in evaluation.limitations:
                if limitation and limitation not in not_proven:
                    not_proven.append(limitation)
        rationale = (
            f"{len(evaluations)} evaluations; "
            f"dominant_band={dominant or 'none'}; "
            f"gate_passed={gate_passed}"
        )
        return ConfidenceSummaryProjection(
            bands={k: bands[k] for k in sorted(bands)},
            dominant_band=dominant,
            rationale_summary=rationale,
            evaluations_with_gate_passed=gate_passed,
            evaluations_with_gate_failed=gate_failed,
            evaluations_with_gate_ineligible=gate_ineligible,
            not_proven=tuple(sorted(set(not_proven))),
        )

    def _claim_boundary_mix(
        self,
        evaluations: Sequence[PolicyEvaluation],
        records: Sequence[EvidenceRecord],
    ) -> dict[str, int]:
        mix: Counter[str] = Counter()
        for evaluation in evaluations:
            for metric in evaluation.outcome_metrics:
                if metric.claim_boundary:
                    mix[metric.claim_boundary] += 1
            if not evaluation.outcome_metrics:
                mix[CLAIM_ORGANISATION] += 0
        for record in records:
            if record.claim_boundary:
                mix[record.claim_boundary] += 1
        return {k: mix[k] for k in sorted(mix) if mix[k]}

    def _metric_series(
        self,
        evaluations: Sequence[PolicyEvaluation],
        claim_mix: Mapping[str, int],
        *,
        as_of: str | None,
    ) -> tuple[MetricSeries, ...]:
        series: list[MetricSeries] = []
        # Prefer explicit OutcomeMetric values from evaluations.
        by_metric: dict[str, list[Any]] = {}
        for evaluation in evaluations:
            for metric in evaluation.outcome_metrics:
                key = metric.metric_id or f"{metric.claim_boundary}:{metric.grain}"
                by_metric.setdefault(key, []).append(metric)
        for metric_id in sorted(by_metric.keys()):
            metrics = by_metric[metric_id]
            claim = metrics[0].claim_boundary
            grain = (metrics[0].grain or "").strip().lower()
            if grain not in ANALYTICS_GRAINS or not grain:
                grain = GRAIN_SYSTEM
            points = tuple(
                MetricPoint(
                    t=as_of or f"point-{idx:04d}",
                    value=m.value,
                    n=m.n,
                    uncertainty=m.uncertainty or (
                        "not_estimable" if m.n is not None and m.n < 3 else ""
                    ),
                )
                for idx, m in enumerate(metrics)
            )
            limitations = tuple(
                sorted(
                    {
                        *sum((tuple(m.limitations) for m in metrics), ()),
                        *(
                            ("not_estimable",)
                            if any(
                                m.n is not None and m.n < 3 for m in metrics
                            )
                            else ()
                        ),
                    }
                )
            )
            series.append(
                MetricSeries(
                    metric_id=metric_id,
                    claim_boundary=claim,
                    grain=grain,
                    points=points,
                    filters={"source": "policy_evaluation"},
                    limitations=limitations,
                )
            )
        # Claim-boundary count series when no OutcomeMetrics present.
        if not series and claim_mix:
            for boundary in sorted(claim_mix.keys()):
                series.append(
                    MetricSeries(
                        metric_id=f"claim_boundary_count:{boundary}",
                        claim_boundary=boundary,
                        grain=GRAIN_SYSTEM,
                        points=(
                            MetricPoint(
                                t=as_of or "",
                                value=claim_mix[boundary],
                                n=claim_mix[boundary],
                                uncertainty="",
                            ),
                        ),
                        filters={"source": "claim_boundary_mix"},
                        limitations=(),
                    )
                )
        return tuple(series)

    def _scorecard_slice(
        self,
        *,
        claim_mix: Mapping[str, int],
        confidence: ConfidenceSummaryProjection,
        evaluations: Sequence[PolicyEvaluation],
        as_of: str | None,
        period: Mapping[str, Any] | None,
    ) -> ScorecardSlice:
        org = {
            "count": claim_mix.get(CLAIM_ORGANISATION, 0),
            "evaluations": len(evaluations),
        }
        signal = {"count": claim_mix.get(CLAIM_LEARNING_SIGNAL, 0)}
        depth_count = claim_mix.get(CLAIM_LEARNING_DEPTH, 0)
        depth = {
            "count": depth_count,
            "status": "deferred" if depth_count == 0 else "observed",
        }
        guardrails = {
            "gate_passed": confidence.evaluations_with_gate_passed,
            "gate_failed": confidence.evaluations_with_gate_failed,
            "gate_ineligible": confidence.evaluations_with_gate_ineligible,
            "dominant_confidence_band": confidence.dominant_band,
        }
        resolved_period = dict(period or {})
        if not resolved_period:
            resolved_period = {"as_of": as_of or "", "grain": GRAIN_SYSTEM}
        slice_material = {
            "guardrails_block": guardrails,
            "learning_depth_block": depth,
            "learning_signal_block": signal,
            "organisation_block": org,
            "period": resolved_period,
        }
        digest = serialize_canonical(slice_material)
        slice_id = f"score-{hashlib.sha256(digest.encode('utf-8')).hexdigest()[:16]}"
        return ScorecardSlice(
            slice_id=slice_id,
            period=resolved_period,
            organisation_block=org,
            learning_signal_block=signal,
            learning_depth_block=depth,
            guardrails_block=guardrails,
            narrative_constraints=NARRATIVE_CONSTRAINTS,
        )

    def _limitations(
        self,
        evaluations: Sequence[PolicyEvaluation],
        observations: Sequence[ExperimentObservation],
        records: Sequence[EvidenceRecord],
        claim_mix: Mapping[str, int],
    ) -> tuple[str, ...]:
        codes: list[str] = []
        if not evaluations:
            codes.append("no_evaluations")
        if not observations and not records:
            codes.append("no_observations")
        if CLAIM_LEARNING_DEPTH in claim_mix:
            codes.append("learning_depth_present_observe_only")
        else:
            codes.append("learning_depth_deferred")
        for evaluation in evaluations:
            codes.extend(evaluation.limitations)
            codes.extend(evaluation.gate_codes)
        for record in records:
            codes.extend(record.limitations)
        # Prefer empty authentic over imputation when thin N.
        if len(observations) < 3 and observations:
            codes.append("thin_n")
        return tuple(dict.fromkeys(codes))

    def _evidence_refs(
        self,
        evaluations: Sequence[PolicyEvaluation],
        observations: Sequence[ExperimentObservation],
        records: Sequence[EvidenceRecord],
    ) -> tuple[str, ...]:
        refs: set[str] = set()
        for evaluation in evaluations:
            refs.update(evaluation.evidence_refs)
            refs.update(evaluation.evidence_bundle_ids)
        for obs in observations:
            if obs.evidence_id:
                refs.add(obs.evidence_id)
        for record in records:
            if record.evidence_id:
                refs.add(record.evidence_id)
        return tuple(sorted(refs))

    def _experiment_refs(
        self,
        evaluations: Sequence[PolicyEvaluation],
        observations: Sequence[ExperimentObservation],
    ) -> tuple[str, ...]:
        refs: set[str] = set()
        for evaluation in evaluations:
            refs.update(evaluation.experiment_refs)
            if evaluation.experiment_id:
                refs.add(evaluation.experiment_id)
        for obs in observations:
            if obs.experiment_id:
                refs.add(obs.experiment_id)
        return tuple(sorted(refs))

    def _student_ids(
        self,
        observations: Sequence[ExperimentObservation],
        records: Sequence[EvidenceRecord],
    ) -> tuple[str, ...]:
        ids: set[str] = set()
        for obs in observations:
            if obs.student_id:
                ids.add(obs.student_id)
        for record in records:
            if record.student_id:
                ids.add(record.student_id)
        return tuple(sorted(ids))

    def _provenance(
        self,
        evaluations: Sequence[PolicyEvaluation],
        observations: Sequence[ExperimentObservation],
        records: Sequence[EvidenceRecord],
        as_of: str | None,
    ) -> dict[str, Any]:
        return {
            "analytics": block_provenance(
                available=True,
                source_service=SOURCE_SERVICE_ANALYTICS,
                source_entity="AnalyticsSummary",
                collected_at=as_of,
            ),
            "evaluations": block_provenance(
                available=bool(evaluations),
                source_service=SOURCE_SERVICE_POLICY_EVALUATION,
                source_entity="PolicyEvaluation",
                collected_at=as_of,
                unavailable_reason="" if evaluations else "no_evaluations",
            ),
            "experiments": block_provenance(
                available=bool(observations),
                source_service=SOURCE_SERVICE_EXPERIMENT,
                source_entity="ExperimentObservation",
                collected_at=as_of,
                unavailable_reason="" if observations else "no_observations",
            ),
            "evidence": block_provenance(
                available=bool(records),
                source_service=SOURCE_SERVICE_EVIDENCE,
                source_entity="EvidenceRecord",
                collected_at=as_of,
                unavailable_reason="" if records else "no_evidence_records",
            ),
        }


def _deterministic_as_of(
    evaluations: Sequence[PolicyEvaluation],
    observations: Sequence[ExperimentObservation],
    records: Sequence[EvidenceRecord],
) -> str | None:
    stamps: list[str] = []
    for evaluation in evaluations:
        if evaluation.created_at:
            stamps.append(evaluation.created_at)
    for obs in observations:
        if obs.observed_at:
            stamps.append(obs.observed_at)
    for record in records:
        if record.as_of:
            stamps.append(record.as_of)
        elif record.observed_at:
            stamps.append(record.observed_at)
    stamps.sort()
    return stamps[-1] if stamps else None


def _contents_ref(summary: AnalyticsSummary) -> str:
    material = summary.to_canonical_dict()
    material["summary_id"] = ""
    material["contents_ref"] = ""
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"aref-{digest[:24]}"


def build_analytics_aggregator(
    *, enabled: bool
) -> AnalyticsAggregator | None:
    """DI helper — construct AnalyticsAggregator only when the flag is on."""
    if not enabled:
        return None
    return AnalyticsAggregator(enabled=True)
