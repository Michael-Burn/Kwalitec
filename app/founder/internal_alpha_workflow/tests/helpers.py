"""Test helpers for Internal Alpha Live Workflow (FSI-003)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.founder.internal_alpha_workflow import InternalAlphaWorkflowService
from app.founder.internal_alpha_workflow.config import REQUIRED_WEEK_DIRNAMES
from app.founder.operational_state.providers import (
    CapabilityProvider,
    KnowledgeProvider,
    StaticCapabilitySource,
    StaticKnowledgeSource,
)
from app.founder.operational_state.tests.helpers import (
    make_capability_dto,
    make_knowledge_dto,
)
from app.founder.recommendations import FounderRecommendationService

FIXED_NOW = datetime(2026, 7, 14, 18, 0, 0, tzinfo=UTC)


def build_internal_alpha_root(tmp_path: Path) -> Path:
    """Create an empty Internal Alpha research root."""

    root = tmp_path / "research" / "internal_alpha"
    root.mkdir(parents=True)
    return root


def build_week(
    root: Path,
    label: str = "week_001",
    *,
    with_feedback: bool = True,
    with_output_dirs: bool = True,
) -> Path:
    """Create a week folder suitable for workflow tests."""

    week = root / label
    week.mkdir(parents=True, exist_ok=True)
    raw = week / "raw_feedback"
    raw.mkdir(parents=True, exist_ok=True)

    if with_output_dirs:
        for dirname in REQUIRED_WEEK_DIRNAMES:
            if dirname == "raw_feedback":
                continue
            (week / dirname).mkdir(parents=True, exist_ok=True)

    if with_feedback:
        (raw / "alice.txt").write_text(
            "The architecture layering feels unclear around services.\n",
            encoding="utf-8",
        )
        (raw / "bob.txt").write_text(
            "There is a bug causing a crash on the mission page.\n",
            encoding="utf-8",
        )
    return week


def make_workflow_service(
    root: Path,
    **overrides,
) -> InternalAlphaWorkflowService:
    """Build a workflow service pointing at a temporary Internal Alpha root."""

    knowledge = overrides.pop(
        "knowledge",
        KnowledgeProvider(StaticKnowledgeSource(make_knowledge_dto())),
    )
    capability = overrides.pop(
        "capability",
        CapabilityProvider(StaticCapabilitySource(make_capability_dto())),
    )
    recommendations = overrides.pop(
        "recommendations",
        FounderRecommendationService(clock=lambda: FIXED_NOW),
    )
    return InternalAlphaWorkflowService(
        internal_alpha_root=root,
        knowledge=knowledge,
        capability=capability,
        recommendations=recommendations,
        clock=lambda: FIXED_NOW,
        **overrides,
    )
