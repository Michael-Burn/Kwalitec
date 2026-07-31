"""Educational Runtime Engine — curriculum-driven student journey (PI-001C).

Consumes PI-001B derived artefacts (study-plan template, mission templates,
progress model, journey). Does not recreate curriculum logic or author
subject-specific educational content.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, date, datetime
from typing import Any

from app.application.curriculum_intelligence.certified_mission_engine import (
    CertifiedMissionEngine,
)
from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    MissionTemplateSnapshot,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.educational_quality.certifier import EducationalQualityCertifier
from app.application.educational_quality.dto import (
    JourneyExplanationSnapshot,
    StudyPlanPacingSnapshot,
)
from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
    RuntimeCoexistencePolicy,
)
from app.application.educational_runtime_engine.dto import (
    EducationalEventSnapshot,
    EnrolmentSnapshot,
    EstimatedKnowledgeRuntimeInputs,
    MissionInstanceSnapshot,
    ProgressSnapshot,
    ReadinessRuntimeInputs,
    RuntimeJourneySnapshot,
    StudyPlanInstanceSnapshot,
)
from app.application.educational_runtime_engine.exceptions import (
    EnrolmentAlreadyExists,
    EnrolmentNotFound,
    IllegalRuntimeState,
    MissionAlreadyCompleted,
    MissionInstanceNotFound,
    PublishedCurriculumUnavailable,
    StudyPlanInstanceNotFound,
    SyllabusAlreadyComplete,
)
from app.application.progress_engine import (
    ProgressEngine,
    StudyProgress,
    TwinEstimateInput,
)
from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.progress import (
    ProgressModelSpec,
    ProgressTopicSpec,
    derive_progress,
)
from app.domain.educational_runtime_engine.state import (
    EnrolmentStatus,
    MissionStatus,
    PlanInstanceStatus,
    assert_mission_transition,
    assert_plan_transition,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    contains_internal_node_identifier,
    sanitize_student_text,
    student_mission_title,
    student_syllabus_code,
)
from app.extensions import db
from app.models.educational_runtime_engine import (
    RuntimeEducationalEvent,
    RuntimeEnrolment,
    RuntimeMissionInstance,
    RuntimeStudyPlanInstance,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class EducationalRuntimeEngineService:
    """Instantiate and advance personalised journeys from published artefacts."""

    SERVICE_ID = "educational_runtime_engine"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
        artefacts: EducationalEngineFoundationService | None = None,
        coexistence: RuntimeCoexistencePolicy | None = None,
        quality: EducationalQualityCertifier | None = None,
        certified_missions: CertifiedMissionEngine | None = None,
        progress_engine: ProgressEngine | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()
        self._artefacts = artefacts or EducationalEngineFoundationService(
            authority=self._authority
        )
        self._coexistence = coexistence or RuntimeCoexistencePolicy(
            authority=self._authority
        )
        self._quality = quality or EducationalQualityCertifier()
        # EI-002B: optional certified LO mission selector (defaults on).
        self._certified_missions = certified_missions or CertifiedMissionEngine()
        # SR-003: Progress Engine is the sole progression AUTHORITY when
        # SR_PROGRESS_SINGULARITY is ON. Event store remains here.
        self._progress_engine = progress_engine or ProgressEngine()
    # ── Enrolment ─────────────────────────────────────────────────────────

    def enrol_student(
        self,
        *,
        user_id: int,
        subject_code: str,
        exam_date: date | None = None,
        auto_instantiate_plan: bool = True,
    ) -> RuntimeJourneySnapshot:
        """Enrol a student against the active published curriculum.

        Automatically instantiates a study-plan instance from the derived
        study-plan template when ``auto_instantiate_plan`` is True.
        """
        code = (subject_code or "").strip().upper()
        if not code:
            raise PublishedCurriculumUnavailable("subject_code is required")

        if (
            self._coexistence.resolve_for_enrolment(code)
            != RuntimeAuthority.PUBLISHED_CURRICULUM
        ):
            raise PublishedCurriculumUnavailable(
                f"no active published curriculum for subject {code}"
            )

        package = self._authority.get_active(code)
        if package is None:
            raise PublishedCurriculumUnavailable(
                f"no active published curriculum for subject {code}"
            )

        snapshot = self._artefacts.derive_from_package(package.package)
        identity = snapshot.curriculum_identity

        existing = RuntimeEnrolment.query.filter_by(
            user_id=user_id,
            curriculum_identity=identity,
        ).first()
        if existing is not None:
            raise EnrolmentAlreadyExists(
                f"user {user_id} already enrolled in {identity}"
            )

        enrolment = RuntimeEnrolment(
            enrolment_id=_new_id("enr"),
            user_id=user_id,
            subject_code=code,
            curriculum_identity=identity,
            published_package_id=package.package_id,
            version_label=snapshot.version_label,
            status=EnrolmentStatus.ACTIVE.value,
            exam_date=exam_date,
        )
        db.session.add(enrolment)
        self._append_event(
            event_type=EducationalEventType.STUDENT_ENROLLED,
            user_id=user_id,
            curriculum_identity=identity,
            enrolment_id=enrolment.enrolment_id,
            payload={
                "subject_code": code,
                "version_label": snapshot.version_label,
                "published_package_id": package.package_id,
            },
        )
        db.session.flush()

        if auto_instantiate_plan:
            self._instantiate_study_plan(
                enrolment=enrolment,
                artefacts=snapshot,
            )
        db.session.commit()
        return self.get_journey(user_id=user_id, subject_code=code)

    def seed_declared_position(
        self,
        *,
        user_id: int,
        subject_code: str,
        curriculum_topic_code: str | None,
        completed_curriculum_topics: list[str] | tuple[str, ...] | None = None,
        realign_today_mission: bool = True,
    ) -> ProgressSnapshot | None:
        """Apply Baseline continue-from position onto Runtime C progress.

        Emits ``TOPIC_COMPLETED`` events (source=baseline_self_declared) for
        prior leaf topics, advances ``current_topic_id``, and optionally
        replaces today's mission when it still points at a pre-baseline topic.

        Idempotent: already-completed topics are skipped.
        """
        from app.application.educational_runtime_engine.baseline_position import (
            resolve_baseline_position_seed,
        )

        code = (subject_code or "").strip().upper()
        if not code or not (curriculum_topic_code or "").strip():
            return None

        enrolment = self._require_active_enrolment(user_id, code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        seed = resolve_baseline_position_seed(
            artefacts,
            curriculum_topic_code=curriculum_topic_code,
            completed_curriculum_topics=completed_curriculum_topics,
        )
        if not seed.completed_topic_ids and seed.current_topic_id is None:
            return None

        plan = self._require_active_plan(enrolment)
        progress_before = self._derive_progress_for(enrolment, artefacts)
        already = set(progress_before.completed_topic_ids)
        to_complete = [
            tid for tid in seed.completed_topic_ids if tid not in already
        ]

        # Also treat "current" as not completed; if caller already completed
        # past it via Confirm-mission, keep those events (honest history) and
        # advance from derive_progress after seeding priors.
        if not to_complete and seed.current_topic_id:
            # Priors already present — still realign mission / pointer if needed.
            if (
                progress_before.current_topic_id == seed.current_topic_id
                and not realign_today_mission
            ):
                return self._progress_snapshot(progress_before)

        now = _utc_now()
        for topic_id in to_complete:
            self._append_event(
                event_type=EducationalEventType.TOPIC_COMPLETED,
                user_id=user_id,
                curriculum_identity=enrolment.curriculum_identity,
                enrolment_id=enrolment.enrolment_id,
                plan_instance_id=plan.plan_instance_id,
                topic_id=topic_id,
                payload={
                    "source": seed.source,
                    "baseline_continue_code": seed.continue_code,
                    "warrant": "thin_self_declared",
                },
                occurred_at=now,
            )

        db.session.flush()
        progress = self._derive_progress_for(enrolment, artefacts)

        # Prefer Baseline resume topic when it is still incomplete.
        target_current = seed.current_topic_id
        if (
            target_current
            and target_current in progress.incomplete_topic_ids
        ):
            plan.current_topic_id = target_current
        else:
            plan.current_topic_id = progress.current_topic_id

        if to_complete or plan.current_topic_id != progress_before.current_topic_id:
            self._append_event(
                event_type=EducationalEventType.JOURNEY_ADVANCED,
                user_id=user_id,
                curriculum_identity=enrolment.curriculum_identity,
                enrolment_id=enrolment.enrolment_id,
                plan_instance_id=plan.plan_instance_id,
                topic_id=plan.current_topic_id,
                payload={
                    "source": seed.source,
                    "from_topic_id": progress_before.current_topic_id,
                    "to_topic_id": plan.current_topic_id,
                    "baseline_continue_code": seed.continue_code,
                    "seeded_topic_count": len(to_complete),
                    "coverage_ratio": progress.coverage_ratio,
                },
                occurred_at=now,
            )

        if realign_today_mission and plan.current_topic_id:
            self._realign_todays_mission_after_baseline_seed(
                enrolment=enrolment,
                plan=plan,
                artefacts=artefacts,
                expected_topic_id=plan.current_topic_id,
            )

        db.session.commit()
        return self.get_progress(user_id=user_id, subject_code=code)

    def reconcile_baseline_position_from_declarations(
        self,
        *,
        user_id: int,
        subject_code: str,
        curriculum_topic_code: str | None,
        completed_curriculum_topics: list[str] | tuple[str, ...] | None = None,
    ) -> ProgressSnapshot | None:
        """Self-heal Runtime C position from a completed Baseline row."""
        return self.seed_declared_position(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_topic_code=curriculum_topic_code,
            completed_curriculum_topics=completed_curriculum_topics,
            realign_today_mission=True,
        )

    def _realign_todays_mission_after_baseline_seed(
        self,
        *,
        enrolment: RuntimeEnrolment,
        plan: RuntimeStudyPlanInstance,
        artefacts: EducationalArtefactSnapshot,
        expected_topic_id: str,
    ) -> None:
        day = date.today()
        mission = RuntimeMissionInstance.query.filter_by(
            plan_instance_id=plan.plan_instance_id,
            mission_date=day,
        ).first()
        if mission is None:
            return
        if mission.topic_id == expected_topic_id:
            return
        # Wrong chapter for declared position — remove so generate_daily_mission
        # can recreate against the seeded current topic (including when the
        # student already "Confirmed" 1.1 without a real session).
        self._append_event(
            event_type=EducationalEventType.MISSION_DEFERRED,
            user_id=enrolment.user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=mission.topic_id,
            mission_instance_id=mission.mission_instance_id,
            payload={
                "source": "baseline_position_realign",
                "reason": "mission_topic_precedes_declared_baseline_position",
                "expected_topic_id": expected_topic_id,
                "prior_status": mission.status,
            },
        )
        db.session.delete(mission)
        db.session.flush()

    # ── Study plan ────────────────────────────────────────────────────────

    def instantiate_study_plan(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> StudyPlanInstanceSnapshot:
        """Create a study-plan instance from the derived template (idempotent)."""
        enrolment = self._require_active_enrolment(user_id, subject_code)
        existing = RuntimeStudyPlanInstance.query.filter_by(
            enrolment_id=enrolment.enrolment_id,
            status=PlanInstanceStatus.ACTIVE.value,
        ).first()
        if existing is not None:
            return self._plan_snapshot(existing)

        artefacts = self._load_artefacts(enrolment.subject_code)
        plan = self._instantiate_study_plan(enrolment=enrolment, artefacts=artefacts)
        db.session.commit()
        return self._plan_snapshot(plan, artefacts=artefacts)

    def _instantiate_study_plan(
        self,
        *,
        enrolment: RuntimeEnrolment,
        artefacts: EducationalArtefactSnapshot,
    ) -> RuntimeStudyPlanInstance:
        progress_model = self._progress_model_spec(artefacts)
        events = self._event_records(
            user_id=enrolment.user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        derived = derive_progress(progress_model, events)

        plan = RuntimeStudyPlanInstance(
            plan_instance_id=_new_id("plan"),
            enrolment_id=enrolment.enrolment_id,
            user_id=enrolment.user_id,
            subject_code=enrolment.subject_code,
            curriculum_identity=enrolment.curriculum_identity,
            version_label=enrolment.version_label,
            status=PlanInstanceStatus.ACTIVE.value,
            current_topic_id=derived.current_topic_id
            or (
                artefacts.progress_model.topic_ids[0]
                if artefacts.progress_model and artefacts.progress_model.topic_ids
                else None
            ),
        )
        db.session.add(plan)
        self._append_event(
            event_type=EducationalEventType.STUDY_PLAN_INSTANTIATED,
            user_id=enrolment.user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=plan.current_topic_id,
            payload={
                "topic_template_count": len(
                    artefacts.study_plan_template.topic_templates
                    if artefacts.study_plan_template
                    else ()
                ),
                "current_topic_id": plan.current_topic_id,
            },
        )
        db.session.flush()
        return plan

    # ── Daily missions ────────────────────────────────────────────────────

    def generate_daily_mission(
        self,
        *,
        user_id: int,
        subject_code: str,
        mission_date: date | None = None,
    ) -> MissionInstanceSnapshot:
        """Generate (idempotently) today's mission from derived mission templates."""
        day = mission_date or date.today()
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._derive_progress_for(enrolment, artefacts)
        if progress.syllabus_complete or progress.current_topic_id is None:
            raise SyllabusAlreadyComplete(
                f"syllabus complete for {enrolment.curriculum_identity}"
            )
        if enrolment.status != EnrolmentStatus.ACTIVE.value:
            raise IllegalRuntimeState(
                f"enrolment {enrolment.enrolment_id} is {enrolment.status}"
            )
        plan = self._require_active_plan(enrolment)

        existing = RuntimeMissionInstance.query.filter_by(
            plan_instance_id=plan.plan_instance_id,
            mission_date=day,
        ).first()
        if existing is not None:
            return self._mission_snapshot(
                existing,
                artefacts=artefacts,
                completed_topic_ids=progress.completed_topic_ids,
            )

        package = self._authority.get_active(enrolment.subject_code)
        package_dict = package.package if package is not None else {}
        certified_spec = self._select_certified_mission(
            package_dict,
            completed_topic_ids=progress.completed_topic_ids,
            artefacts=artefacts,
            preferred_topic_id=progress.current_topic_id,
        )
        # MISSION-002: mission topic must match progress current topic.
        topic_id = progress.current_topic_id
        if (
            certified_spec is not None
            and certified_spec.topic_id == progress.current_topic_id
        ):
            topic_id = certified_spec.topic_id
        template = self._mission_template_for_topic(artefacts, topic_id)
        if template is None:
            raise IllegalRuntimeState(
                f"no mission template for topic {topic_id}"
            )

        # EQ-M07: refuse generation when prerequisites are not satisfied
        topic = next(
            (t for t in artefacts.topics if t["topic_id"] == template.topic_id),
            {},
        )
        required = tuple(
            template.prerequisite_ids
            or tuple(topic.get("prerequisite_ids") or ())
        )
        completed = set(progress.completed_topic_ids)
        missing = [pid for pid in required if pid not in completed]
        if missing:
            raise IllegalRuntimeState(
                f"cannot generate mission for {template.topic_id}; "
                f"unsatisfied prerequisites: {missing}"
            )

        objective_ids = list(
            certified_spec.objective_ids
            if certified_spec is not None
            and certified_spec.topic_id == template.topic_id
            else template.objective_ids
        )
        topic_meta = next(
            (t for t in artefacts.topics if t.get("topic_id") == template.topic_id),
            {},
        )
        topic_title = str(
            topic_meta.get("title") or topic_meta.get("text") or template.title
        )
        human_code = student_syllabus_code(
            code=template.topic_code,
            title=topic_title,
            number=str(topic_meta.get("number") or ""),
        )
        mission_title = student_mission_title(
            code=human_code or template.topic_code,
            title=topic_title,
        )
        human_tasks = tuple(
            sanitize_student_text(task) for task in template.task_descriptions
        )
        mission = RuntimeMissionInstance(
            mission_instance_id=_new_id("msn"),
            plan_instance_id=plan.plan_instance_id,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
            template_id=template.template_id,
            topic_id=template.topic_id,
            topic_code=human_code or template.topic_code,
            title=mission_title,
            task_descriptions_json=json.dumps(list(human_tasks)),
            mission_date=day,
            status=MissionStatus.GENERATED.value,
        )
        db.session.add(mission)
        plan.current_topic_id = template.topic_id
        payload: dict[str, Any] = {
            "template_id": template.template_id,
            "mission_date": day.isoformat(),
            "title": mission_title,
            "objective_ids": objective_ids,
            "estimated_duration_minutes": template.estimated_duration_minutes,
        }
        if certified_spec is not None:
            payload["certified_mission_id"] = certified_spec.mission_id
            payload["selection_reasons"] = [
                r.value for r in certified_spec.selection_reasons
            ]
            payload["curriculum_provenance"] = {
                "chain_id": certified_spec.provenance.chain_id,
                "snapshot_id": certified_spec.provenance.snapshot_id,
                "authority": certified_spec.provenance.authority,
                "status": certified_spec.provenance.status,
            }
            if certified_spec.calibration_notes:
                payload["calibration_notes"] = list(certified_spec.calibration_notes)
        self._append_event(
            event_type=EducationalEventType.MISSION_GENERATED,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=template.topic_id,
            mission_instance_id=mission.mission_instance_id,
            payload=payload,
        )
        db.session.commit()
        return self._mission_snapshot(
            mission,
            artefacts=artefacts,
            completed_topic_ids=progress.completed_topic_ids,
        )

    def get_mission_instance(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
    ) -> MissionInstanceSnapshot | None:
        """Return a mission instance snapshot owned by the user, if any."""
        mission = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mission_instance_id,
            user_id=user_id,
        ).first()
        if mission is None:
            return None
        plan = RuntimeStudyPlanInstance.query.filter_by(
            plan_instance_id=mission.plan_instance_id
        ).first()
        enrolment = None
        if plan is not None:
            enrolment = RuntimeEnrolment.query.filter_by(
                enrolment_id=plan.enrolment_id
            ).first()
        artefacts = None
        completed: tuple[str, ...] = ()
        if enrolment is not None:
            artefacts = self._load_artefacts(enrolment.subject_code)
            if artefacts is not None:
                completed = self._derive_progress_for(
                    enrolment, artefacts
                ).completed_topic_ids
        return self._mission_snapshot(
            mission,
            artefacts=artefacts,
            completed_topic_ids=completed,
        )

    def accept_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        session_id: str,
    ) -> MissionInstanceSnapshot:
        """SR-002a — Mission Accepted ≡ Study Session start (no progress advance).

        Transitions GENERATED|DEFERRED → ACCEPTED and records MISSION_ACCEPTED.
        Does not emit TOPIC_COMPLETED or complete the mission.
        """
        mission = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mission_instance_id,
            user_id=user_id,
        ).first()
        if mission is None:
            raise MissionInstanceNotFound(mission_instance_id)

        if mission.status == MissionStatus.COMPLETED.value:
            raise MissionAlreadyCompleted(mission_instance_id)

        if mission.status == MissionStatus.ACCEPTED.value:
            # Idempotent re-accept (resume) — refresh session_id in event stream.
            plan = RuntimeStudyPlanInstance.query.filter_by(
                plan_instance_id=mission.plan_instance_id
            ).first()
            enrolment = (
                RuntimeEnrolment.query.filter_by(enrolment_id=plan.enrolment_id).first()
                if plan is not None
                else None
            )
            artefacts = (
                self._load_artefacts(enrolment.subject_code)
                if enrolment is not None
                else None
            )
            completed: tuple[str, ...] = ()
            if enrolment is not None and artefacts is not None:
                completed = self._derive_progress_for(
                    enrolment, artefacts
                ).completed_topic_ids
            return self._mission_snapshot(
                mission, artefacts=artefacts, completed_topic_ids=completed
            )

        try:
            assert_mission_transition(mission.status, MissionStatus.ACCEPTED)
        except ValueError as exc:
            raise IllegalRuntimeState(str(exc)) from exc

        plan = RuntimeStudyPlanInstance.query.filter_by(
            plan_instance_id=mission.plan_instance_id
        ).first()
        if plan is None:
            raise StudyPlanInstanceNotFound(mission.plan_instance_id)

        enrolment = RuntimeEnrolment.query.filter_by(
            enrolment_id=plan.enrolment_id
        ).first()
        if enrolment is None:
            raise EnrolmentNotFound(plan.enrolment_id)

        artefacts = self._load_artefacts(enrolment.subject_code)
        now = _utc_now()
        mission.status = MissionStatus.ACCEPTED.value

        self._append_event(
            event_type=EducationalEventType.MISSION_ACCEPTED,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=mission.topic_id,
            mission_instance_id=mission.mission_instance_id,
            payload={
                "session_id": (session_id or "").strip(),
                "template_id": mission.template_id,
                "mission_date": mission.mission_date.isoformat(),
            },
            occurred_at=now,
        )
        db.session.commit()
        completed = ()
        if artefacts is not None:
            completed = self._derive_progress_for(
                enrolment, artefacts
            ).completed_topic_ids
        return self._mission_snapshot(
            mission,
            artefacts=artefacts,
            completed_topic_ids=completed,
        )

    def defer_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        reason_code: str = "not_today",
    ) -> MissionInstanceSnapshot:
        """SR-002a — ILE-004 Deferred without session start or progress advance."""
        mission = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mission_instance_id,
            user_id=user_id,
        ).first()
        if mission is None:
            raise MissionInstanceNotFound(mission_instance_id)

        if mission.status == MissionStatus.COMPLETED.value:
            raise MissionAlreadyCompleted(mission_instance_id)

        if mission.status == MissionStatus.DEFERRED.value:
            plan = RuntimeStudyPlanInstance.query.filter_by(
                plan_instance_id=mission.plan_instance_id
            ).first()
            enrolment = (
                RuntimeEnrolment.query.filter_by(enrolment_id=plan.enrolment_id).first()
                if plan is not None
                else None
            )
            artefacts = (
                self._load_artefacts(enrolment.subject_code)
                if enrolment is not None
                else None
            )
            completed: tuple[str, ...] = ()
            if enrolment is not None and artefacts is not None:
                completed = self._derive_progress_for(
                    enrolment, artefacts
                ).completed_topic_ids
            return self._mission_snapshot(
                mission, artefacts=artefacts, completed_topic_ids=completed
            )

        try:
            assert_mission_transition(mission.status, MissionStatus.DEFERRED)
        except ValueError as exc:
            raise IllegalRuntimeState(str(exc)) from exc

        plan = RuntimeStudyPlanInstance.query.filter_by(
            plan_instance_id=mission.plan_instance_id
        ).first()
        if plan is None:
            raise StudyPlanInstanceNotFound(mission.plan_instance_id)

        enrolment = RuntimeEnrolment.query.filter_by(
            enrolment_id=plan.enrolment_id
        ).first()
        if enrolment is None:
            raise EnrolmentNotFound(plan.enrolment_id)

        artefacts = self._load_artefacts(enrolment.subject_code)
        now = _utc_now()
        mission.status = MissionStatus.DEFERRED.value

        self._append_event(
            event_type=EducationalEventType.MISSION_DEFERRED,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=mission.topic_id,
            mission_instance_id=mission.mission_instance_id,
            payload={
                "reason_code": (reason_code or "not_today").strip() or "not_today",
                "template_id": mission.template_id,
                "mission_date": mission.mission_date.isoformat(),
            },
            occurred_at=now,
        )
        db.session.commit()
        completed = ()
        if artefacts is not None:
            completed = self._derive_progress_for(
                enrolment, artefacts
            ).completed_topic_ids
        return self._mission_snapshot(
            mission,
            artefacts=artefacts,
            completed_topic_ids=completed,
        )

    def complete_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        advance_progress: bool = True,
        evidence_package_id: str | None = None,
        evidence_disposition: str | None = None,
        may_complete_mission: bool | None = None,
    ) -> RuntimeJourneySnapshot:
        """Record mission completion as immutable events and advance journey.

        EV-001B: ``advance_progress`` may be False when Authority accepts the
        sitting with restrictions that forbid coverage advancement.

        SR-003: when ``SR_PROGRESS_SINGULARITY`` is ON, ProgressEngine alone
        authorises coverage advancement from Evidence Authority columns.
        Twin is never written here.
        """
        if self._progress_engine.singularity_enabled():
            self._progress_engine.claim_sole_writer(
                "educational_runtime_engine"
            )
            decision = self._progress_engine.authorise_coverage_advance(
                may_advance_progress=bool(advance_progress),
                evidence_disposition=evidence_disposition,
                may_complete_mission=may_complete_mission,
                mission_instance_id=mission_instance_id,
                package_id=evidence_package_id,
            )
            advance_progress = decision.may_advance
        return self._complete_mission_impl(
            user_id=user_id,
            mission_instance_id=mission_instance_id,
            advance_progress=advance_progress,
            evidence_package_id=evidence_package_id,
        )

    def _complete_mission_impl(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        advance_progress: bool = True,
        evidence_package_id: str | None = None,
    ) -> RuntimeJourneySnapshot:
        """Internal mission completion + optional TOPIC_COMPLETED write."""
        mission = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mission_instance_id,
            user_id=user_id,
        ).first()
        if mission is None:
            raise MissionInstanceNotFound(mission_instance_id)

        if mission.status == MissionStatus.COMPLETED.value:
            raise MissionAlreadyCompleted(mission_instance_id)

        try:
            assert_mission_transition(mission.status, MissionStatus.COMPLETED)
        except ValueError as exc:
            raise IllegalRuntimeState(str(exc)) from exc

        plan = RuntimeStudyPlanInstance.query.filter_by(
            plan_instance_id=mission.plan_instance_id
        ).first()
        if plan is None:
            raise StudyPlanInstanceNotFound(mission.plan_instance_id)

        enrolment = RuntimeEnrolment.query.filter_by(
            enrolment_id=plan.enrolment_id
        ).first()
        if enrolment is None:
            raise EnrolmentNotFound(plan.enrolment_id)

        artefacts = self._load_artefacts(enrolment.subject_code)
        now = _utc_now()
        mission.status = MissionStatus.COMPLETED.value
        mission.completed_at = now

        self._append_event(
            event_type=EducationalEventType.MISSION_COMPLETED,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=mission.topic_id,
            mission_instance_id=mission.mission_instance_id,
            payload={
                "template_id": mission.template_id,
                "mission_date": mission.mission_date.isoformat(),
                "evidence_package_id": evidence_package_id,
                "advance_progress": bool(advance_progress),
                "progress_authority": (
                    "progress_engine"
                    if self._progress_engine.singularity_enabled()
                    else "educational_runtime_engine"
                ),
            },
            occurred_at=now,
        )
        if advance_progress:
            self._append_event(
                event_type=EducationalEventType.TOPIC_COMPLETED,
                user_id=user_id,
                curriculum_identity=enrolment.curriculum_identity,
                enrolment_id=enrolment.enrolment_id,
                plan_instance_id=plan.plan_instance_id,
                topic_id=mission.topic_id,
                mission_instance_id=mission.mission_instance_id,
                payload={
                    "source": "mission_completion",
                    "evidence_package_id": evidence_package_id,
                    "progress_authority": (
                        "progress_engine"
                        if self._progress_engine.singularity_enabled()
                        else "educational_runtime_engine"
                    ),
                },
                occurred_at=now,
            )
        db.session.flush()

        if advance_progress:
            progress = self._derive_progress_for(enrolment, artefacts)
            previous_topic = mission.topic_id
            plan.current_topic_id = progress.current_topic_id

            self._append_event(
                event_type=EducationalEventType.JOURNEY_ADVANCED,
                user_id=user_id,
                curriculum_identity=enrolment.curriculum_identity,
                enrolment_id=enrolment.enrolment_id,
                plan_instance_id=plan.plan_instance_id,
                topic_id=progress.current_topic_id,
                mission_instance_id=mission.mission_instance_id,
                payload={
                    "from_topic_id": previous_topic,
                    "to_topic_id": progress.current_topic_id,
                    "journey_stage": progress.journey_stage.value,
                    "coverage_ratio": progress.coverage_ratio,
                    "evidence_package_id": evidence_package_id,
                },
                occurred_at=now,
            )

            if progress.syllabus_complete:
                self._append_event(
                    event_type=EducationalEventType.SYLLABUS_COMPLETED,
                    user_id=user_id,
                    curriculum_identity=enrolment.curriculum_identity,
                    enrolment_id=enrolment.enrolment_id,
                    plan_instance_id=plan.plan_instance_id,
                    payload={
                        "completed_topic_count": len(progress.completed_topic_ids)
                    },
                    occurred_at=now,
                )
                try:
                    assert_plan_transition(plan.status, PlanInstanceStatus.COMPLETED)
                    plan.status = PlanInstanceStatus.COMPLETED.value
                except ValueError:
                    pass
                enrolment.status = EnrolmentStatus.COMPLETED.value

        db.session.commit()
        return self.get_journey(user_id=user_id, subject_code=enrolment.subject_code)

    # ── Progress / readiness / EK projections ─────────────────────────────

    def get_progress(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> ProgressSnapshot:
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        derived = self._derive_progress_for(enrolment, artefacts)
        return self._progress_snapshot(derived)

    def get_study_progress(
        self,
        *,
        user_id: int,
        subject_code: str,
        twin_estimates: TwinEstimateInput | dict[str, Any] | None = None,
    ) -> StudyProgress:
        """Singular Study Progress via Progress Engine (SR-003).

        Twin estimates are optional projection annotations. Coverage is
        always event-sourced from TOPIC_COMPLETED.
        """
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        model = self._progress_model_spec(artefacts)
        events = self._event_records(
            user_id=enrolment.user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        twin = (
            twin_estimates
            if isinstance(twin_estimates, TwinEstimateInput)
            else TwinEstimateInput.from_opaque(twin_estimates)
        )
        return self._progress_engine.derive_study_progress(
            model, events, twin_estimates=twin
        )

    def get_mission_progress_inputs(
        self,
        *,
        user_id: int,
        subject_code: str,
        twin_estimates: TwinEstimateInput | dict[str, Any] | None = None,
    ):
        """Progress inputs for tomorrow's mission composition (SR-003)."""
        study = self.get_study_progress(
            user_id=user_id,
            subject_code=subject_code,
            twin_estimates=twin_estimates,
        )
        return self._progress_engine.mission_composition_inputs(study)

    def get_readiness_inputs(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> ReadinessRuntimeInputs:
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        derived = self._derive_progress_for(enrolment, artefacts)
        return ReadinessRuntimeInputs(
            curriculum_identity=derived.curriculum_identity,
            subject_code=enrolment.subject_code,
            topic_ids=derived.topic_ids,
            completed_topic_ids=derived.completed_topic_ids,
            coverage_ratio=derived.coverage_ratio,
            current_topic_id=derived.current_topic_id,
            syllabus_complete=derived.syllabus_complete,
            journey_stage=derived.journey_stage.value,
        )

    def get_estimated_knowledge_inputs(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> EstimatedKnowledgeRuntimeInputs:
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        derived = self._derive_progress_for(enrolment, artefacts)
        completed = set(derived.completed_topic_ids)
        topics = tuple(
            {
                "topic_id": topic_id,
                "completed": topic_id in completed,
                "has_estimated_knowledge": False,
                "average_accuracy": None,
                "mastery_score": None,
            }
            for topic_id in derived.topic_ids
        )
        return EstimatedKnowledgeRuntimeInputs(
            curriculum_identity=derived.curriculum_identity,
            subject_code=enrolment.subject_code,
            topic_ids=derived.topic_ids,
            completed_topic_ids=derived.completed_topic_ids,
            topics=topics,
        )

    def get_journey(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> RuntimeJourneySnapshot:
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        plan = RuntimeStudyPlanInstance.query.filter_by(
            enrolment_id=enrolment.enrolment_id,
        ).order_by(RuntimeStudyPlanInstance.id.desc()).first()
        if plan is None:
            raise StudyPlanInstanceNotFound(
                f"no study plan for enrolment {enrolment.enrolment_id}"
            )
        derived = self._derive_progress_for(enrolment, artefacts)
        open_mission = (
            RuntimeMissionInstance.query.filter(
                RuntimeMissionInstance.plan_instance_id == plan.plan_instance_id,
                RuntimeMissionInstance.status.in_(
                    (
                        MissionStatus.GENERATED.value,
                        MissionStatus.ACCEPTED.value,
                        MissionStatus.DEFERRED.value,
                    )
                ),
            )
            .order_by(RuntimeMissionInstance.mission_date.desc())
            .first()
        )
        return RuntimeJourneySnapshot(
            enrolment=self._enrolment_snapshot(enrolment),
            study_plan=self._plan_snapshot(plan, artefacts=artefacts),
            progress=self._progress_snapshot(derived),
            readiness_inputs=ReadinessRuntimeInputs(
                curriculum_identity=derived.curriculum_identity,
                subject_code=enrolment.subject_code,
                topic_ids=derived.topic_ids,
                completed_topic_ids=derived.completed_topic_ids,
                coverage_ratio=derived.coverage_ratio,
                current_topic_id=derived.current_topic_id,
                syllabus_complete=derived.syllabus_complete,
                journey_stage=derived.journey_stage.value,
            ),
            estimated_knowledge_inputs=self.get_estimated_knowledge_inputs(
                user_id=user_id,
                subject_code=subject_code,
            ),
            open_mission=(
                self._mission_snapshot(
                    open_mission,
                    artefacts=artefacts,
                    completed_topic_ids=derived.completed_topic_ids,
                )
                if open_mission
                else None
            ),
            runtime_authority=RuntimeAuthority.PUBLISHED_CURRICULUM.value,
        )

    def get_journey_explanation(
        self,
        *,
        user_id: int,
        subject_code: str,
    ) -> JourneyExplanationSnapshot:
        """Explain why today / why previous complete / what unlocks next (EQ-001)."""
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._progress_snapshot(
            self._derive_progress_for(enrolment, artefacts)
        )
        previous_topic_id = self._previous_completed_topic(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        return self._quality.build_journey_explanation_snapshot(
            artefacts=artefacts,
            progress=progress,
            previous_topic_id=previous_topic_id,
        )

    def project_pacing(
        self,
        *,
        user_id: int,
        subject_code: str,
        as_of: date | None = None,
        weekday_minutes: int = 90,
        weekend_minutes: int = 120,
    ) -> StudyPlanPacingSnapshot:
        """Read-only pacing projection with exam-date awareness and revision share."""
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        return self._quality.build_pacing_snapshot(
            artefacts=artefacts,
            exam_date=enrolment.exam_date,
            as_of=as_of or date.today(),
            weekday_minutes=weekday_minutes,
            weekend_minutes=weekend_minutes,
        )

    def list_events(
        self,
        *,
        user_id: int,
        subject_code: str | None = None,
    ) -> tuple[EducationalEventSnapshot, ...]:
        query = RuntimeEducationalEvent.query.filter_by(user_id=user_id)
        if subject_code:
            enrolment = self._require_enrolment(user_id, subject_code)
            query = query.filter_by(
                curriculum_identity=enrolment.curriculum_identity
            )
        rows = query.order_by(
            RuntimeEducationalEvent.occurred_at.asc(),
            RuntimeEducationalEvent.id.asc(),
        ).all()
        return tuple(self._event_snapshot(row) for row in rows)

    # ── Internals ─────────────────────────────────────────────────────────

    def _load_artefacts(self, subject_code: str) -> EducationalArtefactSnapshot:
        snapshot = self._artefacts.derive_active(subject_code)
        if snapshot is None:
            raise PublishedCurriculumUnavailable(
                f"no active published curriculum for subject {subject_code}"
            )
        return snapshot

    def _select_certified_mission(
        self,
        package: dict[str, Any],
        *,
        completed_topic_ids: tuple[str, ...] | list[str],
        artefacts: EducationalArtefactSnapshot,
        preferred_topic_id: str | None = None,
    ):
        """EI-002B: select Daily Mission from certified LOs when package is certified.

        Pre-EI / empty certification packages keep legacy current-topic selection.
        MISSION-002: prefer ``preferred_topic_id`` (progress current) when eligible.
        """
        cert = package.get("certification") if isinstance(package, dict) else None
        if not isinstance(cert, dict) or not cert:
            return None
        authority = str(cert.get("authority") or "").strip().lower()
        status = str(cert.get("status") or "").strip().lower()
        if authority not in {
            "",
            "certified_snapshot",
            "legacy_cip_fallback",
            "legacy_or_unspecified",
        } and status not in {"certified", "certified_with_warnings"}:
            if not authority.startswith("legacy"):
                return None
        # Mastered objectives inferred from completed topics' objective lists.
        mastered: list[str] = []
        completed = set(completed_topic_ids)
        for topic in artefacts.topics:
            tid = str(topic.get("topic_id") or "")
            if tid in completed:
                mastered.extend(str(o) for o in (topic.get("objective_ids") or ()))
        calibration = None
        structure = package.get("structure") if isinstance(package, dict) else {}
        struct_cal = (
            structure.get("calibration") if isinstance(structure, dict) else None
        )
        if isinstance(struct_cal, dict):
            calibration = dict(struct_cal)
        elif isinstance(package.get("calibration"), dict):
            calibration = dict(package["calibration"])
        try:
            return self._certified_missions.generate(
                package,
                completed_node_ids=tuple(completed_topic_ids),
                mastered_objective_ids=tuple(dict.fromkeys(mastered)),
                preferred_topic_id=preferred_topic_id,
                calibration=calibration,
            )
        except ValueError:
            return None

    def _require_enrolment(self, user_id: int, subject_code: str) -> RuntimeEnrolment:
        code = (subject_code or "").strip().upper()
        enrolment = (
            RuntimeEnrolment.query.filter_by(user_id=user_id, subject_code=code)
            .order_by(RuntimeEnrolment.id.desc())
            .first()
        )
        if enrolment is None:
            raise EnrolmentNotFound(f"user {user_id} not enrolled in {code}")
        return enrolment

    def _require_active_enrolment(
        self, user_id: int, subject_code: str
    ) -> RuntimeEnrolment:
        enrolment = self._require_enrolment(user_id, subject_code)
        if enrolment.status != EnrolmentStatus.ACTIVE.value:
            raise IllegalRuntimeState(
                f"enrolment {enrolment.enrolment_id} is {enrolment.status}"
            )
        return enrolment

    def _require_active_plan(
        self, enrolment: RuntimeEnrolment
    ) -> RuntimeStudyPlanInstance:
        plan = RuntimeStudyPlanInstance.query.filter_by(
            enrolment_id=enrolment.enrolment_id,
            status=PlanInstanceStatus.ACTIVE.value,
        ).first()
        if plan is None:
            raise StudyPlanInstanceNotFound(
                f"no active study plan for enrolment {enrolment.enrolment_id}"
            )
        return plan

    def _progress_model_spec(
        self, artefacts: EducationalArtefactSnapshot
    ) -> ProgressModelSpec:
        model = artefacts.progress_model
        if model is None:
            raise IllegalRuntimeState("artefacts missing progress_model")
        topics = tuple(
            ProgressTopicSpec(
                topic_id=str(topic["topic_id"]),
                topic_code=str(topic.get("topic_code") or ""),
                objective_ids=tuple(topic.get("objective_ids") or ()),
                prerequisite_ids=tuple(topic.get("prerequisite_ids") or ()),
            )
            for topic in model.topics
        )
        return ProgressModelSpec(
            curriculum_identity=model.curriculum_identity,
            topic_ids=tuple(model.topic_ids),
            topics=topics,
        )

    def _derive_progress_for(
        self,
        enrolment: RuntimeEnrolment,
        artefacts: EducationalArtefactSnapshot,
    ):
        return derive_progress(
            self._progress_model_spec(artefacts),
            self._event_records(
                user_id=enrolment.user_id,
                curriculum_identity=enrolment.curriculum_identity,
            ),
        )

    def _event_records(
        self,
        *,
        user_id: int,
        curriculum_identity: str,
    ) -> tuple[EducationalEventRecord, ...]:
        rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=user_id,
                curriculum_identity=curriculum_identity,
            )
            .order_by(
                RuntimeEducationalEvent.occurred_at.asc(),
                RuntimeEducationalEvent.id.asc(),
            )
            .all()
        )
        return tuple(
            EducationalEventRecord(
                event_id=row.event_id,
                event_type=EducationalEventType(row.event_type),
                user_id=row.user_id,
                curriculum_identity=row.curriculum_identity,
                enrolment_id=row.enrolment_id,
                plan_instance_id=row.plan_instance_id,
                topic_id=row.topic_id,
                mission_instance_id=row.mission_instance_id,
                payload=json.loads(row.payload_json or "{}"),
                occurred_at=row.occurred_at,
            )
            for row in rows
        )

    def _mission_template_for_topic(
        self,
        artefacts: EducationalArtefactSnapshot,
        topic_id: str,
    ) -> MissionTemplateSnapshot | None:
        for template in artefacts.mission_templates:
            if template.topic_id == topic_id:
                return template
        return None

    def _append_event(
        self,
        *,
        event_type: EducationalEventType,
        user_id: int,
        curriculum_identity: str,
        enrolment_id: str | None = None,
        plan_instance_id: str | None = None,
        topic_id: str | None = None,
        mission_instance_id: str | None = None,
        payload: dict[str, Any] | None = None,
        occurred_at: datetime | None = None,
    ) -> RuntimeEducationalEvent:
        row = RuntimeEducationalEvent(
            event_id=_new_id("evt"),
            event_type=event_type.value,
            user_id=user_id,
            enrolment_id=enrolment_id,
            plan_instance_id=plan_instance_id,
            curriculum_identity=curriculum_identity,
            topic_id=topic_id,
            mission_instance_id=mission_instance_id,
            payload_json=json.dumps(payload or {}),
            occurred_at=occurred_at or _utc_now(),
        )
        db.session.add(row)
        return row

    def _enrolment_snapshot(self, row: RuntimeEnrolment) -> EnrolmentSnapshot:
        return EnrolmentSnapshot(
            enrolment_id=row.enrolment_id,
            user_id=row.user_id,
            subject_code=row.subject_code,
            curriculum_identity=row.curriculum_identity,
            version_label=row.version_label,
            published_package_id=row.published_package_id,
            status=row.status,
            exam_date=row.exam_date,
            created_at=row.created_at,
        )

    def _plan_snapshot(
        self,
        row: RuntimeStudyPlanInstance,
        *,
        artefacts: EducationalArtefactSnapshot | None = None,
    ) -> StudyPlanInstanceSnapshot:
        topic_ids: tuple[str, ...] = ()
        if artefacts and artefacts.study_plan_template:
            topic_ids = tuple(
                str(t["topic_id"])
                for t in artefacts.study_plan_template.topic_templates
            )
        return StudyPlanInstanceSnapshot(
            plan_instance_id=row.plan_instance_id,
            enrolment_id=row.enrolment_id,
            user_id=row.user_id,
            subject_code=row.subject_code,
            curriculum_identity=row.curriculum_identity,
            version_label=row.version_label,
            status=row.status,
            current_topic_id=row.current_topic_id,
            topic_template_ids=topic_ids,
            created_at=row.created_at,
        )

    def _mission_snapshot(
        self,
        row: RuntimeMissionInstance,
        *,
        artefacts: EducationalArtefactSnapshot | None = None,
        completed_topic_ids: tuple[str, ...] | set[str] | None = None,
    ) -> MissionInstanceSnapshot:
        tasks = tuple(
            sanitize_student_text(task)
            for task in json.loads(row.task_descriptions_json or "[]")
        )
        quality = None
        topic_title = ""
        topic_meta: dict[str, Any] = {}
        if artefacts is not None:
            topic_meta = next(
                (
                    t
                    for t in artefacts.topics
                    if str(t.get("topic_id") or "") == row.topic_id
                ),
                {},
            )
            topic_title = str(
                topic_meta.get("title") or topic_meta.get("text") or ""
            )
            template = next(
                (
                    t
                    for t in artefacts.mission_templates
                    if t.template_id == row.template_id
                ),
                None,
            )
            if template is not None:
                quality = self._quality.build_mission_quality_envelope(
                    template=template,
                    artefacts=artefacts,
                    completed_topic_ids=completed_topic_ids or (),
                )
        human_code = student_syllabus_code(
            code=row.topic_code or "",
            title=topic_title or row.title or "",
            number=str(topic_meta.get("number") or ""),
        )
        title = sanitize_student_text(row.title)
        if not title or contains_internal_node_identifier(title):
            title = student_mission_title(
                code=human_code,
                title=topic_title or sanitize_student_text(row.title) or "",
            )
        return MissionInstanceSnapshot(
            mission_instance_id=row.mission_instance_id,
            plan_instance_id=row.plan_instance_id,
            user_id=row.user_id,
            curriculum_identity=row.curriculum_identity,
            template_id=row.template_id,
            topic_id=row.topic_id,
            topic_code=human_code or sanitize_student_text(row.topic_code),
            title=title,
            task_descriptions=tasks,
            mission_date=row.mission_date,
            status=row.status,
            created_at=row.created_at,
            completed_at=row.completed_at,
            quality=quality,
        )

    def _previous_completed_topic(
        self,
        *,
        user_id: int,
        curriculum_identity: str,
    ) -> str | None:
        rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=user_id,
                curriculum_identity=curriculum_identity,
                event_type=EducationalEventType.TOPIC_COMPLETED.value,
            )
            .order_by(
                RuntimeEducationalEvent.occurred_at.desc(),
                RuntimeEducationalEvent.id.desc(),
            )
            .all()
        )
        for row in rows:
            if row.topic_id:
                return row.topic_id
        return None

    @staticmethod
    def _progress_snapshot(derived) -> ProgressSnapshot:
        return ProgressSnapshot(
            curriculum_identity=derived.curriculum_identity,
            topic_ids=derived.topic_ids,
            completed_topic_ids=derived.completed_topic_ids,
            incomplete_topic_ids=derived.incomplete_topic_ids,
            current_topic_id=derived.current_topic_id,
            coverage_ratio=derived.coverage_ratio,
            journey_stage=derived.journey_stage.value,
            syllabus_complete=derived.syllabus_complete,
        )

    @staticmethod
    def _event_snapshot(row: RuntimeEducationalEvent) -> EducationalEventSnapshot:
        return EducationalEventSnapshot(
            event_id=row.event_id,
            event_type=row.event_type,
            user_id=row.user_id,
            curriculum_identity=row.curriculum_identity,
            enrolment_id=row.enrolment_id,
            plan_instance_id=row.plan_instance_id,
            topic_id=row.topic_id,
            mission_instance_id=row.mission_instance_id,
            payload=json.loads(row.payload_json or "{}"),
            occurred_at=row.occurred_at,
        )
