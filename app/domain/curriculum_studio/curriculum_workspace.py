"""Curriculum workspace — Founder working unit for an educational product.

A workspace is not a file. It is the operational context for preparing
a curriculum release through Curriculum Studio.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.curriculum_studio.publication_checklist import (
    PublicationChecklist,
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.studio_workflow import StudioWorkflow
from app.domain.curriculum_studio.workflow_stage import (
    WorkflowStage,
    resolve_workflow_stage,
)


class WorkspaceStatus(StrEnum):
    """Lifecycle posture of a Curriculum Studio workspace."""

    ACTIVE = "active"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    ABANDONED = "abandoned"


@dataclass(frozen=True)
class CurriculumWorkspace:
    """Founder-facing operational context for one curriculum release.

    Holds references and readiness facts — never PDF bytes.
    """

    workspace_id: str
    subject_code: str
    subject_title: str = ""
    version_label: str = ""
    version_id: str | None = None
    status: WorkspaceStatus = WorkspaceStatus.ACTIVE
    workflow: StudioWorkflow | None = None
    facts: WorkspacePublicationFacts = field(
        default_factory=WorkspacePublicationFacts
    )
    section_ids: tuple[str, ...] = field(default_factory=tuple)
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    estimated_workload_hours: float | None = None
    notes: str = ""

    @classmethod
    def create(
        cls,
        workspace_id: str,
        subject_code: str,
        *,
        subject_title: str = "",
        version_label: str = "",
        version_id: str | None = None,
        status: WorkspaceStatus | str = WorkspaceStatus.ACTIVE,
        workflow: StudioWorkflow | None = None,
        facts: WorkspacePublicationFacts | None = None,
        section_ids: list[str] | tuple[str, ...] | None = None,
        topic_ids: list[str] | tuple[str, ...] | None = None,
        objective_ids: list[str] | tuple[str, ...] | None = None,
        prerequisite_edges: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
        estimated_workload_hours: float | None = None,
        notes: str = "",
    ) -> CurriculumWorkspace:
        """Construct a CurriculumWorkspace after validating invariants."""
        wid = _require_non_empty(workspace_id, "workspace_id")
        code = _require_non_empty(subject_code, "subject_code").upper()
        resolved_status = (
            status
            if isinstance(status, WorkspaceStatus)
            else WorkspaceStatus(str(status).strip().lower())
        )
        wf = workflow or StudioWorkflow.create(
            f"wf-{wid}",
            wid,
        )
        if wf.workspace_id != wid:
            raise ValueError("workflow workspace_id must match workspace")
        facts_obj = facts or WorkspacePublicationFacts.create()
        hours = estimated_workload_hours
        if hours is not None and hours < 0:
            raise ValueError("estimated_workload_hours must be non-negative")
        return cls(
            workspace_id=wid,
            subject_code=code,
            subject_title=(subject_title or "").strip(),
            version_label=(version_label or "").strip(),
            version_id=(
                None
                if version_id is None
                else _require_non_empty(version_id, "version_id")
            ),
            status=resolved_status,
            workflow=wf,
            facts=facts_obj,
            section_ids=tuple(section_ids or ()),
            topic_ids=tuple(topic_ids or ()),
            objective_ids=tuple(objective_ids or ()),
            prerequisite_edges=tuple(prerequisite_edges or ()),
            metadata=tuple(metadata or ()),
            estimated_workload_hours=hours,
            notes=(notes or "").strip(),
        )

    @property
    def current_stage(self) -> WorkflowStage:
        """Current Founder workflow stage."""
        assert self.workflow is not None
        return self.workflow.current_stage

    @property
    def checklist(self) -> PublicationChecklist:
        """Computed publication checklist for this workspace."""
        return PublicationChecklist.compute(self.facts)

    @property
    def ready_to_publish(self) -> bool:
        """True when every publication checklist prerequisite is satisfied."""
        return self.checklist.ready_to_publish

    def with_facts(self, facts: WorkspacePublicationFacts) -> CurriculumWorkspace:
        """Return a copy with updated publication facts."""
        return CurriculumWorkspace(
            workspace_id=self.workspace_id,
            subject_code=self.subject_code,
            subject_title=self.subject_title,
            version_label=self.version_label,
            version_id=self.version_id,
            status=self.status,
            workflow=self.workflow,
            facts=facts,
            section_ids=self.section_ids,
            topic_ids=self.topic_ids,
            objective_ids=self.objective_ids,
            prerequisite_edges=self.prerequisite_edges,
            metadata=self.metadata,
            estimated_workload_hours=self.estimated_workload_hours,
            notes=self.notes,
        )

    def with_workflow(self, workflow: StudioWorkflow) -> CurriculumWorkspace:
        """Return a copy with an updated workflow."""
        if workflow.workspace_id != self.workspace_id:
            raise ValueError("workflow workspace_id must match workspace")
        return CurriculumWorkspace(
            workspace_id=self.workspace_id,
            subject_code=self.subject_code,
            subject_title=self.subject_title,
            version_label=self.version_label,
            version_id=self.version_id,
            status=self.status,
            workflow=workflow,
            facts=self.facts,
            section_ids=self.section_ids,
            topic_ids=self.topic_ids,
            objective_ids=self.objective_ids,
            prerequisite_edges=self.prerequisite_edges,
            metadata=self.metadata,
            estimated_workload_hours=self.estimated_workload_hours,
            notes=self.notes,
        )

    def with_status(self, status: WorkspaceStatus | str) -> CurriculumWorkspace:
        """Return a copy with updated workspace status."""
        resolved = (
            status
            if isinstance(status, WorkspaceStatus)
            else WorkspaceStatus(str(status).strip().lower())
        )
        return CurriculumWorkspace(
            workspace_id=self.workspace_id,
            subject_code=self.subject_code,
            subject_title=self.subject_title,
            version_label=self.version_label,
            version_id=self.version_id,
            status=resolved,
            workflow=self.workflow,
            facts=self.facts,
            section_ids=self.section_ids,
            topic_ids=self.topic_ids,
            objective_ids=self.objective_ids,
            prerequisite_edges=self.prerequisite_edges,
            metadata=self.metadata,
            estimated_workload_hours=self.estimated_workload_hours,
            notes=self.notes,
        )

    def at_stage(self, stage: WorkflowStage | str) -> bool:
        """True when the workspace is currently on ``stage``."""
        return self.current_stage is resolve_workflow_stage(stage)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
