"""Service for managing curriculum and topic data.

This service owns DB import, progress helpers, and the **canonical
curriculum traversal** path used by the rest of the application.

Sections are the primary grouping for V2 curricula
(``Curriculum → Section → Topic → LearningObjective``).  V1 curricula
have no sections; helpers fall back to the ``parent_topic_id`` topic
tree so existing study plans and readiness calculations stay unchanged.

Import uses the Curriculum Engine's automatic format detection to
support both V1 (flat) and V2 (hierarchical) JSON.
"""

from __future__ import annotations

import logging
from typing import Any

from app.extensions import db
from app.models.curriculum import Curriculum, Section, Topic
from app.models.learning import LearningObjective
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


class CurriculumService:
    """Service for curriculum operations and topic management.

    Provides methods for loading curricula, retrieving topics, tracking
    progress through curriculum topics, and idempotently importing
    bundled curriculum data into the database.

    Prefer :meth:`get_sections`, :meth:`get_topics_for_section`,
    :meth:`get_all_topics_ordered`, and
    :meth:`get_learning_objectives_for_topic` over ad-hoc topic queries
    so V1/V2 ordering stays consistent.
    """

    # ── Idempotent import ──────────────────────────────────────────────

    @staticmethod
    def import_curricula() -> int:
        """Import all bundled curricula from the Curriculum Engine into the
        database.

        This method is **idempotent** — safe to call on every application
        startup.  If a ``(exam_name, version)`` record already exists in the
        ``curricula`` table the import is skipped for that curriculum (no
        duplicate rows are created, no existing rows are modified).

        The method uses the Curriculum Engine's automatic format detection
        to support both V1 (flat) and V2 (hierarchical) curriculum formats.

        Returns:
            The number of curricula that were newly imported (0 if all were
            already present).
        """
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        discovered = repo.list_exams()  # [(org, paper, [versions])]

        imported_count = 0
        skipped_count = 0
        error_count = 0

        logger.info("Starting curriculum import. Discovered %d exam(s).", len(discovered))

        for organisation, paper, versions in discovered:
            for version in versions:
                # ── Load from engine with format auto-detection ───────
                try:
                    engine_curriculum = CurriculumService._load_curriculum_auto(
                        repo, organisation, paper, version
                    )
                except Exception as e:
                    logger.exception(
                        "Failed to load curriculum %s/%s/%s — skipping. Error: %s",
                        organisation, paper, version, str(e),
                    )
                    error_count += 1
                    continue

                # ── Detect format ─────────────────────────────────────
                is_v2 = isinstance(engine_curriculum, CurriculumDefinition)
                format_version = "V2" if is_v2 else "V1"
                logger.debug(
                    "Detected %s format for %s %s %s",
                    format_version, organisation, paper, version,
                )

                # ── Build exam_name ───────────────────────────────────
                # DB exam_name follows the product convention "<Provider> <Paper>"
                # (e.g. "IFoA CS1") so study plans and catalogue lookups stay
                # aligned. The official examination title remains on the engine
                # definition (exam_name / description) and in syllabus metadata.
                if is_v2:
                    exam_name = (
                        f"{engine_curriculum.provider} {engine_curriculum.exam_code}"
                    )
                else:
                    exam_name = (
                        f"{engine_curriculum.organisation} {engine_curriculum.paper}"
                    )

                # ── Idempotency check ─────────────────────────────────
                existing = Curriculum.query.filter_by(
                    exam_name=exam_name,
                    version=version,
                ).first()
                if existing is not None:
                    logger.debug(
                        "Curriculum %s v%s already exists — skipping import.",
                        exam_name, version,
                    )
                    skipped_count += 1
                    continue

                # ── Create DB Curriculum row ──────────────────────────
                db_curriculum = Curriculum(
                    exam_name=exam_name,
                    version=version,
                    active=True,
                )
                db.session.add(db_curriculum)
                db.session.flush()  # get db_curriculum.id

                # ── Import sections, topics, and learning objectives ──
                if is_v2:
                    sections_created, topics_imported, los_imported = (
                        CurriculumService._import_v2_topics(
                            db_curriculum, engine_curriculum
                        )
                    )
                else:
                    topics_imported, los_imported = CurriculumService._import_v1_topics(
                        db_curriculum, engine_curriculum
                    )
                    sections_created = 0

                db.session.flush()
                imported_count += 1
                logger.info(
                    "Imported %s curriculum %s v%s: %d sections created, "
                    "%d topics, %d learning objectives",
                    format_version, exam_name, version,
                    sections_created, topics_imported, los_imported,
                )

        if imported_count:
            db.session.commit()

        logger.info(
            "Curriculum import complete: %d imported, %d skipped, %d errors",
            imported_count, skipped_count, error_count,
        )

        return imported_count

    @staticmethod
    def _load_curriculum_auto(
        repo: Any, organisation: str, paper: str, version: str
    ) -> Any:
        """Load a curriculum with automatic format detection.

        Delegates to :meth:`CurriculumRepository.load_auto` — the single
        canonical loader — so V1/V2 detection logic lives in exactly one place.

        Args:
            repo: The CurriculumRepository instance.
            organisation: Examining body (e.g., 'ifoa').
            paper: Paper code (e.g., 'cs1').
            version: Syllabus version year (e.g., '2026').

        Returns:
            A Curriculum (V1) or CurriculumDefinition (V2) instance.

        Raises:
            CurriculumLoadError: If the file cannot be loaded in either format.
        """
        return repo.load_auto(organisation, paper, version)

    @staticmethod
    def _import_v1_topics(
        db_curriculum: Curriculum, engine_curriculum: Any
    ) -> tuple[int, int]:
        """Import topics from a V1 curriculum into the database.

        Args:
            db_curriculum: The database Curriculum record.
            engine_curriculum: The V1 Curriculum from the engine.

        Returns:
            A tuple of (topics_imported, learning_objectives_imported).
        """
        topics_count = 0
        los_count = 0

        for order, engine_topic in enumerate(engine_curriculum.topics, start=1):
            db_topic = Topic(
                curriculum_id=db_curriculum.id,
                name=engine_topic.title,
                order=order,
                recommended_minutes=int(engine_topic.estimated_hours * 60),
                syllabus_weight=engine_topic.weighting,
                active=True,
            )
            db.session.add(db_topic)
            db.session.flush()  # get db_topic.id

            for lo_order, engine_lo in enumerate(
                engine_topic.learning_outcomes, start=1
            ):
                db_lo = LearningObjective(
                    topic_id=db_topic.id,
                    description=(
                        f"[{engine_lo.code}] {engine_lo.description}"
                    ),
                    order=lo_order,
                    active=True,
                )
                db.session.add(db_lo)
                los_count += 1

            topics_count += 1

        return topics_count, los_count

    @staticmethod
    def _import_v2_topics(
        db_curriculum: Curriculum, engine_curriculum: Any
    ) -> tuple[int, int, int]:
        """Import sections, topics, and learning objectives from a V2 curriculum.

        V2 curricula have a hierarchical structure (sections → topics → learning
        objectives). This method persists the full hierarchy:

        1. Creates a ``Section`` DB row for every ``SectionDefinition``.
        2. Creates a ``Topic`` DB row for every ``TopicDefinition`` and sets
           ``Topic.section_id`` to the owning section's primary key.
        3. Creates a ``LearningObjective`` DB row for every learning objective.

        Args:
            db_curriculum: The database Curriculum record (already flushed).
            engine_curriculum: The V2 CurriculumDefinition from the engine.

        Returns:
            A tuple of (sections_created, topics_imported, los_imported).
        """
        sections_count = 0
        topics_count = 0
        los_count = 0
        global_topic_order = 0

        # Sort so Topic.order reflects official display_order even if the
        # engine list arrives unsorted.
        for section in sorted(
            engine_curriculum.sections, key=lambda s: s.display_order
        ):
            db_section = Section(
                curriculum_id=db_curriculum.id,
                official_id=section.id,
                code=section.code,
                title=section.title,
                description=section.description,
                exam_weight=section.exam_weight,
                display_order=section.display_order,
                estimated_hours=section.estimated_hours,
                difficulty=section.difficulty,
            )
            db.session.add(db_section)
            db.session.flush()  # get db_section.id before linking topics

            logger.info(
                "V2 [%s v%s] Section created: %s %r (order=%d, weight=%.1f)",
                db_curriculum.exam_name, db_curriculum.version,
                section.code, section.title,
                section.display_order, section.exam_weight,
            )
            sections_count += 1

            for engine_topic in sorted(
                section.topics, key=lambda t: t.display_order
            ):
                global_topic_order += 1

                db_topic = Topic(
                    curriculum_id=db_curriculum.id,
                    name=engine_topic.title,
                    order=global_topic_order,
                    recommended_minutes=engine_topic.estimated_minutes,
                    syllabus_weight=0.0,  # V2 uses section weights, not topic weights
                    active=True,
                    section_id=db_section.id,
                )
                db.session.add(db_topic)
                db.session.flush()  # get db_topic.id before linking LOs

                for engine_lo in sorted(
                    engine_topic.learning_objectives,
                    key=lambda lo: lo.display_order,
                ):
                    db_lo = LearningObjective(
                        topic_id=db_topic.id,
                        description=(
                            f"[{engine_lo.code}] {engine_lo.description}"
                        ),
                        order=engine_lo.display_order,
                        active=True,
                    )
                    db.session.add(db_lo)
                    los_count += 1

                topics_count += 1

        logger.debug(
            "V2 import complete: %d sections, %d topics, %d learning objectives",
            sections_count, topics_count, los_count,
        )

        return sections_count, topics_count, los_count

    # ── Curriculum traversal helpers ───────────────────────────────────
    #
    # These helpers are the canonical way to walk a curriculum's structure.
    # Services should prefer these over calling model methods directly so
    # that section-aware ordering is applied consistently everywhere.

    @staticmethod
    def get_sections(curriculum: Curriculum) -> list[Section]:
        """Return all sections for a curriculum ordered by display_order.

        Sections are the V2 top-level grouping that sits between a
        :class:`Curriculum` and its :class:`Topic` records.  V1 curricula
        have no sections, so this returns an empty list for them.

        Args:
            curriculum: The curriculum object.

        Returns:
            Sections sorted by ``display_order``, or ``[]`` for V1 curricula.
        """
        return (
            Section.query.filter_by(curriculum_id=curriculum.id)
            .order_by(Section.display_order)
            .all()
        )

    @staticmethod
    def get_topics_for_section(section: Section) -> list[Topic]:
        """Return active topics belonging to a section, ordered by their order field.

        Args:
            section: The section object.

        Returns:
            Active topics in this section, ordered by ``Topic.order``.
        """
        return (
            Topic.query.filter_by(section_id=section.id, active=True)
            .order_by(Topic.order)
            .all()
        )

    @staticmethod
    def get_all_topics_ordered(curriculum: Curriculum) -> list[Topic]:
        """Return all active topics in canonical traversal order.

        Sections are the primary grouping for V2 curricula.  When a
        curriculum has :class:`Section` rows the traversal order becomes::

            Section (display_order) → Topic (order)

        For V1 curricula (no sections) the original ``parent_topic_id``
        depth-first tree is used unchanged so that existing study plans,
        mission generation, and readiness calculations remain unaffected.

        Args:
            curriculum: The curriculum object.

        Returns:
            All active topics in canonical order.
        """
        sections = CurriculumService.get_sections(curriculum)
        if sections:
            # V2 path — topics are owned by sections; ordering is
            # Section.display_order then Topic.order within each section.
            topics: list[Topic] = []
            for section in sections:
                topics.extend(CurriculumService.get_topics_for_section(section))
            return topics
        # V1 path — no sections; fall back to parent_topic_id depth-first tree.
        return curriculum.get_all_topics_ordered()

    @staticmethod
    def get_learning_objectives_for_topic(topic: Topic) -> list[LearningObjective]:
        """Return active learning objectives for a topic ordered by ``order``.

        Completes the canonical hierarchy after topics:
        ``Section → Topic → LearningObjective (display_order / order)``.

        Args:
            topic: The topic object.

        Returns:
            Active learning objectives sorted by ``LearningObjective.order``.
        """
        return (
            LearningObjective.query.filter_by(topic_id=topic.id, active=True)
            .order_by(LearningObjective.order)
            .all()
        )

    # ── Existing query methods ─────────────────────────────────────────

    @staticmethod
    def get_curriculum_by_id(curriculum_id: int) -> Curriculum | None:
        """Get a curriculum by ID.

        Args:
            curriculum_id: The curriculum ID.

        Returns:
            Curriculum: The curriculum object, or None if not found.
        """
        return db.session.get(Curriculum, curriculum_id)

    @staticmethod
    def get_curriculum_by_exam(exam_name: str) -> Curriculum | None:
        """Get the active curriculum for an exam by name.

        If multiple curricula exist for the same exam, returns the most recent.

        Args:
            exam_name: The exam name (e.g., "IFoA CS1").

        Returns:
            Curriculum: The active curriculum, or None if not found.
        """
        return (
            Curriculum.query.filter_by(
                exam_name=exam_name,
                active=True,
            )
            .order_by(Curriculum.version.desc())
            .first()
        )

    @staticmethod
    def get_ordered_topics(curriculum: Curriculum) -> list[Topic]:
        """Get all topics in a curriculum in recommended order.

        Delegates to :meth:`get_all_topics_ordered`, which applies section-
        aware ordering for V2 curricula and the ``parent_topic_id`` tree for
        V1 curricula.

        Args:
            curriculum: The curriculum object.

        Returns:
            list[Topic]: All active topics in canonical order.
        """
        return CurriculumService.get_all_topics_ordered(curriculum)

    @staticmethod
    def get_next_incomplete_topic(
        user_id: int,
        curriculum: Curriculum,
    ) -> Topic | None:
        """Get the next topic that the user hasn't completed.

        This returns the first topic in curriculum order that:
        1. Is a leaf topic (has no active subtopics)
        2. Has not been marked as completed by the user

        If all topics are completed, returns None.

        Args:
            user_id: The ID of the user.
            curriculum: The curriculum object.

        Returns:
            Topic: The next incomplete leaf topic, or None if all completed.
        """
        ordered_topics = CurriculumService.get_ordered_topics(curriculum)

        # Filter to leaf topics only (no active subtopics)
        leaf_topics = [t for t in ordered_topics if t.is_leaf_topic()]

        for topic in leaf_topics:
            # Check if user has progress for this topic
            progress = TopicProgress.query.filter_by(
                user_id=user_id,
                topic_id=topic.id,
            ).first()

            # If no progress exists or not completed, this is the next topic
            if not progress or not progress.completed:
                return topic

        # All topics completed
        return None

    @staticmethod
    def get_curriculum_progress(
        user_id: int,
        curriculum: Curriculum,
    ) -> dict:
        """Get progress statistics for a curriculum.

        Returns a dictionary with:
        - total_topics: Total number of leaf topics
        - completed_topics: Number of completed leaf topics
        - completion_percentage: Percentage of topics completed (0-100)
        - topics_by_confidence: Count of topics at each confidence level

        Args:
            user_id: The ID of the user.
            curriculum: The curriculum object.

        Returns:
            dict: Progress statistics.
        """
        ordered_topics = CurriculumService.get_ordered_topics(curriculum)
        leaf_topics = [t for t in ordered_topics if t.is_leaf_topic()]

        total_topics = len(leaf_topics)
        completed_topics = 0
        confidence_counts = {
            "Not Started": 0,
            "Low": 0,
            "Medium": 0,
            "High": 0,
            "Mastered": 0,
        }

        for topic in leaf_topics:
            progress = TopicProgress.query.filter_by(
                user_id=user_id,
                topic_id=topic.id,
            ).first()

            if progress:
                if progress.completed:
                    completed_topics += 1
                confidence_counts[progress.confidence] += 1
            else:
                confidence_counts["Not Started"] += 1

        completion_percentage = (
            (completed_topics / total_topics * 100) if total_topics > 0 else 0
        )

        return {
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "completion_percentage": completion_percentage,
            "topics_by_confidence": confidence_counts,
        }

    @staticmethod
    def get_or_create_topic_progress(
        user_id: int,
        topic_id: int,
    ) -> TopicProgress:
        """Get or create a TopicProgress record for a user and topic.

        If the record doesn't exist, it's created with default values
        (Not Started, not completed, no reviews).

        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.

        Returns:
            TopicProgress: The progress record.
        """
        progress = TopicProgress.query.filter_by(
            user_id=user_id,
            topic_id=topic_id,
        ).first()

        if progress:
            return progress

        # Create new progress record
        progress = TopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            confidence="Not Started",
            completed=False,
            revision_count=0,
        )
        db.session.add(progress)
        db.session.commit()
        return progress

    @staticmethod
    def update_topic_progress(
        user_id: int,
        topic_id: int,
        completed: bool | None = None,
        confidence: str | None = None,
    ) -> TopicProgress:
        """Update a user's progress on a specific topic.

        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.
            completed: Whether the topic is now completed (optional).
            confidence: New confidence level: "Not Started", "Low", "Medium",
                       "High", or "Mastered" (optional).

        Returns:
            TopicProgress: The updated progress record.

        Raises:
            ValueError: If confidence is not a valid value.
        """
        valid_confidence = {"Not Started", "Low", "Medium", "High", "Mastered"}

        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id,
            topic_id=topic_id,
        )

        if completed is not None:
            progress.completed = completed

        if confidence is not None:
            if confidence not in valid_confidence:
                raise ValueError(
                    f"Invalid confidence: {confidence}. "
                    f"Must be one of {valid_confidence}"
                )
            progress.confidence = confidence

        progress.updated_at = db.func.now()
        db.session.commit()
        return progress

    @staticmethod
    def get_topic_tree(curriculum: Curriculum) -> dict:
        """Get a hierarchical tree structure of the curriculum.

        Uses the centralized traversal helpers so ordering stays consistent
        with :meth:`get_all_topics_ordered` / :meth:`get_ordered_topics`.

        * **V2** (sections present): ``sections → topics → learning_objectives``
        * **V1** (no sections): ``parent_topic_id`` tree under a flat ``topics`` key

        Args:
            curriculum: The curriculum object.

        Returns:
            dict: Nested structure suitable for templates or APIs.
        """
        def build_learning_objectives(topic: Topic) -> list[dict]:
            return [
                {
                    "id": lo.id,
                    "description": lo.description,
                    "order": lo.order,
                }
                for lo in CurriculumService.get_learning_objectives_for_topic(topic)
            ]

        def build_topic_node(topic: Topic, *, include_subtopics: bool) -> dict:
            node: dict[str, Any] = {
                "id": topic.id,
                "name": topic.name,
                "order": topic.order,
                "recommended_minutes": topic.recommended_minutes,
                "syllabus_weight": topic.syllabus_weight,
                "learning_objectives": build_learning_objectives(topic),
            }
            if include_subtopics:
                node["subtopics"] = [
                    build_topic_node(sub, include_subtopics=True)
                    for sub in sorted(topic.subtopics, key=lambda t: t.order)
                    if sub.active
                ]
            return node

        sections = CurriculumService.get_sections(curriculum)
        if sections:
            # V2 path — Section.display_order → Topic.order
            return {
                "curriculum_id": curriculum.id,
                "exam_name": curriculum.exam_name,
                "sections": [
                    {
                        "id": section.id,
                        "code": section.code,
                        "title": section.title,
                        "display_order": section.display_order,
                        "exam_weight": section.exam_weight,
                        "topics": [
                            build_topic_node(topic, include_subtopics=False)
                            for topic in CurriculumService.get_topics_for_section(
                                section
                            )
                        ],
                    }
                    for section in sections
                ],
            }

        # V1 path — parent_topic_id depth-first tree (unchanged shape).
        root_topics = curriculum.get_root_topics()
        return {
            "curriculum_id": curriculum.id,
            "exam_name": curriculum.exam_name,
            "topics": [
                build_topic_node(topic, include_subtopics=True)
                for topic in root_topics
            ],
        }