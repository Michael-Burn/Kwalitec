"""Tests for database models."""

from __future__ import annotations

from datetime import date, timedelta


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, user):
        assert user.email == "test@kwalitec.example"
        assert user.is_active_user is True
        assert user.check_password("password123")
        assert not user.check_password("wrong-password")
        assert user.is_active is True
        assert user.id is not None

    def test_user_password_hashing(self, user):
        """Ensure password is stored as a hash, not plaintext."""
        assert user.password_hash != "password123"
        assert user.password_hash.startswith("scrypt:") or user.password_hash.startswith("pbkdf2:")

    def test_user_repr(self, user):
        assert "User" in repr(user)

    def test_load_user_valid(self, app, user):
        from app.models.user import load_user

        with app.app_context():
            loaded = load_user(str(user.id))
            assert loaded is not None
            assert loaded.id == user.id

    def test_load_user_invalid_id(self, app):
        from app.models.user import load_user

        with app.app_context():
            assert load_user("99999") is None
            assert load_user("not-a-number") is None


class TestMissionModel:
    """Tests for the Mission and MissionTask models."""

    def test_create_mission(self, db, user, subject):
        from app.models.mission import Mission

        m = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study Session",
        )
        db.session.add(m)
        db.session.commit()
        assert m.id is not None
        assert m.status == "Pending"
        assert "Mission" in repr(m)

    def test_mission_completion_percentage_empty(self, db, user, subject):
        from app.models.mission import Mission

        m = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Empty Mission",
        )
        db.session.add(m)
        db.session.commit()
        assert m.get_completion_percentage() == 100.0

    def test_mission_completion_percentage(self, mission):
        pct = mission.get_completion_percentage()
        assert pct == 0.0

    def test_mission_completion_percentage_half(self, db, mission):
        mission.tasks[0].completed = True
        db.session.commit()
        pct = mission.get_completion_percentage()
        assert pct == 50.0

    def test_mission_completion_percentage_all(self, db, mission):
        for t in mission.tasks:
            t.completed = True
        db.session.commit()
        pct = mission.get_completion_percentage()
        assert pct == 100.0

    def test_mission_task_repr(self, mission):
        assert "MissionTask" in repr(mission.tasks[0])


class TestStudyPlanModel:
    """Tests for the StudyPlan and WeekPlan models."""

    def test_create_study_plan(self, db, user):
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CM1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()
        assert sp.id is not None
        assert "StudyPlan" in repr(sp)
        assert sp.get_total_weeks() == 0
        assert sp.get_weeks_remaining() > 0

    def test_week_plan_is_current_week(self, db, user):
        from app.models.study_plan import StudyPlan, WeekPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="Test",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Ch 1",
            study_preference="Mixed",
            target_grade="A",
            active=True,
        )
        db.session.add(sp)
        db.session.flush()

        wp = WeekPlan(
            study_plan_id=sp.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()
        assert wp.is_current_week() is True
        assert wp.is_past() is False

    def test_week_plan_is_past(self, db, user):
        from app.models.study_plan import StudyPlan, WeekPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="Test",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Ch 1",
            study_preference="Mixed",
            target_grade="A",
            active=True,
        )
        db.session.add(sp)
        db.session.flush()

        wp = WeekPlan(
            study_plan_id=sp.id,
            week_number=1,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() - timedelta(days=3),
        )
        db.session.add(wp)
        db.session.commit()
        assert wp.is_current_week() is False
        assert wp.is_past() is True


class TestTopicProgressModel:
    """Tests for the TopicProgress model."""

    def test_create_topic_progress(self, topic_progress):
        assert topic_progress.id is not None
        assert topic_progress.mastery_score == 75.0
        assert topic_progress.current_stage == "Practising"
        assert topic_progress.revision_count == 3

    def test_topic_progress_repr(self, topic_progress):
        assert "TopicProgress" in repr(topic_progress)


class TestSubjectModel:
    """Tests for the Subject model."""

    def test_create_subject(self, db, user):
        from app.models.subject import Subject

        s = Subject(
            user_id=user.id,
            name="Mathematics",
            colour="#00ff00",
            active=True,
        )
        db.session.add(s)
        db.session.commit()
        assert s.id is not None
        assert s.name == "Mathematics"
        assert s.colour == "#00ff00"
        assert s.active is True