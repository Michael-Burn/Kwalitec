"""Pytest fixtures and configuration for Kwalitec tests."""

from __future__ import annotations

import os
import tempfile
from datetime import date, timedelta

import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create a session-scoped Flask application with a temp database."""
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.environ["APP_ENV"] = "testing"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

    from app import config

    original_uri = config._database_uri

    def _test_uri() -> str:
        return f"sqlite:///{db_path}"

    config._database_uri = _test_uri

    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SERVER_NAME="localhost.localdomain",
    )

    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.session.remove()
        _db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)
    config._database_uri = original_uri


@pytest.fixture(scope="function")
def db(app):
    """Truncate all tables between tests for isolation."""
    with app.app_context():
        meta = _db.metadata
        for table in reversed(meta.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
    return _db


@pytest.fixture(scope="function")
def ctx(app, db):
    """Push an app context that stays alive for the duration of the test."""
    ctx = app.app_context()
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Provide a Flask CLI test runner."""
    return app.test_cli_runner()


# ═══ Fixture helpers (run inside a pushed ctx) ═══════════════════════════════


def _make_user():
    from app.models.user import User

    u = User(email="test@kwalitec.example", is_active_user=True)
    u.set_password("password123")
    _db.session.add(u)
    _db.session.commit()
    return u


def _make_subject(uid):
    from app.models.subject import Subject

    s = Subject(user_id=uid, name="Test Subject", colour="#ff0000", active=True)
    _db.session.add(s)
    _db.session.commit()
    return s


def _make_curriculum():
    from app.models.curriculum import Curriculum, Topic

    c = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
    _db.session.add(c)
    _db.session.flush()

    t1 = Topic(
        name="Probability", curriculum_id=c.id, order=1,
        recommended_minutes=60, active=True,
    )
    t2 = Topic(
        name="Statistics", curriculum_id=c.id, order=2,
        recommended_minutes=60, active=True,
    )
    t3 = Topic(
        name="Distributions", curriculum_id=c.id,
        parent_topic_id=t2.id, order=1,
        recommended_minutes=30, active=True,
    )
    _db.session.add_all([t1, t2, t3])
    _db.session.commit()
    return c, [t1, t2, t3]


def _make_study_plan(uid):
    from app.models.study_plan import StudyPlan

    sp = StudyPlan(
        user_id=uid,
        exam_name="IFoA CM1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
    )
    _db.session.add(sp)
    _db.session.commit()
    return sp


def _make_mission(uid, sid):
    from app.models.mission import Mission, MissionTask

    m = Mission(user_id=uid, subject_id=sid, mission_date=date.today(),
                 title="Test Mission", status="Pending")
    _db.session.add(m)
    _db.session.commit()
    _db.session.refresh(m)

    t1 = MissionTask(mission_id=m.id, title="Task 1", description="First task", order=0)
    t2 = MissionTask(mission_id=m.id, title="Task 2", description="Second task", order=1)
    _db.session.add_all([t1, t2])
    _db.session.commit()
    _db.session.refresh(m)
    return m


def _make_study_attempt(uid, tid, mid):
    from app.models.learning import StudyAttempt

    sa = StudyAttempt(
        user_id=uid, topic_id=tid, mission_id=mid,
        study_date=date.today(), questions_attempted=10,
        questions_correct=8,
        confidence_before="Low", confidence_after="Medium",
    )
    _db.session.add(sa)
    _db.session.commit()
    return sa


def _make_topic_progress(uid, tid):
    from app.models.topic_progress import TopicProgress

    tp = TopicProgress(
        user_id=uid, topic_id=tid, mastery_score=75.0,
        current_stage=TopicProgress.STAGE_PRACTISING,
        revision_count=3,
        next_review_date=date.today() + timedelta(days=7),
        completed=False,
    )
    _db.session.add(tp)
    _db.session.commit()
    return tp


# ═══ Fixtures (ctx ensures app context is pushed) ═══════════════════════════


@pytest.fixture(scope="function")
def user(ctx):
    return _make_user()


@pytest.fixture(scope="function")
def logged_in_client(client, ctx, user):
    client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=True,
    )
    return client


@pytest.fixture(scope="function")
def subject(ctx, user):
    return _make_subject(user.id)


@pytest.fixture(scope="function")
def study_plan(ctx, user):
    return _make_study_plan(user.id)


@pytest.fixture(scope="function")
def curriculum(ctx):
    return _make_curriculum()


@pytest.fixture(scope="function")
def mission(ctx, user, subject):
    return _make_mission(user.id, subject.id)


@pytest.fixture(scope="function")
def study_attempt(ctx, user, curriculum, mission):
    _, topics = curriculum
    return _make_study_attempt(user.id, topics[0].id, mission.id)


@pytest.fixture(scope="function")
def topic_progress(ctx, user, curriculum):
    _, topics = curriculum
    return _make_topic_progress(user.id, topics[0].id)