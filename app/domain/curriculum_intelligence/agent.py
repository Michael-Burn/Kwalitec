"""EI-001B Agent contracts — executable educational transformers.

Generations are immutable curriculum snapshots.
Agents perform educational transformations that produce those snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentDescriptor:
    """Common metadata every Curriculum Intelligence Agent must expose."""

    agent_id: str
    name: str
    purpose: str
    consumes: tuple[str, ...]
    produces: tuple[str, ...]
    dependencies: tuple[str, ...]
    version: str
    deterministic: bool
    supports_rollback: bool
    quality_metrics_produced: tuple[str, ...]


# Canonical quality metric names produced by Generation agents.
STANDARD_QUALITY_METRICS: tuple[str, ...] = (
    "coverage",
    "hierarchy",
    "duplicates",
    "noise",
    "granularity",
    "confidence",
    "evidence_quality",
)
