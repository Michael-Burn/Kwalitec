"""G1 dogfood walkthrough for a Runtime C student account.

Usage (production one-off job or local app context)::

    flask g1-student-walkthrough --email ctshumba01@gmail.com
    python -m scripts.g1_student_walkthrough ctshumba01@gmail.com
"""

from __future__ import annotations

import argparse
import json
import sys


def walkthrough(email: str, *, repair_placeholders: bool = True) -> dict:
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.application.educational_experience.service import (
        EducationalExperienceService,
    )
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )
    from app.application.learning_session.substance_planner import (
        EducationalSubstancePlanner,
    )
    from app.application.student_runtime.coordinator import StudentRuntimeCoordinator
    from app.infrastructure.adapters.learning_session.persistence import (
        LearningSessionPersistenceAdapter,
    )
    from app.infrastructure.adapters.learning_session.runtime_engine import (
        LearningSessionRuntimeEngine,
    )
    from app.infrastructure.engines.opaque_bridges import SessionRuntimeOpaqueBridge
    from app.infrastructure.session.composition import (
        build_production_session_experience,
    )
    from app.models import User

    user = User.query.filter_by(email=(email or "").strip().lower()).first()
    if user is None:
        return {"error": f"user not found: {email}"}

    flags = resolve_v2_feature_flags()
    report: dict = {
        "user_id": user.id,
        "email": email,
        "role": getattr(user, "role", None),
        "flags": {
            "SR_SESSION_PRIMARY": flags.SR_SESSION_PRIMARY,
            "SR_SESSION_SUBSTANCE": flags.SR_SESSION_SUBSTANCE,
            "SR_COMMERCIAL_LOOP": flags.SR_COMMERCIAL_LOOP,
            "SOLE_RUNTIME": flags.SOLE_RUNTIME,
            "SEED_DEMO_LEARNERS": flags.SEED_DEMO_LEARNERS,
            "INJECT_PHASE_I_ENGINES": flags.INJECT_PHASE_I_ENGINES,
            "ENABLE_DURABLE_STORE": flags.ENABLE_DURABLE_STORE,
        },
    }

    experience = EducationalExperienceService().load_for_user(
        user.id, ensure_mission=True
    )
    if experience is None:
        report["experience"] = None
        return report

    mission = experience.mission
    report["experience"] = {
        "subject_code": experience.subject_code,
        "curriculum_identity": experience.curriculum_identity,
        "is_runtime_c": experience.is_runtime_c,
        "syllabus_complete": experience.syllabus_complete,
        "examination_label": experience.examination_label,
        "progress_coverage": (
            experience.curriculum_position.coverage_ratio
            if experience.curriculum_position
            else None
        ),
        "current_topic": (
            experience.curriculum_position.topic_title
            if experience.curriculum_position
            else None
        ),
        "position_label": (
            experience.curriculum_position.position_label
            if experience.curriculum_position
            else None
        ),
    }
    if mission is not None:
        runtime_mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
        )
        quality = runtime_mission.quality if runtime_mission is not None else None
        report["mission"] = {
            "mission_instance_id": mission.mission_instance_id,
            "status": mission.status,
            "title": mission.title,
            "topic_title": mission.topic_title,
            "topic_code": mission.topic_code,
            "topic_id": mission.topic_id,
            "estimated_duration_minutes": mission.estimated_duration_minutes,
            "learning_objectives": list(mission.learning_objectives or ())[:8],
            "quality_lo_count": len(quality.objective_ids)
            if quality is not None
            else len(mission.learning_objectives or ()),
            "quality_minutes": quality.estimated_duration_minutes
            if quality is not None
            else mission.estimated_duration_minutes,
            "quality_objective_ids": list(quality.objective_ids or ())[:8]
            if quality is not None
            else [],
        }
        oids = tuple((quality.objective_ids if quality else ()) or ())
        substance = EducationalSubstancePlanner().plan_for_topic(
            curriculum_identity=experience.curriculum_identity,
            topic_id=mission.topic_id,
            topic_title=mission.topic_title or mission.title,
            objective_ids=oids,
            session_minutes=mission.estimated_duration_minutes or 60,
        )
        report["substance_plan"] = None
        if substance is not None:
            report["substance_plan"] = {
                "topic_title": substance.topic_title,
                "topic_code": substance.topic_code,
                "lo_count": len(substance.learning_objectives),
                "source": substance.source,
                "labels": [
                    f"{obj.code} {obj.text}"[:80]
                    for obj in substance.learning_objectives[:5]
                ],
                "has_core_methods": "core methods"
                in (substance.topic_title or "").lower(),
            }

    journey = EducationalRuntimeEngineService().get_journey(
        user_id=user.id, subject_code=experience.subject_code
    )
    report["journey"] = {
        "current_topic_id": journey.progress.current_topic_id,
        "coverage_ratio": round(float(journey.progress.coverage_ratio or 0), 4),
        "completed_topic_count": len(journey.progress.completed_topic_ids),
        "syllabus_complete": journey.progress.syllabus_complete,
    }

    composition, _service = build_production_session_experience(
        seed_demo_learners=False
    )
    engine = composition.runtime._engine
    activity_engine = getattr(composition.activity, "_engine", None)
    report["composition"] = {
        "runtime_engine": type(engine).__name__,
        "is_learning_session_runtime": isinstance(
            engine, LearningSessionRuntimeEngine
        ),
        "is_opaque_bridge": isinstance(engine, SessionRuntimeOpaqueBridge),
        "activity_engine": type(activity_engine).__name__
        if activity_engine is not None
        else None,
    }

    store = LearningSessionPersistenceAdapter(store=composition.store)
    open_doc = store.find_open(student_id=str(user.id))
    report["open_session"] = None
    if open_doc is not None:
        session_id = str(open_doc.get("session_id") or "")
        overview = None
        if hasattr(engine, "get_session_overview_opaque"):
            overview = engine.get_session_overview_opaque(
                str(user.id), session_id=session_id
            )
        seq = composition.store.get(
            "activity.sequence", f"{user.id}::{session_id}"
        )
        topic = str(open_doc.get("topic_title") or "")
        placeholder = "core methods" in topic.lower() or (
            "core methods" in str(overview or {}).lower()
        )
        report["open_session"] = {
            "session_id": session_id,
            "mission_instance_id": open_doc.get("mission_instance_id"),
            "topic_title": topic,
            "status": open_doc.get("status"),
            "placeholder_core_methods": placeholder,
            "overview_objective": (overview or {}).get("objective"),
            "overview_topics": (overview or {}).get("topics"),
            "sequence_topic": None if not seq else seq.get("topic_title"),
            "sequence_lo_count": None
            if not seq
            else len(seq.get("learning_objectives") or []),
            "sequence_source": None if not seq else seq.get("source"),
        }
        if repair_placeholders and placeholder:
            coordinator = StudentRuntimeCoordinator(
                persistence=store,
                session_overview_writer=composition.runtime,
                flags=flags,
            )
            coordinator._supersede_open_session(
                student_id=str(user.id),
                session_id=session_id,
                mission_instance_id=str(
                    open_doc.get("mission_instance_id") or ""
                ),
            )
            report["open_session"]["repaired"] = True
            report["open_session"]["repair_action"] = "superseded_placeholder"

    # Verdict for the operator.
    issues: list[str] = []
    if not flags.SR_SESSION_PRIMARY:
        issues.append("SR_SESSION_PRIMARY is off")
    if not flags.SR_SESSION_SUBSTANCE:
        issues.append("SR_SESSION_SUBSTANCE is off")
    if report["composition"]["is_opaque_bridge"]:
        issues.append("runtime engine is opaque Core-methods bridge")
    substance = report.get("substance_plan") or {}
    if substance.get("has_core_methods"):
        issues.append("substance planner returned Core methods")
    if (report.get("mission") or {}).get("quality_lo_count", 0) > 3:
        issues.append("today's mission still packs more than 3 LOs")
    open_session = report.get("open_session") or {}
    if open_session.get("placeholder_core_methods") and not open_session.get(
        "repaired"
    ):
        issues.append("open session still shows Core methods")
    report["issues"] = issues
    report["ok"] = not issues
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email", nargs="?", default="ctshumba01@gmail.com")
    parser.add_argument(
        "--no-repair",
        action="store_true",
        help="Do not supersede Core methods placeholder sittings",
    )
    args = parser.parse_args(argv)

    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from app import create_app

    app = create_app()
    with app.app_context():
        report = walkthrough(
            args.email, repair_placeholders=not args.no_repair
        )
    print(json.dumps(report, indent=2, default=str))
    return 0 if report.get("ok", False) or report.get("error") else 1


if __name__ == "__main__":
    sys.exit(main())
