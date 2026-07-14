"""Unit tests for briefing report section ordering (FOS-007)."""

from __future__ import annotations

from app.founder.briefing.config import REQUIRED_SECTION_TITLES, SECTION_SPECS
from app.founder.briefing.exporters import MarkdownWeeklyBriefExporter
from app.founder.briefing.tests.helpers import make_attention_inputs, make_builder


class TestReportOrdering:
    def test_section_specs_define_nine_sections(self) -> None:
        assert len(SECTION_SPECS) == 9
        assert [order for order, _ in SECTION_SPECS] == list(range(1, 10))

    def test_ordered_sections_match_required_titles(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        assert (
            tuple(section.title for section in brief.ordered_sections())
            == REQUIRED_SECTION_TITLES
        )

    def test_markdown_document_order(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        text = MarkdownWeeklyBriefExporter().render(brief)
        expected_headings = [f"## {title}" for title in REQUIRED_SECTION_TITLES]
        indices = [text.index(heading) for heading in expected_headings]
        assert indices == sorted(indices)
        assert text.index("## Metadata") > indices[-1]
