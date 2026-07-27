from __future__ import annotations

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.services.curriculum_engine_service import CurriculumEngineService


def _package_from_v2(curriculum) -> dict:
    sections = []
    topics = []
    objectives = []
    for section in sorted(curriculum.sections, key=lambda s: s.display_order):
        sections.append(
            {
                "section_id": section.id,
                "code": section.code,
                "title": section.title,
                "number": section.code,
                "order_index": section.display_order,
            }
        )
        for topic in sorted(section.topics, key=lambda t: t.display_order):
            topics.append(
                {
                    "topic_id": topic.id,
                    "code": topic.code,
                    "title": topic.title,
                    "section_ref": section.id,
                    "number": topic.code,
                    "order_index": topic.display_order,
                    "estimated_minutes": topic.estimated_minutes,
                    "difficulty": topic.difficulty,
                    "prerequisite_ids": [],
                }
            )
            for objective in sorted(
                topic.learning_objectives, key=lambda item: item.display_order
            ):
                objectives.append(
                    {
                        "objective_id": objective.id,
                        "code": objective.code,
                        "text": objective.description,
                        "topic_ref": topic.id,
                        "number": objective.code,
                        "order_index": objective.display_order,
                        "estimated_minutes": objective.estimated_minutes,
                        "learning_type": objective.learning_type,
                        "cognitive_level": objective.cognitive_level,
                    }
                )
    return {
        "subject_code": curriculum.exam_code,
        "version_label": curriculum.version,
        "structure": {
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": [],
            "metadata": tuple(curriculum.metadata.items()),
        },
    }


def test_cs1_equivalence_against_existing_json_behaviour(ctx):
    curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
    package = _package_from_v2(curriculum)

    snapshot = EducationalEngineFoundationService().derive_from_package(package)
    engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
    engine_objectives = [
        objective
        for topic in engine_topics
        for objective in topic.learning_objectives
    ]

    assert len(snapshot.sections) == len(curriculum.sections)
    assert len(snapshot.topics) == len(engine_topics)
    assert len(snapshot.objectives) == len(engine_objectives)
    assert tuple(topic["code"] for topic in snapshot.topics) == tuple(
        topic.code for topic in engine_topics
    )
    assert tuple(topic["title"] for topic in snapshot.topics) == tuple(
        topic.title for topic in engine_topics
    )
    assert tuple(section["code"] for section in snapshot.sections) == tuple(
        section.code
        for section in sorted(
            curriculum.sections,
            key=lambda s: s.display_order,
        )
    )
    assert len(snapshot.study_plan_template.topic_templates) == len(engine_topics)
    assert len(snapshot.mission_templates) == len(engine_topics)
    assert len(snapshot.progress_model.topic_ids) == len(engine_topics)
    assert len(snapshot.progress_model.objective_ids) == len(engine_objectives)
