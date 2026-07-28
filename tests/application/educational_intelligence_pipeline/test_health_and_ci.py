"""Platform health, registration, and CI integration tests (PR-001)."""

from __future__ import annotations

from pathlib import Path

from app.application.educational_intelligence_pipeline.health import (
    EducationalPlatformHealth,
    check_certification_status,
    check_contract_versions,
    check_mission_registration,
    check_pipeline_registration,
    check_projection_registration,
    check_tutor_registration,
)
from app.application.educational_intelligence_pipeline.registry import (
    COMPONENT_REGISTRATIONS,
    pipeline_manifest,
    probe_all_registrations,
)
from app.application.educational_intelligence_pipeline.versions import (
    CERTIFICATION_STATUS,
    ORCHESTRATOR_VERSION,
    PIPELINE_STAGE_ORDER,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


class TestHealthChecks:
    def test_all_readiness_checks_pass(self) -> None:
        report = EducationalPlatformHealth.check()
        assert report.ready is True
        assert report.status == "ok"
        assert report.certification_status == "certified"
        names = {c.name for c in report.checks}
        assert names == {
            "contract_versions",
            "pipeline_registration",
            "projection_registration",
            "mission_registration",
            "tutor_registration",
            "certification_status",
        }

    def test_individual_checks(self) -> None:
        assert check_contract_versions().status == "ok"
        assert check_pipeline_registration().status == "ok"
        assert check_projection_registration().status == "ok"
        assert check_mission_registration().status == "ok"
        assert check_tutor_registration().status == "ok"
        assert check_certification_status().status == "ok"

    def test_health_endpoint(self, client) -> None:
        response = client.get("/health/educational-intelligence")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["ready"] is True
        assert payload["orchestrator_version"] == ORCHESTRATOR_VERSION
        assert payload["certification_status"] == CERTIFICATION_STATUS


class TestRegistration:
    def test_all_components_registered(self) -> None:
        statuses = probe_all_registrations()
        assert len(statuses) == len(COMPONENT_REGISTRATIONS)
        assert all(s.available for s in statuses)

    def test_pipeline_manifest(self) -> None:
        manifest = pipeline_manifest()
        assert manifest["orchestrator_version"] == ORCHESTRATOR_VERSION
        assert manifest["certification_status"] == "certified"
        assert manifest["stage_order"] == list(PIPELINE_STAGE_ORDER)
        assert "pipeline_orchestrator" in manifest["components"]
        assert "graph_projection" in manifest["components"]
        assert "mission_planning" in manifest["components"]
        assert "tutor_explanation" in manifest["components"]


class TestCiIntegration:
    def test_ci_runs_educational_intelligence_certification(self) -> None:
        text = CI_WORKFLOW.read_text(encoding="utf-8")
        assert "educational-intelligence-certification" in text
        assert "tests/certification/educational_intelligence/" in text
        assert "Educational Intelligence Certification" in text

    def test_certification_suite_is_importable(self) -> None:
        from tests.certification.educational_intelligence import (  # noqa: F401
            pipeline_harness,
        )
        from tests.certification.educational_intelligence.pipeline_harness import (
            EducationalIntelligencePipelineHarness,
        )

        assert EducationalIntelligencePipelineHarness is not None
