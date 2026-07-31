"""Unit tests for Baseline → Runtime C leaf-topic position seeding."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.educational_runtime_engine.baseline_position import (
    resolve_baseline_position_seed,
)


def _artefacts():
    return SimpleNamespace(
        sections=(
            {
                "number": "1",
                "title": "1 Data analysis",
                "topic_ids": ("t-1-1", "t-1-2", "t-junk"),
                "display_order": 1,
            },
            {
                "number": "2",
                "title": "2 Random variables and distributions",
                "topic_ids": ("t-2-1",),
                "display_order": 2,
            },
            {
                "number": "4",
                "title": "4 Regression theory and applications",
                "topic_ids": ("t-4-1", "t-4-2-glm"),
                "display_order": 4,
            },
        ),
        topics=(
            {
                "topic_id": "t-1-1",
                "code": "1.1",
                "title": "1.1 Describe the purpose and function of data analysis",
                "number": "1",
                "display_order": 1,
            },
            {
                "topic_id": "t-1-2",
                "code": "1.2",
                "title": "1.2 Complete exploratory data analysis",
                "number": "2",
                "display_order": 2,
            },
            {
                "topic_id": "t-junk",
                "code": "15",
                "title": "1 Jln Kilang Timor #06-01 · Singapore 159303",
                "number": "15",
                "display_order": 15,
            },
            {
                "topic_id": "t-2-1",
                "code": "2.1",
                "title": "2.1 Understand distributions",
                "number": "3",
                "display_order": 3,
            },
            {
                "topic_id": "t-4-1",
                "code": "4.1",
                "title": "4.1 Explain linear models",
                "number": "10",
                "display_order": 10,
            },
            {
                "topic_id": "t-4-2-glm",
                "code": "4.2",
                "title": "4.2 Generalised linear models",
                "number": "11",
                "display_order": 11,
            },
        ),
        progress_model=SimpleNamespace(
            topic_ids=(
                "t-1-1",
                "t-1-2",
                "t-junk",
                "t-2-1",
                "t-4-1",
                "t-4-2-glm",
            )
        ),
    )


def test_section_continue_marks_prior_section_topics_complete():
    seed = resolve_baseline_position_seed(
        _artefacts(),
        curriculum_topic_code="4",
        completed_curriculum_topics=["1", "2"],
    )
    assert seed.current_topic_id == "t-4-1"
    assert seed.completed_topic_ids == ("t-1-1", "t-1-2", "t-junk", "t-2-1")
    assert seed.continue_code == "4"


def test_leaf_continue_from_glm_title_match():
    seed = resolve_baseline_position_seed(
        _artefacts(),
        curriculum_topic_code="Generalised linear models",
    )
    assert seed.current_topic_id == "t-4-2-glm"
    assert "t-4-1" in seed.completed_topic_ids
    assert "t-1-1" in seed.completed_topic_ids
    assert "t-4-2-glm" not in seed.completed_topic_ids


def test_leaf_continue_from_hierarchical_code():
    seed = resolve_baseline_position_seed(
        _artefacts(),
        curriculum_topic_code="4.2",
    )
    assert seed.current_topic_id == "t-4-2-glm"
    assert seed.completed_topic_ids[-1] == "t-4-1"


def test_empty_continue_returns_no_seed():
    seed = resolve_baseline_position_seed(
        _artefacts(),
        curriculum_topic_code=None,
    )
    assert seed.completed_topic_ids == ()
    assert seed.current_topic_id is None
