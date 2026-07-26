"""Integration / boundary / read-only tests — Experience Projection (MS-004 T5)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.adapters.digital_twin import (
    AUTHORITY_DIGITAL_TWIN,
    AVAILABILITY_AVAILABLE,
    StudentTwinProjectionPort,
    TwinExplainabilityService,
    TwinFacetAssembler,
    TwinSnapshotBuilder,
    build_student_twin_projection_port,
    build_student_twin_projector,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)

TWIN_ROOT = Path(digital_twin_pkg.__file__).resolve().parent
PROJECTION_PATH = TWIN_ROOT / "experience_projection.py"

FORBIDDEN_WRITE_TOKENS = (
    "db.session.commit",
    "db.session.add",
    "generate_today_mission",
    "start_session",
    "complete_session",
    "accept_evidence",
    "alembic",
)

FORBIDDEN_SYNTHESIS_CALLS = (
    "TwinSnapshotBuilder(",
    "TwinFacetAssembler(",
    "build_twin_snapshot_builder(",
    "build_twin_facet_assembler(",
)

FORBIDDEN_ADAPTIVE_AUTHORITY = (
    "ENABLE_ADAPTIVE_AUTHORITY",
    "KWALITEC_ADAPTIVE_AUTHORITY",
    "AdaptiveExperiencePortRouter",
)


@pytest.fixture
def learner(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "completed"
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    attempt.duration_minutes = 40
    attempt.confidence_before = "low"
    attempt.confidence_after = "medium"
    progress = _make_topic_progress(user.id, topics[0].id)
    progress.revision_count = 2
    db.session.commit()
    return {
        "user": user,
        "subject": subject,
        "curriculum": curriculum,
        "topics": topics,
        "plan": plan,
        "mission": mission,
        "attempt": attempt,
        "progress": progress,
    }


def test_end_to_end_snapshot_to_experience_projection(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    explain = TwinExplainabilityService()
    projector = build_student_twin_projector(enabled=True)
    port = build_student_twin_projection_port(enabled=True, projector=projector)
    assert port is not None and projector is not None

    sid = str(learner["user"].id)
    snapshot = builder.build(sid, as_of="2026-07-25T12:00:00")
    explanation = explain.explain_snapshot(snapshot)
    projection = projector.project(snapshot, explanation=explanation)

    assert projection.student_id == sid
    assert projection.availability == AVAILABILITY_AVAILABLE
    assert projection.twin_snapshot_ref.startswith("twin-")
    assert projection.completeness
    assert projection.facet_summaries
    assert "learning_rhythm" in projection.facet_summaries

    port.serve_projection(snapshot, explanation=explanation)
    assert isinstance(port, StudentTwinPort)
    learner_summary = port.get_learner_summary(sid)
    readiness = port.get_readiness_summary(sid)
    insights = port.get_learning_insights(sid)
    assert learner_summary is not None
    assert readiness is not None
    assert insights is not None
    assert learner_summary["authority"] == AUTHORITY_DIGITAL_TWIN
    assert readiness["exam_readiness"] is None
    assert readiness["readiness_score"] is None
    assert "facet_summaries" in insights
    assert "explanation_summary" in insights
    assert "provenance_refs" in insights

    again = projector.project(snapshot, explanation=explanation)
    assert again.serialize() == projection.serialize()
    assert serialize_canonical(port.get_learner_summary(sid)) == (
        serialize_canonical(learner_summary)
    )


def test_projection_consistency_across_port_methods(learner):
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler()
    ).build(str(learner["user"].id), as_of="2026-07-25T12:00:00")
    port = StudentTwinProjectionPort()
    projection = port.serve_projection(snapshot)
    sid = projection.student_id
    learner_summary = port.get_learner_summary(sid)
    insights = port.get_learning_insights(sid)
    readiness = port.get_readiness_summary(sid)
    assert learner_summary is not None and insights is not None
    assert readiness is not None
    assert learner_summary["twin_snapshot_ref"] == projection.twin_snapshot_ref
    assert insights["twin_snapshot_ref"] == projection.twin_snapshot_ref
    assert readiness["twin_snapshot_ref"] == projection.twin_snapshot_ref
    assert learner_summary["facet_summaries"] == insights["facet_summaries"]


def test_experience_projection_source_is_read_only():
    text = PROJECTION_PATH.read_text(encoding="utf-8")
    for token in FORBIDDEN_WRITE_TOKENS:
        assert token not in text
    for token in FORBIDDEN_SYNTHESIS_CALLS:
        assert token not in text
    for token in FORBIDDEN_ADAPTIVE_AUTHORITY:
        assert token not in text


def test_experience_projection_does_not_import_experience_or_adaptive_authority():
    tree = ast.parse(
        PROJECTION_PATH.read_text(encoding="utf-8"),
        filename=str(PROJECTION_PATH),
    )
    forbidden_modules = (
        "app.infrastructure.adapters.student_experience",
        "app.infrastructure.adapters.adaptive_engine",
        "app.models",
        "flask",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for forbidden in forbidden_modules:
                assert not module.startswith(forbidden)
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in forbidden_modules:
                    assert not alias.name.startswith(forbidden)


def test_composition_wires_projection_without_authority_cutover(monkeypatch):
    assert build_student_twin_projector(enabled=False) is None
    assert build_student_twin_projection_port(enabled=False) is None
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    composition, _ = build_production_experience()
    assert composition.student_twin_projector.projector_id == (
        "student_twin_projector"
    )
    assert composition.student_twin_projection_port.component_id == (
        "student_twin_projection_port"
    )
    assert composition.student_twin_projection_port.projector() is (
        composition.student_twin_projector
    )
    # Experience UX StudentTwinPort remains prior adapter — projection only.
    assert composition.twin.__class__.__name__ == "ExperienceTwinAdapter"
    assert composition.student_twin_projection_port is not composition.twin


def test_runtime_a_remains_authoritative_no_invented_readiness(learner):
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler()
    ).build(str(learner["user"].id), as_of="2026-07-25T12:00:00")
    port = StudentTwinProjectionPort()
    port.serve_projection(snapshot)
    readiness = port.get_readiness_summary(str(learner["user"].id))
    assert readiness is not None
    # Twin projection must not invent readiness scores from facet synthesis.
    assert readiness["exam_readiness"] is None
    assert readiness["readiness_score"] is None
    assert readiness["authority"] == AUTHORITY_DIGITAL_TWIN
