"""Learner Lifecycle Orchestration version constants (LP-001)."""

from __future__ import annotations

ORCHESTRATOR_VERSION = "llp.v1"
CERTIFICATION_PROGRAMME = "LP-001"
CERTIFICATION_STATUS = "complete"

# Onboarding: bind → node state → twin → decisions → experience
ONBOARDING_STAGE_ORDER: tuple[str, ...] = (
    "bind_instance",
    "initialise_node_state",
    "twin_beliefs",
    "educational_decisions",
    "experience_models",
)

# Evidence refresh: twin → decisions → experience (evidence already persisted)
EVIDENCE_STAGE_ORDER: tuple[str, ...] = (
    "twin_beliefs",
    "educational_decisions",
    "experience_models",
)

# Full evidence path including append
EVIDENCE_RECORD_STAGE_ORDER: tuple[str, ...] = (
    "record_evidence",
    "twin_beliefs",
    "educational_decisions",
    "experience_models",
)
