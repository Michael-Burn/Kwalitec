"""Unit tests for TemplateProvider (FOS-006)."""

from __future__ import annotations

import pytest

from app.founder.recommendations.config import (
    ALL_TEMPLATE_IDS,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.providers import (
    TemplateProvider,
    UnknownTemplateError,
)
from app.founder.recommendations.templates import RecommendationTemplate


class TestTemplateProvider:
    def test_default_catalog_covers_all_v1_templates(self) -> None:
        provider = TemplateProvider()
        assert provider.known_ids() == ALL_TEMPLATE_IDS
        for template_id in ALL_TEMPLATE_IDS:
            template = provider.get(template_id)
            assert template.template_id == template_id
            assert template.title
            assert template.explanation
            assert template.rationale

    def test_has_known_and_unknown(self) -> None:
        provider = TemplateProvider()
        assert provider.has(TEMPLATE_WAIT_FOR_INTERNAL_ALPHA) is True
        assert provider.has("does_not_exist") is False

    def test_unknown_template_raises(self) -> None:
        with pytest.raises(UnknownTemplateError) as exc:
            TemplateProvider().get("missing_template")
        assert exc.value.template_id == "missing_template"

    def test_custom_catalog(self) -> None:
        custom = RecommendationTemplate(
            template_id="custom",
            title="Custom",
            explanation="Explain",
            rationale="Why",
        )
        provider = TemplateProvider({"custom": custom})
        assert provider.get("custom") is custom
        assert provider.has(TEMPLATE_WAIT_FOR_INTERNAL_ALPHA) is False
