"""Shared helpers for Student Experience production adapter tests."""

from __future__ import annotations

from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)

LEARNERS = tuple(f"exp-L{i}" for i in range(10))
SURFACES = ("home", "journey", "revision", "history", "profile")
OPS = ("seed", "read", "session", "recalc")


def make_composition(**kwargs) -> StudentExperienceComposition:
    """Build a composition with learning loop enabled by default."""
    return StudentExperienceComposition(**kwargs)


def make_seeded_service(student_id: str = "stu-1"):
    """Build production service with a seeded learner."""
    composition, service = build_production_experience(seed_demo_learners=False)
    composition.seed_learner(student_id, demo=True)
    return composition, service
