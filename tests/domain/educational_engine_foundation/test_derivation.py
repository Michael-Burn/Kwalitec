from __future__ import annotations

from app.domain.educational_engine_foundation import EducationalArtefactDeriver


def _published_package() -> dict:
    return {
        "subject_code": "LAW1",
        "version_label": "2027.1",
        "structure": {
            "sections": [
                {
                    "section_id": "law1-s1",
                    "code": "1",
                    "title": "Foundations",
                    "number": "1",
                    "order_index": 1,
                },
                {
                    "section_id": "law1-s2",
                    "code": "2",
                    "title": "Remedies",
                    "number": "2",
                    "order_index": 2,
                },
            ],
            "topics": [
                {
                    "topic_id": "law1-t1",
                    "code": "1.1",
                    "title": "Offer and acceptance",
                    "section_ref": "law1-s1",
                    "number": "1.1",
                    "order_index": 1,
                    "estimated_minutes": 90,
                    "difficulty": "foundational",
                    "prerequisite_ids": [],
                },
                {
                    "topic_id": "law1-t2",
                    "code": "2.1",
                    "title": "Damages",
                    "section_ref": "law1-s2",
                    "number": "2.1",
                    "order_index": 2,
                    "estimated_minutes": 120,
                    "difficulty": "intermediate",
                    "prerequisite_ids": ["law1-t1"],
                },
            ],
            "objectives": [
                {
                    "objective_id": "law1-o1",
                    "code": "1.1.1",
                    "text": "Explain formation basics",
                    "topic_ref": "law1-t1",
                    "number": "1.1.1",
                    "order_index": 1,
                },
                {
                    "objective_id": "law1-o2",
                    "code": "2.1.1",
                    "text": "Apply damages principles",
                    "topic_ref": "law1-t2",
                    "number": "2.1.1",
                    "order_index": 1,
                },
            ],
            "prerequisite_edges": [["law1-t2", "law1-t1"]],
            "metadata": [["provider", "Founder Published"]],
        },
    }


def test_deriver_builds_all_required_artefacts():
    bundle = EducationalArtefactDeriver().derive(_published_package())

    assert bundle.curriculum_identity == "LAW1:2027.1"
    assert [section.section_id for section in bundle.sections] == ["law1-s1", "law1-s2"]
    assert [topic.topic_id for topic in bundle.topics] == ["law1-t1", "law1-t2"]
    assert [objective.objective_id for objective in bundle.objectives] == [
        "law1-o1",
        "law1-o2",
    ]

    assert bundle.graph.topic_count() == 2
    assert bundle.graph.edge_count() == 1
    assert tuple(t.value for t in bundle.graph.topological_ordering()) == (
        "law1-t1",
        "law1-t2",
    )

    assert len(bundle.study_plan_template) == 2
    assert bundle.study_plan_template[1].prerequisite_ids == ("law1-t1",)

    assert len(bundle.mission_templates) == 2
    assert bundle.mission_templates[0].topic_id == "law1-t1"
    assert bundle.mission_templates[1].objective_ids == ("law1-o2",)

    assert len(bundle.journey) == 2
    assert bundle.journey[1].topics[0].topic_id == "law1-t2"

    assert bundle.progress_model.topic_ids == ("law1-t1", "law1-t2")
    assert bundle.progress_model.objective_ids == ("law1-o1", "law1-o2")


def test_deriver_does_not_invent_objective_estimated_minutes():
    """Missing LO minutes stay unknown (0) — never a decorative default like 20."""
    bundle = EducationalArtefactDeriver().derive(_published_package())
    assert all(objective.estimated_minutes == 0 for objective in bundle.objectives)
