"""Integration tests for KnowledgeQueryService (FSI-001).

Uses temporary repository fixtures — never the real project tree.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.knowledge_engine import KnowledgeQueryService
from app.founder.knowledge_engine.config import (
    COLLECTION_ADR,
    COLLECTION_ENGINEERING_STANDARDS,
    COLLECTION_FOUNDER_CAPABILITY,
    COLLECTION_RESEARCH,
    KnowledgeEngineConfig,
)
from app.founder.knowledge_engine.tests.helpers import write_markdown


class TestKnowledgeQueryServiceIntegration:
    def test_successful_repository_scan(self, knowledge_repo: Path) -> None:
        service = KnowledgeQueryService(repo_root=knowledge_repo)
        summary = service.get_summary()
        assert summary.source_version == "knowledge-engine-1.0"
        assert summary.engineering_standards == 1
        assert summary.architecture_documents >= 2  # ADR + architecture
        assert summary.research_documents == 1
        assert summary.capability_documents == 1
        assert summary.indexed_artefacts >= 5
        assert summary.validation_errors == 0
        assert summary.tests_pass is True
        assert summary.missing_roots == ()

    def test_dto_completeness_and_no_path_leak(self, knowledge_repo: Path) -> None:
        service = KnowledgeQueryService(repo_root=knowledge_repo)
        artefacts = service.list_artefacts()
        assert artefacts
        root_text = str(knowledge_repo)
        for artefact in artefacts:
            assert artefact.artefact_id
            assert artefact.title
            assert artefact.collection
            payload = str(artefact)
            assert root_text not in payload
            assert "/" not in artefact.artefact_id
            assert "\\" not in artefact.artefact_id

    def test_collection_filter(self, knowledge_repo: Path) -> None:
        service = KnowledgeQueryService(repo_root=knowledge_repo)
        standards = service.list_artefacts(
            collection=COLLECTION_ENGINEERING_STANDARDS
        )
        assert len(standards) == 1
        assert standards[0].document_id == "ENG-001"
        research = service.list_artefacts(collection=COLLECTION_RESEARCH)
        assert len(research) == 1
        founder = service.list_artefacts(collection=COLLECTION_FOUNDER_CAPABILITY)
        assert len(founder) == 1
        adrs = service.list_artefacts(collection=COLLECTION_ADR)
        assert len(adrs) >= 2

    def test_missing_roots_reported(self, tmp_path: Path) -> None:
        root = tmp_path / "sparse"
        root.mkdir()
        (root / "pyproject.toml").write_text('[project]\nname="x"\n', encoding="utf-8")
        (root / "app").mkdir()
        (root / "knowledge").mkdir()
        write_markdown(
            root / "knowledge" / "note.md",
            title="Only Note",
            document_id="NOTE-1",
        )
        config = KnowledgeEngineConfig(
            scan_roots=("knowledge", "research", "docs/architecture", "docs/reviews")
        )
        service = KnowledgeQueryService(repo_root=root, config=config)
        summary = service.get_summary()
        assert "research" in summary.missing_roots
        assert "docs/architecture" in summary.missing_roots
        issues = service.list_validation_issues()
        assert any(i.code == "missing_root" for i in issues)
        assert summary.validation_errors >= 3
        assert summary.tests_pass is False

    def test_provider_connectivity_via_summary(self, knowledge_repo: Path) -> None:
        service = KnowledgeQueryService(repo_root=knowledge_repo)
        first = service.get_summary()
        service.refresh()
        second = service.get_summary()
        assert first == second
