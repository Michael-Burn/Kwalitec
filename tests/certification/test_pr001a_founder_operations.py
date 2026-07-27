"""PR-001A — Founder Operations Certification acceptance tests.

Certifies that a founder can complete publish workflows and recover from
common operational failures without developer intervention.
"""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import (
    SubjectAlreadyExists,
    ValidationError,
    VersionError,
)
from app.application.curriculum_studio.validation_guidance import (
    VALIDATION_FINDING_GUIDANCE,
    enrich_finding,
    guided_finding,
)
from app.domain.curriculum_studio.validation_summary import (
    ValidationFinding,
    ValidationFindingSeverity,
)
from app.presentation.curriculum_studio.operator_guidance import recover_flash
from app.presentation.curriculum_studio.view_models import FLASH_WARNING
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)
from tests.presentation.curriculum_studio.helpers import login_founder, wire_studio


@pytest.fixture
def founder_client(app, client, ctx):
    studio = wire_studio(app, with_workspace=False)
    login_founder(client, app)
    return client, studio


class TestFounderHappyPath:
    """Acceptance: create → upload → validate → review → publish → verify."""

    def test_create_subject(self, founder_client):
        client, studio = founder_client
        response = client.post(
            "/console/studio/subjects",
            data={"subject_code": "OP01", "title": "Operations Cert"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "created your subject successfully" in html.lower()
        subjects = studio.subjects.list_subjects()
        codes = {s.subject_code for s in subjects}
        assert "OP01" in codes

    def test_open_workspace_after_subject(self, founder_client):
        client, studio = founder_client
        studio.create_subject("OP02", title="Workspace Path")
        response = client.post(
            "/console/studio/workspaces",
            data={"subject_code": "OP02"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "opened your workspace successfully" in html.lower()
        assert "ws-op02" in html.lower() or "OP02" in html

    def test_full_service_publish_path(self, ctx):
        """End-to-end service path used by Studio publish."""
        studio, mgmt, _, _ = make_studio_with_ports()
        studio.create_subject("OP03", title="Full Path")
        studio.create_workspace(
            "ws-op03",
            "OP03",
            section_ids=("s1",),
            topic_ids=("t1",),
            objective_ids=("o1",),
        )
        studio.versions.assign_version("ws-op03", "2027.1", version_id="ver-op03")
        studio.upload_sources(
            "ws-op03",
            cmp_reference="ref://cmp/op03",
            syllabus_reference="ref://syllabus/op03",
        )
        studio.publication.update_facts(
            "ws-op03",
            cmp_uploaded=True,
            official_syllabus_uploaded=True,
            blueprint_assigned=True,
            version_assigned=True,
        )
        studio.workflow.advance("ws-op03")  # content_sources
        studio.workflow.advance("ws-op03")  # validation
        studio.validation.mark_passed("ws-op03")
        snap = studio.validation.summarise("ws-op03")
        assert snap.passed is True
        studio.workflow.advance("ws-op03")  # preview
        studio.preview.approve("ws-op03")
        studio.workflow.advance("ws-op03")  # approval
        studio.versions.create_rollback_snapshot("ver-op03")
        studio.publication.update_facts(
            "ws-op03",
            rollback_snapshot_created=True,
            preview_approved=True,
            validation_passed=True,
            cmp_uploaded=True,
            official_syllabus_uploaded=True,
            blueprint_assigned=True,
            version_assigned=True,
        )
        studio.workflow.advance("ws-op03")  # publication
        pub = studio.publication.publish("ws-op03", actor_id="founder")
        assert pub.lifecycle_status == "published"
        assert "ver-op03" in mgmt.publish_calls
        dashboard = studio.founder_dashboard()
        assert dashboard.published_count >= 1


class TestValidationExperience:
    """Acceptance: every guided finding explains issue, why, recovery."""

    @pytest.mark.parametrize("code", list(VALIDATION_FINDING_GUIDANCE))
    def test_catalog_entries_have_three_parts(self, code):
        guide = VALIDATION_FINDING_GUIDANCE[code]
        assert guide.issue.strip()
        assert guide.why_it_matters.strip()
        assert guide.recovery_action.strip()

    def test_missing_sources_produce_guided_findings(self, ctx):
        studio, _, _, _ = make_studio_with_ports()
        seed_workspace(studio, workspace_id="ws-val", subject_code="VAL1")
        snap = studio.validation.summarise("ws-val")
        codes = {e.code for e in snap.errors}
        assert "missing_cmp" in codes or "missing_syllabus" in codes
        for finding in snap.errors:
            assert finding.why_it_matters
            assert finding.recovery_action

    def test_enrich_finding_fills_defaults(self):
        raw = ValidationFinding.create(
            "custom_gap",
            "Structure incomplete",
            severity=ValidationFindingSeverity.BLOCKING,
        )
        enriched = enrich_finding(raw)
        assert enriched.why_it_matters
        assert enriched.recovery_action

    def test_workspace_renders_findings(self, app, client, ctx):
        studio = wire_studio(app, with_workspace=True)
        login_founder(client, app)
        # Fresh workspace without sources → missing CMP/syllabus findings
        html = client.get("/console/studio/workspaces/ws-cs1").get_data(
            as_text=True
        )
        assert "Validation" in html
        # Either findings panel or readiness copy is present
        snap = studio.validation.summarise("ws-cs1")
        if snap.errors:
            assert "Validation findings" in html or "needs attention" in html.lower()


class TestOperationalErrorRecovery:
    """Acceptance: common failure modes map to recovery guidance."""

    def test_duplicate_subject_flash(self):
        msg = recover_flash(SubjectAlreadyExists("CS1"), "subject_create")
        lowered = msg.lower()
        assert "already exists" in lowered
        assert "try again" in lowered
        assert "version" in lowered or "enrol" in lowered or "enrolment" in lowered

    def test_validation_requires_version_flash(self):
        msg = recover_flash(
            ValidationError("Validation requires version for ws-1"),
            "validate",
        )
        assert "version" in msg.lower()
        assert "try again" in msg.lower()

    def test_validation_failed_flash(self):
        msg = recover_flash(
            ValidationError("Validation failed for ws-1: 2 error(s)"),
            "validate",
        )
        assert "blocking" in msg.lower() or "findings" in msg.lower()
        assert "try again" in msg.lower()

    def test_version_conflict_flash(self):
        msg = recover_flash(
            VersionError("Version already exists: ver-1"),
            "version",
        )
        assert "already" in msg.lower()
        assert "try again" in msg.lower()

    def test_http_duplicate_subject_recovery(self, founder_client):
        client, studio = founder_client
        studio.create_subject("DUP1", title="First")
        response = client.post(
            "/console/studio/subjects",
            data={"subject_code": "DUP1", "title": "Second"},
            follow_redirects=True,
        )
        html = response.get_data(as_text=True).lower()
        assert "already exists" in html or "couldn't create" in html
        assert "try again" in html

    def test_upload_without_file_returns_validation_error(self, app, client, ctx):
        wire_studio(app, with_workspace=True)
        login_founder(client, app)
        response = client.post(
            "/console/studio/workspaces/ws-cs1/documents",
            data={"kind": "cmp"},
            content_type="multipart/form-data",
        )
        payload = response.get_json()
        assert response.status_code == 400
        assert payload["ok"] is False
        assert "pdf" in payload["error"].lower() or "choose" in payload["error"].lower()

    def test_publish_without_readiness_recovers(self, app, client, ctx):
        wire_studio(app, with_workspace=True)
        login_founder(client, app)
        response = client.post(
            "/console/studio/workspaces/ws-cs1/publish",
            data={"workspace_id": "ws-cs1"},
            follow_redirects=True,
        )
        html = response.get_data(as_text=True).lower()
        assert "publish" in html
        assert "try again" in html
        assert "couldn" in html  # flash may HTML-escape couldn't

    @pytest.mark.parametrize("key", list(FLASH_WARNING))
    def test_flash_warnings_explain_recovery(self, key):
        msg = FLASH_WARNING[key]
        lowered = msg.lower()
        assert msg.endswith(".")
        assert "try again" in lowered
        # Issue + why + recovery: at least three sentences.
        assert msg.count(".") >= 2


class TestOperatorDocumentation:
    """Acceptance: operator docs exist for documentation-only quality gate."""

    def test_pr001a_deliverables_exist(self):
        from pathlib import Path

        root = (
            Path(__file__).resolve().parents[2]
            / "knowledge"
            / "product"
            / "pr001a"
        )
        required = (
            "FOUNDER_WORKFLOW_SPECIFICATION.md",
            "FOUNDER_USER_GUIDE.md",
            "SUBJECT_PUBLISHING_GUIDE.md",
            "VALIDATION_GUIDE.md",
            "OPERATIONAL_CHECKLIST.md",
            "TROUBLESHOOTING_GUIDE.md",
            "OPERATIONAL_RUNBOOK.md",
            "VALIDATION_UX_REVIEW.md",
            "ERROR_RECOVERY_MATRIX.md",
            "TEST_EVIDENCE.md",
            "COMPLETION_REPORT.md",
        )
        missing = [name for name in required if not (root / name).is_file()]
        assert not missing, f"Missing PR-001A docs: {missing}"

    def test_guided_finding_factory(self):
        finding = guided_finding("missing_cmp")
        assert finding.code == "missing_cmp"
        assert finding.is_blocking
        assert "CMP" in finding.message or "cmp" in finding.message.lower()
        assert finding.why_it_matters
        assert finding.recovery_action
