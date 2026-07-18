"""Port interaction and DTO mapping volume tests."""

from __future__ import annotations

import dataclasses

import pytest

from app.application.curriculum_studio.diff_service import DiffService
from app.application.curriculum_studio.dto.preview_snapshot import PreviewSnapshot
from app.application.curriculum_studio.dto.publication_snapshot import (
    ChecklistItemSnapshot,
    PublicationSnapshot,
)
from app.application.curriculum_studio.dto.validation_snapshot import (
    ValidationSnapshot,
)
from app.application.curriculum_studio.dto.version_snapshot import (
    VersionRecordSnapshot,
    VersionSnapshot,
)
from app.application.curriculum_studio.dto.workflow_snapshot import WorkflowSnapshot
from app.application.curriculum_studio.dto.workspace_snapshot import WorkspaceSnapshot
from app.application.curriculum_studio.exceptions import DiffError, PortUnavailable
from app.domain.curriculum_studio.curriculum_diff import (
    NormalisedCurriculum,
)
from tests.application.curriculum_studio.helpers import (
    FakeIngestionPort,
    FakeManagementPort,
    FakePlatformPort,
    make_studio,
    make_studio_with_ports,
    seed_workspace,
)

DTO_TYPES = (
    WorkspaceSnapshot,
    WorkflowSnapshot,
    ValidationSnapshot,
    PreviewSnapshot,
    PublicationSnapshot,
    ChecklistItemSnapshot,
    VersionSnapshot,
    VersionRecordSnapshot,
)


@pytest.mark.parametrize("dto_cls", DTO_TYPES)
def test_dto_types_are_frozen(dto_cls):
    assert dataclasses.is_dataclass(dto_cls)
    fields = {f.name: f for f in dataclasses.fields(dto_cls)}
    # Construct with minimal kwargs where possible
    if dto_cls is WorkspaceSnapshot:
        obj = WorkspaceSnapshot("w", "CS1")
    elif dto_cls is WorkflowSnapshot:
        obj = WorkflowSnapshot("wf", "w", "subject", "subject", 0, 0)
    elif dto_cls is ValidationSnapshot:
        obj = ValidationSnapshot("v", "w", "not_started", False)
    elif dto_cls is PreviewSnapshot:
        obj = PreviewSnapshot("p", "w", "draft")
    elif dto_cls is PublicationSnapshot:
        obj = PublicationSnapshot("p", "w", "CS1")
    elif dto_cls is ChecklistItemSnapshot:
        obj = ChecklistItemSnapshot("c", "L", "pending", False)
    elif dto_cls is VersionSnapshot:
        obj = VersionSnapshot("CS1")
    else:
        obj = VersionRecordSnapshot("v", "w", "CS1", "2026.1", "draft")
    first = next(iter(fields))
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(obj, first, getattr(obj, first))


@pytest.mark.parametrize("i", range(25))
def test_management_port_asset_list(i):
    mgmt = FakeManagementPort()
    mgmt.create_subject("CS1")
    ver = mgmt.create_version("CS1", "2026.1", version_id=f"ver-{i}")
    mgmt.add_asset_ref(ver["version_id"], kind="cmp", reference=f"r-{i}")
    assets = mgmt.list_assets(ver["version_id"])
    assert len(assets) == 1


@pytest.mark.parametrize("i", range(20))
def test_ingestion_port_normalised_structure(i):
    ingestion = FakeIngestionPort()
    job = ingestion.start_ingestion(
        subject_code="CS1",
        sources=[{"kind": "cmp", "reference": f"r-{i}"}],
        job_id=f"job-{i}",
    )
    structure = ingestion.normalised_structure(job["job_id"])
    assert structure is not None
    assert structure["subject_code"] == "CS1"
    report = ingestion.get_validation_report(job["job_id"])
    assert report["passed"] is True


@pytest.mark.parametrize("i", range(15))
def test_platform_student_surface(i):
    platform = FakePlatformPort()
    surface = platform.student_surface(subject_code="CS1", version_id=f"v-{i}")
    assert surface["subject_code"] == "CS1"
    assert platform.surface_calls[-1] == ("CS1", f"v-{i}")


@pytest.mark.parametrize("i", range(20))
def test_diff_compare_dicts(i):
    left = {
        "curriculum_id": f"L{i}",
        "subject_code": "CS1",
        "topics": [
            {
                "topic_id": "t1",
                "title": "A",
                "objectives": (),
                "prerequisites": (),
            }
        ],
    }
    right = {
        "curriculum_id": f"R{i}",
        "subject_code": "CS1",
        "topics": [
            {
                "topic_id": "t1",
                "title": "B" if i % 2 else "A",
                "objectives": (),
                "prerequisites": (),
            }
        ],
    }
    snap = DiffService().compare_dicts(left, right, diff_id=f"d-{i}")
    if i % 2:
        assert snap.updated_topic_count == 1
    else:
        assert snap.is_identical is True


@pytest.mark.parametrize("i", range(10))
def test_diff_compare_ingestion_requires_port(i):
    del i
    with pytest.raises(PortUnavailable):
        DiffService().compare_ingestion_jobs("a", "b")


@pytest.mark.parametrize("i", range(12))
def test_workspace_assign_blueprint(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{i}")
    studio.versions.assign_version(f"ws-{i}", "2026.1", version_id=f"ver-{i}")
    snap = studio.workspaces.assign_blueprint(
        f"ws-{i}",
        section_id="sec-1",
        blueprint_profile_id=f"bp-{i}",
    )
    assert studio.registry.get_workspace(f"ws-{i}").facts.blueprint_assigned
    assert snap.workspace_id == f"ws-{i}"


@pytest.mark.parametrize("i", range(10))
def test_preview_approve_calls_management_when_versioned(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{i}")
    studio.versions.assign_version(f"ws-{i}", "2026.1", version_id=f"ver-{i}")
    studio.publication.update_facts(f"ws-{i}", validation_passed=True)
    studio.preview.approve(f"ws-{i}")
    assert f"ver-{i}" in mgmt.approve_calls


@pytest.mark.parametrize(
    ("left_code", "right_code"),
    [("CS1", "CM1"), ("CS1", "CB2"), ("A1", "B1")],
)
def test_diff_subject_mismatch_raises(left_code, right_code):
    with pytest.raises(DiffError):
        DiffService().compare(
            NormalisedCurriculum.create("L", left_code),
            NormalisedCurriculum.create("R", right_code),
        )


@pytest.mark.parametrize("i", range(8))
def test_health_port_availability_matrix(i):
    flags = [(i & 1) != 0, (i & 2) != 0, (i & 4) != 0]
    studio = make_studio(
        curriculum_management=FakeManagementPort(available=flags[0])
        if flags[0]
        else None,
        curriculum_ingestion=FakeIngestionPort(available=flags[1])
        if flags[1]
        else None,
        education_platform=FakePlatformPort(available=flags[2])
        if flags[2]
        else None,
    )
    health = studio.health()
    if all(flags):
        assert health["studio_status"] == "ready"
    else:
        assert health["studio_status"] == "degraded"


@pytest.mark.parametrize("i", range(10))
def test_activity_recorded_on_workspace_open(i):
    studio = make_studio()
    studio.open_workspace(f"ws-{i}", "CS1")
    kinds = [a.kind for a in studio.registry.list_activity()]
    assert "workspace_opened" in kinds
