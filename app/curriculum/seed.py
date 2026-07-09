"""Seed helper — loads the bundled IFoA CS1 2026 curriculum into a repository."""

from __future__ import annotations

from app.curriculum.repository import CurriculumRepository


def seed_curricula(repo: CurriculumRepository | None = None) -> CurriculumRepository:
    """Load all bundled curricula into the repository."""
    if repo is None:
        repo = CurriculumRepository()
    repo.load("ifoa", "cs1", "2026")
    return repo
