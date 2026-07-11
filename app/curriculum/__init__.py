"""Curriculum Intelligence Engine — v2.0.

The Curriculum Engine is the central source of truth for all educational
features in Kwalitec. It represents official examination syllabuses as
structured, versioned curriculum data.

Supports both V1 (flat) and V2 (hierarchical) formats with automatic detection.

Public API:
    CurriculumRepository  — load, cache, and query curricula (V1 and V2)
    seed_curricula        — bootstrap bundled curricula at startup

V1 Data models (dataclasses, not ORM):
    Curriculum, Topic, LearningOutcome

V2 Data models (dataclasses, not ORM):
    CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition
"""

from app.curriculum.models import (
    Curriculum,
    CurriculumDefinition,
    LearningObjectiveDefinition,
    LearningOutcome,
    SectionDefinition,
    Topic,
    TopicDefinition,
)
from app.curriculum.repository import CurriculumRepository
from app.curriculum.seed import seed_curricula

__all__ = [
    # V1 models (legacy)
    "Curriculum",
    "LearningOutcome",
    "Topic",
    # V2 models (canonical)
    "CurriculumDefinition",
    "SectionDefinition",
    "TopicDefinition",
    "LearningObjectiveDefinition",
    # Core services
    "CurriculumRepository",
    "seed_curricula",
]