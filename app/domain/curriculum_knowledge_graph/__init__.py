"""Curriculum Knowledge Graph (EI-001) — educational structure domain.

Additive Single Source of Educational Truth for future Educational
Intelligence programmes. Models Subject → Topic → Section → Subsection →
Learning Objective plus educational objects and typed relationships.

Pure domain only: no Flask, SQLAlchemy, HTTP, extraction, or Twin logic.
ORM persistence lives in ``app.models.curriculum_knowledge_graph``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CkgEdge",
    "CkgNodeKind",
    "CkgRelationshipType",
    "CurriculumKnowledgeGraph",
    "Definition",
    "DifficultyBand",
    "EstimatedStudyTime",
    "Formula",
    "LearningObjective",
    "PracticeExercise",
    "ReadingReference",
    "Section",
    "StableCurriculumId",
    "Subject",
    "Subsection",
    "SyllabusOutcome",
    "Topic",
    "WorkedExample",
]

_EXPORT_MODULES = {
    "CkgEdge": "app.domain.curriculum_knowledge_graph.graph.edge",
    "CkgNodeKind": "app.domain.curriculum_knowledge_graph.value_objects.node_kind",
    "CkgRelationshipType": (
        "app.domain.curriculum_knowledge_graph.value_objects.relationship_type"
    ),
    "CurriculumKnowledgeGraph": (
        "app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph"
    ),
    "Definition": "app.domain.curriculum_knowledge_graph.entities.definition",
    "DifficultyBand": (
        "app.domain.curriculum_knowledge_graph.value_objects.difficulty"
    ),
    "EstimatedStudyTime": (
        "app.domain.curriculum_knowledge_graph.value_objects.estimated_study_time"
    ),
    "Formula": "app.domain.curriculum_knowledge_graph.entities.formula",
    "LearningObjective": (
        "app.domain.curriculum_knowledge_graph.entities.learning_objective"
    ),
    "PracticeExercise": (
        "app.domain.curriculum_knowledge_graph.entities.practice_exercise"
    ),
    "ReadingReference": (
        "app.domain.curriculum_knowledge_graph.entities.reading_reference"
    ),
    "Section": "app.domain.curriculum_knowledge_graph.entities.section",
    "StableCurriculumId": (
        "app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id"
    ),
    "Subject": "app.domain.curriculum_knowledge_graph.entities.subject",
    "Subsection": "app.domain.curriculum_knowledge_graph.entities.subsection",
    "SyllabusOutcome": (
        "app.domain.curriculum_knowledge_graph.entities.syllabus_outcome"
    ),
    "Topic": "app.domain.curriculum_knowledge_graph.entities.topic",
    "WorkedExample": (
        "app.domain.curriculum_knowledge_graph.entities.worked_example"
    ),
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
