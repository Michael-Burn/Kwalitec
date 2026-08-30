"""ADR-027 Phase 2 Stage 2 dual-path behaviour preservation suite.

Proves:
- Flag OFF: readers/writers match Stack A/C behaviour (pre-cutover path).
- Flag ON: Stack A/C EK writes skipped; readers source Twin via Query Port.
- Study Progress (completed) is unaffected in both flag states.
- Covered-without-Twin-evidence shows no EK when flag ON.
"""

from __future__ import annotations

import ast
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
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
        evidence_count=3 if has else 0,
        last_practised_at=None,
    )


@pytest.fixture
def dual_path_fixture(ctx, user, curriculum, monkeypatch):
    """Stack A progress rows + Twin EK map stubs for dual-path proofs."""
    _, topics = curriculum
    # Flatten hierarchy so all three topics behave as leaves for readiness.
    for topic in topics:
        topic.parent_topic_id = None
    db.session.commit()

    t_weak, t_strong, t_covered = topics[0], topics[1], topics[2]

    weak_row = TopicProgress(
        user_id=user.id,
        topic_id=t_weak.id,
        completed=False,
        mastery_score=25.0,
        average_accuracy=25.0,
        revision_count=2,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    strong_row = TopicProgress(
        user_id=user.id,
        topic_id=t_strong.id,
        completed=False,
        mastery_score=88.0,
        average_accuracy=88.0,
        revision_count=3,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    covered_no_ek = TopicProgress(
        user_id=user.id,
        topic_id=t_covered.id,
        completed=True,
        mastery_score=0.0,
        average_accuracy=None,
        revision_count=0,
        current_stage=TopicProgress.STAGE_COMPLETED,
    )
    db.session.add_all([weak_row, strong_row, covered_no_ek])
    db.session.commit()

    twin_by_orm = {
        t_weak.id: _fact("CS1-A-T01", ek=0.92),
        t_strong.id: _fact("CS1-A-T02", ek=0.15),
    }

    def _fake_topic_ek_by_orm_id(*, user_id, subject_code=None, topics=None):
        return dict(twin_by_orm)

    def _fake_twin_fact(*, user_id, topic, subject_code=None):
        if topic is None:
            return None
        return twin_by_orm.get(topic.id)

    monkeypatch.setattr(
        "app.services.twin_cutover_service.topic_ek_by_orm_id",
        _fake_topic_ek_by_orm_id,
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.twin_fact_for_orm_topic",
        _fake_twin_fact,
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
        twin_by_orm=twin_by_orm,
    )


# --- Flag default / resolver -------------------------------------------------


def test_phase2_cutover_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ADR027_PHASE2_TWIN_CUTOVER is False


def test_phase2_cutover_flag_not_inherited_from_commercial_loop():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_COMMERCIAL_LOOP": "1",
            "KWALITEC_V2_SOLE_RUNTIME": "1",
        }
    )
    assert flags.ADR027_PHASE2_TWIN_CUTOVER is False


def test_phase2_cutover_absent_from_render_yaml():
    text = (REPO_ROOT / "render.yaml").read_text(encoding="utf-8")
    assert "KWALITEC_ADR027_PHASE2_TWIN_CUTOVER" not in text
    assert "ADR027_PHASE2_TWIN_CUTOVER" not in text


# --- Writer skip (flag ON) ---------------------------------------------------


@pytest.mark.usefixtures("ctx")
def test_stack_a_ek_write_skipped_when_cutover_on(
    user, curriculum, monkeypatch
):
    _set_cutover(monkeypatch, True)
    _, topics = curriculum
    topic = topics[0]
    progress = TopicProgress(
        user_id=user.id,
        topic_id=topic.id,
        completed=False,
        mastery_score=41.0,
        average_accuracy=41.0,
        revision_count=1,
        current_stage=TopicProgress.STAGE_PRACTISING,
    )
    db.session.add(progress)
    db.session.commit()

    # Force authorised observations so the legacy path would write if unguarded.
    monkeypatch.setattr(
        "app.services.educational_evidence_authority"
        ".EducationalEvidenceAuthority.collect_authorised_accuracy_observations",
        staticmethod(lambda attempts: [(90.0, date.today())]),
    )

    before_score = progress.mastery_score
    before_acc = progress.average_accuracy
    before_completed = progress.completed

    AdaptiveLearningService.update_mastery_after_attempt(user.id, topic.id)
    db.session.refresh(progress)

    assert progress.mastery_score == before_score
    assert progress.average_accuracy == before_acc
    assert progress.completed is before_completed


@pytest.mark.usefixtures("ctx")
def test_stack_a_ek_write_runs_when_cutover_off(
    user, curriculum, monkeypatch
):
    _set_cutover(monkeypatch, False)
    _, topics = curriculum
    topic = topics[0]
    progress = TopicProgress(
        user_id=user.id,
        topic_id=topic.id,
        completed=False,
        mastery_score=10.0,
        average_accuracy=None,
        revision_count=0,
        current_stage=TopicProgress.STAGE_NOT_STARTED,
    )
    db.session.add(progress)
    db.session.commit()

    monkeypatch.setattr(
        "app.services.educational_evidence_authority"
        ".EducationalEvidenceAuthority.collect_authorised_accuracy_observations",
        staticmethod(lambda attempts: [(80.0, date.today())]),
    )
    monkeypatch.setattr(
        "app.services.educational_evidence_authority"
        ".EducationalEvidenceAuthority.may_assign_high_mastery_stage",
        staticmethod(lambda count: True),
    )

    AdaptiveLearningService.update_mastery_after_attempt(user.id, topic.id)
    db.session.refresh(progress)
    assert progress.average_accuracy is not None
    assert progress.mastery_score > 10.0


@pytest.mark.usefixtures("ctx")
def test_stack_c_mastery_write_skipped_when_cutover_on(monkeypatch):
    _set_cutover(monkeypatch, True)
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
                    reason="would-write",
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


# --- Reader dual-path --------------------------------------------------------


@pytest.mark.usefixtures("ctx")
def test_readiness_weakest_topics_flag_off_uses_stack_a(
    dual_path_fixture, monkeypatch
):
    _set_cutover(monkeypatch, False)
    fx = dual_path_fixture
    weak = ReadinessService.get_weakest_topics(fx.user.id, limit=5)
    scores = {row["topic_id"]: row["mastery_score"] for row in weak}
    assert scores[fx.weak.id] == pytest.approx(25.0)
    assert scores[fx.strong.id] == pytest.approx(88.0)
    assert fx.covered.id not in scores


@pytest.mark.usefixtures("ctx")
def test_readiness_weakest_topics_flag_on_uses_twin(
    dual_path_fixture, monkeypatch
):
    _set_cutover(monkeypatch, True)
    fx = dual_path_fixture
    weak = ReadinessService.get_weakest_topics(fx.user.id, limit=5)
    scores = {row["topic_id"]: row["mastery_score"] for row in weak}
    assert scores[fx.strong.id] == pytest.approx(15.0)
    assert scores[fx.weak.id] == pytest.approx(92.0)
    assert fx.covered.id not in scores


@pytest.mark.usefixtures("ctx")
def test_readiness_metrics_covered_without_twin_ek_flag_on(
    dual_path_fixture, monkeypatch
):
    _set_cutover(monkeypatch, True)
    fx = dual_path_fixture
    metrics = ReadinessService._study_progress_metrics(fx.user.id)
    assert metrics["topics_completed"] >= 1
    assert metrics["avg_estimated_knowledge"] == pytest.approx((92.0 + 15.0) / 2.0)


@pytest.mark.usefixtures("ctx")
def test_readiness_metrics_flag_off_identical_to_stack_a(
    dual_path_fixture, monkeypatch
):
    _set_cutover(monkeypatch, False)
    fx = dual_path_fixture
    first = ReadinessService._study_progress_metrics(fx.user.id)
    second = ReadinessService._study_progress_metrics(fx.user.id)
    assert first == second
    assert first["avg_estimated_knowledge"] == pytest.approx((25.0 + 88.0) / 2.0)


@pytest.mark.usefixtures("ctx")
def test_adaptive_get_weak_topics_dual_path(dual_path_fixture, monkeypatch):
    fx = dual_path_fixture

    _set_cutover(monkeypatch, False)
    off = AdaptiveLearningService.get_weak_topics(fx.user.id, threshold=60.0)
    off_ids = [p.topic_id for p in off]
    assert fx.weak.id in off_ids
    assert fx.strong.id not in off_ids

    _set_cutover(monkeypatch, True)
    on = AdaptiveLearningService.get_weak_topics(fx.user.id, threshold=60.0)
    on_ids = [p.topic_id for p in on]
    assert fx.strong.id in on_ids
    assert fx.weak.id not in on_ids


@pytest.mark.usefixtures("ctx")
def test_analytics_avg_mastery_dual_path(dual_path_fixture, monkeypatch):
    fx = dual_path_fixture
    monkeypatch.setattr(
        AnalyticsService,
        "_leaf_topic_ids",
        staticmethod(lambda: [fx.weak.id, fx.strong.id, fx.covered.id]),
    )

    _set_cutover(monkeypatch, False)
    off = AnalyticsService.get_mastery_over_time(fx.user.id, weeks=1)
    assert off[0]["average_mastery"] == pytest.approx((25.0 + 88.0) / 2.0)

    _set_cutover(monkeypatch, True)
    on = AnalyticsService.get_mastery_over_time(fx.user.id, weeks=1)
    assert on[0]["average_mastery"] == pytest.approx((92.0 + 15.0) / 2.0)


# --- Study Progress invariant -----------------------------------------------


@pytest.mark.usefixtures("ctx")
def test_study_progress_unaffected_both_flag_states(
    dual_path_fixture, monkeypatch
):
    fx = dual_path_fixture
    for enabled in (False, True):
        _set_cutover(monkeypatch, enabled)
        db.session.refresh(fx.covered_row)
        assert fx.covered_row.completed is True
        fx.covered_row.completed = False
        db.session.commit()
        db.session.refresh(fx.covered_row)
        assert fx.covered_row.completed is False
        fx.covered_row.completed = True
        db.session.commit()
        db.session.refresh(fx.covered_row)
        assert fx.covered_row.completed is True


@pytest.mark.usefixtures("ctx")
def test_update_mastery_never_writes_completed_either_flag(
    user, curriculum, monkeypatch
):
    _, topics = curriculum
    topic = topics[0]
    for enabled in (False, True):
        _set_cutover(monkeypatch, enabled)
        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic.id
        ).first()
        if progress is None:
            progress = TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=False,
                mastery_score=0.0,
                revision_count=0,
                current_stage=TopicProgress.STAGE_NOT_STARTED,
            )
            db.session.add(progress)
            db.session.commit()
        progress.completed = False
        db.session.commit()
        AdaptiveLearningService.update_mastery_after_attempt(user.id, topic.id)
        db.session.refresh(progress)
        assert progress.completed is False


# --- D2 enforcement toggle --------------------------------------------------


def test_d2_toggle_inventory_vs_enforce():
    off = DriftDetector().check_single_writer_sentry(cutover_active=False)
    on = DriftDetector().check_single_writer_sentry(cutover_active=True)
    assert off.mode == "inventory" and off.ok
    assert on.mode == "enforce" and on.ok
    assert on.missing_guards == ()


# --- Content-path AST -------------------------------------------------------


def test_stage2_new_modules_forbid_content_imports():
    paths = [
        REPO_ROOT / "app" / "application" / "student_twin" / "cutover.py",
        REPO_ROOT
        / "tests"
        / "application"
        / "student_twin"
        / "test_phase2_stage2_dual_path.py",
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
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == []


def test_seeded_twin_document_roundtrip_helper():
    engine = make_engine()
    twin = engine.create_twin("1", twin_id="t1", subject_code="CS1")
    twin = engine.ingest_many(
        twin, success_events(2, topic_id="CS1-A-T01", prefix="s2")
    )
    doc = encode_daily_loop_twin(twin)
    assert "CS1-A-T01" in doc["estimated_knowledge"]
