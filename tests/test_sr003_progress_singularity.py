"""SR-003 — Progress Singularity (SR-001A Phase P6).

Verify one Progress Engine: Accepted evidence advances coverage; Rejected
ignored; Twin absence supported; Twin estimates optional; coverage
deterministic; current topic unique; no duplicate progress writers; rollback.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    SessionEvidencePackage,
)
from app.application.progress_engine import (
    DuplicateProgressWriter,
    ProgressEngine,
    TwinEstimateInput,
    clear_progress_writer_registry,
    register_progress_writer,
    registered_progress_writer,
)
from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.progress import (
    ProgressModelSpec,
    ProgressTopicSpec,
)
from app.services.educational_evidence_authority import EducationalEvidenceAuthority

FIXED = datetime(2026, 7, 30, 14, 0, tzinfo=UTC)


def _flags(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_SESSION_SUBSTANCE": "1",
        "SR_EVIDENCE_GATE": "1",
        "SR_PROGRESS_SINGULARITY": "1",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _model() -> ProgressModelSpec:
    return ProgressModelSpec(
        curriculum_identity="CS1:test",
        topic_ids=("t1", "t2", "t3"),
        topics=(
            ProgressTopicSpec(
                topic_id="t1",
                topic_code="1.1",
                objective_ids=("lo-a", "lo-b"),
            ),
            ProgressTopicSpec(
                topic_id="t2",
                topic_code="1.2",
                objective_ids=("lo-c",),
                prerequisite_ids=("t1",),
            ),
            ProgressTopicSpec(
                topic_id="t3",
                topic_code="2.1",
                objective_ids=("lo-d",),
                prerequisite_ids=("t2",),
            ),
        ),
    )


def _topic_completed(topic_id: str, event_id: str = "e1") -> EducationalEventRecord:
    return EducationalEventRecord(
        event_id=event_id,
        event_type=EducationalEventType.TOPIC_COMPLETED,
        user_id=1,
        curriculum_identity="CS1:test",
        topic_id=topic_id,
    )


def _obs(
    type_id: RuntimeEvidenceType,
    *,
    student_id: str = "42",
    session_id: str = "lsr-sr003-1",
) -> CandidateObservation:
    return CandidateObservation.create(
        observation_id=f"obs-{type_id.value}",
        type_id=type_id,
        student_id=student_id,
        session_id=session_id,
        topic_id="t1",
        mission_instance_id="m-1",
        recorded_at=FIXED,
    )


def _validated_package(
    *types: RuntimeEvidenceType,
    finish: str = "yes",
) -> SessionEvidencePackage:
    observations = tuple(_obs(t) for t in types)
    package = SessionEvidencePackage.create(
        student_id="42",
        session_id="lsr-sr003-1",
        mission_instance_id="m-1",
        topic_id="t1",
        topic_title="Cash flows",
        curriculum_identity="CS1:test",
        learning_objectives=("Explain operating cash flow",),
        observations=observations,
        finish_review_verdict=finish,
        created_at=FIXED,
    )
    validation = EducationalEvidenceAuthority.validate_session_evidence_package(
        package
    )
    return package.with_validation(validation)


@pytest.fixture(autouse=True)
def _clear_writer_registry():
    clear_progress_writer_registry()
    yield
    clear_progress_writer_registry()


# ── Unit: derive / position / projections ─────────────────────────────────


def test_accepted_evidence_authorises_coverage_advance():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    package = _validated_package(RuntimeEvidenceType.PRACTICE_CORRECT)
    decision = engine.authorise_from_validation(
        package.validation, topic_id="t1", package_id=package.package_id
    )
    assert decision.may_advance is True
    assert decision.reason == "authority_accepted_coverage_advance"


def test_rejected_evidence_ignored():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    package = _validated_package(RuntimeEvidenceType.READING_COMPLETED)
    decision = engine.authorise_from_validation(package.validation, topic_id="t1")
    assert decision.may_advance is False
    assert decision.reason == "rejected_evidence_ignored"
    assert package.validation.disposition.value == "rejected"


def test_partial_finish_does_not_advance_progress():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    package = _validated_package(
        RuntimeEvidenceType.PRACTICE_CORRECT, finish="partially"
    )
    decision = engine.authorise_from_validation(package.validation, topic_id="t1")
    assert decision.may_advance is False
    assert decision.reason in {
        "authority_denied_progress_advance",
        "mission_completion_not_authorised",
    }


def test_coverage_deterministic_without_twin():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    events = (_topic_completed("t1"),)
    a = engine.derive_study_progress(_model(), events)
    b = engine.derive_study_progress(_model(), events)
    assert a.coverage_ratio == b.coverage_ratio == pytest.approx(1 / 3)
    assert a.completed_topic_ids == b.completed_topic_ids == ("t1",)
    assert a.current_topic_id == b.current_topic_id == "t2"
    assert a.twin_estimates_applied is False
    assert a.projection.projection_basis == "coverage_only"


def test_current_topic_unique():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    study = engine.derive_study_progress(_model(), (_topic_completed("t1"),))
    assert study.current_topic_id == "t2"
    assert study.position.current_topic_id == "t2"
    assert study.incomplete_topic_ids.count("t2") == 1
    assert study.current_topic_id not in study.completed_topic_ids


def test_completed_and_remaining_objectives():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    study = engine.derive_study_progress(_model(), (_topic_completed("t1"),))
    assert study.completed_objective_ids == ("lo-a", "lo-b")
    assert "lo-c" in study.remaining_objective_ids
    assert "lo-d" in study.remaining_objective_ids
    assert "lo-a" not in study.remaining_objective_ids


def test_twin_absence_supported():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    study = engine.derive_study_progress(
        _model(), (), twin_estimates=TwinEstimateInput.absent()
    )
    assert study.projection.twin_present is False
    assert study.projection.weak_topic_ids == ()
    assert study.twin_estimates_applied is False
    inputs = engine.mission_composition_inputs(study)
    assert inputs.twin_present is False
    assert inputs.current_topic_id == "t1"


def test_twin_estimates_optional_annotate_projection():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    twin = TwinEstimateInput(
        estimated_mastery={"t2": 0.2, "t3": 0.8},
        estimated_knowledge={"t2": 0.25, "t3": 0.75},
        overall_mastery=0.5,
        overall_knowledge=0.48,
        twin_status="active",
    )
    study = engine.derive_study_progress(
        _model(), (_topic_completed("t1"),), twin_estimates=twin
    )
    assert study.twin_estimates_applied is True
    assert study.projection.twin_present is True
    assert study.projection.projection_basis == "coverage_plus_optional_twin"
    assert study.projection.weak_topic_ids == ("t2",)
    assert study.coverage_ratio == pytest.approx(1 / 3)
    # Twin must not invent coverage
    assert study.completed_topic_ids == ("t1",)


def test_progress_engine_does_not_revalidate_evidence():
    """Progress Engine trusts Authority columns — never inspects payloads."""
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    decision = engine.authorise_coverage_advance(
        may_advance_progress=True,
        evidence_disposition="accepted",
        may_complete_mission=True,
        topic_id="t1",
    )
    assert decision.may_advance is True
    rejected = engine.authorise_coverage_advance(
        may_advance_progress=True,
        evidence_disposition="rejected",
        may_complete_mission=True,
        topic_id="t1",
    )
    assert rejected.may_advance is False
    assert rejected.reason == "rejected_evidence_ignored"


def test_no_duplicate_progress_writers():
    register_progress_writer("educational_runtime_engine")
    assert registered_progress_writer() == "educational_runtime_engine"
    register_progress_writer("educational_runtime_engine")  # idempotent
    with pytest.raises(DuplicateProgressWriter):
        register_progress_writer("legacy_topic_progress")


def test_mission_composition_inputs_expose_singular_topic():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    study = engine.derive_study_progress(_model(), (_topic_completed("t1"),))
    inputs = engine.mission_composition_inputs(study)
    opaque = inputs.to_opaque()
    assert opaque["authority"] == "progress_engine"
    assert opaque["current_topic_id"] == "t2"
    assert opaque["completed_topic_ids"] == ["t1"]
    assert opaque["remaining_topic_ids"] == ["t2", "t3"]


def test_syllabus_complete_clears_current_topic():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    events = (
        _topic_completed("t1", "e1"),
        _topic_completed("t2", "e2"),
        _topic_completed("t3", "e3"),
    )
    study = engine.derive_study_progress(_model(), events)
    assert study.syllabus_complete is True
    assert study.current_topic_id is None
    assert study.coverage_ratio == 1.0
    assert study.remaining_objective_ids == ()


# ── Acceptance: flag default OFF / enable / rollback ──────────────────────


def test_progress_singularity_flag_default_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.SR_PROGRESS_SINGULARITY is False


def test_progress_singularity_flag_enables():
    flags = resolve_v2_feature_flags(environ={"SR_PROGRESS_SINGULARITY": "1"})
    assert flags.SR_PROGRESS_SINGULARITY is True
    engine = ProgressEngine(flag_resolver=lambda: flags)
    assert engine.singularity_enabled() is True


def test_rollback_off_retains_derive_capability():
    """Flag OFF disables singularity claim; derive math remains available."""
    flags = resolve_v2_feature_flags(environ={"SR_PROGRESS_SINGULARITY": "0"})
    engine = ProgressEngine(flag_resolver=lambda: flags)
    assert engine.singularity_enabled() is False
    study = engine.derive_study_progress(_model(), (_topic_completed("t1"),))
    assert study.current_topic_id == "t2"
    assert study.authority == "progress_engine"


# ── Authority matrix ──────────────────────────────────────────────────────


def test_progress_engine_authority_id():
    assert ProgressEngine.AUTHORITY_ID == "progress_engine"


def test_study_progress_opaque_contract():
    engine = ProgressEngine(flag_resolver=lambda: _flags())
    opaque = engine.derive_study_progress(
        _model(), (_topic_completed("t1"),)
    ).to_opaque()
    assert opaque["authority"] == "progress_engine"
    assert "coverage_ratio" in opaque
    assert "position" in opaque
    assert "projection" in opaque
    assert "completed_objective_ids" in opaque
    assert "remaining_objective_ids" in opaque
    assert opaque["position"]["current_topic_id"] == "t2"
