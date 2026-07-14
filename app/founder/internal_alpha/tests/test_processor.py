"""Unit tests for FeedbackProcessor."""

from __future__ import annotations

from pathlib import Path

from app.founder.internal_alpha.processors import FeedbackProcessor


class TestFeedbackProcessor:
    def test_discovers_and_reads_multiple_files(self, week_dir: Path) -> None:
        items, warnings = FeedbackProcessor().process(week_dir)
        assert warnings == ()
        assert len(items) == 2
        names = {i.filename for i in items}
        assert names == {"alice.txt", "bob.txt"}
        contributors = {i.contributor for i in items}
        assert contributors == {"alice", "bob"}
        assert all(i.week == "2026-W28" for i in items)
        assert all(i.raw_text.strip() for i in items)
        assert all(i.id for i in items)

    def test_stable_ids_are_deterministic(self, week_dir: Path) -> None:
        first, _ = FeedbackProcessor().process(week_dir)
        second, _ = FeedbackProcessor().process(week_dir)
        assert [i.id for i in first] == [i.id for i in second]

    def test_skips_empty_with_warning(self, tmp_path: Path) -> None:
        week = tmp_path / "week"
        raw = week / "raw_feedback"
        raw.mkdir(parents=True)
        (raw / "ok.txt").write_text("architecture concern", encoding="utf-8")
        (raw / "blank.txt").write_text("\n", encoding="utf-8")
        items, warnings = FeedbackProcessor().process(week)
        assert len(items) == 1
        assert items[0].filename == "ok.txt"
        assert any("empty_file" in w for w in warnings)

    def test_custom_week_label(self, week_dir: Path) -> None:
        items, _ = FeedbackProcessor().process(week_dir, week="custom-week")
        assert all(i.week == "custom-week" for i in items)
