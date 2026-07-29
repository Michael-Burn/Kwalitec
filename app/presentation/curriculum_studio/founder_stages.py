"""Founder-facing publication stages (FV-001A).

Domain ``WorkflowStage`` tokens remain authoritative for persistence.
This module maps them to the four Founder strip labels:

Upload → Preview → Approve → Publish

Validation is automatic (Processing) and is not a strip stage.
"""

from __future__ import annotations

from app.domain.curriculum_studio.workflow_stage import (
    WorkflowStage,
    resolve_workflow_stage,
)

# Canonical Founder strip — Upload → Preview → Approve → Publish.
FOUNDER_STAGES: tuple[str, ...] = (
    "Upload",
    "Preview",
    "Approve",
    "Publish",
)

_DOMAIN_TO_FOUNDER: dict[WorkflowStage, str] = {
    WorkflowStage.SUBJECT: "Upload",
    WorkflowStage.CONTENT_SOURCES: "Upload",
    WorkflowStage.VALIDATION: "Upload",  # Processing lives under Upload→Preview
    WorkflowStage.PREVIEW: "Preview",
    WorkflowStage.APPROVAL: "Approve",
    WorkflowStage.PUBLICATION: "Publish",
}

_FOUNDER_TO_INDEX: dict[str, int] = {
    label: idx for idx, label in enumerate(FOUNDER_STAGES)
}


def founder_stage_label(stage: WorkflowStage | str) -> str:
    """Return the Founder stage label for a domain stage."""
    resolved = resolve_workflow_stage(stage)
    return _DOMAIN_TO_FOUNDER[resolved]


def founder_stage_index(stage: WorkflowStage | str) -> int:
    """Zero-based index into ``FOUNDER_STAGES`` for the domain stage."""
    return _FOUNDER_TO_INDEX[founder_stage_label(stage)]
