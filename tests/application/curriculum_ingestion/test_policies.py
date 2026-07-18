"""Policy unit tests for Curriculum Ingestion."""

from __future__ import annotations

import pytest

from app.application.curriculum_ingestion.policies.extraction_policy import (
    ExtractionPolicy,
)
from app.application.curriculum_ingestion.policies.normalization_policy import (
    NormalizationPolicy,
)
from app.application.curriculum_ingestion.policies.validation_policy import (
    ValidationPolicy,
)
from app.domain.curriculum_ingestion.curriculum_document import DocumentKind
from app.domain.curriculum_ingestion.normalization_result import (
    NormalizationResult,
    NormalizedObjective,
    NormalizedSection,
    NormalizedTopic,
)


@pytest.mark.parametrize("kind", list(DocumentKind))
def test_extraction_policy_entry_types_non_empty(kind):
    assert ExtractionPolicy.extractable_entry_types(kind)


@pytest.mark.parametrize(
    "kind,allows",
    [
        (DocumentKind.SYLLABUS, True),
        (DocumentKind.CMP, True),
        (DocumentKind.LEARNING_OBJECTIVES, False),
        (DocumentKind.FORMULA_SHEET, False),
    ],
)
def test_extraction_policy_allows_sections(kind, allows):
    assert ExtractionPolicy.allows_sections(kind) is allows


@pytest.mark.parametrize(
    "kind,allows",
    [
        (DocumentKind.LEARNING_OBJECTIVES, True),
        (DocumentKind.SYLLABUS, True),
        (DocumentKind.FORMULA_SHEET, False),
    ],
)
def test_extraction_policy_allows_objectives(kind, allows):
    assert ExtractionPolicy.allows_objectives(kind) is allows


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello World", "hello-world"),
        ("  A--B  ", "a-b"),
        ("!!!", "item"),
        ("Probability & Stats", "probability-stats"),
    ],
)
def test_normalization_slugify(text, expected):
    assert NormalizationPolicy.slugify(text) == expected


@pytest.mark.parametrize(
    "number,order,parent,expected",
    [
        ("1.2", 0, None, "1.2"),
        (None, 0, None, "1"),
        (None, 2, "3", "3.3"),
        ("  ", 1, None, "2"),
    ],
)
def test_normalization_canonical_number(number, order, parent, expected):
    assert (
        NormalizationPolicy.canonical_number(
            number, order_index=order, parent_number=parent
        )
        == expected
    )


@pytest.mark.parametrize(
    "numbers,ok",
    [
        (["1", "2", "3"], True),
        (["1.1", "1.2", "2.1"], True),
        (["2", "1"], False),
        (["1.2", "1.2"], False),
        (["a", "b"], True),  # non-numeric ignored
    ],
)
def test_normalization_numbers_consistent(numbers, ok):
    assert NormalizationPolicy.numbers_are_consistent(numbers) is ok


def _norm(
    *,
    topics: list[NormalizedTopic] | None = None,
    objectives: list[NormalizedObjective] | None = None,
    sections: list[NormalizedSection] | None = None,
    metadata: tuple[tuple[str, str], ...] = (("subject_code", "CS1"),),
    edges: tuple[tuple[str, str], ...] = (),
) -> NormalizationResult:
    sec = sections or [
        NormalizedSection.create("section-ch1", "Chapter 1", "1", 0)
    ]
    tops = topics or [
        NormalizedTopic.create(
            "topic-a", "Topic A", "section-ch1", "1.1", 0
        )
    ]
    objs = objectives
    if objs is None:
        objs = [
            NormalizedObjective.create(
                "objective-1", "Do A", "topic-a", "1", 0
            )
        ]
    return NormalizationResult.create(
        "n1",
        "e1",
        sections=sec,
        topics=tops,
        objectives=objs,
        prerequisite_edges=edges,
        metadata=metadata,
    )


def test_validation_policy_clean_passes():
    issues = ValidationPolicy.collect_issues(_norm())
    blocking = [i for i in issues if i.is_blocking]
    assert blocking == []


def test_validation_policy_duplicate_topic_title():
    topics = [
        NormalizedTopic.create("topic-a", "Same", "section-ch1", "1.1", 0),
        NormalizedTopic.create("topic-b", "Same", "section-ch1", "1.2", 1),
    ]
    objectives = [
        NormalizedObjective.create("o1", "x", "topic-a", "1", 0),
        NormalizedObjective.create("o2", "y", "topic-b", "1", 1),
    ]
    issues = ValidationPolicy.collect_issues(
        _norm(topics=topics, objectives=objectives)
    )
    assert any(i.code.value == "duplicate_topic" for i in issues)


def test_validation_policy_unknown_section():
    topics = [
        NormalizedTopic.create("topic-a", "A", "section-missing", "1.1", 0)
    ]
    issues = ValidationPolicy.collect_issues(
        _norm(topics=topics, objectives=[])
    )
    assert any(i.code.value == "unknown_section" for i in issues)


def test_validation_policy_malformed_self_parent():
    sections = [
        NormalizedSection.create(
            "section-ch1", "Ch", "1", 0, parent_section_id="section-ch1"
        )
    ]
    issues = ValidationPolicy.collect_issues(_norm(sections=sections))
    assert any(i.code.value == "malformed_hierarchy" for i in issues)


def test_validation_policy_missing_metadata():
    issues = ValidationPolicy.collect_issues(_norm(metadata=()))
    assert any(i.code.value == "missing_metadata" for i in issues)


def test_validation_policy_dangling_prerequisite():
    issues = ValidationPolicy.collect_issues(
        _norm(edges=(("topic-a", "topic-ghost"),))
    )
    assert any(i.code.value == "dangling_prerequisite" for i in issues)


def test_validation_policy_inconsistent_numbering():
    sections = [
        NormalizedSection.create("section-a", "A", "2", 0),
        NormalizedSection.create("section-b", "B", "1", 1),
    ]
    topics = [
        NormalizedTopic.create("topic-a", "A", "section-a", "1.1", 0),
    ]
    objectives = [
        NormalizedObjective.create("o1", "x", "topic-a", "1", 0),
    ]
    issues = ValidationPolicy.collect_issues(
        _norm(sections=sections, topics=topics, objectives=objectives)
    )
    assert any(i.code.value == "inconsistent_numbering" for i in issues)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("  a   b  ", "a b"),
        ("x", "x"),
        ("", ""),
    ],
)
def test_collapse_whitespace(text, expected):
    assert NormalizationPolicy.collapse_whitespace(text) == expected


@pytest.mark.parametrize("prefix", ["section", "topic", "objective"])
def test_canonical_id_with_prefix(prefix):
    cid = NormalizationPolicy.canonical_id("Hello", prefix=prefix, fallback_title="X")
    assert cid.startswith(f"{prefix}-")
