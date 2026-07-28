"""Operational contract identity for the Educational Intelligence pipeline.

This version identifies the orchestration layer only. It does not version
educational stage contracts (interpretation, decision, projection, planning,
explanation) — those remain owned by their certified stage packages.
"""

from __future__ import annotations

ORCHESTRATOR_VERSION = "PR-001.educational_intelligence_pipeline.v1"

# Ordered stage tokens executed by the production orchestrator.
PIPELINE_STAGE_ORDER: tuple[str, ...] = (
    "interpretation",
    "decision",
    "twin_update",
    "graph_projection",
    "mission_planning",
    "tutor_explanation",
)

CERTIFICATION_STATUS = "certified"
CERTIFICATION_PROGRAMME = "AP-002D7"
