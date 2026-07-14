"""Feedback discovery and reading (no classification or aggregation)."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.models import FeedbackItem
from app.founder.internal_alpha.validators import FeedbackFileValidator


class FeedbackProcessor:
    """Discover ``.txt`` files, read contents, create FeedbackItem objects.

    Single responsibility: ingest only. No classification. No aggregation.
    """

    def __init__(
        self,
        config: InternalAlphaPipelineConfig | None = None,
        file_validator: FeedbackFileValidator | None = None,
    ) -> None:
        self._config = config or default_config()
        self._file_validator = file_validator or FeedbackFileValidator()

    def process(
        self,
        week_dir: Path,
        *,
        week: str | None = None,
    ) -> tuple[tuple[FeedbackItem, ...], tuple[str, ...]]:
        """Discover and read feedback files under ``week_dir/raw_feedback``.

        Args:
            week_dir: Week folder containing raw_feedback/.
            week: Optional week label; defaults to the week directory name.

        Returns:
            ``(items, warnings)`` where warnings cover skipped invalid files.
        """
        week_path = Path(week_dir)
        week_label = week if week is not None else week_path.name
        raw_dir = week_path / self._config.raw_feedback_dirname

        paths = sorted(
            p
            for p in raw_dir.iterdir()
            if p.is_file() and p.suffix.lower() == self._config.feedback_extension
        )

        items: list[FeedbackItem] = []
        warnings: list[str] = []

        for path in paths:
            text, issue = self._file_validator.validate_and_read(path)
            if issue is not None:
                warnings.append(f"{issue.code}: {issue.message}")
                continue
            assert text is not None
            items.append(self._to_item(path, text, week_label))

        return tuple(items), tuple(warnings)

    def _to_item(self, path: Path, text: str, week: str) -> FeedbackItem:
        contributor = path.stem
        item_id = self._stable_id(week, path.name, text)
        created_at = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        return FeedbackItem(
            id=item_id,
            filename=path.name,
            contributor=contributor,
            week=week,
            raw_text=text,
            created_at=created_at,
        )

    @staticmethod
    def _stable_id(week: str, filename: str, text: str) -> str:
        digest = hashlib.sha256(
            f"{week}\0{filename}\0{text}".encode()
        ).hexdigest()
        return digest[:16]
