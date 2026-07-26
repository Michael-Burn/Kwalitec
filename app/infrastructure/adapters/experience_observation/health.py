"""Pipeline health checks for Experience Observation diagnostics (P2-MS007).

Operational readiness only — never educational authority or student UX.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

HEALTH_STATUS_OK = "ok"
HEALTH_STATUS_DEGRADED = "degraded"
HEALTH_STATUS_UNAVAILABLE = "unavailable"
HEALTH_STATUSES = frozenset(
    {
        HEALTH_STATUS_OK,
        HEALTH_STATUS_DEGRADED,
        HEALTH_STATUS_UNAVAILABLE,
    }
)

CHECK_PUBLISHER = "observation_publisher"
CHECK_EVIDENCE_INTAKE = "evidence_intake"
CHECK_FEATURE_FLAGS = "feature_flag_consistency"
CHECK_DI_WIRING = "dependency_injection_wiring"


@dataclass(frozen=True)
class HealthCheckResult:
    """Immutable result of one operational health check."""

    name: str
    status: str
    ok: bool
    detail: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", (self.name or "").strip())
        status = (self.status or "").strip().lower()
        if status not in HEALTH_STATUSES:
            raise ValueError(f"unknown health status: {self.status!r}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "ok", bool(self.ok))
        object.__setattr__(self, "detail", (self.detail or "").strip())
        if not self.name:
            raise ValueError("health check name is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "detail": self.detail,
            "name": self.name,
            "ok": self.ok,
            "status": self.status,
        }


@dataclass(frozen=True)
class PipelineHealthReport:
    """Aggregate pipeline health for Observation → Evidence."""

    overall_status: str
    overall_ok: bool
    checks: tuple[HealthCheckResult, ...]
    publisher_available: bool = False
    evidence_intake_available: bool = False
    diagnostics_enabled: bool = False
    observation_flag: bool = False
    evidence_flag: bool = False

    def __post_init__(self) -> None:
        status = (self.overall_status or "").strip().lower()
        if status not in HEALTH_STATUSES:
            raise ValueError(f"unknown overall_status: {self.overall_status!r}")
        object.__setattr__(self, "overall_status", status)
        object.__setattr__(self, "overall_ok", bool(self.overall_ok))
        object.__setattr__(self, "checks", tuple(self.checks))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "checks": [c.to_canonical_dict() for c in self.checks],
            "diagnostics_enabled": self.diagnostics_enabled,
            "evidence_flag": self.evidence_flag,
            "evidence_intake_available": self.evidence_intake_available,
            "observation_flag": self.observation_flag,
            "overall_ok": self.overall_ok,
            "overall_status": self.overall_status,
            "publisher_available": self.publisher_available,
        }


def _roll_up(checks: tuple[HealthCheckResult, ...]) -> tuple[str, bool]:
    if not checks:
        return HEALTH_STATUS_UNAVAILABLE, False
    if all(c.ok and c.status == HEALTH_STATUS_OK for c in checks):
        return HEALTH_STATUS_OK, True
    if any(c.status == HEALTH_STATUS_UNAVAILABLE for c in checks):
        # Degraded when some paths work; unavailable only if all critical fail.
        if any(c.ok for c in checks):
            return HEALTH_STATUS_DEGRADED, False
        return HEALTH_STATUS_UNAVAILABLE, False
    return HEALTH_STATUS_DEGRADED, False


@dataclass(frozen=True)
class PipelineHealthChecker:
    """Evaluate Observation Publisher / Evidence / flag / DI health."""

    diagnostics_enabled: bool = False
    observation_flag: bool = False
    evidence_flag: bool = False
    publisher: Any | None = None
    evidence: Any | None = None

    def check_publisher(self) -> HealthCheckResult:
        """Publisher construct + enabled surface."""
        if not self.observation_flag:
            return HealthCheckResult(
                name=CHECK_PUBLISHER,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="ENABLE_EXPERIENCE_OBSERVATION is OFF",
            )
        if self.publisher is None:
            return HealthCheckResult(
                name=CHECK_PUBLISHER,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="publisher not injected despite observation flag ON",
            )
        enabled = bool(getattr(self.publisher, "enabled", False))
        if not enabled:
            return HealthCheckResult(
                name=CHECK_PUBLISHER,
                status=HEALTH_STATUS_DEGRADED,
                ok=False,
                detail="publisher present but enabled=False",
            )
        return HealthCheckResult(
            name=CHECK_PUBLISHER,
            status=HEALTH_STATUS_OK,
            ok=True,
            detail="publisher available",
        )

    def check_evidence_intake(self) -> HealthCheckResult:
        """Evidence public intake availability for observation publish."""
        if not self.evidence_flag:
            return HealthCheckResult(
                name=CHECK_EVIDENCE_INTAKE,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="ENABLE_EVIDENCE_PLATFORM is OFF",
            )
        if self.evidence is None:
            return HealthCheckResult(
                name=CHECK_EVIDENCE_INTAKE,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="Evidence adapter not injected despite evidence flag ON",
            )
        if not hasattr(self.evidence, "collect_event"):
            return HealthCheckResult(
                name=CHECK_EVIDENCE_INTAKE,
                status=HEALTH_STATUS_DEGRADED,
                ok=False,
                detail="Evidence sink missing collect_event",
            )
        return HealthCheckResult(
            name=CHECK_EVIDENCE_INTAKE,
            status=HEALTH_STATUS_OK,
            ok=True,
            detail="Evidence intake available",
        )

    def check_feature_flags(self) -> HealthCheckResult:
        """Flag consistency for diagnostics / observation / evidence."""
        if not self.diagnostics_enabled:
            return HealthCheckResult(
                name=CHECK_FEATURE_FLAGS,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="ENABLE_EXPERIENCE_DIAGNOSTICS is OFF",
            )
        # Independent flags are valid in any combination; consistency means
        # boolean fields are present and independently resolved (always true
        # once diagnostics is ON). Surface the matrix for operators.
        detail = (
            f"diagnostics=on observation={'on' if self.observation_flag else 'off'} "
            f"evidence={'on' if self.evidence_flag else 'off'}"
        )
        return HealthCheckResult(
            name=CHECK_FEATURE_FLAGS,
            status=HEALTH_STATUS_OK,
            ok=True,
            detail=detail,
        )

    def check_di_wiring(self) -> HealthCheckResult:
        """Publisher ↔ Evidence DI wiring integrity."""
        if not self.observation_flag:
            return HealthCheckResult(
                name=CHECK_DI_WIRING,
                status=HEALTH_STATUS_OK,
                ok=True,
                detail="observation OFF — no publisher wiring required",
            )
        if self.publisher is None:
            return HealthCheckResult(
                name=CHECK_DI_WIRING,
                status=HEALTH_STATUS_UNAVAILABLE,
                ok=False,
                detail="observation ON but publisher missing from composition",
            )
        pub_evidence = getattr(self.publisher, "evidence", None)
        if self.evidence_flag:
            if pub_evidence is None:
                return HealthCheckResult(
                    name=CHECK_DI_WIRING,
                    status=HEALTH_STATUS_DEGRADED,
                    ok=False,
                    detail=(
                        "both flags ON but publisher.evidence is None "
                        "(publish will skip)"
                    ),
                )
            if self.evidence is not None and pub_evidence is not self.evidence:
                return HealthCheckResult(
                    name=CHECK_DI_WIRING,
                    status=HEALTH_STATUS_DEGRADED,
                    ok=False,
                    detail="publisher.evidence is not composition evidence_platform",
                )
            return HealthCheckResult(
                name=CHECK_DI_WIRING,
                status=HEALTH_STATUS_OK,
                ok=True,
                detail="publisher wired to Evidence intake",
            )
        # Observation ON, Evidence OFF — publisher may exist with sink None.
        if pub_evidence is not None:
            return HealthCheckResult(
                name=CHECK_DI_WIRING,
                status=HEALTH_STATUS_DEGRADED,
                ok=False,
                detail="evidence flag OFF but publisher has a non-None sink",
            )
        return HealthCheckResult(
            name=CHECK_DI_WIRING,
            status=HEALTH_STATUS_OK,
            ok=True,
            detail="publisher present; Evidence sink intentionally None",
        )

    def evaluate(self) -> PipelineHealthReport:
        """Run all pipeline health checks and roll up overall status."""
        checks = (
            self.check_publisher(),
            self.check_evidence_intake(),
            self.check_feature_flags(),
            self.check_di_wiring(),
        )
        overall_status, overall_ok = _roll_up(checks)
        publisher_ok = checks[0].ok
        evidence_ok = checks[1].ok
        return PipelineHealthReport(
            overall_status=overall_status,
            overall_ok=overall_ok,
            checks=checks,
            publisher_available=publisher_ok,
            evidence_intake_available=evidence_ok,
            diagnostics_enabled=self.diagnostics_enabled,
            observation_flag=self.observation_flag,
            evidence_flag=self.evidence_flag,
        )


def build_pipeline_health_checker(
    *,
    diagnostics_enabled: bool = False,
    observation_flag: bool = False,
    evidence_flag: bool = False,
    publisher: Any | None = None,
    evidence: Any | None = None,
) -> PipelineHealthChecker:
    """DI helper for PipelineHealthChecker."""
    return PipelineHealthChecker(
        diagnostics_enabled=diagnostics_enabled,
        observation_flag=observation_flag,
        evidence_flag=evidence_flag,
        publisher=publisher,
        evidence=evidence,
    )
