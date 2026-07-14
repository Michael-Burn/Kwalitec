"""Unit tests for FounderWeeklyBriefValidator (FOS-007)."""

from __future__ import annotations

from dataclasses import replace

from app.founder.briefing.config import REPORT_VERSION
from app.founder.briefing.dto import ValidationIssue
from app.founder.briefing.models import BriefMetadata, BriefSection
from app.founder.briefing.tests.helpers import (
    make_attention_inputs,
    make_builder,
    make_recommendation_set,
)
from app.founder.briefing.validators import FounderWeeklyBriefValidator
from app.founder.recommendations.tests.helpers import make_healthy_state


class TestFounderWeeklyBriefValidator:
    def test_valid_brief_passes(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(
            state, recommendation_set, validate=False
        )
        report = FounderWeeklyBriefValidator().validate(
            brief, state=state, recommendation_set=recommendation_set
        )
        assert report.ok
        assert report.issues == ()

    def test_missing_section_content_fails(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set, validate=False)
        empty = BriefSection(title=brief.executive_summary.title, content="", order=1)
        broken = replace(brief, executive_summary=empty)
        report = FounderWeeklyBriefValidator().validate(broken, state=state)
        assert not report.ok
        assert any(issue.code == "empty_section_content" for issue in report.issues)

    def test_section_order_mismatch_fails(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set, validate=False)
        swapped = BriefSection(
            title=brief.engineering_summary.title,
            content=brief.engineering_summary.content,
            order=1,
        )
        broken = replace(brief, engineering_summary=swapped)
        report = FounderWeeklyBriefValidator().validate(broken)
        assert not report.ok
        codes = {issue.code for issue in report.issues}
        assert "duplicate_section_order" in codes or "section_order_mismatch" in codes

    def test_snapshot_version_mismatch_fails(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set, validate=False)
        broken = replace(
            brief,
            snapshot_version="9.9",
            metadata=BriefMetadata(
                generated_at=brief.generated_at,
                snapshot_version="9.9",
                report_version=REPORT_VERSION,
            ),
        )
        report = FounderWeeklyBriefValidator().validate(broken, state=state)
        assert not report.ok
        assert any(issue.code == "snapshot_version_mismatch" for issue in report.issues)

    def test_report_version_mismatch_fails(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set, validate=False)
        broken = replace(
            brief,
            metadata=BriefMetadata(
                generated_at=brief.generated_at,
                snapshot_version=brief.snapshot_version,
                report_version="0.0",
            ),
        )
        report = FounderWeeklyBriefValidator().validate(broken)
        assert not report.ok
        assert any(issue.code == "report_version_mismatch" for issue in report.issues)

    def test_missing_recommendation_reference_fails(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(
            state, recommendation_set, validate=False
        )
        scrubbed = BriefSection(
            title=brief.recommendations.title,
            content="Overall status: attention. Count: 1.\n- No details.",
            order=7,
        )
        broken = replace(brief, recommendations=scrubbed)
        report = FounderWeeklyBriefValidator().validate(
            broken, state=state, recommendation_set=recommendation_set
        )
        assert not report.ok
        assert any(
            issue.code == "missing_recommendation_reference" for issue in report.issues
        )

    def test_validation_issue_is_explicit(self) -> None:
        issue = ValidationIssue(
            code="missing_week",
            message="week must be a non-empty string",
            field="week",
        )
        assert issue.code == "missing_week"
        assert issue.field == "week"
