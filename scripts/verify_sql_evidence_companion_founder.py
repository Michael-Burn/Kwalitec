#!/usr/bin/env python3
"""Direct local verification: SR_SESSION_SQL_EVIDENCE_COMPANION write-through.

Runs against the developer's local SQLite and the founder account from
``ADMIN_EMAIL``. Completes one scored practice sitting on a real approved
package via the live Accept → seed practice → complete path, then asserts a
real ``StudyAttempt`` (and practiced-topic ``TopicProgress``) was written.

Not for production. Not imported by the app. Safe to delete after review.
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta

# Dogfood flags must win before create_app / load_dotenv (override=False).
os.environ.setdefault("APP_ENV", "development")
os.environ["SR_SESSION_SQL_EVIDENCE_COMPANION"] = "1"
# Local .env may set enrolment without discovery; published-category enrol
# requires discovery ON for this verification path.
os.environ["KWALITEC_RUNTIME_C_ENROLMENT"] = "1"
os.environ["KWALITEC_PUBLISHED_SUBJECT_DISCOVERY"] = "1"


def main() -> int:
    from app import create_app
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.application.educational_experience import EducationalExperienceService
    from app.application.educational_packages.loader import EducationalPackageLoader
    from app.application.educational_packages.substance import substance_from_package
    from app.application.learning_session.educational_flow import EducationalStage
    from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
    from app.application.platform_integration.enrolment_bridge import (
        FounderStudentEnrolmentBridge,
    )
    from app.application.platform_integration.exceptions import BridgeEnrolmentBlocked
    from app.application.student_runtime import StudentRuntimeCoordinator
    from app.extensions import db
    from app.infrastructure.adapters.learning_session.package_activity_engine import (
        PackageActivityEngine,
    )
    from app.infrastructure.adapters.learning_session.persistence import (
        LearningSessionPersistenceAdapter,
    )
    from app.infrastructure.adapters.learning_session.runtime_engine import (
        LearningSessionRuntimeEngine,
    )
    from app.infrastructure.session.store import SessionDocumentStore
    from app.models.curriculum import Topic
    from app.models.educational_runtime_engine import (
        RuntimeEnrolment,
        RuntimeMissionInstance,
    )
    from app.models.learning import StudyAttempt
    from app.models.mission import Mission
    from app.models.topic_progress import TopicProgress
    from app.models.user import User
    from app.services.educational_evidence_authority import EducationalEvidenceAuthority

    app = create_app()
    with app.app_context():
        flags = resolve_v2_feature_flags()
        if not flags.SR_SESSION_SQL_EVIDENCE_COMPANION:
            print("FAIL: SR_SESSION_SQL_EVIDENCE_COMPANION is OFF")
            return 1

        email = (os.environ.get("ADMIN_EMAIL") or "").strip().lower()
        if not email:
            print("FAIL: ADMIN_EMAIL unset")
            return 1
        user = User.query.filter_by(email=email).one_or_none()
        if user is None:
            print(f"FAIL: founder user not found for {email!r}")
            return 1

        if RuntimeEnrolment.query.filter_by(user_id=user.id).first() is None:
            try:
                result = FounderStudentEnrolmentBridge().enrol(
                    user_id=user.id,
                    category_code=PUBLISHED_CATEGORY_CODE,
                    subject_code="CS1",
                    exam_date=date.today() + timedelta(days=120),
                )
                print(
                    f"enrolled Runtime C authority={result.runtime_authority} "
                    f"subject=CS1"
                )
            except BridgeEnrolmentBlocked as exc:
                print(f"FAIL: enrolment blocked: {exc}")
                return 1
            except Exception as exc:  # noqa: BLE001
                # Duplicate enrolment is fine; other errors are not.
                from app.application.educational_runtime_engine.exceptions import (
                    EnrolmentAlreadyExists,
                )

                if not isinstance(exc, EnrolmentAlreadyExists):
                    print(f"FAIL: enrolment error: {exc}")
                    return 1

        snap = EducationalExperienceService().load_for_user(user.id)
        if snap is None or snap.mission is None:
            print("FAIL: no Runtime C mission available for founder")
            return 1

        mid = snap.mission.mission_instance_id
        topic_code = (snap.mission.topic_code or "").strip()
        print(f"mission={mid} topic_code={topic_code!r}")

        # Prefer the mission's package when the sitting already names one;
        # otherwise bind a real approved package for that topic_code.
        pack = None
        loader = EducationalPackageLoader()
        for candidate in loader.all_approved():
            if (candidate.topic_code or "").strip() == topic_code:
                pack = candidate
                break
        if pack is None:
            pack = next(iter(loader.all_approved()), None)
        if pack is None:
            print("FAIL: no approved educational package")
            return 1
        print(f"package={pack.package_id} pack_topic={pack.topic_code}")

        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        coordinator = StudentRuntimeCoordinator(persistence=persistence)
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mid,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mid, user_id=user.id
        ).one()
        if row.sql_mission_id is None:
            print("FAIL: accept did not bind sql_mission_id (companion)")
            return 1
        companion_id = int(row.sql_mission_id)
        print(f"companion_mission_id={companion_id} session={binding.session_id}")

        # Ensure the sitting handle names the real package for Phase 3 resolution.
        handle = persistence.load(session_id=binding.session_id) or {}
        if not str(handle.get("educational_package_id") or "").strip():
            handle = {
                **handle,
                "educational_package_id": pack.package_id,
                "topic_id": pack.topic_code,
            }
            persistence.save(session_id=binding.session_id, record=handle)

        substance = substance_from_package(
            pack,
            curriculum_identity=f"CS1:{pack.topic_code}",
            topic_id=pack.topic_code,
        )
        practice_acts = [
            a
            for a in substance.activities
            if a.stage is EducationalStage.PRACTICE and a.scoreable is not None
        ]
        if not practice_acts:
            print(f"FAIL: package {pack.package_id} has no scoreable practice")
            return 1

        # Score first correct, rest incorrect — real scored_correct values.
        items = []
        correct_n = 0
        for index, act in enumerate(practice_acts):
            scored = index == 0
            if scored:
                correct_n += 1
            items.append(
                {
                    "activity_id": act.activity_id,
                    "stage": "practice",
                    "item_id": act.scoreable.item_id,
                    "response": "verify-companion",
                    "scored_correct": scored,
                }
            )
        key = PackageActivityEngine._key(str(user.id), binding.session_id)
        store.save(
            PackageActivityEngine.NS_RESPONSES,
            key,
            {
                "student_id": str(user.id),
                "session_id": binding.session_id,
                "items": items,
            },
        )
        attempted_n = len(items)
        print(f"seeded_scored_practice attempted={attempted_n} correct={correct_n}")

        before_attempts = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=companion_id
        ).count()
        before_progress = TopicProgress.query.filter_by(user_id=user.id).count()

        engine = LearningSessionRuntimeEngine(persistence=persistence)
        result = engine.complete_session_opaque(
            str(user.id),
            session_id=binding.session_id,
            finish_verdict="partially",
        )
        db.session.commit()

        attempt_id = (result or {}).get("sql_evidence_attempt_id")
        if attempt_id is None:
            print("FAIL: complete_session returned no sql_evidence_attempt_id")
            print(f"result_keys={sorted((result or {}).keys())}")
            return 1

        attempt = StudyAttempt.query.get(int(attempt_id))
        if attempt is None:
            print(f"FAIL: StudyAttempt id={attempt_id} missing")
            return 1
        if int(attempt.user_id) != int(user.id):
            print("FAIL: StudyAttempt user mismatch")
            return 1
        if int(attempt.mission_id) != companion_id:
            print("FAIL: StudyAttempt not on companion mission")
            return 1
        if attempt.questions_attempted != attempted_n:
            print(
                f"FAIL: attempted={attempt.questions_attempted} "
                f"expected={attempted_n}"
            )
            return 1
        if attempt.questions_correct != correct_n:
            print(
                f"FAIL: correct={attempt.questions_correct} expected={correct_n}"
            )
            return 1
        if not EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
            attempt
        ):
            print("FAIL: StudyAttempt lacks structured question results")
            return 1

        companion = Mission.query.get(companion_id)
        if companion is None or companion.status != "Completed":
            print(f"FAIL: companion status={getattr(companion, 'status', None)}")
            return 1

        after_attempts = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=companion_id
        ).count()
        if after_attempts != before_attempts + 1:
            print(
                f"FAIL: attempt count {before_attempts} -> {after_attempts} "
                "(expected +1)"
            )
            return 1

        topic = None
        if attempt.topic_id is not None:
            topic = Topic.query.get(int(attempt.topic_id))
            progress = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=attempt.topic_id
            ).one_or_none()
            if progress is None:
                print("FAIL: TopicProgress missing for practiced topic_id")
                return 1

        after_progress = TopicProgress.query.filter_by(user_id=user.id).count()
        print("PASS")
        print(f"  founder_user_id={user.id}")
        print(f"  study_attempt_id={attempt.id}")
        print(f"  companion_mission_id={companion_id}")
        print(
            f"  questions_attempted={attempt.questions_attempted} "
            f"questions_correct={attempt.questions_correct}"
        )
        print(f"  topic_id={attempt.topic_id}")
        if topic is not None:
            print(f"  topic_name={topic.name!r}")
        print(
            f"  topic_progress_rows {before_progress} -> {after_progress}"
        )
        print(
            "  note: Stack A Estimated Knowledge columns are retired "
            "(Twin cutover); SQL companion proof is StudyAttempt + "
            "TopicProgress write-through on the companion Mission."
        )
        return 0


if __name__ == "__main__":
    sys.exit(main())
