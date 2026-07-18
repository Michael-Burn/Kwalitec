"""Shared helpers for Curriculum Studio domain tests."""

from __future__ import annotations

from app.domain.curriculum_studio.curriculum_diff import (
    NormalisedCurriculum,
    NormalisedTopic,
)
from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.studio_workflow import StudioWorkflow
from app.domain.curriculum_studio.version_history import VersionRecord
from app.domain.curriculum_studio.workflow_stage import WorkflowStage


def make_facts(**kwargs) -> WorkspacePublicationFacts:
    defaults = {
        "cmp_uploaded": False,
        "official_syllabus_uploaded": False,
        "validation_passed": False,
        "blueprint_assigned": False,
        "preview_approved": False,
        "version_assigned": False,
        "rollback_snapshot_created": False,
    }
    defaults.update(kwargs)
    return WorkspacePublicationFacts.create(**defaults)


def make_ready_facts() -> WorkspacePublicationFacts:
    return make_facts(
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )


def make_workflow(
    workspace_id: str = "ws-1",
    *,
    stage: WorkflowStage | str = WorkflowStage.SUBJECT,
) -> StudioWorkflow:
    return StudioWorkflow.create("wf-1", workspace_id, current_stage=stage)


def make_workspace(
    workspace_id: str = "ws-1",
    *,
    subject_code: str = "CS1",
    facts: WorkspacePublicationFacts | None = None,
    stage: WorkflowStage | str = WorkflowStage.SUBJECT,
    section_ids: tuple[str, ...] = ("sec-1",),
    topic_ids: tuple[str, ...] = ("topic-1",),
    objective_ids: tuple[str, ...] = ("obj-1",),
    version_label: str = "",
) -> CurriculumWorkspace:
    wf = make_workflow(workspace_id, stage=stage)
    return CurriculumWorkspace.create(
        workspace_id,
        subject_code,
        subject_title="Core Statistics",
        version_label=version_label,
        workflow=wf,
        facts=facts or make_facts(),
        section_ids=section_ids,
        topic_ids=topic_ids,
        objective_ids=objective_ids,
    )


def make_topic(
    topic_id: str = "t1",
    title: str = "Topic 1",
    **kwargs,
) -> NormalisedTopic:
    return NormalisedTopic.create(topic_id, title, **kwargs)


def make_curriculum(
    curriculum_id: str = "cur-1",
    subject_code: str = "CS1",
    *,
    topics: list[NormalisedTopic] | None = None,
    **kwargs,
) -> NormalisedCurriculum:
    return NormalisedCurriculum.create(
        curriculum_id,
        subject_code,
        topics=topics if topics is not None else [make_topic()],
        **kwargs,
    )


def make_version_record(
    version_id: str = "ver-1",
    *,
    workspace_id: str = "ws-1",
    subject_code: str = "CS1",
    version_label: str = "2026.1",
    **kwargs,
) -> VersionRecord:
    return VersionRecord.create(
        version_id,
        workspace_id,
        subject_code,
        version_label,
        **kwargs,
    )
