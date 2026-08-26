"""Observational monitors for Adaptive Shadow Soak (MS-003 A6).

Comparison, determinism, and drift detection — telemetry / measurement only.
No automatic correction. No Experience / Runtime A influence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
)
from app.infrastructure.adapters.adaptive_engine.shadow import explanation_is_complete

# Drift kinds (observational; no auto-remediation).
DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE = "unexpected_recommendation_change"
DRIFT_DETERMINISM_FAILURE = "determinism_failure"
DRIFT_UNEXPLAINED_DIVERGENCE = "unexplained_divergence"
DRIFT_MISSING_EXPLANATION = "missing_explanation_bundle"
DRIFT_TRACE_FAILURE = "trace_failure"

DRIFT_KINDS: frozenset[str] = frozenset(
    {
        DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE,
        DRIFT_DETERMINISM_FAILURE,
        DRIFT_UNEXPLAINED_DIVERGENCE,
        DRIFT_MISSING_EXPLANATION,
        DRIFT_TRACE_FAILURE,
    }
)

SEVERITY_INFO = "info"
SEVERITY_WARN = "warn"
SEVERITY_CRITICAL = "critical"


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _baseline_label(baseline: dict[str, Any] | None) -> str:
    if not baseline:
        return ""
    return str(
        baseline.get("title")
        or baseline.get("recommendation_label")
        or baseline.get("topic_title")
        or ""
    ).strip()


def _baseline_topic_code(baseline: dict[str, Any] | None) -> str:
    if not baseline:
        return ""
    return str(baseline.get("topic_code") or "").strip()


def _baseline_category(baseline: dict[str, Any] | None) -> str:
    if not baseline:
        return ""
    return str(baseline.get("category") or "").strip()


def _adaptive_label(output: AdaptiveOutputBundle | None) -> str:
    if output is None:
        return ""
    rec = output.recommendation
    return str(
        rec.label or rec.title or rec.topic_code or ""
    ).strip()


@dataclass(frozen=True)
class RecommendationComparison:
    """Observational comparison of baseline vs adaptive recommendation."""

    agreed: bool
    baseline_label: str = ""
    adaptive_label: str = ""
    baseline_topic_code: str = ""
    adaptive_topic_code: str = ""
    baseline_category: str = ""
    adaptive_decision_kind: str = ""
    divergence_reason: str = ""
    comparable: bool = True

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "agreed": self.agreed,
            "adaptive_decision_kind": self.adaptive_decision_kind,
            "adaptive_label": self.adaptive_label,
            "adaptive_topic_code": self.adaptive_topic_code,
            "baseline_category": self.baseline_category,
            "baseline_label": self.baseline_label,
            "baseline_topic_code": self.baseline_topic_code,
            "comparable": self.comparable,
            "divergence_reason": self.divergence_reason,
        }


class RecommendationComparisonMonitor:
    """Compare RecommendationService baseline vs Adaptive Engine output."""

    MONITOR_ID = "recommendation_comparison_monitor"

    def compare(
        self,
        baseline: dict[str, Any] | None,
        adaptive: AdaptiveOutputBundle | None,
    ) -> RecommendationComparison:
        """Return agreement / divergence without mutating either side.

        Agreement prefers topic_code match when both present; otherwise
        normalised label / title equality. Divergence is measurable, not
        corrected.
        """
        if adaptive is None:
            return RecommendationComparison(
                agreed=False,
                baseline_label=_baseline_label(baseline),
                baseline_topic_code=_baseline_topic_code(baseline),
                baseline_category=_baseline_category(baseline),
                comparable=False,
                divergence_reason="adaptive_output_unavailable",
            )
        if baseline is None:
            return RecommendationComparison(
                agreed=False,
                adaptive_label=_adaptive_label(adaptive),
                adaptive_topic_code=adaptive.recommendation.topic_code or "",
                adaptive_decision_kind=adaptive.recommendation.decision_kind or "",
                comparable=False,
                divergence_reason="baseline_unavailable",
            )

        base_label = _baseline_label(baseline)
        base_code = _baseline_topic_code(baseline)
        base_cat = _baseline_category(baseline)
        adapt_label = _adaptive_label(adaptive)
        adapt_code = (adaptive.recommendation.topic_code or "").strip()
        adapt_kind = (adaptive.recommendation.decision_kind or "").strip()

        # Mission baselines: identity is title (and topic_code when present).
        # Prefer label match so Adaptive's empty/mismatched topic_code after
        # mission alignment does not create false topic_code_mismatch noise.
        mission_baseline = (
            str(baseline.get("baseline_kind") or "").strip().lower() == "mission"
            or bool(baseline.get("mission_aligned"))
        )
        if mission_baseline and base_label and adapt_label:
            agreed = _norm(base_label) == _norm(adapt_label)
            reason = "" if agreed else "label_mismatch"
        elif base_code and adapt_code:
            agreed = _norm(base_code) == _norm(adapt_code)
            reason = "" if agreed else "topic_code_mismatch"
        elif base_label and adapt_label:
            agreed = _norm(base_label) == _norm(adapt_label)
            reason = "" if agreed else "label_mismatch"
        else:
            agreed = False
            reason = "insufficient_identity_for_comparison"

        return RecommendationComparison(
            agreed=agreed,
            baseline_label=base_label,
            adaptive_label=adapt_label,
            baseline_topic_code=base_code,
            adaptive_topic_code=adapt_code,
            baseline_category=base_cat,
            adaptive_decision_kind=adapt_kind,
            divergence_reason=reason,
            comparable=True,
        )


@dataclass(frozen=True)
class DeterminismReplayResult:
    """Result of replaying AdaptiveEngineExecutor on a frozen input snapshot."""

    success: bool
    first_decision_id: str = ""
    second_decision_id: str = ""
    detail: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "detail": self.detail,
            "first_decision_id": self.first_decision_id,
            "second_decision_id": self.second_decision_id,
            "success": self.success,
        }


class DeterminismMonitor:
    """Verify identical AdaptiveInputBundle → identical AdaptiveOutputBundle."""

    MONITOR_ID = "determinism_monitor"

    def verify_replay(
        self,
        executor: Any,
        inputs: AdaptiveInputBundle,
    ) -> DeterminismReplayResult:
        """Evaluate twice on the same frozen inputs; compare serializations."""
        if executor is None:
            return DeterminismReplayResult(
                success=False,
                detail="executor_unavailable",
            )
        if not isinstance(inputs, AdaptiveInputBundle):
            return DeterminismReplayResult(
                success=False,
                detail="inputs_not_adaptive_input_bundle",
            )
        try:
            first = executor.evaluate(inputs)
            second = executor.evaluate(inputs)
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return DeterminismReplayResult(
                success=False,
                detail=f"evaluate_raised:{type(exc).__name__}",
            )
        if first.serialize() != second.serialize():
            return DeterminismReplayResult(
                success=False,
                first_decision_id=first.decision_id,
                second_decision_id=second.decision_id,
                detail="output_serialize_mismatch",
            )
        return DeterminismReplayResult(
            success=True,
            first_decision_id=first.decision_id,
            second_decision_id=second.decision_id,
            detail="identical_replay",
        )


@dataclass(frozen=True)
class DriftSignal:
    """Single observational drift signal (no automatic correction)."""

    kind: str
    severity: str
    detail: str
    student_id: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "detail": self.detail,
            "kind": self.kind,
            "severity": self.severity,
            "student_id": self.student_id,
        }


class DriftDetectionMonitor:
    """Detect soak drift conditions and emit signal DTOs only."""

    MONITOR_ID = "drift_detection_monitor"

    def detect(
        self,
        *,
        student_id: str,
        comparison: RecommendationComparison | None = None,
        determinism: DeterminismReplayResult | None = None,
        adaptive: AdaptiveOutputBundle | None = None,
        gate_passed: bool | None = None,
        trace_ok: bool | None = None,
        prior_adaptive_topic_code: str | None = None,
    ) -> tuple[DriftSignal, ...]:
        """Return drift signals for unexpected / unsafe observational outcomes.

        Never mutates recommendations or educational state.
        """
        sid = (student_id or "").strip()
        signals: list[DriftSignal] = []

        if determinism is not None and not determinism.success:
            signals.append(
                DriftSignal(
                    kind=DRIFT_DETERMINISM_FAILURE,
                    severity=SEVERITY_CRITICAL,
                    detail=determinism.detail or "determinism_replay_failed",
                    student_id=sid,
                )
            )

        if adaptive is not None and not explanation_is_complete(adaptive):
            signals.append(
                DriftSignal(
                    kind=DRIFT_MISSING_EXPLANATION,
                    severity=SEVERITY_CRITICAL,
                    detail="explanation_bundle_incomplete",
                    student_id=sid,
                )
            )
        elif gate_passed is False:
            signals.append(
                DriftSignal(
                    kind=DRIFT_MISSING_EXPLANATION,
                    severity=SEVERITY_WARN,
                    detail="explainability_gate_failed",
                    student_id=sid,
                )
            )

        if trace_ok is False:
            signals.append(
                DriftSignal(
                    kind=DRIFT_TRACE_FAILURE,
                    severity=SEVERITY_WARN,
                    detail="decision_trace_missing_or_failed",
                    student_id=sid,
                )
            )

        if comparison is not None and comparison.comparable and not comparison.agreed:
            unexplained = comparison.divergence_reason in {
                "topic_code_mismatch",
                "label_mismatch",
                "insufficient_identity_for_comparison",
            }
            if unexplained:
                signals.append(
                    DriftSignal(
                        kind=DRIFT_UNEXPLAINED_DIVERGENCE,
                        severity=SEVERITY_INFO,
                        detail=comparison.divergence_reason,
                        student_id=sid,
                    )
                )

        if (
            prior_adaptive_topic_code is not None
            and adaptive is not None
            and (adaptive.recommendation.topic_code or "").strip()
            and prior_adaptive_topic_code.strip()
            and _norm(prior_adaptive_topic_code)
            != _norm(adaptive.recommendation.topic_code)
        ):
            # Same Runtime A snapshot soak windows should not thrash; when
            # callers supply a prior code for the same snapshot, flag change.
            signals.append(
                DriftSignal(
                    kind=DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE,
                    severity=SEVERITY_WARN,
                    detail=(
                        f"topic_changed:{prior_adaptive_topic_code.strip()}"
                        f"->{adaptive.recommendation.topic_code.strip()}"
                    ),
                    student_id=sid,
                )
            )

        return tuple(signals)


__all__ = [
    "DRIFT_DETERMINISM_FAILURE",
    "DRIFT_KINDS",
    "DRIFT_MISSING_EXPLANATION",
    "DRIFT_TRACE_FAILURE",
    "DRIFT_UNEXPECTED_RECOMMENDATION_CHANGE",
    "DRIFT_UNEXPLAINED_DIVERGENCE",
    "SEVERITY_CRITICAL",
    "SEVERITY_INFO",
    "SEVERITY_WARN",
    "DeterminismMonitor",
    "DeterminismReplayResult",
    "DriftDetectionMonitor",
    "DriftSignal",
    "RecommendationComparison",
    "RecommendationComparisonMonitor",
]
