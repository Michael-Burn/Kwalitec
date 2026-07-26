"""Unit tests — Twin Explainability (MS-004 T3)."""

from __future__ import annotations

from typing import Any

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import CollectorResult
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    EXPLAINABILITY_VERSION,
    FACET_LEARNING_RHYTHM,
    FACET_RUNTIME_A_FIELDS,
    FACET_SYNTHESIS_ORDER,
    CompletenessEvaluator,
    FacetExplanation,
    LearningRhythmFacet,
    SnapshotExplanation,
    TwinCompleteness,
    TwinExplainabilityService,
    TwinExplainabilityValidationError,
    TwinFacetAssembler,
    TwinProfile,
    TwinSnapshot,
    TwinSnapshotBuilder,
    UnavailableSummary,
    aggregate_snapshot_provenance,
    build_twin_explainability_service,
    expand_facet_provenance,
    expand_snapshot_provenance,
    format_provenance_reference,
    serialize_canonical,
    snapshot_root_provenance,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FIELD_STUDY_ATTEMPTS,
    REASON_NO_CONFIDENCE_EVIDENCE,
    SOURCE_SERVICE_TWIN_FACET,
    available_facet_provenance,
    unavailable_facet_provenance,
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

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (user_id, as_of, context)
        return CollectorResult(
            available=self._available,
            payload=self._payload,
            source_service=self._source_service,
            source_entity=self._source_entity,
            unavailable_reason=self._reason,
        )


class _FakePlan:
    id = 1


class _FakePlanService:
    def __init__(self, plan: Any) -> None:
        self._plan = plan

    def read_active_plan(self, user_id: int) -> Any:
        _ = user_id
        return self._plan


def _stub_collectors(**overrides: _StubCollector) -> dict[str, _StubCollector]:
    from app.infrastructure.adapters.digital_twin import RUNTIME_A_FIELD_NAMES

    collectors: dict[str, _StubCollector] = {}
    for name in RUNTIME_A_FIELD_NAMES:
        if name in overrides:
            collectors[name] = overrides[name]
            continue
        collectors[name] = _StubCollector(name)
    return collectors


def _snapshot_with_rhythm(
    *,
    available: bool = True,
    evidence_refs: tuple[str, ...] = ("attempt:1",),
    reason: str = "",
) -> TwinSnapshot:
    if available:
        facet = LearningRhythmFacet(
            label="sparse",
            typical_session_minutes=30.0,
            cadence_note="attempt_count=1;median_duration_minutes=30.0",
            evidence_refs=evidence_refs,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )
        provenance = available_facet_provenance(
            source_service="learning_service",
            source_entity="StudyAttempt",
            collected_at="2026-07-25",
        )
    else:
        facet = LearningRhythmFacet(
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason or "UNAVAILABLE",
        )
        provenance = unavailable_facet_provenance(
            source_service=SOURCE_SERVICE_TWIN_FACET,
            source_entity="StudyAttempt",
            collected_at="2026-07-25",
            reason=reason or "UNAVAILABLE",
        )

    profile = TwinProfile(student_id="42", learning_rhythm=facet)
    field_provenance = {name: unavailable_facet_provenance(
        source_service=SOURCE_SERVICE_TWIN_FACET,
        source_entity=name,
        collected_at="2026-07-25",
        reason="UNAVAILABLE",
    ) for name in FACET_SYNTHESIS_ORDER}
    field_provenance[FACET_LEARNING_RHYTHM] = provenance

    completeness = CompletenessEvaluator().evaluate(profile, field_provenance)
    unavailable = CompletenessEvaluator().unavailable_summary(
        profile, field_provenance, completeness=completeness
    )
    provenance_summary = aggregate_snapshot_provenance(
        field_provenance, as_of="2026-07-25"
    )
    root = snapshot_root_provenance(
        collected_at="2026-07-25",
        completeness_status=completeness.status,
        contributing_sources=provenance_summary.contributing_runtime_a_sources,
    )
    return TwinSnapshot(
        profile=profile,
        profile_version="t1.0",
        source_evidence_version="runtime_a:test",
        generated_at="2026-07-25",
        provenance=root,
        completeness=completeness,
        twin_id="twin-42",
        field_provenance=field_provenance,
        snapshot_version="t2.0",
        schema_version="twin_snapshot.v2",
        provenance_summary=provenance_summary,
        unavailable_summary=unavailable,
    )


def test_facet_explanation_exposes_required_fields():
    service = TwinExplainabilityService()
    snapshot = _snapshot_with_rhythm(available=True)
    explanation = service.explain_facet(snapshot, FACET_LEARNING_RHYTHM)
    assert isinstance(explanation, FacetExplanation)
    assert explanation.facet_name == FACET_LEARNING_RHYTHM
    assert explanation.availability == AVAILABILITY_AVAILABLE
    assert explanation.contributing_runtime_a_evidence
    assert any(
        item.startswith("runtime_a_field:")
        for item in explanation.contributing_runtime_a_evidence
    )
    assert "attempt:1" in explanation.contributing_runtime_a_evidence
    assert explanation.derivation_summary
    assert "Derived learning_rhythm" in explanation.derivation_summary
    assert explanation.completeness_reasoning
    assert explanation.unavailable_reasoning == ""
    assert explanation.provenance_refs
    assert explanation.rule_or_model_id == "twin.structure.learning_rhythm"


def test_unavailable_facet_explanation_is_honest():
    service = TwinExplainabilityService()
    snapshot = _snapshot_with_rhythm(
        available=False, reason=REASON_NO_CONFIDENCE_EVIDENCE
    )
    # Force confidence_trend unavailable narrative via learning_rhythm reason.
    explanation = service.explain_facet(snapshot, FACET_LEARNING_RHYTHM)
    assert explanation.availability == AVAILABILITY_UNAVAILABLE
    assert explanation.unavailable_reasoning == REASON_NO_CONFIDENCE_EVIDENCE
    assert "no derivation performed" in explanation.derivation_summary
    assert explanation.rule_or_model_id == "twin.insight.sparse_evidence"
    # Unavailable facets still declare required Runtime A fields, not invented refs.
    assert explanation.contributing_runtime_a_evidence == (
        f"runtime_a_field:{FIELD_STUDY_ATTEMPTS}",
    )
    assert "attempt:" not in ";".join(explanation.contributing_runtime_a_evidence)


def test_snapshot_explanation_aggregates_all_facets():
    service = TwinExplainabilityService()
    snapshot = _snapshot_with_rhythm(available=True)
    explanation = service.explain_snapshot(snapshot)
    assert isinstance(explanation, SnapshotExplanation)
    assert explanation.explainability_version == EXPLAINABILITY_VERSION
    assert explanation.twin_id == "twin-42"
    assert explanation.student_id == "42"
    assert explanation.generated_at == "2026-07-25"
    assert explanation.overall_completeness_explanation
    assert explanation.unavailable_summary_explanation
    assert explanation.evidence_coverage_summary
    assert len(explanation.facet_explanations) == len(FACET_SYNTHESIS_ORDER)
    names = [item.facet_name for item in explanation.facet_explanations]
    assert names == list(FACET_SYNTHESIS_ORDER)
    assert explanation.provenance_refs
    assert explanation.serialize() == serialize_canonical(
        explanation.to_canonical_dict()
    )


def test_identical_snapshot_yields_identical_explanations():
    service = TwinExplainabilityService()
    snapshot = _snapshot_with_rhythm(available=True)
    first = service.explain_snapshot(snapshot)
    second = service.explain_snapshot(snapshot)
    assert first.serialize() == second.serialize()
    for a, b in zip(first.facet_explanations, second.facet_explanations, strict=True):
        assert a.serialize() == b.serialize()


def test_provenance_expansion_is_deterministic_and_complete():
    snapshot = _snapshot_with_rhythm(available=True)
    expansions = expand_snapshot_provenance(
        snapshot.field_provenance, root=snapshot.provenance
    )
    assert len(expansions) == len(FACET_SYNTHESIS_ORDER) + 1
    again = expand_snapshot_provenance(
        snapshot.field_provenance, root=snapshot.provenance
    )
    assert [item.to_canonical_dict() for item in expansions] == [
        item.to_canonical_dict() for item in again
    ]
    rhythm = expand_facet_provenance(
        FACET_LEARNING_RHYTHM,
        snapshot.field_provenance[FACET_LEARNING_RHYTHM],
    )
    assert rhythm.reference.startswith("provenance:learning_service/StudyAttempt")
    assert rhythm.contributing_runtime_a_fields == FACET_RUNTIME_A_FIELDS[
        FACET_LEARNING_RHYTHM
    ]
    formatted = format_provenance_reference(
        source_service="learning_service",
        source_entity="StudyAttempt",
        collected_at="2026-07-25",
        availability="available",
        kind="runtime_a_derived",
    )
    assert formatted == rhythm.reference


def test_missing_data_explanations_remain_explicit():
    service = TwinExplainabilityService()
    profile = TwinProfile(student_id="7")
    field_provenance = {
        name: unavailable_facet_provenance(
            source_service=SOURCE_SERVICE_TWIN_FACET,
            source_entity=name,
            collected_at="2026-07-25",
            reason="NO_ACTIVE_PLAN",
        )
        for name in FACET_SYNTHESIS_ORDER
    }
    completeness = TwinCompleteness(
        score=None,
        facets_present=(),
        facets_unavailable=tuple(FACET_SYNTHESIS_ORDER),
        status="empty",
        summary="status=empty;present=0;unavailable=7",
    )
    unavailable = UnavailableSummary(
        facets=tuple(FACET_SYNTHESIS_ORDER),
        reasons={name: "NO_ACTIVE_PLAN" for name in FACET_SYNTHESIS_ORDER},
        summary="unavailable=7;reasons=NO_ACTIVE_PLAN",
    )
    provenance_summary = aggregate_snapshot_provenance(
        field_provenance, as_of="2026-07-25"
    )
    snapshot = TwinSnapshot(
        profile=profile,
        generated_at="2026-07-25",
        completeness=completeness,
        unavailable_summary=unavailable,
        field_provenance=field_provenance,
        provenance_summary=provenance_summary,
        provenance=snapshot_root_provenance(
            collected_at="2026-07-25",
            completeness_status="empty",
            contributing_sources=(),
        ),
        twin_id="twin-7",
    )
    explanation = service.explain_snapshot(snapshot)
    assert "status=empty" in explanation.overall_completeness_explanation
    assert "NO_ACTIVE_PLAN" in explanation.unavailable_summary_explanation
    for item in explanation.facet_explanations:
        assert item.availability == AVAILABILITY_UNAVAILABLE
        assert item.unavailable_reasoning == "NO_ACTIVE_PLAN"
        assert item.provenance_refs


def test_unknown_facet_raises():
    service = TwinExplainabilityService()
    snapshot = _snapshot_with_rhythm()
    with pytest.raises(TwinExplainabilityValidationError):
        service.explain_facet(snapshot, "not_a_facet")


def test_disabled_service_raises():
    service = TwinExplainabilityService(enabled=False)
    snapshot = _snapshot_with_rhythm()
    with pytest.raises(TwinExplainabilityValidationError):
        service.explain_snapshot(snapshot)


def test_di_helper_respects_flag():
    assert build_twin_explainability_service(enabled=False) is None
    wired = build_twin_explainability_service(enabled=True)
    assert isinstance(wired, TwinExplainabilityService)
    assert wired.is_enabled()


def test_digital_twin_flag_defaults_off_and_wires_explainability():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False
    composition, _service = build_production_experience(
        flags=resolve_v2_feature_flags(environ={}),
        seed_demo_learners=False,
    )
    assert composition.digital_twin is None
    assert composition.twin_explainability is None

    on_flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DIGITAL_TWIN": "1"}
    )
    assert on_flags.ENABLE_DIGITAL_TWIN is True
    composition_on, _ = build_production_experience(
        flags=on_flags,
        seed_demo_learners=False,
    )
    assert composition_on.twin_explainability is not None
    assert composition_on.twin_explainability.is_enabled()


def test_stub_collectors_pipeline_explanations_are_deterministic():
    collectors = _stub_collectors(
        study_attempts=_StubCollector(
            "study_attempts",
            payload=[
                {
                    "attempt_id": "9",
                    "duration_minutes": 25,
                    "study_date": "2026-07-20",
                }
            ],
            source_service="learning_service",
            source_entity="StudyAttempt",
        ),
        mission=_StubCollector(
            "mission",
            payload={
                "history": [
                    {"mission_id": "m1", "status": "completed"},
                ]
            },
            source_service="mission_service",
            source_entity="Mission",
        ),
        topic_progress=_StubCollector(
            "topic_progress",
            payload=[{"topic_progress_id": "tp1", "revision_count": 1}],
            source_service="progress_service",
            source_entity="TopicProgress",
        ),
    )
    assembler = TwinFacetAssembler(
        collectors=collectors,
        study_plan_service=_FakePlanService(_FakePlan()),
    )
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    service = TwinExplainabilityService()
    first = service.explain_snapshot(
        builder.build("42", as_of="2026-07-25")
    )
    second = service.explain_snapshot(
        builder.build("42", as_of="2026-07-25")
    )
    assert first.serialize() == second.serialize()
    assert len(first.facet_explanations) == 7
