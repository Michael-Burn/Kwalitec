"""Canonical IFoA CM2 2026 syllabus fidelity validation.

Verifies the bundled curriculum JSON matches the official IFoA CM2 Syllabus
for the 2026 Examinations (April 2025): hierarchy, numbering, weights, and
uniqueness, without changing Educational Intelligence algorithms.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.curriculum.loader import load_from_json
from app.curriculum.models import CurriculumDefinition
from app.curriculum.repository import CurriculumRepository
from app.curriculum.validator import validate_curriculum_v2

# Official major-topic weights from the IFoA CM2 2026 syllabus.
OFFICIAL_SECTION_WEIGHTS: dict[str, float] = {
    "1": 10.0,
    "2": 10.0,
    "3": 30.0,
    "4": 20.0,
    "5": 30.0,
}

# Official learning-objective codes in published order.
OFFICIAL_LEARNING_OBJECTIVE_CODES: tuple[str, ...] = (
    # 1 Rational economic theory
    "1.1.1",
    "1.1.2",
    "1.2.1",
    "1.2.2",
    "1.2.3",
    "1.2.4",
    "1.2.5",
    "1.2.6",
    "1.2.7",
    # 2 Measures of investment risk
    "2.1.1",
    "2.1.2",
    "2.1.3",
    "2.1.4",
    "2.2.1",
    "2.2.2",
    # 3 Asset valuations
    "3.1.1",
    "3.1.2",
    "3.1.3",
    "3.1.4",
    "3.2.1",
    "3.2.2",
    "3.2.3",
    "3.2.4",
    "3.3.1",
    "3.3.2",
    "3.3.3",
    "3.3.4",
    "3.3.5",
    "3.4.1",
    "3.4.2",
    "3.4.3",
    "3.4.4",
    "3.4.5",
    "3.4.6",
    "3.5.1",
    "3.5.2",
    "3.5.3",
    "3.5.4",
    "3.5.5",
    "3.6.1",
    "3.6.2",
    "3.6.3",
    "3.6.4",
    # 4 Liability Valuations
    "4.1.1",
    "4.1.2",
    "4.1.3",
    "4.1.4",
    "4.1.5",
    "4.1.6",
    "4.1.7",
    "4.1.8",
    "4.2.1",
    "4.2.2",
    "4.2.3",
    "4.2.4",
    "4.2.5",
    "4.2.6",
    "4.2.7",
    "4.3.1",
    # 5 Option theory
    "5.1.1",
    "5.1.2",
    "5.1.3",
    "5.1.4",
    "5.2.1",
    "5.2.2",
    "5.2.3",
    "5.2.4",
    "5.2.5",
    "5.3.1",
    "5.3.2",
    "5.3.3",
    "5.3.4",
    "5.3.5",
    "5.3.6",
    "5.3.7",
)

OFFICIAL_SUBTOPIC_CODES: tuple[str, ...] = (
    "1.1",
    "1.2",
    "2.1",
    "2.2",
    "3.1",
    "3.2",
    "3.3",
    "3.4",
    "3.5",
    "3.6",
    "4.1",
    "4.2",
    "4.3",
    "5.1",
    "5.2",
    "5.3",
)

OFFICIAL_SECTION_TITLES: dict[str, str] = {
    "1": "Rational economic theory",
    "2": "Measures of investment risk",
    "3": "Asset valuations",
    "4": "Liability Valuations",
    "5": "Option theory",
}

CM2_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "curriculum"
    / "data"
    / "ifoa"
    / "cm2"
    / "2026.json"
)


@pytest.fixture(scope="module")
def cm2_raw() -> dict:
    return json.loads(CM2_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def cm2(cm2_raw: dict) -> CurriculumDefinition:
    curriculum = load_from_json(CM2_PATH)
    assert isinstance(curriculum, CurriculumDefinition)
    return curriculum


class TestCM2CanonicalLoad:
    def test_curriculum_loads_as_v2(self, cm2: CurriculumDefinition) -> None:
        assert cm2.exam_code == "CM2"
        assert cm2.provider == "IFoA"
        assert cm2.version == "2026"
        assert cm2.exam_name == "Economic Modelling"

    def test_load_auto_returns_v2(self) -> None:
        repo = CurriculumRepository()
        loaded = repo.load_auto("ifoa", "cm2", "2026")
        assert isinstance(loaded, CurriculumDefinition)
        validate_curriculum_v2(loaded)

    def test_validator_accepts_bundled_curriculum(
        self, cm2: CurriculumDefinition
    ) -> None:
        validate_curriculum_v2(cm2)

    def test_omits_invented_total_study_hours(self, cm2_raw: dict, cm2) -> None:
        """Official source did not specify a total hour figure; do not invent one."""
        assert "total_estimated_hours" not in cm2_raw
        metadata = cm2_raw.get("metadata") or {}
        assert "recommended_study_hours" not in metadata
        # Loader may derive an operational total from section hours; that must
        # not reintroduce an invented official claim into the JSON source.
        assert isinstance(cm2.total_estimated_hours, float)
        assert cm2.total_estimated_hours == sum(
            section.estimated_hours for section in cm2.sections
        )

    def test_source_document_metadata(self, cm2_raw: dict) -> None:
        metadata = cm2_raw["metadata"]
        assert metadata["source_document"] == "cm2_syllabus-2026-_final-proof.pdf"
        assert metadata["published"] == "April 2025"
        assert metadata["source"] == "IFoA CM2 Syllabus for the 2026 Examinations"
        assert metadata["qualification_level"] == "Core Principles"


class TestCM2OfficialCoverage:
    def test_every_official_objective_exists(self, cm2: CurriculumDefinition) -> None:
        codes = [
            lo.code
            for section in cm2.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert codes == list(OFFICIAL_LEARNING_OBJECTIVE_CODES)
        assert len(codes) == 75

    def test_official_subtopic_numbering(self, cm2: CurriculumDefinition) -> None:
        codes = [topic.code for section in cm2.sections for topic in section.topics]
        assert codes == list(OFFICIAL_SUBTOPIC_CODES)
        assert len(codes) == 16

    def test_official_section_numbering_and_titles(
        self, cm2: CurriculumDefinition
    ) -> None:
        assert [section.code for section in cm2.sections] == ["1", "2", "3", "4", "5"]
        for section in cm2.sections:
            assert section.title == OFFICIAL_SECTION_TITLES[section.code]


class TestCM2Hierarchy:
    def test_hierarchy_preserved(self, cm2: CurriculumDefinition) -> None:
        assert len(cm2.sections) == 5
        assert sum(len(section.topics) for section in cm2.sections) == 16
        assert (
            sum(
                len(topic.learning_objectives)
                for section in cm2.sections
                for topic in section.topics
            )
            == 75
        )

    def test_topic_4_3_has_single_founder_encoded_objective(
        self, cm2: CurriculumDefinition
    ) -> None:
        """Official syllabus has no numbered sub-objectives under 4.3.

        Founder decision: encode the topic statement itself as LO 4.3.1.
        """
        topic_43 = next(
            topic
            for section in cm2.sections
            for topic in section.topics
            if topic.code == "4.3"
        )
        assert len(topic_43.learning_objectives) == 1
        lo = topic_43.learning_objectives[0]
        assert lo.code == "4.3.1"
        assert lo.description == (
            "Value basic benefit guarantees using simulation techniques"
        )

    def test_parent_child_relationships_valid(self, cm2: CurriculumDefinition) -> None:
        for section in cm2.sections:
            for topic in section.topics:
                assert topic.section_id == section.id
                assert topic.code.startswith(f"{section.code}.")
                for lo in topic.learning_objectives:
                    assert lo.topic_id == topic.id
                    assert lo.code.startswith(f"{topic.code}.")
                    assert lo.metadata.get("syllabus_code") == lo.code

    def test_display_order_matches_official_sequence(
        self, cm2: CurriculumDefinition
    ) -> None:
        for index, section in enumerate(
            sorted(cm2.sections, key=lambda s: s.display_order), start=1
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


class TestCM2WeightsAndIdentity:
    def test_weights_equal_official_syllabus(self, cm2: CurriculumDefinition) -> None:
        by_code = {section.code: section.exam_weight for section in cm2.sections}
        assert by_code == OFFICIAL_SECTION_WEIGHTS
        assert abs(sum(by_code.values()) - 100.0) < 1e-9

    def test_no_duplicate_ids(self, cm2: CurriculumDefinition) -> None:
        section_ids = [section.id for section in cm2.sections]
        topic_ids = [topic.id for section in cm2.sections for topic in section.topics]
        lo_ids = [
            lo.id
            for section in cm2.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert len(section_ids) == len(set(section_ids))
        assert len(topic_ids) == len(set(topic_ids))
        assert len(lo_ids) == len(set(lo_ids))

    def test_no_duplicate_official_codes(self, cm2: CurriculumDefinition) -> None:
        lo_codes = [
            lo.code
            for section in cm2.sections
            for topic in section.topics
            for lo in topic.learning_objectives
        ]
        assert len(lo_codes) == len(set(lo_codes))


class TestCM2MetadataDoesNotAlterHierarchy:
    def test_metadata_present_without_changing_codes(self, cm2_raw: dict) -> None:
        for section in cm2_raw["sections"]:
            for topic in section["topics"]:
                for lo in topic["learning_objectives"]:
                    metadata = lo.get("metadata") or {}
                    assert metadata.get("syllabus_code") == lo["code"]
                    assert "estimated_hours" in metadata
                    assert "difficulty" in metadata
                    # Metadata must not invent alternate hierarchy keys.
                    assert "parent_code" not in metadata
                    assert "merged_into" not in metadata
