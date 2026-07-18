"""Port protocol and edge-case tests for Curriculum Studio."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.diff_service import DiffService
from app.application.curriculum_studio.exceptions import DiffError
from app.application.curriculum_studio.ports import (
    PORT_NAMES,
    CurriculumIngestionPort,
    CurriculumManagementPort,
    EducationPlatformPort,
)
from app.domain.curriculum_studio.curriculum_diff import NormalisedTopic
from tests.application.curriculum_studio.helpers import (
    FakeIngestionPort,
    FakeManagementPort,
    FakePlatformPort,
    make_studio,
    make_studio_with_ports,
    seed_workspace,
)


@pytest.mark.parametrize(
    "port_cls",
    [FakeManagementPort, FakeIngestionPort, FakePlatformPort],
)
def test_fake_ports_satisfy_protocols(port_cls):
    port = port_cls()
    assert port.is_available() is True
    assert port.component_id
    assert port.component_version


def test_management_port_runtime_checkable():
    assert isinstance(FakeManagementPort(), CurriculumManagementPort)


def test_ingestion_port_runtime_checkable():
    assert isinstance(FakeIngestionPort(), CurriculumIngestionPort)


def test_platform_port_runtime_checkable():
    assert isinstance(FakePlatformPort(), EducationPlatformPort)


@pytest.mark.parametrize("name", PORT_NAMES)
def test_port_names(name):
    assert name in {
        "curriculum_management",
        "curriculum_ingestion",
        "education_platform",
    }


def test_unavailable_ports_in_diagnostics():
    studio = make_studio(
        curriculum_management=FakeManagementPort(available=False),
        curriculum_ingestion=FakeIngestionPort(available=False),
        education_platform=FakePlatformPort(available=False),
    )
    report = studio.diagnostic_report()
    assert all(v is False for v in report.port_availability.values())


def test_diff_compare_dicts():
    svc = DiffService()
    left = {
        "curriculum_id": "L",
        "subject_code": "CS1",
        "topics": [{"topic_id": "t1", "title": "A"}],
    }
    right = {
        "curriculum_id": "R",
        "subject_code": "CS1",
        "topics": [{"topic_id": "t1", "title": "B"}],
    }
    snap = svc.compare_dicts(left, right)
    assert snap.updated_topic_count == 1


def test_diff_compare_dicts_invalid():
    with pytest.raises(DiffError):
        DiffService().compare_dicts({}, {"subject_code": "CS1"})


def test_diff_objective_and_prereq_via_dicts():
    svc = DiffService()
    left = {
        "curriculum_id": "L",
        "subject_code": "CS1",
        "topics": [
            {
                "topic_id": "t1",
                "title": "A",
                "objectives": ["o1"],
                "prerequisites": ["p1"],
            }
        ],
    }
    right = {
        "curriculum_id": "R",
        "subject_code": "CS1",
        "topics": [
            {
                "topic_id": "t1",
                "title": "A",
                "objectives": ["o1", "o2"],
                "prerequisites": ["p2"],
            }
        ],
    }
    snap = svc.compare_dicts(left, right)
    assert snap.objective_change_count == 1
    assert snap.prerequisite_change_count == 1


def test_empty_structure_preview():
    studio = make_studio()
    studio.create_workspace("ws-empty", "CS1")
    snap = studio.preview.preview("ws-empty")
    assert snap.node_count == 0


def test_approve_empty_hierarchy_raises():
    studio = make_studio()
    studio.create_workspace("ws-empty", "CS1")
    studio.publication.update_facts("ws-empty", validation_passed=True)
    from app.application.curriculum_studio.exceptions import PreviewError

    with pytest.raises(PreviewError):
        studio.preview.approve("ws-empty")


def test_archive_requires_published():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, ready=True)
    studio.versions.assign_version("ws-1", "2026.1", version_id="ver-1")
    from app.application.curriculum_studio.exceptions import PublicationError

    with pytest.raises(PublicationError):
        studio.publication.archive("ws-1")


def test_advance_at_publication_raises():
    studio = seed_workspace()
    studio.workflow.transition(
        "ws-1", "jump_to_publication", enforce_gates=False
    )
    from app.application.curriculum_studio.exceptions import WorkflowError

    with pytest.raises(WorkflowError):
        studio.workflow.advance("ws-1")


@pytest.mark.parametrize(
    "bad_id",
    ["", "  "],
)
def test_workspace_rejects_blank_ids(bad_id):
    studio = make_studio()
    with pytest.raises(ValueError):
        studio.create_workspace(bad_id, "CS1")


def test_topic_create_rejects_blank():
    with pytest.raises(ValueError):
        NormalisedTopic.create("", "Title")


def test_registry_clear():
    studio = seed_workspace()
    assert studio.registry.workspace_count == 1
    studio.registry.clear()
    assert studio.registry.workspace_count == 0
