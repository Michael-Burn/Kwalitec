"""Version 2 Curriculum Studio — domain package.

Founder-facing operational vocabulary for curriculum readiness:
workflow stages, workspaces, publication checklists, validation /
preview / publication summaries, version history, and structural diffs.

No Flask, SQLAlchemy, PDF parsing, or persistence.

Prefer explicit imports such as
``app.domain.curriculum_studio.workflow_stage.WorkflowStage``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CANONICAL_WORKFLOW",
    "CHECKLIST_ORDER",
    "ChecklistItem",
    "ChecklistItemCode",
    "ChecklistItemStatus",
    "CurriculumDiff",
    "CurriculumWorkspace",
    "DiffChangeKind",
    "DiffEntry",
    "LAWFUL_WORKFLOW_TRANSITIONS",
    "NormalisedCurriculum",
    "NormalisedTopic",
    "PreviewNode",
    "PreviewReadiness",
    "PreviewSummary",
    "PublicationChecklist",
    "PublicationLifecycleStatus",
    "PublicationSummary",
    "STAGE_LABELS",
    "StudioVersionStatus",
    "StudioWorkflow",
    "ValidationFinding",
    "ValidationFindingSeverity",
    "ValidationReadiness",
    "ValidationSummary",
    "VersionHistory",
    "VersionRecord",
    "WorkflowStage",
    "WorkflowTransitionEvent",
    "WorkflowTransitionRecord",
    "WorkspacePublicationFacts",
    "WorkspaceStatus",
    "compute_checklist",
    "has_reached",
    "is_lawful_transition",
    "is_lawful_version_transition",
    "next_workflow_state",
    "resolve_workflow_stage",
    "stage_index",
]

_EXPORT_MODULES = {
    "CANONICAL_WORKFLOW": "app.domain.curriculum_studio.workflow_stage",
    "CHECKLIST_ORDER": "app.domain.curriculum_studio.publication_checklist",
    "ChecklistItem": "app.domain.curriculum_studio.publication_checklist",
    "ChecklistItemCode": "app.domain.curriculum_studio.publication_checklist",
    "ChecklistItemStatus": "app.domain.curriculum_studio.publication_checklist",
    "CurriculumDiff": "app.domain.curriculum_studio.curriculum_diff",
    "CurriculumWorkspace": "app.domain.curriculum_studio.curriculum_workspace",
    "DiffChangeKind": "app.domain.curriculum_studio.curriculum_diff",
    "DiffEntry": "app.domain.curriculum_studio.curriculum_diff",
    "LAWFUL_WORKFLOW_TRANSITIONS": "app.domain.curriculum_studio.studio_workflow",
    "NormalisedCurriculum": "app.domain.curriculum_studio.curriculum_diff",
    "NormalisedTopic": "app.domain.curriculum_studio.curriculum_diff",
    "PreviewNode": "app.domain.curriculum_studio.preview_summary",
    "PreviewReadiness": "app.domain.curriculum_studio.preview_summary",
    "PreviewSummary": "app.domain.curriculum_studio.preview_summary",
    "PublicationChecklist": (
        "app.domain.curriculum_studio.publication_checklist"
    ),
    "PublicationLifecycleStatus": (
        "app.domain.curriculum_studio.publication_summary"
    ),
    "PublicationSummary": "app.domain.curriculum_studio.publication_summary",
    "STAGE_LABELS": "app.domain.curriculum_studio.workflow_stage",
    "StudioVersionStatus": "app.domain.curriculum_studio.version_history",
    "StudioWorkflow": "app.domain.curriculum_studio.studio_workflow",
    "ValidationFinding": "app.domain.curriculum_studio.validation_summary",
    "ValidationFindingSeverity": (
        "app.domain.curriculum_studio.validation_summary"
    ),
    "ValidationReadiness": "app.domain.curriculum_studio.validation_summary",
    "ValidationSummary": "app.domain.curriculum_studio.validation_summary",
    "VersionHistory": "app.domain.curriculum_studio.version_history",
    "VersionRecord": "app.domain.curriculum_studio.version_history",
    "WorkflowStage": "app.domain.curriculum_studio.workflow_stage",
    "WorkflowTransitionEvent": "app.domain.curriculum_studio.studio_workflow",
    "WorkflowTransitionRecord": "app.domain.curriculum_studio.studio_workflow",
    "WorkspacePublicationFacts": (
        "app.domain.curriculum_studio.publication_checklist"
    ),
    "WorkspaceStatus": "app.domain.curriculum_studio.curriculum_workspace",
    "has_reached": "app.domain.curriculum_studio.workflow_stage",
    "is_lawful_transition": "app.domain.curriculum_studio.studio_workflow",
    "is_lawful_version_transition": (
        "app.domain.curriculum_studio.version_history"
    ),
    "next_workflow_state": "app.domain.curriculum_studio.studio_workflow",
    "resolve_workflow_stage": "app.domain.curriculum_studio.workflow_stage",
    "stage_index": "app.domain.curriculum_studio.workflow_stage",
}


def compute_checklist(facts):  # noqa: ANN001
    """Compute a PublicationChecklist from workspace facts."""
    from app.domain.curriculum_studio.publication_checklist import (
        PublicationChecklist,
    )

    return PublicationChecklist.compute(facts)


def __getattr__(name: str) -> Any:
    if name == "compute_checklist":
        return compute_checklist
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
