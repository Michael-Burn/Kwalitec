"""Application service tests for Curriculum Studio."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import (
    PortUnavailable,
    PreviewError,
    PublicationError,
    ValidationError,
    VersionError,
    VersionNotFound,
    WorkflowError,
    WorkflowGateBlocked,
    WorkspaceAlreadyExists,
    WorkspaceNotFound,
)
from app.domain.curriculum_studio.curriculum_diff import (
    NormalisedCurriculum,
    NormalisedTopic,
)
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from tests.application.curriculum_studio.helpers import (
    FakeIngestionPort,
    FakeManagementPort,
    FakePlatformPort,
    make_studio,
    make_studio_with_ports,
    seed_publishable,
    seed_workspace,
)


def test_create_and_get_workspace():
    studio = make_studio()
    snap = studio.create_workspace("ws-1", "CS1", subject_title="Core Stats")
    assert snap.workspace_id == "ws-1"
    assert snap.subject_code == "CS1"
    assert studio.get_workspace("ws-1").subject_title == "Core Stats"


def test_duplicate_workspace_raises():
    studio = seed_workspace()
    with pytest.raises(WorkspaceAlreadyExists):
        studio.create_workspace("ws-1", "CS1")


def test_missing_workspace_raises():
    studio = make_studio()
    with pytest.raises(WorkspaceNotFound):
        studio.get_workspace("missing")


def test_list_workspaces():
    studio = make_studio()
    studio.create_workspace("a", "CS1")
    studio.create_workspace("b", "CM1")
    assert len(studio.list_workspaces()) == 2


def test_advance_subject_to_content_sources():
    studio = seed_workspace()
    snap = studio.workflow.advance("ws-1")
    assert snap.current_stage == WorkflowStage.CONTENT_SOURCES.value


def test_advance_to_validation_requires_sources():
    studio = seed_workspace()
    studio.workflow.advance("ws-1")
    with pytest.raises(WorkflowGateBlocked):
        studio.workflow.advance("ws-1")


def test_advance_to_validation_with_sources():
    studio = seed_workspace()
    studio.publication.update_facts(
        "ws-1", cmp_uploaded=True, official_syllabus_uploaded=True
    )
    studio.workflow.advance("ws-1")
    snap = studio.workflow.advance("ws-1")
    assert snap.current_stage == WorkflowStage.VALIDATION.value


def test_retreat_from_content_sources():
    studio = seed_workspace()
    studio.workflow.advance("ws-1")
    snap = studio.workflow.retreat("ws-1")
    assert snap.current_stage == WorkflowStage.SUBJECT.value


def test_retreat_at_subject_raises():
    studio = seed_workspace()
    with pytest.raises(WorkflowError):
        studio.workflow.retreat("ws-1")


def test_reset_workflow():
    studio = seed_workspace()
    studio.workflow.advance("ws-1")
    snap = studio.workflow.reset("ws-1")
    assert snap.current_stage == WorkflowStage.SUBJECT.value


def test_validation_summarise_blocking():
    studio = seed_workspace()
    snap = studio.validation.summarise("ws-1")
    assert snap.blocks_publication is True
    assert snap.error_count >= 1


def test_validation_mark_passed():
    studio = seed_workspace()
    studio.publication.update_facts(
        "ws-1", cmp_uploaded=True, official_syllabus_uploaded=True
    )
    snap = studio.validation.mark_passed("ws-1")
    assert studio.get_workspace("ws-1").ready_to_publish is False
    assert studio.registry.get_workspace("ws-1").facts.validation_passed is True
    assert snap.passed is True


def test_validation_mark_passed_blocked_without_sources():
    studio = seed_workspace()
    with pytest.raises(ValidationError):
        studio.validation.mark_passed("ws-1")


def test_preview_requires_validation_for_approve():
    studio = seed_workspace()
    with pytest.raises(PreviewError):
        studio.preview.approve("ws-1")


def test_preview_approve():
    studio = seed_workspace()
    studio.publication.update_facts(
        "ws-1",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
    )
    snap = studio.preview.approve("ws-1")
    assert snap.is_approved is True


def test_preview_reject():
    studio = seed_workspace()
    studio.publication.update_facts(
        "ws-1",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        preview_approved=True,
    )
    snap = studio.preview.reject("ws-1")
    assert snap.readiness == "rejected"
    assert (
        studio.registry.get_workspace("ws-1").facts.preview_approved is False
    )


def test_checklist_not_ready_initially():
    studio = seed_workspace()
    snap = studio.publication.checklist("ws-1")
    assert snap.ready_to_publish is False
    assert len(snap.blocking_codes) > 0


def test_publishable_checklist_ready():
    studio = seed_publishable()
    snap = studio.publication.checklist("ws-1")
    assert snap.ready_to_publish is True


def test_publish_and_archive():
    studio = seed_publishable()
    pub = studio.publication.publish("ws-1", occurred_at="2026-07-18T10:00:00Z")
    assert pub.lifecycle_status == "published"
    arch = studio.publication.archive("ws-1", occurred_at="2026-07-19T10:00:00Z")
    assert arch.lifecycle_status == "archived"


def test_publish_requires_management_port():
    studio = seed_workspace(ready=True)
    studio.publication.update_facts(
        "ws-1",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )
    # No version + no port
    with pytest.raises((PublicationError, PortUnavailable)):
        studio.publication.publish("ws-1")


def test_publish_not_ready_raises():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    with pytest.raises(PublicationError):
        studio.publication.publish("ws-1")


def test_version_assign_and_history():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    rec = studio.versions.assign_version("ws-1", "2026.1")
    assert rec.status == "draft"
    hist = studio.versions.history("CS1")
    assert hist.version_count == 1
    assert studio.get_workspace("ws-1").version_label == "2026.1"


def test_version_duplicate_raises():
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    studio.versions.assign_version("ws-1", "2026.1", version_id="ver-1")
    with pytest.raises((VersionError, ValueError)):
        studio.versions.assign_version("ws-1", "2026.2", version_id="ver-1")


def test_version_not_found():
    studio, _, _, _ = make_studio_with_ports()
    with pytest.raises(VersionNotFound):
        studio.versions.get_version("missing")


def test_version_publish_archive():
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    studio.versions.assign_version("ws-1", "2026.1", version_id="ver-1")
    studio.versions.create_rollback_snapshot("ver-1")
    pub = studio.versions.publish_version("ver-1")
    assert pub.status == "published"
    assert pub.rollback_eligible is True
    arch = studio.versions.archive_version("ver-1")
    assert arch.status == "archived"
    assert "ver-1" in mgmt.publish_calls
    assert "ver-1" in mgmt.archive_calls


def test_diff_via_facade():
    studio = make_studio()
    left = NormalisedCurriculum.create(
        "L", "CS1", topics=[NormalisedTopic.create("t1", "A")]
    )
    right = NormalisedCurriculum.create(
        "R", "CS1", topics=[NormalisedTopic.create("t1", "B")]
    )
    snap = studio.compare_curricula(left, right)
    assert snap.updated_topic_count == 1


def test_diff_subject_mismatch():
    studio = make_studio()
    left = NormalisedCurriculum.create("L", "CS1")
    right = NormalisedCurriculum.create("R", "CM1")
    with pytest.raises(Exception):
        studio.compare_curricula(left, right)


def test_health_degraded_without_ports():
    studio = make_studio()
    health = studio.health()
    assert health["studio_status"] == "degraded"
    assert set(health["missing_ports"]) == {
        "curriculum_management",
        "curriculum_ingestion",
        "education_platform",
    }


def test_health_ready_with_ports():
    studio = make_studio(
        curriculum_management=FakeManagementPort(),
        curriculum_ingestion=FakeIngestionPort(),
        education_platform=FakePlatformPort(),
    )
    health = studio.health()
    assert health["studio_status"] == "ready"
    assert health["missing_ports"] == []


def test_diagnostics_report():
    studio = seed_workspace()
    report = studio.diagnostic_report()
    assert report.workspace_count == 1
    assert report.canonical_workflow[0] == "subject"


def test_update_structure():
    studio = seed_workspace()
    snap = studio.update_structure(
        "ws-1",
        topic_ids=("t-a", "t-b"),
        estimated_workload_hours=12.5,
    )
    assert snap.topic_ids == ("t-a", "t-b")
    assert snap.estimated_workload_hours == 12.5


def test_port_available():
    studio = make_studio(curriculum_management=FakeManagementPort())
    assert studio.port_available("curriculum_management") is True
    assert studio.port_available("curriculum_ingestion") is False


def test_publish_calls_management_port():
    studio = seed_publishable()
    mgmt = studio._ports["curriculum_management"]  # noqa: SLF001
    studio.publication.publish("ws-1")
    assert "ver-1" in mgmt.publish_calls
