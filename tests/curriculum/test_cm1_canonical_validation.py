"""Canonical IFoA CM1 2026 syllabus fidelity validation.

Verifies the bundled curriculum JSON matches the official IFoA CM1 Syllabus
for the 2026 Examinations (April 2025): hierarchy, numbering, weights, and
uniqueness — without changing Educational Intelligence algorithms.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.curriculum.loader import load_from_json
from app.curriculum.models import CurriculumDefinition
from app.curriculum.repository import CurriculumRepository
from app.curriculum.validator import validate_curriculum_v2

# Official major-topic weights from the IFoA CM1 2026 syllabus.
OFFICIAL_SECTION_WEIGHTS: dict[str, float] = {
    "1": 25.0,
    "2": 20.0,
    "3": 20.0,
    "4": 35.0,
}

# Official learning-objective codes in published order.
# Undivided objectives (1.3, 1.4, 2.1, 4.1, 4.3, 4.5) are encoded as a single
# structural LO with code X.Y.1 carrying the official objective text.
OFFICIAL_LEARNING_OBJECTIVE_CODES: tuple[str, ...] = (
    # 1 Theory of interest rates
    "1.1.1",
    "1.1.2",
    "1.1.3",
    "1.2.1",
    "1.2.2",
    "1.3.1",
    "1.4.1",
    "1.5.1",
    "1.5.2",
    "1.5.3",
    "1.5.4",
    "1.5.5",
    "1.6.1",
    "1.6.2",
    "1.6.3",
    "1.7.1",
    "1.7.2",
    "1.7.3",
    "1.8.1",
    "1.8.2",
    # 2 Equation of value and its applications
    "2.1.1",
    "2.2.1",
    "2.2.2",
    "2.2.3",
    "2.2.4",
    "2.2.5",
    "2.3.1",
    "2.3.2",
    # 3 Decrement and multiple life models
    "3.1.1",
    "3.1.2",
    "3.1.3",
    "3.1.4",
    "3.2.1",
    "3.2.2",
    "3.2.3",
    "3.2.4",
    "3.2.5",
    "3.2.6",
    "3.2.7",
    "3.2.8",
    "3.3.1",
    "3.3.2",
    "3.4.1",
    "3.4.2",
    "3.4.3",
    "3.5.1",
    "3.5.2",
    "3.5.3",
    "3.5.4",
    # 4 Pricing and reserving
    "4.1.1",
    "4.2.1",
    "4.2.2",
    "4.2.3",
    "4.2.4",
    "4.2.5",
    "4.2.6",
    "4.3.1",
    "4.4.1",
    "4.4.2",
    "4.4.3",
    "4.5.1",
)

OFFICIAL_SUBTOPIC_CODES: tuple[str, ...] = (
    "1.1",
    "1.2",
    "1.3",
    "1.4",
    "1.5",
    "1.6",
    "1.7",
    "1.8",
    "2.1",
    "2.2",
    "2.3",
    "3.1",
    "3.2",
    "3.3",
    "3.4",
    "3.5",
    "4.1",
    "4.2",
    "4.3",
    "4.4",
    "4.5",
)

OFFICIAL_SECTION_TITLES: dict[str, str] = {
    "1": "Theory of interest rates",
    "2": "Equation of value and its applications",
    "3": "Decrement and multiple life models",
    "4": "Pricing and reserving",
}

CM1_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "curriculum"
    / "data"
    / "ifoa"
    / "cm1"
    / "2026.json"
)


@pytest.fixture(scope="module")
def cm1_raw() -> dict:
    return json.loads(CM1_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def cm1(cm1_raw: dict) -> CurriculumDefinition:
    curriculum = load_from_json(CM1_PATH)
    assert isinstance(curriculum, CurriculumDefinition)
    return curriculum


class TestCM1CanonicalLoad:
    def test_curriculum_loads_as_v2(self, cm1: CurriculumDefinition) -> None:
        assert cm1.exam_code == "CM1"
        assert cm1.provider == "IFoA"
        assert cm1.version == "2026"
        assert cm1.exam_name == "Actuarial Mathematics for Modelling"

    def test_load_auto_returns_v2(self) -> None:
        repo = CurriculumRepository()
        loaded = repo.load_auto("ifoa", "cm1", "2026")
        assert isinstance(loaded, CurriculumDefinition)
        validate_curriculum_v2(loaded)

    def test_validator_accepts_bundled_curriculum(
        self, cm1: CurriculumDefinition
    ) -> None:
        validate_curriculum_v2(cm1)


class TestCM1OfficialCoverage:
    def test_every_official_objective_exists(self, cm1: CurriculumDefinition) -> None:
        codes = [
            lo.code
            for section in cm1.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert codes == list(OFFICIAL_LEARNING_OBJECTIVE_CODES)

    def test_official_subtopic_numbering(self, cm1: CurriculumDefinition) -> None:
        codes = [topic.code for section in cm1.sections for topic in section.topics]
        assert codes == list(OFFICIAL_SUBTOPIC_CODES)

    def test_official_section_numbering_and_titles(
        self, cm1: CurriculumDefinition
    ) -> None:
        assert [section.code for section in cm1.sections] == ["1", "2", "3", "4"]
        for section in cm1.sections:
            assert section.title == OFFICIAL_SECTION_TITLES[section.code]


class TestCM1Hierarchy:
    def test_hierarchy_preserved(self, cm1: CurriculumDefinition) -> None:
        assert len(cm1.sections) == 4
        assert sum(len(section.topics) for section in cm1.sections) == 21
        assert (
            sum(
                len(topic.learning_objectives)
                for section in cm1.sections
                for topic in section.topics
            )
            == 61
        )

    def test_parent_child_relationships_valid(self, cm1: CurriculumDefinition) -> None:
        for section in cm1.sections:
            for topic in section.topics:
                assert topic.section_id == section.id
                assert topic.code.startswith(f"{section.code}.")
                for lo in topic.learning_objectives:
                    assert lo.topic_id == topic.id
                    assert lo.code.startswith(f"{topic.code}.")
                    assert lo.metadata.get("syllabus_code") == lo.code

    def test_display_order_matches_official_sequence(
        self, cm1: CurriculumDefinition
    ) -> None:
        for index, section in enumerate(
            sorted(cm1.sections, key=lambda s: s.display_order), start=1
        ):
            assert section.display_order == index
            assert section.code == str(index)
            for topic_index, topic in enumerate(
                sorted(section.topics, key=lambda t: t.display_order), start=1
            ):
                assert topic.display_order == topic_index
                for lo_index, lo in enumerate(
                    sorted(topic.learning_objectives, key=lambda o: o.display_order),
                    start=1,
                ):
                    assert lo.display_order == lo_index


class TestCM1WeightsAndIdentity:
    def test_weights_equal_official_syllabus(self, cm1: CurriculumDefinition) -> None:
        by_code = {section.code: section.exam_weight for section in cm1.sections}
        assert by_code == OFFICIAL_SECTION_WEIGHTS
        assert abs(sum(by_code.values()) - 100.0) < 1e-9

    def test_no_duplicate_ids(self, cm1: CurriculumDefinition) -> None:
        section_ids = [section.id for section in cm1.sections]
        topic_ids = [topic.id for section in cm1.sections for topic in section.topics]
        lo_ids = [
            lo.id
            for section in cm1.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert len(section_ids) == len(set(section_ids))
        assert len(topic_ids) == len(set(topic_ids))
        assert len(lo_ids) == len(set(lo_ids))

    def test_no_duplicate_official_codes(self, cm1: CurriculumDefinition) -> None:
        lo_codes = [
            lo.code
            for section in cm1.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert len(lo_codes) == len(set(lo_codes))


class TestCM1MetadataDoesNotAlterHierarchy:
    def test_metadata_present_without_changing_codes(self, cm1_raw: dict) -> None:
        for section in cm1_raw["sections"]:
            for topic in section["topics"]:
                for lo in topic["learning_objectives"]:
                    metadata = lo.get("metadata") or {}
                    assert metadata.get("syllabus_code") == lo["code"]
                    assert "estimated_hours" in metadata
                    assert "difficulty" in metadata
                    # Metadata must not invent alternate hierarchy keys.
                    assert "parent_code" not in metadata
                    assert "merged_into" not in metadata
