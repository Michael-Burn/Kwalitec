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
    SittingExecutionSpec,
    StudyPlanInstanceSnapshot,
)
from app.application.educational_runtime_engine.exceptions import (
    CertifiedGuidanceUnavailable,
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
        """Generate (idempotently) today's mission from derived mission templates.

        Legacy flag-OFF path: syllabus/enrolment guards, ops short-circuit,
        then selection, then materialise. Selection helpers are shared with
        ADR-027 Policy V0; composition unchanged.
        """
        day = mission_date or date.today()
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._derive_progress_for(enrolment, artefacts)
        completed_packs = self._completed_educational_package_ids(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        last_pack_id = self._last_completed_educational_package_id(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        from app.application.educational_packages.selection import (
            pending_post_tip_front_package,
        )

        memory_pack = pending_post_tip_front_package(
            subject_id=enrolment.subject_code,
            completed_package_ids=completed_packs,
            last_completed_package_id=last_pack_id,
        )
        # Preserve pre-M0 guard order: syllabus/inactive before short-circuit.
        if (
            progress.syllabus_complete or progress.current_topic_id is None
        ) and memory_pack is None:
            raise SyllabusAlreadyComplete(
                f"syllabus complete for {enrolment.curriculum_identity}"
            )
        if enrolment.status != EnrolmentStatus.ACTIVE.value:
            if memory_pack is None:
                raise IllegalRuntimeState(
                    f"enrolment {enrolment.enrolment_id} is {enrolment.status}"
                )
            enrolment.status = EnrolmentStatus.ACTIVE.value

        existing = self.try_return_existing_daily_mission(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=day,
        )
        if existing is not None:
            return existing
        spec = self.compute_daily_sitting_selection(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=day,
        )
        return self.materialise_daily_mission_from_spec(spec)

    def try_return_existing_daily_mission(
        self,
        *,
        user_id: int,
        subject_code: str,
        mission_date: date | None = None,
    ) -> MissionInstanceSnapshot | None:
        """Operational short-circuit: return today's mission when still valid.

        Handles tip-complete reopen, PX-B-005/006 retirement, and oversized
        regeneration prep. Does not perform topic/package selection. Returns
        None when a new sitting identity must be chosen (caller decides).
        """
        day = mission_date or date.today()
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._derive_progress_for(enrolment, artefacts)
        completed_packs = self._completed_educational_package_ids(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        last_pack_id = self._last_completed_educational_package_id(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        from app.application.educational_packages.selection import (
            pending_post_tip_front_package,
        )

        memory_pack = pending_post_tip_front_package(
            subject_id=enrolment.subject_code,
            completed_package_ids=completed_packs,
            last_completed_package_id=last_pack_id,
        )
        # Tip-complete reopen for post-tip fronts (selection may still BLOCK).
        if enrolment.status != EnrolmentStatus.ACTIVE.value and memory_pack is not None:
            enrolment.status = EnrolmentStatus.ACTIVE.value
        if memory_pack is not None:
            plan = (
                RuntimeStudyPlanInstance.query.filter_by(
                    enrolment_id=enrolment.enrolment_id,
                    status=PlanInstanceStatus.ACTIVE.value,
                ).first()
                or RuntimeStudyPlanInstance.query.filter_by(
                    enrolment_id=enrolment.enrolment_id,
                )
                .order_by(RuntimeStudyPlanInstance.id.desc())
                .first()
            )
            if plan is None:
                return None
            if plan.status != PlanInstanceStatus.ACTIVE.value:
                plan.status = PlanInstanceStatus.ACTIVE.value
        else:
            plan = RuntimeStudyPlanInstance.query.filter_by(
                enrolment_id=enrolment.enrolment_id,
                status=PlanInstanceStatus.ACTIVE.value,
            ).first()
            if plan is None:
                return None

        existing = RuntimeMissionInstance.query.filter_by(
            plan_instance_id=plan.plan_instance_id,
            mission_date=day,
        ).first()
        if existing is None:
            return None

        # PX-B-005 / PX-B-006: retire wrong-package or completed-learning blocking
        # revision, then allow regeneration.
        owed = None
        if memory_pack is not None:
            owed = memory_pack
        else:
            from app.application.educational_packages.selection import (
                resolve_active_educational_package,
            )

            owed = resolve_active_educational_package(
                subject_id=enrolment.subject_code,
                syllabus_topic_code=progress.current_topic_id or "",
                completed_package_ids=completed_packs,
                last_completed_package_id=last_pack_id,
            )
        existing_pack = self._educational_package_id_for_mission(
            existing.mission_instance_id
        )
        if existing.status == MissionStatus.COMPLETED.value:
            if (
                owed is not None
                and owed.package_id
                and owed.package_id != existing_pack
                and (owed.mode or "").strip().lower() == "revision"
            ):
                db.session.delete(existing)
                db.session.flush()
                return None
        elif (
            existing.status
            in {
                MissionStatus.GENERATED.value,
                MissionStatus.ACCEPTED.value,
            }
            and owed is not None
            and owed.package_id
            and existing_pack
            and owed.package_id != existing_pack
        ):
            db.session.delete(existing)
            db.session.flush()
            return None
        if not self._mission_exceeds_session_budget(
            existing,
            user_id=user_id,
            artefacts=artefacts,
            mission_date=day,
        ):
            return self._mission_snapshot(
                existing,
                artefacts=artefacts,
                completed_topic_ids=progress.completed_topic_ids,
            )
        self._retire_oversized_daily_mission(
            existing,
            enrolment=enrolment,
            plan=plan,
        )
        return None

    def compute_daily_sitting_selection(
        self,
        *,
        user_id: int,
        subject_code: str,
        mission_date: date | None = None,
    ) -> SittingExecutionSpec:
        """Select daily sitting identity (pre-chunk objectives).

        Behavioural extract of the pre-M0 selection block inside
        ``generate_daily_mission``. Raises the same exceptions as today for
        syllabus-complete / inactive / guidance / template / prerequisite cases.
        """
        day = mission_date or date.today()
        enrolment = self._require_enrolment(user_id, subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._derive_progress_for(enrolment, artefacts)
        completed_packs = self._completed_educational_package_ids(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        last_pack_id = self._last_completed_educational_package_id(
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        from app.application.educational_packages.selection import (
            pending_post_tip_front_package,
        )

        memory_pack = pending_post_tip_front_package(
            subject_id=enrolment.subject_code,
            completed_package_ids=completed_packs,
            last_completed_package_id=last_pack_id,
        )
        # RO-014/RO-015: tip-complete must not block CP-D1...CP-R1 or CR-D1...CR-R1.
        if (
            progress.syllabus_complete or progress.current_topic_id is None
        ) and memory_pack is None:
            raise SyllabusAlreadyComplete(
                f"syllabus complete for {enrolment.curriculum_identity}"
            )
        if enrolment.status != EnrolmentStatus.ACTIVE.value:
            if memory_pack is None:
                raise IllegalRuntimeState(
                    f"enrolment {enrolment.enrolment_id} is {enrolment.status}"
                )
            enrolment.status = EnrolmentStatus.ACTIVE.value
        if memory_pack is not None:
            plan = (
                RuntimeStudyPlanInstance.query.filter_by(
                    enrolment_id=enrolment.enrolment_id,
                    status=PlanInstanceStatus.ACTIVE.value,
                ).first()
                or RuntimeStudyPlanInstance.query.filter_by(
                    enrolment_id=enrolment.enrolment_id,
                )
                .order_by(RuntimeStudyPlanInstance.id.desc())
                .first()
            )
            if plan is None:
                raise StudyPlanInstanceNotFound(
                    f"no study plan for enrolment {enrolment.enrolment_id}"
                )
            if plan.status != PlanInstanceStatus.ACTIVE.value:
                plan.status = PlanInstanceStatus.ACTIVE.value
        else:
            plan = self._require_active_plan(enrolment)

        package = self._authority.get_active(enrolment.subject_code)
        package_dict = package.package if package is not None else {}
        preferred_topic = progress.current_topic_id
        if memory_pack is not None and (
            progress.syllabus_complete or progress.current_topic_id is None
        ):
            preferred_topic = self._topic_id_for_package_code(
                artefacts, memory_pack.topic_code
            ) or preferred_topic
        certified_spec = self._select_certified_mission(
            package_dict,
            completed_topic_ids=progress.completed_topic_ids,
            artefacts=artefacts,
            preferred_topic_id=preferred_topic,
            user_id=user_id,
            curriculum_identity=enrolment.curriculum_identity,
        )
        # MISSION-002: mission topic must match progress current topic,
        # except post-tip Memory/Publication Front sittings (CP/CR package topic).
        topic_id = preferred_topic or progress.current_topic_id
        if (
            certified_spec is not None
            and certified_spec.topic_id == progress.current_topic_id
            and memory_pack is None
        ):
            topic_id = certified_spec.topic_id
        template = self._mission_template_for_topic(artefacts, topic_id)
        if template is None:
            raise IllegalRuntimeState(
                f"no mission template for topic {topic_id}"
            )

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
        mastered = set(
            self._mastered_objective_ids_from_events(
                user_id=user_id,
                curriculum_identity=enrolment.curriculum_identity,
            )
        )
        objective_ids = [oid for oid in objective_ids if oid not in mastered]
        if not objective_ids:
            objective_ids = [
                oid
                for oid in self._topic_objective_ids(artefacts, template.topic_id)
                if oid not in mastered
            ] or list(template.objective_ids[:1])

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
        from app.application.educational_packages.guard import (
            certified_guidance_enforced,
            withhold_message,
        )
        from app.application.educational_packages.selection import (
            resolve_active_educational_package,
        )

        pack = memory_pack
        if pack is None and certified_guidance_enforced(enrolment.subject_code):
            pack = resolve_active_educational_package(
                subject_id=enrolment.subject_code,
                syllabus_topic_code=human_code or template.topic_code,
                completed_package_ids=completed_packs,
                last_completed_package_id=last_pack_id,
            )
            if pack is None:
                raise CertifiedGuidanceUnavailable(
                    withhold_message(topic_code=human_code or template.topic_code),
                    topic_code=human_code or template.topic_code,
                    subject_code=enrolment.subject_code,
                )

        selection_reasons: tuple[str, ...] = ()
        provenance: dict[str, Any] | None = None
        calibration: tuple[str, ...] = ()
        certified_mission_id: str | None = None
        if certified_spec is not None:
            certified_mission_id = certified_spec.mission_id
            selection_reasons = tuple(
                r.value for r in certified_spec.selection_reasons
            )
            provenance = {
                "chain_id": certified_spec.provenance.chain_id,
                "snapshot_id": certified_spec.provenance.snapshot_id,
                "authority": certified_spec.provenance.authority,
                "status": certified_spec.provenance.status,
            }
            if certified_spec.calibration_notes:
                calibration = tuple(certified_spec.calibration_notes)

        return SittingExecutionSpec(
            user_id=user_id,
            subject_code=enrolment.subject_code,
            mission_date=day,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=template.topic_id,
            topic_code=human_code or template.topic_code,
            template_id=template.template_id,
            objective_ids=tuple(objective_ids),
            educational_package_id=(
                pack.package_id if pack is not None else None
            ),
            educational_package_mode=(pack.mode if pack is not None else None),
            educational_campaign_day=(
                pack.campaign_day if pack is not None else None
            ),
            certified_mission_id=certified_mission_id,
            selection_reasons=selection_reasons,
            curriculum_provenance=provenance,
            calibration_notes=calibration,
            selection_trace={
                "preferred_topic": preferred_topic,
                "memory_pack_id": (
                    memory_pack.package_id if memory_pack is not None else None
                ),
                "owed_pack_id": pack.package_id if pack is not None else None,
                "progress_current_topic_id": progress.current_topic_id,
                "adaptive_attempted": False,
            },
        )

    def materialise_daily_mission_from_spec(
        self,
        spec: SittingExecutionSpec,
    ) -> MissionInstanceSnapshot:
        """Persist a daily mission from an execution spec (composition only).

        Applies session-budget chunking, title/task assembly, and MISSION_GENERATED.
        Does not import or consult the Adaptive Decision Engine.
        """
        day = spec.mission_date
        enrolment = self._require_enrolment(spec.user_id, spec.subject_code)
        artefacts = self._load_artefacts(enrolment.subject_code)
        progress = self._derive_progress_for(enrolment, artefacts)
        plan = RuntimeStudyPlanInstance.query.filter_by(
            plan_instance_id=spec.plan_instance_id,
        ).first()
        if plan is None:
            plan = self._require_active_plan(enrolment)

        template = next(
            (
                t
                for t in artefacts.mission_templates
                if t.template_id == spec.template_id
            ),
            None,
        )
        if template is None:
            template = self._mission_template_for_topic(artefacts, spec.topic_id)
        if template is None:
            raise IllegalRuntimeState(
                f"no mission template for topic {spec.topic_id}"
            )

        session_budget = self._session_budget_minutes(spec.user_id, day)
        objective_ids = list(
            self._chunk_objectives_for_session(
                list(spec.objective_ids),
                artefacts=artefacts,
                session_minutes=session_budget,
            )
        )
        topic_meta = next(
            (
                t
                for t in artefacts.topics
                if t.get("topic_id") == template.topic_id
            ),
            {},
        )
        topic_title = str(
            topic_meta.get("title") or topic_meta.get("text") or template.title
        )
        human_code = spec.topic_code or student_syllabus_code(
            code=template.topic_code,
            title=topic_title,
            number=str(topic_meta.get("number") or ""),
        )

        pack = None
        if spec.educational_package_id:
            from app.application.educational_packages.loader import (
                find_package_by_id,
            )

            pack = find_package_by_id(spec.educational_package_id)

        if pack is not None and pack.display_title:
            mission_title = str(pack.display_title).strip()
        elif template.title and not str(template.title).lower().startswith(
            "study "
        ):
            mission_title = str(template.title).strip()
        else:
            mission_title = student_mission_title(
                code=human_code or template.topic_code,
                title=topic_title,
            )
        if pack is not None and pack.task_descriptions:
            task_source = pack.task_descriptions
        else:
            task_source = template.task_descriptions
        human_tasks = tuple(
            sanitize_student_text(task) for task in task_source
        )
        mission = RuntimeMissionInstance(
            mission_instance_id=_new_id("msn"),
            plan_instance_id=plan.plan_instance_id,
            user_id=spec.user_id,
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
            "estimated_duration_minutes": session_budget
            or template.estimated_duration_minutes,
            "session_budget_minutes": session_budget,
            "objective_chunk": True,
        }
        if pack is not None:
            payload["educational_package_id"] = pack.package_id
            payload["educational_package_mode"] = (
                spec.educational_package_mode or pack.mode
            )
            payload["educational_campaign_day"] = (
                spec.educational_campaign_day
                if spec.educational_campaign_day is not None
                else pack.campaign_day
            )
        elif spec.educational_package_id:
            payload["educational_package_id"] = spec.educational_package_id
            if spec.educational_package_mode:
                payload["educational_package_mode"] = (
                    spec.educational_package_mode
                )
            if spec.educational_campaign_day is not None:
                payload["educational_campaign_day"] = (
                    spec.educational_campaign_day
                )
        if spec.certified_mission_id:
            payload["certified_mission_id"] = spec.certified_mission_id
            if spec.selection_reasons:
                payload["selection_reasons"] = list(spec.selection_reasons)
            if spec.curriculum_provenance:
                payload["curriculum_provenance"] = dict(
                    spec.curriculum_provenance
                )
            if spec.calibration_notes:
                payload["calibration_notes"] = list(spec.calibration_notes)
        self._append_event(
            event_type=EducationalEventType.MISSION_GENERATED,
            user_id=spec.user_id,
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

        pack_id = self._educational_package_id_for_mission(
            mission.mission_instance_id
        )
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
                "educational_package_id": pack_id,
                "objective_ids": list(
                    self._objective_ids_for_mission(mission.mission_instance_id)
                ),
                "progress_authority": (
                    "progress_engine"
                    if self._progress_engine.singularity_enabled()
                    else "educational_runtime_engine"
                ),
            },
            occurred_at=now,
        )
        topic_fully_covered = False
        if advance_progress:
            topic_fully_covered = self._topic_objectives_fully_covered(
                enrolment=enrolment,
                artefacts=artefacts,
                topic_id=mission.topic_id,
                including_mission_id=mission.mission_instance_id,
            )
        # PB-002 F8: stay on syllabus leaf while package chain owes same-leaf
        # or revision day; force advance after revision terminal.
        if advance_progress and pack_id:
            from app.application.educational_packages.loader import find_package_by_id
            from app.application.educational_packages.selection import (
                should_suppress_topic_completed,
            )

            pack = find_package_by_id(pack_id)
            if pack is not None:
                completed_after = self._completed_educational_package_ids(
                    user_id=user_id,
                    curriculum_identity=enrolment.curriculum_identity,
                ) | {pack_id}
                if should_suppress_topic_completed(
                    pack, completed_package_ids=completed_after - {pack_id}
                ):
                    topic_fully_covered = False
                elif (pack.mode or "").strip().lower() == "revision":
                    topic_fully_covered = True
        if advance_progress and topic_fully_covered:
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

        if advance_progress and topic_fully_covered:
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
                # RO-014/RO-015: hold enrolment/plan open while CP/CR fronts remain.
                from app.application.educational_packages.selection import (
                    pending_post_tip_front_package,
                )

                completed_after = self._completed_educational_package_ids(
                    user_id=user_id,
                    curriculum_identity=enrolment.curriculum_identity,
                )
                last_after = self._last_completed_educational_package_id(
                    user_id=user_id,
                    curriculum_identity=enrolment.curriculum_identity,
                )
                memory_remaining = pending_post_tip_front_package(
                    subject_id=enrolment.subject_code,
                    completed_package_ids=completed_after,
                    last_completed_package_id=last_after,
                )
                self._append_event(
                    event_type=EducationalEventType.SYLLABUS_COMPLETED,
                    user_id=user_id,
                    curriculum_identity=enrolment.curriculum_identity,
                    enrolment_id=enrolment.enrolment_id,
                    plan_instance_id=plan.plan_instance_id,
                    payload={
                        "completed_topic_count": len(progress.completed_topic_ids),
                        "memory_front_pending": bool(memory_remaining),
                        "post_tip_front_pending": bool(memory_remaining),
                    },
                    occurred_at=now,
                )
                if memory_remaining is None:
                    try:
                        assert_plan_transition(plan.status, PlanInstanceStatus.COMPLETED)
                        plan.status = PlanInstanceStatus.COMPLETED.value
                    except ValueError:
                        pass
                    enrolment.status = EnrolmentStatus.COMPLETED.value
                else:
                    enrolment.status = EnrolmentStatus.ACTIVE.value
                    plan.status = PlanInstanceStatus.ACTIVE.value
        elif advance_progress:
            # Partial topic coverage — stay on this topic for the next sitting.
            plan.current_topic_id = mission.topic_id

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

        from app.application.student_twin.cutover import (
            phase2_twin_cutover_enabled,
        )
        from app.services.twin_cutover_service import (
            learner_twin_query,
        )

        if phase2_twin_cutover_enabled():
            query = learner_twin_query()
            topics_list = []
            for topic_id in derived.topic_ids:
                fact = query.topic_knowledge(
                    user_id=user_id,
                    subject_code=enrolment.subject_code,
                    topic_id=topic_id,
                )
                ek = (
                    float(fact.estimated_knowledge)
                    if fact.has_estimated_knowledge
                    and fact.estimated_knowledge is not None
                    else None
                )
                topics_list.append(
                    {
                        "topic_id": topic_id,
                        "completed": topic_id in completed,
                        "has_estimated_knowledge": bool(fact.has_estimated_knowledge),
                        "estimated_knowledge": ek,
                        "average_accuracy": None,
                        "mastery_score": (
                            round(ek * 100.0, 1) if ek is not None else None
                        ),
                    }
                )
            topics = tuple(topics_list)
        else:
            topics = tuple(
                {
                    "topic_id": topic_id,
                    "completed": topic_id in completed,
                    "has_estimated_knowledge": False,
                    "estimated_knowledge": None,
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

    def _session_budget_minutes(self, user_id: int, mission_date: date) -> int:
        """Student preferred sitting length; default 60 for Runtime C."""
        try:
            from app.application.student_experience.session_duration import (
                resolve_planned_session_minutes,
            )
            from app.services.study_plan_service import StudyPlanService

            plan = StudyPlanService.get_user_active_plan(user_id)
            minutes = resolve_planned_session_minutes(
                plan, mission_date=mission_date
            )
            if minutes is not None and minutes > 0:
                return int(minutes)
        except Exception:
            pass
        return 60

    def _objective_minutes_map(
        self, artefacts: EducationalArtefactSnapshot
    ) -> dict[str, int]:
        out: dict[str, int] = {}
        for obj in artefacts.objectives or ():
            oid = str(obj.get("objective_id") or "").strip()
            if not oid:
                continue
            try:
                out[oid] = int(obj.get("estimated_minutes") or 0)
            except (TypeError, ValueError):
                out[oid] = 0
        return out

    def _chunk_objectives_for_session(
        self,
        objective_ids: list[str] | tuple[str, ...],
        *,
        artefacts: EducationalArtefactSnapshot,
        session_minutes: int,
    ) -> tuple[str, ...]:
        from app.application.curriculum_intelligence.objective_chunk import (
            select_objectives_for_session,
        )

        return select_objectives_for_session(
            objective_ids,
            session_minutes=session_minutes,
            objective_minutes=self._objective_minutes_map(artefacts),
        )

    def _mission_generated_payload(
        self, mission_instance_id: str
    ) -> dict[str, Any]:
        row = (
            RuntimeEducationalEvent.query.filter_by(
                mission_instance_id=mission_instance_id,
                event_type=EducationalEventType.MISSION_GENERATED.value,
            )
            .order_by(RuntimeEducationalEvent.id.desc())
            .first()
        )
        if row is None:
            return {}
        try:
            payload = json.loads(row.payload_json or "{}")
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _educational_package_id_for_mission(
        self, mission_instance_id: str
    ) -> str:
        return str(
            self._mission_generated_payload(mission_instance_id).get(
                "educational_package_id"
            )
            or ""
        ).strip()

    def _completed_educational_package_ids(
        self, *, user_id: int, curriculum_identity: str
    ) -> frozenset[str]:
        if not curriculum_identity:
            return frozenset()
        rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=user_id,
                curriculum_identity=curriculum_identity,
                event_type=EducationalEventType.MISSION_COMPLETED.value,
            )
            .order_by(RuntimeEducationalEvent.id.asc())
            .all()
        )
        ids: list[str] = []
        for row in rows:
            try:
                payload = json.loads(row.payload_json or "{}")
            except json.JSONDecodeError:
                payload = {}
            if not isinstance(payload, dict):
                continue
            pid = str(payload.get("educational_package_id") or "").strip()
            if pid:
                ids.append(pid)
        return frozenset(ids)

    def _last_completed_educational_package_id(
        self, *, user_id: int, curriculum_identity: str
    ) -> str:
        if not curriculum_identity:
            return ""
        rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=user_id,
                curriculum_identity=curriculum_identity,
                event_type=EducationalEventType.MISSION_COMPLETED.value,
            )
            .order_by(RuntimeEducationalEvent.id.desc())
            .all()
        )
        for row in rows:
            try:
                payload = json.loads(row.payload_json or "{}")
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            pid = str(payload.get("educational_package_id") or "").strip()
            if pid:
                return pid
        return ""

    def _objective_ids_for_mission(
        self, mission_instance_id: str
    ) -> tuple[str, ...]:
        payload = self._mission_generated_payload(mission_instance_id)
        raw = payload.get("objective_ids") or ()
        return tuple(str(oid).strip() for oid in raw if str(oid).strip())

    def _mastered_objective_ids_from_events(
        self, *, user_id: int, curriculum_identity: str
    ) -> tuple[str, ...]:
        if not curriculum_identity:
            return ()
        rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=user_id,
                curriculum_identity=curriculum_identity,
            )
            .order_by(RuntimeEducationalEvent.id.asc())
            .all()
        )
        completed_missions: set[str] = set()
        generated: dict[str, tuple[str, ...]] = {}
        from_completion: list[str] = []
        for row in rows:
            mid = str(row.mission_instance_id or "").strip()
            if (
                row.event_type == EducationalEventType.MISSION_GENERATED.value
                and mid
            ):
                try:
                    payload = json.loads(row.payload_json or "{}")
                except json.JSONDecodeError:
                    payload = {}
                if isinstance(payload, dict):
                    generated[mid] = tuple(
                        str(oid).strip()
                        for oid in (payload.get("objective_ids") or ())
                        if str(oid).strip()
                    )
            elif row.event_type == EducationalEventType.MISSION_COMPLETED.value:
                if mid:
                    completed_missions.add(mid)
                try:
                    payload = json.loads(row.payload_json or "{}")
                except json.JSONDecodeError:
                    payload = {}
                if isinstance(payload, dict):
                    from_completion.extend(
                        str(oid).strip()
                        for oid in (payload.get("objective_ids") or ())
                        if str(oid).strip()
                    )
        mastered: list[str] = list(from_completion)
        for mid in completed_missions:
            mastered.extend(generated.get(mid) or ())
        return tuple(dict.fromkeys(mastered))

    def _topic_objective_ids(
        self, artefacts: EducationalArtefactSnapshot, topic_id: str
    ) -> tuple[str, ...]:
        template = self._mission_template_for_topic(artefacts, topic_id)
        if template is not None and template.objective_ids:
            return tuple(template.objective_ids)
        topic = next(
            (
                t
                for t in artefacts.topics
                if str(t.get("topic_id") or "") == topic_id
            ),
            {},
        )
        return tuple(
            str(o)
            for o in (
                topic.get("learning_objective_ids")
                or topic.get("objective_ids")
                or ()
            )
        )

    def _topic_objectives_fully_covered(
        self,
        *,
        enrolment: RuntimeEnrolment,
        artefacts: EducationalArtefactSnapshot,
        topic_id: str,
        including_mission_id: str,
    ) -> bool:
        required = set(self._topic_objective_ids(artefacts, topic_id))
        if not required:
            # No LO list — keep legacy whole-topic completion.
            return True
        mastered = set(
            self._mastered_objective_ids_from_events(
                user_id=enrolment.user_id,
                curriculum_identity=enrolment.curriculum_identity,
            )
        )
        mastered.update(self._objective_ids_for_mission(including_mission_id))
        progress = self._derive_progress_for(enrolment, artefacts)
        if topic_id in progress.completed_topic_ids:
            return True
        return required.issubset(mastered)

    def _mission_exceeds_session_budget(
        self,
        mission: RuntimeMissionInstance,
        *,
        user_id: int,
        artefacts: EducationalArtefactSnapshot,
        mission_date: date,
    ) -> bool:
        objective_ids = self._objective_ids_for_mission(mission.mission_instance_id)
        if not objective_ids:
            # Legacy missions omitted payload LOs — fall back to topic template.
            objective_ids = self._topic_objective_ids(artefacts, mission.topic_id)
        if len(objective_ids) <= 1:
            return False
        budget = self._session_budget_minutes(user_id, mission_date)
        chunked = self._chunk_objectives_for_session(
            objective_ids,
            artefacts=artefacts,
            session_minutes=budget,
        )
        return len(chunked) < len(objective_ids)

    def _retire_oversized_daily_mission(
        self,
        mission: RuntimeMissionInstance,
        *,
        enrolment: RuntimeEnrolment,
        plan: RuntimeStudyPlanInstance,
    ) -> None:
        """Remove today's oversized mission so a budgeted one can be generated."""
        prior_mission_id = mission.mission_instance_id
        self._append_event(
            event_type=EducationalEventType.MISSION_DEFERRED,
            user_id=enrolment.user_id,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=enrolment.enrolment_id,
            plan_instance_id=plan.plan_instance_id,
            topic_id=mission.topic_id,
            mission_instance_id=prior_mission_id,
            payload={
                "source": "session_budget_rechunk",
                "reason": "mission_objectives_exceed_preferred_session_minutes",
                "prior_status": mission.status,
            },
        )
        db.session.delete(mission)
        db.session.flush()
        self._supersede_open_session_for_mission(
            user_id=enrolment.user_id,
            mission_instance_id=prior_mission_id,
        )

    def _supersede_open_session_for_mission(
        self, *, user_id: int, mission_instance_id: str
    ) -> None:
        """Drop open Study Session bindings for a retired oversized mission."""
        mid = (mission_instance_id or "").strip()
        try:
            from app.infrastructure.adapters.learning_session.persistence import (
                NS_HANDLE,
                NS_MISSION,
                NS_OPEN,
                LearningSessionPersistenceAdapter,
            )
            from app.infrastructure.session.composition import (
                build_production_session_experience,
            )

            # Must use the production durable store — a bare adapter is
            # process-local memory and silently no-ops against real sittings.
            composition, _service = build_production_session_experience(
                seed_demo_learners=False
            )
            adapter = LearningSessionPersistenceAdapter(store=composition.store)
            sid = str(user_id)
            open_doc = None
            if mid:
                open_doc = adapter.find_open(
                    student_id=sid, mission_instance_id=mid
                )
            if open_doc is None:
                open_doc = adapter.find_open(student_id=sid)
            if open_doc is None:
                if mid:
                    adapter.store.delete(NS_MISSION, f"{sid}::{mid}")
                return
            session_id = str(open_doc.get("session_id") or "").strip()
            bound_mid = str(
                open_doc.get("mission_instance_id") or mid or ""
            ).strip()
            if session_id:
                handle = adapter.load(session_id=session_id) or {}
                adapter.store.save(
                    NS_HANDLE,
                    session_id,
                    {
                        **handle,
                        "status": "superseded",
                        "phase": "abandoned",
                        "superseded_reason": "session_budget_rechunk",
                    },
                )
                open_ptr = adapter.store.get(NS_OPEN, sid)
                if open_ptr and str(open_ptr.get("session_id")) == session_id:
                    adapter.store.delete(NS_OPEN, sid)
            if bound_mid:
                adapter.store.delete(NS_MISSION, f"{sid}::{bound_mid}")
            if mid and mid != bound_mid:
                adapter.store.delete(NS_MISSION, f"{sid}::{mid}")
        except Exception:
            return

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
        user_id: int | None = None,
        curriculum_identity: str | None = None,
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
        # Mastered objectives: completed topics + LOs covered by completed missions.
        mastered: list[str] = []
        completed = set(completed_topic_ids)
        for topic in artefacts.topics:
            tid = str(topic.get("topic_id") or "")
            if tid in completed:
                mastered.extend(
                    str(o)
                    for o in (
                        topic.get("learning_objective_ids")
                        or topic.get("objective_ids")
                        or ()
                    )
                )
        if user_id and curriculum_identity:
            mastered.extend(
                self._mastered_objective_ids_from_events(
                    user_id=int(user_id),
                    curriculum_identity=str(curriculum_identity),
                )
            )
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
        topic_id: str | None,
    ):
        if not topic_id:
            return None
        for template in artefacts.mission_templates:
            if template.topic_id == topic_id:
                return template
        return None

    def _topic_id_for_package_code(
        self,
        artefacts: EducationalArtefactSnapshot,
        topic_code: str,
    ) -> str | None:
        """Map package topic_code (e.g. 2.1 / CR-R1) to a curriculum topic_id."""
        code = (topic_code or "").strip()
        if not code:
            return None
        # Campaign revision codes (CA-R1, CP-R1, CR-R1, …) are not syllabus
        # numbers — bind to tip topic 5.1 when present so tip-complete
        # terminal Revision can generate without force-R1 (PX-B-005).
        upper = code.upper()
        if (
            not code[0].isdigit()
            and "-" in upper
            and ("-R" in upper or upper.endswith("R1"))
        ):
            code = "5.1"
        for topic in artefacts.topics or ():
            t_code = str(topic.get("topic_code") or "").strip()
            number = str(topic.get("number") or "").strip()
            if t_code == code or number == code or t_code.startswith(code + "."):
                tid = str(topic.get("topic_id") or "").strip()
                if tid:
                    return tid
            title = str(topic.get("title") or topic.get("text") or "")
            if title.startswith(code + " ") or title.startswith(code + "–"):
                tid = str(topic.get("topic_id") or "").strip()
                if tid:
                    return tid
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
                generated = self._mission_generated_payload(
                    row.mission_instance_id
                )
                chunk_ids = tuple(
                    str(oid).strip()
                    for oid in (generated.get("objective_ids") or ())
                    if str(oid).strip()
                )
                budget_raw = generated.get("session_budget_minutes")
                if budget_raw is None:
                    budget_raw = generated.get("estimated_duration_minutes")
                try:
                    budget = int(budget_raw) if budget_raw is not None else None
                except (TypeError, ValueError):
                    budget = None
                quality = self._quality.build_mission_quality_envelope(
                    template=template,
                    artefacts=artefacts,
                    completed_topic_ids=completed_topic_ids or (),
                    objective_ids=chunk_ids or None,
                    estimated_duration_minutes=budget,
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
        generated_payload = self._mission_generated_payload(row.mission_instance_id)
        educational_package_id = str(
            generated_payload.get("educational_package_id") or ""
        ).strip()
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
            educational_package_id=educational_package_id,
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
