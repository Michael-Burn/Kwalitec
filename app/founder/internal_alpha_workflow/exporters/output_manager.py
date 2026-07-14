"""Workflow output management — distribute artefacts into week folders (FSI-003).

Coordinator writers only. Never overwrite unrelated files. Only managed
filenames from config may be created or replaced.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from app.founder.briefing.exporters import (
    MarkdownWeeklyBriefExporter,
    WeeklyBriefExportBundle,
)
from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.internal_alpha_workflow.config import (
    ARCHIVE_DIRNAME,
    DECISIONS_DIRNAME,
    FINDINGS_DIRNAME,
    RELEASE_DIRNAME,
    WEEKLY_REVIEW_DIRNAME,
    InternalAlphaWorkflowConfig,
    default_config,
)
from app.founder.internal_alpha_workflow.dto import WeekReference
from app.founder.recommendations.models import RecommendationSet


def recommendation_set_to_dict(recommendation_set: RecommendationSet) -> dict[str, Any]:
    """Serialise a RecommendationSet for JSON export (no engine changes)."""

    return {
        "snapshot_version": recommendation_set.snapshot_version,
        "generated_at": recommendation_set.generated_at.isoformat(),
        "overall_status": recommendation_set.overall_status,
        "recommendations": [
            {
                "id": item.id,
                "category": item.category,
                "priority": item.priority,
                "title": item.title,
                "explanation": item.explanation,
                "rationale": item.rationale,
                "evidence": [
                    {
                        "source": evidence.source,
                        "metric": evidence.metric,
                        "value": evidence.value,
                    }
                    for evidence in item.evidence
                ],
                "created_at": item.created_at.isoformat(),
            }
            for item in recommendation_set.recommendations
        ],
    }


def recommendation_set_to_markdown(recommendation_set: RecommendationSet) -> str:
    """Render a RecommendationSet as markdown (advisory export only)."""

    lines = [
        "# Founder Recommendations",
        "",
        f"Generated at: {recommendation_set.generated_at.isoformat()}",
        f"Snapshot version: {recommendation_set.snapshot_version}",
        f"Overall status: {recommendation_set.overall_status}",
        "",
    ]
    if not recommendation_set.recommendations:
        lines.extend(["No recommendations generated.", ""])
        return "\n".join(lines)

    for item in recommendation_set.recommendations:
        lines.extend(
            [
                f"## [{item.priority}] {item.title}",
                "",
                f"- id: {item.id}",
                f"- category: {item.category}",
                "",
                item.explanation,
                "",
                f"**Rationale:** {item.rationale}",
                "",
            ]
        )
        if item.evidence:
            lines.append("**Evidence:**")
            lines.append("")
            for evidence in item.evidence:
                lines.append(
                    f"- {evidence.source}.{evidence.metric} = {evidence.value}"
                )
            lines.append("")
    return "\n".join(lines)


class WorkflowOutputManager:
    """Ensure week output directories and write managed workflow exports."""

    def __init__(
        self,
        config: InternalAlphaWorkflowConfig | None = None,
        *,
        briefing_exporters: WeeklyBriefExportBundle | None = None,
        markdown_brief_exporter: MarkdownWeeklyBriefExporter | None = None,
    ) -> None:
        self._config = config or default_config()
        self._briefing_exporters = briefing_exporters or WeeklyBriefExportBundle()
        self._markdown_brief = markdown_brief_exporter or MarkdownWeeklyBriefExporter()

    def ensure_directories(self, week: WeekReference) -> None:
        """Create missing output directories. Never deletes existing content."""

        for dirname in self._config.output_dirnames:
            (week.path / dirname).mkdir(parents=True, exist_ok=True)

    def export_all(
        self,
        week: WeekReference,
        *,
        recommendation_set: RecommendationSet,
        brief: FounderWeeklyBrief,
        started_at: datetime,
        completed_at: datetime,
    ) -> tuple[str, ...]:
        """Write all post-pipeline managed outputs. All-or-nothing for this stage.

        Pipeline ``processed/`` artefacts are assumed already present. This method
        distributes managed copies and generated advisory/brief files into
        findings/, decisions/, weekly_review/, release/, and archive/.

        Only config-managed filenames are written. Unrelated files are untouched.

        Raises:
            FileNotFoundError: When a required processed source file is missing
                before distribution begins (no partial new exports).
            OSError: On filesystem write failure after preparation.
        """

        self.ensure_directories(week)
        self._assert_processed_sources(week)

        written: list[str] = []
        written.extend(self._copy_findings(week))
        written.extend(self._write_decisions(week, recommendation_set))
        written.extend(self._write_weekly_review(week, brief))
        written.extend(self._copy_release(week))
        written.extend(
            self._write_archive(
                week,
                recommendation_set=recommendation_set,
                brief=brief,
                started_at=started_at,
                completed_at=completed_at,
            )
        )
        return tuple(written)

    def _assert_processed_sources(self, week: WeekReference) -> None:
        required = (
            *self._config.findings_from_processed,
            *self._config.release_from_processed,
            *self._config.decisions_from_processed,
        )
        missing = [
            name
            for name in required
            if not (week.processed_dir / name).is_file()
        ]
        if missing:
            raise FileNotFoundError(
                "Processed sources missing before export: " + ", ".join(missing)
            )

    def _copy_managed(
        self,
        *,
        source_dir: Path,
        target_dir: Path,
        filenames: tuple[str, ...],
    ) -> list[str]:
        written: list[str] = []
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in filenames:
            source = source_dir / name
            if not source.is_file():
                continue
            destination = target_dir / name
            shutil.copy2(source, destination)
            written.append(str(destination))
        return written

    def _copy_findings(self, week: WeekReference) -> list[str]:
        return self._copy_managed(
            source_dir=week.processed_dir,
            target_dir=week.findings_dir,
            filenames=self._config.findings_from_processed,
        )

    def _copy_release(self, week: WeekReference) -> list[str]:
        return self._copy_managed(
            source_dir=week.processed_dir,
            target_dir=week.release_dir,
            filenames=self._config.release_from_processed,
        )

    def _write_decisions(
        self, week: WeekReference, recommendation_set: RecommendationSet
    ) -> list[str]:
        written = self._copy_managed(
            source_dir=week.processed_dir,
            target_dir=week.decisions_dir,
            filenames=self._config.decisions_from_processed,
        )
        week.decisions_dir.mkdir(parents=True, exist_ok=True)

        json_path = week.decisions_dir / self._config.recommendations_json
        json_path.write_text(
            json.dumps(
                recommendation_set_to_dict(recommendation_set),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        written.append(str(json_path))

        md_path = week.decisions_dir / self._config.recommendations_md
        md_path.write_text(
            recommendation_set_to_markdown(recommendation_set),
            encoding="utf-8",
        )
        written.append(str(md_path))
        return written

    def _write_weekly_review(
        self, week: WeekReference, brief: FounderWeeklyBrief
    ) -> list[str]:
        week.weekly_review_dir.mkdir(parents=True, exist_ok=True)
        bundle = self._briefing_exporters.export_all(week.weekly_review_dir, brief)
        return [bundle.markdown_path, bundle.json_path]

    def _write_archive(
        self,
        week: WeekReference,
        *,
        recommendation_set: RecommendationSet,
        brief: FounderWeeklyBrief,
        started_at: datetime,
        completed_at: datetime,
    ) -> list[str]:
        week.archive_dir.mkdir(parents=True, exist_ok=True)
        written: list[str] = []

        summary_src = week.processed_dir / "WEEK_SUMMARY.md"
        if summary_src.is_file():
            destination = week.archive_dir / "WEEK_SUMMARY.md"
            shutil.copy2(summary_src, destination)
            written.append(str(destination))

        rec_path = week.archive_dir / "recommendations.json"
        rec_path.write_text(
            json.dumps(
                recommendation_set_to_dict(recommendation_set),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        written.append(str(rec_path))

        brief_path = week.archive_dir / "FOUNDER_WEEKLY_REPORT.md"
        brief_path.write_text(
            self._markdown_brief.render(brief),
            encoding="utf-8",
        )
        written.append(str(brief_path))

        manifest = {
            "week": week.label,
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "folders": [
                FINDINGS_DIRNAME,
                DECISIONS_DIRNAME,
                WEEKLY_REVIEW_DIRNAME,
                RELEASE_DIRNAME,
                ARCHIVE_DIRNAME,
            ],
        }
        manifest_path = week.archive_dir / self._config.archive_manifest
        manifesto = (
            json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        )
        manifest_path.write_text(manifesto, encoding="utf-8")
        written.append(str(manifest_path))
        return written
