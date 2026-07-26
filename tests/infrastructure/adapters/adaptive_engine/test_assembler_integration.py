"""Integration tests — Adaptive Input Assembler vs Runtime A (MS-003 A1)."""

from __future__ import annotations

import ast
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

import pytest

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
from app.infrastructure.adapters.adaptive_engine import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    INPUT_FIELD_NAMES,
    REASON_NO_ACTIVE_PLAN,
    AdaptiveInputAssembler,
)
from app.infrastructure.adapters.adaptive_engine.collectors import (
    EvidenceCollector,
    MissionCollector,
    StudentGoalsCollector,
    TopicProgressCollector,
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

ADAPTER_ROOT = Path(adaptive_engine_pkg.__file__).resolve().parent

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
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    progress = _make_topic_progress(user.id, topics[0].id)
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


def test_identical_runtime_a_state_produces_identical_bundles(learner):
    assembler = AdaptiveInputAssembler()
    sid = str(learner["user"].id)
    as_of = date.today().isoformat()
    first = assembler.assemble(sid, as_of=as_of)
    second = assembler.assemble(sid, as_of=as_of)
    assert first.serialize() == second.serialize()
    assert first.student_id == sid
    assert first.as_of == as_of


def test_assembled_bundle_reflects_runtime_a_facts(learner):
    assembler = AdaptiveInputAssembler()
    bundle = assembler.assemble(
        str(learner["user"].id),
        as_of=date.today().isoformat(),
    )
    assert dict(bundle.field_provenance["evidence"])["availability"] == (
        AVAILABILITY_AVAILABLE
    )
    assert int(bundle.evidence["attempt_count"]) >= 1
    assert any(
        row["attempt_id"] == str(learner["attempt"].id)
        for row in bundle.evidence["attempts"]
    )
    assert any(
        row["topic_id"] == str(learner["topics"][0].id)
        for row in bundle.topic_progress
    )
    assert any(
        row["mission_id"] == str(learner["mission"].id)
        for row in bundle.mission["history"]
    )
    assert bundle.student_goals["study_plan_id"] == str(learner["plan"].id)
    assert bundle.curriculum["curriculum_id"] == str(learner["curriculum"].id)
    assert bundle.lifecycle_stage in {"learning", "revision", "not_started"}


def test_missing_plan_marks_goals_and_curriculum_unavailable(app, ctx):
    user = _make_user()
    assembler = AdaptiveInputAssembler()
    bundle = assembler.assemble(str(user.id), as_of="2026-07-25")
    goals = dict(bundle.field_provenance["student_goals"])
    curriculum = dict(bundle.field_provenance["curriculum"])
    assert goals["availability"] == AVAILABILITY_UNAVAILABLE
    assert goals["unavailable_reason"] == REASON_NO_ACTIVE_PLAN
    assert curriculum["availability"] == AVAILABILITY_UNAVAILABLE
    assert dict(bundle.student_goals) == {}
    assert dict(bundle.curriculum) == {}
    # Evidence / attempts remain available (honest empty or present).
    assert dict(bundle.field_provenance["evidence"])["availability"] == (
        AVAILABILITY_AVAILABLE
    )


def test_every_field_exposes_provenance(learner):
    bundle = AdaptiveInputAssembler().assemble(
        str(learner["user"].id),
        as_of="2026-07-25",
    )
    for name in INPUT_FIELD_NAMES:
        entry = dict(bundle.field_provenance[name])
        assert entry["source_service"]
        assert entry["source_entity"]
        assert entry["collected_at"] == "2026-07-25"
        assert entry["availability"] in {
            AVAILABILITY_AVAILABLE,
            AVAILABILITY_UNAVAILABLE,
        }
        if entry["availability"] == AVAILABILITY_UNAVAILABLE:
            assert entry["unavailable_reason"]


def test_assembler_modules_forbid_runtime_a_writes():
    """Static contract: A1 assembler package must not write Runtime A."""
    forbidden_attrs = {
        "generate_today_mission",
        "start_session",
        "complete_session",
        "accept_evidence",
        "ensure_curriculum_binding",
        "repair_inconsistent_completion",
        "get_user_active_plan",
    }
    for path in ADAPTER_ROOT.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_WRITE_TOKENS:
            assert forbidden not in text, f"{path.name} must not contain {forbidden}"
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in forbidden_attrs, (
                    f"{path.name} calls forbidden write API {node.func.attr}"
                )


def test_no_runtime_a_writes_during_assemble(learner):
    assembler = AdaptiveInputAssembler()
    sid = str(learner["user"].id)
    with mock.patch("app.extensions.db.session.commit") as commit:
        with mock.patch("app.extensions.db.session.add") as add:
            bundle = assembler.assemble(sid, as_of=date.today().isoformat())
    assert bundle.student_id == sid
    commit.assert_not_called()
    add.assert_not_called()


def test_collectors_do_not_use_mission_repair_path(learner):
    """Mission collector must query ORM directly (no status repair writes)."""
    collector = MissionCollector()
    with mock.patch(
        "app.services.mission_service.MissionService.repair_inconsistent_completion"
    ) as repair:
        result = collector.collect(
            learner["user"].id,
            as_of=date.today().isoformat(),
            context={"study_plan_id": learner["plan"].id},
        )
    assert result.available is True
    repair.assert_not_called()


def test_evidence_and_progress_collectors_read_sql(learner):
    evidence = EvidenceCollector().collect(learner["user"].id)
    progress = TopicProgressCollector().collect(learner["user"].id)
    goals = StudentGoalsCollector().collect(
        learner["user"].id,
        context={"active_plan": learner["plan"]},
    )
    assert evidence.available is True
    assert progress.available is True
    assert goals.available is True
    assert goals.payload["exam_date"] == (
        (date.today() + timedelta(days=180)).isoformat()
    )
