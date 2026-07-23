"""Build XP IntegrationInputs from adapter cargo without educational reasoning.

Null-safe mapping only. Education OS application artefacts are passed through
when already present; pipeline / missing cargo degrades to student_id + as_of.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.integration.integration_composer import (
    aligned_module_inputs,
)
from application.student_experience.integration.integration_inputs import (
    IntegrationInputs,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)


def build_home_inputs(
    student_id: str,
    as_of: datetime,
    *,
    evaluation: Any = None,
    assessment: Any = None,
    recommendation_set: Any = None,
    mission_plan: Any = None,
    schedule: Any = None,
    current_execution: Any = None,
    execution_history: Any = None,
    exam_target: Any = None,
    cargo: Any = None,
) -> HomeInputs:
    """Compose ``HomeInputs`` from optional Education OS artefacts.

    Missing or incompatible cargo is ignored — home composition degrades
    gracefully. Never invents educational state.
    """
    resolved_id = (student_id or "").strip()
    if not resolved_id:
        resolved_id = "anonymous"

    kwargs: dict[str, Any] = {
        "student_id": resolved_id,
        "as_of": as_of,
    }
    # Prefer explicit kwargs; otherwise duck-type already-validated XP fields
    # from a caller-supplied cargo object (IntegrationInputs / HomeInputs /
    # Education OS application DTOs). Pipeline domain types are skipped —
    # they are not HomeInputs artefacts.
    source = cargo if cargo is not None else None
    field_map = {
        "evaluation": evaluation,
        "assessment": assessment,
        "recommendation_set": recommendation_set,
        "mission_plan": mission_plan,
        "schedule": schedule,
        "current_execution": current_execution,
        "execution_history": execution_history,
        "exam_target": exam_target,
    }
    for name, explicit in field_map.items():
        value = explicit
        if value is None and source is not None:
            value = getattr(source, name, None)
            if value is None and name == "current_execution":
                value = getattr(source, "mission_execution", None)
        if value is not None:
            kwargs[name] = value

    try:
        return HomeInputs(**kwargs)
    except Exception:
        # Incompatible artefact shapes must not break the HTTP surface.
        return HomeInputs(student_id=resolved_id, as_of=as_of)


def build_integration_inputs(
    student_id: str,
    as_of: datetime,
    *,
    cargo: Any = None,
    prior_readiness_snapshot: ReadinessSnapshot | None = None,
    evidence_recorded: bool = False,
) -> IntegrationInputs:
    """Build aligned ``IntegrationInputs`` for ExperienceIntegrationService."""
    if isinstance(cargo, IntegrationInputs):
        if prior_readiness_snapshot is None and not evidence_recorded:
            return cargo
        return IntegrationInputs(
            home=cargo.home,
            journey=cargo.journey,
            readiness=cargo.readiness,
            workspace=cargo.workspace,
            evaluation=cargo.evaluation,
            mission_plan=cargo.mission_plan,
            schedule=cargo.schedule,
            mission_execution=cargo.mission_execution,
            prior_readiness_snapshot=(
                prior_readiness_snapshot or cargo.prior_readiness_snapshot
            ),
            evidence_recorded=evidence_recorded or cargo.evidence_recorded,
        )

    if isinstance(cargo, HomeInputs):
        home = cargo
    else:
        home = build_home_inputs(student_id, as_of, cargo=cargo)

    journey, readiness, workspace = aligned_module_inputs(home)
    return IntegrationInputs(
        home=home,
        journey=journey,
        readiness=readiness,
        workspace=workspace,
        prior_readiness_snapshot=prior_readiness_snapshot,
        evidence_recorded=evidence_recorded,
    )
