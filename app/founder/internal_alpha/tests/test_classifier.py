"""Unit tests for RuleBasedClassifier."""

from __future__ import annotations

from types import MappingProxyType

from app.founder.internal_alpha.classifiers import RuleBasedClassifier
from app.founder.internal_alpha.config import InternalAlphaPipelineConfig
from app.founder.internal_alpha.tests.helpers import make_item


class TestRuleBasedClassifier:
    def test_architecture_keyword(self) -> None:
        item = make_item(raw_text="Please clarify the architecture layering.")
        result = RuleBasedClassifier().classify(item)
        assert result.category == "Architecture"
        assert result.confidence > 0

    def test_bug_keyword(self) -> None:
        item = make_item(raw_text="There is a bug and a crash on login.")
        result = RuleBasedClassifier().classify(item)
        assert result.category == "Bug"
        assert result.confidence > 0

    def test_default_other(self) -> None:
        item = make_item(raw_text="Nice weather today for a walk.")
        result = RuleBasedClassifier().classify(item)
        assert result.category == "Other"
        assert result.confidence == 0.0

    def test_configurable_rules_without_pipeline_change(self) -> None:
        config = InternalAlphaPipelineConfig(
            categories=("Alpha", "Other"),
            keyword_rules=MappingProxyType({"Alpha": ("zebra",)}),
            default_category="Other",
        )
        item = make_item(raw_text="I saw a zebra in the feedback.")
        result = RuleBasedClassifier(config).classify(item)
        assert result.category == "Alpha"

    def test_classify_many_preserves_order(self) -> None:
        items = (
            make_item(item_id="1", raw_text="architecture note"),
            make_item(item_id="2", raw_text="random noise"),
        )
        results = RuleBasedClassifier().classify_many(items)
        assert [r.feedback_item.id for r in results] == ["1", "2"]
        assert results[0].category == "Architecture"
        assert results[1].category == "Other"

    def test_educational_match(self) -> None:
        item = make_item(raw_text="The curriculum mastery model is confusing.")
        result = RuleBasedClassifier().classify(item)
        assert result.category == "Educational"
