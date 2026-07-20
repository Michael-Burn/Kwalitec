"""Educational Atomicity tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode import (
    AtomicityPolicy,
    EpisodeIsAtomicSpecification,
)
from tests.domain.education.learning_episode.conftest import make_episode, make_goal

ATOMIC_EXAMPLES = [
    "Teach exponential-family intuition",
    "Repair one misconception about select vs ultimate",
    "Guided practice on term-assurance EPV under constant force",
    "Retrieval of commutation-function selection rules",
    "Transfer practice on deferred annuities from whole-life drills",
    "Strengthen independent application of net premium equivalence",
    "Calibrate confidence on deferred annuity stems",
    "Connect force of mortality to survival probability",
]

NON_ATOMIC_EXAMPLES = [
    "Teach all GLMs",
    "Revise an entire chapter",
    "Learn mortality",  # vague but "Learn mortality" might pass - check patterns
    "Do Chapter 4",
    "Practice everything I got wrong this month",
    "Capstone the whole subject in one sitting",
    "Finish the chapter",
    "Revise the whole syllabus",
    "Cover all topics before the exam",
    "Introduce X and also revise Y as well as exam practice Z",
]


class TestAtomicExamples:
    @pytest.mark.parametrize("statement", ATOMIC_EXAMPLES)
    def test_atomic_accepted(self, statement: str) -> None:
        assert AtomicityPolicy.is_atomic_statement(statement)
        episode = make_episode(
            goal=make_goal(statement=statement, purpose=statement)
        )
        assert EpisodeIsAtomicSpecification().is_satisfied_by(episode)


class TestNonAtomicExamples:
    @pytest.mark.parametrize(
        "statement",
        [
            "Teach all GLMs",
            "Revise an entire chapter",
            "Do Chapter 4",
            "Finish the chapter",
            "Revise the whole subject",
            "Cover all topics before the exam",
            "Introduce X and also revise Y",
            "Master the topic in one sitting",
            "Revise the whole chapter on GLMs",
            "Teach all of chapter 4",
        ],
    )
    def test_non_atomic_rejected(self, statement: str) -> None:
        assert not AtomicityPolicy.is_atomic_statement(statement)
        with pytest.raises(EducationalInvariantViolation):
            make_episode(goal=make_goal(statement=statement, purpose=statement))


class TestAtomicityPolicyEdgeCases:
    def test_empty_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AtomicityPolicy.assert_atomic_statement("  ")

    def test_purpose_multi_connector(self) -> None:
        goal = make_goal(
            statement="Repair select confusion",
            purpose="Repair select confusion and also teach all GLMs",
        )
        with pytest.raises(EducationalInvariantViolation):
            AtomicityPolicy.assert_atomic_goal(goal)
        with pytest.raises(EducationalInvariantViolation):
            make_episode(goal=goal)

    def test_case_insensitive(self) -> None:
        assert not AtomicityPolicy.is_atomic_statement("REVISE THE ENTIRE CHAPTER")
        assert not AtomicityPolicy.is_atomic_statement("do chapter 12")
