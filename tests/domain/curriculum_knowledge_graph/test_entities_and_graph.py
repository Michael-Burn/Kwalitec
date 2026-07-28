"""Entity invariant and graph behaviour tests for CKG."""

from __future__ import annotations

import pytest

from app.domain.curriculum_knowledge_graph.entities.definition import Definition
from app.domain.curriculum_knowledge_graph.entities.learning_objective import (
    LearningObjective,
)
from app.domain.curriculum_knowledge_graph.entities.section import Section
from app.domain.curriculum_knowledge_graph.entities.subject import Subject
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)


def _build_mini_graph() -> tuple[
    CurriculumKnowledgeGraph,
    LearningObjective,
    LearningObjective,
    Definition,
]:
    subject = Subject.create("CS1", "Actuarial Statistics", edition_label="2026")
    topic = Topic.create("CS1.T04", "CS1", "Conditional probability", display_order=4)
    section = Section.create(
        "CS1.T04.S04.02", "CS1.T04", "Bayes theorem", display_order=2
    )
    subsection = Subsection.create(
        "CS1.T04.S04.02.SS01",
        "CS1.T04.S04.02",
        "Statement of Bayes",
        display_order=1,
    )
    lo1 = LearningObjective.create(
        "CS1.T04.S04.02.SS01.LO01",
        "CS1.T04.S04.02.SS01",
        "State Bayes theorem",
        display_order=1,
    )
    lo3 = LearningObjective.create(
        "CS1.T04.S04.02.SS01.LO03",
        "CS1.T04.S04.02.SS01",
        "Apply Bayes theorem",
        display_order=3,
        estimated_study_minutes=45,
    )
    definition = Definition.create(
        StableCurriculumId.educational_object(
            "CS1.T04.S04.02.SS01", "definition", 1
        ),
        "CS1.T04.S04.02.SS01",
        "Prior probability",
        body="Operational definition label",
    )

    graph = CurriculumKnowledgeGraph(subject=subject)
    for node in (topic, section, subsection, lo1, lo3, definition):
        graph.add_node(node)

    graph.connect("CS1", "CS1.T04", CkgRelationshipType.CONTAINS)
    graph.connect("CS1.T04", "CS1.T04.S04.02", CkgRelationshipType.CONTAINS)
    graph.connect(
        "CS1.T04.S04.02", "CS1.T04.S04.02.SS01", CkgRelationshipType.CONTAINS
    )
    graph.connect(
        "CS1.T04.S04.02.SS01",
        "CS1.T04.S04.02.SS01.LO01",
        CkgRelationshipType.CONTAINS,
    )
    graph.connect(
        "CS1.T04.S04.02.SS01",
        "CS1.T04.S04.02.SS01.LO03",
        CkgRelationshipType.CONTAINS,
    )
    graph.connect(
        "CS1.T04.S04.02.SS01",
        definition.stable_id.value,
        CkgRelationshipType.CONTAINS,
    )
    graph.connect(
        lo3.stable_id.value,
        definition.stable_id.value,
        CkgRelationshipType.REFERENCES,
    )
    graph.connect(
        lo3.stable_id.value,
        lo1.stable_id.value,
        CkgRelationshipType.REQUIRES,
    )
    return graph, lo1, lo3, definition


def test_entity_ownership_mismatch_rejected() -> None:
    with pytest.raises(ValueError, match="child of subject_id"):
        Topic.create("CS1.T04", "CM1", "Wrong subject")


def test_containment_traversal_order() -> None:
    graph, _, _, definition = _build_mini_graph()
    order = graph.traverse_containment()
    assert order[0] == "CS1"
    assert "CS1.T04" in order
    assert "CS1.T04.S04.02.SS01.LO03" in order
    assert definition.stable_id.value in order


def test_requires_acyclicity() -> None:
    graph, lo1, lo3, _ = _build_mini_graph()
    with pytest.raises(ValueError, match="cycle"):
        graph.connect(
            lo1.stable_id.value,
            lo3.stable_id.value,
            CkgRelationshipType.REQUIRES,
        )


def test_topological_learning_objectives() -> None:
    graph, lo1, lo3, _ = _build_mini_graph()
    ordered = graph.topological_learning_objectives()
    assert ordered.index(lo1.stable_id.value) < ordered.index(lo3.stable_id.value)


def test_duplicate_node_rejected() -> None:
    graph, _, _, _ = _build_mini_graph()
    with pytest.raises(ValueError, match="duplicate"):
        graph.add_node(
            Topic.create("CS1.T04", "CS1", "Duplicate")
        )
