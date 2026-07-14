"""Export / service result DTOs for Founder Weekly Briefing (FOS-007)."""

from __future__ import annotations

from dataclasses import dataclass

from app.founder.briefing.models import FounderWeeklyBrief


@dataclass(frozen=True)
class BriefingExportBundle:
    """Paths written by exporters for one briefing run."""

    markdown_path: str
    json_path: str

    @property
    def paths(self) -> tuple[str, ...]:
        return (self.markdown_path, self.json_path)


@dataclass(frozen=True)
class BriefingResult:
    """Immutable service outcome: validated brief plus optional exports."""

    brief: FounderWeeklyBrief
    exports: BriefingExportBundle | None = None
