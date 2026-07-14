"""Resilience certification — missing / corrupt / empty inputs."""

from __future__ import annotations

from pathlib import Path

from app.founder.capability_archive import CapabilityArchiveQueryService
from app.founder.capability_archive.tests.helpers import build_archive_fixture
from app.founder.internal_alpha_workflow.tests.helpers import build_week
from app.founder.knowledge_engine import KnowledgeQueryService
from app.founder.knowledge_engine.tests.helpers import build_knowledge_fixture
from tests.certification.helpers import (
    CERT_NOW,
    make_workflow_service,
    write_corrupt_archive_entry,
    write_duplicate_archive_entries,
)


class TestMissingAndCorruptInputs:
    def test_missing_knowledge_roots_reported(self, tmp_path: Path) -> None:
        root = tmp_path / "empty_repo"
        root.mkdir()
        (root / "pyproject.toml").write_text(
            '[project]\nname = "empty"\n', encoding="utf-8"
        )
        (root / "app").mkdir()
        (root / "app" / "__init__.py").write_text("", encoding="utf-8")
        service = KnowledgeQueryService(repo_root=root)
        summary = service.get_summary()
        assert summary.indexed_artefacts == 0
        assert summary.missing_roots

    def test_missing_archive_entries_dir(self, tmp_path: Path) -> None:
        root = tmp_path / "no_archive"
        root.mkdir()
        (root / "pyproject.toml").write_text(
            '[project]\nname = "empty"\n', encoding="utf-8"
        )
        (root / "app").mkdir()
        (root / "app" / "__init__.py").write_text("", encoding="utf-8")
        service = CapabilityArchiveQueryService(repo_root=root)
        summary = service.get_summary()
        issues = service.list_validation_issues()
        assert summary.total_count == 0
        assert any(
            issue.code in {"missing_archive_root", "missing_entries_dir"}
            for issue in issues
        )

    def test_corrupt_archive_metadata(self, tmp_path: Path) -> None:
        root = build_archive_fixture(tmp_path / "corrupt")
        entries = root / "research" / "capability_archive" / "entries"
        write_corrupt_archive_entry(entries)
        service = CapabilityArchiveQueryService(repo_root=root)
        issues = service.list_validation_issues()
        assert any(issue.code == "unreadable_entry" for issue in issues)
        assert service.get_summary().total_count >= 2

    def test_duplicate_capability_ids(self, tmp_path: Path) -> None:
        root = build_archive_fixture(tmp_path / "dupes")
        entries = root / "research" / "capability_archive" / "entries"
        write_duplicate_archive_entries(entries)
        service = CapabilityArchiveQueryService(repo_root=root)
        summary = service.get_summary()
        assert "DUP-001" in summary.duplicate_capability_ids
        assert summary.archive_inconsistencies >= 1

    def test_empty_internal_alpha_week(self, tmp_path: Path) -> None:
        alpha_root = tmp_path / "research" / "internal_alpha"
        alpha_root.mkdir(parents=True)
        build_week(alpha_root, "week_001", with_feedback=False)
        result = make_workflow_service(alpha_root).run(
            week="week_001", generated_at=CERT_NOW
        )
        assert result.success is False
        assert result.pipeline_success is False
        assert any("raw_feedback" in err for err in result.errors)

    def test_invalid_week_folder(self, tmp_path: Path) -> None:
        alpha_root = tmp_path / "research" / "internal_alpha"
        alpha_root.mkdir(parents=True)
        build_week(alpha_root, "week_001", with_feedback=True)
        result = make_workflow_service(alpha_root).run(
            week="week_999", generated_at=CERT_NOW
        )
        assert result.success is False
        assert any("week_missing" in err for err in result.errors)

    def test_empty_knowledge_tree_still_indexes(self, tmp_path: Path) -> None:
        root = build_knowledge_fixture(tmp_path / "knowledge_only")
        for path in root.rglob("*.md"):
            path.unlink()
        service = KnowledgeQueryService(repo_root=root)
        summary = service.get_summary()
        assert summary.indexed_artefacts == 0
        assert isinstance(service.list_artefacts(), tuple)
