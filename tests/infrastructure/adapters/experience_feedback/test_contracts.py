"""Contract tests — Experience Feedback Loop (P2-MS008)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.experience_feedback import (
    CONTRACT_VERSION,
    DEFAULT_SOURCE_DESCRIPTION,
    ExperienceFeedback,
    ExperienceFeedbackFact,
    deterministic_feedback_id,
)


def _fact(**overrides) -> ExperienceFeedbackFact:
    base = dict(
        key="completed_missions",
        label="Missions completed this week",
        value=2,
        value_label="2 missions",
        source_description=DEFAULT_SOURCE_DESCRIPTION,
    )
    base.update(overrides)
    return ExperienceFeedbackFact(**base)


def _feedback(**overrides) -> ExperienceFeedback:
    base = dict(
        feedback_id="expfb-test",
        reporting_period="this_week",
        completed_missions=2,
        completed_reflections=1,
        study_sessions=2,
        active_streak=3,
        generated_at="2026-07-25T12:00:00+00:00",
        facts=(_fact(),),
        student_id="42",
        evidence_summary_id="evfact-abc",
        source_description=DEFAULT_SOURCE_DESCRIPTION,
    )
    base.update(overrides)
    return ExperienceFeedback(**base)


def test_experience_feedback_is_immutable():
    fb = _feedback()
    with pytest.raises(Exception):
        fb.completed_missions = 99  # type: ignore[misc]


def test_experience_feedback_requires_ids_and_timestamp():
    with pytest.raises(ValueError, match="feedback_id"):
        _feedback(feedback_id="")
    with pytest.raises(ValueError, match="generated_at"):
        _feedback(generated_at="")


def test_experience_feedback_rejects_negative_counts():
    with pytest.raises(ValueError):
        _feedback(completed_missions=-1)


def test_experience_feedback_canonical_round_trip():
    fb = _feedback()
    assert fb.contract_version == CONTRACT_VERSION
    assert fb.source_description == DEFAULT_SOURCE_DESCRIPTION
    assert "completed_missions" in fb.serialize()
    assert fb.to_canonical_dict()["reporting_period_label"] == "This week"


def test_deterministic_feedback_id_stable():
    a = deterministic_feedback_id(
        student_id="7",
        reporting_period="this_week",
        completed_missions=1,
        completed_reflections=0,
        study_sessions=1,
        active_streak=1,
        generated_at="2026-07-25T00:00:00+00:00",
        evidence_summary_id="evfact-1",
    )
    b = deterministic_feedback_id(
        student_id="7",
        reporting_period="this_week",
        completed_missions=1,
        completed_reflections=0,
        study_sessions=1,
        active_streak=1,
        generated_at="2026-07-25T00:00:00+00:00",
        evidence_summary_id="evfact-1",
    )
    assert a == b
    assert a.startswith("expfb-")


def test_fact_requires_key_and_label():
    with pytest.raises(ValueError, match="key"):
        _fact(key="")
    with pytest.raises(ValueError, match="label"):
        _fact(label="")
