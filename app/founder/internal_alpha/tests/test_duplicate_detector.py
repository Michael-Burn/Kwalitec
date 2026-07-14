"""Unit tests for DuplicateDetector."""

from __future__ import annotations

from app.founder.internal_alpha.classifiers.duplicate_detector import (
    DuplicateDetector,
    normalise_feedback_text,
)
from app.founder.internal_alpha.config import InternalAlphaPipelineConfig
from app.founder.internal_alpha.tests.helpers import make_item


class TestNormaliseFeedbackText:
    def test_collapses_whitespace_and_case(self) -> None:
        assert normalise_feedback_text("  Hello   WORLD  ") == "hello world"

    def test_strips_punctuation(self) -> None:
        assert normalise_feedback_text("Hello, world!") == "hello world"


class TestDuplicateDetector:
    def test_identical(self) -> None:
        a = make_item(item_id="a", raw_text="Same text")
        b = make_item(item_id="b", raw_text="Same text")
        relations = DuplicateDetector().detect([a, b])
        assert len(relations) == 1
        assert relations[0].reason == "identical"
        assert relations[0].source_id == "b"
        assert relations[0].target_id == "a"
        assert relations[0].similarity == 1.0

    def test_normalised_identical(self) -> None:
        a = make_item(item_id="a", raw_text="Hello world")
        b = make_item(item_id="b", raw_text="  HELLO   WORLD!  ")
        relations = DuplicateDetector().detect([a, b])
        assert len(relations) == 1
        assert relations[0].reason == "normalised_identical"

    def test_similar_above_threshold(self) -> None:
        config = InternalAlphaPipelineConfig(similarity_threshold=0.8)
        a = make_item(
            item_id="a",
            raw_text="The mission page crashes when saving progress",
        )
        b = make_item(
            item_id="b",
            raw_text="The mission page crashes when saving the progress",
        )
        relations = DuplicateDetector(config).detect([a, b])
        assert len(relations) == 1
        assert relations[0].reason == "similar"
        assert relations[0].similarity >= 0.8

    def test_below_threshold_not_duplicate(self) -> None:
        config = InternalAlphaPipelineConfig(similarity_threshold=0.99)
        a = make_item(item_id="a", raw_text="Architecture needs clearer layering")
        b = make_item(item_id="b", raw_text="UX copy on settings is confusing")
        relations = DuplicateDetector(config).detect([a, b])
        assert relations == ()

    def test_does_not_remove_items(self) -> None:
        a = make_item(item_id="a", raw_text="dup")
        b = make_item(item_id="b", raw_text="dup")
        items = [a, b]
        DuplicateDetector().detect(items)
        assert len(items) == 2
