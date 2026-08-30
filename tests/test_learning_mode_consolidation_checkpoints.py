"""Learning Mode consolidation checkpoint regression tests.

Cadence bands, skip-and-reset, anti-repeat, distinct title/MES, determinism.
Distinct from Revision Mode post-syllabus consolidation rotation.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.student_twin.query import TopicKnowledgeFact
from app.extensions import db
from app.mission.routes import _apply_mission_topic_progress
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.planning_service import PlanningService

_TWIN_EK: dict[int, TopicKnowledgeFact] = {}


def _make_curriculum(
    exam_name: str, topic_names: list[str]
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topics: list[Topic] = []
    for index, name in enumerate(topic_names, start=1):
        topic = Topic(
            name=name,
            curriculum_id=curriculum.id,
            order=index,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        topics.append(topic)
    db.session.flush()
    return curriculum, topics


def _make_active_plan(
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
    days_until_exam: int = 180,
    watermark: int = 0,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=days_until_exam),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
        new_topics_since_consolidation_checkpoint=watermark,
    )
    db.session.add(plan)
    db.session.flush()
    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(week)
    db.session.commit()
    return plan


def _add_progress(
    user_id: int,
    topic: Topic,
    *,
    completed: bool,
    estimated_knowledge: float,
) -> TopicProgress:
    row = TopicProgress(
        user_id=user_id,
        topic_id=topic.id,
        completed=completed,
        current_stage=(
            TopicProgress.STAGE_COMPLETED
            if completed
            else TopicProgress.STAGE_LEARNING
        ),
    )
    db.session.add(row)
    if estimated_knowledge > 0:
        score = estimated_knowledge / 100.0
        _TWIN_EK[topic.id] = TopicKnowledgeFact(
            topic_id=f"TEST-{topic.id}",
            has_estimated_knowledge=True,
            estimated_knowledge=score,
            estimated_mastery=score,
            evidence_count=2,
            last_practised_at=None,
        )
    return row


@pytest.fixture(autouse=True)
def twin_ek_stub(monkeypatch):
    _TWIN_EK.clear()
    monkeypatch.setattr(
        "app.services.twin_cutover_service.topic_ek_by_orm_id",
        lambda **kwargs: dict(_TWIN_EK),
    )
    yield
    _TWIN_EK.clear()


@pytest.mark.usefixtures("ctx")
class TestConsolidationCadenceBands:
    """Exam-proximity cadence: >60 → 4; 30–60 → 3; <30 → 2."""

    @pytest.mark.parametrize(
        ("days_until_exam", "expected_cadence"),
        [
            (61, 4),
            (45, 3),
            (30, 3),
            (60, 3),
            (29, 2),
        ],
    )
    def test_cadence_helper(self, days_until_exam, expected_cadence):
        assert (
            PlanningService._consolidation_cadence(days_until_exam)
            == expected_cadence
        )

    @pytest.mark.parametrize(
        ("days_until_exam", "watermark", "should_consolidate"),
        [
            (61, 3, False),  # cadence 4; watermark 3 → CLT
            (61, 4, True),
            (45, 2, False),  # cadence 3
            (45, 3, True),
            (29, 1, False),  # cadence 2
            (29, 2, True),
        ],
    )
    def test_cadence_band_selection(
        self, db, user, days_until_exam, watermark, should_consolidate
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak Covered", "Current Learning Topic", "Future"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=days_until_exam,
            watermark=watermark,
        )
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=15.0
        )
        _add_progress(
            user.id, topics[1], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        if should_consolidate:
            assert selected.id == topics[0].id
            assert plan.new_topics_since_consolidation_checkpoint == 0
            assert plan.last_consolidation_topic_id == topics[0].id
        else:
            assert selected.id == topics[1].id


@pytest.mark.usefixtures("ctx")
class TestConsolidationSkipAndAntiRepeat:
    def test_skip_and_reset_when_no_weak_topic(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Strong Covered", "Current Learning Topic"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=3,
        )
        # Covered but Practising (mastery 75) — not weak.
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=75.0
        )
        _add_progress(
            user.id, topics[1], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == topics[1].id
        assert plan.new_topics_since_consolidation_checkpoint == 0
        assert plan.last_consolidation_topic_id is None

    def test_anti_repeat_picks_other_weak_topic(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak A", "Weak B", "Current Learning Topic"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=3,
        )
        plan.last_consolidation_topic_id = None  # set after first pick
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=10.0
        )
        _add_progress(
            user.id, topics[1], completed=True, estimated_knowledge=20.0
        )
        _add_progress(
            user.id, topics[2], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        first = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert first is not None
        assert first.id == topics[0].id  # lowest mastery
        assert plan.last_consolidation_topic_id == topics[0].id

        # Next checkpoint: watermark again at cadence; must not repeat Weak A.
        plan.new_topics_since_consolidation_checkpoint = 3
        db.session.add(plan)
        db.session.commit()

        second = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert second is not None
        assert second.id == topics[1].id
        assert plan.last_consolidation_topic_id == topics[1].id


@pytest.mark.usefixtures("ctx")
class TestConsolidationVisibilityAndDeterminism:
    def test_consolidation_mission_has_distinct_title_and_mes(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak Covered Topic", "Current Learning Topic", "Future"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=3,
        )
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=18.0
        )
        _add_progress(
            user.id, topics[1], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        mission = PlanningService._generate_mission_for_date(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert mission.title.startswith("Consolidate ")
        assert "Study " not in mission.title.split("—")[0]
        assert any(
            "consolidation checkpoint" in (t.description or "").lower()
            for t in mission.tasks
        )

        narrative = EducationalExplainabilityService.build_mission_narrative(
            mission_title=mission.title,
            mission_status=mission.status,
            exam_name=plan.exam_name,
            completed_topics=1,
            total_topics=3,
        )
        assert narrative is not None
        reason = narrative.reason_for_selection.lower()
        assert "consolidation checkpoint" in reason
        assert "checkpoint" in reason
        assert "revision mode" in reason
        assert "not" in reason

    def test_determinism_same_inputs_same_topic(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak A", "Weak B", "CLT"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=3,
        )
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=12.0
        )
        _add_progress(
            user.id, topics[1], completed=True, estimated_knowledge=25.0
        )
        _add_progress(
            user.id, topics[2], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        # Snapshot state before selection mutates watermark.
        plan.new_topics_since_consolidation_checkpoint = 3
        plan.last_consolidation_topic_id = None
        db.session.add(plan)
        db.session.commit()

        a = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        # Restore identical inputs and re-select.
        plan.new_topics_since_consolidation_checkpoint = 3
        plan.last_consolidation_topic_id = None
        db.session.add(plan)
        db.session.commit()
        b = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert a is not None and b is not None
        assert a.id == b.id == topics[0].id

    def test_clt_completion_increments_watermark(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Topic A", "Topic B"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=0,
        )
        _add_progress(
            user.id, topics[0], completed=False, estimated_knowledge=0.0
        )
        db.session.commit()

        _apply_mission_topic_progress(user.id, topics[0])
        db.session.refresh(plan)
        assert plan.new_topics_since_consolidation_checkpoint == 1

    def test_consolidation_revisit_does_not_increment_watermark(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak Covered", "CLT"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=0,
        )
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=15.0
        )
        db.session.commit()

        _apply_mission_topic_progress(user.id, topics[0])
        db.session.refresh(plan)
        assert plan.new_topics_since_consolidation_checkpoint == 0

    def test_acceptance_example_45_days_three_completions(self, db, user):
        """Exam 45 days out; after 3 new topics with one weak → consolidation."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Weak One", "Strong Two", "Strong Three", "Fourth CLT", "Fifth"],
        )
        plan = _make_active_plan(
            user.id,
            exam_name="IFoA CS1",
            curriculum=curriculum,
            days_until_exam=45,
            watermark=0,
        )
        # Simulate three CLT completions via watermark + covered progress.
        _add_progress(
            user.id, topics[0], completed=True, estimated_knowledge=22.0
        )
        _add_progress(
            user.id, topics[1], completed=True, estimated_knowledge=80.0
        )
        _add_progress(
            user.id, topics[2], completed=True, estimated_knowledge=85.0
        )
        _add_progress(
            user.id, topics[3], completed=False, estimated_knowledge=0.0
        )
        plan.new_topics_since_consolidation_checkpoint = 3
        db.session.add(plan)
        db.session.commit()

        mission = PlanningService._generate_mission_for_date(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert mission.title.startswith("Consolidate ")
        assert "Weak One" in mission.title or "weak one" in mission.title.lower()
        narrative = EducationalExplainabilityService.build_mission_narrative(
            mission_title=mission.title,
            exam_name=plan.exam_name,
        )
        assert narrative is not None
        assert "consolidation checkpoint" in narrative.reason_for_selection.lower()
