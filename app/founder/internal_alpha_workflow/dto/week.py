"""WeekReference DTO for Internal Alpha Live Workflow (FSI-003)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WeekReference:
    """Immutable reference to one Internal Alpha week folder.

    Paths are absolute. Directory existence is not guaranteed; callers use
    WeekDiscoveryService / WorkflowOutputManager for validation and ensure.
    """

    label: str
    path: Path
    raw_feedback_dir: Path
    processed_dir: Path
    findings_dir: Path
    decisions_dir: Path
    weekly_review_dir: Path
    release_dir: Path
    archive_dir: Path

    @classmethod
    def from_path(cls, week_path: Path) -> WeekReference:
        """Build a WeekReference from a week directory path."""

        resolved = week_path.resolve()
        return cls(
            label=resolved.name,
            path=resolved,
            raw_feedback_dir=resolved / "raw_feedback",
            processed_dir=resolved / "processed",
            findings_dir=resolved / "findings",
            decisions_dir=resolved / "decisions",
            weekly_review_dir=resolved / "weekly_review",
            release_dir=resolved / "release",
            archive_dir=resolved / "archive",
        )
