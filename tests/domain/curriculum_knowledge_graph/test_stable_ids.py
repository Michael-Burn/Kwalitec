"""StableCurriculumId parse / build / reject cases."""

from __future__ import annotations

import pytest

from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


def test_example_lo_id_from_brief() -> None:
    sid = StableCurriculumId.of("CS1.T04.S04.02.SS01.LO03")
    assert sid.depth == StableIdDepth.LEARNING_OBJECTIVE
    assert sid.kind == CkgNodeKind.LEARNING_OBJECTIVE
    assert sid.subject_code == "CS1"
    assert str(sid.parent_id()) == "CS1.T04.S04.02.SS01"


def test_builders_match_pattern() -> None:
    lo = StableCurriculumId.learning_objective("CS1", 4, 4, 2, 1, 3)
    assert lo.value == "CS1.T04.S04.02.SS01.LO03"
    section = StableCurriculumId.section("CS1", 4, 4, 2)
    assert section.value == "CS1.T04.S04.02"
    assert section.depth == StableIdDepth.SECTION


def test_educational_object_suffix() -> None:
    parent = StableCurriculumId.subsection("CS1", 4, 4, 2, 1)
    definition = StableCurriculumId.educational_object(
        parent, CkgNodeKind.DEFINITION, 3
    )
    assert definition.value == "CS1.T04.S04.02.SS01.DEF03"
    assert definition.kind == CkgNodeKind.DEFINITION


def test_subject_level_reading_reference() -> None:
    rr = StableCurriculumId.educational_object(
        "CS1", CkgNodeKind.READING_REFERENCE, 1
    )
    assert rr.value == "CS1.RR01"
    assert rr.parent_id() is not None
    assert rr.parent_id().value == "CS1"


def test_rejects_empty_and_malformed() -> None:
    with pytest.raises(ValueError):
        StableCurriculumId.of("")
    with pytest.raises(ValueError):
        StableCurriculumId.of("CS1.T04.S04")  # missing ordinal
    with pytest.raises(ValueError):
        StableCurriculumId.of("CS1.T04.S04.02.XX01")
    with pytest.raises(ValueError):
        StableCurriculumId.educational_object(
            "CS1", CkgNodeKind.DEFINITION, 1
        )


def test_parent_chain() -> None:
    lo = StableCurriculumId.of("CS1.T04.S04.02.SS01.LO03")
    ss = lo.parent_id()
    assert ss is not None and ss.value == "CS1.T04.S04.02.SS01"
    section = ss.parent_id()
    assert section is not None and section.value == "CS1.T04.S04.02"
    topic = section.parent_id()
    assert topic is not None and topic.value == "CS1.T04"
    subject = topic.parent_id()
    assert subject is not None and subject.value == "CS1"
    assert subject.parent_id() is None
