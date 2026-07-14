"""Unit tests for FounderRecommendationService (FOS-006)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.founder.recommendations.config import (
    STATUS_ATTENTION,
    STATUS_HEALTHY,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.dto import RecommendationValidationError
from app.founder.recommendations.evaluators import RecommendationEngine
from app.founder.recommendations.models import RecommendationSet
from app.founder.recommendations.tests.helpers import (
    RECOMMENDATION_NOW,
    make_healthy_state,
    make_service,
    make_state,
)
from app.founder.recommendations.validators import RecommendationSetValidator


class _PassthroughValidator(RecommendationSetValidator):
    """Validator that always fails for service-raise coverage."""

    def validate(self, recommendation_set: RecommendationSet):  # type: ignore[override]
        from app.founder.recommendations.dto.validation import (
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


class TestFounderRecommendationService:
    def test_recommend_healthy_state(self) -> None:
        result = make_service().recommend(make_healthy_state())
        assert isinstance(result, RecommendationSet)
        assert result.recommendations == ()
        assert result.overall_status == STATUS_HEALTHY
        assert result.generated_at == RECOMMENDATION_NOW

    def test_recommend_fires_rule_and_returns_immutable_set(self) -> None:
        state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
        result = make_service().recommend(state)
        assert len(result.recommendations) == 1
        assert result.recommendations[0].id == TEMPLATE_WAIT_FOR_INTERNAL_ALPHA
        assert result.overall_status == STATUS_ATTENTION
        assert result.snapshot_version == state.snapshot_version
        with pytest.raises(Exception):
            result.recommendations[0].title = "mutated"  # type: ignore[misc]

    def test_validation_failure_raises(self) -> None:
        service = make_service(validator=_PassthroughValidator())
        with pytest.raises(RecommendationValidationError) as exc:
            service.recommend(make_healthy_state())
        assert "forced_failure" in str(exc.value)

    def test_preserves_snapshot_version_from_state(self) -> None:
        state = replace(make_healthy_state(), snapshot_version="1.0")
        result = make_service().recommend(state)
        assert result.snapshot_version == "1.0"

    def test_uses_injected_engine(self) -> None:
        engine = RecommendationEngine(rules=(), clock=lambda: RECOMMENDATION_NOW)
        result = make_service(engine=engine).recommend(make_healthy_state())
        assert result.recommendations == ()
