"""Unit tests for FeedbackFolderValidator and FeedbackFileValidator."""

from __future__ import annotations

from pathlib import Path

from app.founder.internal_alpha.validators import (
    FeedbackFileValidator,
    FeedbackFolderValidator,
)


class TestFeedbackFolderValidator:
    def test_valid_week(self, week_dir: Path) -> None:
        report = FeedbackFolderValidator().validate(week_dir)
        assert report.ok is True
        assert report.issues == ()

    def test_missing_week(self, tmp_path: Path) -> None:
        report = FeedbackFolderValidator().validate(tmp_path / "missing")
        assert report.ok is False
        assert report.issues[0].code == "week_missing"

    def test_missing_raw_feedback(self, tmp_path: Path) -> None:
        week = tmp_path / "week"
        week.mkdir()
        report = FeedbackFolderValidator().validate(week)
        assert report.ok is False
        assert report.issues[0].code == "raw_feedback_missing"

    def test_no_txt_files(self, tmp_path: Path) -> None:
        week = tmp_path / "week"
        (week / "raw_feedback").mkdir(parents=True)
        (week / "raw_feedback" / "notes.md").write_text("x", encoding="utf-8")
        report = FeedbackFolderValidator().validate(week)
        assert report.ok is False
        assert report.issues[0].code == "no_txt_files"

    def test_week_path_is_file(self, tmp_path: Path) -> None:
        target = tmp_path / "not_a_dir"
        target.write_text("x", encoding="utf-8")
        report = FeedbackFolderValidator().validate(target)
        assert report.ok is False
        assert report.issues[0].code == "week_not_directory"


class TestFeedbackFileValidator:
    def test_reads_utf8(self, tmp_path: Path) -> None:
        path = tmp_path / "a.txt"
        path.write_text("feedback about curriculum", encoding="utf-8")
        text, issue = FeedbackFileValidator().validate_and_read(path)
        assert issue is None
        assert text == "feedback about curriculum"

    def test_rejects_empty(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.txt"
        path.write_text("   \n", encoding="utf-8")
        text, issue = FeedbackFileValidator().validate_and_read(path)
        assert text is None
        assert issue is not None
        assert issue.code == "empty_file"

    def test_latin1_fallback(self, tmp_path: Path) -> None:
        path = tmp_path / "latin.txt"
        path.write_bytes(b"caf\xe9 feedback")
        text, issue = FeedbackFileValidator().validate_and_read(path)
        assert issue is None
        assert text is not None
        assert "caf" in text

    def test_missing_file(self, tmp_path: Path) -> None:
        text, issue = FeedbackFileValidator().validate_and_read(
            tmp_path / "gone.txt"
        )
        assert text is None
        assert issue is not None
        assert issue.code == "file_missing"

    def test_normalise_encoding_utf8(self) -> None:
        assert FeedbackFileValidator.normalise_encoding(b"hello") == "hello"
