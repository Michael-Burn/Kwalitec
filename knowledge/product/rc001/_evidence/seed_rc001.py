#!/usr/bin/env python3
"""RC-001 evidence-capture seed script.

Builds a small, isolated SQLite database with two accounts used only for
Playwright evidence capture (B7 responsive validation, B4/B5/B6 live
accessibility checks). Does not modify application code or the developer's
own `instance/kwalitec.sqlite3`.

Accounts:
    rc001.full@kwalitec.example / RC001Evidence!2026
        Active study plan, mission, topic progress — used for Success-state
        screenshots (Home, Mission, Study Plan, History, Journey, Revision,
        Profile, Settings, Help).
    rc001.empty@kwalitec.example / RC001Evidence!2026
        No study plan, no onboarding completed — used for Empty-state and
        Onboarding screenshots.

Usage:
    RC001_DB_PATH=/tmp/rc001_evidence.sqlite3 python seed_rc001.py
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta

DB_PATH = os.environ.get("RC001_DB_PATH", "/tmp/rc001_evidence.sqlite3")

os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("SECRET_KEY", "rc001-evidence-secret-key")
os.environ["KWALITEC_V2_STUDENT_EXPERIENCE"] = "1"
os.environ["KWALITEC_V2_SOLE_RUNTIME"] = "1"
os.environ["KWALITEC_V2_DURABLE_STORE"] = "1"
os.environ["KWALITEC_V2_INJECT_ENGINES"] = "1"
os.environ["KWALITEC_EI_INTERNAL_ALPHA"] = "1"
os.environ["KWALITEC_V2_SEED_DEMO"] = "0"

from app import config  # noqa: E402

test_uri = f"sqlite:///{DB_PATH}"
config._database_uri = lambda: test_uri
config.BaseConfig.SQLALCHEMY_DATABASE_URI = test_uri

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402

PASSWORD = "RC001Evidence!2026"


def main() -> int:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    app = create_app()
    app.config.update(SQLALCHEMY_DATABASE_URI=test_uri)

    with app.app_context():
        db.create_all()

        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import StudyAttempt
        from app.models.mission import Mission, MissionTask
        from app.models.study_plan import StudyPlan
        from app.models.subject import Subject
        from app.models.topic_progress import TopicProgress
        from app.models.user import User

        curriculum = Curriculum(exam_name="IFoA CM1", version="2026", active=True)
        db.session.add(curriculum)
        db.session.flush()

        topics = [
            Topic(
                name="Probability",
                curriculum_id=curriculum.id,
                order=1,
                recommended_minutes=60,
                active=True,
            ),
            Topic(
                name="Statistics",
                curriculum_id=curriculum.id,
                order=2,
                recommended_minutes=60,
                active=True,
            ),
        ]
        db.session.add_all(topics)
        db.session.flush()
        topics.append(
            Topic(
                name="Distributions",
                curriculum_id=curriculum.id,
                parent_topic_id=topics[1].id,
                order=1,
                recommended_minutes=30,
                active=True,
            )
        )
        db.session.add(topics[-1])
        db.session.commit()

        # --- Full account (Success states) ---
        full = User(email="rc001.full@kwalitec.example", is_active_user=True)
        full.set_password(PASSWORD)
        full.alpha_onboarding_completed = True
        full.alpha_onboarding_skipped = False
        db.session.add(full)
        db.session.commit()

        subject = Subject(
            user_id=full.id, name="IFoA CM1", colour="#3B4FB8", active=True
        )
        db.session.add(subject)
        db.session.commit()

        plan = StudyPlan(
            user_id=full.id,
            exam_name="IFoA CM1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=90,
            weekend_study_minutes=150,
            current_stage="Chapter 2",
            study_preference="Mixed",
            target_grade="A",
            preferred_session_minutes=None,
            curriculum_version="2026",
            active=True,
        )
        db.session.add(plan)
        db.session.commit()

        mission = Mission(
            user_id=full.id,
            subject_id=subject.id,
            study_plan_id=plan.id,
            mission_date=date.today(),
            title="Distributions — focused practice",
            status="Pending",
        )
        db.session.add(mission)
        db.session.commit()
        db.session.refresh(mission)

        db.session.add_all(
            [
                MissionTask(
                    mission_id=mission.id,
                    title="Review key formulae",
                    description="Skim the distribution formula sheet",
                    order=0,
                ),
                MissionTask(
                    mission_id=mission.id,
                    title="Practice set A",
                    description="10 questions on joint distributions",
                    order=1,
                ),
            ]
        )
        db.session.commit()

        db.session.add(
            StudyAttempt(
                user_id=full.id,
                topic_id=topics[0].id,
                mission_id=mission.id,
                study_date=date.today() - timedelta(days=1),
                questions_attempted=10,
                questions_correct=8,
                confidence_before="Low",
                confidence_after="Medium",
            )
        )
        db.session.add(
            TopicProgress(
                user_id=full.id,
                topic_id=topics[0].id,
                mastery_score=72.0,
                current_stage=TopicProgress.STAGE_PRACTISING,
                revision_count=3,
                average_accuracy=76.0,
                next_review_date=date.today() + timedelta(days=5),
                completed=False,
            )
        )
        db.session.commit()

        # --- Empty account (Empty states + Onboarding) ---
        empty = User(email="rc001.empty@kwalitec.example", is_active_user=True)
        empty.set_password(PASSWORD)
        empty.alpha_onboarding_completed = False
        empty.alpha_onboarding_skipped = False
        db.session.add(empty)
        db.session.commit()

        print(f"Seeded {DB_PATH}")
        print(f"  full account:  rc001.full@kwalitec.example / {PASSWORD}")
        print(f"  empty account: rc001.empty@kwalitec.example / {PASSWORD}")
        print(f"  full user id={full.id} empty user id={empty.id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
