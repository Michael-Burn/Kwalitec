"""Unit tests for V2 Curriculum Engine (Canonical Format).

Covers:
    - V2 data models (CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition)
    - V2 JSON Schema validation
    - V2 loader (load_from_dict, load_from_json, load_curriculum_v2)
    - V2 validator (validate_curriculum_v2)
    - V2 repository (CurriculumRepository V2 methods)
    - Format detection
    - Backwards compatibility with V1
"""

from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Test Data
# ═══════════════════════════════════════════════════════════════════════════════

def _valid_v2_curriculum_dict() -> dict:
    """Return a minimal valid V2 curriculum dict for use across tests."""
    return {
        "exam_code": "CS1",
        "exam_name": "Actuarial Statistics",
        "provider": "IFoA",
        "version": "2026",
        "effective_date": "2026-01-01",
        "superseded_date": None,
        "total_estimated_hours": 190.0,
        "description": "The aim of the CS1 syllabus is to provide a grounding in mathematical and statistical techniques.",
        "sections": [
            {
                "id": "CS1-A",
                "code": "CS1-A",
                "title": "Random Variables and Distributions",
                "description": "Understand and apply key concepts related to random variables.",
                "exam_weight": 50.0,
                "estimated_hours": 45.0,
                "difficulty": "foundational",
                "display_order": 1,
                "topics": [
                    {
                        "id": "CS1-A-T01",
                        "section_id": "CS1-A",
                        "code": "CS1-A.1",
                        "title": "Discrete and Continuous Random Variables",
                        "description": "Define and distinguish between discrete, continuous and mixed random variables.",
                        "estimated_minutes": 90,
                        "difficulty": "foundational",
                        "display_order": 1,
                        "learning_objectives": [
                            {
                                "id": "CS1-A-T01-LO01",
                                "topic_id": "CS1-A-T01",
                                "code": "CS1-A.1.1",
                                "description": "Define and distinguish between discrete, continuous and mixed random variables.",
                                "cognitive_level": "understand",
                                "estimated_minutes": 30,
                                "learning_type": "concept",
                                "display_order": 1
                            },
                            {
                                "id": "CS1-A-T01-LO02",
                                "topic_id": "CS1-A-T01",
                                "code": "CS1-A.1.2",
                                "description": "Calculate and interpret probability mass functions.",
                                "cognitive_level": "apply",
                                "estimated_minutes": 45,
                                "learning_type": "procedure",
                                "display_order": 2
                            }
                        ]
                    },
                    {
                        "id": "CS1-A-T02",
                        "section_id": "CS1-A",
                        "code": "CS1-A.2",
                        "title": "Expectation, Variance, and Moments",
                        "description": "Calculate and interpret expectation, variance, skewness, and kurtosis.",
                        "estimated_minutes": 120,
                        "difficulty": "foundational",
                        "display_order": 2,
                        "learning_objectives": [
                            {
                                "id": "CS1-A-T02-LO01",
                                "topic_id": "CS1-A-T02",
                                "code": "CS1-A.2.1",
                                "description": "Calculate and interpret expectation, variance, skewness and kurtosis.",
                                "cognitive_level": "apply",
                                "estimated_minutes": 45,
                                "learning_type": "procedure",
                                "display_order": 1
                            }
                        ]
                    }
                ]
            },
            {
                "id": "CS1-B",
                "code": "CS1-B",
                "title": "Common Statistical Distributions",
                "description": "Apply the binomial, Poisson, negative binomial, exponential, gamma, normal, log-normal, chi-squared, t and F distributions.",
                "exam_weight": 50.0,
                "estimated_hours": 35.0,
                "difficulty": "intermediate",
                "display_order": 2,
                "topics": [
                    {
                        "id": "CS1-B-T01",
                        "section_id": "CS1-B",
                        "code": "CS1-B.1",
                        "title": "Discrete Distributions",
                        "description": "Apply the binomial, Poisson, and negative binomial distributions.",
                        "estimated_minutes": 90,
                        "difficulty": "intermediate",
                        "display_order": 1,
                        "learning_objectives": [
                            {
                                "id": "CS1-B-T01-LO01",
                                "topic_id": "CS1-B-T01",
                                "code": "CS1-B.1.1",
                                "description": "Derive moments, mode and quantiles for the binomial, Poisson and negative binomial distributions.",
                                "cognitive_level": "apply",
                                "estimated_minutes": 45,
                                "learning_type": "procedure",
                                "display_order": 1
                            }
                        ]
                    }
                ]
            }
        ],
        "metadata": {
            "source_url": "https://www.actuaries.org.uk/studying/curriculum/actuarial-statistics",
            "qualification_level": "Core Principles",
            "language": "en"
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Models
# ═══════════════════════════════════════════════════════════════════════════════

class TestLearningObjectiveDefinition:
    """Tests for the LearningObjectiveDefinition dataclass."""

    def test_create_minimal(self):
        from app.curriculum.models import LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01",
            topic_id="CS1-A-T01",
            code="CS1-A.1.1",
            description="Define discrete random variables.",
            cognitive_level="understand",
            estimated_minutes=30,
            learning_type="concept",
        )
        assert lo.id == "CS1-A-T01-LO01"
        assert lo.topic_id == "CS1-A-T01"
        assert lo.code == "CS1-A.1.1"
        assert lo.cognitive_level == "understand"
        assert lo.estimated_minutes == 30
        assert lo.learning_type == "concept"
        assert lo.display_order == 1

    def test_create_with_display_order(self):
        from app.curriculum.models import LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO02",
            topic_id="CS1-A-T01",
            code="CS1-A.1.2",
            description="Calculate PMFs.",
            cognitive_level="apply",
            estimated_minutes=45,
            learning_type="procedure",
            display_order=2,
        )
        assert lo.display_order == 2

    def test_is_frozen(self):
        from app.curriculum.models import LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="X", topic_id="Y", code="Z", description="d",
            cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        with pytest.raises(Exception):
            lo.id = "new_id"  # type: ignore[misc]

    def test_equality(self):
        from app.curriculum.models import LearningObjectiveDefinition

        a = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        b = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        c = LearningObjectiveDefinition(
            id="CS1-A-T01-LO02", topic_id="CS1-A-T01", code="CS1-A.1.2",
            description="other", cognitive_level="apply", estimated_minutes=45, learning_type="procedure"
        )
        assert a == b
        assert a != c


class TestTopicDefinition:
    """Tests for the TopicDefinition dataclass."""

    def test_create_minimal(self):
        from app.curriculum.models import TopicDefinition

        t = TopicDefinition(
            id="CS1-A-T01",
            section_id="CS1-A",
            code="CS1-A.1",
            title="Discrete Random Variables",
            description="Define and distinguish between discrete random variables.",
            estimated_minutes=90,
            difficulty="foundational",
        )
        assert t.id == "CS1-A-T01"
        assert t.section_id == "CS1-A"
        assert t.code == "CS1-A.1"
        assert t.estimated_minutes == 90
        assert t.difficulty == "foundational"
        assert t.display_order == 1
        assert t.learning_objectives == []

    def test_create_with_learning_objectives(self):
        from app.curriculum.models import LearningObjectiveDefinition, TopicDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t = TopicDefinition(
            id="CS1-A-T01",
            section_id="CS1-A",
            code="CS1-A.1",
            title="Discrete Random Variables",
            description="Define and distinguish between discrete random variables.",
            estimated_minutes=90,
            difficulty="foundational",
            display_order=1,
            learning_objectives=[lo],
        )
        assert len(t.learning_objectives) == 1
        assert t.learning_objectives[0].id == "CS1-A-T01-LO01"

    def test_is_frozen(self):
        from app.curriculum.models import TopicDefinition

        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Title", description="Desc", estimated_minutes=90, difficulty="foundational"
        )
        with pytest.raises(Exception):
            t.title = "New Title"  # type: ignore[misc]

    def test_hash_uses_id(self):
        from app.curriculum.models import TopicDefinition

        t1 = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="One", description="d", estimated_minutes=90, difficulty="foundational"
        )
        t2 = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Two", description="d", estimated_minutes=90, difficulty="foundational"
        )
        t3 = TopicDefinition(
            id="CS1-A-T02", section_id="CS1-A", code="CS1-A.2",
            title="One", description="d", estimated_minutes=90, difficulty="foundational"
        )
        assert hash(t1) == hash(t2)
        assert hash(t1) != hash(t3)

    def test_equality(self):
        from app.curriculum.models import TopicDefinition

        a = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="T", description="d", estimated_minutes=90, difficulty="foundational"
        )
        b = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="T", description="d", estimated_minutes=90, difficulty="foundational"
        )
        c = TopicDefinition(
            id="CS1-A-T02", section_id="CS1-A", code="CS1-A.2",
            title="T", description="d", estimated_minutes=90, difficulty="foundational"
        )
        assert a == b
        assert a != c


class TestSectionDefinition:
    """Tests for the SectionDefinition dataclass."""

    def test_create_minimal(self):
        from app.curriculum.models import SectionDefinition

        s = SectionDefinition(
            id="CS1-A",
            code="CS1-A",
            title="Random Variables",
            description="Understand random variables.",
            exam_weight=25.0,
            estimated_hours=45.0,
            difficulty="foundational",
        )
        assert s.id == "CS1-A"
        assert s.code == "CS1-A"
        assert s.exam_weight == 25.0
        assert s.estimated_hours == 45.0
        assert s.difficulty == "foundational"
        assert s.display_order == 1
        assert s.topics == []

    def test_create_with_topics(self):
        from app.curriculum.models import SectionDefinition, TopicDefinition

        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Discrete RVs", description="d", estimated_minutes=90, difficulty="foundational"
        )
        s = SectionDefinition(
            id="CS1-A",
            code="CS1-A",
            title="Random Variables",
            description="Understand random variables.",
            exam_weight=25.0,
            estimated_hours=45.0,
            difficulty="foundational",
            display_order=1,
            topics=[t],
        )
        assert len(s.topics) == 1
        assert s.topics[0].id == "CS1-A-T01"

    def test_is_frozen(self):
        from app.curriculum.models import SectionDefinition

        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Title", description="Desc",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        with pytest.raises(Exception):
            s.title = "New Title"  # type: ignore[misc]

    def test_hash_uses_id(self):
        from app.curriculum.models import SectionDefinition

        s1 = SectionDefinition(
            id="CS1-A", code="CS1-A", title="One", description="d",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        s2 = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Two", description="d",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        s3 = SectionDefinition(
            id="CS1-B", code="CS1-B", title="One", description="d",
            exam_weight=20.0, estimated_hours=35.0, difficulty="intermediate"
        )
        assert hash(s1) == hash(s2)
        assert hash(s1) != hash(s3)

    def test_equality(self):
        from app.curriculum.models import SectionDefinition

        a = SectionDefinition(
            id="CS1-A", code="CS1-A", title="T", description="d",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        b = SectionDefinition(
            id="CS1-A", code="CS1-A", title="T", description="d",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        c = SectionDefinition(
            id="CS1-B", code="CS1-B", title="T", description="d",
            exam_weight=20.0, estimated_hours=35.0, difficulty="intermediate"
        )
        assert a == b
        assert a != c


class TestCurriculumDefinition:
    """Tests for the CurriculumDefinition dataclass."""

    def test_create(self):
        from app.curriculum.models import CurriculumDefinition, SectionDefinition

        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Random Variables", description="d",
            exam_weight=25.0, estimated_hours=45.0, difficulty="foundational"
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=190.0,
            description="The aim of the CS1 syllabus...",
            sections=[s],
            metadata={"source_url": "https://..."},
        )
        assert c.exam_code == "CS1"
        assert c.exam_name == "Actuarial Statistics"
        assert c.provider == "IFoA"
        assert c.version == "2026"
        assert c.effective_date == date(2026, 1, 1)
        assert c.superseded_date is None
        assert c.total_estimated_hours == 190.0
        assert len(c.sections) == 1
        assert c.metadata == {"source_url": "https://..."}

    def test_exam_key(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=190.0,
            description="d",
        )
        assert c.exam_key == "ifoa/cs1"

    def test_version_key(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="CM1",
            exam_name="Actuarial Mathematics",
            provider="IFoA",
            version="2025",
            effective_date=date(2025, 1, 1),
            superseded_date=None,
            total_estimated_hours=200.0,
            description="d",
        )
        assert c.version_key == "ifoa/cm1/2025"

    def test_exam_key_capitalisation(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="Cs1",
            exam_name="Actuarial Statistics",
            provider="IfoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=190.0,
            description="d",
        )
        assert c.exam_key == "ifoa/cs1"

    def test_is_frozen(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=190.0,
            description="d",
        )
        with pytest.raises(Exception):
            c.exam_code = "CM1"  # type: ignore[misc]

    def test_defaults(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=0.0,
            description="d",
        )
        assert c.sections == []
        assert c.metadata == {}

    def test_effective_to_set(self):
        from app.curriculum.models import CurriculumDefinition

        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=date(2028, 12, 31),
            total_estimated_hours=190.0,
            description="d",
        )
        assert c.superseded_date == date(2028, 12, 31)


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Schema
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetV2Schema:
    """Tests for get_v2_schema()."""

    def test_returns_dict(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        assert isinstance(schema, dict)

    def test_has_required_keys(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        assert "$schema" in schema
        assert "type" in schema
        assert schema["type"] == "object"
        assert "required" in schema
        required = schema["required"]
        assert "exam_code" in required
        assert "exam_name" in required
        assert "provider" in required
        assert "version" in required
        assert "effective_date" in required
        assert "sections" in required

    def test_exam_code_pattern(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        ec = schema["properties"]["exam_code"]
        assert ec["pattern"] == r"^[A-Z]{2}[0-9]$"

    def test_sections_min_items(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        assert schema["properties"]["sections"]["minItems"] == 1

    def test_section_id_pattern(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        sid = schema["properties"]["sections"]["items"]["properties"]["id"]
        assert sid["pattern"] == r"^[A-Z]{2}[0-9]-[A-Z]$"

    def test_topic_id_pattern(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        tid = schema["properties"]["sections"]["items"]["properties"]["topics"]["items"]["properties"]["id"]
        assert tid["pattern"] == r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$"

    def test_lo_id_pattern(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        lo_schema = schema["properties"]["sections"]["items"]["properties"]["topics"]["items"]["properties"]["learning_objectives"]["items"]
        lid = lo_schema["properties"]["id"]
        assert lid["pattern"] == r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}$"

    def test_cognitive_level_enum(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        lo_schema = schema["properties"]["sections"]["items"]["properties"]["topics"]["items"]["properties"]["learning_objectives"]["items"]
        cog = lo_schema["properties"]["cognitive_level"]
        assert cog["enum"] == ["remember", "understand", "apply", "analyze", "evaluate", "create"]

    def test_learning_type_enum(self):
        from app.curriculum.schemas import get_v2_schema

        schema = get_v2_schema()
        lo_schema = schema["properties"]["sections"]["items"]["properties"]["topics"]["items"]["properties"]["learning_objectives"]["items"]
        lt = lo_schema["properties"]["learning_type"]
        assert lt["enum"] == ["concept", "procedure", "problem_solving", "application", "analysis"]


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Format Detection
# ═══════════════════════════════════════════════════════════════════════════════

class TestDetectFormat:
    """Tests for detect_format()."""

    def test_detects_v1_format(self):
        from app.curriculum.schemas import detect_format

        data = {"organisation": "IFoA", "examination": "X", "paper": "CS1", "topics": []}
        assert detect_format(data) == "v1"

    def test_detects_v2_format(self):
        from app.curriculum.schemas import detect_format

        data = {"exam_code": "CS1", "exam_name": "X", "provider": "IFoA", "sections": []}
        assert detect_format(data) == "v2"

    def test_raises_on_ambiguous(self):
        from app.curriculum.schemas import detect_format

        data = {"unknown": "format"}
        with pytest.raises(ValueError, match="Cannot determine"):
            detect_format(data)

    def test_raises_on_empty(self):
        from app.curriculum.schemas import detect_format

        data = {}
        with pytest.raises(ValueError, match="Cannot determine"):
            detect_format(data)


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Schema Validation
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidateV2Instance:
    """Tests for validate_v2_instance()."""

    def test_valid_instance_passes(self):
        from app.curriculum.schemas import validate_v2_instance

        errors = validate_v2_instance(_valid_v2_curriculum_dict())
        assert errors == []

    def test_missing_required_field(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        del data["exam_code"]
        errors = validate_v2_instance(data)
        assert any("exam_code" in e for e in errors)

    def test_multiple_missing_fields(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        del data["exam_code"]
        del data["provider"]
        errors = validate_v2_instance(data)
        assert len(errors) >= 2

    def test_invalid_exam_code_not_digits(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["exam_code"] = "CS"
        errors = validate_v2_instance(data)
        assert any("exam_code" in e for e in errors)

    def test_invalid_exam_code_pattern(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["exam_code"] = "CS12"  # Too long
        errors = validate_v2_instance(data)
        assert any("exam_code" in e for e in errors)

    def test_invalid_version_not_digits(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["version"] = "abcd"
        errors = validate_v2_instance(data)
        assert any("version" in e for e in errors)

    def test_invalid_version_wrong_length(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["version"] = "202"
        errors = validate_v2_instance(data)
        assert any("version" in e for e in errors)

    def test_empty_sections_array(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"] = []
        errors = validate_v2_instance(data)
        assert any("sections" in e for e in errors)

    def test_section_missing_required_field(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        del data["sections"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("id" in e for e in errors)

    def test_duplicate_section_id(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][1]["id"] = data["sections"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_invalid_section_id_pattern(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["id"] = "CS1-A1"  # Wrong pattern
        errors = validate_v2_instance(data)
        assert any("does not match pattern" in e for e in errors)

    def test_invalid_section_weight(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["exam_weight"] = 150.0
        errors = validate_v2_instance(data)
        assert any("exam_weight" in e for e in errors)

    def test_negative_estimated_hours(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["estimated_hours"] = -5.0
        errors = validate_v2_instance(data)
        assert any("estimated_hours" in e for e in errors)

    def test_invalid_difficulty_value(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["difficulty"] = "expert"
        errors = validate_v2_instance(data)
        assert any("difficulty" in e for e in errors)

    def test_topic_missing_required_field(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        del data["sections"][0]["topics"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("id" in e for e in errors)

    def test_duplicate_topic_id(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][1]["id"] = data["sections"][0]["topics"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_invalid_topic_id_pattern(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["id"] = "CS1-A-T1"  # Not zero-padded
        errors = validate_v2_instance(data)
        assert any("does not match pattern" in e for e in errors)

    def test_topic_section_id_mismatch(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["section_id"] = "CS1-B"
        errors = validate_v2_instance(data)
        assert any("section_id" in e for e in errors)

    def test_negative_estimated_minutes(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["estimated_minutes"] = -10
        errors = validate_v2_instance(data)
        assert any("estimated_minutes" in e for e in errors)

    def test_lo_missing_required_field(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        del data["sections"][0]["topics"][0]["learning_objectives"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("id" in e for e in errors)

    def test_duplicate_lo_id(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][1]["id"] = data["sections"][0]["topics"][0]["learning_objectives"][0]["id"]
        errors = validate_v2_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_invalid_lo_id_pattern(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][0]["id"] = "CS1-A-T01-LO1"  # Not zero-padded
        errors = validate_v2_instance(data)
        assert any("does not match pattern" in e for e in errors)

    def test_lo_topic_id_mismatch(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][0]["topic_id"] = "CS1-A-T02"
        errors = validate_v2_instance(data)
        assert any("topic_id" in e for e in errors)

    def test_duplicate_lo_code(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][1]["code"] = data["sections"][0]["topics"][0]["learning_objectives"][0]["code"]
        errors = validate_v2_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_invalid_cognitive_level(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][0]["cognitive_level"] = "memorize"
        errors = validate_v2_instance(data)
        assert any("cognitive_level" in e for e in errors)

    def test_invalid_learning_type(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][0]["learning_type"] = "memorization"
        errors = validate_v2_instance(data)
        assert any("learning_type" in e for e in errors)

    def test_negative_lo_estimated_minutes(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"][0]["estimated_minutes"] = -5
        errors = validate_v2_instance(data)
        assert any("estimated_minutes" in e for e in errors)

    def test_weighting_out_of_range(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["exam_weight"] = 150.0
        errors = validate_v2_instance(data)
        assert any("exam_weight" in e for e in errors)

    def test_total_weight_out_of_tolerance(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        # Make total weight 90% (outside 95-105% tolerance)
        data["sections"][0]["exam_weight"] = 70.0
        data["sections"][1]["exam_weight"] = 20.0
        errors = validate_v2_instance(data)
        assert any("weight" in e.lower() for e in errors)

    def test_empty_topics_array(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"] = []
        errors = validate_v2_instance(data)
        assert any("topics" in e for e in errors)

    def test_empty_learning_objectives_array(self):
        from app.curriculum.schemas import validate_v2_instance

        data = _valid_v2_curriculum_dict()
        data["sections"][0]["topics"][0]["learning_objectives"] = []
        errors = validate_v2_instance(data)
        assert any("learning_objectives" in e for e in errors)


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Loader
# ═══════════════════════════════════════════════════════════════════════════════

class TestLoadV2FromDict:
    """Tests for load_from_dict() with V2 data."""

    def test_builds_valid_v2_curriculum(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition

        c = load_from_dict(_valid_v2_curriculum_dict(), version="v2")
        assert isinstance(c, CurriculumDefinition)
        assert c.exam_code == "CS1"
        assert c.provider == "IFoA"
        assert c.version == "2026"
        assert len(c.sections) == 2
        assert c.sections[0].id == "CS1-A"
        assert c.sections[0].topics[0].id == "CS1-A-T01"

    def test_schema_validation_rejects_invalid_v2(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.exceptions import CurriculumLoadError

        data = _valid_v2_curriculum_dict()
        del data["exam_code"]
        with pytest.raises(CurriculumLoadError):
            load_from_dict(data, version="v2")

    def test_learning_objectives_are_built(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_v2_curriculum_dict(), version="v2")
        topic = c.sections[0].topics[0]
        assert len(topic.learning_objectives) == 2
        lo = topic.learning_objectives[0]
        assert lo.id == "CS1-A-T01-LO01"
        assert lo.cognitive_level == "understand"
        assert lo.learning_type == "concept"

    def test_metadata_present(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_v2_curriculum_dict(), version="v2")
        assert "source_url" in c.metadata
        assert c.metadata["source_url"] == "https://www.actuaries.org.uk/studying/curriculum/actuarial-statistics"

    def test_metadata_default_when_missing(self):
        from app.curriculum.loader import load_from_dict

        data = _valid_v2_curriculum_dict()
        del data["metadata"]
        c = load_from_dict(data, version="v2")
        assert c.metadata == {}

    def test_superseded_date_default(self):
        from app.curriculum.loader import load_from_dict

        data = _valid_v2_curriculum_dict()
        del data["superseded_date"]
        c = load_from_dict(data, version="v2")
        assert c.superseded_date == date(2099, 12, 31)

    def test_auto_detects_v2_format(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition

        c = load_from_dict(_valid_v2_curriculum_dict())  # No version specified
        assert isinstance(c, CurriculumDefinition)
        assert c.exam_code == "CS1"

    def test_auto_detects_v1_format(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import Curriculum

        data = {
            "organisation": "IFoA",
            "examination": "Actuarial Statistics",
            "paper": "CS1",
            "syllabus_version": "2026",
            "effective_from": "2026-01-01",
            "effective_to": None,
            "metadata": {},
            "topics": [
                {
                    "id": "cs1-2026-1",
                    "code": "CS1-A",
                    "title": "Random Variables",
                    "description": "d",
                    "weighting": 100.0,
                    "estimated_hours": 10.0,
                    "difficulty": "foundational",
                    "prerequisites": [],
                    "learning_outcomes": [
                        {
                            "id": "lo-1",
                            "code": "CS1-A-1",
                            "description": "Define random variables.",
                        }
                    ],
                }
            ],
        }
        c = load_from_dict(data)  # No version specified
        assert isinstance(c, Curriculum)
        assert c.organisation == "IFoA"


class TestLoadV2FromJson:
    """Tests for load_from_json() with V2 data."""

    def test_loads_valid_v2_file(self):
        from app.curriculum.loader import load_from_json
        from app.curriculum.models import CurriculumDefinition

        data = _valid_v2_curriculum_dict()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp_path = f.name

        try:
            c = load_from_json(tmp_path, version="v2")
            assert isinstance(c, CurriculumDefinition)
            assert c.exam_code == "CS1"
            assert len(c.sections) == 2
        finally:
            Path(tmp_path).unlink()

    def test_file_not_found(self):
        from app.curriculum.loader import load_from_json
        from app.curriculum.exceptions import CurriculumLoadError

        with pytest.raises(CurriculumLoadError):
            load_from_json("/nonexistent/path/curriculum.json", version="v2")

    def test_invalid_json(self):
        from app.curriculum.loader import load_from_json
        from app.curriculum.exceptions import CurriculumLoadError

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("not valid json {{{")
            tmp_path = f.name

        try:
            with pytest.raises(CurriculumLoadError, match="Invalid JSON"):
                load_from_json(tmp_path, version="v2")
        finally:
            Path(tmp_path).unlink()

    def test_top_level_not_object(self):
        from app.curriculum.loader import load_from_json
        from app.curriculum.exceptions import CurriculumLoadError

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump([1, 2, 3], f)
            tmp_path = f.name

        try:
            with pytest.raises(CurriculumLoadError, match="object"):
                load_from_json(tmp_path, version="v2")
        finally:
            Path(tmp_path).unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Validator
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidateCurriculumV2:
    """Tests for validate_curriculum_v2()."""

    def _curriculum(self, **overrides):
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=45.0,
            description="d",
            sections=[s],
        )
        # Apply overrides
        for k, v in overrides.items():
            object.__setattr__(c, k, v)
        return c

    def test_valid_passes(self):
        from app.curriculum.validator import validate_curriculum_v2

        c = self._curriculum()
        validate_curriculum_v2(c)  # should not raise

    def test_duplicate_section_id_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s1 = SectionDefinition(
            id="DUP", code="CS1-A", title="S1", description="d",
            exam_weight=50.0, estimated_hours=20.0, difficulty="foundational", topics=[t]
        )
        s2 = SectionDefinition(
            id="DUP", code="CS1-B", title="S2", description="d",
            exam_weight=50.0, estimated_hours=20.0, difficulty="intermediate", topics=[]
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s1, s2])

        with pytest.raises(CurriculumValidationError, match="Duplicate section id"):
            validate_curriculum_v2(c)

    def test_duplicate_topic_id_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t1 = TopicDefinition(
            id="DUP", section_id="CS1-A", code="CS1-A.1",
            title="T1", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        t2 = TopicDefinition(
            id="DUP", section_id="CS1-A", code="CS1-A.2",
            title="T2", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t1, t2],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="Duplicate topic id"):
            validate_curriculum_v2(c)

    def test_duplicate_lo_id_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo1 = LearningObjectiveDefinition(
            id="DUP", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d1", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        lo2 = LearningObjectiveDefinition(
            id="DUP", topic_id="CS1-A-T01", code="CS1-A.1.2",
            description="d2", cognitive_level="apply", estimated_minutes=45, learning_type="procedure"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo1, lo2],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="Duplicate learning objective id"):
            validate_curriculum_v2(c)

    def test_duplicate_lo_code_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo1 = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="DUP",
            description="d1", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        lo2 = LearningObjectiveDefinition(
            id="CS1-A-T01-LO02", topic_id="CS1-A-T01", code="DUP",
            description="d2", cognitive_level="apply", estimated_minutes=45, learning_type="procedure"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo1, lo2],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="Duplicate learning objective code"):
            validate_curriculum_v2(c)

    def test_weighting_out_of_range_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition

        c = self._curriculum()
        object.__setattr__(c, "sections", [
            SectionDefinition(
                id="CS1-A", code="CS1-A", title="S1", description="d",
                exam_weight=50.0, estimated_hours=20.0, difficulty="foundational", topics=[]
            )
        ])

        with pytest.raises(CurriculumValidationError, match="weight"):
            validate_curriculum_v2(c)

    def test_non_positive_estimated_hours_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError

        c = self._curriculum()
        object.__setattr__(c.sections[0], "estimated_hours", 0.0)

        with pytest.raises(CurriculumValidationError, match="estimated_hours"):
            validate_curriculum_v2(c)

    def test_non_positive_estimated_minutes_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError

        c = self._curriculum()
        object.__setattr__(c.sections[0].topics[0], "estimated_minutes", 0)

        with pytest.raises(CurriculumValidationError, match="estimated_minutes"):
            validate_curriculum_v2(c)

    def test_invalid_section_id_reference_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-B", code="CS1-A.1",  # Wrong section_id
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="section_id"):
            validate_curriculum_v2(c)

    def test_invalid_topic_id_reference_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T02", code="CS1-A.1.1",  # Wrong topic_id
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="topic_id"):
            validate_curriculum_v2(c)

    def test_invalid_difficulty_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError

        c = self._curriculum()
        object.__setattr__(c.sections[0], "difficulty", "expert")

        with pytest.raises(CurriculumValidationError, match="difficulty"):
            validate_curriculum_v2(c)

    def test_invalid_cognitive_level_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import LearningObjectiveDefinition, TopicDefinition, SectionDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="memorize", estimated_minutes=30, learning_type="concept"  # Invalid
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="cognitive_level"):
            validate_curriculum_v2(c)

    def test_invalid_learning_type_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import LearningObjectiveDefinition, TopicDefinition, SectionDefinition

        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="memorization"  # Invalid
        )
        t = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section", description="d",
            exam_weight=100.0, estimated_hours=45.0, difficulty="foundational",
            topics=[t],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError, match="learning_type"):
            validate_curriculum_v2(c)

    def test_non_positive_display_order_raises(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError

        c = self._curriculum()
        object.__setattr__(c.sections[0], "display_order", 0)

        with pytest.raises(CurriculumValidationError, match="display_order"):
            validate_curriculum_v2(c)

    def test_aggregates_multiple_errors(self):
        from app.curriculum.validator import validate_curriculum_v2
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import SectionDefinition

        s = SectionDefinition(
            id="CS1-A", code="CS1-A", title="S", description="d",
            exam_weight=50.0, estimated_hours=0.0, difficulty="expert",  # Two errors
            display_order=0,  # Third error
            topics=[],
        )
        c = self._curriculum()
        object.__setattr__(c, "sections", [s])

        with pytest.raises(CurriculumValidationError) as exc_info:
            validate_curriculum_v2(c)
        assert len(exc_info.value.messages) >= 3


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Repository
# ═══════════════════════════════════════════════════════════════════════════════

class TestCurriculumRepositoryV2:
    """Tests for CurriculumRepository V2 methods."""

    def test_load_v2_caches(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        # We can't actually load a V2 file since we don't have one, but we can test the cache logic
        # by manually adding a V2 curriculum
        from app.curriculum.models import CurriculumDefinition, SectionDefinition
        
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Test", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational"
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        # Manually cache it
        repo._cache["ifoa/cs1/2026"] = c
        assert repo.is_loaded_v2("ifoa", "cs1", "2026")
        result = repo.get_curriculum_v2("ifoa", "cs1", "2026")
        assert result.exam_code == "CS1"

    def test_get_sections(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition

        repo = CurriculumRepository()
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=50.0, estimated_hours=20.0, difficulty="foundational"
        )
        section2 = SectionDefinition(
            id="CS1-B", code="CS1-B", title="Section B", description="d",
            exam_weight=50.0, estimated_hours=20.0, difficulty="intermediate"
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=40.0,
            description="d",
            sections=[section, section2],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        sections = repo.get_sections("ifoa", "cs1", "2026")
        assert len(sections) == 2
        assert sections[0].id == "CS1-A"
        assert sections[1].id == "CS1-B"

    def test_get_section_found(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition

        repo = CurriculumRepository()
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational"
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        s = repo.get_section("ifoa", "cs1", "2026", "CS1-A")
        assert s.title == "Section A"

    def test_get_section_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError
        from app.curriculum.models import CurriculumDefinition, SectionDefinition

        repo = CurriculumRepository()
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational"
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        with pytest.raises(CurriculumNotFoundError):
            repo.get_section("ifoa", "cs1", "2026", "CS1-Z")

    def test_get_topics_v2(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition

        repo = CurriculumRepository()
        topic1 = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational"
        )
        topic2 = TopicDefinition(
            id="CS1-A-T02", section_id="CS1-A", code="CS1-A.2",
            title="Topic 2", description="d", estimated_minutes=90, difficulty="foundational"
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic1, topic2],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        topics = repo.get_topics_v2("ifoa", "cs1", "2026", "CS1-A")
        assert len(topics) == 2
        assert topics[0].id == "CS1-A-T01"
        assert topics[1].id == "CS1-A-T02"

    def test_get_topic_v2_found(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition

        repo = CurriculumRepository()
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational"
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        t = repo.get_topic_v2("ifoa", "cs1", "2026", "CS1-A-T01")
        assert t.title == "Topic 1"

    def test_get_topic_v2_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition

        repo = CurriculumRepository()
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational"
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        with pytest.raises(CurriculumNotFoundError):
            repo.get_topic_v2("ifoa", "cs1", "2026", "CS1-A-T99")

    def test_get_learning_objectives(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        repo = CurriculumRepository()
        lo1 = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="LO1", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        lo2 = LearningObjectiveDefinition(
            id="CS1-A-T01-LO02", topic_id="CS1-A-T01", code="CS1-A.1.2",
            description="LO2", cognitive_level="apply", estimated_minutes=45, learning_type="procedure"
        )
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo1, lo2],
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        los = repo.get_learning_objectives("ifoa", "cs1", "2026", "CS1-A-T01")
        assert len(los) == 2
        assert los[0].id == "CS1-A-T01-LO01"
        assert los[1].id == "CS1-A-T01-LO02"

    def test_get_learning_objective_found(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        repo = CurriculumRepository()
        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="Define RVs", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        result = repo.get_learning_objective("ifoa", "cs1", "2026", "CS1-A-T01-LO01")
        assert result.description == "Define RVs"
        assert result.cognitive_level == "understand"

    def test_get_learning_objective_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        repo = CurriculumRepository()
        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="d", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        with pytest.raises(CurriculumNotFoundError):
            repo.get_learning_objective("ifoa", "cs1", "2026", "CS1-A-T01-LO99")

    def test_find_learning_objective_global_search(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import CurriculumDefinition, SectionDefinition, TopicDefinition, LearningObjectiveDefinition

        repo = CurriculumRepository()
        lo = LearningObjectiveDefinition(
            id="CS1-A-T01-LO01", topic_id="CS1-A-T01", code="CS1-A.1.1",
            description="Define RVs", cognitive_level="understand", estimated_minutes=30, learning_type="concept"
        )
        topic = TopicDefinition(
            id="CS1-A-T01", section_id="CS1-A", code="CS1-A.1",
            title="Topic 1", description="d", estimated_minutes=90, difficulty="foundational",
            learning_objectives=[lo],
        )
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational",
            topics=[topic],
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        result_curriculum, result_section, result_topic, result_lo = repo.find_learning_objective("CS1-A-T01-LO01")
        assert result_curriculum.exam_code == "CS1"
        assert result_section.id == "CS1-A"
        assert result_topic.id == "CS1-A-T01"
        assert result_lo.id == "CS1-A-T01-LO01"
        assert result_lo.description == "Define RVs"

    def test_find_learning_objective_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError
        from app.curriculum.models import CurriculumDefinition, SectionDefinition

        repo = CurriculumRepository()
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational", topics=[]
        )
        c = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Test",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2026"] = c
        
        with pytest.raises(CurriculumNotFoundError):
            repo.find_learning_objective("CS1-A-T01-LO99")

    def test_v1_and_v2_coexist_in_cache(self):
        """Test that V1 and V2 curricula can coexist in the same repository."""
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.models import Curriculum, CurriculumDefinition, SectionDefinition

        repo = CurriculumRepository()
        
        # Add a V1 curriculum
        v1_curriculum = Curriculum(
            organisation="IFoA",
            examination="Actuarial Statistics",
            paper="CS1",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=10.0,
            topics=[],
        )
        repo._cache["ifoa/cs1/2026"] = v1_curriculum
        
        # Add a V2 curriculum
        section = SectionDefinition(
            id="CS1-A", code="CS1-A", title="Section A", description="d",
            exam_weight=100.0, estimated_hours=10.0, difficulty="foundational", topics=[]
        )
        v2_curriculum = CurriculumDefinition(
            exam_code="CS1",
            exam_name="Actuarial Statistics",
            provider="IFoA",
            version="2026",
            effective_date=date(2026, 1, 1),
            superseded_date=None,
            total_estimated_hours=10.0,
            description="d",
            sections=[section],
        )
        repo._cache["ifoa/cs1/2027"] = v2_curriculum
        
        # Both should be accessible
        assert repo.is_loaded("ifoa", "cs1", "2026")
        assert repo.is_loaded_v2("ifoa", "cs1", "2027")
        
        v1 = repo.get_curriculum("ifoa", "cs1", "2026")
        assert isinstance(v1, Curriculum)
        
        v2 = repo.get_curriculum_v2("ifoa", "cs1", "2027")
        assert isinstance(v2, CurriculumDefinition)