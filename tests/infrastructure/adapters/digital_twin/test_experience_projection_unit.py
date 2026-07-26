"""Unit tests — Student Twin Experience Projection (MS-004 T5)."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.adapters.digital_twin import (
    AUTHORITY_DIGITAL_TWIN,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    ConsistencyFacet,
    ExplanationSummaryProjection,
    FacetExplanation,
    FacetSummaryProjection,
    LearningRhythmFacet,
    ProjectionProvenance,
    SnapshotExplanation,
    StudentTwinProjection,
    StudentTwinProjectionPort,
    StudentTwinProjector,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    TwinSnapshot,
    UnavailableSummary,
    build_student_twin_projection_port,
    build_student_twin_projector,
    serialize_canonical,
)
from app.infrastructure.adapters.digital_twin.experience_projection import (
    REASON_READINESS_PASS_THROUGH_DEFERRED,
    REASON_TWIN_FLAG_OFF,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def _sample_snapshot(*, student_id: str = "42") -> TwinSnapshot:
    return TwinSnapshot(
        profile=TwinProfile(
            student_id=student_id,
            learning_rhythm=LearningRhythmFacet(
                label="steady",
                typical_session_minutes=25.0,
                cadence_note="regular mornings",
                availability="available",
                unavailable_reason="",
                evidence_refs=("attempt:1",),
            ),
            consistency=ConsistencyFacet(
                label="regular",
                adherence_note="on plan",
                availability="available",
                unavailable_reason="",
                evidence_refs=("mission:9",),
            ),
            limitations_codes=("sparse_predictions",),
        ),
        profile_version="t1.0",
        source_evidence_version="ev-1",
        generated_at="2026-07-25T10:00:00",
        provenance=TwinProvenance(
            source_service="twin_snapshot_builder",
            source_entity="TwinSnapshot",
            collected_at="2026-07-25T10:00:00",
            availability="available",
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=None,
            facets_present=("consistency", "learning_rhythm"),
            facets_unavailable=("cognitive_load_indicators",),
            status="partial",
            summary="partial structural coverage",
        ),
        twin_id=f"twin-{student_id}",
        snapshot_version="t2.0",
        schema_version="twin_snapshot.v2",
        unavailable_summary=UnavailableSummary(
            facets=("cognitive_load_indicators",),
            reasons={"cognitive_load_indicators": "estimate_deferred"},
        ),
    )


def _sample_explanation(snapshot: TwinSnapshot) -> SnapshotExplanation:
    return SnapshotExplanation(
        twin_id=snapshot.twin_id,
        student_id=snapshot.profile.student_id,
        generated_at=snapshot.generated_at,
        explainability_version="t3.0",
        overall_completeness_explanation="partial",
        unavailable_summary_explanation="some facets unavailable",
        evidence_coverage_summary="runtime_a refs present",
        facet_explanations=(
            FacetExplanation(
                facet_name="learning_rhythm",
                availability="available",
                contributing_runtime_a_evidence=("attempt:1",),
                derivation_summary="from study attempts",
                completeness_reasoning="present",
                provenance_refs=("study_attempts",),
                rule_or_model_id="twin.structure.learning_rhythm",
                rule_version="t3.0",
            ),
        ),
        provenance_refs=("study_attempts",),
    )


def test_projection_dtos_are_immutable():
    facet = FacetSummaryProjection(
        facet_name="learning_rhythm",
        label="steady",
        availability="available",
        evidence_refs=("attempt:1",),
    )
    explanation = ExplanationSummaryProjection(
        overall_completeness_explanation="ok",
        provenance_refs=("study_attempts",),
    )
    provenance = ProjectionProvenance(
        twin_snapshot_ref="twin-abc",
        twin_id="twin-1",
        provenance_refs=("attempt:1",),
    )
    projection = StudentTwinProjection(
        student_id="42",
        twin_snapshot_ref="twin-abc",
        twin_id="twin-1",
        projection_version="t5.0",
        learner_profile_summary={"student_id": "42"},
        facet_summaries={"learning_rhythm": facet.to_canonical_dict()},
        completeness={"status": "partial"},
        explanation_summary=explanation,
        provenance=provenance,
        availability="available",
    )
    assert isinstance(projection.learner_profile_summary, MappingProxyType)
    assert isinstance(projection.facet_summaries, MappingProxyType)
    with pytest.raises((TypeError, AttributeError)):
        projection.student_id = "x"  # type: ignore[misc]
    with pytest.raises((TypeError, AttributeError)):
        projection.facet_summaries["x"] = {}  # type: ignore[index]


def test_project_exposes_allowed_fields_only():
    projector = StudentTwinProjector()
    snapshot = _sample_snapshot()
    explanation = _sample_explanation(snapshot)
    projection = projector.project(snapshot, explanation=explanation)

    assert isinstance(projection, StudentTwinProjection)
    assert projection.availability == AVAILABILITY_AVAILABLE
    assert projection.twin_id == "twin-42"
    assert projection.twin_snapshot_ref.startswith("twin-")
    assert projection.learner_profile_summary["preferred_session_minutes"] == 25.0
    assert "learning_rhythm" in projection.facet_summaries
    assert projection.facet_summaries["learning_rhythm"]["label"] == "steady"
    assert projection.facet_summaries["learning_rhythm"]["summary_note"] == (
        "regular mornings"
    )
    assert projection.completeness["status"] == "partial"
    assert projection.explanation_summary.overall_completeness_explanation == (
        "partial"
    )
    assert "attempt:1" in projection.provenance.provenance_refs
    assert "mission:9" in projection.provenance.provenance_refs
    assert "study_attempts" in projection.provenance.provenance_refs
    assert "sparse_predictions" in projection.limitations_codes
    assert "twin_facets_unavailable" in projection.limitations_codes
    # Internal Twin builder / Runtime A entities must not leak as objects.
    payload = projection.to_canonical_dict()
    assert "TwinSnapshotBuilder" not in serialize_canonical(payload)
    assert "db.session" not in serialize_canonical(payload)


def test_project_is_deterministic():
    projector = StudentTwinProjector()
    snapshot = _sample_snapshot()
    explanation = _sample_explanation(snapshot)
    left = projector.project(snapshot, explanation=explanation).serialize()
    right = projector.project(snapshot, explanation=explanation).serialize()
    assert left == right
    assert serialize_canonical(
        projector.project(snapshot).to_canonical_dict()
    ) == projector.project(snapshot).serialize()


def test_projection_port_implements_student_twin_port():
    port = StudentTwinProjectionPort()
    assert isinstance(port, StudentTwinPort)
    snapshot = _sample_snapshot()
    projection = port.serve_projection(
        snapshot, explanation=_sample_explanation(snapshot)
    )
    assert projection.student_id == "42"

    learner = port.get_learner_summary("42")
    readiness = port.get_readiness_summary("42")
    insights = port.get_learning_insights("42")
    assert learner is not None
    assert readiness is not None
    assert insights is not None
    assert learner["authority"] == AUTHORITY_DIGITAL_TWIN
    assert learner["preferences"]["preferred_session_minutes"] == 25.0
    assert "facet_summaries" in learner
    assert "provenance_refs" in learner
    assert readiness["exam_readiness"] is None
    assert readiness["readiness_score"] is None
    assert readiness["unavailable_reason"] == REASON_READINESS_PASS_THROUGH_DEFERRED
    assert insights["completed_sessions"] == ()
    assert insights["facet_summaries"]["consistency"]["label"] == "regular"
    assert insights["explanation_summary"]["evidence_coverage_summary"] == (
        "runtime_a refs present"
    )


def test_projection_port_unknown_student_returns_none():
    port = StudentTwinProjectionPort()
    assert port.get_learner_summary("missing") is None
    assert port.get_readiness_summary("missing") is None
    assert port.get_learning_insights("missing") is None


def test_projection_port_snapshot_provider_path():
    snapshot = _sample_snapshot(student_id="7")

    def provider(student_id: str) -> TwinSnapshot | None:
        return snapshot if student_id == "7" else None

    port = StudentTwinProjectionPort(snapshot_provider=provider)
    learner = port.get_learner_summary("7")
    assert learner is not None
    assert learner["twin_id"] == "twin-7"
    assert learner["student_id"] == "7"


def test_projection_port_flag_off_unavailable():
    port = StudentTwinProjectionPort(enabled=False)
    assert port.is_available() is False
    projection = port.get_projection("42")
    assert projection is not None
    assert projection.availability == AVAILABILITY_UNAVAILABLE
    assert projection.unavailable_reason == REASON_TWIN_FLAG_OFF


def test_port_opaque_dicts_are_deterministic():
    port = StudentTwinProjectionPort()
    snapshot = _sample_snapshot()
    port.serve_projection(snapshot, explanation=_sample_explanation(snapshot))
    left = serialize_canonical(port.get_learner_summary("42"))
    right = serialize_canonical(port.get_learner_summary("42"))
    assert left == right
    assert serialize_canonical(port.get_learning_insights("42")) == (
        serialize_canonical(port.get_learning_insights("42"))
    )


def test_di_helpers_respect_flag():
    assert build_student_twin_projector(enabled=False) is None
    assert build_student_twin_projection_port(enabled=False) is None
    projector = build_student_twin_projector(enabled=True)
    port = build_student_twin_projection_port(enabled=True, projector=projector)
    assert isinstance(projector, StudentTwinProjector)
    assert isinstance(port, StudentTwinProjectionPort)
    assert port.projector() is projector


def test_digital_twin_flag_defaults_off_and_wires_projection():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False
    composition, _ = build_production_experience(
        flags=flags,
        seed_demo_learners=False,
    )
    assert composition.student_twin_projector is None
    assert composition.student_twin_projection_port is None
    # Live Experience TwinPort remains prior adapter (no authority cutover).
    assert composition.twin.__class__.__name__ == "ExperienceTwinAdapter"

    on_flags = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    assert on_flags.ENABLE_DIGITAL_TWIN is True
    composition_on, _ = build_production_experience(
        flags=on_flags,
        seed_demo_learners=False,
    )
    assert composition_on.student_twin_projector is not None
    assert composition_on.student_twin_projection_port is not None
    assert composition_on.student_twin_projection_port.is_available()
    assert composition_on.twin.__class__.__name__ == "ExperienceTwinAdapter"
