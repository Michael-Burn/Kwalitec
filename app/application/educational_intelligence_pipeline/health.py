"""Release health checks for the Educational Intelligence Platform.

Operational readiness only — contract versions, component registration,
and certification status. No educational judgement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.educational_intelligence_pipeline.registry import (
    probe_all_registrations,
)
from app.application.educational_intelligence_pipeline.versions import (
    CERTIFICATION_PROGRAMME,
    CERTIFICATION_STATUS,
    ORCHESTRATOR_VERSION,
    PIPELINE_STAGE_ORDER,
)
from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_VERSION,
)
from app.application.learning_graph.projections.versions import PROJECTION_VERSION
from app.application.mission_engine.planning.versions import PLANNING_VERSION
from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.application.reasoning.interpretation.versions import INTERPRETATION_VERSION
from domain.assessment.evidence.models import PACKAGING_VERSION

# Expected certified matrix (mirrors AP-002D7; operational check only).
_EXPECTED_CONTRACTS: dict[str, str] = {
    "packaging": "AP-002C.1",
    "interpretation": "AP-002D2.interpretation.v1",
    "decision": "AP-002D3.decision.v1",
    "projection": "AP-002D4.projection.v1",
    "planning": "AP-002D5.planning.v1",
    "explanation": "AP-002D6.explanation.v1",
}


@dataclass(frozen=True, slots=True)
class HealthCheckItem:
    """Single readiness check result."""

    name: str
    status: str  # ok | error | degraded
    detail: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": self.name, "status": self.status}
        if self.detail:
            payload["detail"] = self.detail
        if self.meta:
            payload["meta"] = self.meta
        return payload


@dataclass(frozen=True, slots=True)
class PlatformHealthReport:
    """Aggregated Educational Intelligence platform readiness."""

    status: str
    ready: bool
    checks: tuple[HealthCheckItem, ...]
    orchestrator_version: str = ORCHESTRATOR_VERSION
    certification_status: str = CERTIFICATION_STATUS

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "ready": self.ready,
            "orchestrator_version": self.orchestrator_version,
            "certification_status": self.certification_status,
            "certification_programme": CERTIFICATION_PROGRAMME,
            "checks": {c.name: c.to_dict() for c in self.checks},
        }


def _live_contracts() -> dict[str, str]:
    return {
        "packaging": PACKAGING_VERSION,
        "interpretation": INTERPRETATION_VERSION,
        "decision": DECISION_VERSION,
        "projection": PROJECTION_VERSION,
        "planning": PLANNING_VERSION,
        "explanation": EXPLANATION_VERSION,
    }


def check_contract_versions() -> HealthCheckItem:
    """Verify certified educational contract versions match the expected matrix."""
    live = _live_contracts()
    drifts: list[str] = []
    for key, expected_version in _EXPECTED_CONTRACTS.items():
        actual = live.get(key)
        if actual != expected_version:
            drifts.append(f"{key}: {actual!r} != {expected_version!r}")
    if drifts:
        return HealthCheckItem(
            name="contract_versions",
            status="error",
            detail="; ".join(drifts),
            meta={"contracts": live},
        )
    return HealthCheckItem(
        name="contract_versions",
        status="ok",
        meta={"contracts": live},
    )


def check_pipeline_registration() -> HealthCheckItem:
    """Confirm the pipeline orchestrator is registered and importable."""
    statuses = {s.name: s for s in probe_all_registrations()}
    orch = statuses.get("pipeline_orchestrator")
    if orch is None or not orch.available:
        return HealthCheckItem(
            name="pipeline_registration",
            status="error",
            detail=orch.detail if orch else "missing registration",
        )
    return HealthCheckItem(
        name="pipeline_registration",
        status="ok",
        meta={"version": orch.version, "stages": list(PIPELINE_STAGE_ORDER)},
    )


def check_projection_registration() -> HealthCheckItem:
    """Confirm Learning Graph projection authority is registered."""
    return _component_check("graph_projection", "projection_registration")


def check_mission_registration() -> HealthCheckItem:
    """Confirm Mission planning authority is registered."""
    return _component_check("mission_planning", "mission_registration")


def check_tutor_registration() -> HealthCheckItem:
    """Confirm Tutor explanation authority is registered."""
    return _component_check("tutor_explanation", "tutor_registration")


def check_certification_status() -> HealthCheckItem:
    """Report Educational Intelligence certification status."""
    if CERTIFICATION_STATUS != "certified":
        return HealthCheckItem(
            name="certification_status",
            status="error",
            detail=f"status is {CERTIFICATION_STATUS!r}, expected 'certified'",
            meta={"programme": CERTIFICATION_PROGRAMME},
        )
    return HealthCheckItem(
        name="certification_status",
        status="ok",
        meta={
            "status": CERTIFICATION_STATUS,
            "programme": CERTIFICATION_PROGRAMME,
        },
    )


def _component_check(component_name: str, check_name: str) -> HealthCheckItem:
    statuses = {s.name: s for s in probe_all_registrations()}
    item = statuses.get(component_name)
    if item is None or not item.available:
        return HealthCheckItem(
            name=check_name,
            status="error",
            detail=item.detail if item else "missing registration",
        )
    return HealthCheckItem(
        name=check_name,
        status="ok",
        meta={"version": item.version, "component": component_name},
    )


class EducationalPlatformHealth:
    """Aggregate platform readiness for release / ops probes."""

    @staticmethod
    def check() -> PlatformHealthReport:
        """Run all Educational Intelligence readiness checks."""
        checks = (
            check_contract_versions(),
            check_pipeline_registration(),
            check_projection_registration(),
            check_mission_registration(),
            check_tutor_registration(),
            check_certification_status(),
        )
        statuses = {c.status for c in checks}
        if "error" in statuses:
            overall = "error"
            ready = False
        elif "degraded" in statuses:
            overall = "degraded"
            ready = False
        else:
            overall = "ok"
            ready = True
        return PlatformHealthReport(
            status=overall,
            ready=ready,
            checks=checks,
        )
