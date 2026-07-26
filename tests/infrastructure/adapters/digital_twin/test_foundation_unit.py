"""Unit tests — Student Digital Twin Foundation (EP-001.1)."""

from __future__ import annotations

import dataclasses
from types import MappingProxyType

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    ConsistencyFacet,
    LearningRhythmFacet,
    PersistenceFacet,
    SessionHabitsFacet,
    TwinCompleteness,
    TwinFacetBundle,
    TwinProfile,
    TwinRuntimeEvidence,
    TwinSnapshot,
    build_student_digital_twin_foundation,
    build_student_twin_foundation_authority_port,
)
from app.infrastructure.adapters.digital_twin.authority import (
    StudentTwinFoundationAuthorityPort,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    REASON_MOCK_NOT_DISTINGUISHED,
    CanonicalLearnerState,
    StudentDigitalTwinFoundation,
)


def _evidence(*, student_id: str = "42") -> TwinRuntimeEvidence:
    return TwinRuntimeEvidence(
        student_id=student_id,
        as_of="2026-07-26T10:00:00",
        topic_progress=(
            MappingProxyType(
                {
                    "topic_progress_id": "1",
                    "topic_id": "10",
                    "topic_name": "Algebra",
                    "mastery_score": 72.0,
                    "average_accuracy": 80.0,
                    "current_stage": "Mastered",
                    "confidence": "High",
                    "completed": True,
                    "revision_count": 2,
                    "last_reviewed": "2026-07-20T00:00:00",
                    "next_review_date": "2026-07-27",
                }
            ),
            MappingProxyType(
                {
                    "topic_progress_id": "2",
                    "topic_id": "11",
                    "topic_name": "Calculus",
                    "mastery_score": 40.0,
                    "average_accuracy": 55.0,
                    "current_stage": "Learning",
                    "confidence": "Low",
                    "completed": False,
                    "revision_count": 0,
                    "last_reviewed": None,
                    "next_review_date": None,
                }
            ),
        ),
        study_attempts=(
            MappingProxyType(
                {
                    "attempt_id": "100",
                    "mission_id": "9",
                    "topic_id": "10",
                    "study_date": "2026-07-25",
                    "duration_minutes": 30,
                    "questions_attempted": 10,
                    "questions_correct": 8,
                    "accuracy_pct": 80.0,
                }
            ),
        ),
        mission=MappingProxyType(
            {
                "today": {
                    "mission_id": "9",
                    "mission_date": "2026-07-26",
                    "status": "completed",
                },
                "history": [
                    {
                        "mission_id": "9",
                        "mission_date": "2026-07-26",
                        "status": "completed",
                    },
                    {
                        "mission_id": "8",
                        "mission_date": "2026-07-25",
                        "status": "missed",
                    },
                ],
                "history_count": 2,
            }
        ),
        readiness=MappingProxyType(
            {
                "overall": {"score": 61.0, "label": "building"},
                "coverage": {},
                "review_backlog": {},
                "streaks": {"current_streak": 3, "longest_streak": 7},
                "current_streak": 3,
                "longest_streak": 7,
            }
        ),
        student_goals=MappingProxyType(
            {
                "exam_name": "Sample Exam",
                "target_exam_date": "2026-11-01",
                "planned_weekly_hours": 10,
                "exam_countdown_days": 98,
            }
        ),
        curriculum=MappingProxyType({"exam_name": "Sample Exam"}),
        lifecycle_stage="learning",
        field_available=MappingProxyType(
            {
                "topic_progress": True,
                "study_attempts": True,
                "mission": True,
                "readiness": True,
                "student_goals": True,
                "curriculum": True,
                "evidence": True,
                "lifecycle_stage": True,
            }
        ),
        field_reasons=MappingProxyType({}),
        field_sources=MappingProxyType({}),
    )


def _facet_bundle(evidence: TwinRuntimeEvidence) -> TwinFacetBundle:
    return TwinFacetBundle(
        student_id=evidence.student_id,
        as_of=evidence.as_of,
        profile=TwinProfile(
            student_id=evidence.student_id,
            learning_rhythm=LearningRhythmFacet(
                label="steady",
                typical_session_minutes=30.0,
                cadence_note="regular",
                availability="available",
                evidence_refs=("attempt:100",),
            ),
            consistency=ConsistencyFacet(
                label="regular",
                adherence_note="on plan",
                availability="available",
                evidence_refs=("mission:9",),
            ),
            persistence=PersistenceFacet(
                label="observed",
                continuity_note="continuing",
                availability="available",
                evidence_refs=("attempt:100",),
            ),
            session_habits=SessionHabitsFacet(
                label="observed",
                habits_note="mornings",
                availability="available",
                evidence_refs=("attempt:100",),
            ),
        ),
        completeness=TwinCompleteness(
            facets_present=("consistency", "learning_rhythm"),
            status="partial",
        ),
        source_evidence_version="ev-test",
    )


def test_foundation_assembles_canonical_dimensions():
    evidence = _evidence()
    bundle = _facet_bundle(evidence)
    foundation = StudentDigitalTwinFoundation(enabled=True)
    state = foundation.assemble(
        "42",
        as_of=evidence.as_of,
        evidence=evidence,
        facet_bundle=bundle,
        snapshot=TwinSnapshot(
            profile=bundle.profile,
            profile_version="t1.0",
            source_evidence_version="ev-test",
            generated_at=evidence.as_of,
            twin_id="twin-42",
        ),
    )

    assert isinstance(state, CanonicalLearnerState)
    assert state.availability == AVAILABILITY_AVAILABLE
    assert state.foundation_version == FOUNDATION_VERSION
    assert state.topic_mastery["availability"] == AVAILABILITY_AVAILABLE
    assert state.topic_mastery["payload"]["mastered_topic_count"] == 1
    assert state.topic_progress["payload"]["topic_count"] == 2
    assert state.learning_evidence["payload"]["attempt_count"] == 1
    assert state.practice_performance["payload"]["mean_accuracy_pct"] == 80.0
    assert state.mock_performance["availability"] == AVAILABILITY_UNAVAILABLE
    assert state.mock_performance["unavailable_reason"] == REASON_MOCK_NOT_DISTINGUISHED
    assert state.streaks["payload"]["current_streak"] == 3
    assert state.mission_completion["payload"]["completed_count"] == 1
    assert state.study_consistency["availability"] == AVAILABILITY_AVAILABLE
    assert "study_behaviour" in state.to_canonical_dict()


def test_foundation_serialize_is_deterministic():
    evidence = _evidence()
    bundle = _facet_bundle(evidence)
    foundation = StudentDigitalTwinFoundation(enabled=True)
    a = foundation.assemble(
        "42", as_of=evidence.as_of, evidence=evidence, facet_bundle=bundle
    )
    b = foundation.assemble(
        "42", as_of=evidence.as_of, evidence=evidence, facet_bundle=bundle
    )
    assert a.serialize() == b.serialize()


def test_foundation_disabled_returns_unavailable():
    foundation = StudentDigitalTwinFoundation(enabled=False)
    state = foundation.assemble("42")
    assert state.availability == AVAILABILITY_UNAVAILABLE
    assert state.unavailable_reason == "foundation_flag_off"


def test_build_foundation_requires_flag():
    assert build_student_digital_twin_foundation(enabled=False) is None
    built = build_student_digital_twin_foundation(enabled=True)
    assert built is not None
    assert built.is_enabled()


def test_authority_port_implements_student_twin_port():
    evidence = _evidence()
    bundle = _facet_bundle(evidence)
    foundation = StudentDigitalTwinFoundation(enabled=True)

    class _StubFoundation(StudentDigitalTwinFoundation):
        def assemble(self, student_id, **kwargs):  # noqa: ANN001
            return foundation.assemble(
                student_id,
                as_of=evidence.as_of,
                evidence=evidence,
                facet_bundle=bundle,
            )

    port = StudentTwinFoundationAuthorityPort(
        foundation=_StubFoundation(enabled=True),
        fallback=None,
        enabled=True,
    )
    assert isinstance(port, StudentTwinPort)
    summary = port.get_learner_summary("42")
    assert summary is not None
    assert summary["authority"] == "digital_twin_synthesis"
    assert summary["statistics"]["study_streak_days"] == 3
    assert summary["canonical_state"]["mission_completion"]["payload"][
        "completed_count"
    ] == 1
    readiness = port.get_readiness_summary("42")
    assert readiness["current_streak"] == 3
    insights = port.get_learning_insights("42")
    assert insights["topics_mastered"] == 1


def test_authority_falls_back_when_foundation_unavailable():
    class _Fallback:
        def get_learner_summary(self, student_id):  # noqa: ANN001
            return {"student_id": student_id, "authority": "fallback"}

        def get_readiness_summary(self, student_id):  # noqa: ANN001
            return {"authority": "fallback"}

        def get_learning_insights(self, student_id):  # noqa: ANN001
            return {"authority": "fallback"}

    foundation = StudentDigitalTwinFoundation(enabled=False)
    port = build_student_twin_foundation_authority_port(
        enabled=True,
        foundation=foundation,
        fallback=_Fallback(),
    )
    assert port is not None
    assert port.get_learner_summary("42")["authority"] == "fallback"


def test_digital_twin_authority_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        }
    )
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False

    flags_on = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        }
    )
    assert flags_on.ENABLE_DIGITAL_TWIN is True
    assert flags_on.ENABLE_DIGITAL_TWIN_AUTHORITY is True


def test_canonical_state_is_immutable():
    state = CanonicalLearnerState(
        student_id="42",
        as_of="2026-07-26T10:00:00",
        foundation_version=FOUNDATION_VERSION,
        twin_id="twin-42",
        study_state={"availability": "available", "payload": {}},
        topic_mastery={"availability": "available", "payload": {}},
        topic_progress={"availability": "available", "payload": {}},
        learning_evidence={"availability": "available", "payload": {}},
        practice_performance={"availability": "available", "payload": {}},
        mock_performance={"availability": "unavailable", "payload": {}},
        study_behaviour={"availability": "available", "payload": {}},
        study_consistency={"availability": "available", "payload": {}},
        streaks={"availability": "available", "payload": {"current_streak": 1}},
        mission_completion={"availability": "available", "payload": {}},
    )
    with pytest.raises((TypeError, dataclasses.FrozenInstanceError)):
        state.student_id = "99"  # type: ignore[misc]
