"""Internal Alpha enablement tests (Capability 4.2)."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.mission import Mission, MissionTask
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.services.curriculum_service import CurriculumService
from app.services.mission_service import MissionService
from app.services.planning_service import DayType, PlanningService


class TestMissionCompletion:
    def test_complete_mission_persists_tasks_and_status(self, db, user):
        subject = Subject(user_id=user.id, name="CS1")
        db.session.add(subject)
        db.session.flush()
        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study Generalised Linear Models — Monday, Jul 13",
            status="Pending",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=True))
        mission.tasks.append(MissionTask(title="Practice", order=1, completed=True))
        db.session.add(mission)
        db.session.commit()

        updated = MissionService.complete_mission(mission.id, user.id)
        db.session.refresh(updated)

        assert updated.status == "Completed"
        assert all(task.completed for task in updated.tasks)
        assert updated.get_completion_percentage() == 100.0

    def test_complete_mission_rejects_incomplete_tasks(self, db, user):
        subject = Subject(user_id=user.id, name="CS1")
        db.session.add(subject)
        db.session.flush()
        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study Generalised Linear Models — Monday, Jul 13",
            status="In Progress",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=True))
        mission.tasks.append(MissionTask(title="Practice", order=1, completed=False))
        db.session.add(mission)
        db.session.commit()

        with pytest.raises(ValueError, match="Complete all mission points"):
            MissionService.complete_mission(mission.id, user.id)

        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert mission.tasks[1].completed is False

    def test_repair_reopens_completed_mission_with_incomplete_tasks(self, db, user):
        subject = Subject(user_id=user.id, name="CS1")
        db.session.add(subject)
        db.session.flush()
        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study topic — Monday, Jul 13",
            status="Completed",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=True))
        mission.tasks.append(MissionTask(title="Practice", order=1, completed=False))
        db.session.add(mission)
        db.session.commit()

        repaired = MissionService.get_today_mission(user.id)
        assert repaired is not None
        assert repaired.status == "In Progress"
        assert repaired.tasks[1].completed is False

    def test_complete_mission_endpoint_updates_progress(self, app, ctx, user):
        CurriculumService.import_curricula()
        from app.models.curriculum import Curriculum, Topic
        from app.models.study_plan import StudyPlan

        curriculum = Curriculum.query.filter_by(exam_name="IFoA CS1").first()
        assert curriculum is not None
        topic = (
            Topic.query.filter_by(curriculum_id=curriculum.id)
            .order_by(Topic.order)
            .first()
        )
        assert topic is not None

        subject = Subject(user_id=user.id, name="CS1")
        db.session.add(subject)
        db.session.flush()

        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="Apr 2027",
            exam_date=date.today() + timedelta(days=120),
            target_grade="Pass",
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            preferred_session_minutes=60,
            active=True,
            curriculum_id=curriculum.id,
            curriculum_version="2026",
        )
        db.session.add(plan)
        db.session.flush()

        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title=f"Study {topic.name} — Monday, Jul 13",
            status="In Progress",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=True))
        db.session.add(mission)
        db.session.commit()

        client = app.test_client()
        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        resp = client.post(
            f"/missions/{mission.id}/complete",
            json={},
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["success"] is True
        assert payload["mission"]["status"] == "Completed"

        db.session.refresh(mission)
        assert mission.status == "Completed"
        assert all(t.completed for t in mission.tasks)

        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic.id
        ).first()
        assert progress is not None
        assert progress.completed is True

    def test_complete_mission_endpoint_rejects_incomplete_tasks(self, app, ctx, user):
        subject = Subject(user_id=user.id, name="CS1")
        db.session.add(subject)
        db.session.flush()
        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study topic — Monday, Jul 13",
            status="In Progress",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=False))
        mission.tasks.append(MissionTask(title="Practice", order=1, completed=False))
        db.session.add(mission)
        db.session.commit()

        client = app.test_client()
        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        resp = client.post(
            f"/missions/{mission.id}/complete",
            json={},
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 400
        payload = resp.get_json()
        assert payload["success"] is False
        assert "mission points" in payload["error"].lower()

        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert not any(t.completed for t in mission.tasks)


class TestMissionWording:
    def test_topic_study_label_strips_imperative_verbs(self):
        class _T:
            name = "Understand and use generalised linear models"

        label = PlanningService._topic_study_label(_T())
        assert label == "Generalised Linear Models"
        assert "Understand" not in label

    def test_mixed_task_copy_is_natural(self):
        class _T:
            name = "Understand and use generalised linear models"

        tasks = PlanningService._generate_weekday_tasks(
            study_minutes=180,
            current_stage="Chapter",
            study_preference="Mixed",
            topic=_T(),
        )
        assert tasks[0]["title"] == "Study Generalised Linear Models"
        assert "Study and practice Understand" not in tasks[0]["description"]
        assert "Core Reading" in tasks[0]["description"]

    def test_mission_title_reads_naturally(self):
        class _T:
            name = "Understand and use generalised linear models"

        title = PlanningService._generate_mission_title(
            DayType.WEEKDAY, date(2026, 7, 13), topic=_T()
        )
        assert title.startswith("Study Generalised Linear Models")
        assert "Understand and use" not in title


class TestCreateTestUserCommand:
    def test_creates_additional_user(self, runner, user, ctx):
        result = runner.invoke(
            args=[
                "create-test-user",
                "--name",
                "Alpha Friend",
                "--email",
                "friend@kwalitec.example",
                "--password",
                "securepassword123",
            ]
        )
        assert result.exit_code == 0
        assert "Test user created successfully" in result.output
        created = User.query.filter_by(email="friend@kwalitec.example").first()
        assert created is not None
        assert created.check_password("securepassword123") is True

    def test_rejects_duplicate_email(self, runner, user, ctx):
        result = runner.invoke(
            args=[
                "create-test-user",
                "--name",
                "Duplicate",
                "--email",
                user.email,
                "--password",
                "securepassword123",
            ]
        )
        assert result.exit_code != 0
        assert "already exists" in result.output


class TestCb2Curriculum:
    def test_cb2_loads_and_validates(self):
        from app.curriculum.loader import load_curriculum_v2
        from app.curriculum.validator import validate_curriculum_v2

        curriculum = load_curriculum_v2("ifoa", "cb2", "2026")
        validate_curriculum_v2(curriculum)
        assert curriculum.exam_code == "CB2"
        assert curriculum.exam_name == "Business Economics"
        assert len(curriculum.sections) == 3
        assert sum(s.exam_weight for s in curriculum.sections) == 100.0
        assert sum(len(s.topics) for s in curriculum.sections) == 21

    def test_cb2_imports_and_supports_study_plan(self, db, user):
        CurriculumService.import_curricula()
        from app.models.curriculum import Curriculum
        from app.models.study_plan import StudyPlan
        from app.services.examination_catalogue import parse_exam_name

        curriculum = Curriculum.query.filter_by(exam_name="IFoA CB2").first()
        assert curriculum is not None
        sections = CurriculumService.get_sections(curriculum)
        assert len(sections) == 3
        topics = CurriculumService.get_all_topics_ordered(curriculum)
        assert len(topics) == 21

        org, paper = parse_exam_name("IFoA CB2")
        assert org == "IFoA"
        assert paper == "CB2"

        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CB2",
            exam_sitting="Apr 2027",
            exam_date=date.today() + timedelta(days=180),
            target_grade="Pass",
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Reading First",
            preferred_session_minutes=60,
            active=True,
            curriculum_id=curriculum.id,
            curriculum_version="2026",
        )
        db.session.add(plan)
        db.session.commit()

        next_topic = CurriculumService.get_next_incomplete_topic(user.id, curriculum)
        assert next_topic is not None


class TestCm1Curriculum:
    def test_cm1_loads_and_validates(self):
        from app.curriculum.loader import load_curriculum_v2
        from app.curriculum.validator import validate_curriculum_v2

        curriculum = load_curriculum_v2("ifoa", "cm1", "2026")
        validate_curriculum_v2(curriculum)
        assert curriculum.exam_code == "CM1"
        assert curriculum.exam_name == "Actuarial Mathematics for Modelling"
        assert len(curriculum.sections) == 4
        assert sum(s.exam_weight for s in curriculum.sections) == 100.0
        assert sum(len(s.topics) for s in curriculum.sections) == 21

    def test_cm1_imports_and_supports_study_plan(self, db, user):
        CurriculumService.import_curricula()
        from app.models.curriculum import Curriculum
        from app.models.study_plan import StudyPlan
        from app.services.examination_catalogue import parse_exam_name

        curriculum = Curriculum.query.filter_by(exam_name="IFoA CM1").first()
        assert curriculum is not None
        sections = CurriculumService.get_sections(curriculum)
        assert len(sections) == 4
        topics = CurriculumService.get_all_topics_ordered(curriculum)
        assert len(topics) == 21

        org, paper = parse_exam_name("IFoA CM1")
        assert org == "IFoA"
        assert paper == "CM1"

        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CM1",
            exam_sitting="Apr 2027",
            exam_date=date.today() + timedelta(days=180),
            target_grade="Pass",
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Reading First",
            preferred_session_minutes=60,
            active=True,
            curriculum_id=curriculum.id,
            curriculum_version="2026",
        )
        db.session.add(plan)
        db.session.commit()

        next_topic = CurriculumService.get_next_incomplete_topic(user.id, curriculum)
        assert next_topic is not None
