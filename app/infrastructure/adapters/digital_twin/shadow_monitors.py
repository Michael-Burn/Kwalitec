"""Observational monitors for Twin Shadow Validation (MS-004 T6).

Snapshot stability, projection consistency, and explainability consistency —
telemetry / measurement only. No automatic correction. No Experience /
Runtime A / Adaptive influence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    SnapshotExplanation,
    StudentTwinProjection,
    TwinSnapshot,
)

# Drift kinds (observational; no auto-remediation).
DRIFT_SNAPSHOT_INSTABILITY = "snapshot_instability"
DRIFT_PROJECTION_INCONSISTENCY = "projection_inconsistency"
DRIFT_EXPLAINABILITY_INCONSISTENCY = "explainability_inconsistency"
DRIFT_MISSING_EXPLANATION = "missing_explanation"
DRIFT_UNAVAILABLE_FACETS = "unavailable_facets"
DRIFT_DETERMINISM_FAILURE = "determinism_failure"

DRIFT_KINDS: frozenset[str] = frozenset(
    {
        DRIFT_SNAPSHOT_INSTABILITY,
        DRIFT_PROJECTION_INCONSISTENCY,
        DRIFT_EXPLAINABILITY_INCONSISTENCY,
        DRIFT_MISSING_EXPLANATION,
        DRIFT_UNAVAILABLE_FACETS,
        DRIFT_DETERMINISM_FAILURE,
    }
)

SEVERITY_INFO = "info"
SEVERITY_WARN = "warn"
SEVERITY_CRITICAL = "critical"


def explanation_is_complete(explanation: SnapshotExplanation | None) -> bool:
    """Return True when SnapshotExplanation has required T3 facets populated."""
    if explanation is None:
        return False
    if not explanation.twin_id and not explanation.student_id:
        return False
    if not (explanation.overall_completeness_explanation or "").strip():
        return False
    if not (explanation.evidence_coverage_summary or "").strip():
        return False
    if explanation.facet_explanations is None:
        return False
    if len(explanation.facet_explanations) == 0:
        return False
    if explanation.provenance_refs is None:
        return False
    return True


@dataclass(frozen=True)
class StabilityResult:
    """Result of replaying a Twin pipeline stage on frozen inputs."""

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


class SnapshotStabilityMonitor:
    """Verify identical Runtime A as_of → identical TwinSnapshot.serialize()."""

    MONITOR_ID = "twin_snapshot_stability_monitor"

    def verify_replay(
        self,
        builder: Any,
        student_id: str,
        *,
        as_of: str | None = None,
        snapshot: TwinSnapshot | None = None,
    ) -> StabilityResult:
        """Build twice (or rebuild once against a frozen snapshot) and compare."""
        if builder is None:
            return StabilityResult(success=False, detail="builder_unavailable")
        sid = (student_id or "").strip()
        if not sid:
            return StabilityResult(success=False, detail="student_id_empty")
        # Prefer explicit as_of; fall back to frozen snapshot clock so replay
        # does not pick up wall-clock drift when callers omit as_of.
        replay_as_of = as_of
        if replay_as_of is None and snapshot is not None:
            replay_as_of = snapshot.generated_at
        try:
            first = snapshot if snapshot is not None else builder.build(
                sid, as_of=replay_as_of
            )
            second = builder.build(sid, as_of=replay_as_of)
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"build_raised:{type(exc).__name__}",
            )
        if not isinstance(first, TwinSnapshot) or not isinstance(
            second, TwinSnapshot
        ):
            return StabilityResult(
                success=False, detail="build_did_not_return_twin_snapshot"
            )
        first_ser = first.serialize()
        second_ser = second.serialize()
        if first_ser != second_ser:
            return StabilityResult(
                success=False,
                first_fingerprint=first_ser[:64],
                second_fingerprint=second_ser[:64],
                detail="snapshot_serialize_mismatch",
            )
        return StabilityResult(
            success=True,
            first_fingerprint=first_ser[:64],
            second_fingerprint=second_ser[:64],
            detail="identical_snapshot_replay",
        )


class ProjectionConsistencyMonitor:
    """Verify identical TwinSnapshot → identical StudentTwinProjection."""

    MONITOR_ID = "twin_projection_consistency_monitor"

    def verify_replay(
        self,
        projector: Any,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
        as_of: str | None = None,
        projection: StudentTwinProjection | None = None,
    ) -> StabilityResult:
        """Project twice from the same snapshot; compare serialize()."""
        if projector is None:
            return StabilityResult(success=False, detail="projector_unavailable")
        if not isinstance(snapshot, TwinSnapshot):
            return StabilityResult(
                success=False, detail="snapshot_not_twin_snapshot"
            )
        try:
            first = (
                projection
                if projection is not None
                else projector.project(
                    snapshot, explanation=explanation, as_of=as_of
                )
            )
            second = projector.project(
                snapshot, explanation=explanation, as_of=as_of
            )
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"project_raised:{type(exc).__name__}",
            )
        if not isinstance(first, StudentTwinProjection) or not isinstance(
            second, StudentTwinProjection
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


class ExplainabilityConsistencyMonitor:
    """Verify identical TwinSnapshot → identical SnapshotExplanation."""

    MONITOR_ID = "twin_explainability_consistency_monitor"

    def verify_replay(
        self,
        explainability: Any,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
    ) -> StabilityResult:
        """Explain twice from the same snapshot; compare serialize()."""
        if explainability is None:
            return StabilityResult(
                success=False, detail="explainability_unavailable"
            )
        if not isinstance(snapshot, TwinSnapshot):
            return StabilityResult(
                success=False, detail="snapshot_not_twin_snapshot"
            )
        try:
            first = (
                explanation
                if explanation is not None
                else explainability.explain_snapshot(snapshot)
            )
            second = explainability.explain_snapshot(snapshot)
        except Exception as exc:  # noqa: BLE001 — observational monitor
            return StabilityResult(
                success=False,
                detail=f"explain_raised:{type(exc).__name__}",
            )
        if not isinstance(first, SnapshotExplanation) or not isinstance(
            second, SnapshotExplanation
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


class TwinDriftDetectionMonitor:
    """Detect shadow-validation drift conditions and emit signal DTOs only."""

    MONITOR_ID = "twin_drift_detection_monitor"

    def detect(
        self,
        *,
        student_id: str,
        snapshot_stability: StabilityResult | None = None,
        projection_stability: StabilityResult | None = None,
        explainability_stability: StabilityResult | None = None,
        explanation: SnapshotExplanation | None = None,
        snapshot: TwinSnapshot | None = None,
        determinism_success: bool | None = None,
    ) -> tuple[DriftSignal, ...]:
        """Return drift signals for unstable / incomplete observational outcomes."""
        sid = (student_id or "").strip()
        signals: list[DriftSignal] = []

        if snapshot_stability is not None and not snapshot_stability.success:
            signals.append(
                DriftSignal(
                    kind=DRIFT_SNAPSHOT_INSTABILITY,
                    severity=SEVERITY_CRITICAL,
                    detail=snapshot_stability.detail or "snapshot_unstable",
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

        if explanation is not None and not explanation_is_complete(explanation):
            signals.append(
                DriftSignal(
                    kind=DRIFT_MISSING_EXPLANATION,
                    severity=SEVERITY_CRITICAL,
                    detail="snapshot_explanation_incomplete",
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

        if snapshot is not None:
            unavailable = tuple(
                name
                for name in (snapshot.completeness.facets_unavailable or ())
                if name
            )
            if unavailable:
                profile_unavailable = [
                    name
                    for name in unavailable
                    if getattr(
                        getattr(snapshot.profile, name, None),
                        "availability",
                        "",
                    )
                    != AVAILABILITY_AVAILABLE
                ]
                signals.append(
                    DriftSignal(
                        kind=DRIFT_UNAVAILABLE_FACETS,
                        severity=SEVERITY_INFO,
                        detail=(
                            "unavailable_facets="
                            + ",".join(profile_unavailable or unavailable)
                        ),
                        student_id=sid,
                    )
                )

        return tuple(signals)


__all__ = [
    "DRIFT_DETERMINISM_FAILURE",
    "DRIFT_EXPLAINABILITY_INCONSISTENCY",
    "DRIFT_KINDS",
    "DRIFT_MISSING_EXPLANATION",
    "DRIFT_PROJECTION_INCONSISTENCY",
    "DRIFT_SNAPSHOT_INSTABILITY",
    "DRIFT_UNAVAILABLE_FACETS",
    "SEVERITY_CRITICAL",
    "SEVERITY_INFO",
    "SEVERITY_WARN",
    "DriftSignal",
    "ExplainabilityConsistencyMonitor",
    "ProjectionConsistencyMonitor",
    "SnapshotStabilityMonitor",
    "StabilityResult",
    "TwinDriftDetectionMonitor",
    "explanation_is_complete",
]
