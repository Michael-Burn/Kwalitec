"""DTO immutability tests for Curriculum Studio."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.curriculum_studio.diff_service import (
    DiffEntrySnapshot,
    DiffSnapshot,
)
from app.application.curriculum_studio.dto.preview_snapshot import (
    PreviewNodeSnapshot,
    PreviewSnapshot,
)
from app.application.curriculum_studio.dto.publication_snapshot import (
    ChecklistItemSnapshot,
    PublicationSnapshot,
)
from app.application.curriculum_studio.dto.validation_snapshot import (
    ValidationFindingSnapshot,
    ValidationSnapshot,
)
from app.application.curriculum_studio.dto.version_snapshot import (
    VersionRecordSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio.dto.workflow_snapshot import (
    WorkflowSnapshot,
    WorkflowTransitionSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)

DTO_FACTORIES = [
    lambda: WorkspaceSnapshot("ws", "CS1"),
    lambda: WorkflowSnapshot("wf", "ws", "subject", "subject"),
    lambda: WorkflowTransitionSnapshot("subject", "content_sources", "advance"),
    lambda: ValidationSnapshot("s", "ws", "passed", True),
    lambda: ValidationFindingSnapshot("c", "m", "warning"),
    lambda: PreviewSnapshot("p", "ws", "not_ready"),
    lambda: PreviewNodeSnapshot("n", "Title"),
    lambda: PublicationSnapshot("p", "ws", "CS1"),
    lambda: ChecklistItemSnapshot("cmp_uploaded", "CMP Uploaded", "pending", False),
    lambda: VersionSnapshot("CS1"),
    lambda: VersionRecordSnapshot("v", "ws", "CS1", "2026.1", "draft"),
    lambda: DiffSnapshot("d", "L", "R"),
    lambda: DiffEntrySnapshot("added_topic", "topic/t1"),
]


@pytest.mark.parametrize("factory", DTO_FACTORIES)
def test_dto_frozen(factory):
    dto = factory()
    field_name = list(dto.__dataclass_fields__)[0]
    with pytest.raises(FrozenInstanceError):
        setattr(dto, field_name, "mutated")


def test_workspace_snapshot_from_service_frozen():
    studio = seed_workspace()
    snap = studio.get_workspace("ws-1")
    with pytest.raises(FrozenInstanceError):
        snap.subject_code = "XX"  # type: ignore[misc]


def test_workflow_snapshot_frozen():
    studio = seed_workspace()
    snap = studio.workflow.get_workflow("ws-1")
    with pytest.raises(FrozenInstanceError):
        snap.current_stage = "x"  # type: ignore[misc]


def test_publication_snapshot_frozen():
    studio = seed_workspace()
    snap = studio.publication.checklist("ws-1")
    with pytest.raises(FrozenInstanceError):
        snap.ready_to_publish = True  # type: ignore[misc]


def test_validation_snapshot_frozen():
    studio = seed_workspace()
    snap = studio.validation.summarise("ws-1")
    with pytest.raises(FrozenInstanceError):
        snap.passed = True  # type: ignore[misc]


def test_preview_snapshot_frozen():
    studio = seed_workspace()
    snap = studio.preview.preview("ws-1")
    with pytest.raises(FrozenInstanceError):
        snap.readiness = "x"  # type: ignore[misc]


def test_version_snapshot_frozen():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    studio.versions.assign_version("ws-1", "2026.1")
    snap = studio.versions.history("CS1")
    with pytest.raises(FrozenInstanceError):
        snap.version_count = 99  # type: ignore[misc]


@pytest.mark.parametrize(
    "attr",
    [
        "workspace_id",
        "subject_code",
        "status",
        "current_stage",
        "ready_to_publish",
    ],
)
def test_workspace_snapshot_attrs(attr):
    studio = seed_workspace()
    snap = studio.get_workspace("ws-1")
    assert hasattr(snap, attr)
