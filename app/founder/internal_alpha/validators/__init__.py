"""Validators for Internal Alpha week folders and feedback files."""

from __future__ import annotations

from pathlib import Path

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.dto import ValidationIssue, ValidationReport


class FeedbackFolderValidator:
    """Verify week folder layout before processing.

    Checks:
    - week folder exists
    - raw_feedback directory exists
    - at least one feedback text file exists
    """

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def validate(self, week_dir: Path) -> ValidationReport:
        """Validate ``week_dir`` structure.

        Args:
            week_dir: Path to a week folder (contains raw_feedback/).

        Returns:
            ValidationReport with ok=False when hard errors are present.
        """
        issues: list[ValidationIssue] = []
        week_path = Path(week_dir)

        if not week_path.exists():
            issues.append(
                ValidationIssue(
                    code="week_missing",
                    message=f"Week folder does not exist: {week_path}",
                    path=str(week_path),
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        if not week_path.is_dir():
            issues.append(
                ValidationIssue(
                    code="week_not_directory",
                    message=f"Week path is not a directory: {week_path}",
                    path=str(week_path),
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        raw_dir = week_path / self._config.raw_feedback_dirname
        if not raw_dir.exists():
            issues.append(
                ValidationIssue(
                    code="raw_feedback_missing",
                    message=(
                        f"raw_feedback directory missing: expected "
                        f"{self._config.raw_feedback_dirname!r} under {week_path}"
                    ),
                    path=str(raw_dir),
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        if not raw_dir.is_dir():
            issues.append(
                ValidationIssue(
                    code="raw_feedback_not_directory",
                    message=f"raw_feedback path is not a directory: {raw_dir}",
                    path=str(raw_dir),
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        txt_files = sorted(
            p
            for p in raw_dir.iterdir()
            if p.is_file() and p.suffix.lower() == self._config.feedback_extension
        )
        if not txt_files:
            issues.append(
                ValidationIssue(
                    code="no_txt_files",
                    message=(
                        f"No {self._config.feedback_extension} files found in {raw_dir}"
                    ),
                    path=str(raw_dir),
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        return ValidationReport(ok=True, issues=tuple(issues))


class FeedbackFileValidator:
    """Validate individual feedback files: readable, non-empty, normalised encoding."""

    def validate_and_read(
        self, path: Path
    ) -> tuple[str | None, ValidationIssue | None]:
        """Read and normalise file text.

        Args:
            path: Path to a feedback ``.txt`` file.

        Returns:
            ``(text, None)`` on success, or ``(None, issue)`` on failure.
            Encoding is normalised to Unicode via UTF-8 with Latin-1 fallback.
        """
        file_path = Path(path)
        if not file_path.exists():
            return None, ValidationIssue(
                code="file_missing",
                message=f"Feedback file does not exist: {file_path}",
                path=str(file_path),
            )
        if not file_path.is_file():
            return None, ValidationIssue(
                code="not_a_file",
                message=f"Path is not a file: {file_path}",
                path=str(file_path),
            )

        try:
            raw_bytes = file_path.read_bytes()
        except OSError as exc:
            return None, ValidationIssue(
                code="unreadable",
                message=f"Cannot read feedback file: {file_path} ({exc})",
                path=str(file_path),
            )

        text = self.normalise_encoding(raw_bytes)
        if text.strip() == "":
            return None, ValidationIssue(
                code="empty_file",
                message=f"Feedback file is empty: {file_path}",
                path=str(file_path),
            )

        return text, None

    @staticmethod
    def normalise_encoding(raw_bytes: bytes) -> str:
        """Decode bytes as UTF-8, falling back to Latin-1 (never raises)."""

        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return raw_bytes.decode("latin-1")
