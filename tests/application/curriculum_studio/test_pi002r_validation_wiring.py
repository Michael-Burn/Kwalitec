"""PI-002R — Publication Validation Wiring tests.

Proves a single authoritative curriculum representation flows through
Validate → Preview → Approve → Publish, and that stub Ingestion jobs
never poison the Founder publication gate.
"""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import (
    PublicationError,
    ValidationError,
)
from app.application.curriculum_studio.validation_service import (
    _ingestion_job_is_authoritative,
    _map_report,
)
from app.domain.curriculum_studio.validation_summary import (
    ValidationFindingSeverity,
    ValidationReadiness,
)
from app.presentation.curriculum_studio.operator_guidance import recover_flash
from app.presentation.curriculum_studio.view_models import friendly_preview_summary
from tests.application.curriculum_studio.helpers import (
    FakeIngestionPort,
    FakeManagementPort,
    make_studio_with_ports,
    seed_workspace,
)

# ---------------------------------------------------------------------------
# Phase 1 / 2 — Validation authority + identity
# ---------------------------------------------------------------------------


def test_reference_only_upload_does_not_start_ingestion():
    studio, _, ingestion, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-ref")
    studio.versions.assign_version("ws-ref", "2026.1", version_id="ver-ref")
    studio.upload_sources(
        "ws-ref",
        cmp_reference="ref://cmp",
        syllabus_reference="ref://syl",
    )
    assert ingestion.start_calls == []
    assert studio.registry.get_ingestion_job("ws-ref") is None


def test_stub_ingestion_job_is_not_authoritative():
    ingestion = FakeIngestionPort()
    job = ingestion.start_ingestion(
        subject_code="CS1",
        sources=({"kind": "cmp", "reference": "ref://cmp"},),
    )
    # Override normalised structure to look like production stub (no objectives).
    jid = job["job_id"]
    ingestion.normalised_structure = (  # type: ignore[method-assign]
        lambda job_id: {
            "topics": [
                {"topic_id": "topic-e-1", "title": "Untitled", "objectives": ()}
            ]
        }
        if job_id == jid
        else None
    )
    assert _ingestion_job_is_authoritative(ingestion, jid) is False


def test_structured_ingestion_job_is_authoritative():
    ingestion = FakeIngestionPort()
    job = ingestion.start_ingestion(
        subject_code="CS1",
        sources=(
            {
                "kind": "cmp",
                "reference": "ref://cmp",
                "entries": (
                    {
                        "entry_id": "t1",
                        "entry_type": "topic",
                        "text": "Real topic",
                    },
                ),
            },
        ),
    )
    assert _ingestion_job_is_authoritative(ingestion, job["job_id"]) is True


def test_validate_ignores_stub_ingestion_and_uses_management():
    """Management pass + stub ingestion fail → Studio validation must pass."""
    studio, mgmt, ingestion, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-stub")
    studio.versions.assign_version("ws-stub", "2026.1", version_id="ver-stub")
    studio.upload_sources(
        "ws-stub",
        cmp_reference="ref://cmp",
        syllabus_reference="ref://syl",
        start_ingestion=False,
    )
    # Manually register a failing stub-like job.
    job = ingestion.start_ingestion(
        subject_code="CS1",
        sources=({"kind": "cmp", "reference": "ref://cmp"},),
    )
    jid = job["job_id"]
    studio.registry.set_ingestion_job("ws-stub", jid)
    ingestion.normalised_structure = (  # type: ignore[method-assign]
        lambda job_id: {
            "topics": [
                {"topic_id": "topic-e-1", "title": "Untitled", "objectives": ()}
            ]
        }
    )
    ingestion.get_validation_report = (  # type: ignore[method-assign]
        lambda job_id: {
            "passed": False,
            "readiness": "failed",
            "issues": [
                {
                    "code": "missing_objectives",
                    "message": "Topic topic-e-1 has no learning objectives",
                    "severity": "blocking",
                }
            ],
        }
    )

    snap = studio.validation.validate_curriculum("ws-stub")
    assert snap.passed is True
    assert "ver-stub" in mgmt.validate_calls
    ws = studio.registry.get_workspace("ws-stub")
    assert ws is not None
    assert ws.facts.validation_passed is True


def test_curriculum_identity_flows_validate_preview_approve_publish():
    """Same workspace + version identity through every publication stage."""
    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-id",
        "CSID",
        section_ids=("sec-a", "sec-b"),
        topic_ids=("top-a", "top-b", "top-c"),
        objective_ids=("obj-a", "obj-b"),
    )
    studio.publication.update_facts(
        "ws-id",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
    )
    studio.versions.assign_version("ws-id", "2026.1", version_id="ver-id")
    studio.upload_sources(
        "ws-id",
        cmp_reference="ref://cmp/csid",
        syllabus_reference="ref://syl/csid",
        start_ingestion=False,
    )

    val = studio.validation.validate_curriculum("ws-id")
    assert val.passed is True
    ws = studio.registry.get_workspace("ws-id")
    assert ws is not None
    assert ws.version_id == "ver-id"
    assert tuple(ws.section_ids) == ("sec-a", "sec-b")
    assert tuple(ws.topic_ids) == ("top-a", "top-b", "top-c")

    preview = studio.preview.build_for_review("ws-id")
    assert preview.workspace_id == "ws-id"
    assert preview.validation_passed is True
    assert preview.readiness == "ready_for_review"
    # Structure ids from validation must appear in preview hierarchy.
    preview_ids = {n.node_id for n in preview.hierarchy}
    assert {"sec-a", "sec-b", "top-a", "top-b", "top-c"} <= preview_ids
    assert preview.node_count >= 5

    approved = studio.publication.approve("ws-id")
    assert approved.workspace_id == "ws-id"
    ws = studio.registry.get_workspace("ws-id")
    assert ws is not None
    assert ws.facts.preview_approved is True
    assert ws.facts.validation_passed is True
    assert "ver-id" in mgmt.approve_calls

    studio.versions.create_rollback_snapshot("ver-id")
    studio.publication.update_facts(
        "ws-id",
        version_assigned=True,
        rollback_snapshot_created=True,
        intelligence_certified=True,
    )
    pub = studio.publication.publish("ws-id")
    assert pub.lifecycle_status == "published"
    assert "ver-id" in mgmt.publish_calls
    ws = studio.registry.get_workspace("ws-id")
    assert ws is not None
    assert ws.version_id == "ver-id"
    assert ws.status.value == "published"


# ---------------------------------------------------------------------------
# Phase 3 — Findings projection
# ---------------------------------------------------------------------------


def test_map_report_consumes_issues_array():
    errors: list = []
    warnings: list = []
    readiness, errors, warnings = _map_report(
        {
            "passed": False,
            "issues": [
                {
                    "code": "missing_objectives",
                    "message": "Topic has no objectives",
                    "severity": "blocking",
                },
                {
                    "code": "missing_metadata",
                    "message": "Missing subject_code",
                    "severity": "warning",
                },
            ],
        },
        errors,
        warnings,
    )
    assert readiness is ValidationReadiness.FAILED
    assert len(errors) == 1
    assert errors[0].code == "missing_objectives"
    assert errors[0].severity is ValidationFindingSeverity.BLOCKING
    assert len(warnings) == 1
    assert warnings[0].code == "missing_metadata"


def test_map_report_explicit_fail_without_issues_is_failed():
    readiness, errors, warnings = _map_report(
        {"passed": False, "blocks_publication": True},
        [],
        [],
    )
    assert readiness is ValidationReadiness.FAILED
    assert errors == []
    assert warnings == []


def test_friendly_preview_never_claims_ready_when_not_ready():
    summary = friendly_preview_summary(readiness="not_ready", node_count=12)
    assert "Preview ready" not in summary
    assert "needs attention" in summary.lower()


def test_approve_flash_does_not_use_publish_verbs():
    exc = PublicationError("Approval requires successful validation")
    message = recover_flash(exc, "approve")
    lowered = message.lower()
    assert "approve" in lowered or "validation" in lowered
    assert "publish this curriculum" not in lowered


def test_approve_flash_for_preview_gate():
    exc = PublicationError(
        "Approval requires a successful preview with curriculum content"
    )
    message = recover_flash(exc, "approve")
    assert "preview" in message.lower()
    assert "publish this curriculum" not in message.lower()


# ---------------------------------------------------------------------------
# Regression — safety gates remain enforced
# ---------------------------------------------------------------------------


def test_regression_empty_structure_fails_prepare():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace("ws-empty", "CS0")
    studio.versions.assign_version("ws-empty", "2026.1", version_id="ver-empty")
    with pytest.raises(ValidationError, match="No extracted curriculum"):
        studio.validation.validate_curriculum("ws-empty")


def test_regression_validation_requires_version():
    """Reconciliation creates a Management version when workspace has none."""
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-nover")
    assert studio.registry.get_workspace("ws-nover").version_id is None
    snap = studio.validation.validate_curriculum("ws-nover")
    assert snap.passed is True
    assert studio.registry.get_workspace("ws-nover").version_id


def test_regression_approval_requires_validation():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-noval")
    studio.versions.assign_version("ws-noval", "2026.1", version_id="ver-noval")
    studio.publication.update_facts(
        "ws-noval",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=False,
    )
    with pytest.raises(PublicationError, match="validation"):
        studio.publication.approve("ws-noval")


def test_regression_publish_requires_checklist():
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-nopub")
    studio.versions.assign_version("ws-nopub", "2026.1", version_id="ver-nopub")
    with pytest.raises(PublicationError, match="Not ready"):
        studio.publication.publish("ws-nopub")


def test_regression_management_failure_blocks_validation():
    """Management gate still blocks — we never bypass ValidationPolicy."""

    class FailingManagement(FakeManagementPort):
        def validate_version(self, version_id: str) -> dict:
            self.validate_calls.append(version_id)
            raise RuntimeError("EMPTY_PACKAGE")

    mgmt = FailingManagement()
    studio, _, _, _ = make_studio_with_ports(management=mgmt)
    seed_workspace(studio, workspace_id="ws-mgmt-fail")
    studio.versions.assign_version(
        "ws-mgmt-fail", "2026.1", version_id="ver-mgmt-fail"
    )
    studio.upload_sources(
        "ws-mgmt-fail",
        cmp_reference="ref://cmp",
        syllabus_reference="ref://syl",
        start_ingestion=False,
    )
    with pytest.raises(ValidationError, match="Validation failed"):
        studio.validation.validate_curriculum("ws-mgmt-fail")
    ws = studio.registry.get_workspace("ws-mgmt-fail")
    assert ws is not None
    assert ws.facts.validation_passed is False
