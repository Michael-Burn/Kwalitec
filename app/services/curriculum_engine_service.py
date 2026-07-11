"""Curriculum Engine Service — bridge between the Curriculum Engine and the rest
of the application.

This service is a thin wrapper around CurriculumRepository. It contains no
business logic and simply delegates all calls to the repository.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.curriculum.models import (
    Curriculum,
    CurriculumDefinition,
    LearningOutcome,
    Topic,
)
from app.curriculum.repository import CurriculumRepository


@dataclass(frozen=True)
class StudentCurriculumSummary:
    """Read-only summary of a student's progress through a curriculum.

    Attributes:
        total_topics: Total number of topics in the curriculum.
        completed_topics: Number of topics marked as completed.
        remaining_topics: Number of topics not yet completed.
        current_topic_code: The topic code the student is currently studying.
        next_topic_code: The code of the next non-completed topic after current.
        next_topic_title: The title of the next non-completed topic.
        curriculum_coverage_percentage: completed_topics / total_topics.
        weighted_completed_percentage: Sum of syllabus weightings for completed
            topics divided by total syllabus weight.
        weighted_remaining_percentage: 1 - weighted_completed_percentage.
        completed_topic_codes: Codes of all completed topics.
        remaining_topic_codes: Codes of all remaining topics.
    """

    total_topics: int
    completed_topics: int
    remaining_topics: int
    current_topic_code: str | None
    next_topic_code: str | None
    next_topic_title: str | None
    curriculum_coverage_percentage: float
    weighted_completed_percentage: float
    weighted_remaining_percentage: float
    completed_topic_codes: tuple[str, ...]
    remaining_topic_codes: tuple[str, ...]


class CurriculumEngineService:
    """Thin delegation layer over CurriculumRepository.

    Every public method maps directly to a corresponding repository method
    with no additional logic, transformation, or side-effects.
    """

    def __init__(self, repository: CurriculumRepository | None = None) -> None:
        self._repo = repository or CurriculumRepository()

    # ------------------------------------------------------------------
    # Delegates
    # ------------------------------------------------------------------

    def curriculum_exists(self, exam: str, paper: str, version: str) -> bool:
        """Check whether a curriculum file exists on disk.

        Args:
            exam: Organisation name (e.g. "ifoa").
            paper: Exam paper code (e.g. "cs1").
            version: Syllabus version string (e.g. "2026").

        Returns:
            True if the curriculum JSON file exists on disk.
        """
        return self._repo.exists(exam, paper, version)

    def load_curriculum(self, exam: str, paper: str, version: str) -> Curriculum:
        """Load a curriculum from disk, validate, cache, and return it.

        Args:
            exam: Organisation name.
            paper: Exam paper code.
            version: Syllabus version string.

        Returns:
            The loaded and validated Curriculum object.
        """
        return self._repo.load(exam, paper, version)

    def get_curriculum(self, exam: str, paper: str, version: str) -> Curriculum:
        """Return a previously loaded (cached) curriculum.

        Args:
            exam: Organisation name.
            paper: Exam paper code.
            version: Syllabus version string.

        Returns:
            The cached Curriculum object.

        Raises:
            CurriculumNotFoundError: If the curriculum has not been loaded.
        """
        return self._repo.get_curriculum(exam, paper, version)

    def get_topics(self, exam: str, paper: str, version: str) -> list[Topic]:
        """Return all topics for a curriculum.

        Args:
            exam: Organisation name.
            paper: Exam paper code.
            version: Syllabus version string.

        Returns:
            A list of Topic objects belonging to the curriculum.
        """
        return self._repo.get_topics(exam, paper, version)

    def get_topic(
        self, exam: str, paper: str, version: str, topic_code: str
    ) -> Topic:
        """Return a single topic by its code (ID).

        Args:
            exam: Organisation name.
            paper: Exam paper code.
            version: Syllabus version string.
            topic_code: The topic identifier (e.g. "cs1-2026-1").

        Returns:
            The matching Topic object.

        Raises:
            CurriculumNotFoundError: If the topic cannot be found.
        """
        return self._repo.get_topic(exam, paper, version, topic_code)

    def get_learning_outcome(
        self, exam: str, paper: str, version: str, outcome_code: str
    ) -> LearningOutcome:
        """Return a single learning outcome by its code (ID).

        Args:
            exam: Organisation name.
            paper: Exam paper code.
            version: Syllabus version string.
            outcome_code: The learning outcome identifier (e.g. "cs1-2026-1-1").

        Returns:
            The matching LearningOutcome object.

        Raises:
            CurriculumNotFoundError: If the learning outcome cannot be found.
        """
        return self._repo.get_learning_outcome(exam, paper, version, outcome_code)

    def list_supported_exams(self) -> list[tuple[str, str, list[str]]]:
        """Return all on-disk curricula as (organisation, paper, [versions]).

        Returns:
            A list of tuples, each containing (org, paper, [version, ...]).
        """
        return self._repo.list_exams()

    def list_supported_versions(self, exam: str, paper: str) -> list[str]:
        """Return all available syllabus versions for a given exam.

        Args:
            exam: Organisation name.
            paper: Exam paper code.

        Returns:
            A list of version strings (e.g. ["2026"]).
        """
        return self._repo.list_versions(exam, paper)

    def load_auto(
        self, exam: str, paper: str, version: str
    ) -> Curriculum | CurriculumDefinition:
        """Load a curriculum with automatic V1/V2 format detection.

        This is the **canonical public loader** for all callers that need to
        handle both V1 and V2 curricula without knowing in advance which format
        is on disk.  Tries V1 first, then falls back to V2.

        Args:
            exam: Organisation name (e.g. ``"IFoA"`` or ``"ifoa"``).
            paper: Exam paper code (e.g. ``"CS1"`` or ``"cs1"``).
            version: Syllabus version string (e.g. ``"2026"``).

        Returns:
            A :class:`~app.curriculum.models.Curriculum` (V1) or
            :class:`~app.curriculum.models.CurriculumDefinition` (V2).

        Raises:
            CurriculumLoadError: If the file cannot be loaded in either format.
        """
        return self._repo.load_auto(exam, paper, version)

    @staticmethod
    def get_topics_flat(
        curriculum: Curriculum | CurriculumDefinition,
    ) -> list:
        """Return engine topics as a flat, canonically ordered list.

        This is the **single engine-level flattening helper** used throughout
        the application.  All callers that previously duplicated the
        ``Section (display_order) → Topic (display_order)`` traversal should
        delegate here.

        * **V2** (:class:`CurriculumDefinition`): sections sorted by
          ``display_order``, then topics within each section sorted by
          ``display_order``.
        * **V1** (:class:`Curriculum`): original flat ``topics`` list,
          unchanged (prerequisite-based order is handled downstream by
          ``PlanningService``).

        Args:
            curriculum: A V1 :class:`Curriculum` or V2
                :class:`CurriculumDefinition` from the engine layer.

        Returns:
            Flat list of engine topic objects in canonical curriculum order.
        """
        if isinstance(curriculum, CurriculumDefinition):
            return [
                topic
                for section in sorted(
                    curriculum.sections, key=lambda s: s.display_order
                )
                for topic in sorted(
                    section.topics, key=lambda t: t.display_order
                )
            ]
        return list(curriculum.topics)

    # ------------------------------------------------------------------
    # Student Curriculum Summary
    # ------------------------------------------------------------------

    def build_student_curriculum(
        self, study_plan: object
    ) -> StudentCurriculumSummary | None:
        """Build a read-only curriculum summary from a study plan's TopicProgress data.

        Calculates which topics have been completed based solely on
        ``TopicProgress.completed`` flags.  No mastery, weighting, or
        readiness calculations are performed.

        Supports both V1 (flat topic list) and V2 (section-hierarchical) engine
        curricula.  For V2 curricula topics are flattened in canonical order
        (``Section.display_order`` → ``TopicDefinition.display_order``) before
        comparison.  V1 weighted coverage uses official syllabus topic
        weightings; V2 uses equal weighting (no per-topic weights exist in the
        V2 format).

        Args:
            study_plan: A ``StudyPlan`` ORM instance.

        Returns:
            A frozen ``StudentCurriculumSummary`` if a curriculum is attached,
            or ``None`` if the study plan has no curriculum version or the
            curriculum cannot be loaded.
        """
        # No curriculum attached → nothing to summarise
        if not study_plan.curriculum_id or not study_plan.curriculum_version:
            return None

        # Parse the exam name to extract organisation and paper code
        from app.services.examination_catalogue import parse_exam_name

        org, paper = parse_exam_name(study_plan.exam_name)
        if not org or not paper:
            return None

        version: str = study_plan.curriculum_version
        org_lower = org.lower()
        paper_lower = paper.lower()

        # Load the engine curriculum using the canonical auto-detect loader.
        try:
            engine_curriculum = self.load_auto(org_lower, paper_lower, version)
        except Exception:
            return None

        is_v2_engine = isinstance(engine_curriculum, CurriculumDefinition)

        # Flatten topics in canonical order via the shared helper.
        engine_topics = self.get_topics_flat(engine_curriculum)

        # Retrieve the DB-side curriculum topics
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        db_topics = DBTopic.query.filter_by(
            curriculum_id=study_plan.curriculum_id
        ).all()

        # Build mapping: engine topic code → DB Topic (matched by title/name)
        code_to_db_topic: dict[str, object] = {}
        for engine_topic in engine_topics:
            for db_topic in db_topics:
                if db_topic.name == engine_topic.title:
                    code_to_db_topic[engine_topic.code] = db_topic
                    break

        if not code_to_db_topic:
            return None

        # Look up TopicProgress for every mapped DB topic
        db_topic_ids = [t.id for t in code_to_db_topic.values()]
        progress_rows = TopicProgress.query.filter(
            TopicProgress.user_id == study_plan.user_id,
            TopicProgress.topic_id.in_(db_topic_ids),
        ).all()

        topic_id_to_completed: dict[int, bool] = {
            tp.topic_id: tp.completed for tp in progress_rows
        }

        # Walk the engine topics in order and classify each
        completed_codes: list[str] = []
        remaining_codes: list[str] = []

        for engine_topic in engine_topics:
            db_topic = code_to_db_topic.get(engine_topic.code)
            if db_topic is None:
                remaining_codes.append(engine_topic.code)
                continue
            if topic_id_to_completed.get(db_topic.id, False):
                completed_codes.append(engine_topic.code)
            else:
                remaining_codes.append(engine_topic.code)

        total_topics = len(engine_topics)
        completed_count = len(completed_codes)
        remaining_count = len(remaining_codes)
        coverage = completed_count / total_topics if total_topics > 0 else 0.0

        # Weighted coverage.
        # V1: use official per-topic syllabus weightings.
        # V2: no per-topic weights exist; fall back to equal weighting so that
        #     weighted_completed_percentage == curriculum_coverage_percentage.
        if is_v2_engine:
            code_to_weighting: dict[str, float] = {
                t.code: 1.0 for t in engine_topics
            }
            total_weight = float(total_topics)
        else:
            code_to_weighting = {t.code: t.weighting for t in engine_topics}
            total_weight = engine_curriculum.total_weight

        completed_weight = sum(
            code_to_weighting.get(code, 0.0) for code in completed_codes
        )
        weighted_coverage = (
            completed_weight / total_weight if total_weight > 0 else 0.0
        )
        weighted_remaining = 1.0 - weighted_coverage

        # Determine the next recommended topic
        # Walk topics in curriculum order; look *past* the current topic
        # for the first non-completed topic. Skip completed and current.
        completed_set = frozenset(completed_codes)
        current_code = study_plan.curriculum_topic_code
        next_topic_code: str | None = None
        next_topic_title: str | None = None

        # Find the index of the current topic so we only look ahead
        current_index: int | None = None
        for i, engine_topic in enumerate(engine_topics):
            if engine_topic.code == current_code:
                current_index = i
                break

        if current_index is not None:
            for engine_topic in engine_topics[current_index + 1:]:
                if engine_topic.code in completed_set:
                    continue
                # Found the first non-completed topic after current
                next_topic_code = engine_topic.code
                next_topic_title = engine_topic.title
                break

        return StudentCurriculumSummary(
            total_topics=total_topics,
            completed_topics=completed_count,
            remaining_topics=remaining_count,
            current_topic_code=study_plan.curriculum_topic_code,
            next_topic_code=next_topic_code,
            next_topic_title=next_topic_title,
            curriculum_coverage_percentage=coverage,
            weighted_completed_percentage=weighted_coverage,
            weighted_remaining_percentage=weighted_remaining,
            completed_topic_codes=tuple(completed_codes),
            remaining_topic_codes=tuple(remaining_codes),
        )
