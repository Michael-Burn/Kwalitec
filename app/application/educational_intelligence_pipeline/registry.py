"""Component registration for Educational Intelligence release health.

Registration confirms certified stage packages are importable and versioned.
It introduces no educational logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from app.application.educational_intelligence_pipeline.versions import (
    CERTIFICATION_PROGRAMME,
    CERTIFICATION_STATUS,
    ORCHESTRATOR_VERSION,
    PIPELINE_STAGE_ORDER,
)


@dataclass(frozen=True, slots=True)
class ComponentRegistration:
    """Descriptor for a registered pipeline component."""

    name: str
    module_path: str
    symbol: str
    version_module: str
    version_attr: str
    role: str


# Canonical registrations — certified Educational Intelligence Platform stages.
COMPONENT_REGISTRATIONS: tuple[ComponentRegistration, ...] = (
    ComponentRegistration(
        name="pipeline_orchestrator",
        module_path="app.application.educational_intelligence_pipeline.orchestrator",
        symbol="EducationalPipelineOrchestrator",
        version_module="app.application.educational_intelligence_pipeline.versions",
        version_attr="ORCHESTRATOR_VERSION",
        role="pipeline",
    ),
    ComponentRegistration(
        name="interpretation",
        module_path="app.application.reasoning.interpretation.evidence_interpreter",
        symbol="EvidenceInterpreter",
        version_module="app.application.reasoning.interpretation.versions",
        version_attr="INTERPRETATION_VERSION",
        role="interpretation",
    ),
    ComponentRegistration(
        name="decision",
        module_path="app.application.reasoning.decisions.decision_generator",
        symbol="DecisionGenerator",
        version_module="app.application.reasoning.decisions.versions",
        version_attr="DECISION_VERSION",
        role="decision",
    ),
    ComponentRegistration(
        name="twin_update",
        module_path="app.application.reasoning.decisions.twin_updater",
        symbol="TwinUpdater",
        version_module="app.application.reasoning.decisions.versions",
        version_attr="DECISION_VERSION",
        role="twin",
    ),
    ComponentRegistration(
        name="graph_projection",
        module_path="app.application.learning_graph.projections.twin_projection_service",
        symbol="TwinProjectionService",
        version_module="app.application.learning_graph.projections.versions",
        version_attr="PROJECTION_VERSION",
        role="projection",
    ),
    ComponentRegistration(
        name="mission_planning",
        module_path="app.application.mission_engine.planning.mission_planning_service",
        symbol="MissionPlanningService",
        version_module="app.application.mission_engine.planning.versions",
        version_attr="PLANNING_VERSION",
        role="mission",
    ),
    ComponentRegistration(
        name="tutor_explanation",
        module_path=(
            "app.application.intelligent_tutor.explainability.tutor_explanation_service"
        ),
        symbol="TutorExplanationService",
        version_module="app.application.intelligent_tutor.explainability.versions",
        version_attr="EXPLANATION_VERSION",
        role="tutor",
    ),
)


@dataclass(frozen=True, slots=True)
class RegistrationStatus:
    """Result of probing one registered component."""

    name: str
    role: str
    available: bool
    version: str | None
    detail: str = ""


def probe_registration(reg: ComponentRegistration) -> RegistrationStatus:
    """Import and resolve a registered component without invoking it."""
    try:
        module = import_module(reg.module_path)
        symbol = getattr(module, reg.symbol, None)
        if symbol is None:
            return RegistrationStatus(
                name=reg.name,
                role=reg.role,
                available=False,
                version=None,
                detail=f"missing symbol {reg.symbol}",
            )
        version_mod = import_module(reg.version_module)
        version = getattr(version_mod, reg.version_attr, None)
        return RegistrationStatus(
            name=reg.name,
            role=reg.role,
            available=True,
            version=str(version) if version is not None else None,
        )
    except Exception as exc:  # noqa: BLE001 — health probes must not raise
        return RegistrationStatus(
            name=reg.name,
            role=reg.role,
            available=False,
            version=None,
            detail=exc.__class__.__name__,
        )


def probe_all_registrations() -> tuple[RegistrationStatus, ...]:
    """Probe every registered Educational Intelligence component."""
    return tuple(probe_registration(reg) for reg in COMPONENT_REGISTRATIONS)


def pipeline_manifest() -> dict[str, Any]:
    """Return an operational manifest of the registered pipeline."""
    registrations = probe_all_registrations()
    return {
        "orchestrator_version": ORCHESTRATOR_VERSION,
        "certification_status": CERTIFICATION_STATUS,
        "certification_programme": CERTIFICATION_PROGRAMME,
        "stage_order": list(PIPELINE_STAGE_ORDER),
        "components": {
            status.name: {
                "role": status.role,
                "available": status.available,
                "version": status.version,
                "detail": status.detail or None,
            }
            for status in registrations
        },
    }
