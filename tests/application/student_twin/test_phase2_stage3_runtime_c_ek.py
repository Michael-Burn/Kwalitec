"""ADR-027 Phase 2 Stage 4 Runtime C permanent Twin EK suite.

Runtime C always reads Estimated Knowledge from LearnerTwinQueryPort. Study
Progress remains separate, and covered topics without Twin evidence have no EK.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from app.application.educational_runtime_engine import EducationalRuntimeEngineService
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
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
        return self._by_topic.get(topic_id, _fact(topic_id, ek=None))

    def knowledge_snapshot(self, *, user_id, subject_code):
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=None,
            overall_estimated_knowledge=None,
            topics=tuple(self._by_topic.values()),
        )


@pytest.fixture
def runtime_ek_fixture(ctx, monkeypatch):
    user = make_user("stage4-ek@example.com")
    subject = publish_subject("S4EK")
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

    initial = runtime.get_estimated_knowledge_inputs(
        user_id=user.id, subject_code=subject
    )
    topic_ids = list(initial.topic_ids)
    assert len(topic_ids) == 2
    completed = set(initial.completed_topic_ids)
    assert len(completed) == 1
    covered_id = next(iter(completed))
    other_id = next(topic_id for topic_id in topic_ids if topic_id not in completed)

    fake = _FakeTwinQuery(
        {
            other_id: _fact(other_id, ek=0.73),
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


def test_runtime_c_ek_is_always_twin_backed(runtime_ek_fixture):
    fx = runtime_ek_fixture
    result = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    by_id = {topic["topic_id"]: topic for topic in result.topics}

    other = by_id[fx["other_id"]]
    assert other["has_estimated_knowledge"] is True
    assert other["estimated_knowledge"] == pytest.approx(0.73)
    assert other["mastery_score"] == pytest.approx(73.0)
    assert other["completed"] is False


def test_runtime_c_covered_without_twin_evidence_has_no_ek(
    runtime_ek_fixture,
):
    fx = runtime_ek_fixture
    result = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    by_id = {topic["topic_id"]: topic for topic in result.topics}

    covered = by_id[fx["covered_id"]]
    assert covered["completed"] is True
    assert covered["has_estimated_knowledge"] is False
    assert covered["estimated_knowledge"] is None
    assert covered["mastery_score"] is None
    assert set(result.completed_topic_ids) == fx["completed"]


def test_runtime_c_study_progress_is_independent_of_twin_ek(
    runtime_ek_fixture,
):
    fx = runtime_ek_fixture
    result = fx["runtime"].get_estimated_knowledge_inputs(
        user_id=fx["user"].id, subject_code=fx["subject"]
    )
    assert result.topic_ids == tuple(fx["topic_ids"])
    assert set(result.completed_topic_ids) == fx["completed"]
    completed_by_topic = {
        topic["topic_id"]: topic["completed"] for topic in result.topics
    }
    assert completed_by_topic[fx["covered_id"]] is True
    assert completed_by_topic[fx["other_id"]] is False


def test_stage4_runtime_modules_forbid_content_imports():
    paths = [
        REPO_ROOT / "app" / "presentation" / "stack_c_sandbox.py",
        REPO_ROOT
        / "app"
        / "presentation"
        / "student_digital_twin"
        / "routes.py",
        Path(__file__),
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
                for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
                    if fragment in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == []
