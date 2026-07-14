"""Exporters for Founder Weekly Briefing (FOS-007).

Exporters contain no business logic — they only render and write already
assembled FounderWeeklyBrief cargo.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.founder.briefing.config import JSON_FILENAME, MARKDOWN_FILENAME
from app.founder.briefing.dto import BriefingExportBundle
from app.founder.briefing.models import BriefSection, FounderWeeklyBrief


def _write_text(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def brief_to_dict(brief: FounderWeeklyBrief) -> dict[str, Any]:
    """Serialise a briefing to a plain JSON-ready mapping."""

    def section_dict(section: BriefSection) -> dict[str, Any]:
        return {
            "title": section.title,
            "content": section.content,
            "order": section.order,
        }

    return {
        "week": brief.week,
        "generated_at": brief.generated_at.isoformat(),
        "snapshot_version": brief.snapshot_version,
        "recommendation_version": brief.recommendation_version,
        "sections": [section_dict(section) for section in brief.ordered_sections()],
        "metadata": {
            "generated_at": brief.metadata.generated_at.isoformat(),
            "snapshot_version": brief.metadata.snapshot_version,
            "report_version": brief.metadata.report_version,
        },
    }


class MarkdownWeeklyBriefExporter:
    """Render / write FOUNDER_WEEKLY_REPORT.md."""

    def __init__(self, *, filename: str = MARKDOWN_FILENAME) -> None:
        self._filename = filename

    def render(self, brief: FounderWeeklyBrief) -> str:
        """Return markdown text for ``brief`` (no filesystem access)."""
        lines = [
            "# Founder Weekly Briefing",
            "",
            f"Week: {brief.week}",
            "",
        ]
        for section in brief.ordered_sections():
            lines.extend(
                [
                    f"## {section.title}",
                    "",
                    section.content,
                    "",
                ]
            )
        lines.extend(
            [
                "---",
                "",
                "## Metadata",
                "",
                f"- generated_at: {brief.metadata.generated_at.isoformat()}",
                f"- snapshot_version: {brief.metadata.snapshot_version}",
                f"- report_version: {brief.metadata.report_version}",
                f"- recommendation_version: {brief.recommendation_version}",
                "",
            ]
        )
        return "\n".join(lines)

    def export(self, output_dir: Path | str, brief: FounderWeeklyBrief) -> str:
        """Write markdown report under ``output_dir``; return path written."""
        content = self.render(brief)
        return _write_text(Path(output_dir) / self._filename, content)


class JsonWeeklyBriefExporter:
    """Render / write founder_weekly_report.json."""

    def __init__(self, *, filename: str = JSON_FILENAME) -> None:
        self._filename = filename

    def render(self, brief: FounderWeeklyBrief) -> str:
        """Return JSON text for ``brief`` (no filesystem access)."""
        return json.dumps(
            brief_to_dict(brief),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        ) + "\n"

    def export(self, output_dir: Path | str, brief: FounderWeeklyBrief) -> str:
        """Write JSON report under ``output_dir``; return path written."""
        content = self.render(brief)
        return _write_text(Path(output_dir) / self._filename, content)


class WeeklyBriefExportBundle:
    """Run Version 1 exporters for one FounderWeeklyBrief."""

    def __init__(
        self,
        *,
        markdown: MarkdownWeeklyBriefExporter | None = None,
        json_exporter: JsonWeeklyBriefExporter | None = None,
    ) -> None:
        self._markdown = markdown or MarkdownWeeklyBriefExporter()
        self._json = json_exporter or JsonWeeklyBriefExporter()

    def export_all(
        self, output_dir: Path | str, brief: FounderWeeklyBrief
    ) -> BriefingExportBundle:
        """Write markdown and JSON outputs; return paths written."""
        return BriefingExportBundle(
            markdown_path=self._markdown.export(output_dir, brief),
            json_path=self._json.export(output_dir, brief),
        )
