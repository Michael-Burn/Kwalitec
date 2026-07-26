"""Unit tests — Twin Facet Synthesis (MS-004 T1)."""

from __future__ import annotations

from typing import Any

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import CollectorResult
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_SYNTHESIS_ORDER,
    REASON_INVALID_STUDENT_ID,
    REASON_NO_ACTIVE_PLAN,
    REASON_NO_CONFIDENCE_EVIDENCE,
    RUNTIME_A_FIELD_NAMES,
    TwinFacetAssembler,
    TwinFacetValidationError,
    TwinRuntimeEvidence,
    build_twin_facet_assembler,
    default_facet_builders,
    serialize_canonical,
)
from app.infrastructure.adapters.digital_twin.builders import (
    ConfidenceTrendBuilder,
    LearningRhythmBuilder,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FIELD_MISSION,
    FIELD_STUDENT_GOALS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_TOPIC_PROGRESS,
)
from app.infrastructure.adapters.digital_twin.validation import (
    validate_no_facet_cross_dependency,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


class _StubCollector:
    def __init__(
        self,
        field_name: str,
        *,
        available: bool = True,
        payload: Any = None,
        reason: str = "",
        source_service: str = "stub_service",
        source_entity: str = "StubEntity",
    ) -> None:
        self.field_name = field_name
        self._available = available
        self._payload = payload if payload is not None else (
            [] if field_name in {"topic_progress", "study_attempts"} else {}
        )
        self._reason = reason
        self._source_service = source_service
        self._source_entity = source_entity
        self.calls = 0

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        self.calls += 1
        _ = (user_id, as_of, context)
        return CollectorResult(
            available=self._available,
            payload=self._payload,
            source_service=self._source_service,
            source_entity=self._source_entity,
            unavailable_reason=self._reason,
        )


class _FakePlanService:
    def __init__(self, plan: Any) -> None:
        self._plan = plan

    def read_active_plan(self, user_id: int) -> Any:
        _ = user_id
        return self._plan


def _stub_collectors(**overrides: _StubCollector) -> dict[str, _StubCollector]:
    collectors: dict[str, _StubCollector] = {}
    for name in RUNTIME_A_FIELD_NAMES:
        if name in overrides:
            collectors[name] = overrides[name]
            continue
        if name == "evidence":
            payload: Any = {
                "attempt_count": 0,
                "authorised_count": 0,
                "attempts": [],
            }
        elif name == "topic_progress":
            payload = []
        elif name == "study_attempts":
            payload = []
        elif name == "mission":
            payload = {"today": None, "history": [], "history_count": 0}
        elif name == "readiness":
            payload = {"overall": {"score": 1.0}, "coverage": {}, "review_backlog": {}}
        elif name == "curriculum":
            payload = {
                "curriculum_id": "9",
                "exam_name": "CM1",
                "version": "2025",
                "leaves": [{"topic_id": "1", "topic_name": "A", "order": 1}],
                "leaf_count": 1,
            }
        elif name == "student_goals":
            payload = {
                "study_plan_id": "3",
                "exam_date": "2026-09-01",
                "preferred_session_minutes": 45,
            }
        else:
            payload = {"stage": "learning"}
        collectors[name] = _StubCollector(name, payload=payload)
    return collectors


def _rich_attempt_collectors() -> dict[str, _StubCollector]:
    return _stub_collectors(
        study_attempts=_StubCollector(
            "study_attempts",
            payload=[
                {
                    "attempt_id": "2",
                    "mission_id": "10",
                    "topic_id": "1",
                    "study_date": "2026-07-20",
                    "duration_minutes": 40,
                    "questions_attempted": 8,
                    "questions_correct": 5,
                    "accuracy_pct": 62.5,
                    "confidence_before": "low",
                    "confidence_after": "medium",
                },
                {
                    "attempt_id": "1",
                    "mission_id": "9",
                    "topic_id": "1",
                    "study_date": "2026-07-18",
                    "duration_minutes": 50,
                    "questions_attempted": 10,
                    "questions_correct": 7,
                    "accuracy_pct": 70.0,
                    "confidence_before": "medium",
                    "confidence_after": "high",
                },
            ],
        ),
        mission=_StubCollector(
            "mission",
            payload={
                "today": None,
                "history": [
                    {
                        "mission_id": "9",
                        "mission_date": "2026-07-18",
                        "title": "A",
                        "status": "completed",
                        "study_plan_id": "3",
                        "subject_id": "1",
                    },
                    {
                        "mission_id": "10",
                        "mission_date": "2026-07-20",
                        "title": "B",
                        "status": "completed",
                        "study_plan_id": "3",
                        "subject_id": "1",
                    },
                ],
                "history_count": 2,
            },
        ),
        topic_progress=_StubCollector(
            "topic_progress",
            payload=[
                {
                    "topic_progress_id": "5",
                    "topic_id": "1",
                    "topic_name": "A",
                    "mastery_score": 0.4,
                    "average_accuracy": 0.7,
                    "current_stage": "learning",
                    "confidence": "medium",
                    "completed": False,
                    "revision_count": 1,
                    "last_reviewed": "2026-07-20T10:00:00",
                    "next_review_date": "2026-07-27",
                }
            ],
        ),
    )


def test_builders_declare_no_facet_dependencies():
    builders = default_facet_builders()
    validate_no_facet_cross_dependency(
        {b.facet_name: set(b.source_fields) for b in builders}
    )


def test_assembler_builds_deterministic_bundle():
    collectors = _rich_attempt_collectors()
    assembler = TwinFacetAssembler(
        collectors=collectors,
        study_plan_service=_FakePlanService(None),
    )
    first = assembler.assemble("42", as_of="2026-07-25")
    second = assembler.assemble("42", as_of="2026-07-25")
    assert first.serialize() == second.serialize()
    assert serialize_canonical(first.to_canonical_dict()) == first.serialize()


def test_assembler_provenance_on_every_facet():
    assembler = TwinFacetAssembler(
        collectors=_rich_attempt_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("7", as_of="2026-07-25T12:00:00")
    assert set(FACET_SYNTHESIS_ORDER).issubset(bundle.field_provenance.keys())
    for name in FACET_SYNTHESIS_ORDER:
        entry = dict(bundle.field_provenance[name])
        assert entry["source_service"]
        assert entry["source_entity"]
        assert entry["collected_at"] == "2026-07-25T12:00:00"
        assert entry["availability"] in {
            AVAILABILITY_AVAILABLE,
            AVAILABILITY_UNAVAILABLE,
        }
        if entry["availability"] == AVAILABILITY_UNAVAILABLE:
            assert entry["unavailable_reason"]


def test_missing_inputs_return_explicit_unavailable():
    collectors = _stub_collectors(
        study_attempts=_StubCollector(
            "study_attempts",
            available=False,
            payload=[],
            reason=REASON_NO_ACTIVE_PLAN,
            source_service="learning_service",
            source_entity="StudyAttempt",
        ),
        mission=_StubCollector(
            "mission",
            available=False,
            payload={},
            reason=REASON_NO_ACTIVE_PLAN,
            source_service="mission_service",
            source_entity="Mission",
        ),
        topic_progress=_StubCollector(
            "topic_progress",
            available=False,
            payload=[],
            reason=REASON_NO_ACTIVE_PLAN,
            source_service="adaptive_learning_service",
            source_entity="TopicProgress",
        ),
    )
    assembler = TwinFacetAssembler(
        collectors=collectors,
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("11", as_of="2026-07-25")
    rhythm = dict(bundle.field_provenance["learning_rhythm"])
    assert rhythm["availability"] == AVAILABILITY_UNAVAILABLE
    assert rhythm["unavailable_reason"] == REASON_NO_ACTIVE_PLAN
    assert bundle.profile.learning_rhythm.availability == AVAILABILITY_UNAVAILABLE
    assert bundle.profile.learning_rhythm.evidence_refs == ()
    assert bundle.profile.learning_rhythm.typical_session_minutes is None


def test_confidence_trend_unavailable_without_confidence_fields():
    evidence = TwinRuntimeEvidence(
        student_id="5",
        as_of="2026-07-25",
        study_attempts=(
            {
                "attempt_id": "1",
                "study_date": "2026-07-20",
                "duration_minutes": 30,
                "confidence_before": "",
                "confidence_after": "",
            },
        ),
        field_available={FIELD_STUDY_ATTEMPTS: True},
        field_sources={
            FIELD_STUDY_ATTEMPTS: {
                "source_service": "learning_service",
                "source_entity": "StudyAttempt",
            }
        },
    )
    result = ConfidenceTrendBuilder().build(evidence, collected_at="2026-07-25")
    assert result.provenance.availability == AVAILABILITY_UNAVAILABLE
    assert result.provenance.unavailable_reason == REASON_NO_CONFIDENCE_EVIDENCE
    assert result.facet.evidence_refs == ()


def test_learning_rhythm_median_from_observed_durations():
    evidence = TwinRuntimeEvidence(
        student_id="5",
        as_of="2026-07-25",
        study_attempts=(
            {
                "attempt_id": "1",
                "study_date": "2026-07-18",
                "duration_minutes": 30,
            },
            {
                "attempt_id": "2",
                "study_date": "2026-07-20",
                "duration_minutes": 50,
            },
        ),
        field_available={FIELD_STUDY_ATTEMPTS: True},
        field_sources={
            FIELD_STUDY_ATTEMPTS: {
                "source_service": "learning_service",
                "source_entity": "StudyAttempt",
            }
        },
    )
    result = LearningRhythmBuilder().build(evidence, collected_at="2026-07-25")
    assert result.facet.availability == AVAILABILITY_AVAILABLE
    assert result.facet.typical_session_minutes == 40.0
    assert result.facet.label == "regular"
    assert "attempt:1" in result.facet.evidence_refs


def test_invalid_student_id_yields_unavailable_contract():
    assembler = TwinFacetAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble(" ", as_of="2026-07-25")
    for name in FACET_SYNTHESIS_ORDER:
        assert (
            dict(bundle.field_provenance[name])["availability"]
            == AVAILABILITY_UNAVAILABLE
        )
        assert (
            dict(bundle.field_provenance[name])["unavailable_reason"]
            == REASON_INVALID_STUDENT_ID
        )


def test_bundle_and_profile_are_immutable():
    assembler = TwinFacetAssembler(
        collectors=_rich_attempt_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("3", as_of="2026-07-25")
    with pytest.raises(Exception):
        bundle.student_id = "x"  # type: ignore[misc]
    with pytest.raises(Exception):
        bundle.profile.learning_rhythm.label = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        bundle.field_provenance["learning_rhythm"] = {}  # type: ignore[index]


def test_disabled_assembler_raises():
    assembler = TwinFacetAssembler(enabled=False)
    with pytest.raises(TwinFacetValidationError):
        assembler.assemble("1", as_of="2026-07-25")


def test_build_helper_respects_flag():
    assert build_twin_facet_assembler(enabled=False) is None
    wired = build_twin_facet_assembler(enabled=True)
    assert isinstance(wired, TwinFacetAssembler)


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_DIGITAL_TWIN is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.digital_twin is None
    assert composition_off.twin_facet_assembler is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    assert flags_on.ENABLE_DIGITAL_TWIN is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.twin_facet_assembler is not None
    assert composition_on.twin_facet_assembler.assembler_id == "twin_facet_assembler"
    # T1 must not cut over Experience StudentTwinPort.
    assert composition_on.digital_twin is not composition_on.twin


def test_empty_available_evidence_is_honest_emptiness():
    """Collector success with empty rows → available facets, not fabricated."""
    assembler = TwinFacetAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("9", as_of="2026-07-25")
    assert bundle.profile.learning_rhythm.availability == AVAILABILITY_AVAILABLE
    assert bundle.profile.learning_rhythm.label == "none"
    assert bundle.profile.learning_rhythm.typical_session_minutes is None
    assert bundle.profile.consistency.availability == AVAILABILITY_AVAILABLE
    # Confidence requires observed before/after pairs.
    assert bundle.profile.confidence_trend.availability == AVAILABILITY_UNAVAILABLE
    assert (
        bundle.profile.confidence_trend.unavailable_reason
        == REASON_NO_CONFIDENCE_EVIDENCE
    )


def test_synthesise_from_evidence_does_not_read_other_facets():
    evidence = TwinRuntimeEvidence(
        student_id="8",
        as_of="2026-07-25",
        study_attempts=(
            {
                "attempt_id": "1",
                "study_date": "2026-07-20",
                "duration_minutes": 45,
                "confidence_before": "low",
                "confidence_after": "high",
            },
        ),
        mission={"today": None, "history": [], "history_count": 0},
        topic_progress=(),
        student_goals={"preferred_session_minutes": 45},
        lifecycle_stage="learning",
        field_available={
            FIELD_STUDY_ATTEMPTS: True,
            FIELD_MISSION: True,
            FIELD_TOPIC_PROGRESS: True,
            FIELD_STUDENT_GOALS: True,
        },
        field_sources={
            FIELD_STUDY_ATTEMPTS: {
                "source_service": "learning_service",
                "source_entity": "StudyAttempt",
            },
            FIELD_MISSION: {
                "source_service": "mission_service",
                "source_entity": "Mission",
            },
            FIELD_TOPIC_PROGRESS: {
                "source_service": "adaptive_learning_service",
                "source_entity": "TopicProgress",
            },
            FIELD_STUDENT_GOALS: {
                "source_service": "study_plan_service",
                "source_entity": "StudyPlan",
            },
        },
    )
    assembler = TwinFacetAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.synthesise_from_evidence(evidence)
    assert "learning_rhythm" in bundle.completeness.facets_present
    assert bundle.profile.learning_rhythm.typical_session_minutes == 45.0
