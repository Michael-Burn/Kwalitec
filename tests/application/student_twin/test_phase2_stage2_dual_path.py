"""ADR-027 Phase 2 Stage 4 permanent Twin cutover suite.

Proves that Stack A readers use Twin Estimated Knowledge, Stack A no longer
persists EK, Study Progress remains independent, and D2 permanently enforces
zero writes to retired TopicProgress EK columns.
"""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.application.student_twin.daily_loop_codec import encode_daily_loop_twin
from app.application.student_twin.drift_detector import DriftDetector
from app.application.student_twin.query import TopicKnowledgeFact
from app.extensions import db
from app.models.topic_progress import TopicProgress
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.analytics_service import AnalyticsService
from app.services.readiness_service import ReadinessService
from tests.application.student_twin.helpers import make_engine, success_events

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
        evidence_count=3 if has else 0,
        last_practised_at=None,
    )


@pytest.fixture
def permanent_cutover_fixture(ctx, user, curriculum, monkeypatch):
    """Study Progress rows plus canonical Twin EK facts."""
    _, topics = curriculum
    for topic in topics:
        topic.parent_topic_id = None
    db.session.commit()

    t_weak, t_strong, t_covered = topics[0], topics[1], topics[2]
    weak_row = TopicProgress(
        user_id=user.id,
        topic_id=t_weak.id,
        completed=False,
        revision_count=2,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    strong_row = TopicProgress(
        user_id=user.id,
        topic_id=t_strong.id,
        completed=False,
        revision_count=3,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    covered_no_ek = TopicProgress(
        user_id=user.id,
        topic_id=t_covered.id,
        completed=True,
        revision_count=0,
        current_stage=TopicProgress.STAGE_COMPLETED,
    )
    db.session.add_all([weak_row, strong_row, covered_no_ek])
    db.session.commit()

    twin_by_orm = {
        t_weak.id: _fact("CS1-A-T01", ek=0.92),
        t_strong.id: _fact("CS1-A-T02", ek=0.15),
    }

    monkeypatch.setattr(
        "app.services.twin_cutover_service.topic_ek_by_orm_id",
        lambda **kwargs: dict(twin_by_orm),
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.twin_fact_for_orm_topic",
        lambda *, topic, **kwargs: (
            twin_by_orm.get(topic.id) if topic is not None else None
        ),
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.subject_code_for_user",
        lambda user_id: "CS1",
    )
    monkeypatch.setattr(
        ReadinessService,
        "_leaf_topics_for_user",
        staticmethod(lambda user_id, read_only=False: list(topics)),
    )

    return SimpleNamespace(
        user=user,
        weak=t_weak,
        strong=t_strong,
        covered=t_covered,
        weak_row=weak_row,
        strong_row=strong_row,
        covered_row=covered_no_ek,
        topics=topics,
    )


@pytest.mark.usefixtures("ctx")
def test_stack_a_update_returns_progress_without_writing_ek(user, curriculum):
    _, topics = curriculum
    topic = topics[0]
    progress = TopicProgress(
        user_id=user.id,
        topic_id=topic.id,
        completed=False,
        revision_count=1,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    db.session.add(progress)
    db.session.commit()

    updated = AdaptiveLearningService.update_mastery_after_attempt(
        user.id, topic.id
    )
    db.session.refresh(progress)

    assert updated.id == progress.id
    assert progress.completed is False
    assert progress.has_estimated_knowledge is False


@pytest.mark.usefixtures("ctx")
def test_stack_c_mastery_write_remains_retired():
    from app.application.student_digital_twin.persistence import (
        TwinPersistenceService,
    )
    from app.domain.student_digital_twin.mastery import (
        MasteryMap,
        MasteryRecord,
        MasteryTrend,
    )
    from app.domain.student_digital_twin.student import Student
    from app.domain.student_digital_twin.student_digital_twin import (
        StudentDigitalTwin,
    )
    from app.models.student_digital_twin import (
        SdtMasteryRecord,
        SdtStudentDigitalTwin,
    )

    now = datetime.now()
    twin_row = SdtStudentDigitalTwin(
        twin_id="twin-cutover-c",
        student_id="student-cutover-c",
        display_name="Cutover",
        created_at=now,
        updated_at=now,
    )
    db.session.add(twin_row)
    db.session.flush()
    existing = SdtMasteryRecord(
        mastery_id="m-keep",
        twin_id="twin-cutover-c",
        concept_id="concept-a",
        concept_title="Concept A",
        mastery_score=0.42,
        confidence=0.5,
        trend="stable",
        evidence_count=2,
        supporting_evidence_json="[]",
        reason="baseline",
        last_updated=now,
    )
    db.session.add(existing)
    db.session.commit()

    domain_twin = StudentDigitalTwin.create(
        twin_id="twin-cutover-c",
        student=Student(
            student_id="student-cutover-c", display_name="Cutover"
        ),
        created_at=now,
    )
    domain_twin = domain_twin.with_inferences(
        mastery=MasteryMap(
            records=(
                MasteryRecord(
                    mastery_id="m-new",
                    twin_id="twin-cutover-c",
                    concept_id="concept-b",
                    concept_title="Concept B",
                    mastery_score=0.99,
                    confidence=0.9,
                    trend=MasteryTrend.IMPROVING,
                    evidence_count=5,
                    supporting_evidence=(),
                    reason="sandbox",
                    last_updated=now,
                ),
            )
        ),
        knowledge_gaps=(),
        recommendations=(),
        predictions=(),
        updated_at=now,
    )

    TwinPersistenceService().replace_inferences(domain_twin)
    db.session.commit()

    rows = SdtMasteryRecord.query.filter_by(twin_id="twin-cutover-c").all()
    assert len(rows) == 1
    assert rows[0].mastery_id == "m-keep"
    assert rows[0].mastery_score == pytest.approx(0.42)


@pytest.mark.usefixtures("ctx")
def test_readiness_weakest_topics_uses_twin(permanent_cutover_fixture):
    fx = permanent_cutover_fixture
    weak = ReadinessService.get_weakest_topics(fx.user.id, limit=5)
    scores = {row["topic_id"]: row["mastery_score"] for row in weak}
    assert scores[fx.strong.id] == pytest.approx(15.0)
    assert scores[fx.weak.id] == pytest.approx(92.0)
    assert fx.covered.id not in scores


@pytest.mark.usefixtures("ctx")
def test_readiness_covered_without_twin_evidence_has_no_ek(
    permanent_cutover_fixture,
):
    fx = permanent_cutover_fixture
    metrics = ReadinessService._study_progress_metrics(fx.user.id)
    assert metrics["topics_completed"] >= 1
    assert metrics["avg_estimated_knowledge"] == pytest.approx(
        (92.0 + 15.0) / 2.0
    )
    assert fx.covered_row.has_estimated_knowledge is False


@pytest.mark.usefixtures("ctx")
def test_adaptive_weak_topics_uses_twin(permanent_cutover_fixture):
    fx = permanent_cutover_fixture
    weak = AdaptiveLearningService.get_weak_topics(
        fx.user.id, threshold=60.0
    )
    weak_ids = [progress.topic_id for progress in weak]
    assert fx.strong.id in weak_ids
    assert fx.weak.id not in weak_ids


@pytest.mark.usefixtures("ctx")
def test_analytics_average_mastery_uses_twin(
    permanent_cutover_fixture, monkeypatch
):
    fx = permanent_cutover_fixture
    monkeypatch.setattr(
        AnalyticsService,
        "_leaf_topic_ids",
        staticmethod(lambda: [fx.weak.id, fx.strong.id, fx.covered.id]),
    )
    result = AnalyticsService.get_mastery_over_time(fx.user.id, weeks=1)
    assert result[0]["average_mastery"] == pytest.approx(
        (92.0 + 15.0) / 2.0
    )


@pytest.mark.usefixtures("ctx")
def test_study_progress_remains_independent(permanent_cutover_fixture):
    row = permanent_cutover_fixture.covered_row
    assert row.completed is True
    row.completed = False
    db.session.commit()
    db.session.refresh(row)
    assert row.completed is False
    row.completed = True
    db.session.commit()
    db.session.refresh(row)
    assert row.completed is True


def test_d2_permanently_enforces_zero_retired_writes():
    report = DriftDetector().check_single_writer_sentry()
    assert report.mode == "enforce"
    assert report.cutover_active is True
    assert report.ok
    assert report.retired_writes == ()


def test_stage4_modules_forbid_content_imports():
    paths = [
        REPO_ROOT / "app" / "application" / "student_twin" / "cutover.py",
        Path(__file__),
    ]
    offenders: list[str] = []
    for path in paths:
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


def test_seeded_twin_document_roundtrip_helper():
    engine = make_engine()
    twin = engine.create_twin("1", twin_id="t1", subject_code="CS1")
    twin = engine.ingest_many(
        twin, success_events(2, topic_id="CS1-A-T01", prefix="s2")
    )
    document = encode_daily_loop_twin(twin)
    assert "CS1-A-T01" in document["estimated_knowledge"]
