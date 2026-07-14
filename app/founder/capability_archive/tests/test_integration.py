"""Integration tests for CapabilityArchiveQueryService (FSI-001).

Uses temporary repository fixtures — never the real project tree.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.capability_archive import CapabilityArchiveQueryService
from app.founder.capability_archive.tests.helpers import sample_entry, write_entry


class TestCapabilityArchiveQueryServiceIntegration:
    def test_successful_archive_scan(self, archive_repo: Path) -> None:
        service = CapabilityArchiveQueryService(repo_root=archive_repo)
        summary = service.get_summary()
        assert summary.source_version == "capability-archive-1.0"
        assert summary.total_count == 2
        assert summary.completed_count == 1
        assert summary.active_count == 1
        assert summary.archive_inconsistencies == 0
        assert summary.current_release == "1.0"
        assert "CAP-002" in summary.recent_capability_ids

    def test_dto_completeness_and_immutability(self, archive_repo: Path) -> None:
        service = CapabilityArchiveQueryService(repo_root=archive_repo)
        records = service.list_capabilities()
        assert len(records) == 2
        for record in records:
            assert record.capability_id
            assert record.status
            assert record.version
            assert record.completion_date
            assert record.programme
            assert record.subsystem
            assert isinstance(record.related_documents, tuple)
            payload = str(record)
            assert str(archive_repo) not in payload
            assert ".json" not in payload

        one = service.get_capability("CAP-001")
        assert one is not None
        assert one.capability_id == "CAP-001"
        assert service.get_capability("MISSING") is None

    def test_missing_fields_reported(self, archive_repo: Path) -> None:
        entries = archive_repo / "research" / "capability_archive" / "entries"
        write_entry(
            entries / "CAP-BAD.json",
            {
                "capability_id": "CAP-BAD",
                "status": "active",
                # missing version, completion_date, programme, subsystem,
                # related_documents
            },
        )
        service = CapabilityArchiveQueryService(repo_root=archive_repo)
        summary = service.get_summary()
        assert summary.archive_inconsistencies > 0
        assert summary.missing_artefacts
        issues = service.list_validation_issues()
        assert any(i.code == "missing_field" for i in issues)
        assert any(i.capability_id == "CAP-BAD" for i in issues)

    def test_duplicate_capability_ids_reported(self, archive_repo: Path) -> None:
        entries = archive_repo / "research" / "capability_archive" / "entries"
        write_entry(
            entries / "CAP-001-dup.json",
            sample_entry(
                capability_id="CAP-001",
                title="Duplicate",
                completion_date="2026-07-11",
            ),
        )
        service = CapabilityArchiveQueryService(repo_root=archive_repo)
        summary = service.get_summary()
        assert "CAP-001" in summary.duplicate_capability_ids
        assert summary.archive_inconsistencies >= 1
        issues = service.list_validation_issues()
        assert any(i.code == "duplicate_capability_id" for i in issues)

    def test_missing_archive_root_reported(self, tmp_path: Path) -> None:
        root = tmp_path / "empty"
        root.mkdir()
        (root / "pyproject.toml").write_text('[project]\nname="x"\n', encoding="utf-8")
        (root / "app").mkdir()
        service = CapabilityArchiveQueryService(repo_root=root)
        summary = service.get_summary()
        assert summary.total_count == 0
        assert summary.archive_inconsistencies >= 1
        assert summary.missing_artefacts
        issues = service.list_validation_issues()
        assert any(i.code == "missing_archive_root" for i in issues)
