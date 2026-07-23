"""GA-001 WS8/WS9 — production documentation and release checklist verification."""

from __future__ import annotations

import re

import pytest

from tests.ga.helpers import (
    REPO_ROOT,
    REQUIRED_GA_CHECKLIST_SECTIONS,
    REQUIRED_GA_DOCS,
    REQUIRED_PRODUCTION_DOCS,
)

PRODUCTION_SECTION_MARKERS = {
    "docs/production/DEPLOYMENT.md": ("Deploy", "Rollback", "health"),
    "docs/production/RUNBOOK.md": ("health",),
    "docs/production/INCIDENT_RESPONSE.md": ("severity", "correlation"),
    "docs/production/RELEASE_PROCESS.md": ("gate", "VERSION"),
    "docs/production/VERSIONING_POLICY.md": ("VERSION", "semver"),
    "docs/production/CONSOLE_OPERATIONS.md": ("console", "capability", "403"),
    "docs/production/BACKUP_AND_RECOVERY.md": ("pg_dump", "restore"),
    "docs/production/ACCESSIBILITY_AUDIT.md": ("WCAG", "skip"),
    "docs/production/ENVIRONMENT.md": ("SECRET_KEY", "DATABASE_URL"),
}


class TestProductionDocumentation:
    def test_all_production_docs_exist(self) -> None:
        missing = [
            path
            for path in REQUIRED_PRODUCTION_DOCS
            if not (REPO_ROOT / path).is_file()
        ]
        assert not missing, f"Missing: {missing}"

    @pytest.mark.parametrize(
        "path,markers",
        list(PRODUCTION_SECTION_MARKERS.items()),
        ids=list(PRODUCTION_SECTION_MARKERS),
    )
    def test_production_doc_content(
        self, path: str, markers: tuple[str, ...]
    ) -> None:
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in markers:
            assert marker.lower() in lowered, f"{path} missing marker {marker!r}"


class TestGaDocumentation:
    def test_ga_docs_exist(self) -> None:
        missing = [
            path for path in REQUIRED_GA_DOCS if not (REPO_ROOT / path).is_file()
        ]
        assert not missing, f"Missing GA docs: {missing}"

    def test_release_checklist_covers_deploy_gates(self) -> None:
        text = (REPO_ROOT / "docs/ga/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        for section in REQUIRED_GA_CHECKLIST_SECTIONS:
            assert section in text, f"Checklist missing section: {section}"

    def test_certification_report_required_sections(self) -> None:
        text = (REPO_ROOT / "docs/ga/CERTIFICATION_REPORT.md").read_text(
            encoding="utf-8"
        )
        required = (
            "Architecture status",
            "Security status",
            "Performance status",
            "Operational status",
            "Known limitations",
            "Release recommendation",
        )
        missing = [h for h in required if h not in text]
        assert not missing, f"Certification report missing: {missing}"

    def test_cursor_release_checklist_references_health(self) -> None:
        text = (REPO_ROOT / ".cursor/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        assert "health/ready" in text
        assert "docs/ga" in text or "GA-001" in text

    def test_governance_release_checklist_still_present(self) -> None:
        assert (REPO_ROOT / ".cursor/RELEASE_CHECKLIST.md").is_file()
        text = (REPO_ROOT / ".cursor/RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        assert re.search(r"pytest", text, re.I)
        assert re.search(r"ruff", text, re.I)
