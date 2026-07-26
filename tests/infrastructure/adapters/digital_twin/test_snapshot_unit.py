"""Unit tests — Twin Snapshot Builder (MS-004 T2)."""

from __future__ import annotations

from typing import Any

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import CollectorResult
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    COMPLETENESS_COMPLETE,
    COMPLETENESS_EMPTY,
    COMPLETENESS_PARTIAL,
    FACET_SYNTHESIS_ORDER,
    RUNTIME_A_FIELD_NAMES,
    SNAPSHOT_CONSTRUCTION_VERSION,
    SNAPSHOT_SCHEMA_VERSION,
    CompletenessEvaluator,
    SnapshotVersion,
    TwinFacetAssembler,
    TwinProfile,
    TwinProvenance,
    TwinSnapshot,
    TwinSnapshotBuilder,
    TwinSnapshotValidationError,
    UnavailableSummary,
    aggregate_snapshot_provenance,
    build_twin_snapshot_builder,
    serialize_canonical,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FIELD_STUDY_ATTEMPTS,
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
    collectors: dict[str, _StubCollector] = {}
    for name in RUNTIME_A_FIELD_NAMES:
        if name in overrides:
            collectors[name] = overrides[name]
            continue
        if name == "evidence":
            payload: Any = {"attempt_count": 0, "attempts": []}
        elif name in {"topic_progress", "study_attempts"}:
            payload = []
        elif name == "lifecycle_stage":
            payload = "learning"
        else:
            payload = {}
        collectors[name] = _StubCollector(name, payload=payload)
    return collectors


def _rich_collectors() -> dict[str, _StubCollector]:
    return _stub_collectors(
        **{
            FIELD_STUDY_ATTEMPTS: _StubCollector(
                FIELD_STUDY_ATTEMPTS,
                payload=[
                    {
                        "id": 11,
                        "duration_minutes": 40,
                        "confidence_before": "low",
                        "confidence_after": "medium",
                        "topic_id": 1,
                    }
                ],
            ),
            "topic_progress": _StubCollector(
                "topic_progress",
                payload=[{"topic_id": 1, "revision_count": 2, "status": "in_progress"}],
            ),
            "mission": _StubCollector(
                "mission",
                payload={"id": 5, "status": "completed"},
            ),
            "student_goals": _StubCollector(
                "student_goals",
                payload={"weekly_hours": 6},
            ),
            "curriculum": _StubCollector(
                "curriculum",
                payload={"curriculum_id": "c1", "version": "v2"},
            ),
        }
    )


def _assembler(**kwargs: Any) -> TwinFacetAssembler:
    return TwinFacetAssembler(
        collectors=kwargs.pop("collectors", _rich_collectors()),
        study_plan_service=kwargs.pop(
            "study_plan_service", _FakePlanService(_FakePlan())
        ),
        **kwargs,
    )


def test_snapshot_version_model():
    version = SnapshotVersion(
        snapshot_version="t2.0",
        schema_version="twin_snapshot.v2",
        evidence_version="runtime_a:abcd",
    )
    assert version.to_canonical_dict() == {
        "evidence_version": "runtime_a:abcd",
        "schema_version": "twin_snapshot.v2",
        "snapshot_version": "t2.0",
    }


def test_build_from_bundle_contains_seven_facets_and_versions():
    assembler = _assembler()
    bundle = assembler.assemble("9", as_of="2026-07-25")
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    snapshot = builder.build_from_bundle(bundle, generated_at="2026-07-25")

    assert isinstance(snapshot, TwinSnapshot)
    profile = snapshot.profile.to_canonical_dict()
    for name in FACET_SYNTHESIS_ORDER:
        assert name in profile
    assert snapshot.snapshot_version == SNAPSHOT_CONSTRUCTION_VERSION
    assert snapshot.schema_version == SNAPSHOT_SCHEMA_VERSION
    assert snapshot.source_evidence_version == bundle.source_evidence_version
    assert snapshot.profile_version == bundle.profile_version
    assert snapshot.generated_at == "2026-07-25"
    assert snapshot.version().evidence_version == snapshot.source_evidence_version
    assert snapshot.completeness.status in {
        COMPLETENESS_COMPLETE,
        COMPLETENESS_PARTIAL,
        COMPLETENESS_EMPTY,
    }
    assert isinstance(snapshot.unavailable_summary, UnavailableSummary)
    assert snapshot.provenance_summary.evidence_window_start is not None
    assert snapshot.authority == "digital_twin_synthesis"


def test_build_via_assembler_is_deterministic():
    assembler = _assembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    first = builder.build("9", as_of="2026-07-25")
    second = builder.build("9", as_of="2026-07-25")
    assert first.serialize() == second.serialize()
    assert serialize_canonical(first.to_canonical_dict()) == first.serialize()


def test_snapshot_equality_for_identical_bundles():
    assembler = _assembler()
    bundle = assembler.assemble("9", as_of="2026-07-25")
    builder = TwinSnapshotBuilder()
    left = builder.build_from_bundle(bundle, generated_at="2026-07-25")
    right = builder.build_from_bundle(bundle, generated_at="2026-07-25")
    assert left.serialize() == right.serialize()
    assert left == right


def test_completeness_evaluator_structural_only():
    evaluator = CompletenessEvaluator()
    provenance = {
        name: available_facet_provenance(
            source_service=SOURCE_SERVICE_TWIN_FACET,
            source_entity=name,
            collected_at="2026-07-25",
        )
        for name in FACET_SYNTHESIS_ORDER
    }
    # Use a real profile from assembler so facet objects exist.
    bundle = _assembler().assemble("9", as_of="2026-07-25")
    # Force all available via provenance override.
    completeness = evaluator.evaluate(bundle.profile, provenance)
    assert completeness.score is None
    assert completeness.status == COMPLETENESS_COMPLETE
    assert completeness.facets_unavailable == ()
    assert set(completeness.facets_present) == set(FACET_SYNTHESIS_ORDER)

    empty_prov = {
        name: unavailable_facet_provenance(
            source_service=SOURCE_SERVICE_TWIN_FACET,
            source_entity=name,
            collected_at="2026-07-25",
            reason="UNAVAILABLE",
        )
        for name in FACET_SYNTHESIS_ORDER
    }
    empty = evaluator.evaluate(TwinProfile(student_id="1"), empty_prov)
    assert empty.status == COMPLETENESS_EMPTY
    assert empty.facets_present == ()
    assert len(empty.facets_unavailable) == 7


def test_completeness_partial_and_unavailable_summary():
    assembler = TwinFacetAssembler(
        collectors=_stub_collectors(
            study_attempts=_StubCollector(
                "study_attempts",
                available=False,
                reason="UNAVAILABLE",
            )
        ),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("3", as_of="2026-07-25")
    builder = TwinSnapshotBuilder()
    snapshot = builder.build_from_bundle(bundle, generated_at="2026-07-25")
    assert snapshot.completeness.status in {
        COMPLETENESS_PARTIAL,
        COMPLETENESS_EMPTY,
    }
    assert snapshot.completeness.score is None
    for name in snapshot.unavailable_summary.facets:
        assert name in snapshot.unavailable_summary.reasons
        assert snapshot.unavailable_summary.reasons[name]


def test_provenance_aggregation():
    provenance = {
        "learning_rhythm": TwinProvenance(
            source_service="attempts_svc",
            source_entity="learning_rhythm",
            collected_at="2026-07-20",
            availability=AVAILABILITY_AVAILABLE,
            kind="runtime_a_derived",
        ),
        "consistency": TwinProvenance(
            source_service="mission_svc",
            source_entity="consistency",
            collected_at="2026-07-22",
            availability=AVAILABILITY_AVAILABLE,
            kind="runtime_a_derived",
        ),
        "persistence": TwinProvenance(
            source_service="progress_svc",
            source_entity="persistence",
            collected_at="2026-07-21",
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="INSUFFICIENT_EVIDENCE",
            kind="runtime_a_derived",
        ),
    }
    # Fill remaining facets as unavailable for a complete map.
    for name in FACET_SYNTHESIS_ORDER:
        if name in provenance:
            continue
        provenance[name] = TwinProvenance(
            source_service="twin_facet_assembler",
            source_entity=name,
            collected_at="2026-07-25",
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="UNAVAILABLE",
            kind="runtime_a_derived",
        )
    summary = aggregate_snapshot_provenance(provenance, as_of="2026-07-25")
    assert summary.contributing_runtime_a_sources == (
        "attempts_svc",
        "mission_svc",
    )
    assert summary.evidence_window_start == "2026-07-20"
    assert summary.evidence_window_end == "2026-07-25"
    assert "persistence" in summary.unavailable_inputs
    assert "learning_rhythm" not in summary.unavailable_inputs


def test_snapshot_is_immutable():
    bundle = _assembler().assemble("9", as_of="2026-07-25")
    snapshot = TwinSnapshotBuilder().build_from_bundle(
        bundle, generated_at="2026-07-25"
    )
    with pytest.raises(Exception):
        snapshot.snapshot_version = "mutated"  # type: ignore[misc]
    with pytest.raises(Exception):
        snapshot.completeness.status = "empty"  # type: ignore[misc]
    with pytest.raises(TypeError):
        snapshot.field_provenance["learning_rhythm"] = {}  # type: ignore[index]


def test_disabled_builder_raises():
    builder = TwinSnapshotBuilder(enabled=False)
    with pytest.raises(TwinSnapshotValidationError):
        builder.build("1", as_of="2026-07-25")


def test_build_requires_assembler():
    builder = TwinSnapshotBuilder(facet_assembler=None)
    with pytest.raises(TwinSnapshotValidationError):
        builder.build("1", as_of="2026-07-25")


def test_build_helper_respects_flag():
    assert build_twin_snapshot_builder(enabled=False) is None
    wired = build_twin_snapshot_builder(
        enabled=True,
        facet_assembler=_assembler(),
    )
    assert isinstance(wired, TwinSnapshotBuilder)


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_DIGITAL_TWIN is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.digital_twin is None
    assert composition_off.twin_facet_assembler is None
    assert composition_off.twin_snapshot_builder is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    assert flags_on.ENABLE_DIGITAL_TWIN is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.twin_snapshot_builder is not None
    assert (
        composition_on.twin_snapshot_builder.builder_id
        == "twin_snapshot_builder"
    )
    # T2 must not cut over Experience StudentTwinPort.
    assert composition_on.digital_twin is not composition_on.twin
    assert composition_on.twin_facet_assembler is not None


def test_bundle_type_guard():
    builder = TwinSnapshotBuilder()
    with pytest.raises(TwinSnapshotValidationError):
        builder.build_from_bundle("not-a-bundle")  # type: ignore[arg-type]


def test_completeness_does_not_estimate_score():
    """Structural completeness never invents a numeric score."""
    evaluator = CompletenessEvaluator()
    bundle = _assembler().assemble("9", as_of="2026-07-25")
    result = evaluator.evaluate(bundle.profile, bundle.field_provenance)
    assert result.score is None
    if result.status == COMPLETENESS_PARTIAL:
        assert result.facets_present
        assert result.facets_unavailable
