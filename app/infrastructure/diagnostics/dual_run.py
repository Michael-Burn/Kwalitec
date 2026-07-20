"""Dual-run observability helpers for Version 2 coexistence (ADR-007)."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.config.v2_flags import (
    Version2FeatureFlags,
    resolve_v2_feature_flags,
)


@dataclass(frozen=True)
class DualRunStatus:
    """Operational dual-run status for Founder / ops surfaces."""

    student_experience_enabled: bool
    durable_store: bool
    seed_demo: bool
    engines_injected: bool
    sole_runtime: bool
    founder_intelligence: bool
    label: str
    ready_for_cutover_checklist: tuple[str, ...]


def build_dual_run_status(
    *,
    flags: Version2FeatureFlags | None = None,
) -> DualRunStatus:
    """Project dual-run feature flags into an ops-facing status."""
    active = flags or resolve_v2_feature_flags()
    if active.SOLE_RUNTIME:
        label = "sole-runtime-v2"
    elif active.ENABLE_STUDENT_EXPERIENCE:
        label = "dual-run-active"
    else:
        label = "v1-primary"
    checklist = (
        "Persistence + adapters stable in production dual-run",
        "Student path explainable end-to-end on V2",
        "No unresolved dual-authority defects",
        "Founder Studio operable over Management/Ingestion",
        "Product Strategy evidence gates satisfied",
        "V2-020 retirement runbook executed",
    )
    return DualRunStatus(
        student_experience_enabled=active.ENABLE_STUDENT_EXPERIENCE,
        durable_store=active.ENABLE_DURABLE_STORE,
        seed_demo=active.SEED_DEMO_LEARNERS,
        engines_injected=active.INJECT_PHASE_I_ENGINES,
        sole_runtime=active.SOLE_RUNTIME,
        founder_intelligence=active.ENABLE_FOUNDER_INTELLIGENCE,
        label=label,
        ready_for_cutover_checklist=checklist,
    )
