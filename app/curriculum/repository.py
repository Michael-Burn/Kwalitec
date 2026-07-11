"""Curriculum Repository — single entry point for curriculum access.

Caches loaded curricula in memory. All other modules talk to the repository
rather than touching the loader or file system directly.

Supports both V1 (flat) and V2 (hierarchical) formats.
"""

from __future__ import annotations

from app.curriculum.exceptions import CurriculumNotFoundError
from app.curriculum.loader import discover_curricula, load_curriculum, load_curriculum_v2
from app.curriculum.models import (
    Curriculum,
    CurriculumDefinition,
    LearningObjectiveDefinition,
    LearningOutcome,
    SectionDefinition,
    Topic,
    TopicDefinition,
)
from app.curriculum.validator import validate_curriculum, validate_curriculum_v2


class CurriculumRepository:
    """In-memory repository for versioned curricula.

    Curricula are lazy-loaded on first access and cached for the lifetime of
    the process. Supports both V1 and V2 curriculum formats.
    """

    def __init__(self) -> None:
        self._cache: dict[str, Curriculum | CurriculumDefinition] = {}

    @staticmethod
    def _cache_key(organisation: str, paper: str, version: str) -> str:
        return f"{organisation.lower()}/{paper.lower()}/{version}"

    def load(self, organisation: str, paper: str, version: str) -> Curriculum:
        """Load a V1 curriculum, validate it, and cache it.
        
        Maintains backwards compatibility with existing V1 code.
        For V2 curricula, use load_v2() instead.
        """
        key = self._cache_key(organisation, paper, version)
        if key in self._cache:
            # Type narrowing: V1 cache entries are Curriculum instances
            cached = self._cache[key]
            if not isinstance(cached, Curriculum):
                raise CurriculumNotFoundError(f"{organisation}/{paper}", version)
            return cached
        
        curriculum = load_curriculum(organisation, paper, version)
        validate_curriculum(curriculum)
        self._cache[key] = curriculum
        return curriculum

    def load_v2(self, provider: str, exam_code: str, version: str) -> CurriculumDefinition:
        """Load a V2 curriculum, validate it, and cache it.
        
        Args:
            provider: Examining body (e.g., 'ifoa').
            exam_code: Exam code (e.g., 'cs1').
            version: Syllabus version year (e.g., '2026').
            
        Returns:
            A CurriculumDefinition instance (V2 format).
        """
        key = self._cache_key(provider, exam_code, version)
        if key in self._cache:
            # Type narrowing: V2 cache entries are CurriculumDefinition instances
            cached = self._cache[key]
            if not isinstance(cached, CurriculumDefinition):
                raise CurriculumNotFoundError(f"{provider}/{exam_code}", version)
            return cached
        
        curriculum = load_curriculum_v2(provider, exam_code, version)
        validate_curriculum_v2(curriculum)
        self._cache[key] = curriculum
        return curriculum

    def exists(self, organisation: str, paper: str, version: str) -> bool:
        """Check whether a curriculum file exists on disk."""
        for org, pap, versions in self.list_exams():
            if org.lower() == organisation.lower() and pap.lower() == paper.lower():
                return version in versions
        return False

    def get_curriculum(self, organisation: str, paper: str, version: str) -> Curriculum:
        """Return a cached V1 curriculum. Raises CurriculumNotFoundError if not loaded."""
        key = self._cache_key(organisation, paper, version)
        if key not in self._cache:
            raise CurriculumNotFoundError(f"{organisation}/{paper}", version)
        cached = self._cache[key]
        if not isinstance(cached, Curriculum):
            raise CurriculumNotFoundError(f"{organisation}/{paper}", version)
        return cached

    def get_curriculum_v2(self, provider: str, exam_code: str, version: str) -> CurriculumDefinition:
        """Return a cached V2 curriculum. Raises CurriculumNotFoundError if not loaded."""
        key = self._cache_key(provider, exam_code, version)
        if key not in self._cache:
            raise CurriculumNotFoundError(f"{provider}/{exam_code}", version)
        cached = self._cache[key]
        if not isinstance(cached, CurriculumDefinition):
            raise CurriculumNotFoundError(f"{provider}/{exam_code}", version)
        return cached

    # ═══════════════════════════════════════════════════════════════════════════
    # V1 Lookup Methods (Legacy)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_topics(self, organisation: str, paper: str, version: str) -> list[Topic]:
        """Return all topics for a V1 curriculum."""
        return self.get_curriculum(organisation, paper, version).topics

    def get_topic(self, organisation: str, paper: str, version: str, topic_id: str) -> Topic:
        """Return a single V1 topic by ID."""
        for t in self.get_topics(organisation, paper, version):
            if t.id == topic_id:
                return t
        raise CurriculumNotFoundError(f"{organisation}/{paper}/{version}/topic/{topic_id}")

    def get_learning_outcome(self, organisation: str, paper: str, version: str, lo_id: str) -> LearningOutcome:
        """Return a single V1 learning outcome by ID."""
        for t in self.get_topics(organisation, paper, version):
            for lo in t.learning_outcomes:
                if lo.id == lo_id:
                    return lo
        raise CurriculumNotFoundError(f"{organisation}/{paper}/{version}/lo/{lo_id}")

    # ═══════════════════════════════════════════════════════════════════════════
    # V2 Lookup Methods (Canonical Format)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_sections(self, provider: str, exam_code: str, version: str) -> list[SectionDefinition]:
        """Return all sections for a V2 curriculum."""
        return self.get_curriculum_v2(provider, exam_code, version).sections

    def get_section(self, provider: str, exam_code: str, version: str, section_id: str) -> SectionDefinition:
        """Return a single V2 section by ID."""
        for s in self.get_sections(provider, exam_code, version):
            if s.id == section_id:
                return s
        raise CurriculumNotFoundError(f"{provider}/{exam_code}/{version}/section/{section_id}")

    def get_topics_v2(self, provider: str, exam_code: str, version: str, section_id: str) -> list[TopicDefinition]:
        """Return all topics for a V2 section."""
        return self.get_section(provider, exam_code, version, section_id).topics

    def get_topic_v2(self, provider: str, exam_code: str, version: str, topic_id: str) -> TopicDefinition:
        """Return a single V2 topic by ID."""
        for s in self.get_sections(provider, exam_code, version):
            for t in s.topics:
                if t.id == topic_id:
                    return t
        raise CurriculumNotFoundError(f"{provider}/{exam_code}/{version}/topic/{topic_id}")

    def get_learning_objectives(self, provider: str, exam_code: str, version: str, topic_id: str) -> list[LearningObjectiveDefinition]:
        """Return all learning objectives for a V2 topic."""
        return self.get_topic_v2(provider, exam_code, version, topic_id).learning_objectives

    def get_learning_objective(self, provider: str, exam_code: str, version: str, lo_id: str) -> LearningObjectiveDefinition:
        """Return a single V2 learning objective by ID."""
        for s in self.get_sections(provider, exam_code, version):
            for t in s.topics:
                for lo in t.learning_objectives:
                    if lo.id == lo_id:
                        return lo
        raise CurriculumNotFoundError(f"{provider}/{exam_code}/{version}/lo/{lo_id}")

    def find_learning_objective(self, lo_id: str) -> tuple[CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition]:
        """Find a learning objective by ID across all loaded V2 curricula.
        
        Searches through all cached V2 curricula to find the learning objective.
        
        Args:
            lo_id: The learning objective ID to find.
            
        Returns:
            A tuple of (curriculum, section, topic, learning_objective).
            
        Raises:
            CurriculumNotFoundError: If the learning objective is not found.
        """
        for cached in self._cache.values():
            if not isinstance(cached, CurriculumDefinition):
                continue
            
            for section in cached.sections:
                for topic in section.topics:
                    for lo in topic.learning_objectives:
                        if lo.id == lo_id:
                            return (cached, section, topic, lo)
        
        raise CurriculumNotFoundError(f"global/lo/{lo_id}")

    # ═══════════════════════════════════════════════════════════════════════════
    # Discovery and Cache Management
    # ═══════════════════════════════════════════════════════════════════════════

    def list_exams(self) -> list[tuple[str, str, list[str]]]:
        """Return (organisation, paper, [version, ...]) for all on-disk curricula."""
        return discover_curricula()

    def list_versions(self, organisation: str, paper: str) -> list[str]:
        """Return all available versions for a given exam."""
        for org, pap, versions in self.list_exams():
            if org.lower() == organisation.lower() and pap.lower() == paper.lower():
                return versions
        return []

    def clear(self) -> None:
        """Clear the in-memory cache."""
        self._cache.clear()

    def is_loaded(self, organisation: str, paper: str, version: str) -> bool:
        """Check whether a curriculum is currently cached."""
        return self._cache_key(organisation, paper, version) in self._cache

    def is_loaded_v2(self, provider: str, exam_code: str, version: str) -> bool:
        """Check whether a V2 curriculum is currently cached."""
        return self._cache_key(provider, exam_code, version) in self._cache

    # ═══════════════════════════════════════════════════════════════════════════
    # Auto-detect (canonical entry point)
    # ═══════════════════════════════════════════════════════════════════════════

    def load_auto(
        self, organisation: str, paper: str, version: str
    ) -> Curriculum | CurriculumDefinition:
        """Load a curriculum with automatic V1/V2 format detection.

        This is the **canonical loader entry point** for all application code.
        Tries V1 first (backwards compatibility), then falls back to V2.
        Caches the result so subsequent calls are free.

        Args:
            organisation: Examining body (e.g. ``"ifoa"``).
            paper: Paper code (e.g. ``"cs1"``).
            version: Syllabus version year (e.g. ``"2026"``).

        Returns:
            A :class:`Curriculum` (V1) or :class:`CurriculumDefinition` (V2).

        Raises:
            CurriculumLoadError: If the file cannot be loaded in either format.
        """
        from app.curriculum.exceptions import CurriculumError

        try:
            return self.load(organisation, paper, version)
        except CurriculumError:
            pass  # V2-only file — fall through.

        return self.load_v2(organisation, paper, version)
