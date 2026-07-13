"""Discovery-driven curriculum parity tests (Capability 4.5).

Every on-disk syllabus under ``app/curriculum/data/`` must satisfy the same
product pipeline: import → study plan → topic selection → recommendation →
mission → dashboard → roadmap. Future IFoA papers inherit these checks
automatically when their JSON is added — no per-paper test edits required.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.curriculum.validator import validate_curriculum_v2
from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.curriculum_service import CurriculumService
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService


def _discovered_cases() -> list[tuple[str, str, str, str, str]]:
    """Return (exam_name, org, paper, version, first_topic_title) for every syllabus.

    ``exam_name`` uses the official provider / exam_code from the loaded JSON so
    it matches ``CurriculumService.import_curricula`` product naming (e.g.
    ``IFoA CS1``), not the filesystem directory casing (``IFOA``).
    """
    engine = CurriculumEngineService()
    cases: list[tuple[str, str, str, str, str]] = []
    for organisation, paper, versions in engine.list_supported_exams():
        version = max(versions)
        curriculum = engine.load_auto(organisation, paper, version)
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        assert topics, f"{organisation}/{paper}/{version} has no topics"
        first = topics[0]
        if hasattr(curriculum, "provider") and hasattr(curriculum, "exam_code"):
            exam_name = f"{curriculum.provider} {curriculum.exam_code}"
        else:
            exam_name = f"{curriculum.organisation} {curriculum.paper}"
        cases.append((exam_name, organisation, paper, version, first.title))
    return cases


DISCOVERED = _discovered_cases()
assert DISCOVERED, "Expected at least one on-disk curriculum"


def _create_plan(user_id: int, exam_name: str, version: str, topic_code: str = "1.1"):
    sp = StudyPlanService.create_study_plan(
        user_id=user_id,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=60,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="B",
        curriculum_version=version,
        curriculum_topic_code=topic_code,
    )
    wp = WeekPlan(
        study_plan_id=sp.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(wp)
    db.session.commit()
    return sp


@pytest.mark.parametrize(
    "exam_name,organisation,paper,version,first_topic_title",
    DISCOVERED,
    ids=[c[0] for c in DISCOVERED],
)
class TestDiscoveredCurriculumParity:
    """Parity contract for every discovered curriculum — not a hardcoded paper list."""

    def test_loads_validates_and_imports(
        self, ctx, db, exam_name, organisation, paper, version, first_topic_title
    ):
        engine = CurriculumEngineService()
        curriculum = engine.load_auto(organisation, paper, version)
        # V2 curricula expose sections; validate the hierarchical contract.
        if hasattr(curriculum, "sections"):
            validate_curriculum_v2(curriculum)
            assert len(curriculum.sections) >= 1
            assert sum(len(s.topics) for s in curriculum.sections) >= 1

        CurriculumService.import_curricula()
        row = Curriculum.query.filter_by(exam_name=exam_name, version=version).one()
        topics = CurriculumService.get_all_topics_ordered(row)
        assert len(topics) >= 1
        assert topics[0].name == first_topic_title

    def test_study_plan_binds_curriculum_and_progress(
        self, db, user, exam_name, organisation, paper, version, first_topic_title
    ):
        sp = _create_plan(user.id, exam_name, version)
        assert sp.curriculum_id is not None
        assert sp.curriculum.exam_name == exam_name
        topic_count = Topic.query.filter_by(curriculum_id=sp.curriculum_id).count()
        assert topic_count >= 1
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

    def test_mission_references_real_syllabus_topic(
        self, db, user, exam_name, organisation, paper, version, first_topic_title
    ):
        _create_plan(user.id, exam_name, version)
        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None

        class _Topic:
            name = first_topic_title

        natural_label = PlanningService._topic_study_label(_Topic())
        assert "1.1" in mission.title
        assert natural_label.lower() in mission.title.lower()
        assert "study learning" not in mission.title.lower()

        # Task copy must lead with the syllabus node, not a bare Core Reading stub.
        assert mission.tasks
        lead = mission.tasks[0].description.lower()
        assert natural_label.lower() in lead or "1.1" in lead
        assert not lead.startswith("read the core reading for today's section")

    def test_recommendation_references_real_syllabus_topic(
        self, db, user, exam_name, organisation, paper, version, first_topic_title
    ):
        _create_plan(user.id, exam_name, version)
        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert len(recs) >= 1

        class _Topic:
            name = first_topic_title

        natural_label = PlanningService._topic_study_label(_Topic())
        titles = " ".join(r["title"] for r in recs)
        assert (
            natural_label in titles
            or "1.1" in titles
            or first_topic_title in titles
        )
    def test_dashboard_and_roadmap_render(
        self,
        logged_in_client,
        db,
        user,
        exam_name,
        organisation,
        paper,
        version,
        first_topic_title,
    ):
        sp = _create_plan(user.id, exam_name, version)

        dash = logged_in_client.get("/dashboard/")
        assert dash.status_code == 200
        body = dash.data.lower()
        assert b"mission" in body or b"study" in body
        assert b"study learning" not in body

        roadmap = logged_in_client.get(f"/study-plan/{sp.id}")
        assert roadmap.status_code == 200
        # Official first topic title should appear on the curriculum roadmap.
        assert first_topic_title.encode("utf-8") in roadmap.data
