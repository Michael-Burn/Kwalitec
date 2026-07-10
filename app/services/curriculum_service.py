"""Service for managing curriculum and topic data.

This service provides both query methods for existing curriculum data and
an idempotent import method that reads official curriculum JSON from the
Curriculum Engine and persists it into the database (Curriculum, Topic,
LearningObjective records).
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import LearningObjective
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


class CurriculumService:
    """Service for curriculum operations and topic management.
    
    Provides methods for loading curricula, retrieving topics, tracking
    progress through curriculum topics, and idempotently importing
    bundled curriculum data into the database.
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

        Returns:
            The number of curricula that were newly imported (0 if all were
            already present).
        """
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        discovered = repo.list_exams()  # [(org, paper, [versions])]

        imported_count = 0

        for organisation, paper, versions in discovered:
            for version in versions:
                # ── Load from engine ─────────────────────────────────
                try:
                    engine_curriculum = repo.load(
                        organisation.lower(),
                        paper.lower(),
                        version,
                    )
                except Exception:
                    logger.exception(
                        "Failed to load curriculum %s/%s/%s — skipping.",
                        organisation, paper, version,
                    )
                    continue

                # Use the engine's canonical organisation and paper
                # (preserves casing from JSON, e.g. "IFoA" not "IFOA").
                exam_name = (
                    f"{engine_curriculum.organisation} {engine_curriculum.paper}"
                )

                # ── Idempotency check ───────────────────────────────
                existing = Curriculum.query.filter_by(
                    exam_name=exam_name,
                    version=version,
                ).first()
                if existing is not None:
                    logger.debug(
                        "Curriculum %s v%s already exists — skipping import.",
                        exam_name, version,
                    )
                    continue

                # ── Create DB Curriculum row ─────────────────────────
                db_curriculum = Curriculum(
                    exam_name=exam_name,
                    version=version,
                    active=True,
                )
                db.session.add(db_curriculum)
                db.session.flush()  # get db_curriculum.id

                # ── Create DB Topic + LearningObjective rows ─────────
                for order, engine_topic in enumerate(engine_curriculum.topics, start=1):
                    db_topic = Topic(
                        curriculum_id=db_curriculum.id,
                        name=engine_topic.title,
                        order=order,
                        recommended_minutes=int(
                            engine_topic.estimated_hours * 60
                        ),
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

                db.session.flush()
                imported_count += 1
                logger.info(
                    "Imported curriculum %s v%s (%d topics) into database.",
                    exam_name, version, len(engine_curriculum.topics),
                )

        if imported_count:
            db.session.commit()
        return imported_count

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
        
        Returns topics in depth-first hierarchical order, respecting the
        'order' field at each level.
        
        Args:
            curriculum: The curriculum object.
        
        Returns:
            list[Topic]: All active topics ordered hierarchically.
        """
        return curriculum.get_all_topics_ordered()

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
        """Get a hierarchical tree structure of topics.
        
        Returns a nested dictionary suitable for rendering topic hierarchies
        in templates or APIs.
        
        Args:
            curriculum: The curriculum object.
        
        Returns:
            dict: Nested structure with 'topics' key containing tree nodes.
        """
        def build_node(topic: Topic) -> dict:
            """Build a tree node for a topic."""
            return {
                "id": topic.id,
                "name": topic.name,
                "order": topic.order,
                "recommended_minutes": topic.recommended_minutes,
                "syllabus_weight": topic.syllabus_weight,
                "subtopics": [
                    build_node(sub)
                    for sub in sorted(topic.subtopics, key=lambda t: t.order)
                    if sub.active
                ],
            }
        
        root_topics = curriculum.get_root_topics()
        return {
            "curriculum_id": curriculum.id,
            "exam_name": curriculum.exam_name,
            "topics": [build_node(topic) for topic in root_topics],
        }
