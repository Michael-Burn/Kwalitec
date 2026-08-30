"""ADR-027 Phase 2 Stage 3 — Runtime C Estimated Knowledge dual-path suite.

Proves:
- Flag OFF: get_estimated_knowledge_inputs keeps the Stage 2 stub (no Twin EK).
- Flag ON: topics carry explicit estimated_knowledge (0-1) from LearnerTwinQueryPort.
- Study Progress (completed / completed_topic_ids) is identical across flag states
  for the same enrolment events — Twin EK never mints completion.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_runtime_engine import EducationalRuntimeEngineService
from app.application.student_twin.query import TopicKnowledgeFact
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)


def _set_cutover(monkeypatch, enabled: bool) -> None:
    value = "1" if enabled else "0"
    monkeypatch.setenv("KWALITEC_ADR027_PHASE2_TWIN_CUTOVER", value)
    import app.application.config.v2_flags as flags_mod

    flags_mod.V2_FEATURE_FLAGS = resolve_v2_feature_flags()


def _fact(topic_id: str, *, ek: float | None) -> TopicKnowledgeFact:
    has = ek is not None
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=has,
        estimated_knowledge=ek,
        estimated_mastery=ek,
        evidence_count=2 if has else 0,
        last_practised_at=None,
    )


class _FakeTwinQuery:
    def __init__(self, by_topic: dict[str, TopicKnowledgeFact]) -> None:
        self._by_topic = by_topic

    def topic_knowledge(self, *, user_id, subject_code, topic_id):
        return self._by_topic.get(
            topic_id,
            _fact(topic_id, ek=None),
        )

    def knowledge_snapshot(self, *, user_id, subject_code):
        from app.application.student_twin.query import LearnerKnowledgeSnapshot

        topics = tuple(self._by_topic.values())
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=None,
            overall_estimated_knowledge=None,
            topics=topics,
        )


@pytest.fixture
def runtime_ek_fixture(ctx, monkeypatch):
    user = make_user("stage3-ek@example.com")
    subject = publish_subject("S3EK")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 30),
    )
    runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )
    # After one completion, topic_ids length is 2 and one is completed.
    ek_off = runtime.get_estimated_knowledge_inputs(
        user_id=user.id, subject_code=subject
    )
    topic_ids = list(ek_off.topic_ids)
    assert len(topic_ids) == 2
    completed = set(ek_off.completed_topic_ids)
    assert len(completed) == 1
    covered_id = next(iter(completed))
    other_id = next(t for t in topic_ids if t not in completed)

    fake = _FakeTwinQuery(
        {
            other_id: _fact(other_id, ek=0.73),
            # Covered topic deliberately has no Twin EK.
            covered_id: _fact(covered_id, ek=None),
        }
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.learner_twin_query",
        lambda: fake,
    )
    return {
        "user": user,
        "subject": subject,
        "runtime": runtime,
        "topic_ids": topic_ids,
        "covered_id": covered_id,
        "other_id": other_id,
        "completed": completed,
    }


def test_runtime_c_ek_stub_when_cutover_off(runtime_ek_fixture, monkeypatch):
    _set_cutover(monkeypatch, False)
    fx = runtime_ek_fixture
    ek = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    assert set(ek.completed_topic_ids) == fx["completed"]
    for topic in ek.topics:
        assert topic["has_estimated_knowledge"] is False
        assert topic["estimated_knowledge"] is None
        assert topic["mastery_score"] is None
        assert topic["completed"] is (topic["topic_id"] in fx["completed"])


def test_runtime_c_ek_twin_backed_when_cutover_on(runtime_ek_fixture, monkeypatch):
    _set_cutover(monkeypatch, True)
    fx = runtime_ek_fixture
    ek = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    by_id = {t["topic_id"]: t for t in ek.topics}

    other = by_id[fx["other_id"]]
    assert other["has_estimated_knowledge"] is True
    assert other["estimated_knowledge"] == pytest.approx(0.73)
    assert other["mastery_score"] == pytest.approx(73.0)
    assert other["completed"] is False

    covered = by_id[fx["covered_id"]]
    assert covered["completed"] is True
    assert covered["has_estimated_knowledge"] is False
    assert covered["estimated_knowledge"] is None
    assert covered["mastery_score"] is None


def test_runtime_c_study_progress_unaffected_by_cutover_flag(
    runtime_ek_fixture, monkeypatch
):
    fx = runtime_ek_fixture
    _set_cutover(monkeypatch, False)
    off = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    _set_cutover(monkeypatch, True)
    on = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    assert off.completed_topic_ids == on.completed_topic_ids
    assert off.topic_ids == on.topic_ids
    off_completed = {t["topic_id"]: t["completed"] for t in off.topics}
    on_completed = {t["topic_id"]: t["completed"] for t in on.topics}
    assert off_completed == on_completed


def test_stage3_modules_forbid_content_imports():
    paths = [
        REPO_ROOT / "app" / "presentation" / "stack_c_sandbox.py",
        REPO_ROOT
        / "app"
        / "presentation"
        / "student_digital_twin"
        / "routes.py",
        REPO_ROOT
        / "tests"
        / "application"
        / "student_twin"
        / "test_phase2_stage3_runtime_c_ek.py",
        REPO_ROOT
        / "tests"
        / "application"
        / "student_twin"
        / "test_phase2_stage3_founder_surfaces.py",
    ]
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                lowered = mod.replace("\\", "/")
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == []
