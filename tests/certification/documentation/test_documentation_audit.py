"""Documentation certification — capability docs, ADRs, handbook, READMEs."""

from __future__ import annotations

import re

from tests.certification.helpers import KNOWLEDGE_ROOT, REPO_ROOT

FOUNDER_DOCS = KNOWLEDGE_ROOT / "founder"
ARCHITECTURE = KNOWLEDGE_ROOT / "architecture"
ENGINEERING = KNOWLEDGE_ROOT / "engineering"
ARCHIVE_ENTRIES = REPO_ROOT / "research" / "capability_archive" / "entries"

# Documented Founder + FSI capability set for production certification.
REQUIRED_FOUNDER_DOCS = (
    "FSI-001_KNOWLEDGE_INTEGRATION.md",
    "FSI-002_DASHBOARD_LIVE_INTEGRATION.md",
    "FSI-003_INTERNAL_ALPHA_LIVE_WORKFLOW.md",
    "FSI-005_OPERATIONAL_CERTIFICATION.md",
    "FOS-003_INTERNAL_ALPHA_PIPELINE.md",
    "FOS-004_FOUNDER_DASHBOARD.md",
    "FOS-005_OPERATIONAL_STATE.md",
    "FOS-006_RECOMMENDATION_ENGINE.md",
    "FOS-007_FOUNDER_WEEKLY_BRIEFING.md",
)

REQUIRED_ADR_FILES = (
    "ADR-001-service-layer.md",
    "ADR-002-blueprint-architecture.md",
    "ADR-003-curriculum-v1-v2.md",
    "ADR-004-canonical-topic-traversal.md",
    "ADR-005-testing-strategy.md",
)

REQUIRED_ARCHIVE_IDS = (
    "FOS-003",
    "FOS-004",
    "FOS-005",
    "FOS-006",
    "FOS-007",
    "FSI-001",
    "FSI-002",
    "FSI-003",
    "FSI-004",
    "FSI-005",
)

HANDBOOK = ENGINEERING / "handbook" / "ENG-001_ENGINEERING_HANDBOOK.md"
AUTOMATION_DOC = ENGINEERING / "automation" / "AUTOMATION_FRAMEWORK.md"


def _markdown_links(text: str) -> list[str]:
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)


class TestDocumentationAudit:
    def test_founder_capability_docs_exist(self) -> None:
        missing = [
            name
            for name in REQUIRED_FOUNDER_DOCS
            if not (FOUNDER_DOCS / name).is_file()
        ]
        assert not missing, f"Missing founder docs: {missing}"

    def test_fsi004_automation_doc_exists(self) -> None:
        assert AUTOMATION_DOC.is_file()
        text = AUTOMATION_DOC.read_text(encoding="utf-8")
        assert "FSI-004" in text
        assert "Automation" in text

    def test_adr_index_complete(self) -> None:
        missing = [
            name
            for name in REQUIRED_ADR_FILES
            if not (ARCHITECTURE / name).is_file()
        ]
        assert not missing, f"Missing ADRs: {missing}"
        for name in REQUIRED_ADR_FILES:
            text = (ARCHITECTURE / name).read_text(encoding="utf-8")
            assert re.search(r"(?i)status", text)
            assert re.search(r"(?i)accepted", text)

    def test_engineering_handbook_present(self) -> None:
        assert HANDBOOK.is_file()
        text = HANDBOOK.read_text(encoding="utf-8")
        assert "ENG-001" in text
        assert "Engineering" in text

    def test_founder_readme_navigation(self) -> None:
        readme = FOUNDER_DOCS / "README.md"
        assert readme.is_file()
        text = readme.read_text(encoding="utf-8")
        for name in REQUIRED_FOUNDER_DOCS:
            assert name in text, f"README missing link to {name}"
        # Relative markdown links resolve on disk.
        for _label, target in _markdown_links(text):
            if target.startswith(("http://", "https://", "#")):
                continue
            linked = (FOUNDER_DOCS / target).resolve()
            assert linked.is_file(), f"Broken README link: {target}"

    def test_knowledge_readme_references_architecture(self) -> None:
        readme = KNOWLEDGE_ROOT / "README.md"
        text = readme.read_text(encoding="utf-8")
        for adr in REQUIRED_ADR_FILES:
            assert adr.replace(".md", "") in text or adr in text

    def test_capability_archive_entries_complete(self) -> None:
        missing = [
            cap_id
            for cap_id in REQUIRED_ARCHIVE_IDS
            if not (ARCHIVE_ENTRIES / f"{cap_id}.json").is_file()
        ]
        assert not missing, f"Missing archive entries: {missing}"

    def test_certification_report_sections(self) -> None:
        report = FOUNDER_DOCS / "FSI-005_OPERATIONAL_CERTIFICATION.md"
        text = report.read_text(encoding="utf-8")
        required_headings = (
            "Executive Summary",
            "Scope",
            "Test Results",
            "Performance Metrics",
            "Architecture Compliance",
            "Risks",
            "Technical Debt",
            "Production Readiness Decision",
            "Production Checklist",
        )
        missing = [h for h in required_headings if h not in text]
        assert not missing, f"Certification report missing sections: {missing}"
