"""Service for managing study plans and week plans.

Study plan generation traverses the canonical curriculum hierarchy:

    Curriculum → Section (display_order) → Topic (display_order) → LearningObjective

For V2 curricula (those with ``Section`` rows) this ordering is enforced
via the two private helpers :meth:`StudyPlanService._load_engine_curriculum_auto`
and :meth:`StudyPlanService._get_engine_topics_ordered`.  V1 curricula (no
sections) continue to use the original flat ``topics`` list so that all
existing study plans and topic-progress records remain unaffected.

Why this improves architectural consistency
-------------------------------------------
Previously, :meth:`_initialize_topic_progress_from_curriculum` called
``engine.load_curriculum()`` which only supports V1, and then accessed
``curriculum.topics`` directly — a flat V1-only attribute that does not
exist on V2 ``CurriculumDefinition`` objects.  As a result, study plans
created against V2 curricula would silently skip all TopicProgress
initialisation.

The refactoring delegates topic ordering to ``_get_engine_topics_ordered``,
which mirrors the canonical DB-side ordering applied by
:meth:`CurriculumService.get_all_topics_ordered`.  No duplication of
traversal logic is introduced: the DB traversal still goes through
``CurriculumService``; the engine-side traversal uses the same
``Section.display_order → Topic.display_order`` rule.

V1 compatibility
-----------------
V1 curricula have no ``sections`` attribute — ``is_v2`` is ``False`` and
``_get_engine_topics_ordered`` returns the original ``curriculum.topics``
list unchanged.  All existing study plans, week plans, TopicProgress rows,
and mission generation paths are unaffected.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from app.extensions import db
from app.models.curriculum import Curriculum, Section, Topic
from app.models.learning import LearningObjective
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


class StudyPlanService:
    """Service for creating and managing study plans."""

    @staticmethod
    def create_study_plan(
        user_id: int,
        exam_name: str,
        exam_sitting: str,
        exam_date: date,
        weekday_study_minutes: int,
        weekend_study_minutes: int,
        current_stage: str,
        study_preference: str,
        target_grade: str,
        preferred_session_minutes: int = 60,
        curriculum_version: str | None = None,
        curriculum_topic_code: str | None = None,
        completed_curriculum_topics: list[str] | None = None,
    ) -> StudyPlan:
        """Create a new study plan with associated week plans.

        Args:
            user_id: The ID of the user creating the study plan.
            exam_name: Name of the exam (e.g., "IFoA CS1").
            exam_sitting: Exam sitting/session (e.g., "April 2027").
            exam_date: The date of the exam.
            weekday_study_minutes: Minutes per weekday for study.
            weekend_study_minutes: Minutes per weekend day for study.
            current_stage: Current study stage (e.g., "Learning", "Revision").
            study_preference: Study preference (Reading First, Questions First, Mixed).
            target_grade: Target grade to achieve.
            preferred_session_minutes: Preferred study session length in minutes.
            curriculum_version: Optional curriculum version this plan was created against.
            curriculum_topic_code: Optional official curriculum topic code (e.g., "1.1").
            completed_curriculum_topics: Optional list of topic codes the user has
                already completed (from the Study Plan Wizard).

        Returns:
            StudyPlan: The created study plan with week plans.

        Raises:
            ValueError: If input validation fails.
        """
        # Validate inputs
        StudyPlanService._validate_study_plan_input(
            exam_date, weekday_study_minutes, weekend_study_minutes
        )

        # Deactivate any existing active study plans for this user
        StudyPlanService.deactivate_user_plans(user_id)

        # Create the study plan
        study_plan = StudyPlan(
            user_id=user_id,
            exam_name=exam_name,
            exam_sitting=exam_sitting,
            exam_date=exam_date,
            weekday_study_minutes=weekday_study_minutes,
            weekend_study_minutes=weekend_study_minutes,
            current_stage=current_stage,
            study_preference=study_preference,
            target_grade=target_grade,
            preferred_session_minutes=preferred_session_minutes,
            curriculum_version=curriculum_version,
            curriculum_topic_code=curriculum_topic_code,
            active=True,
        )

        db.session.add(study_plan)
        db.session.flush()  # Flush to get the study_plan.id

        # Create week plans
        week_plans = StudyPlanService._generate_week_plans(study_plan)
        for week_plan in week_plans:
            db.session.add(week_plan)

        # Initialize TopicProgress from curriculum if applicable
        StudyPlanService._initialize_topic_progress_from_curriculum(
            study_plan,
            completed_curriculum_topics or [],
        )

        db.session.commit()
        return study_plan

    @staticmethod
    def _validate_study_plan_input(
        exam_date: date,
        weekday_study_minutes: int,
        weekend_study_minutes: int,
    ) -> None:
        """Validate study plan input parameters.

        Args:
            exam_date: The exam date to validate.
            weekday_study_minutes: Weekday study time to validate.
            weekend_study_minutes: Weekend study time to validate.

        Raises:
            ValueError: If any validation fails.
        """
        today = date.today()

        if exam_date <= today:
            raise ValueError("Exam date must be in the future.")

        if weekday_study_minutes < 15 or weekday_study_minutes > 480:
            raise ValueError("Weekday study time must be between 15 and 480 minutes.")

        if weekend_study_minutes < 15 or weekend_study_minutes > 480:
            raise ValueError("Weekend study time must be between 15 and 480 minutes.")

    # ── Private engine-loading helpers ────────────────────────────────────

    @staticmethod
    def _load_engine_curriculum_auto(
        organisation: str, paper: str, version: str
    ) -> tuple[Any, bool] | None:
        """Load a curriculum from the engine with automatic V1/V2 detection.

        Delegates to :meth:`CurriculumEngineService.load_auto` — the single
        canonical loader — so V1/V2 detection logic lives in exactly one place.

        Args:
            organisation: Examining body (e.g. ``"IFoA"``).
            paper: Paper code (e.g. ``"CS1"``).
            version: Syllabus version string (e.g. ``"2026"``).

        Returns:
            ``(engine_curriculum, is_v2)`` on success, or ``None`` if the
            curriculum cannot be loaded in either format.
        """
        from app.curriculum.models import CurriculumDefinition
        from app.services.curriculum_engine_service import CurriculumEngineService

        try:
            engine = CurriculumEngineService()
            curriculum = engine.load_auto(organisation, paper, version)
            return curriculum, isinstance(curriculum, CurriculumDefinition)
        except Exception:
            logger.exception(
                "Failed to load curriculum %s/%s/%s.",
                organisation, paper, version,
            )
            return None

    @staticmethod
    def _get_engine_topics_ordered(engine_curriculum: Any, is_v2: bool) -> list:
        """Return engine topics in canonical curriculum order.

        Delegates to :meth:`CurriculumEngineService.get_topics_flat` — the
        single engine-level flattening helper — so traversal logic lives in
        exactly one place.

        Args:
            engine_curriculum: A V1 ``Curriculum`` or a V2
                ``CurriculumDefinition`` from the engine layer.
            is_v2: Unused; format is detected from the curriculum type.
                Kept for API compatibility.

        Returns:
            Flat list of engine topic objects in canonical order.
        """
        from app.services.curriculum_engine_service import CurriculumEngineService

        return CurriculumEngineService.get_topics_flat(engine_curriculum)

    # ── Topic-progress initialisation ─────────────────────────────────────

    @staticmethod
    def _initialize_topic_progress_from_curriculum(
        study_plan: StudyPlan,
        completed_curriculum_topics: list[str] | None = None,
    ) -> None:
        """Initialize TopicProgress records from the curriculum backing this plan.

        When a study plan is created against a known curriculum, this method
        ensures that every topic in the curriculum has a corresponding
        TopicProgress row for the user.  Existing records are left untouched
        so that progress is preserved across plan changes.

        Topics whose ``code`` appears in ``completed_curriculum_topics`` are
        initialised as *study completed* only (completed=True,
        current_stage="Completed", mastery_score unchanged at 0.0).
        Completion never declares Mastery and never co-writes student-felt
        confidence (IA-004 / EIP-001).

        The topic identified by ``curriculum_topic_code`` is promoted as the
        student's *current* topic (``current_stage`` = ``Learning``) when that
        row is not already completed. Existing ``completed=True`` progress is
        never demoted — heal/re-init must not undo mission or wizard progress
        when the plan pointer is stale (common for CS1 topic ``1.1``).

        After initialisation, :meth:`reconcile_current_topic_pointer` advances
        a stale pointer past any completed topics.

        Traversal order
        ---------------
        Topics are enumerated via :meth:`_get_engine_topics_ordered`, which
        applies the canonical ``Section (display_order) → Topic
        (display_order)`` ordering for V2 curricula and the original flat
        ``topics`` list for V1 curricula.  The generator therefore naturally
        carries section context for every topic it processes.
        """
        curriculum_version = study_plan.curriculum_version
        curriculum_topic_code = study_plan.curriculum_topic_code

        if curriculum_version is None:
            return  # Not a curriculum-backed plan — nothing to do.

        if completed_curriculum_topics is None:
            completed_curriculum_topics = []

        # Parse exam_name to extract organisation and paper.
        # Expected format: "<Organisation> <Paper>" (e.g. "IFoA CS1").
        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) != 2:
            logger.debug(
                "Cannot parse exam_name '%s' for curriculum initialisation — skipping.",
                study_plan.exam_name,
            )
            return

        organisation, paper = parts

        # ── Load engine curriculum (V1 first, V2 fallback) ────────────────
        load_result = StudyPlanService._load_engine_curriculum_auto(
            organisation, paper, curriculum_version
        )
        if load_result is None:
            logger.debug(
                "Curriculum %s/%s/%s not found — skipping topic progress init.",
                organisation, paper, curriculum_version,
            )
            return

        engine_curriculum, is_v2 = load_result

        # ── Find or create the SQLAlchemy Curriculum row ──────────────────
        db_curriculum = Curriculum.query.filter_by(
            exam_name=f"{organisation} {paper}",
            version=curriculum_version,
        ).first()
        if db_curriculum is None:
            db_curriculum = Curriculum(
                exam_name=f"{organisation} {paper}",
                version=curriculum_version,
                active=True,
            )
            db.session.add(db_curriculum)
            db.session.flush()

        # Link the study plan to its curriculum.
        study_plan.curriculum_id = db_curriculum.id

        # ── Ensure a Topic + TopicProgress row for every engine topic ─────
        # Topics are enumerated in canonical order: for V2 curricula the
        # iteration traverses Section (display_order) → Topic (display_order)
        # so that section context is naturally available at each step.
        # V1 curricula use the original flat topics list unchanged.

        if is_v2:
            # V2: iterate sections → topics, preserving section context.
            global_order = 0
            for engine_section in sorted(
                engine_curriculum.sections, key=lambda s: s.display_order
            ):
                # Find or create the DB Section row so Topic.section_id can
                # be populated — this lets CurriculumService.get_all_topics_ordered
                # return the correct canonical order from the DB side too.
                db_section = Section.query.filter_by(
                    curriculum_id=db_curriculum.id,
                    code=engine_section.code,
                ).first()
                if db_section is None:
                    db_section = Section(
                        curriculum_id=db_curriculum.id,
                        official_id=engine_section.id,
                        code=engine_section.code,
                        title=engine_section.title,
                        description=getattr(engine_section, "description", None),
                        exam_weight=getattr(engine_section, "exam_weight", None),
                        display_order=engine_section.display_order,
                        estimated_hours=getattr(
                            engine_section, "estimated_hours", None
                        ),
                        difficulty=getattr(engine_section, "difficulty", None),
                    )
                    db.session.add(db_section)
                    db.session.flush()

                # current_section is naturally known here — section context
                # is preserved throughout the inner topic loop.
                for engine_topic in sorted(
                    engine_section.topics, key=lambda t: t.display_order
                ):
                    global_order += 1
                    db_topic = Topic.query.filter_by(
                        curriculum_id=db_curriculum.id,
                        name=engine_topic.title,
                    ).first()
                    if db_topic is None:
                        db_topic = Topic(
                            curriculum_id=db_curriculum.id,
                            name=engine_topic.title,
                            order=global_order,
                            recommended_minutes=engine_topic.estimated_minutes,
                            syllabus_weight=0.0,  # V2 weights live on Section
                            active=True,
                            section_id=db_section.id,
                        )
                        db.session.add(db_topic)
                        db.session.flush()

                        # Persist learning objectives (V2 uses display_order).
                        for engine_lo in sorted(
                            engine_topic.learning_objectives,
                            key=lambda lo: lo.display_order,
                        ):
                            db.session.add(LearningObjective(
                                topic_id=db_topic.id,
                                description=(
                                    f"[{engine_lo.code}] {engine_lo.description}"
                                ),
                                order=engine_lo.display_order,
                                active=True,
                            ))

                    StudyPlanService._create_topic_progress_if_absent(
                        study_plan, db_topic, engine_topic.code,
                        completed_curriculum_topics,
                    )

        else:
            # V1: original flat-topic enumeration — unchanged behaviour.
            for order, engine_topic in enumerate(engine_curriculum.topics, start=1):
                db_topic = Topic.query.filter_by(
                    curriculum_id=db_curriculum.id,
                    name=engine_topic.title,
                ).first()
                if db_topic is None:
                    db_topic = Topic(
                        curriculum_id=db_curriculum.id,
                        name=engine_topic.title,
                        order=order,
                        recommended_minutes=int(engine_topic.estimated_hours * 60),
                        syllabus_weight=engine_topic.weighting,
                        active=True,
                    )
                    db.session.add(db_topic)
                    db.session.flush()

                    # Persist learning objectives (V1 uses enumeration order).
                    for lo_order, engine_lo in enumerate(
                        engine_topic.learning_outcomes, start=1
                    ):
                        db.session.add(LearningObjective(
                            topic_id=db_topic.id,
                            description=(
                                f"[{engine_lo.code}] {engine_lo.description}"
                            ),
                            order=lo_order,
                            active=True,
                        ))

                StudyPlanService._create_topic_progress_if_absent(
                    study_plan, db_topic, engine_topic.code,
                    completed_curriculum_topics,
                )

        # EIP-005: after target syllabus units exist, continue learner history
        # from prior curricula of the same exam by objective topic-code match.
        # Existing progress on the target curriculum is never overwritten.
        from app.services.educational_continuity_service import (
            EducationalContinuityService,
        )

        EducationalContinuityService.remap_study_progress_to_curriculum(
            study_plan.user_id,
            db_curriculum,
            exam_name=study_plan.exam_name,
        )

        # ── Mark the selected topic as the student's current topic ────────
        if curriculum_topic_code is None:
            return  # No current topic selected — all topics stay "Not Started".

        engine_topics = StudyPlanService._get_engine_topics_ordered(
            engine_curriculum, is_v2
        )
        for engine_topic in engine_topics:
            if engine_topic.code != curriculum_topic_code:
                continue

            db_topic = Topic.query.filter_by(
                curriculum_id=db_curriculum.id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                continue

            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is None:
                # Should not normally happen, but guard anyway.
                continue

            # Preserve earned / declared completion. Demoting here caused CS1
            # 1.1 (and other first topics) to uncheck on refresh when the plan
            # pointer still named a completed topic.
            if tp.completed:
                break

            # EIP-005: promote live pointer without erasing Estimated Knowledge /
            # Mastery continuity already held on this TopicProgress row.
            tp.current_stage = TopicProgress.STAGE_LEARNING
            tp.completed = False
            break

        StudyPlanService.reconcile_current_topic_pointer(study_plan)

    @staticmethod
    def reconcile_current_topic_pointer(study_plan: StudyPlan) -> None:
        """Advance ``curriculum_topic_code`` past topics already completed.

        Mission completion updates TopicProgress but historically left the
        plan pointer unchanged. A stale pointer on the first topic (e.g.
        ``1.1``) then caused heal/re-init and edit sync to treat that topic
        as the live learning target and reset ``completed`` to ``False``.

        Idempotent: no-op when the pointer is already on an incomplete topic
        or when the plan is not curriculum-backed.

        Args:
            study_plan: The study plan whose pointer may need advancing.
        """
        if (
            not study_plan.curriculum_id
            or not study_plan.curriculum_version
            or not study_plan.curriculum_topic_code
        ):
            return

        parts = (study_plan.exam_name or "").split(" ", 1)
        if len(parts) != 2:
            return

        organisation, paper = parts
        load_result = StudyPlanService._load_engine_curriculum_auto(
            organisation, paper, study_plan.curriculum_version
        )
        if load_result is None:
            return

        engine_curriculum, is_v2 = load_result
        engine_topics = StudyPlanService._get_engine_topics_ordered(
            engine_curriculum, is_v2
        )

        completed_codes: set[str] = set()
        for engine_topic in engine_topics:
            db_topic = Topic.query.filter_by(
                curriculum_id=study_plan.curriculum_id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                continue
            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is not None and tp.completed:
                completed_codes.add(engine_topic.code)

        if study_plan.curriculum_topic_code not in completed_codes:
            return

        for engine_topic in engine_topics:
            if engine_topic.code in completed_codes:
                continue
            study_plan.curriculum_topic_code = engine_topic.code
            db_topic = Topic.query.filter_by(
                curriculum_id=study_plan.curriculum_id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                return
            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is not None and not tp.completed:
                tp.current_stage = TopicProgress.STAGE_LEARNING
            return

        # Entire syllabus completed — clear the live pointer.
        study_plan.curriculum_topic_code = None

    @staticmethod
    def _create_topic_progress_if_absent(
        study_plan: StudyPlan,
        db_topic: Topic,
        engine_topic_code: str,
        completed_curriculum_topics: list[str],
    ) -> None:
        """Create a TopicProgress row for *db_topic* if one does not already exist.

        Extracted from :meth:`_initialize_topic_progress_from_curriculum` to
        avoid repeating the creation logic in both the V1 and V2 branches.

        Args:
            study_plan: The study plan being initialised.
            db_topic: The DB Topic row to create progress for.
            engine_topic_code: The engine-side topic code (e.g. ``"1.1"``).
            completed_curriculum_topics: Codes of topics the user has already
                completed (from the Study Plan Wizard).
        """
        existing = TopicProgress.query.filter_by(
            user_id=study_plan.user_id,
            topic_id=db_topic.id,
        ).first()
        if existing is not None:
            return  # Existing progress is preserved unchanged.

        is_completed = engine_topic_code in completed_curriculum_topics

        # EIP-001 / EL-001 / IA-004: Manual topic completion writes Study
        # Progress only. Never invent Mastery or student-felt confidence
        # from a coverage declaration.
        db.session.add(TopicProgress(
            user_id=study_plan.user_id,
            topic_id=db_topic.id,
            confidence="Not Started",
            completed=is_completed,
            mastery_score=0.0,
            revision_count=0,
            last_reviewed=None,
            current_stage=(
                TopicProgress.STAGE_COMPLETED
                if is_completed
                else TopicProgress.STAGE_NOT_STARTED
            ),
        ))

    @staticmethod
    def _generate_week_plans(study_plan: StudyPlan) -> list[WeekPlan]:
        """Generate week plans from study start date to exam date.
        
        For curriculum-backed study plans (those with both
        ``curriculum_version`` and ``curriculum_topic_code`` set), week
        plans are paced according to the official curriculum topic order
        loaded from the Curriculum Engine.  Otherwise, a simple date-based
        week-plan grid is produced.

        Args:
            study_plan: The study plan to generate weeks for.
        
        Returns:
            list[WeekPlan]: List of generated week plans.
        """
        # ── Try curriculum-backed sequencing first ──────────────────────
        if study_plan.curriculum_version and study_plan.curriculum_topic_code:
            from app.services.planning_service import PlanningService
            curriculum_weeks = PlanningService.generate_curriculum_week_plans(study_plan)
            if curriculum_weeks:
                return curriculum_weeks

        # ── Fall back to simple date-based grid ─────────────────────────
        today = date.today()
        exam_date = study_plan.exam_date

        # Find the Monday of the current week
        days_since_monday = today.weekday()
        start_of_week = today - timedelta(days=days_since_monday)

        week_plans = []
        week_number = 1
        current_week_start = start_of_week

        while current_week_start < exam_date:
            current_week_end = current_week_start + timedelta(days=6)

            # Clamp the end date to the exam date if necessary
            if current_week_end >= exam_date:
                current_week_end = exam_date - timedelta(days=1)

            week_plan = WeekPlan(
                study_plan_id=study_plan.id,
                week_number=week_number,
                start_date=current_week_start,
                end_date=current_week_end,
            )
            week_plans.append(week_plan)

            current_week_start = current_week_end + timedelta(days=1)
            week_number += 1

        return week_plans

    @staticmethod
    def get_user_active_plan(user_id: int) -> StudyPlan | None:
        """Get the active study plan for a user.

        Self-heals curriculum binding when the exam has an on-disk syllabus.
        Callers may assume a returned curriculum-backed plan is already valid.

        Args:
            user_id: The user ID.

        Returns:
            StudyPlan | None: The active study plan or None if not found.
        """
        study_plan = StudyPlan.query.filter_by(
            user_id=user_id, active=True
        ).first()
        if study_plan is None:
            return None
        StudyPlanService.ensure_curriculum_binding(study_plan)
        return study_plan

    @staticmethod
    def get_plan(
        study_plan_id: int, user_id: int | None = None
    ) -> StudyPlan | None:
        """Load a study plan by id, self-healing curriculum binding.

        This is the canonical single-plan access path. Prefer it over raw
        ``StudyPlan.query.get`` so legacy unbound plans are repaired once
        before any consumer uses them.

        Args:
            study_plan_id: The study plan primary key.
            user_id: Optional owner check. When provided and the plan belongs
                to another user, returns ``None`` (does not raise).

        Returns:
            StudyPlan | None: The healed plan, or ``None`` if missing / not owned.
        """
        study_plan = db.session.get(StudyPlan, study_plan_id)
        if study_plan is None:
            return None
        if user_id is not None and study_plan.user_id != user_id:
            return None
        StudyPlanService.ensure_curriculum_binding(study_plan)
        return study_plan

    @staticmethod
    def ensure_curriculum_binding(study_plan: StudyPlan) -> bool:
        """Bind an unbound study plan to its on-disk syllabus when discoverable.

        Product invariant (Capability 4.6): every curriculum-backed study plan
        must eventually have ``curriculum_id``, ``curriculum_version``, and
        TopicProgress rows. Plans created before discovery-driven version
        resolution may lack either identity field; this method repairs them
        transparently.

        Trigger: ``curriculum_id`` is ``None`` **or** ``curriculum_version``
        is ``None``. Idempotent and paper-agnostic — discovers the latest
        on-disk version for the plan's organisation/paper, initialises
        TopicProgress (which also sets ``curriculum_id``), and persists.

        Args:
            study_plan: The study plan to inspect and possibly bind.

        Returns:
            bool: ``True`` when the plan is curriculum-bound after this call
            (``curriculum_id`` and ``curriculum_version`` both set). ``False``
            when the exam has no on-disk syllabus (genuine non-curriculum plan).
        """
        if study_plan.curriculum_id and study_plan.curriculum_version:
            return True

        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.examination_catalogue import parse_exam_name

        organisation, paper = parse_exam_name(study_plan.exam_name or "")
        if not organisation or not paper:
            parts = (study_plan.exam_name or "").split(" ", 1)
            if len(parts) != 2:
                logger.debug(
                    "Cannot parse exam_name %r for curriculum binding — skipping.",
                    study_plan.exam_name,
                )
                return False
            organisation, paper = parts

        version = study_plan.curriculum_version
        if not version:
            engine = CurriculumEngineService()
            versions = engine.list_supported_versions(organisation, paper)
            if not versions:
                logger.debug(
                    "No on-disk curriculum for %s/%s — leaving plan %s unbound.",
                    organisation,
                    paper,
                    study_plan.id,
                )
                return False
            version = max(versions)
            study_plan.curriculum_version = version
            logger.info(
                "Discovered curriculum version %s for unbound plan %s (%s/%s).",
                version,
                study_plan.id,
                organisation,
                paper,
            )

        StudyPlanService._initialize_topic_progress_from_curriculum(study_plan)
        db.session.commit()

        bound = bool(
            study_plan.curriculum_id and study_plan.curriculum_version
        )
        if bound:
            logger.info(
                "Bound study plan %s to curriculum_id=%s version=%s",
                study_plan.id,
                study_plan.curriculum_id,
                study_plan.curriculum_version,
            )
        else:
            logger.warning(
                "Curriculum binding failed for study plan %s (%s version=%s)",
                study_plan.id,
                study_plan.exam_name,
                study_plan.curriculum_version,
            )
        return bound

    @staticmethod
    def deactivate_user_plans(user_id: int) -> None:
        """Deactivate all study plans for a user.

        Args:
            user_id: The user ID.
        """
        StudyPlan.query.filter_by(user_id=user_id, active=True).update({"active": False})
        db.session.commit()

    @staticmethod
    def set_active_plan(study_plan_id: int, user_id: int) -> StudyPlan:
        """Set a specific study plan as active for a user.

        After committing the active flag, synchronizes derived student-facing
        state (today's mission) so dashboard / mission / recommendation
        surfaces observe the new plan without a manual refresh (IA-002).

        Args:
            study_plan_id: The ID of the study plan to activate.
            user_id: The ID of the user (for authorization).

        Returns:
            StudyPlan: The activated study plan.

        Raises:
            ValueError: If the study plan doesn't exist or doesn't belong to the user.
        """
        study_plan = db.session.get(StudyPlan, study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(
                f"Study plan {study_plan_id} does not belong to user {user_id}"
            )

        StudyPlanService.ensure_curriculum_binding(study_plan)

        # Deactivate other plans
        StudyPlanService.deactivate_user_plans(user_id)

        # Activate this plan
        study_plan.active = True
        db.session.commit()

        StudyPlanService.synchronize_student_surfaces(user_id)
        return study_plan

    @staticmethod
    def synchronize_student_surfaces(user_id: int) -> None:
        """Align derived student surfaces with the DB active study plan.

        The active ``StudyPlan`` row remains the single source of truth. This
        method only regenerates/binds today's mission for that plan so
        subsequent dashboard and mission renders need no browser refresh.
        No Flask-session or client-side plan cache is introduced (IA-002).
        """
        from app.services.planning_service import PlanningService

        PlanningService.generate_today_mission(user_id)

    @staticmethod
    def update_study_plan(
        study_plan_id: int,
        user_id: int,
        **kwargs,
    ) -> StudyPlan:
        """Update an existing study plan's details and regenerate week plans.

        Args:
            study_plan_id: The ID of the study plan to update.
            user_id: The ID of the user (for authorization).
            **kwargs: Fields to update (exam_name, exam_sitting, exam_date,
                weekday_study_minutes, weekend_study_minutes, current_stage,
                study_preference, target_grade, preferred_session_minutes,
                curriculum_topic_code, completed_curriculum_topics).

        Returns:
            StudyPlan: The updated study plan.

        Raises:
            ValueError: If the plan doesn't exist, doesn't belong to the user,
                or validation fails.
        """
        study_plan = db.session.get(StudyPlan, study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(
                f"Study plan {study_plan_id} does not belong to user {user_id}"
            )

        StudyPlanService.ensure_curriculum_binding(study_plan)

        if study_plan.archived:
            raise ValueError("Cannot edit an archived study plan.")

        # List of allowed scalar fields that can be updated
        updatable_fields = {
            "exam_name",
            "exam_sitting",
            "exam_date",
            "weekday_study_minutes",
            "weekend_study_minutes",
            "current_stage",
            "study_preference",
            "target_grade",
            "preferred_session_minutes",
            "curriculum_topic_code",
            "curriculum_version",
        }

        # Validate new values for study minutes if provided
        test_weekday = kwargs.get("weekday_study_minutes", study_plan.weekday_study_minutes)
        test_weekend = kwargs.get("weekend_study_minutes", study_plan.weekend_study_minutes)
        test_exam_date = kwargs.get("exam_date", study_plan.exam_date)
        StudyPlanService._validate_study_plan_input(test_exam_date, test_weekday, test_weekend)

        # Apply scalar updates
        for field in updatable_fields:
            if field in kwargs:
                setattr(study_plan, field, kwargs[field])

        db.session.flush()

        # Regenerate week plans (delete old, create new)
        WeekPlan.query.filter_by(study_plan_id=study_plan.id).delete()
        week_plans = StudyPlanService._generate_week_plans(study_plan)
        for week_plan in week_plans:
            db.session.add(week_plan)

        # Update completed curriculum topics if provided and plan is curriculum-backed
        completed_topics = kwargs.get("completed_curriculum_topics")
        if completed_topics is not None and study_plan.curriculum_version:
            curriculum_topic_code = kwargs.get(
                "curriculum_topic_code", study_plan.curriculum_topic_code
            )
            StudyPlanService._sync_completed_topics(
                study_plan, completed_topics, curriculum_topic_code
            )
        elif (
            completed_topics is not None
            and "curriculum_version" in kwargs
            and kwargs["curriculum_version"]
        ):
            curriculum_topic_code = kwargs.get(
                "curriculum_topic_code", study_plan.curriculum_topic_code
            )
            StudyPlanService._sync_completed_topics(
                study_plan, completed_topics, curriculum_topic_code
            )

        db.session.commit()
        return study_plan

    @staticmethod
    def _sync_completed_topics(
        study_plan: StudyPlan,
        completed_codes: list[str],
        curriculum_topic_code: str | None,
    ) -> None:
        """Synchronise TopicProgress completed status with the supplied list.

        Topics whose engine code appears in *completed_codes* are marked as
        completed. Explicit completion wins over a stale
        ``curriculum_topic_code`` pointer — callers should advance the
        pointer (and this method reconciles it afterward).

        Topics NOT in the list that were previously completed are reset to
        ``Not Started`` (so the user can un-check a previously completed
        topic). The live current topic, when not in *completed_codes*, is
        set to Learning.

        Topics are visited in canonical curriculum order (Section → Topic
        for V2, flat list for V1) via :meth:`_get_engine_topics_ordered`.
        """
        from app.models.curriculum import Topic as DBTopic

        if not study_plan.curriculum_id or not study_plan.curriculum_version:
            return

        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) != 2:
            return

        organisation, paper = parts

        load_result = StudyPlanService._load_engine_curriculum_auto(
            organisation, paper, study_plan.curriculum_version
        )
        if load_result is None:
            logger.debug(
                "Curriculum %s/%s/%s not found — skipping topic sync.",
                organisation, paper, study_plan.curriculum_version,
            )
            return

        engine_curriculum, is_v2 = load_result
        engine_topics = StudyPlanService._get_engine_topics_ordered(
            engine_curriculum, is_v2
        )
        completed_set = set(completed_codes)

        for engine_topic in engine_topics:
            db_topic = DBTopic.query.filter_by(
                curriculum_id=study_plan.curriculum_id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                continue

            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is None:
                continue

            is_current = (
                curriculum_topic_code
                and engine_topic.code == curriculum_topic_code
            )
            in_completed = engine_topic.code in completed_set

            if in_completed:
                # EIP-001 / EL-001: Study Progress only — do not write mastery
                # or student-felt confidence from coverage edits.
                tp.completed = True
                tp.current_stage = TopicProgress.STAGE_COMPLETED
            elif is_current:
                tp.completed = False
                tp.current_stage = TopicProgress.STAGE_LEARNING
            elif tp.completed:
                tp.completed = False
                tp.current_stage = TopicProgress.STAGE_NOT_STARTED

        StudyPlanService.reconcile_current_topic_pointer(study_plan)

    @staticmethod
    def sync_declared_completed_topics(
        study_plan_id: int,
        user_id: int,
        completed_codes: list[str],
    ) -> None:
        """Apply declared coverage from Educational History to Study Progress."""
        study_plan = StudyPlanService.get_plan(study_plan_id, user_id=user_id)
        if study_plan is None:
            return
        StudyPlanService._sync_completed_topics(
            study_plan,
            completed_codes,
            study_plan.curriculum_topic_code,
        )
        db.session.commit()

    @staticmethod
    def delete_study_plan(study_plan_id: int, user_id: int) -> None:
        """Permanently delete a Study Plan's planning artefacts only.

        EIP-005 Educational Continuity: educational history belongs to the
        learner. Deleting a Study Plan removes planning metadata and week
        schedules, and clears temporary mission plan pointers. It must not
        delete Study Progress, Study Attempts, Educational Evidence posture,
        Estimated Knowledge, or Estimated Mastery.

        Args:
            study_plan_id: The ID of the study plan to delete.
            user_id: The ID of the user (for authorization).

        Raises:
            ValueError: If the plan doesn't exist or doesn't belong to the user.
        """
        from app.services.educational_continuity_service import (
            EducationalContinuityService,
        )

        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        # Detach disposable plan context; retain learner educational history.
        EducationalContinuityService.release_plan_planning_artifacts(study_plan)

        # Week plans cascade via delete-orphan. TopicProgress is intentionally
        # untouched — it is learner-owned Study Progress / estimate storage.
        db.session.delete(study_plan)
        db.session.commit()

    @staticmethod
    def archive_study_plan(study_plan_id: int, user_id: int) -> StudyPlan:
        """Archive a study plan — preserve history but remove from active scheduling.

        If the plan being archived is currently active, it is deactivated
        so that no new missions are generated from it.

        Args:
            study_plan_id: The ID of the study plan to archive.
            user_id: The ID of the user (for authorization).

        Returns:
            StudyPlan: The archived study plan.

        Raises:
            ValueError: If the plan doesn't exist or doesn't belong to the user.
        """
        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        study_plan.archived = True
        study_plan.active = False
        db.session.commit()
        return study_plan

    @staticmethod
    def get_user_plans(
        user_id: int, include_archived: bool = False
    ) -> list[StudyPlan]:
        """Get all study plans for a user.

        Args:
            user_id: The user ID.
            include_archived: If True, also return archived plans.

        Returns:
            list[StudyPlan]: List of study plans ordered by creation date (newest first).
        """
        query = StudyPlan.query.filter_by(user_id=user_id)
        if not include_archived:
            query = query.filter_by(archived=False)
        plans = query.order_by(StudyPlan.created_at.desc()).all()
        for plan in plans:
            StudyPlanService.ensure_curriculum_binding(plan)
        return plans

    @staticmethod
    def get_current_week_plan(study_plan: StudyPlan) -> WeekPlan | None:
        """Get the current week plan for a study plan.

        Args:
            study_plan: The study plan.

        Returns:
            WeekPlan | None: The current week plan or None if not found.
        """
        today = date.today()
        return WeekPlan.query.filter(
            WeekPlan.study_plan_id == study_plan.id,
            WeekPlan.start_date <= today,
            WeekPlan.end_date >= today,
        ).first()
