"""Learner use-case catalogue tests."""

from __future__ import annotations

import pytest

from tests.application.student_experience.helpers import make_experience

USE_CASES = [
    "view_home",
    "view_journey",
    "view_revision",
    "view_history",
    "view_profile",
    "view_explanation",
    "start_session",
    "view_dashboard",
]


@pytest.mark.parametrize("use_case", USE_CASES)
def test_use_case_runs(use_case):
    exp = make_experience()
    if use_case == "view_home":
        assert exp.get_home("stu-1").student_id == "stu-1"
    elif use_case == "view_journey":
        assert exp.get_journey("stu-1").student_id == "stu-1"
    elif use_case == "view_revision":
        assert exp.get_revision("stu-1").student_id == "stu-1"
    elif use_case == "view_history":
        assert exp.get_history("stu-1").student_id == "stu-1"
    elif use_case == "view_profile":
        assert exp.get_profile("stu-1").student_id == "stu-1"
    elif use_case == "view_explanation":
        assert exp.explain("stu-1").is_complete
    elif use_case == "start_session":
        assert exp.start_session("stu-1").student_id == "stu-1"
    elif use_case == "view_dashboard":
        assert exp.get_dashboard("stu-1").student_id == "stu-1"
