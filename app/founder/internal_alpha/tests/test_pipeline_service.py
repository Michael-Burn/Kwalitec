"""Unit tests for InternalAlphaPipelineService end-to-end coordination."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from app.founder.internal_alpha.config import DEFAULT_OUTPUT_FILENAMES
from app.founder.internal_alpha.services import InternalAlphaPipelineService


class TestInternalAlphaPipelineService:
    def test_full_pipeline_success(self, week_dir: Path) -> None:
        stamp = datetime(2026, 7, 14, 16, 0, tzinfo=UTC)
        result = InternalAlphaPipelineService().run(
            week_dir,
            generated_at=stamp,
        )
        assert result.success is True
        assert len(result.processed_items) == 2
        assert result.warnings == ()
        assert len(result.output_files) == len(DEFAULT_OUTPUT_FILENAMES)

        processed = week_dir / "processed"
        for name in DEFAULT_OUTPUT_FILENAMES.values():
            assert (processed / name).is_file(), name

        classified = json.loads(
            (processed / "classified_feedback.json").read_text(encoding="utf-8")
        )
        assert classified["count"] == 2

        stats = json.loads(
            (processed / "feedback_statistics.json").read_text(encoding="utf-8")
        )
        assert stats["week"] == "2026-W28"
        assert stats["total_feedback"] == 2
        assert stats["generated_at"] == stamp.isoformat()

        summary_md = (processed / "WEEK_SUMMARY.md").read_text(encoding="utf-8")
        assert "2026-W28" in summary_md
        assert "Total feedback: 2" in summary_md

        architecture = (processed / "architecture.md").read_text(encoding="utf-8")
        assert "Architecture" in architecture

    def test_pipeline_deterministic_outputs(self, week_dir: Path) -> None:
        stamp = datetime(2026, 7, 14, 16, 0, tzinfo=UTC)
        first = InternalAlphaPipelineService().run(week_dir, generated_at=stamp)
        # Reset processed and re-run
        for path in (week_dir / "processed").iterdir():
            path.unlink()
        second = InternalAlphaPipelineService().run(week_dir, generated_at=stamp)
        assert [i.feedback_item.id for i in first.processed_items] == [
            i.feedback_item.id for i in second.processed_items
        ]
        assert [i.category for i in first.processed_items] == [
            i.category for i in second.processed_items
        ]
        classified_a = (week_dir / "processed" / "classified_feedback.json").read_text(
            encoding="utf-8"
        )
        # Third run for byte-stable JSON with same stamp
        for path in (week_dir / "processed").iterdir():
            path.unlink()
        InternalAlphaPipelineService().run(week_dir, generated_at=stamp)
        classified_b = (week_dir / "processed" / "classified_feedback.json").read_text(
            encoding="utf-8"
        )
        assert classified_a == classified_b

    def test_validation_failure(self, tmp_path: Path) -> None:
        result = InternalAlphaPipelineService().run(tmp_path / "absent")
        assert result.success is False
        assert result.processed_items == ()
        assert result.output_files == ()
        assert any("week_missing" in w for w in result.warnings)

    def test_duplicate_annotation(self, tmp_path: Path) -> None:
        week = tmp_path / "dup-week"
        raw = week / "raw_feedback"
        raw.mkdir(parents=True)
        (raw / "one.txt").write_text("Identical body text", encoding="utf-8")
        (raw / "two.txt").write_text("Identical body text", encoding="utf-8")
        result = InternalAlphaPipelineService().run(week)
        assert result.success is True
        duped = [c for c in result.processed_items if c.duplicate_of is not None]
        assert len(duped) == 1
        report = json.loads(
            (week / "processed" / "duplicate_report.json").read_text(encoding="utf-8")
        )
        assert report["duplicate_count"] == 1

    def test_custom_output_dir(self, week_dir: Path, tmp_path: Path) -> None:
        out = tmp_path / "exports"
        result = InternalAlphaPipelineService().run(week_dir, output_dir=out)
        assert result.success is True
        assert (out / "classified_feedback.json").is_file()
        assert not (week_dir / "processed").exists()
