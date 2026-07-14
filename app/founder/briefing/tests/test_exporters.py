"""Unit tests for Founder Weekly Briefing exporters (FOS-007)."""

from __future__ import annotations

import json
from pathlib import Path

from app.founder.briefing.config import JSON_FILENAME, MARKDOWN_FILENAME
from app.founder.briefing.exporters import (
    JsonWeeklyBriefExporter,
    MarkdownWeeklyBriefExporter,
    WeeklyBriefExportBundle,
    brief_to_dict,
)
from app.founder.briefing.tests.helpers import make_attention_inputs, make_builder


class TestExporters:
    def test_markdown_render_structure(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        text = MarkdownWeeklyBriefExporter().render(brief)
        assert text.startswith("# Founder Weekly Briefing\n")
        assert "## Executive Summary" in text
        assert "## Engineering Overview" in text
        assert "## Internal Alpha" in text
        assert "## Capability Progress" in text
        assert "## Release Readiness" in text
        assert "## Top Priorities" in text
        assert "## Recommendations" in text
        assert "## Risks" in text
        assert "## Next Week Focus" in text
        assert "## Metadata" in text
        assert f"snapshot_version: {brief.snapshot_version}" in text

    def test_markdown_section_order(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        text = MarkdownWeeklyBriefExporter().render(brief)
        positions = [
            text.index(f"## {section.title}")
            for section in brief.ordered_sections()
        ]
        assert positions == sorted(positions)

    def test_json_render_round_trip_keys(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        payload = json.loads(JsonWeeklyBriefExporter().render(brief))
        assert payload["week"] == brief.week
        assert payload["snapshot_version"] == brief.snapshot_version
        assert len(payload["sections"]) == 9
        assert payload["metadata"]["report_version"] == brief.metadata.report_version
        assert brief_to_dict(brief)["recommendation_version"] == (
            brief.recommendation_version
        )

    def test_export_bundle_writes_files(self, tmp_path: Path) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        result = WeeklyBriefExportBundle().export_all(tmp_path, brief)
        assert Path(result.markdown_path).name == MARKDOWN_FILENAME
        assert Path(result.json_path).name == JSON_FILENAME
        assert Path(result.markdown_path).is_file()
        assert Path(result.json_path).is_file()
        assert "Founder Weekly Briefing" in Path(result.markdown_path).read_text(
            encoding="utf-8"
        )
