"""Pipeline stage vocabulary for the Learning Orchestrator."""

from __future__ import annotations

from enum import StrEnum


class PipelineStageName(StrEnum):
    """Canonical live-learner pipeline stages (execution order)."""

    EVIDENCE = "evidence"
    TWIN = "twin"
    DECISION = "decision"
    MISSION = "mission"
    ANALYTICS = "analytics"


class StageOutcome(StrEnum):
    """Outcome reported by a single pipeline stage."""

    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    WARNING = "warning"


# Canonical execution order for a full live-learner pass.
CANONICAL_PIPELINE: tuple[PipelineStageName, ...] = (
    PipelineStageName.EVIDENCE,
    PipelineStageName.TWIN,
    PipelineStageName.DECISION,
    PipelineStageName.MISSION,
    PipelineStageName.ANALYTICS,
)

STAGE_PORT_NAMES: dict[PipelineStageName, str] = {
    PipelineStageName.EVIDENCE: "evidence",
    PipelineStageName.TWIN: "twin",
    PipelineStageName.DECISION: "adaptive_learning",
    PipelineStageName.MISSION: "mission",
    PipelineStageName.ANALYTICS: "analytics",
}
