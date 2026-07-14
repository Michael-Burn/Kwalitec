"""WeekDiscoveryService — locate and validate Internal Alpha week folders."""

from __future__ import annotations

import re
from pathlib import Path

from app.founder.internal_alpha_workflow.config import (
    DEFAULT_INTERNAL_ALPHA_RELATIVE,
    InternalAlphaWorkflowConfig,
    default_config,
)
from app.founder.internal_alpha_workflow.dto import (
    WeekReference,
    WorkflowError,
    WorkflowValidationIssue,
    WorkflowValidationReport,
)


def _default_repo_root() -> Path:
    """Resolve repository root from this package location."""

    # app/founder/internal_alpha_workflow/discovery/week_discovery.py → repo
    return Path(__file__).resolve().parents[4]


class WeekDiscoveryService:
    """Locate available week folders and return immutable WeekReference DTOs.

    Responsibilities:
    - Locate available week folders
    - Determine latest week
    - Validate required structure
    - Return immutable WeekReference

    Does not process feedback or mutate repository contents.
    """

    def __init__(
        self,
        *,
        root: Path | str | None = None,
        repo_root: Path | str | None = None,
        config: InternalAlphaWorkflowConfig | None = None,
    ) -> None:
        self._config = config or default_config()
        self._week_re = re.compile(self._config.week_dir_pattern)
        if root is not None:
            self._root = Path(root).resolve()
        else:
            if repo_root is not None:
                base = Path(repo_root).resolve()
            else:
                base = _default_repo_root()
            self._root = (base.joinpath(*DEFAULT_INTERNAL_ALPHA_RELATIVE)).resolve()

    @property
    def root(self) -> Path:
        """Absolute path to the Internal Alpha research root."""

        return self._root

    def list_weeks(self) -> tuple[WeekReference, ...]:
        """Return week folders under the root, ordered by week number ascending."""

        if not self._root.is_dir():
            return ()

        weeks: list[tuple[int, WeekReference]] = []
        for child in self._root.iterdir():
            if not child.is_dir():
                continue
            if child.name == self._config.week_template_dirname:
                continue
            match = self._week_re.match(child.name)
            if match is None:
                continue
            weeks.append((int(match.group(1)), WeekReference.from_path(child)))

        weeks.sort(key=lambda item: item[0])
        return tuple(ref for _, ref in weeks)

    def latest_week(self) -> WeekReference | None:
        """Return the highest-numbered week, or None when none exist."""

        weeks = self.list_weeks()
        return weeks[-1] if weeks else None

    def get_week(self, label: str) -> WeekReference:
        """Resolve one week by directory label.

        Raises:
            WorkflowError: When the week directory does not exist.
        """

        week_path = self._root / label
        if not week_path.is_dir():
            raise WorkflowError(
                f"Week folder does not exist: {label}",
                code="week_missing",
            )
        match = self._week_re.match(label)
        if match is None:
            raise WorkflowError(
                f"Week folder name is invalid: {label}",
                code="week_invalid_name",
            )
        return WeekReference.from_path(week_path)

    def resolve_week(self, week: str | None = None) -> WeekReference:
        """Resolve an explicit week label or the latest available week.

        Raises:
            WorkflowError: When the requested week is missing or no weeks exist.
        """

        if week is not None:
            return self.get_week(week)
        latest = self.latest_week()
        if latest is None:
            raise WorkflowError(
                f"No week folders found under {self._root}",
                code="no_weeks",
            )
        return latest

    def validate_structure(self, week: WeekReference) -> WorkflowValidationReport:
        """Validate that required week directories exist."""

        issues: list[WorkflowValidationIssue] = []
        if not week.path.is_dir():
            issues.append(
                WorkflowValidationIssue(
                    code="week_missing",
                    message=f"Week path is not a directory: {week.path}",
                    path=str(week.path),
                )
            )
            return WorkflowValidationReport(ok=False, issues=tuple(issues))

        for dirname in self._config.required_week_dirnames:
            child = week.path / dirname
            if not child.is_dir():
                issues.append(
                    WorkflowValidationIssue(
                        code="folder_missing",
                        message=f"Required folder missing: {dirname}",
                        path=str(child),
                    )
                )

        return WorkflowValidationReport(ok=not issues, issues=tuple(issues))

    def validate_raw_feedback(self, week: WeekReference) -> WorkflowValidationReport:
        """Validate that raw_feedback/ exists and contains at least one .txt file."""

        issues: list[WorkflowValidationIssue] = []
        raw = week.raw_feedback_dir
        if not raw.is_dir():
            issues.append(
                WorkflowValidationIssue(
                    code="raw_feedback_missing",
                    message="raw_feedback/ directory is missing",
                    path=str(raw),
                )
            )
            return WorkflowValidationReport(ok=False, issues=tuple(issues))

        txt_files = sorted(
            p for p in raw.iterdir() if p.is_file() and p.suffix == ".txt"
        )
        if not txt_files:
            issues.append(
                WorkflowValidationIssue(
                    code="raw_feedback_empty",
                    message="raw_feedback/ contains no .txt files",
                    path=str(raw),
                )
            )
        return WorkflowValidationReport(ok=not issues, issues=tuple(issues))
