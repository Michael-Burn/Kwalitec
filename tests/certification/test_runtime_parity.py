"""Runtime parity comparison: Runtime A vs Runtime C for CS1.

This test compares the structural and behavioural outputs of both runtimes
operating on the same CS1 curriculum data to document equivalences and
intentional differences.
"""

from __future__ import annotations

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.services.curriculum_engine_service import CurriculumEngineService


def _package_from_v2(curriculum) -> dict:
    """Build a published package dict from a V2 engine curriculum."""
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
            for obj in sorted(
                topic.learning_objectives, key=lambda o: o.display_order
            ):
                objectives.append(
                    {
                        "objective_id": obj.id,
                        "code": obj.code,
                        "text": obj.description,
                        "topic_ref": topic.id,
                        "number": obj.code,
                        "order_index": obj.display_order,
                        "estimated_minutes": obj.estimated_minutes,
                        "learning_type": obj.learning_type,
                        "cognitive_level": obj.cognitive_level,
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


class TestRuntimeParity:
    """Compare Runtime A and Runtime C structural outputs for CS1."""

    def test_section_count_matches(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.sections) == len(curriculum.sections)

    def test_topic_count_matches(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.topics) == len(engine_topics)

    def test_topic_codes_match_in_order(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        runtime_a_codes = tuple(t.code for t in engine_topics)
        runtime_c_codes = tuple(t["code"] for t in snapshot.topics)
        assert runtime_c_codes == runtime_a_codes

    def test_topic_titles_match(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        runtime_a_titles = tuple(t.title for t in engine_topics)
        runtime_c_titles = tuple(t["title"] for t in snapshot.topics)
        assert runtime_c_titles == runtime_a_titles

    def test_section_codes_match_in_order(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        runtime_a_codes = tuple(
            s.code
            for s in sorted(curriculum.sections, key=lambda s: s.display_order)
        )
        runtime_c_codes = tuple(s["code"] for s in snapshot.sections)
        assert runtime_c_codes == runtime_a_codes

    def test_objective_count_matches(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        engine_obj_count = sum(
            len(t.learning_objectives) for t in engine_topics
        )
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.objectives) == engine_obj_count

    def test_study_plan_template_covers_all_topics(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.study_plan_template.topic_templates) == len(engine_topics)

    def test_mission_template_covers_all_topics(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.mission_templates) == len(engine_topics)

    def test_progress_model_covers_all_topics(self, ctx):
        curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)
        package = _package_from_v2(curriculum)
        snapshot = EducationalEngineFoundationService().derive_from_package(package)

        assert len(snapshot.progress_model.topic_ids) == len(engine_topics)
