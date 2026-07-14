"""Filesystem exporters for Internal Alpha pipeline artefacts.

Exporters only write files. Content is rendered from already-computed domain
objects — no classification, aggregation, or recommendation logic.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from app.founder.internal_alpha.config import (
    CATEGORY_MARKDOWN_KEYS,
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.dto import (
    DuplicateRelation,
    classified_feedback_to_dict,
    duplicate_relations_to_dict,
    weekly_summary_to_dict,
)
from app.founder.internal_alpha.models import ClassifiedFeedback, WeeklySummary


def _write_text(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def _write_json(path: Path, payload: Any) -> str:
    return _write_text(
        path,
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    )


class ClassifiedFeedbackJsonExporter:
    """Write classified_feedback.json."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(
        self,
        output_dir: Path,
        classified: tuple[ClassifiedFeedback, ...] | list[ClassifiedFeedback],
    ) -> str:
        filename = self._config.output_filenames["classified_feedback"]
        payload = {
            "items": [classified_feedback_to_dict(item) for item in classified],
            "count": len(classified),
        }
        return _write_json(Path(output_dir) / filename, payload)


class FeedbackStatisticsJsonExporter:
    """Write feedback_statistics.json."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(self, output_dir: Path, summary: WeeklySummary) -> str:
        filename = self._config.output_filenames["feedback_statistics"]
        return _write_json(
            Path(output_dir) / filename,
            weekly_summary_to_dict(summary),
        )


class DuplicateReportJsonExporter:
    """Write duplicate_report.json."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(
        self,
        output_dir: Path,
        relations: tuple[DuplicateRelation, ...] | list[DuplicateRelation],
    ) -> str:
        filename = self._config.output_filenames["duplicate_report"]
        return _write_json(
            Path(output_dir) / filename,
            dict(duplicate_relations_to_dict(tuple(relations))),
        )


class WeekSummaryMarkdownExporter:
    """Write WEEK_SUMMARY.md."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(self, output_dir: Path, summary: WeeklySummary) -> str:
        filename = self._config.output_filenames["week_summary"]
        lines = [
            f"# Week Summary — {summary.week}",
            "",
            f"Generated at: {summary.generated_at.isoformat()}",
            "",
            "## Totals",
            "",
            f"- Total feedback: {summary.total_feedback}",
            f"- Duplicate relations: {summary.duplicate_count}",
            "",
            "## Category counts",
            "",
        ]
        for category, count in summary.category_counts.items():
            lines.append(f"- {category}: {count}")
        lines.extend(["", "## Contributor counts", ""])
        if summary.contributor_counts:
            for contributor, count in summary.contributor_counts.items():
                lines.append(f"- {contributor}: {count}")
        else:
            lines.append("- (none)")
        lines.append("")
        return _write_text(Path(output_dir) / filename, "\n".join(lines))


class CategoryMarkdownExporter:
    """Write per-category markdown files (architecture, engineering, …)."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(
        self,
        output_dir: Path,
        classified: tuple[ClassifiedFeedback, ...] | list[ClassifiedFeedback],
        category: str,
        output_key: str,
    ) -> str:
        filename = self._config.output_filenames[output_key]
        items = [c for c in classified if c.category == category]
        lines = [
            f"# {category}",
            "",
            f"Items: {len(items)}",
            "",
        ]
        if not items:
            lines.append("_No feedback classified in this category._")
            lines.append("")
        else:
            for item in items:
                fi = item.feedback_item
                lines.extend(
                    [
                        f"## {fi.filename}",
                        "",
                        f"- Contributor: {fi.contributor}",
                        f"- Confidence: {item.confidence}",
                        f"- Duplicate of: {item.duplicate_of or '—'}",
                        "",
                        fi.raw_text.strip(),
                        "",
                    ]
                )
        return _write_text(Path(output_dir) / filename, "\n".join(lines))

    def export_configured_categories(
        self,
        output_dir: Path,
        classified: tuple[ClassifiedFeedback, ...] | list[ClassifiedFeedback],
        category_keys: Mapping[str, str] | None = None,
    ) -> tuple[str, ...]:
        keys = category_keys if category_keys is not None else CATEGORY_MARKDOWN_KEYS
        written: list[str] = []
        for category, output_key in keys.items():
            written.append(
                self.export(output_dir, classified, category, output_key)
            )
        return tuple(written)


class ProposedActionsMarkdownExporter:
    """Write proposed_actions.md from Suggestion / Question classified items."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(
        self,
        output_dir: Path,
        classified: tuple[ClassifiedFeedback, ...] | list[ClassifiedFeedback],
    ) -> str:
        filename = self._config.output_filenames["proposed_actions"]
        action_categories = ("Suggestion", "Question", "Bug")
        lines = [
            "# Proposed Actions",
            "",
            "Derived from classified Suggestion, Question, and Bug feedback.",
            "",
        ]
        selected = [c for c in classified if c.category in action_categories]
        if not selected:
            lines.append("_No proposed actions this week._")
            lines.append("")
        else:
            for item in selected:
                fi = item.feedback_item
                lines.extend(
                    [
                        f"## [{item.category}] {fi.filename}",
                        "",
                        fi.raw_text.strip(),
                        "",
                    ]
                )
        return _write_text(Path(output_dir) / filename, "\n".join(lines))


class ReleaseReadinessMarkdownExporter:
    """Write release_readiness.md from summary statistics."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def export(self, output_dir: Path, summary: WeeklySummary) -> str:
        filename = self._config.output_filenames["release_readiness"]
        bugs = summary.category_counts.get("Bug", 0)
        performance = summary.category_counts.get("Performance", 0)
        lines = [
            "# Release Readiness",
            "",
            f"Week: {summary.week}",
            f"Generated at: {summary.generated_at.isoformat()}",
            "",
            "## Signals",
            "",
            f"- Total feedback: {summary.total_feedback}",
            f"- Bug class count: {bugs}",
            f"- Performance class count: {performance}",
            f"- Duplicate relations: {summary.duplicate_count}",
            "",
            "## Note",
            "",
            "Version 1 emits counts only. No founder recommendations.",
            "",
        ]
        return _write_text(Path(output_dir) / filename, "\n".join(lines))


class InternalAlphaExportBundle:
    """Run all Version 1 exporters against a processed output directory."""

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()
        self._classified = ClassifiedFeedbackJsonExporter(self._config)
        self._statistics = FeedbackStatisticsJsonExporter(self._config)
        self._duplicates = DuplicateReportJsonExporter(self._config)
        self._week_summary = WeekSummaryMarkdownExporter(self._config)
        self._categories = CategoryMarkdownExporter(self._config)
        self._actions = ProposedActionsMarkdownExporter(self._config)
        self._readiness = ReleaseReadinessMarkdownExporter(self._config)

    def export_all(
        self,
        output_dir: Path,
        classified: tuple[ClassifiedFeedback, ...],
        summary: WeeklySummary,
        duplicates: tuple[DuplicateRelation, ...],
    ) -> tuple[str, ...]:
        """Write every configured output file; return paths written."""

        written: list[str] = [
            self._classified.export(output_dir, classified),
            self._statistics.export(output_dir, summary),
            self._duplicates.export(output_dir, duplicates),
            self._week_summary.export(output_dir, summary),
        ]
        written.extend(
            self._categories.export_configured_categories(output_dir, classified)
        )
        written.append(self._actions.export(output_dir, classified))
        written.append(self._readiness.export(output_dir, summary))
        return tuple(written)
