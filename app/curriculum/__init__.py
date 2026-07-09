"""Curriculum Intelligence Engine — v1.0.

The Curriculum Engine is the central source of truth for all educational
features in Kwalitec.  It represents official examination syllabuses as
structured, versioned curriculum data.

Public API:
    CurriculumRepository  — load, cache, and query curricula
    seed_curricula        — bootstrap bundled curricula at startup

Data models (dataclasses, not ORM):
    Curriculum, Topic, LearningOutcome
"""

from app.curriculum.models import Curriculum, LearningOutcome, Topic
from app.curriculum.repository import CurriculumRepository
from app.curriculum.seed import seed_curricula

__all__ = [
    "Curriculum",
    "CurriculumRepository",
    "LearningOutcome",
    "Topic",
    "seed_curricula",
]
