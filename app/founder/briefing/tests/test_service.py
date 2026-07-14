"""Unit tests for FounderWeeklyBriefingService (FOS-007)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.founder.briefing.dto import BriefingResult, BriefingValidationError
from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.briefing.tests.helpers import (
    BRIEFING_NOW,
    make_attention_inputs,
    make_recommendation_set,
    make_service,
)
from app.founder.briefing.validators import FounderWeeklyBriefValidator
from app.founder.recommendations.tests.helpers import make_healthy_state


class _FailingValidator(FounderWeeklyBriefValidator):
    def validate(self, brief, *, state=None, recommendation_set=None):  # type: ignore[override]
        from app.founder.briefing.dto.validation import (
            ValidationIssue,
            ValidationReport,
        )

        return ValidationReport(
            ok=False,
            issues=(
                ValidationIssue(
                    code="forced_failure",
                    message="injected failure",
                    field=None,
                ),
            ),
        )


class TestFounderWeeklyBriefingService:
    def test_generate_returns_result(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        result = make_service().generate(state, recommendation_set)
        assert isinstance(result, BriefingResult)
        assert isinstance(result.brief, FounderWeeklyBrief)
        assert result.exports is None
        assert result.brief.generated_at == BRIEFING_NOW

    def test_generate_brief_convenience(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_service().generate_brief(state, recommendation_set)
        assert brief.recommendations.content
        assert "wait_for_internal_alpha" in brief.recommendations.content

    def test_generate_with_export(self, tmp_path: Path) -> None:
        state, recommendation_set = make_attention_inputs()
        result = make_service().generate(
            state, recommendation_set, output_dir=tmp_path
        )
        assert result.exports is not None
        assert Path(result.exports.markdown_path).is_file()
        assert Path(result.exports.json_path).is_file()

    def test_validation_failure_raises(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        service = make_service(validator=_FailingValidator())
        with pytest.raises(BriefingValidationError) as exc:
            service.generate(state, recommendation_set)
        assert "forced_failure" in str(exc.value)

    def test_preserves_snapshot_version(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_service().generate_brief(state, recommendation_set)
        assert brief.snapshot_version == state.snapshot_version
        assert brief.metadata.snapshot_version == state.snapshot_version
