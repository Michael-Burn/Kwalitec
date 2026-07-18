"""Terminology translation and student-safety matrices."""

from __future__ import annotations

import pytest

from app.domain.student_experience.recommendation_explanation import (
    FORBIDDEN_INTERNAL_TERMS,
    TERMINOLOGY_MAP,
    assert_student_safe,
    build_explanation,
    is_student_safe,
    translate_to_student_language,
)

INTERNAL_SAMPLES = [
    "Student Digital Twin",
    "Digital Twin",
    "Adaptive Decision Engine",
    "Adaptive Decision",
    "Readiness Score",
    "Mission Engine",
    "Learning Orchestrator",
]

STUDENT_SAMPLES = [
    "Learning Insights",
    "Today's Recommendation",
    "Exam Readiness",
    "Today's Session",
    "Learning Activity",
]


@pytest.mark.parametrize("internal", INTERNAL_SAMPLES)
def test_translate_maps_internal_terms(internal):
    out = translate_to_student_language(f"See {internal} for details")
    assert is_student_safe(out)
    assert internal.lower() not in out.lower()


@pytest.mark.parametrize("term", list(TERMINOLOGY_MAP.keys()))
def test_terminology_map_keys_translate(term):
    out = translate_to_student_language(term)
    assert out == TERMINOLOGY_MAP[term]
    assert is_student_safe(out)


@pytest.mark.parametrize("term", FORBIDDEN_INTERNAL_TERMS)
def test_forbidden_terms_detected(term):
    assert is_student_safe(term) is False


@pytest.mark.parametrize("phrase", STUDENT_SAMPLES)
def test_student_phrases_are_safe(phrase):
    assert is_student_safe(phrase)


@pytest.mark.parametrize(
    "reason",
    [
        "low_retention",
        "declining_confidence",
        "exam_proximity",
        "prerequisite_gap",
        "high_roi",
        "overdue_revision",
        "mastery_incomplete",
        "unknown_code",
    ],
)
@pytest.mark.parametrize("topic", ["Equity", "Leases", "Ethics", "Tax"])
def test_build_explanation_reason_matrix(reason, topic):
    expl = build_explanation(
        topic_title=topic,
        reason_codes=(reason,),
        evidence_phrases=(f"Evidence for {topic}",),
        expected_benefit="Improve exam readiness",
        priority_band="high",
    )
    assert expl.is_complete
    assert topic in expl.summary or topic.lower() in expl.summary.lower()
    assert is_student_safe(expl.summary)
    assert is_student_safe(expl.why_recommended)
    for p in expl.evidence_points:
        assert is_student_safe(p)


@pytest.mark.parametrize(
    "text",
    [
        "Adaptive Decision Engine suggests review",
        "Digital Twin readiness score is rising",
        "Learning Orchestrator queued Mission Engine work",
        "Student Digital Twin snapshot ready",
    ],
)
def test_assert_student_safe_after_translate(text):
    translated = translate_to_student_language(text)
    safe = assert_student_safe(translated)
    assert is_student_safe(safe)


@pytest.mark.parametrize("i", range(20))
def test_empty_and_none_translation(i):
    assert translate_to_student_language(None) == ""
    assert translate_to_student_language("") == ""
    assert is_student_safe("")
