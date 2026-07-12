"""Seed helper — loads the bundled IFoA CS1 2026 curriculum into a repository."""

from __future__ import annotations

from app.curriculum.repository import CurriculumRepository


def seed_curricula(repo: CurriculumRepository | None = None) -> CurriculumRepository:
    """Load all bundled curricula into the repository.

    Uses :meth:`CurriculumRepository.load_auto` so both V1 and V2 syllabus
    files are accepted without callers needing to know the format.
    """
    if repo is None:
        repo = CurriculumRepository()
    repo.load_auto("ifoa", "cs1", "2026")
    return repo
