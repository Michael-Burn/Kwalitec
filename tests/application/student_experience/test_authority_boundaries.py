"""Authority boundary tests — experience owns projection only."""

from __future__ import annotations

import inspect

import pytest

from app.application.student_experience import student_experience_service as ses_mod
from app.application.student_experience.home_service import HomeService
from app.application.student_experience.revision_service import RevisionService
from app.domain.student_experience.recommendation_explanation import (
    FORBIDDEN_INTERNAL_TERMS,
    is_student_safe,
)
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeTwinPort,
    make_experience,
)


def test_home_requires_twin_and_adaptive_ports():
    svc = HomeService()
    with pytest.raises(Exception):
        svc.home("stu-1")


def test_revision_only_uses_adaptive():
    svc = RevisionService(adaptive_decision=FakeAdaptivePort())
    snap = svc.revision("stu-1")
    assert snap.has_revision
    # Ensure no twin dependency on RevisionService signature
    params = inspect.signature(RevisionService.__init__).parameters
    assert "student_twin" not in params


def test_facade_source_has_no_educational_calc_keywords():
    src = inspect.getsource(ses_mod.StudentExperienceService)
    for banned in ("mastery_score", "calculate_readiness", "publish_curriculum"):
        assert banned not in src


@pytest.mark.parametrize("term", FORBIDDEN_INTERNAL_TERMS)
def test_home_output_never_contains_internal_terms(term):
    exp = make_experience()
    home = exp.get_home("stu-1")
    blob = " ".join(
        [
            home.greeting,
            home.recommendation_title,
            home.recommendation_summary,
            home.exam_readiness_label,
            "" if home.explanation is None else home.explanation.summary,
            "" if home.explanation is None else home.explanation.why_recommended,
        ]
    )
    assert term.lower() not in blob.lower()
    assert is_student_safe(blob)


def test_experience_does_not_mutate_twin():
    twin = FakeTwinPort()
    before = twin.get_readiness_summary("stu-1")
    exp = make_experience(student_twin=twin)
    exp.get_home("stu-1")
    after = twin.get_readiness_summary("stu-1")
    assert before == after


def test_start_session_delegates_to_mission():
    from tests.application.student_experience.helpers import FakeMissionPort

    mission = FakeMissionPort()
    exp = make_experience(mission=mission)
    handle = exp.start_session("stu-1", mission_id="m1")
    assert mission.start_calls
    assert handle.mission_id == "m1"
