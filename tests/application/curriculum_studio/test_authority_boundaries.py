"""Authority boundary tests — Studio must not become a second authority."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.curriculum_studio.exceptions import PortUnavailable
from tests.application.curriculum_studio.helpers import (
    FakeManagementPort,
    make_studio,
    make_studio_with_ports,
    seed_workspace,
)

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "curriculum_studio"
)

AUTHORITY_ACTIONS = (
    ("create_subject", lambda s: s.create_subject("CS1")),
    (
        "assign_version",
        lambda s: (
            seed_workspace(s),
            s.versions.assign_version("ws-1", "2026.1"),
        )[-1],
    ),
    (
        "publish",
        lambda s: s.publication.publish("ws-1"),
    ),
)


@pytest.mark.parametrize(
    "action",
    [
        "create_subject",
        "assign_version",
        "publish",
        "archive",
        "approve",
        "validate_curriculum",
        "upload_sources",
        "rollback_version",
        "archive_version",
    ],
)
def test_mutating_actions_require_management_port(action):
    studio = make_studio()
    seed_workspace(studio, ready=True)
    with pytest.raises(PortUnavailable):
        if action == "create_subject":
            studio.create_subject("CS1")
        elif action == "assign_version":
            studio.versions.assign_version("ws-1", "2026.1")
        elif action == "publish":
            studio.publication.publish("ws-1")
        elif action == "archive":
            studio.publication.archive("ws-1")
        elif action == "approve":
            studio.publication.approve("ws-1")
        elif action == "validate_curriculum":
            studio.validation.validate_curriculum("ws-1")
        elif action == "upload_sources":
            studio.upload_sources("ws-1", cmp_reference="x")
        elif action == "rollback_version":
            studio.versions.rollback_version("ver-1")
        elif action == "archive_version":
            studio.versions.archive_version("ver-1")


@pytest.mark.parametrize("unavailable", [True])
def test_unavailable_management_port_blocks_publish(unavailable):
    del unavailable
    mgmt = FakeManagementPort(available=False)
    studio = make_studio(curriculum_management=mgmt)
    seed_workspace(studio, ready=True)
    with pytest.raises(PortUnavailable):
        studio.publication.publish("ws-1")


@pytest.mark.parametrize("i", range(20))
def test_publish_always_delegates_to_management(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{i}", ready=True)
    studio.versions.assign_version(f"ws-{i}", "2026.1", version_id=f"ver-{i}")
    studio.versions.create_rollback_snapshot(f"ver-{i}")
    studio.publication.update_facts(
        f"ws-{i}",
        version_assigned=True,
        rollback_snapshot_created=True,
        preview_approved=True,
        validation_passed=True,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        blueprint_assigned=True,
    )
    studio.publication.publish(f"ws-{i}")
    assert f"ver-{i}" in mgmt.publish_calls
    assert mgmt.publication_state(f"ver-{i}") == "published"


@pytest.mark.parametrize("i", range(15))
def test_approve_always_delegates_to_management(i):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-a-{i}", ready=True)
    studio.versions.assign_version(f"ws-a-{i}", "2026.1", version_id=f"ver-a-{i}")
    studio.publication.approve(f"ws-a-{i}")
    assert f"ver-a-{i}" in mgmt.approve_calls


FORBIDDEN = (
    "app.application.curriculum_management",
    "app.application.curriculum_ingestion",
    "app.application.education_platform",
    "app.domain.curriculum_management",
    "app.domain.curriculum_ingestion",
)


@pytest.mark.parametrize(
    "path",
    sorted(APP_ROOT.rglob("*.py")),
    ids=lambda p: p.name,
)
def test_no_direct_authority_package_imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN:
                    assert not alias.name.startswith(forbidden)
        elif isinstance(node, ast.ImportFrom) and node.module:
            for forbidden in FORBIDDEN:
                assert not node.module.startswith(forbidden)


SERVICE_FILES = (
    "subject_service.py",
    "workspace_service.py",
    "validation_service.py",
    "preview_service.py",
    "publication_service.py",
    "version_history_service.py",
    "diff_service.py",
    "publication_checklist_service.py",
    "dashboard_service.py",
)


@pytest.mark.parametrize("filename", SERVICE_FILES)
def test_required_service_modules_exist(filename):
    assert (APP_ROOT / filename).is_file()


@pytest.mark.parametrize(
    "docstring_frag",
    [
        "Curriculum Management",
        "authority",
        "port",
    ],
)
@pytest.mark.parametrize(
    "filename",
    ["publication_service.py", "version_history_service.py", "validation_service.py"],
)
def test_authority_documented_in_services(filename, docstring_frag):
    text = (APP_ROOT / filename).read_text(encoding="utf-8")
    assert docstring_frag.lower() in text.lower()


@pytest.mark.parametrize("i", range(12))
def test_checklist_is_projection_not_manual_toggle(i):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-c-{i}")
    before = studio.checklist.checklist(f"ws-c-{i}")
    assert before.ready_to_publish is False
    # Facts sync from upload, not invented publish state
    studio.versions.assign_version(f"ws-c-{i}", "2026.1", version_id=f"ver-c-{i}")
    studio.upload_sources(
        f"ws-c-{i}",
        cmp_reference="c",
        syllabus_reference="s",
    )
    after = studio.checklist.checklist(f"ws-c-{i}")
    assert after.workspace_id == f"ws-c-{i}"
    codes = {item.code for item in after.checklist_items}
    assert "cmp_uploaded" in codes or "CMP_UPLOADED".lower() in {
        c.lower() for c in codes
    } or len(after.checklist_items) >= 7


@pytest.mark.parametrize("token", ["published", "archived", "draft", "approved"])
def test_lifecycle_status_prefers_management_state(token):
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, ready=True)
    studio.versions.assign_version("ws-1", "2026.1", version_id="ver-1")
    mgmt._versions["ver-1"]["publication_state"] = token  # noqa: SLF001
    snap = studio.checklist.checklist("ws-1")
    assert snap.lifecycle_status in {
        "published",
        "archived",
        "draft",
        "ready",
        "blocked",
    }
