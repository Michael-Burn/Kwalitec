"""Evidence read integration + flag isolation — Experience Feedback (P2-MS008)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    CLAIM_ORGANISATION,
    CLASS_DELIVERY_EVENT,
    EvidencePlatformAdapter,
    ObservedEvent,
    build_evidence_platform_adapter,
    build_factual_summary,
)
from app.infrastructure.adapters.experience_feedback import (
    DEFAULT_SOURCE_DESCRIPTION,
    ExperienceFeedbackReader,
    build_experience_feedback_reader,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _event(
    *,
    student_id: str,
    event_type: str,
    observed_at: str,
) -> ObservedEvent:
    return ObservedEvent(
        student_id=student_id,
        event_type=event_type,
        observed_at=observed_at,
        ingested_at=observed_at,
        as_of=observed_at,
        claim_boundary=CLAIM_ORGANISATION,
        evidence_class=CLASS_DELIVERY_EVENT,
        payload_summary={"experience_event": event_type},
    )


def test_experience_feedback_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_FEEDBACK is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_feedback is False


def test_experience_feedback_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_FEEDBACK": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_FEEDBACK is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_feedback is True


def test_flag_isolation_from_prior_programme_ii_flags():
    feedback_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_FEEDBACK": "1"}
    )
    assert feedback_only.ENABLE_EXPERIENCE_FEEDBACK is True
    assert feedback_only.ENABLE_EXPERIENCE_OBSERVATION is False
    assert feedback_only.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    assert feedback_only.ENABLE_EVIDENCE_PLATFORM is False
    assert feedback_only.ENABLE_UNIFIED_JOURNEY is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EXPERIENCE_DIAGNOSTICS": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_UNIFIED_JOURNEY": "1",
        }
    )
    assert others_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert others_only.ENABLE_EXPERIENCE_OBSERVATION is True
    assert others_only.ENABLE_UNIFIED_JOURNEY is True


def test_build_reader_respects_enabled_flag():
    assert build_experience_feedback_reader(enabled=False) is None
    reader = build_experience_feedback_reader(enabled=True)
    assert isinstance(reader, ExperienceFeedbackReader)


def test_composition_wires_feedback_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.experience_feedback is None

    flags_on = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.experience_feedback, ExperienceFeedbackReader)
    assert isinstance(composition_on.evidence_platform, EvidencePlatformAdapter)
    assert (
        composition_on.experience_feedback.evidence
        is composition_on.evidence_platform
    )


def test_evidence_query_factual_summary_from_collect_event():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="42",
            event_type="session_completed",
            observed_at="2026-07-24T10:00:00+00:00",
        )
    )
    adapter.collect_event(
        _event(
            student_id="42",
            event_type="reflection_completed",
            observed_at="2026-07-24T10:30:00+00:00",
        )
    )
    adapter.collect_event(
        _event(
            student_id="42",
            event_type="session_completed",
            observed_at="2026-07-25T09:00:00+00:00",
        )
    )
    result = adapter.query_factual_summary(
        "42",
        reporting_period="this_week",
        as_of="2026-07-25T12:00:00+00:00",
    )
    assert result.ok is True
    summary = result.value
    assert summary is not None
    assert summary.completed_missions == 2
    assert summary.study_sessions == 2
    assert summary.completed_reflections == 1
    assert summary.active_streak == 2
    assert summary.source_description == DEFAULT_SOURCE_DESCRIPTION
    assert summary.authority == "evidence_platform"


def test_reader_load_through_public_evidence_read():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="7",
            event_type="session_completed",
            observed_at="2026-07-25T08:00:00+00:00",
        )
    )
    reader = ExperienceFeedbackReader(enabled=True, evidence=adapter)
    feedback = reader.load(
        "7",
        as_of="2026-07-25T12:00:00+00:00",
    )
    assert feedback is not None
    assert feedback.completed_missions == 1
    assert feedback.study_sessions == 1
    assert feedback.active_streak == 1
    assert feedback.source_description == DEFAULT_SOURCE_DESCRIPTION
    assert all(
        fact.source_description == DEFAULT_SOURCE_DESCRIPTION
        for fact in feedback.facts
    )


def test_reader_returns_none_when_evidence_unavailable():
    reader = ExperienceFeedbackReader(enabled=True, evidence=None)
    assert reader.load("1") is None


def test_reader_returns_none_when_flag_off():
    adapter = build_evidence_platform_adapter(enabled=True)
    reader = ExperienceFeedbackReader(enabled=False, evidence=adapter)
    assert reader.load("1") is None


def test_build_factual_summary_isolates_students():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="a",
            event_type="session_completed",
            observed_at="2026-07-25T08:00:00+00:00",
        )
    )
    adapter.collect_event(
        _event(
            student_id="b",
            event_type="session_completed",
            observed_at="2026-07-25T08:00:00+00:00",
        )
    )
    summary = build_factual_summary(
        "a",
        adapter.retained_observations(),
        as_of="2026-07-25T12:00:00+00:00",
    )
    assert summary.completed_missions == 1
    assert summary.student_id == "a"
