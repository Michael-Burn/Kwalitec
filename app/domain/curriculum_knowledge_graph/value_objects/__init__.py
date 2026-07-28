"""Curriculum Knowledge Graph value objects."""

from __future__ import annotations

from app.domain.curriculum_knowledge_graph.value_objects.difficulty import (
    DifficultyBand,
)
from app.domain.curriculum_knowledge_graph.value_objects.estimated_study_time import (
    EstimatedStudyTime,
)
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)

__all__ = [
    "CkgNodeKind",
    "CkgRelationshipType",
    "DifficultyBand",
    "EstimatedStudyTime",
    "StableCurriculumId",
]
