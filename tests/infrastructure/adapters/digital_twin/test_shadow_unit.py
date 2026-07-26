"""Unit tests — Twin Shadow Validation (MS-004 T6)."""

from __future__ import annotations

from unittest import mock

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    COMPLETENESS_COMPLETE,
    COMPLETENESS_PARTIAL,
    DRIFT_EXPLAINABILITY_INCONSISTENCY,
    DRIFT_PROJECTION_INCONSISTENCY,
    DRIFT_SNAPSHOT_INSTABILITY,
    DRIFT_UNAVAILABLE_FACETS,
    ExplainabilityConsistencyMonitor,
    ProjectionConsistencyMonitor,
    SnapshotStabilityMonitor,
    TwinCompleteness,
    TwinDriftDetectionMonitor,
    TwinProfile,
    TwinProvenance,
    TwinShadowHealthMetrics,
    TwinShadowValidator,
    TwinSnapshot,
    UnavailableSummary,
    build_twin_shadow_ops_dashboard,
    build_twin_shadow_validator,
    explanation_is_complete,
    verify_twin_rollback,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    FacetExplanation,
    SnapshotExplanation,
    StudentTwinProjection,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVENT_TYPES,
    TWIN_SHADOW_COMPLETED,
    TWIN_SHADOW_EVENT_TYPES,
    TWIN_SHADOW_HEALTH,
    TWIN_SHADOW_LATENCY,
    TWIN_SHADOW_REQUESTED,
    TWIN_SHADOW_ROLLBACK_VERIFIED,
    TWIN_SHADOW_STABILITY,
)


def _empty_snapshot(
    *,
    student_id: str = "7",
    generated_at: str = "2026-07-25T00:00:00Z",
    unavailable: tuple[str, ...] = (),
) -> TwinSnapshot:
    facets_unavailable = unavailable
    facets_present = ()
    return TwinSnapshot(
        profile=TwinProfile(student_id=student_id),
        profile_version="t2.0",
        source_evidence_version="ev-1",
        generated_at=generated_at,
        provenance=TwinProvenance(
            source_service="digital_twin",
            source_entity="TwinSnapshot",
            collected_at=generated_at,
            availability=AVAILABILITY_AVAILABLE,
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=0.5 if facets_unavailable else 1.0,
            facets_present=facets_present,
            facets_unavailable=facets_unavailable,
            status=(
                COMPLETENESS_PARTIAL
                if facets_unavailable
                else COMPLETENESS_COMPLETE
            ),
            summary="unit",
        ),
        twin_id=f"twin-{student_id}",
        authority="digital_twin",
        unavailable_summary=UnavailableSummary(
            facets=facets_unavailable,
            reasons={name: "UNAVAILABLE" for name in facets_unavailable},
        ),
    )


def _complete_explanation(
    *,
    student_id: str = "7",
    twin_id: str = "twin-7",
) -> SnapshotExplanation:
    return SnapshotExplanation(
        twin_id=twin_id,
        student_id=student_id,
        generated_at="2026-07-25T00:00:00Z",
        explainability_version="t3.0",
        overall_completeness_explanation="status=complete;present=7;unavailable=0",
        unavailable_summary_explanation="all_facets_available",
        evidence_coverage_summary="available_facets=7/7;contributing_sources=[]",
        facet_explanations=(
            FacetExplanation(
                facet_name="learning_rhythm",
                availability=AVAILABILITY_AVAILABLE,
                derivation_summary="unit stub",
                completeness_reasoning="present",
                provenance_refs=("runtime_a:study_attempts",),
            ),
        ),
        provenance_refs=("runtime_a:study_attempts",),
    )


class _StubBuilder:
    def __init__(self, snapshot: TwinSnapshot) -> None:
        self._snapshot = snapshot
        self.calls = 0

    def build(self, student_id: str, *, as_of: str | None = None) -> TwinSnapshot:
        self.calls += 1
        _ = (student_id, as_of)
        return self._snapshot


class _StubExplainability:
    def __init__(self, explanation: SnapshotExplanation) -> None:
        self._explanation = explanation
        self.calls = 0

    def explain_snapshot(self, snapshot: TwinSnapshot) -> SnapshotExplanation:
        self.calls += 1
        _ = snapshot
        return self._explanation


class _StubProjector:
    def __init__(self, projection: StudentTwinProjection) -> None:
        self._projection = projection
        self.calls = 0

    def project(
        self,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
        as_of: str | None = None,
    ) -> StudentTwinProjection:
        self.calls += 1
        _ = (snapshot, explanation, as_of)
        return self._projection


def _projection_for(snapshot: TwinSnapshot) -> StudentTwinProjection:
    from app.infrastructure.adapters.digital_twin import StudentTwinProjector

    return StudentTwinProjector().project(snapshot)


def test_twin_shadow_event_types_registered():
    for event_type in TWIN_SHADOW_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_explanation_is_complete_requires_coverage():
    incomplete = SnapshotExplanation(
        twin_id="t",
        student_id="7",
        overall_completeness_explanation="ok",
        evidence_coverage_summary="",
        facet_explanations=(),
        provenance_refs=(),
    )
    assert explanation_is_complete(incomplete) is False
    assert explanation_is_complete(_complete_explanation()) is True


def test_snapshot_stability_monitor_identical_replay():
    snapshot = _empty_snapshot()
    monitor = SnapshotStabilityMonitor()
    result = monitor.verify_replay(
        _StubBuilder(snapshot),
        "7",
        as_of="2026-07-25T00:00:00Z",
        snapshot=snapshot,
    )
    assert result.success is True
    assert result.detail == "identical_snapshot_replay"


def test_snapshot_stability_monitor_detects_mismatch():
    first = _empty_snapshot(generated_at="2026-07-25T00:00:00Z")
    second = _empty_snapshot(generated_at="2026-07-26T00:00:00Z")

    class _FlipBuilder:
        def __init__(self) -> None:
            self._n = 0

        def build(self, student_id: str, *, as_of: str | None = None) -> TwinSnapshot:
            _ = (student_id, as_of)
            self._n += 1
            return first if self._n == 1 else second

    result = SnapshotStabilityMonitor().verify_replay(_FlipBuilder(), "7")
    assert result.success is False
    assert result.detail == "snapshot_serialize_mismatch"


def test_projection_and_explainability_consistency_monitors():
    snapshot = _empty_snapshot()
    explanation = _complete_explanation()
    projection = _projection_for(snapshot)

    assert (
        ProjectionConsistencyMonitor()
        .verify_replay(
            _StubProjector(projection),
            snapshot,
            explanation=explanation,
            projection=projection,
        )
        .success
        is True
    )
    assert (
        ExplainabilityConsistencyMonitor()
        .verify_replay(
            _StubExplainability(explanation),
            snapshot,
            explanation=explanation,
        )
        .success
        is True
    )


def test_drift_monitor_emits_instability_and_unavailable():
    snapshot = _empty_snapshot(unavailable=("learning_rhythm",))
    from app.infrastructure.adapters.digital_twin.shadow_monitors import (
        StabilityResult,
    )

    signals = TwinDriftDetectionMonitor().detect(
        student_id="7",
        snapshot_stability=StabilityResult(
            success=False, detail="snapshot_serialize_mismatch"
        ),
        projection_stability=StabilityResult(success=True),
        explainability_stability=StabilityResult(
            success=False, detail="explanation_serialize_mismatch"
        ),
        snapshot=snapshot,
        determinism_success=False,
    )
    kinds = {s.kind for s in signals}
    assert DRIFT_SNAPSHOT_INSTABILITY in kinds
    assert DRIFT_EXPLAINABILITY_INCONSISTENCY in kinds
    assert DRIFT_UNAVAILABLE_FACETS in kinds


def test_health_metrics_rates():
    health = TwinShadowHealthMetrics()
    health.record_execution(
        ok=True,
        snapshot_ok=True,
        projection_ok=True,
        explainability_ok=True,
        unavailable_facet_count=2,
        determinism_success=True,
        drift_signals=1,
        latency_ms=12.5,
    )
    health.record_rollback(ok=True)
    health.record_feature_flag_isolation(passed=True)
    snap = health.snapshot()
    assert snap.executions == 1
    assert snap.snapshot_generation_success_rate == 1.0
    assert snap.projection_success_rate == 1.0
    assert snap.explainability_success_rate == 1.0
    assert snap.unavailable_facet_frequency == 2.0
    assert snap.deterministic_replay_success_rate == 1.0
    assert snap.rollback_success_rate == 1.0
    assert snap.feature_flag_isolation_pass_rate == 1.0


def test_validator_emits_telemetry_and_discards():
    events = EventRegistry()
    snapshot = _empty_snapshot()
    explanation = _complete_explanation()
    projection = _projection_for(snapshot)
    validator = TwinShadowValidator(
        snapshot_builder=_StubBuilder(snapshot),
        explainability=_StubExplainability(explanation),
        projector=_StubProjector(projection),
        events=events,
        enabled=True,
    )
    observation = validator.validate_shadow(
        "7", as_of="2026-07-25T00:00:00Z"
    )
    assert observation.ok is True
    assert observation.snapshot_ok is True
    assert observation.projection_ok is True
    assert observation.explainability_ok is True
    assert observation.determinism_ok is True
    types = [e.event_type for e in events.published()]
    assert TWIN_SHADOW_REQUESTED in types
    assert TWIN_SHADOW_COMPLETED in types
    assert TWIN_SHADOW_STABILITY in types
    assert TWIN_SHADOW_LATENCY in types
    assert TWIN_SHADOW_HEALTH in types
    completed = next(
        e for e in events.published() if e.event_type == TWIN_SHADOW_COMPLETED
    )
    assert completed.payload["discarded_for_ux"] is True
    assert completed.payload["influences_student"] is False


def test_validator_disabled_returns_unavailable():
    validator = TwinShadowValidator(
        snapshot_builder=_StubBuilder(_empty_snapshot()),
        enabled=False,
    )
    observation = validator.validate_shadow("7")
    assert observation.ok is False
    assert observation.error_code == "UNAVAILABLE"


def test_build_helpers_respect_flag():
    assert (
        build_twin_shadow_validator(
            enabled=False, snapshot_builder=_StubBuilder(_empty_snapshot())
        )
        is None
    )
    assert (
        build_twin_shadow_validator(enabled=True, snapshot_builder=None) is None
    )
    built = build_twin_shadow_validator(
        enabled=True,
        snapshot_builder=_StubBuilder(_empty_snapshot()),
    )
    assert built is not None
    dashboard = build_twin_shadow_ops_dashboard(built)
    assert dashboard["twin_shadow_validation"]["enabled"] is True
    assert dashboard["twin_shadow_validation"]["influences_student"] is False


def test_verify_twin_rollback_removes_participation():
    events = EventRegistry()
    result = verify_twin_rollback(events=events)
    assert result.ok is True
    assert result.twin_disabled_removes_participation is True
    assert result.experience_twin_port_preserved is True
    assert result.feature_flag_isolation_ok is True
    assert TWIN_SHADOW_ROLLBACK_VERIFIED in [
        e.event_type for e in events.published()
    ]


def test_composition_wires_twin_shadow_when_flag_on():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DIGITAL_TWIN": "1"}
    )
    composition, _service = build_production_experience(flags=flags)
    assert composition.twin_shadow is not None
    assert composition.twin_shadow.is_enabled() is True
    assert composition.twin is not None  # Experience TwinPort remains


def test_composition_omits_twin_shadow_when_flag_off():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DIGITAL_TWIN": "0"}
    )
    composition, _service = build_production_experience(flags=flags)
    assert composition.twin_shadow is None
    assert composition.twin_snapshot_builder is None
    assert composition.student_twin_projection_port is None
    assert composition.twin is not None


def test_projection_consistency_monitor_detects_mismatch():
    snapshot = _empty_snapshot()
    first = _projection_for(snapshot)
    second = StudentTwinProjection(
        student_id="7",
        twin_snapshot_ref="other",
        twin_id="twin-7",
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason="x",
    )

    class _Flip:
        def __init__(self) -> None:
            self._n = 0

        def project(self, *args, **kwargs):
            _ = (args, kwargs)
            self._n += 1
            return first if self._n == 1 else second

    result = ProjectionConsistencyMonitor().verify_replay(_Flip(), snapshot)
    assert result.success is False
    assert result.detail == "projection_serialize_mismatch"
    assert DRIFT_PROJECTION_INCONSISTENCY  # constant import smoke


def test_batch_long_running_replay_is_stable():
    snapshot = _empty_snapshot()
    explanation = _complete_explanation()
    projection = _projection_for(snapshot)
    validator = TwinShadowValidator(
        snapshot_builder=_StubBuilder(snapshot),
        explainability=_StubExplainability(explanation),
        projector=_StubProjector(projection),
        events=EventRegistry(),
    )
    results = validator.validate_shadow_batch(
        ("7", "7"),
        as_of="2026-07-25T00:00:00Z",
        iterations=3,
    )
    assert len(results) == 6
    assert all(item.ok and item.determinism_ok for item in results)


def test_validator_does_not_call_experience_put(monkeypatch):
    snapshot = _empty_snapshot()
    explanation = _complete_explanation()
    projection = _projection_for(snapshot)
    put = mock.Mock()
    monkeypatch.setattr(
        "app.infrastructure.adapters.student_experience.composition."
        "ExperienceTwinAdapter.put_projection",
        put,
        raising=False,
    )
    TwinShadowValidator(
        snapshot_builder=_StubBuilder(snapshot),
        explainability=_StubExplainability(explanation),
        projector=_StubProjector(projection),
        events=EventRegistry(),
    ).validate_shadow("7", as_of="2026-07-25T00:00:00Z")
    put.assert_not_called()
