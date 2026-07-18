"""Founder use-case orchestration tests for Curriculum Studio."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import (
    PortUnavailable,
    SubjectAlreadyExists,
    SubjectNotFound,
    ValidationError,
)
from tests.application.curriculum_studio.helpers import (
    make_studio,
    make_studio_with_ports,
    seed_publishable,
    seed_workspace,
)

SUBJECT_CODES = tuple(f"S{i:02d}" for i in range(1, 31))
VERSION_LABELS = tuple(f"2026.{i}" for i in range(1, 21))


@pytest.mark.parametrize("code", SUBJECT_CODES)
def test_create_subject_use_case(code):
    studio, _, _, _ = make_studio_with_ports()
    snap = studio.create_subject(code, title=f"Subject {code}")
    assert snap.subject_code == code
    assert studio.subjects.get_subject(code).title == f"Subject {code}"


def test_create_subject_requires_port():
    studio = make_studio()
    with pytest.raises(PortUnavailable):
        studio.create_subject("CS1")


def test_create_subject_duplicate():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_subject("CS1", title="A")
    with pytest.raises(SubjectAlreadyExists):
        studio.create_subject("CS1", title="B")


def test_get_subject_missing():
    studio, _, _, _ = make_studio_with_ports()
    with pytest.raises(SubjectNotFound):
        studio.subjects.get_subject("ZZ9")


def test_list_subjects():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_subject("CS1")
    studio.create_subject("CM1")
    codes = {s.subject_code for s in studio.subjects.list_subjects()}
    assert codes == {"CS1", "CM1"}


@pytest.mark.parametrize("i", range(25))
def test_open_workspace_use_case(i):
    studio = make_studio()
    snap = studio.open_workspace(f"ws-{i}", "CS1", subject_title="T")
    assert snap.workspace_id == f"ws-{i}"
    assert studio.registry.activity_count >= 1


@pytest.mark.parametrize("i", range(15))
def test_upload_sources_use_case(i):
    studio, mgmt, ingestion, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-u-{i}")
    studio.versions.assign_version(f"ws-u-{i}", "2026.1", version_id=f"ver-u-{i}")
    snap = studio.upload_sources(
        f"ws-u-{i}",
        cmp_reference=f"ref://cmp/{i}",
        syllabus_reference=f"ref://syl/{i}",
    )
    assert snap.workspace_id == f"ws-u-{i}"
    assert studio.registry.get_workspace(f"ws-u-{i}").facts.cmp_uploaded
    assert studio.registry.get_workspace(f"ws-u-{i}").facts.official_syllabus_uploaded
    assert len(mgmt.list_assets(f"ver-u-{i}")) == 2
    assert len(ingestion.start_calls) == 1


@pytest.mark.parametrize("i", range(12))
def test_validate_curriculum_use_case(i):
    studio, mgmt, ingestion, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-v-{i}")
    studio.versions.assign_version(f"ws-v-{i}", "2026.1", version_id=f"ver-v-{i}")
    studio.upload_sources(
        f"ws-v-{i}",
        cmp_reference="ref://cmp",
        syllabus_reference="ref://syl",
    )
    snap = studio.validation.validate_curriculum(f"ws-v-{i}")
    assert snap.passed is True
    assert f"ver-v-{i}" in mgmt.validate_calls


def test_validate_curriculum_requires_version():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio)
    with pytest.raises(ValidationError):
        studio.validation.validate_curriculum("ws-1")


@pytest.mark.parametrize("i", range(12))
def test_generate_preview_use_case(i):
    studio, mgmt, _, platform = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-p-{i}")
    studio.versions.assign_version(f"ws-p-{i}", "2026.1", version_id=f"ver-p-{i}")
    snap = studio.preview.preview(f"ws-p-{i}")
    assert snap.node_count >= 1
    assert platform.surface_calls


@pytest.mark.parametrize("i", range(10))
def test_approve_curriculum_use_case(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-a-{i}", ready=True)
    studio.versions.assign_version(f"ws-a-{i}", "2026.1", version_id=f"ver-a-{i}")
    studio.versions.create_rollback_snapshot(f"ver-a-{i}")
    snap = studio.publication.approve(f"ws-a-{i}")
    assert f"ver-a-{i}" in mgmt.approve_calls
    assert snap.workspace_id == f"ws-a-{i}"


@pytest.mark.parametrize("i", range(10))
def test_publish_curriculum_use_case(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-pub-{i}", ready=True)
    studio.versions.assign_version(
        f"ws-pub-{i}", "2026.1", version_id=f"ver-pub-{i}"
    )
    studio.versions.create_rollback_snapshot(f"ver-pub-{i}")
    studio.publication.update_facts(
        f"ws-pub-{i}",
        version_assigned=True,
        rollback_snapshot_created=True,
        preview_approved=True,
        validation_passed=True,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        blueprint_assigned=True,
    )
    snap = studio.publication.publish(f"ws-pub-{i}")
    assert snap.lifecycle_status == "published"
    assert f"ver-pub-{i}" in mgmt.publish_calls


@pytest.mark.parametrize("label", VERSION_LABELS)
def test_view_version_history_use_case(label):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{label}")
    studio.versions.assign_version(
        f"ws-{label}", label, version_id=f"ver-{label}"
    )
    hist = studio.versions.history("CS1")
    assert any(r.version_label == label for r in hist.records)


@pytest.mark.parametrize("i", range(8))
def test_archive_version_use_case(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-ar-{i}")
    studio.versions.assign_version(f"ws-ar-{i}", "2026.1", version_id=f"ver-ar-{i}")
    studio.versions.publish_version(f"ver-ar-{i}")
    snap = studio.versions.archive_version(f"ver-ar-{i}")
    assert snap.status == "archived"
    assert f"ver-ar-{i}" in mgmt.archive_calls


@pytest.mark.parametrize("i", range(8))
def test_rollback_version_use_case(i):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-rb-{i}")
    studio.versions.assign_version(f"ws-rb-{i}", "2026.1", version_id=f"ver-rb-{i}")
    studio.versions.create_rollback_snapshot(f"ver-rb-{i}")
    studio.versions.publish_version(f"ver-rb-{i}")
    snap = studio.versions.rollback_version(f"ver-rb-{i}")
    assert snap.version_id == f"ver-rb-{i}"


@pytest.mark.parametrize("i", range(10))
def test_compare_versions_via_ingestion(i):
    studio, _, ingestion, _ = make_studio_with_ports()
    left = ingestion.start_ingestion(
        subject_code="CS1", sources=[{"kind": "cmp", "reference": "a"}]
    )
    ingestion.start_ingestion(
        subject_code="CS1", sources=[{"kind": "cmp", "reference": "b"}]
    )
    # Force distinct titles
    job_l = left["job_id"]
    job_r = "job-x"
    ingestion._jobs[job_r] = {  # noqa: SLF001
        "job_id": job_r,
        "subject_code": "CS1",
        "state": "completed",
        "sources": [],
    }
    snap = studio.diff.compare_ingestion_jobs(job_l, job_r)
    assert snap.change_count >= 0


def test_seed_publishable_then_dashboard():
    studio = seed_publishable()
    studio.publication.publish("ws-1")
    dash = studio.founder_dashboard()
    assert dash.published_count >= 1
    assert dash.recent_activity
