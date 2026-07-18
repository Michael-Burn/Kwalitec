"""Curriculum domain entities."""

from __future__ import annotations

from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.entities.curriculum_version import CurriculumVersion
from app.domain.curriculum.entities.dependency import Dependency
from app.domain.curriculum.entities.learning_path import LearningPath
from app.domain.curriculum.entities.module import Module
from app.domain.curriculum.entities.prerequisite import Prerequisite
from app.domain.curriculum.entities.revision_link import RevisionLink
from app.domain.curriculum.entities.subject import Subject
from app.domain.curriculum.entities.topic import Topic

__all__ = [
    "Curriculum",
    "CurriculumVersion",
    "Dependency",
    "LearningPath",
    "Module",
    "Prerequisite",
    "RevisionLink",
    "Subject",
    "Topic",
]
