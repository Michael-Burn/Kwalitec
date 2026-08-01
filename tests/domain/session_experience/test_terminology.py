"""Terminology and safety for Learning Session Experience domain."""

from __future__ import annotations

import pytest

from app.domain.session_experience.activity_projection import (
    FORBIDDEN_ACTIVITY_TERMS,
    is_student_safe_copy,
)
from app.domain.session_experience.reflection_projection import (
    FORBIDDEN_REFLECTION_TERMS,
    is_reflection_safe,
)
from tests.domain.session_experience.helpers import make_activity, make_reflection


@pytest.mark.parametrize("term", FORBIDDEN_ACTIVITY_TERMS)
def test_forbidden_activity_terms_detected(term):
    assert not is_student_safe_copy(f"Please consult the {term} now")


@pytest.mark.parametrize("term", FORBIDDEN_REFLECTION_TERMS)
def test_forbidden_reflection_terms_detected(term):
    assert not is_reflection_safe(f"Your {term} is high")


@pytest.mark.parametrize(
    "text",
    [
        "Ownership influence drives equity accounting",
        "Practice consolidations with care",
        "Review leases before the exam",
    ],
)
def test_safe_educational_copy(text):
    assert is_student_safe_copy(text)
    assert is_reflection_safe(text)


@pytest.mark.parametrize(
    "text",
    [
        "You worked through reading on Complete exploratory data analysis",
        "Growing comfort with Explain the aims of data analysis",
        "Growing comfort with Explain how a GLM joins an exponential-family",
        "Retrieve the purpose-to-EDA exploratory judgement chain",
    ],
)
def test_reflection_safe_despite_xp_substring(text):
    """PB-002 F6: substance copy must not trip on 'xp' inside educational words."""
    assert is_reflection_safe(text)
    make_reflection(key_insight=text, concept_confidence=text)


@pytest.mark.parametrize(
    "text",
    [
        "Your xp is climbing",
        "Great score today",
        "Badge unlocked for tonight",
    ],
)
def test_reflection_rejects_standalone_gamification_tokens(text):
    assert not is_reflection_safe(text)


def test_activity_accepts_safe_question():
    activity = make_activity(question="Explain the equity method briefly.")
    assert "equity" in activity.question.lower()


def test_reflection_rejects_each_forbidden_insight():
    for term in ("score", "points", "badge", "streak"):
        with pytest.raises(ValueError):
            make_reflection(key_insight=f"Great {term} today")
