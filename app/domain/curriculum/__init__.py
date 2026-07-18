"""Version 2 Curriculum Graph domain package.

Pure educational knowledge model for curriculum structure, topic
relationships, prerequisites, revision links, and pathways.

Does **not** store copyrighted educational material. No Flask, SQLAlchemy,
routes, or persistence implementations.

Domain structure::

    curriculum/
        entities/          Curriculum, Subject, Module, Topic, …
        value_objects/     TopicId, DependencyType, TopicDifficulty, …
        graph/             CurriculumGraph, builder, validator, algorithms
        services/          Navigation, prerequisites, revision paths
        interfaces/        CurriculumRepository contract only

Prefer explicit imports such as
``app.domain.curriculum.graph.curriculum_graph``.

Future Learning Journey Engine integration (not wired in this milestone)::

    Learning Journey Engine
            ↓
    Curriculum Navigation
            ↓
    Curriculum Graph
            ↓
    Topic
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "Curriculum",
    "CurriculumGraph",
    "CurriculumId",
    "CurriculumNavigationService",
    "CurriculumRepository",
    "CurriculumVersion",
    "Dependency",
    "DependencyType",
    "GraphBuilder",
    "GraphEdge",
    "GraphNode",
    "GraphValidationResult",
    "GraphValidator",
    "LearningPath",
    "Module",
    "Prerequisite",
    "PrerequisiteEvaluation",
    "PrerequisiteService",
    "RevisionLink",
    "RevisionPathService",
    "Subject",
    "Topic",
    "TopicDifficulty",
    "TopicId",
    "TopicStatus",
]

_EXPORT_MODULES = {
    "Curriculum": "app.domain.curriculum.entities.curriculum",
    "CurriculumGraph": "app.domain.curriculum.graph.curriculum_graph",
    "CurriculumId": "app.domain.curriculum.value_objects.curriculum_id",
    "CurriculumNavigationService": (
        "app.domain.curriculum.services.curriculum_navigation_service"
    ),
    "CurriculumRepository": (
        "app.domain.curriculum.interfaces.curriculum_repository"
    ),
    "CurriculumVersion": "app.domain.curriculum.entities.curriculum_version",
    "Dependency": "app.domain.curriculum.entities.dependency",
    "DependencyType": "app.domain.curriculum.value_objects.dependency_type",
    "GraphBuilder": "app.domain.curriculum.graph.graph_builder",
    "GraphEdge": "app.domain.curriculum.graph.graph_edge",
    "GraphNode": "app.domain.curriculum.graph.graph_node",
    "GraphValidationResult": "app.domain.curriculum.graph.graph_validator",
    "GraphValidator": "app.domain.curriculum.graph.graph_validator",
    "LearningPath": "app.domain.curriculum.entities.learning_path",
    "Module": "app.domain.curriculum.entities.module",
    "Prerequisite": "app.domain.curriculum.entities.prerequisite",
    "PrerequisiteEvaluation": (
        "app.domain.curriculum.services.prerequisite_service"
    ),
    "PrerequisiteService": (
        "app.domain.curriculum.services.prerequisite_service"
    ),
    "RevisionLink": "app.domain.curriculum.entities.revision_link",
    "RevisionPathService": (
        "app.domain.curriculum.services.revision_path_service"
    ),
    "Subject": "app.domain.curriculum.entities.subject",
    "Topic": "app.domain.curriculum.entities.topic",
    "TopicDifficulty": "app.domain.curriculum.value_objects.topic_difficulty",
    "TopicId": "app.domain.curriculum.value_objects.topic_id",
    "TopicStatus": "app.domain.curriculum.value_objects.topic_status",
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
