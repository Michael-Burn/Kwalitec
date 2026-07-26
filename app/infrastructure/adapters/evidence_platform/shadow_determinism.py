"""Determinism validation for Evidence Shadow Validation (MS-006 E5).

Verifies identical platform artefacts / pipeline replays yield identical
serializations. Observational only — never mutates Evidence Platform inputs,
never deploys policy, never changes educational behaviour.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AnalyticsSummary,
    EvidenceProjection,
    EvidenceRecord,
    ExperimentObservation,
    PolicyEvaluation,
)

# Drift kinds (observational; no auto-remediation).
DRIFT_EVIDENCE_INSTABILITY = "evidence_instability"
DRIFT_OBSERVATION_INSTABILITY = "observation_instability"
DRIFT_EVALUATION_INSTABILITY = "evaluation_instability"
DRIFT_ANALYTICS_INSTABILITY = "analytics_instability"
DRIFT_PROJECTION_INSTABILITY = "projection_instability"
DRIFT_PIPELINE_REPLAY_FAILURE = "pipeline_replay_failure"
DRIFT_DETERMINISM_FAILURE = "determinism_failure"
DRIFT_CLAIM_BOUNDARY_LEAKAGE = "claim_boundary_leakage"
DRIFT_INPUT_MUTATION = "input_mutation"

DRIFT_KINDS: frozenset[str] = frozenset(
    {
        DRIFT_EVIDENCE_INSTABILITY,
        DRIFT_OBSERVATION_INSTABILITY,
        DRIFT_EVALUATION_INSTABILITY,
        DRIFT_ANALYTICS_INSTABILITY,
        DRIFT_PROJECTION_INSTABILITY,
        DRIFT_PIPELINE_REPLAY_FAILURE,
        DRIFT_DETERMINISM_FAILURE,
        DRIFT_CLAIM_BOUNDARY_LEAKAGE,
        DRIFT_INPUT_MUTATION,
    }
)

SEVERITY_INFO = "info"
SEVERITY_WARN = "warn"
SEVERITY_CRITICAL = "critical"

SUBSYSTEM_EVIDENCE = "evidence_collection"
SUBSYSTEM_EXPERIMENT = "experiment_framework"
SUBSYSTEM_EVALUATION = "policy_evaluation"
SUBSYSTEM_ANALYTICS = "analytics"
SUBSYSTEM_PROJECTION = "projection"


@dataclass(frozen=True)
class DeterminismCheckResult:
    """Result of one artefact / pipeline determinism check."""

    subsystem: str
    success: bool
    first_fingerprint: str = ""
    second_fingerprint: str = ""
    detail: str = ""
    artefact_count: int = 0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "artefact_count": self.artefact_count,
            "detail": self.detail,
            "first_fingerprint": self.first_fingerprint,
            "second_fingerprint": self.second_fingerprint,
            "subsystem": self.subsystem,
            "success": self.success,
        }


@dataclass(frozen=True)
class DriftSignal:
    """Single observational drift signal (no automatic correction)."""

    kind: str
    severity: str
    detail: str
    subsystem: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "detail": self.detail,
            "kind": self.kind,
            "severity": self.severity,
            "subsystem": self.subsystem,
        }


@dataclass(frozen=True)
class DeterminismValidationResult:
    """Aggregate determinism outcome for one shadow cycle."""

    success: bool
    evidence: DeterminismCheckResult | None = None
    observation: DeterminismCheckResult | None = None
    evaluation: DeterminismCheckResult | None = None
    analytics: DeterminismCheckResult | None = None
    projection: DeterminismCheckResult | None = None
    pipeline_replay: DeterminismCheckResult | None = None
    drift_signals: tuple[DriftSignal, ...] = ()
    detail: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "analytics": None
            if self.analytics is None
            else self.analytics.to_canonical_dict(),
            "detail": self.detail,
            "drift_signals": [s.to_canonical_dict() for s in self.drift_signals],
            "evaluation": None
            if self.evaluation is None
            else self.evaluation.to_canonical_dict(),
            "evidence": None
            if self.evidence is None
            else self.evidence.to_canonical_dict(),
            "observation": None
            if self.observation is None
            else self.observation.to_canonical_dict(),
            "pipeline_replay": None
            if self.pipeline_replay is None
            else self.pipeline_replay.to_canonical_dict(),
            "projection": None
            if self.projection is None
            else self.projection.to_canonical_dict(),
            "success": self.success,
        }


def _fingerprint_sequence(items: Sequence[Any]) -> str:
    parts: list[str] = []
    for item in items:
        serialize = getattr(item, "serialize", None)
        if callable(serialize):
            parts.append(serialize())
        else:
            parts.append(repr(item))
    return "|".join(parts)


def _serialize_stable(item: Any) -> DeterminismCheckResult | None:
    """Re-serialize twice; return failure if fingerprints diverge."""
    serialize = getattr(item, "serialize", None)
    if not callable(serialize):
        return DeterminismCheckResult(
            subsystem="unknown",
            success=False,
            detail="artefact_missing_serialize",
        )
    first = serialize()
    second = serialize()
    if first != second:
        return DeterminismCheckResult(
            subsystem="unknown",
            success=False,
            first_fingerprint=first[:64],
            second_fingerprint=second[:64],
            detail="serialize_not_stable",
            artefact_count=1,
        )
    return None


def _check_sequence(
    *,
    subsystem: str,
    items: Sequence[Any],
    expected_type: type,
    empty_ok: bool = True,
) -> DeterminismCheckResult:
    if not items:
        return DeterminismCheckResult(
            subsystem=subsystem,
            success=bool(empty_ok),
            detail="empty_coverage" if empty_ok else "missing_required_artefacts",
            artefact_count=0,
        )
    for item in items:
        if not isinstance(item, expected_type):
            return DeterminismCheckResult(
                subsystem=subsystem,
                success=False,
                detail=f"unexpected_type:{type(item).__name__}",
                artefact_count=len(items),
            )
        unstable = _serialize_stable(item)
        if unstable is not None:
            return DeterminismCheckResult(
                subsystem=subsystem,
                success=False,
                first_fingerprint=unstable.first_fingerprint,
                second_fingerprint=unstable.second_fingerprint,
                detail=unstable.detail or "serialize_not_stable",
                artefact_count=len(items),
            )
    first = _fingerprint_sequence(items)
    second = _fingerprint_sequence(items)
    if first != second:
        return DeterminismCheckResult(
            subsystem=subsystem,
            success=False,
            first_fingerprint=first[:64],
            second_fingerprint=second[:64],
            detail="sequence_fingerprint_mismatch",
            artefact_count=len(items),
        )
    return DeterminismCheckResult(
        subsystem=subsystem,
        success=True,
        first_fingerprint=first[:64],
        second_fingerprint=second[:64],
        detail="identical_serialize_replay",
        artefact_count=len(items),
    )


def _claim_boundary_leakage(
    evidence_records: Sequence[EvidenceRecord],
    evaluations: Sequence[PolicyEvaluation],
) -> DriftSignal | None:
    """Detect organisation vs learning_depth claim-boundary leakage signals."""
    for record in evidence_records:
        boundary = (getattr(record, "claim_boundary", "") or "").strip()
        payload = dict(getattr(record, "payload_summary", {}) or {})
        # Learning-depth language inside organisation artefacts is a SP8 leak.
        if boundary == "organisation":
            text = " ".join(str(v) for v in payload.values()).lower()
            if "learning_depth" in text or "exam_ready" in text:
                return DriftSignal(
                    kind=DRIFT_CLAIM_BOUNDARY_LEAKAGE,
                    severity=SEVERITY_CRITICAL,
                    detail="organisation_payload_contains_learning_depth_language",
                    subsystem=SUBSYSTEM_EVIDENCE,
                )
    for evaluation in evaluations:
        gate = (getattr(evaluation, "gate_result", "") or "").strip()
        recommendation = (getattr(evaluation, "recommendation", "") or "").strip()
        metrics = tuple(getattr(evaluation, "outcome_metrics", ()) or ())
        boundaries = {
            (getattr(metric, "claim_boundary", "") or "").strip()
            for metric in metrics
            if (getattr(metric, "claim_boundary", "") or "").strip()
        }
        if (
            "organisation" in boundaries
            and "learning_depth" in boundaries
            and recommendation in {"keep", "expand_soak"}
            and gate == "passed"
        ):
            # Mixed claim boundaries with promote-leaning recommendation needs review.
            return DriftSignal(
                kind=DRIFT_CLAIM_BOUNDARY_LEAKAGE,
                severity=SEVERITY_WARN,
                detail="mixed_claim_boundaries_with_promote_leaning_recommendation",
                subsystem=SUBSYSTEM_EVALUATION,
            )
    return None


class DeterminismValidator:
    """Validate determinism of frozen Evidence Platform artefacts.

    Identical platform state → identical fingerprints every execution.
    Never mutates inputs.
    """

    VALIDATOR_ID = "evidence_determinism_validator"
    VALIDATOR_VERSION = "1.0.0-e5"

    def validate(
        self,
        *,
        evidence_records: Sequence[EvidenceRecord] = (),
        observations: Sequence[ExperimentObservation] = (),
        evaluations: Sequence[PolicyEvaluation] = (),
        analytics_summaries: Sequence[AnalyticsSummary] = (),
        projections: Sequence[EvidenceProjection] = (),
        adapter: Any | None = None,
        run_pipeline_replay: bool = True,
    ) -> DeterminismValidationResult:
        """Validate serialize stability and optional pipeline replay determinism."""
        evidence_records = tuple(evidence_records or ())
        observations = tuple(observations or ())
        evaluations = tuple(evaluations or ())
        analytics_summaries = tuple(analytics_summaries or ())
        projections = tuple(projections or ())

        # Capture pre-check fingerprints to detect accidental mutation.
        pre_fingerprints = {
            "evidence": _fingerprint_sequence(evidence_records),
            "observations": _fingerprint_sequence(observations),
            "evaluations": _fingerprint_sequence(evaluations),
            "analytics": _fingerprint_sequence(analytics_summaries),
            "projections": _fingerprint_sequence(projections),
        }

        evidence = _check_sequence(
            subsystem=SUBSYSTEM_EVIDENCE,
            items=evidence_records,
            expected_type=EvidenceRecord,
        )
        observation = _check_sequence(
            subsystem=SUBSYSTEM_EXPERIMENT,
            items=observations,
            expected_type=ExperimentObservation,
        )
        evaluation = _check_sequence(
            subsystem=SUBSYSTEM_EVALUATION,
            items=evaluations,
            expected_type=PolicyEvaluation,
        )
        analytics = _check_sequence(
            subsystem=SUBSYSTEM_ANALYTICS,
            items=analytics_summaries,
            expected_type=AnalyticsSummary,
        )
        projection = _check_sequence(
            subsystem=SUBSYSTEM_PROJECTION,
            items=projections,
            expected_type=EvidenceProjection,
        )

        pipeline_replay: DeterminismCheckResult | None = None
        if run_pipeline_replay and adapter is not None:
            pipeline_replay = self._verify_pipeline_replay(
                adapter=adapter,
                evidence_records=evidence_records,
                observations=observations,
                evaluations=evaluations,
                analytics_summaries=analytics_summaries,
                projections=projections,
            )

        post_fingerprints = {
            "evidence": _fingerprint_sequence(evidence_records),
            "observations": _fingerprint_sequence(observations),
            "evaluations": _fingerprint_sequence(evaluations),
            "analytics": _fingerprint_sequence(analytics_summaries),
            "projections": _fingerprint_sequence(projections),
        }

        drift_signals: list[DriftSignal] = []
        if pre_fingerprints != post_fingerprints:
            drift_signals.append(
                DriftSignal(
                    kind=DRIFT_INPUT_MUTATION,
                    severity=SEVERITY_CRITICAL,
                    detail="input_artefacts_mutated_during_validation",
                    subsystem="shadow_validation",
                )
            )

        checks = (evidence, observation, evaluation, analytics, projection)
        for check in checks:
            if check is not None and not check.success and check.artefact_count > 0:
                kind_map = {
                    SUBSYSTEM_EVIDENCE: DRIFT_EVIDENCE_INSTABILITY,
                    SUBSYSTEM_EXPERIMENT: DRIFT_OBSERVATION_INSTABILITY,
                    SUBSYSTEM_EVALUATION: DRIFT_EVALUATION_INSTABILITY,
                    SUBSYSTEM_ANALYTICS: DRIFT_ANALYTICS_INSTABILITY,
                    SUBSYSTEM_PROJECTION: DRIFT_PROJECTION_INSTABILITY,
                }
                drift_signals.append(
                    DriftSignal(
                        kind=kind_map.get(check.subsystem, DRIFT_DETERMINISM_FAILURE),
                        severity=SEVERITY_CRITICAL,
                        detail=check.detail or "subsystem_unstable",
                        subsystem=check.subsystem,
                    )
                )

        if pipeline_replay is not None and not pipeline_replay.success:
            drift_signals.append(
                DriftSignal(
                    kind=DRIFT_PIPELINE_REPLAY_FAILURE,
                    severity=SEVERITY_CRITICAL,
                    detail=pipeline_replay.detail or "pipeline_replay_failed",
                    subsystem="pipeline",
                )
            )

        leakage = _claim_boundary_leakage(evidence_records, evaluations)
        if leakage is not None:
            drift_signals.append(leakage)

        covered = any(c.artefact_count > 0 for c in checks)
        subsystem_ok = all(
            c.success or c.artefact_count == 0 for c in checks
        )
        pipeline_ok = pipeline_replay is None or pipeline_replay.success
        mutation_ok = pre_fingerprints == post_fingerprints
        success = covered and subsystem_ok and pipeline_ok and mutation_ok

        if covered and not success:
            drift_signals.append(
                DriftSignal(
                    kind=DRIFT_DETERMINISM_FAILURE,
                    severity=SEVERITY_CRITICAL,
                    detail="deterministic_replay_failed",
                    subsystem="shadow_validation",
                )
            )

        detail = "identical_platform_state_replay" if success else "determinism_failed"
        if not covered:
            detail = "no_artefacts_to_validate"
            success = False

        return DeterminismValidationResult(
            success=success,
            evidence=evidence,
            observation=observation,
            evaluation=evaluation,
            analytics=analytics,
            projection=projection,
            pipeline_replay=pipeline_replay,
            drift_signals=tuple(drift_signals),
            detail=detail,
        )

    def _verify_pipeline_replay(
        self,
        *,
        adapter: Any,
        evidence_records: Sequence[EvidenceRecord],
        observations: Sequence[ExperimentObservation],
        evaluations: Sequence[PolicyEvaluation],
        analytics_summaries: Sequence[AnalyticsSummary],
        projections: Sequence[EvidenceProjection],
    ) -> DeterminismCheckResult:
        """Re-run analytics / projection from frozen inputs when wired."""
        try:
            if analytics_summaries and (
                evaluations or observations or evidence_records
            ):
                first_summary = analytics_summaries[0]
                audience = first_summary.audience or "governance"
                as_of = first_summary.as_of
                period = dict(first_summary.period or {})
                result = adapter.aggregate_analytics(
                    evaluations=evaluations,
                    observations=observations,
                    evidence_records=evidence_records,
                    audience=audience,
                    as_of=as_of,
                    period=period or None,
                )
                if not getattr(result, "ok", False):
                    return DeterminismCheckResult(
                        subsystem="pipeline",
                        success=False,
                        detail=f"aggregate_failed:{getattr(result, 'error_code', '')}",
                    )
                replayed = result.value
                if not isinstance(replayed, AnalyticsSummary):
                    return DeterminismCheckResult(
                        subsystem="pipeline",
                        success=False,
                        detail="aggregate_did_not_return_summary",
                    )
                # Compare observational counts / claim mix (ids may include
                # provenance clocks); prefer structural fingerprint fields.
                first_fp = self._analytics_structural_fingerprint(first_summary)
                second_fp = self._analytics_structural_fingerprint(replayed)
                if first_fp != second_fp:
                    return DeterminismCheckResult(
                        subsystem="pipeline",
                        success=False,
                        first_fingerprint=first_fp[:64],
                        second_fingerprint=second_fp[:64],
                        detail="analytics_structural_mismatch",
                        artefact_count=1,
                    )
                if projections:
                    proj_result = adapter.project_evidence(
                        replayed, audience=audience, as_of=as_of
                    )
                    if not getattr(proj_result, "ok", False):
                        return DeterminismCheckResult(
                            subsystem="pipeline",
                            success=False,
                            detail=(
                                "project_failed:"
                                f"{getattr(proj_result, 'error_code', '')}"
                            ),
                        )
                    replayed_proj = proj_result.value
                    if not isinstance(replayed_proj, EvidenceProjection):
                        return DeterminismCheckResult(
                            subsystem="pipeline",
                            success=False,
                            detail="project_did_not_return_projection",
                        )
                    # Re-project twice for serialize identity.
                    again = adapter.project_evidence(
                        replayed, audience=audience, as_of=as_of
                    )
                    if not getattr(again, "ok", False) or again.value.serialize() != (
                        replayed_proj.serialize()
                    ):
                        return DeterminismCheckResult(
                            subsystem="pipeline",
                            success=False,
                            detail="projection_replay_mismatch",
                        )
            elif evaluations and observations:
                # Double-evaluate first evaluation's policy when factory wired.
                factory = getattr(adapter, "policy_evaluation_factory", None)
                if factory is not None:
                    first = evaluations[0]
                    policy_id = getattr(first, "policy_id", "") or ""
                    created_at = getattr(first, "created_at", None)
                    second = factory.evaluate(
                        observations,
                        policy_id=policy_id or None,
                        created_at=created_at,
                    )
                    if first.serialize() != second.serialize():
                        # Allow evaluation_id / created_at differences only if
                        # structural recommendation / gate match.
                        if (
                            first.recommendation != second.recommendation
                            or first.gate_result != second.gate_result
                        ):
                            return DeterminismCheckResult(
                                subsystem="pipeline",
                                success=False,
                                first_fingerprint=first.serialize()[:64],
                                second_fingerprint=second.serialize()[:64],
                                detail="evaluation_replay_mismatch",
                            )
            return DeterminismCheckResult(
                subsystem="pipeline",
                success=True,
                detail="pipeline_replay_ok",
                artefact_count=(
                    len(evidence_records)
                    + len(observations)
                    + len(evaluations)
                    + len(analytics_summaries)
                    + len(projections)
                ),
            )
        except Exception as exc:  # noqa: BLE001 — observational validator
            return DeterminismCheckResult(
                subsystem="pipeline",
                success=False,
                detail=f"pipeline_raised:{type(exc).__name__}",
            )

    @staticmethod
    def _analytics_structural_fingerprint(summary: AnalyticsSummary) -> str:
        return "|".join(
            [
                str(summary.evidence_count),
                str(summary.observation_count),
                str(summary.evaluation_count),
                str(summary.student_count),
                str(summary.experiment_count),
                summary.audience,
                str(dict(summary.claim_boundary_mix)),
                summary.confidence_summary.serialize()
                if hasattr(summary.confidence_summary, "serialize")
                else "",
            ]
        )


def build_determinism_validator() -> DeterminismValidator:
    """DI helper — fresh DeterminismValidator."""
    return DeterminismValidator()


__all__ = [
    "DRIFT_ANALYTICS_INSTABILITY",
    "DRIFT_CLAIM_BOUNDARY_LEAKAGE",
    "DRIFT_DETERMINISM_FAILURE",
    "DRIFT_EVALUATION_INSTABILITY",
    "DRIFT_EVIDENCE_INSTABILITY",
    "DRIFT_INPUT_MUTATION",
    "DRIFT_KINDS",
    "DRIFT_OBSERVATION_INSTABILITY",
    "DRIFT_PIPELINE_REPLAY_FAILURE",
    "DRIFT_PROJECTION_INSTABILITY",
    "DeterminismCheckResult",
    "DeterminismValidationResult",
    "DeterminismValidator",
    "DriftSignal",
    "SEVERITY_CRITICAL",
    "SEVERITY_INFO",
    "SEVERITY_WARN",
    "SUBSYSTEM_ANALYTICS",
    "SUBSYSTEM_EVALUATION",
    "SUBSYSTEM_EVIDENCE",
    "SUBSYSTEM_EXPERIMENT",
    "SUBSYSTEM_PROJECTION",
    "build_determinism_validator",
]
