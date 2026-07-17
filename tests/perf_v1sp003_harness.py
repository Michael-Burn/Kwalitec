"""V1SP-003 performance profiling harness.

Measures wall-clock time and SQLAlchemy query counts for Version 1 hot paths.
Used for baseline / after comparison — not a soft CI budget suite.
"""

from __future__ import annotations

import json
import statistics
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)
from app.services.vision_journal_service import VisionJournalService


@dataclass
class PathMetric:
    path: str
    iterations: int
    median_ms: float
    mean_ms: float
    min_ms: float
    max_ms: float
    median_queries: float
    mean_queries: float
    min_queries: int
    max_queries: int


@contextmanager
def count_queries():
    """Count SQL statements issued inside the block."""
    statements: list[str] = []

    def _before(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(Engine, "before_cursor_execute", _before)
    try:
        yield statements
    finally:
        event.remove(Engine, "before_cursor_execute", _before)


def time_and_count(fn, *, iterations: int = 5) -> tuple[list[float], list[int]]:
    """Run ``fn`` repeatedly; return ms timings and query counts."""
    timings: list[float] = []
    counts: list[int] = []
    # Warm-up
    with count_queries():
        fn()
    db.session.expire_all()

    for _ in range(iterations):
        with count_queries() as stmts:
            start = time.perf_counter()
            fn()
            elapsed_ms = (time.perf_counter() - start) * 1000
        timings.append(elapsed_ms)
        counts.append(len(stmts))
        db.session.expire_all()
    return timings, counts


def summarise(path: str, timings: list[float], counts: list[int]) -> PathMetric:
    return PathMetric(
        path=path,
        iterations=len(timings),
        median_ms=round(statistics.median(timings), 2),
        mean_ms=round(statistics.mean(timings), 2),
        min_ms=round(min(timings), 2),
        max_ms=round(max(timings), 2),
        median_queries=statistics.median(counts),
        mean_queries=round(statistics.mean(counts), 2),
        min_queries=min(counts),
        max_queries=max(counts),
    )


def seed_perf_dataset(
    *,
    learner_count: int = 12,
    feedback_per_user: int = 4,
    missions_per_user: int = 20,
    leaf_topics: int = 30,
) -> dict[str, int]:
    """Seed a representative Internal Alpha dataset for profiling."""
    admin = User(email="founder-perf@kwalitec.example", is_active_user=True)
    admin.set_password("password123")
    db.session.add(admin)
    db.session.flush()

    curriculum = Curriculum(exam_name="IFoA CS1 Perf", version="2026", active=True)
    db.session.add(curriculum)
    db.session.flush()

    parent = Topic(
        curriculum_id=curriculum.id,
        name="Section A",
        order=1,
        active=True,
        recommended_minutes=120,
    )
    db.session.add(parent)
    db.session.flush()

    topics: list[Topic] = []
    for i in range(leaf_topics):
        t = Topic(
            curriculum_id=curriculum.id,
            name=f"Topic {i + 1}",
            order=i + 1,
            active=True,
            recommended_minutes=45,
            parent_topic_id=parent.id,
        )
        db.session.add(t)
        topics.append(t)
    db.session.flush()

    today = date.today()
    learners: list[User] = []
    for i in range(learner_count):
        u = User(email=f"learner{i}@kwalitec.example", is_active_user=True)
        u.set_password("password123")
        db.session.add(u)
        learners.append(u)
    db.session.flush()

    for idx, user in enumerate(learners):
        subject = Subject(
            user_id=user.id, name="CS1", colour="#003366", active=True
        )
        db.session.add(subject)
        db.session.flush()

        plan = StudyPlan(
            user_id=user.id,
            curriculum_id=curriculum.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=today + timedelta(days=200),
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            active=True,
            archived=False,
            revision_entered_at=(
                datetime.utcnow() - timedelta(days=10) if idx % 4 == 0 else None
            ),
        )
        db.session.add(plan)
        db.session.flush()

        for m_i in range(missions_per_user):
            m_date = today - timedelta(days=m_i)
            status = "Completed" if m_i > 0 else "Pending"
            if m_i == 1:
                status = "In Progress"
            mission = Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=plan.id,
                mission_date=m_date,
                title=f"Mission {m_i}",
                status=status,
            )
            db.session.add(mission)
            db.session.flush()
            db.session.add(
                MissionTask(
                    mission_id=mission.id,
                    title="Task 1",
                    order=1,
                    completed=status == "Completed",
                )
            )
            if status == "Completed":
                db.session.add(
                    StudyAttempt(
                        user_id=user.id,
                        mission_id=mission.id,
                        topic_id=topics[m_i % len(topics)].id,
                        study_date=m_date,
                        duration_minutes=45,
                        questions_attempted=10,
                        questions_correct=7,
                    )
                )

        for t_i, topic in enumerate(topics[:20]):
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=topic.id,
                    confidence="Medium",
                    completed=t_i < 5,
                    revision_count=t_i + 1,
                    mastery_score=40.0 + t_i,
                    current_stage=(
                        TopicProgress.STAGE_MASTERED
                        if t_i < 3
                        else TopicProgress.STAGE_LEARNING
                    ),
                    next_review_date=today - timedelta(days=t_i % 5),
                )
            )

        for f_i in range(feedback_per_user):
            rating = "Frustrating" if f_i < 2 and idx % 3 == 0 else "Good"
            classification = "Bug" if f_i == 0 else "Question"
            ResearchFeedbackService.submit_checkin(
                user.id,
                experience_rating=rating,
                feature_helped_most="Dashboard",
                friction_area="Nothing",
                confidence_rating="High",
                return_intent="Probably",
                submission_source=SOURCE_SETTINGS,
                classification=classification,
                free_text="Perf seed" if f_i == 0 else None,
                submitted_at=datetime.utcnow() - timedelta(days=f_i),
            )

    entry = VisionJournalService.create_entry(
        author_user_id=admin.id,
        title="Perf vision",
        description="Baseline seed",
        reason="Profiling fixture",
        potential_value="medium",
        expected_impact="Faster Founder ops",
        target_version="version_1_x",
        category="Operations",
        tags=["perf"],
    )
    VisionJournalService.promote_to_development(
        entry.id,
        promoted_by_user_id=admin.id,
        placeholder_ref="V1SP-003-PERF",
        notes="Seed only",
    )
    db.session.commit()

    return {
        "admin_id": admin.id,
        "primary_learner_id": learners[0].id,
        "learner_count": learner_count,
        "leaf_topics": leaf_topics,
        "missions_per_user": missions_per_user,
        "feedback_per_user": feedback_per_user,
    }


def measure_static_assets(static_root: Path) -> dict[str, dict[str, int | str]]:
    """Return byte sizes for first-party CSS/JS/brand assets."""
    assets: dict[str, dict[str, int | str]] = {}
    patterns = [
        "css/*.css",
        "js/*.js",
        "branding/*",
        "founder_dashboard/*",
    ]
    for pattern in patterns:
        for path in sorted(static_root.glob(pattern)):
            if not path.is_file():
                continue
            rel = str(path.relative_to(static_root))
            assets[rel] = {"bytes": path.stat().st_size, "suffix": path.suffix}
    return assets


def run_profile(app, *, label: str, iterations: int = 5) -> dict:
    """Seed data and measure all V1SP-003 hot paths."""
    from flask_login import login_user

    from app.founder.dashboard.services.command_centre_service import (
        CommandCentreService,
    )
    from app.founder.dashboard.services.operational_health_service import (
        OperationalHealthService,
    )
    from app.services.analytics_service import AnalyticsService
    from app.services.readiness_service import ReadinessService
    from app.services.study_session_service import StudySessionService

    with app.app_context():
        seed = seed_perf_dataset()
        learner_id = seed["primary_learner_id"]
        admin = db.session.get(User, seed["admin_id"])
        learner = db.session.get(User, learner_id)

        metrics: list[PathMetric] = []

        # Student dashboard (full HTTP render)
        client = app.test_client()
        with client.session_transaction() as sess:
            sess["_user_id"] = str(learner_id)
            sess["_fresh"] = True

        def dashboard():
            with app.test_request_context("/dashboard/"):
                login_user(learner)
                from app.dashboard.routes import index as dash_index

                dash_index()

        t, c = time_and_count(dashboard, iterations=iterations)
        metrics.append(summarise("dashboard_render", t, c))

        # Founder overview (service build — ops FS skipped under TESTING)
        def founder_overview():
            with app.test_request_context("/founder/"):
                login_user(admin)
                CommandCentreService().build_overview()

        t, c = time_and_count(founder_overview, iterations=iterations)
        metrics.append(summarise("founder_overview", t, c))

        def operational_health():
            with app.test_request_context("/founder/operational-health"):
                login_user(admin)
                OperationalHealthService().build_page(on_date=date.today())

        t, c = time_and_count(operational_health, iterations=iterations)
        metrics.append(summarise("operational_health", t, c))

        # Study session start
        pending = (
            Mission.query.filter_by(user_id=learner_id, status="Pending")
            .order_by(Mission.mission_date.desc())
            .first()
        )

        def study_start():
            # Reset status so start remains idempotent across iterations
            pending.status = "Pending"
            db.session.commit()
            StudySessionService.start_session(pending.id, learner_id)

        t, c = time_and_count(study_start, iterations=iterations)
        metrics.append(summarise("study_session_start", t, c))

        # Analytics — full route composition via services (mirrors route)
        def analytics():
            ReadinessService.get_overall_readiness(learner_id)
            ReadinessService.get_curriculum_coverage(learner_id)
            ReadinessService.get_review_backlog(learner_id)
            ReadinessService.get_review_completion_rate(learner_id)
            ReadinessService.get_current_streak(learner_id)
            ReadinessService.get_longest_streak(learner_id)
            ReadinessService.get_weakest_topics(learner_id, limit=5)
            ReadinessService.get_strongest_topics(learner_id, limit=5)
            AnalyticsService.get_readiness_over_time(learner_id, weeks=12)
            AnalyticsService.get_mastery_over_time(learner_id, weeks=12)
            AnalyticsService.get_accuracy_trend(learner_id, weeks=12)
            AnalyticsService.get_weekly_study_hours(learner_id, weeks=12)
            AnalyticsService.get_mission_completion_trend(learner_id, weeks=12)
            AnalyticsService.get_review_completion_trend(learner_id, weeks=12)
            AnalyticsService.get_lifetime_summary(learner_id)
            AnalyticsService.generate_weekly_report(learner_id)

        t, c = time_and_count(analytics, iterations=iterations)
        metrics.append(summarise("analytics_compose", t, c))

        # Isolated algorithmic hotspots for evidence
        def readiness_trend_only():
            AnalyticsService.get_readiness_over_time(learner_id, weeks=12)

        t, c = time_and_count(readiness_trend_only, iterations=iterations)
        metrics.append(summarise("analytics_readiness_trend", t, c))

        def revision_idle_only():
            OperationalHealthService._revision_without_sessions_count()

        t, c = time_and_count(revision_idle_only, iterations=iterations)
        metrics.append(summarise("oh_revision_idle", t, c))

        def negative_sentiment_only():
            OperationalHealthService._consecutive_negative_sentiment_users()

        t, c = time_and_count(negative_sentiment_only, iterations=iterations)
        metrics.append(summarise("oh_negative_sentiment", t, c))

        static_root = Path(app.root_path) / "static"
        assets = measure_static_assets(static_root)
        css_bytes = sum(
            v["bytes"] for k, v in assets.items() if k.startswith("css/")
        )
        js_bytes = sum(
            v["bytes"] for k, v in assets.items() if k.startswith("js/")
        )
        brand_bytes = sum(
            v["bytes"] for k, v in assets.items() if k.startswith("branding/")
        )

        payload = {
            "label": label,
            "seed": seed,
            "metrics": [asdict(m) for m in metrics],
            "static_assets": {
                "css_bytes": css_bytes,
                "js_bytes": js_bytes,
                "brand_bytes": brand_bytes,
                "files": assets,
            },
        }
        return payload


def write_report(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
