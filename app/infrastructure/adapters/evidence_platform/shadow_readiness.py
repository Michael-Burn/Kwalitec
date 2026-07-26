"""Readiness evaluation for Evidence Shadow Validation (MS-006 E5).

Produces immutable ReadinessReport artefacts. Never deploys policy. Never
changes educational behaviour. Never mutates Evidence Platform inputs.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    EVIDENCE_VERSION_E5,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.shadow_determinism import (
    DeterminismValidationResult,
)
from app.infrastructure.adapters.evidence_platform.shadow_health import (
    OperationalHealthSnapshot,
)

READINESS_READY = "ready"
READINESS_DEGRADED = "degraded"
READINESS_NOT_READY = "not_ready"
READINESS_UNAVAILABLE = "unavailable"

READINESS_STATUSES = frozenset(
    {
        READINESS_READY,
        READINESS_DEGRADED,
        READINESS_NOT_READY,
        READINESS_UNAVAILABLE,
        "",
    }
)

REPORT_VERSION = EVIDENCE_VERSION_E5
EVALUATOR_VERSION = "1.0.0-e5"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


def _freeze_str_tuple(value: Sequence[str] | None) -> tuple[str, ...]:
    return tuple(str(item) for item in (value or ()))


@dataclass(frozen=True)
class ValidationCoverage:
    """Immutable coverage counts for one readiness evaluation."""

    evidence_records: int = 0
    observations: int = 0
    evaluations: int = 0
    analytics_summaries: int = 0
    projections: int = 0
    subsystems_covered: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "subsystems_covered",
            _freeze_str_tuple(self.subsystems_covered),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "analytics_summaries": self.analytics_summaries,
            "evaluations": self.evaluations,
            "evidence_records": self.evidence_records,
            "observations": self.observations,
            "projections": self.projections,
            "subsystems_covered": list(self.subsystems_covered),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ReadinessReport:
    """Immutable Evidence Platform operational readiness artefact (E5).

    Contains subsystem health, determinism status, validation coverage,
    reproducibility checks, telemetry summary, operational recommendations,
    and version metadata. Never triggers deployment.
    """

    report_id: str = ""
    report_version: str = REPORT_VERSION
    evaluator_version: str = EVALUATOR_VERSION
    as_of: str | None = None
    readiness_status: str = READINESS_NOT_READY
    ok: bool = False
    determinism_ok: bool = False
    coverage: ValidationCoverage = field(default_factory=ValidationCoverage)
    subsystem_health: Mapping[str, Any] = field(default_factory=dict)
    determinism_status: Mapping[str, Any] = field(default_factory=dict)
    reproducibility_checks: tuple[Mapping[str, Any], ...] = ()
    telemetry_summary: Mapping[str, Any] = field(default_factory=dict)
    operational_recommendations: tuple[str, ...] = ()
    drift_signals: tuple[Mapping[str, Any], ...] = ()
    version_metadata: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    influences_student: bool = False
    deploys_policy: bool = False

    def __post_init__(self) -> None:
        status = (self.readiness_status or "").strip().lower()
        if status not in READINESS_STATUSES:
            allowed = sorted(k for k in READINESS_STATUSES if k)
            raise ValueError(f"readiness_status must be one of {allowed} or empty")
        object.__setattr__(self, "readiness_status", status)
        object.__setattr__(self, "report_id", (self.report_id or "").strip())
        if not isinstance(self.coverage, ValidationCoverage):
            raise TypeError("coverage must be a ValidationCoverage")
        object.__setattr__(
            self, "subsystem_health", _freeze_mapping(self.subsystem_health)
        )
        object.__setattr__(
            self, "determinism_status", _freeze_mapping(self.determinism_status)
        )
        object.__setattr__(
            self,
            "reproducibility_checks",
            tuple(
                _freeze_mapping(item)
                for item in (self.reproducibility_checks or ())
            ),
        )
        object.__setattr__(
            self, "telemetry_summary", _freeze_mapping(self.telemetry_summary)
        )
        object.__setattr__(
            self,
            "operational_recommendations",
            _freeze_str_tuple(self.operational_recommendations),
        )
        object.__setattr__(
            self,
            "drift_signals",
            tuple(_freeze_mapping(item) for item in (self.drift_signals or ())),
        )
        object.__setattr__(
            self, "version_metadata", _freeze_mapping(self.version_metadata)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        object.__setattr__(self, "influences_student", False)
        object.__setattr__(self, "deploys_policy", False)
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority": self.authority,
            "coverage": self.coverage.to_canonical_dict(),
            "deploys_policy": self.deploys_policy,
            "determinism_ok": self.determinism_ok,
            "determinism_status": dict(self.determinism_status),
            "drift_signals": [dict(item) for item in self.drift_signals],
            "evaluator_version": self.evaluator_version,
            "influences_student": self.influences_student,
            "limitations": list(self.limitations),
            "ok": self.ok,
            "operational_recommendations": list(self.operational_recommendations),
            "readiness_status": self.readiness_status,
            "report_id": self.report_id,
            "report_version": self.report_version,
            "reproducibility_checks": [
                dict(item) for item in self.reproducibility_checks
            ],
            "subsystem_health": dict(self.subsystem_health),
            "telemetry_summary": dict(self.telemetry_summary),
            "version_metadata": dict(self.version_metadata),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def deterministic_report_id(
    *,
    as_of: str | None,
    coverage: ValidationCoverage,
    determinism_ok: bool,
    readiness_status: str,
) -> str:
    """Stable report id from frozen readiness inputs (no wall clock)."""
    material = serialize_canonical(
        {
            "as_of": as_of,
            "coverage": coverage.to_canonical_dict(),
            "determinism_ok": bool(determinism_ok),
            "readiness_status": readiness_status,
            "report_version": REPORT_VERSION,
        }
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"evidence-readiness-{digest}"


class ReadinessEvaluator:
    """Evaluate Evidence Platform operational readiness from shadow results."""

    EVALUATOR_ID = "evidence_readiness_evaluator"
    EVALUATOR_VERSION = EVALUATOR_VERSION

    def evaluate(
        self,
        *,
        determinism: DeterminismValidationResult,
        health: OperationalHealthSnapshot | None = None,
        coverage: ValidationCoverage | None = None,
        as_of: str | None = None,
        telemetry_summary: Mapping[str, Any] | None = None,
        version_metadata: Mapping[str, Any] | None = None,
        rollback_ok: bool | None = None,
    ) -> ReadinessReport:
        """Produce an immutable ReadinessReport (never deploys)."""
        resolved_coverage = coverage or ValidationCoverage()
        health_dict = (
            {} if health is None else health.to_canonical_dict()
        )
        # Prefer explicit cycle health when provided via telemetry_summary.
        cycle_health = dict((telemetry_summary or {}).get("cycle_health") or {})
        if cycle_health and not health_dict:
            health_dict = cycle_health
        determinism_dict = determinism.to_canonical_dict()
        reproducibility = []
        for check in (
            determinism.evidence,
            determinism.observation,
            determinism.evaluation,
            determinism.analytics,
            determinism.projection,
            determinism.pipeline_replay,
        ):
            if check is not None:
                reproducibility.append(check.to_canonical_dict())

        critical_drift = any(
            (signal.severity == "critical") for signal in determinism.drift_signals
        )
        covered_subsystems = len(resolved_coverage.subsystems_covered)
        full_coverage = covered_subsystems >= 5
        partial_coverage = covered_subsystems >= 3

        recommendations: list[str] = []
        limitations: list[str] = [
            "observational_only",
            "no_policy_deployment",
            "no_educational_authority",
        ]

        if not determinism.success:
            recommendations.append("investigate_determinism_drift_before_ready")
            limitations.append("determinism_incomplete")
        if critical_drift:
            recommendations.append("triage_critical_drift_signals")
        if not full_coverage:
            recommendations.append("expand_validation_coverage_across_subsystems")
            limitations.append("partial_validation_coverage")
        if rollback_ok is False:
            recommendations.append("rehearse_feature_flag_rollback_drill")
            limitations.append("rollback_drill_failed")
        failure_count = 0
        if health is not None:
            failure_count = int(health.failure_count)
        if failure_count > 0:
            recommendations.append("review_shadow_failure_telemetry")
        if not recommendations:
            recommendations.append("continue_observational_shadow_window")
            recommendations.append("await_architecture_review_before_ready_declaration")

        if (
            determinism.success
            and full_coverage
            and not critical_drift
            and rollback_ok is not False
        ):
            status = READINESS_READY
            ok = True
        elif determinism.success and partial_coverage and not critical_drift:
            status = READINESS_DEGRADED
            ok = True
            recommendations.append("coverage_incomplete_treat_as_degraded")
        elif not resolved_coverage.subsystems_covered:
            status = READINESS_UNAVAILABLE
            ok = False
        else:
            status = READINESS_NOT_READY
            ok = False

        report_id = deterministic_report_id(
            as_of=as_of,
            coverage=resolved_coverage,
            determinism_ok=determinism.success,
            readiness_status=status,
        )
        versions = {
            "evaluator_id": self.EVALUATOR_ID,
            "evaluator_version": self.EVALUATOR_VERSION,
            "report_version": REPORT_VERSION,
            "evidence_platform_version": EVIDENCE_VERSION_E5,
            **dict(version_metadata or {}),
        }
        # Strip non-deterministic ops counters from telemetry embedded in report.
        telemetry_for_report = dict(telemetry_summary or {})
        telemetry_for_report.pop("ops_health_executions", None)
        return ReadinessReport(
            report_id=report_id,
            report_version=REPORT_VERSION,
            evaluator_version=self.EVALUATOR_VERSION,
            as_of=as_of,
            readiness_status=status,
            ok=ok,
            determinism_ok=determinism.success,
            coverage=resolved_coverage,
            subsystem_health=health_dict,
            determinism_status=determinism_dict,
            reproducibility_checks=tuple(reproducibility),
            telemetry_summary=telemetry_for_report,
            operational_recommendations=tuple(recommendations),
            drift_signals=tuple(
                signal.to_canonical_dict() for signal in determinism.drift_signals
            ),
            version_metadata=versions,
            limitations=tuple(limitations),
        )


def build_readiness_evaluator() -> ReadinessEvaluator:
    """DI helper — fresh ReadinessEvaluator."""
    return ReadinessEvaluator()


__all__ = [
    "EVALUATOR_VERSION",
    "READINESS_DEGRADED",
    "READINESS_NOT_READY",
    "READINESS_READY",
    "READINESS_STATUSES",
    "READINESS_UNAVAILABLE",
    "REPORT_VERSION",
    "ReadinessEvaluator",
    "ReadinessReport",
    "ValidationCoverage",
    "build_readiness_evaluator",
    "deterministic_report_id",
]
