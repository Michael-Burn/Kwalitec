"""EP-002.3 Twin & Authority soak contracts.

Observational only — no student UX influence, no HTTP cutover.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Matrix cell identifiers (Soak Plan §2).
CELL_TWIN_OFF_AUTHORITY_OFF = "A_twin_off_authority_off"
CELL_TWIN_OFF_AUTHORITY_ENV = "B_twin_off_authority_env"
CELL_TWIN_ON_AUTHORITY_OFF = "C_twin_on_authority_off"
CELL_TWIN_ON_AUTHORITY_ON = "D_twin_on_authority_on"
CELL_ROLLBACK = "E_rollback"

SOAK_MATRIX_CELLS: tuple[str, ...] = (
    CELL_TWIN_OFF_AUTHORITY_OFF,
    CELL_TWIN_OFF_AUTHORITY_ENV,
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    CELL_ROLLBACK,
)

SOAK_ADAPTER_ID = "consumer_chain_twin_authority_soak"
SOAK_ADAPTER_VERSION = "ep002.3.0"

LOG_SOAK_REQUESTED = "consumer_chain.soak.requested"
LOG_SOAK_COMPLETED = "consumer_chain.soak.completed"
LOG_SOAK_FAILED = "consumer_chain.soak.failed"
LOG_SOAK_HEALTH = "consumer_chain.soak.health"
LOG_SOAK_ROLLBACK = "consumer_chain.soak.rollback"
LOG_SOAK_MATRIX = "consumer_chain.soak.matrix"

TWINPORT_EXPERIENCE = "ExperienceTwinAdapter"
TWINPORT_FOUNDATION_AUTHORITY = "StudentTwinFoundationAuthorityPort"


@dataclass(frozen=True)
class FlagMatrixCell:
    """One Twin × Authority configuration observation."""

    cell_id: str
    twin_env: bool
    authority_env: bool
    twin_resolved: bool
    authority_resolved: bool
    twin_port_kind: str
    build_apis_available: bool
    ok: bool
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_env": self.authority_env,
            "authority_resolved": self.authority_resolved,
            "build_apis_available": self.build_apis_available,
            "cell_id": self.cell_id,
            "details": list(self.details),
            "ok": self.ok,
            "twin_env": self.twin_env,
            "twin_port_kind": self.twin_port_kind,
            "twin_resolved": self.twin_resolved,
        }


@dataclass(frozen=True)
class SoakApiObservation:
    """One observational build_* invocation during soak."""

    api_name: str
    student_id: str
    twin_enabled: bool
    authority_enabled: bool
    outcome: str
    latency_ms: float
    returned_none: bool
    limitation_codes: tuple[str, ...] = ()
    error_code: str = ""
    ok: bool = True

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "api_name": self.api_name,
            "authority_enabled": self.authority_enabled,
            "error_code": self.error_code,
            "latency_ms": round(float(self.latency_ms), 3),
            "limitation_codes": list(self.limitation_codes),
            "ok": self.ok,
            "outcome": self.outcome,
            "returned_none": self.returned_none,
            "student_id": self.student_id,
            "twin_enabled": self.twin_enabled,
        }


@dataclass(frozen=True)
class TwinAuthoritySoakReport:
    """Aggregated non-production soak report."""

    ok: bool
    soak_duration_ms: float
    requests_exercised: int
    average_latency_ms: float
    p95_latency_ms: float
    foundation_assemble_count: int
    share_hit_count: int
    share_hit_rate: float
    failure_count: int
    exception_count: int
    limitation_code_counts: dict[str, int] = field(default_factory=dict)
    matrix_cells: tuple[FlagMatrixCell, ...] = ()
    rollback_success: bool = False
    ownership_violations: int = 0
    behavioural_regressions: int = 0
    observations: tuple[SoakApiObservation, ...] = ()
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "average_latency_ms": self.average_latency_ms,
            "behavioural_regressions": self.behavioural_regressions,
            "details": list(self.details),
            "exception_count": self.exception_count,
            "failure_count": self.failure_count,
            "foundation_assemble_count": self.foundation_assemble_count,
            "limitation_code_counts": dict(self.limitation_code_counts),
            "matrix_cells": [c.to_canonical_dict() for c in self.matrix_cells],
            "observations": [o.to_canonical_dict() for o in self.observations],
            "ok": self.ok,
            "ownership_violations": self.ownership_violations,
            "p95_latency_ms": self.p95_latency_ms,
            "requests_exercised": self.requests_exercised,
            "rollback_success": self.rollback_success,
            "share_hit_count": self.share_hit_count,
            "share_hit_rate": self.share_hit_rate,
            "soak_duration_ms": round(float(self.soak_duration_ms), 3),
        }


__all__ = [
    "CELL_ROLLBACK",
    "CELL_TWIN_OFF_AUTHORITY_ENV",
    "CELL_TWIN_OFF_AUTHORITY_OFF",
    "CELL_TWIN_ON_AUTHORITY_OFF",
    "CELL_TWIN_ON_AUTHORITY_ON",
    "FlagMatrixCell",
    "LOG_SOAK_COMPLETED",
    "LOG_SOAK_FAILED",
    "LOG_SOAK_HEALTH",
    "LOG_SOAK_MATRIX",
    "LOG_SOAK_REQUESTED",
    "LOG_SOAK_ROLLBACK",
    "SOAK_ADAPTER_ID",
    "SOAK_ADAPTER_VERSION",
    "SOAK_MATRIX_CELLS",
    "SoakApiObservation",
    "TWINPORT_EXPERIENCE",
    "TWINPORT_FOUNDATION_AUTHORITY",
    "TwinAuthoritySoakReport",
]
