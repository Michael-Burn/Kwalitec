"""Observational monitors for Strategy Shadow Validation (MS-005 S3).

Intervention stability, explainability consistency, projection stability,
and planner consistency — telemetry / measurement only. No automatic
correction. No Experience / Runtime A / Twin / Adaptive influence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.strategy_engine.contracts import (
    LearningIntervention,
    StrategyContext,
    StrategyExplanationBundle,
    StrategyProjection,
)
from app.infrastructure.adapters.strategy_engine.explainability import (
    explanation_is_complete,
)

# Drift kinds (observational; no auto-remediation).
DRIFT_INTERVENTION_INSTABILITY = "intervention_instability"
DRIFT_PROJECTION_INCONSISTENCY = "projection_inconsistency"
DRIFT_EXPLAINABILITY_INCONSISTENCY = "explainability_inconsistency"
DRIFT_PLANNER_INCONSISTENCY = "planner_inconsistency"
DRIFT_MISSING_EXPLANATION = "missing_explanation"
DRIFT_DETERMINISM_FAILURE = "determinism_failure"

DRIFT_KINDS: frozenset[str] = frozenset(
    {
        DRIFT_INTERVENTION_INSTABILITY,
        DRIFT_PROJECTION_INCONSISTENCY,
        DRIFT_EXPLAINABILITY_INCONSISTENCY,
        DRIFT_PLANNER_INCONSISTENCY,
        DRIFT_MISSING_EXPLANATION,
        DRIFT_DETERMINISM_FAILURE,
    }
)

SEVERITY_INFO = "info"
SEVERITY_WARN = "warn"
SEVERITY_CRITICAL = "critical"


@dataclass(frozen=True)
class StabilityResult:
    """Result of replaying a Strategy pipeline stage on frozen inputs."""

    success: bool
    first_fingerprint: str = ""
    second_fingerprint: str = ""
    detail: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "detail": self.detail,
            "first_fingerprint": self.first_fingerprint,
            "second_fingerprint": self.second_fingerprint,
            "success": self.success,
        }


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


class InterventionStabilityMonitor:
    """Verify identical StrategyContext → identical LearningIntervention."""

    MONITOR_ID = "strategy_intervention_stability_monitor"

    def verify_replay(
        self,
        engine: Any,
        context: StrategyContext,
        *,
        intervention: LearningIntervention | None = None,
    ) -> StabilityResult:
        """Evaluate twice (or re-evaluate once against a frozen intervention)."""
        if engine is None:
            return StabilityResult(success=False, detail="engine_unavailable")
        if not isinstance(context, StrategyContext):
            return StabilityResult(
                success=False, detail="context_not_strategy_context"
            )
        try:
            first = (
                intervention
                if intervention is not None
                else engine.evaluate(context)
            )
            second = engine.evaluate(context)
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"evaluate_raised:{type(exc).__name__}",
            )
        if not isinstance(first, LearningIntervention) or not isinstance(
            second, LearningIntervention
        ):
            return StabilityResult(
                success=False, detail="evaluate_did_not_return_intervention"
            )
        first_ser = first.serialize()
        second_ser = second.serialize()
        if first_ser != second_ser:
            return StabilityResult(
                success=False,
                first_fingerprint=first_ser[:64],
                second_fingerprint=second_ser[:64],
                detail="intervention_serialize_mismatch",
            )
        return StabilityResult(
            success=True,
            first_fingerprint=first_ser[:64],
            second_fingerprint=second_ser[:64],
            detail="identical_intervention_replay",
        )


class ExplainabilityConsistencyMonitor:
    """Verify identical LearningIntervention → identical explanation."""

    MONITOR_ID = "strategy_explainability_consistency_monitor"

    def verify_replay(
        self,
        explainability: Any,
        intervention: LearningIntervention,
        *,
        explanation: StrategyExplanationBundle | None = None,
    ) -> StabilityResult:
        """Explain twice from the same intervention; compare serialize()."""
        if explainability is None:
            return StabilityResult(
                success=False, detail="explainability_unavailable"
            )
        if not isinstance(intervention, LearningIntervention):
            return StabilityResult(
                success=False, detail="intervention_not_learning_intervention"
            )
        try:
            first = (
                explanation
                if explanation is not None
                else explainability.explain(intervention)
            )
            second = explainability.explain(intervention)
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"explain_raised:{type(exc).__name__}",
            )
        if not isinstance(first, StrategyExplanationBundle) or not isinstance(
            second, StrategyExplanationBundle
        ):
            return StabilityResult(
                success=False, detail="explain_did_not_return_explanation"
            )
        first_ser = first.serialize()
        second_ser = second.serialize()
        if first_ser != second_ser:
            return StabilityResult(
                success=False,
                first_fingerprint=first_ser[:64],
                second_fingerprint=second_ser[:64],
                detail="explanation_serialize_mismatch",
            )
        return StabilityResult(
            success=True,
            first_fingerprint=first_ser[:64],
            second_fingerprint=second_ser[:64],
            detail="identical_explanation_replay",
        )


class ProjectionConsistencyMonitor:
    """Verify identical LearningIntervention → identical StrategyProjection."""

    MONITOR_ID = "strategy_projection_consistency_monitor"

    def verify_replay(
        self,
        projector: Any,
        intervention: LearningIntervention,
        *,
        explanation: StrategyExplanationBundle | None = None,
        student_id: str | None = None,
        as_of: str | None = None,
        projection: StrategyProjection | None = None,
    ) -> StabilityResult:
        """Project twice from the same intervention; compare serialize()."""
        if projector is None:
            return StabilityResult(success=False, detail="projector_unavailable")
        if not isinstance(intervention, LearningIntervention):
            return StabilityResult(
                success=False, detail="intervention_not_learning_intervention"
            )
        sid = (student_id or "").strip() or None
        try:
            first = (
                projection
                if projection is not None
                else projector.project(
                    intervention,
                    explanation=explanation,
                    student_id=sid,
                    as_of=as_of,
                )
            )
            second = projector.project(
                intervention,
                explanation=explanation,
                student_id=sid,
                as_of=as_of,
            )
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"project_raised:{type(exc).__name__}",
            )
        if not isinstance(first, StrategyProjection) or not isinstance(
            second, StrategyProjection
        ):
            return StabilityResult(
                success=False, detail="project_did_not_return_projection"
            )
        first_ser = first.serialize()
        second_ser = second.serialize()
        if first_ser != second_ser:
            return StabilityResult(
                success=False,
                first_fingerprint=first_ser[:64],
                second_fingerprint=second_ser[:64],
                detail="projection_serialize_mismatch",
            )
        return StabilityResult(
            success=True,
            first_fingerprint=first_ser[:64],
            second_fingerprint=second_ser[:64],
            detail="identical_projection_replay",
        )


class PlannerConsistencyMonitor:
    """Verify planner outputs inside LearningIntervention stay coherent."""

    MONITOR_ID = "strategy_planner_consistency_monitor"

    def verify(
        self,
        intervention: LearningIntervention,
        context: StrategyContext,
    ) -> StabilityResult:
        """Check primary kind / Adaptive topic / mission coherence."""
        if not isinstance(intervention, LearningIntervention):
            return StabilityResult(
                success=False, detail="intervention_not_learning_intervention"
            )
        if not isinstance(context, StrategyContext):
            return StabilityResult(
                success=False, detail="context_not_strategy_context"
            )

        if not (intervention.kind or "").strip():
            return StabilityResult(
                success=False, detail="primary_kind_empty"
            )
        if intervention.sequencing.primary_kind != intervention.kind:
            return StabilityResult(
                success=False,
                detail="sequencing_primary_kind_mismatch",
                first_fingerprint=intervention.kind,
                second_fingerprint=intervention.sequencing.primary_kind,
            )

        adaptive = dict(context.adaptive or {})
        recommendation = dict(adaptive.get("recommendation") or {})
        adaptive_topic = str(
            recommendation.get("topic_code")
            or recommendation.get("topic_id")
            or ""
        ).strip()
        if adaptive_topic:
            study_topics = tuple(intervention.study.focus_topics or ())
            if study_topics and study_topics[0] != adaptive_topic:
                return StabilityResult(
                    success=False,
                    detail="study_focus_diverged_from_adaptive",
                    first_fingerprint=adaptive_topic,
                    second_fingerprint=study_topics[0],
                )
            revision_topic = (
                intervention.revision.primary_revision_topic or ""
            ).strip()
            if revision_topic and revision_topic != adaptive_topic:
                return StabilityResult(
                    success=False,
                    detail="revision_primary_diverged_from_adaptive",
                    first_fingerprint=adaptive_topic,
                    second_fingerprint=revision_topic,
                )

        mission = dict((context.runtime_a or {}).get("mission") or {})
        mission_topic = str(
            mission.get("topic_code") or mission.get("topic_id") or ""
        ).strip()
        session_topic = (intervention.session.primary_topic or "").strip()
        if mission_topic and session_topic and session_topic != mission_topic:
            return StabilityResult(
                success=False,
                detail="session_primary_diverged_from_mission",
                first_fingerprint=mission_topic,
                second_fingerprint=session_topic,
            )

        fingerprint = (
            f"{intervention.kind}|{intervention.sequencing.primary_kind}|"
            f"{'|'.join(intervention.study.focus_topics or ())}|"
            f"{intervention.session.primary_topic}|"
            f"{intervention.revision.primary_revision_topic}"
        )
        return StabilityResult(
            success=True,
            first_fingerprint=fingerprint[:64],
            second_fingerprint=fingerprint[:64],
            detail="planner_outputs_coherent",
        )


class StrategyDriftDetectionMonitor:
    """Detect shadow-validation drift conditions and emit signal DTOs only."""

    MONITOR_ID = "strategy_drift_detection_monitor"

    def detect(
        self,
        *,
        student_id: str,
        intervention_stability: StabilityResult | None = None,
        projection_stability: StabilityResult | None = None,
        explainability_stability: StabilityResult | None = None,
        planner_consistency: StabilityResult | None = None,
        explanation: StrategyExplanationBundle | None = None,
        determinism_success: bool | None = None,
    ) -> tuple[DriftSignal, ...]:
        """Return drift signals for unstable / incomplete observational outcomes."""
        sid = (student_id or "").strip()
        signals: list[DriftSignal] = []

        if (
            intervention_stability is not None
            and not intervention_stability.success
        ):
            signals.append(
                DriftSignal(
                    kind=DRIFT_INTERVENTION_INSTABILITY,
                    severity=SEVERITY_CRITICAL,
                    detail=(
                        intervention_stability.detail or "intervention_unstable"
                    ),
                    student_id=sid,
                )
            )

        if projection_stability is not None and not projection_stability.success:
            signals.append(
                DriftSignal(
                    kind=DRIFT_PROJECTION_INCONSISTENCY,
                    severity=SEVERITY_CRITICAL,
                    detail=(
                        projection_stability.detail or "projection_inconsistent"
                    ),
                    student_id=sid,
                )
            )

        if (
            explainability_stability is not None
            and not explainability_stability.success
        ):
            signals.append(
                DriftSignal(
                    kind=DRIFT_EXPLAINABILITY_INCONSISTENCY,
                    severity=SEVERITY_CRITICAL,
                    detail=(
                        explainability_stability.detail
                        or "explainability_inconsistent"
                    ),
                    student_id=sid,
                )
            )

        if planner_consistency is not None and not planner_consistency.success:
            signals.append(
                DriftSignal(
                    kind=DRIFT_PLANNER_INCONSISTENCY,
                    severity=SEVERITY_CRITICAL,
                    detail=(
                        planner_consistency.detail or "planner_inconsistent"
                    ),
                    student_id=sid,
                )
            )

        if explanation is not None and not explanation_is_complete(explanation):
            signals.append(
                DriftSignal(
                    kind=DRIFT_MISSING_EXPLANATION,
                    severity=SEVERITY_CRITICAL,
                    detail="strategy_explanation_incomplete",
                    student_id=sid,
                )
            )

        if determinism_success is False:
            signals.append(
                DriftSignal(
                    kind=DRIFT_DETERMINISM_FAILURE,
                    severity=SEVERITY_CRITICAL,
                    detail="deterministic_replay_failed",
                    student_id=sid,
                )
            )

        return tuple(signals)


__all__ = [
    "DRIFT_DETERMINISM_FAILURE",
    "DRIFT_EXPLAINABILITY_INCONSISTENCY",
    "DRIFT_INTERVENTION_INSTABILITY",
    "DRIFT_KINDS",
    "DRIFT_MISSING_EXPLANATION",
    "DRIFT_PLANNER_INCONSISTENCY",
    "DRIFT_PROJECTION_INCONSISTENCY",
    "SEVERITY_CRITICAL",
    "SEVERITY_INFO",
    "SEVERITY_WARN",
    "DriftSignal",
    "ExplainabilityConsistencyMonitor",
    "InterventionStabilityMonitor",
    "PlannerConsistencyMonitor",
    "ProjectionConsistencyMonitor",
    "StabilityResult",
    "StrategyDriftDetectionMonitor",
    "explanation_is_complete",
]
