"""Curriculum Repository — single entry point for curriculum access.

Caches loaded curricula in memory. All other modules talk to the repository
rather than touching the loader or file system directly.
"""

from __future__ import annotations

from app.curriculum.exceptions import CurriculumNotFoundError
from app.curriculum.loader import discover_curricula, load_curriculum
from app.curriculum.models import Curriculum, LearningOutcome, Topic
from app.curriculum.validator import validate_curriculum


class CurriculumRepository:
    """In-memory repository for versioned curricula.

    Curricula are lazy-loaded on first access and cached for the lifetime of
    the process.
    """

    def __init__(self) -> None:
        self._cache: dict[str, Curriculum] = {}

    @staticmethod
    def _cache_key(organisation: str, paper: str, version: str) -> str:
        return f"{organisation.lower()}/{paper.lower()}/{version}"

    def load(self, organisation: str, paper: str, version: str) -> Curriculum:
        """Load a curriculum, validate it, and cache it."""
        key = self._cache_key(organisation, paper, version)
        if key in self._cache:
            return self._cache[key]
        curriculum = load_curriculum(organisation, paper, version)
        validate_curriculum(curriculum)
        self._cache[key] = curriculum
        return curriculum

    def exists(self, organisation: str, paper: str, version: str) -> bool:
        """Check whether a curriculum file exists on disk."""
        for org, pap, versions in self.list_exams():
            if org.lower() == organisation.lower() and pap.lower() == paper.lower():
                return version in versions
        return False

    def get_curriculum(self, organisation: str, paper: str, version: str) -> Curriculum:
        """Return a cached curriculum. Raises CurriculumNotFoundError if not loaded."""
        key = self._cache_key(organisation, paper, version)
        if key not in self._cache:
            raise CurriculumNotFoundError(f"{organisation}/{paper}", version)
        return self._cache[key]

    def get_topics(self, organisation: str, paper: str, version: str) -> list[Topic]:
        """Return all topics for a curriculum."""
        return self.get_curriculum(organisation, paper, version).topics

    def get_topic(self, organisation: str, paper: str, version: str, topic_id: str) -> Topic:
        """Return a single topic by ID."""
        for t in self.get_topics(organisation, paper, version):
            if t.id == topic_id:
                return t
        raise CurriculumNotFoundError(f"{organisation}/{paper}/{version}/topic/{topic_id}")

    def get_learning_outcome(self, organisation: str, paper: str, version: str, lo_id: str) -> LearningOutcome:
        """Return a single learning outcome by ID."""
        for t in self.get_topics(organisation, paper, version):
            for lo in t.learning_outcomes:
                if lo.id == lo_id:
                    return lo
        raise CurriculumNotFoundError(f"{organisation}/{paper}/{version}/lo/{lo_id}")

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
