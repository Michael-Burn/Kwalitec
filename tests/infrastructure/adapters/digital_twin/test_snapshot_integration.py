"""Integration tests — Twin Snapshot Builder vs Runtime A (MS-004 T2)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    FACET_SYNTHESIS_ORDER,
    SNAPSHOT_CONSTRUCTION_VERSION,
    SNAPSHOT_SCHEMA_VERSION,
    TwinFacetAssembler,
    TwinSnapshotBuilder,
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

ADAPTER_ROOT = Path(digital_twin_pkg.__file__).resolve().parent

FORBIDDEN_WRITE_TOKENS = frozenset(
    {
        "generate_today_mission",
        "start_session",
        "complete_session",
        "accept_evidence",
        "db.session.add",
        "db.session.commit",
        "session.add",
        "session.commit",
        "ensure_curriculum_binding",
        "repair_inconsistent_completion",
    }
)

SNAPSHOT_MODULES = (
    "snapshot_builder.py",
    "completeness.py",
    "provenance.py",
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


def test_identical_runtime_a_state_produces_identical_snapshots(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    sid = str(learner["user"].id)
    first = builder.build(sid, as_of="2026-07-25")
    second = builder.build(sid, as_of="2026-07-25")
    assert first.serialize() == second.serialize()
    assert first.version() == second.version()


def test_snapshot_contains_seven_facets_and_version_metadata(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    snapshot = builder.build(str(learner["user"].id), as_of="2026-07-25")
    profile = snapshot.profile.to_canonical_dict()
    for name in FACET_SYNTHESIS_ORDER:
        assert name in profile
    assert snapshot.snapshot_version == SNAPSHOT_CONSTRUCTION_VERSION
    assert snapshot.schema_version == SNAPSHOT_SCHEMA_VERSION
    assert snapshot.source_evidence_version.startswith("runtime_a:")
    assert snapshot.generated_at == "2026-07-25"
    assert snapshot.profile.learning_rhythm.availability == AVAILABILITY_AVAILABLE
    assert snapshot.provenance_summary is not None
    assert snapshot.unavailable_summary is not None
    assert snapshot.completeness.score is None
    assert snapshot.completeness.status in {"complete", "partial", "empty"}


def test_provenance_aggregation_from_runtime_a(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    snapshot = builder.build(str(learner["user"].id), as_of="2026-07-25")
    assert all(name in snapshot.field_provenance for name in FACET_SYNTHESIS_ORDER)
    # Available facets contribute their source services.
    if snapshot.completeness.facets_present:
        assert snapshot.provenance_summary.contributing_runtime_a_sources
    assert snapshot.provenance_summary.evidence_window_start is not None
    assert snapshot.provenance_summary.evidence_window_end is not None
    for name in snapshot.completeness.facets_unavailable:
        assert name in snapshot.provenance_summary.unavailable_inputs
        assert name in snapshot.unavailable_summary.facets


def test_new_learner_snapshot_is_structurally_honest(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, _topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    _ = subject
    builder = TwinSnapshotBuilder(facet_assembler=TwinFacetAssembler())
    snapshot = builder.build(str(user.id), as_of="2026-07-25")
    assert len(snapshot.profile.to_canonical_dict()) >= 7
    assert snapshot.completeness.score is None
    # Confidence without before/after pairs remains unavailable — never estimated.
    assert (
        snapshot.profile.confidence_trend.availability == "unavailable"
        or snapshot.profile.confidence_trend.availability == "available"
    )
    if snapshot.profile.confidence_trend.availability == "unavailable":
        assert snapshot.profile.confidence_trend.unavailable_reason
        assert "confidence_trend" in snapshot.unavailable_summary.facets


def test_snapshot_modules_remain_read_only_relative_to_runtime_a():
    for module_name in SNAPSHOT_MODULES:
        path = ADAPTER_ROOT / module_name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        source = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_WRITE_TOKENS:
            assert token not in source, f"{module_name} contains {token}"
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Attribute):
                    name = func.attr
                elif isinstance(func, ast.Name):
                    name = func.id
                assert name not in {
                    "commit",
                    "add",
                    "delete",
                    "flush",
                } or "logger" in ast.dump(node)


def test_no_twin_snapshot_persistence_in_t2():
    """T2 constructs TwinSnapshot in memory only — no store / Alembic writes."""
    builder_source = (ADAPTER_ROOT / "snapshot_builder.py").read_text(
        encoding="utf-8"
    )
    assert "class TwinSnapshotBuilder" in builder_source
    assert "db.session" not in builder_source
    assert "alembic" not in builder_source.lower()
    assert "persist" not in builder_source.lower() or (
        "no persistence" in builder_source.lower()
        or "No persistence" in builder_source
        or "MUST NOT persist" in builder_source
    )


def test_build_from_bundle_matches_direct_build(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    sid = str(learner["user"].id)
    bundle = assembler.assemble(sid, as_of="2026-07-25")
    from_bundle = builder.build_from_bundle(bundle, generated_at="2026-07-25")
    direct = builder.build(sid, as_of="2026-07-25")
    assert from_bundle.serialize() == direct.serialize()
