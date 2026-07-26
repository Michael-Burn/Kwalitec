"""Integration tests — Twin Facet Synthesis vs Runtime A (MS-004 T1)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_SYNTHESIS_ORDER,
    TwinFacetAssembler,
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

SYNTHESIS_MODULES = (
    "assembler.py",
    "builders.py",
    "evidence.py",
    "provenance.py",
    "validation.py",
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


def test_identical_runtime_a_state_produces_identical_facets(learner):
    assembler = TwinFacetAssembler()
    sid = str(learner["user"].id)
    first = assembler.assemble(sid, as_of="2026-07-25")
    second = assembler.assemble(sid, as_of="2026-07-25")
    assert first.serialize() == second.serialize()
    assert first.profile.serialize() == second.profile.serialize()


def test_runtime_a_evidence_surfaces_in_facets(learner):
    assembler = TwinFacetAssembler()
    bundle = assembler.assemble(str(learner["user"].id), as_of="2026-07-25")
    assert bundle.profile.learning_rhythm.availability == AVAILABILITY_AVAILABLE
    assert bundle.profile.learning_rhythm.typical_session_minutes == 40.0
    attempt_ref = f"attempt:{learner['attempt'].id}"
    assert attempt_ref in bundle.profile.learning_rhythm.evidence_refs
    assert bundle.profile.consistency.availability == AVAILABILITY_AVAILABLE
    mission_ref = f"mission:{learner['mission'].id}"
    assert mission_ref in bundle.profile.consistency.evidence_refs
    assert bundle.profile.persistence.availability == AVAILABILITY_AVAILABLE
    assert bundle.profile.revision_behaviour.availability == AVAILABILITY_AVAILABLE
    assert "total_revision_count=2" in bundle.profile.revision_behaviour.revision_note
    assert bundle.profile.confidence_trend.availability == AVAILABILITY_AVAILABLE
    assert "low->medium" in bundle.profile.confidence_trend.trend_note
    assert all(
        name in bundle.field_provenance for name in FACET_SYNTHESIS_ORDER
    )


def test_new_learner_empty_available_facets(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, _topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    _ = subject
    assembler = TwinFacetAssembler()
    bundle = assembler.assemble(str(user.id), as_of="2026-07-25")
    assert bundle.profile.learning_rhythm.availability == AVAILABILITY_AVAILABLE
    assert bundle.profile.learning_rhythm.label == "none"
    assert bundle.profile.consistency.availability == AVAILABILITY_AVAILABLE
    assert bundle.profile.confidence_trend.availability == AVAILABILITY_UNAVAILABLE


def test_synthesis_modules_remain_read_only_relative_to_runtime_a():
    for module_name in SYNTHESIS_MODULES:
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


def test_no_twin_snapshot_persistence_in_t1():
    """T1 must not introduce snapshot store / Alembic writes."""
    assembler_source = (ADAPTER_ROOT / "assembler.py").read_text(encoding="utf-8")
    assert "TwinSnapshot(" not in assembler_source or (
        "empty_twin_snapshot" in assembler_source
    )
    # Facet assembler returns TwinFacetBundle, not TwinSnapshot.
    assert "class TwinFacetBundle" in assembler_source
    assert "db.session" not in assembler_source
