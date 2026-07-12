"""Unit tests for the Curriculum Intelligence Engine.

Covers:
    - Data models (Curriculum, Topic, LearningOutcome)
    - Exceptions (all CurriculumError subclasses)
    - JSON Schema (get_schema, validate_instance)
    - Loader (load_from_dict, load_from_json, discover_curricula)
    - Validator (validate_curriculum and individual rules)
    - Repository (CurriculumRepository caching, lookup, discovery)
    - Seed (seed_curricula)
"""

from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

import pytest


# ── helpers ──────────────────────────────────────────────────────────────────

def _valid_curriculum_dict() -> dict:
    """Return a minimal valid curriculum dict for use across loader/schema tests."""
    return {
        "organisation": "IFoA",
        "examination": "Actuarial Statistics",
        "paper": "CS1",
        "syllabus_version": "2026",
        "effective_from": "2026-01-01",
        "effective_to": None,
        "metadata": {"language": "en"},
        "topics": [
            {
                "id": "cs1-2026-1",
                "code": "CS1-A",
                "title": "Probability Basics",
                "description": "Core probability concepts.",
                "weighting": 40.0,
                "estimated_hours": 12.0,
                "difficulty": "foundational",
                "prerequisites": [],
                "learning_outcomes": [
                    {
                        "id": "lo-1",
                        "code": "CS1-A-1",
                        "description": "Define sample spaces and events.",
                        "suggested_revision_days": 7,
                    },
                    {
                        "id": "lo-2",
                        "code": "CS1-A-2",
                        "description": "Apply Bayes' theorem.",
                        "suggested_revision_days": 14,
                    },
                ],
            },
            {
                "id": "cs1-2026-2",
                "code": "CS1-B",
                "title": "Distributions",
                "description": "Common distributions.",
                "weighting": 60.0,
                "estimated_hours": 18.0,
                "difficulty": "intermediate",
                "prerequisites": ["cs1-2026-1"],
                "learning_outcomes": [
                    {
                        "id": "lo-3",
                        "code": "CS1-B-1",
                        "description": "Describe binomial distribution.",
                    },
                ],
            },
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════════════════════════

class TestLearningOutcome:
    """Tests for the LearningOutcome dataclass."""

    def test_create_minimal(self):
        from app.curriculum.models import LearningOutcome

        lo = LearningOutcome(id="x", code="X-1", description="desc")
        assert lo.id == "x"
        assert lo.code == "X-1"
        assert lo.description == "desc"
        assert lo.suggested_revision_days == 14

    def test_create_with_revision_days(self):
        from app.curriculum.models import LearningOutcome

        lo = LearningOutcome(
            id="x", code="X-1", description="desc", suggested_revision_days=21
        )
        assert lo.suggested_revision_days == 21

    def test_is_frozen(self):
        from app.curriculum.models import LearningOutcome

        lo = LearningOutcome(id="x", code="X-1", description="desc")
        with pytest.raises(Exception):
            lo.id = "y"  # type: ignore[misc]

    def test_equality(self):
        from app.curriculum.models import LearningOutcome

        a = LearningOutcome(id="x", code="X-1", description="desc")
        b = LearningOutcome(id="x", code="X-1", description="desc")
        c = LearningOutcome(id="y", code="Y-1", description="other")
        assert a == b
        assert a != c


class TestTopic:
    """Tests for the Topic dataclass."""

    def test_create_minimal(self):
        from app.curriculum.models import Topic

        t = Topic(id="t1", code="T1", title="Title", description="Desc")
        assert t.id == "t1"
        assert t.weighting == 0.0
        assert t.estimated_hours == 0.0
        assert t.difficulty == "intermediate"
        assert t.prerequisites == []
        assert t.learning_outcomes == []

    def test_create_with_learning_outcomes(self):
        from app.curriculum.models import LearningOutcome, Topic

        lo = LearningOutcome(id="lo1", code="L1", description="desc")
        t = Topic(
            id="t1",
            code="T1",
            title="Title",
            description="Desc",
            weighting=25.0,
            estimated_hours=10.0,
            difficulty="advanced",
            prerequisites=["t0"],
            learning_outcomes=[lo],
        )
        assert len(t.learning_outcomes) == 1
        assert t.difficulty == "advanced"
        assert t.prerequisites == ["t0"]

    def test_is_frozen(self):
        from app.curriculum.models import Topic

        t = Topic(id="t1", code="T1", title="Title", description="Desc")
        with pytest.raises(Exception):
            t.title = "New"  # type: ignore[misc]

    def test_hash_uses_id(self):
        from app.curriculum.models import Topic

        t1 = Topic(id="a", code="A", title="One", description="d")
        t2 = Topic(id="a", code="B", title="Two", description="d")
        t3 = Topic(id="b", code="A", title="One", description="d")
        assert hash(t1) == hash(t2)
        assert hash(t1) != hash(t3)

    def test_equality(self):
        from app.curriculum.models import Topic

        a = Topic(id="x", code="A", title="T", description="d")
        b = Topic(id="x", code="A", title="T", description="d")
        c = Topic(id="y", code="B", title="T", description="d")
        assert a == b
        assert a != c


class TestCurriculum:
    """Tests for the Curriculum dataclass."""

    def test_create(self):
        from app.curriculum.models import Curriculum, Topic

        t = Topic(id="t1", code="T1", title="One", description="d", weighting=100.0, estimated_hours=5.0)
        c = Curriculum(
            organisation="IFoA",
            examination="Actuarial Practice",
            paper="CS1",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=5.0,
            topics=[t],
            metadata={"lang": "en"},
        )
        assert c.organisation == "IFoA"
        assert c.paper == "CS1"
        assert c.effective_from == date(2026, 1, 1)
        assert c.effective_to is None
        assert c.metadata == {"lang": "en"}
        assert len(c.topics) == 1

    def test_exam_key(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="IFoA",
            examination="Actuarial Practice",
            paper="CS1",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=0.0,
        )
        assert c.exam_key == "ifoa/cs1"

    def test_version_key(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="IFoA",
            examination="Actuarial Practice",
            paper="CM2",
            syllabus_version="2025",
            effective_from=date(2025, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=0.0,
        )
        assert c.version_key == "ifoa/cm2/2025"

    def test_exam_key_capitalisation(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="IFoA",
            examination="X",
            paper="Cs1",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=0.0,
        )
        assert c.exam_key == "ifoa/cs1"

    def test_is_frozen(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="IFoA",
            examination="X",
            paper="CS1",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=100.0,
            estimated_total_hours=0.0,
        )
        with pytest.raises(Exception):
            c.paper = "CM1"  # type: ignore[misc]

    def test_defaults(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="A",
            examination="B",
            paper="C",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=None,
            total_weight=0.0,
            estimated_total_hours=0.0,
        )
        assert c.topics == []
        assert c.metadata == {}

    def test_effective_to_set(self):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="A",
            examination="B",
            paper="C",
            syllabus_version="2026",
            effective_from=date(2026, 1, 1),
            effective_to=date(2028, 12, 31),
            total_weight=100.0,
            estimated_total_hours=0.0,
        )
        assert c.effective_to == date(2028, 12, 31)


# ═══════════════════════════════════════════════════════════════════════════════
# Exceptions
# ═══════════════════════════════════════════════════════════════════════════════

class TestCurriculumError:
    """Tests for the base CurriculumError."""

    def test_is_exception(self):
        from app.curriculum.exceptions import CurriculumError

        assert issubclass(CurriculumError, Exception)

    def test_raise_and_catch(self):
        from app.curriculum.exceptions import CurriculumError

        with pytest.raises(CurriculumError):
            raise CurriculumError("something went wrong")


class TestCurriculumNotFoundError:
    """Tests for CurriculumNotFoundError."""

    def test_with_version(self):
        from app.curriculum.exceptions import CurriculumNotFoundError

        err = CurriculumNotFoundError("ifoa/cs1", "2025")
        assert "2025" in str(err)
        assert err.exam_key == "ifoa/cs1"
        assert err.version == "2025"

    def test_without_version(self):
        from app.curriculum.exceptions import CurriculumNotFoundError

        err = CurriculumNotFoundError("ifoa/cm1")
        assert "ifoa/cm1" in str(err)
        assert err.exam_key == "ifoa/cm1"
        assert err.version is None

    def test_is_curriculum_error(self):
        from app.curriculum.exceptions import CurriculumError, CurriculumNotFoundError

        assert issubclass(CurriculumNotFoundError, CurriculumError)


class TestCurriculumLoadError:
    """Tests for CurriculumLoadError."""

    def test_message_includes_path_and_reason(self):
        from app.curriculum.exceptions import CurriculumLoadError

        err = CurriculumLoadError("data/x.json", "Invalid JSON")
        assert "data/x.json" in str(err)
        assert "Invalid JSON" in str(err)
        assert err.path == "data/x.json"
        assert err.reason == "Invalid JSON"


class TestCurriculumValidationError:
    """Tests for CurriculumValidationError."""

    def test_single_message(self):
        from app.curriculum.exceptions import CurriculumValidationError

        err = CurriculumValidationError(["Missing field"])
        assert "Missing field" in str(err)
        assert err.messages == ["Missing field"]

    def test_multiple_messages(self):
        from app.curriculum.exceptions import CurriculumValidationError

        err = CurriculumValidationError(["Error A", "Error B"])
        assert "Error A" in str(err)
        assert "Error B" in str(err)
        assert len(err.messages) == 2

    def test_is_curriculum_error(self):
        from app.curriculum.exceptions import CurriculumError, CurriculumValidationError

        assert issubclass(CurriculumValidationError, CurriculumError)


class TestDuplicateTopicCodeError:
    """Tests for DuplicateTopicCodeError."""

    def test_message(self):
        from app.curriculum.exceptions import DuplicateTopicCodeError

        err = DuplicateTopicCodeError("CS1-A")
        assert "Duplicate topic code" in str(err)
        assert "CS1-A" in str(err)
        assert err.code == "CS1-A"


class TestDuplicateLearningOutcomeCodeError:
    """Tests for DuplicateLearningOutcomeCodeError."""

    def test_message(self):
        from app.curriculum.exceptions import DuplicateLearningOutcomeCodeError

        err = DuplicateLearningOutcomeCodeError("LO-X")
        assert "Duplicate learning outcome code" in str(err)
        assert "LO-X" in str(err)
        assert err.code == "LO-X"


class TestInvalidWeightingError:
    """Tests for InvalidWeightingError."""

    def test_message(self):
        from app.curriculum.exceptions import InvalidWeightingError

        err = InvalidWeightingError(150.0)
        assert "150.0" in str(err)
        assert err.total == 150.0


class TestInvalidPrerequisiteError:
    """Tests for InvalidPrerequisiteError."""

    def test_message(self):
        from app.curriculum.exceptions import InvalidPrerequisiteError

        err = InvalidPrerequisiteError("t1", "t99")
        assert "t1" in str(err)
        assert "t99" in str(err)
        assert err.topic_id == "t1"
        assert err.prerequisite == "t99"


# ═══════════════════════════════════════════════════════════════════════════════
# JSON Schema
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetSchema:
    """Tests for get_schema()."""

    def test_returns_dict(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        assert isinstance(schema, dict)

    def test_has_required_keys(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        assert "$schema" in schema
        assert "type" in schema
        assert schema["type"] == "object"
        assert "required" in schema
        required = schema["required"]
        assert "organisation" in required
        assert "examination" in required
        assert "paper" in required
        assert "syllabus_version" in required
        assert "effective_from" in required
        assert "topics" in required

    def test_syllabus_version_pattern(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        sv = schema["properties"]["syllabus_version"]
        assert sv["pattern"] == r"^\d{4}$"

    def test_topics_min_items(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        assert schema["properties"]["topics"]["minItems"] == 1

    def test_difficulty_enum(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        diff = schema["properties"]["topics"]["items"]["properties"]["difficulty"]
        assert diff["enum"] == ["foundational", "intermediate", "advanced"]

    def test_learning_outcomes_min_items(self):
        from app.curriculum.schemas import get_schema

        schema = get_schema()
        lo = schema["properties"]["topics"]["items"]["properties"]["learning_outcomes"]
        assert lo["minItems"] == 1


class TestValidateInstance:
    """Tests for validate_instance()."""

    def test_valid_instance_passes(self):
        from app.curriculum.schemas import validate_instance

        errors = validate_instance(_valid_curriculum_dict())
        assert errors == []

    def test_missing_required_field(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        del data["organisation"]
        errors = validate_instance(data)
        assert any("organisation" in e for e in errors)

    def test_multiple_missing_fields(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        del data["organisation"]
        del data["paper"]
        errors = validate_instance(data)
        # Should report first missing field and short-circuit
        assert len(errors) >= 1

    def test_invalid_syllabus_version_not_digits(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["syllabus_version"] = "abc"
        errors = validate_instance(data)
        assert any("syllabus_version" in e for e in errors)

    def test_syllabus_version_wrong_length(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["syllabus_version"] = "202"
        errors = validate_instance(data)
        assert any("syllabus_version" in e for e in errors)

    def test_empty_topics_array(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"] = []
        errors = validate_instance(data)
        assert any("topics" in e for e in errors)

    def test_topic_missing_required_field(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        del data["topics"][0]["id"]
        errors = validate_instance(data)
        assert any("id" in e for e in errors)

    def test_duplicate_topic_id(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][1]["id"] = data["topics"][0]["id"]
        errors = validate_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_duplicate_lo_code(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][1]["learning_outcomes"][0]["code"] = "CS1-A-1"
        errors = validate_instance(data)
        assert any("duplicate" in e.lower() for e in errors)

    def test_weighting_out_of_range(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0]["weighting"] = 150.0
        errors = validate_instance(data)
        assert any("weighting" in e for e in errors)

    def test_negative_estimated_hours(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0]["estimated_hours"] = -5.0
        errors = validate_instance(data)
        assert any("estimated_hours" in e for e in errors)

    def test_invalid_difficulty_value(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0]["difficulty"] = "expert"
        errors = validate_instance(data)
        assert any("difficulty" in e for e in errors)

    def test_missing_learning_outcome_required_field(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        del data["topics"][0]["learning_outcomes"][0]["code"]
        errors = validate_instance(data)
        assert any("code" in e for e in errors)

    def test_empty_learning_outcomes(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0]["learning_outcomes"] = []
        errors = validate_instance(data)
        assert any("learning_outcomes" in e for e in errors)

    def test_topic_not_a_dict(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0] = "not-a-dict"  # type: ignore[assignment]
        errors = validate_instance(data)
        assert any("object" in e for e in errors)

    def test_lo_not_a_dict(self):
        from app.curriculum.schemas import validate_instance

        data = _valid_curriculum_dict()
        data["topics"][0]["learning_outcomes"][0] = "bad"  # type: ignore[assignment]
        errors = validate_instance(data)
        assert any("object" in e for e in errors)


# ═══════════════════════════════════════════════════════════════════════════════
# Loader
# ═══════════════════════════════════════════════════════════════════════════════

class TestLoadFromDict:
    """Tests for load_from_dict()."""

    def test_builds_valid_curriculum(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_curriculum_dict())
        assert c.organisation == "IFoA"
        assert c.paper == "CS1"
        assert c.syllabus_version == "2026"
        assert len(c.topics) == 2
        assert c.total_weight == 100.0
        assert c.estimated_total_hours == 30.0

    def test_schema_validation_rejects_invalid(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.exceptions import CurriculumLoadError

        data = _valid_curriculum_dict()
        del data["organisation"]
        with pytest.raises(CurriculumLoadError):
            load_from_dict(data)

    def test_learning_outcomes_are_built(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_curriculum_dict())
        topic = c.topics[0]
        assert len(topic.learning_outcomes) == 2
        lo = topic.learning_outcomes[0]
        assert lo.code == "CS1-A-1"
        assert lo.suggested_revision_days == 7

    def test_learning_outcome_default_revision_days(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_curriculum_dict())
        lo = c.topics[1].learning_outcomes[0]
        assert lo.suggested_revision_days == 14  # default

    def test_prerequisites_are_built(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_curriculum_dict())
        assert c.topics[1].prerequisites == ["cs1-2026-1"]

    def test_metadata_present(self):
        from app.curriculum.loader import load_from_dict

        c = load_from_dict(_valid_curriculum_dict())
        assert c.metadata == {"language": "en"}

    def test_metadata_default_when_missing(self):
        from app.curriculum.loader import load_from_dict

        data = _valid_curriculum_dict()
        del data["metadata"]
        c = load_from_dict(data)
        assert c.metadata == {}

    def test_effective_to_default(self):
        from app.curriculum.loader import load_from_dict

        data = _valid_curriculum_dict()
        del data["effective_to"]
        c = load_from_dict(data)
        assert c.effective_to == date(2099, 12, 31)

    def test_difficulty_default(self):
        """Schema now requires difficulty; removing it should fail schema validation."""
        from app.curriculum.loader import load_from_dict
        from app.curriculum.exceptions import CurriculumLoadError

        data = _valid_curriculum_dict()
        del data["topics"][0]["difficulty"]
        with pytest.raises(CurriculumLoadError, match="difficulty"):
            load_from_dict(data)


class TestParseDate:
    """Tests for _parse_date helper."""

    def test_none_returns_sentinel(self):
        from app.curriculum.loader import _parse_date

        assert _parse_date(None) == date(2099, 12, 31)

    def test_iso_string(self):
        from app.curriculum.loader import _parse_date

        assert _parse_date("2026-06-15") == date(2026, 6, 15)

    def test_date_object(self):
        from app.curriculum.loader import _parse_date
        import datetime

        d = date(2025, 1, 1)
        assert _parse_date(d) == d

    def test_datetime_object(self):
        from app.curriculum.loader import _parse_date
        import datetime

        dt = datetime.datetime(2025, 6, 15, 12, 30)
        assert _parse_date(dt) == date(2025, 6, 15)

    def test_unexpected_type_raises(self):
        from app.curriculum.loader import _parse_date
        from app.curriculum.exceptions import CurriculumLoadError

        with pytest.raises(CurriculumLoadError):
            _parse_date(42)


class TestLoadFromJson:
    """Tests for load_from_json()."""

    def test_loads_valid_file(self):
        from app.curriculum.loader import load_from_json
        import json as _json

        data = _valid_curriculum_dict()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            _json.dump(data, f)
            tmp_path = f.name

        try:
            c = load_from_json(tmp_path)
            assert c.paper == "CS1"
            assert len(c.topics) == 2
        finally:
            Path(tmp_path).unlink()

    def test_file_not_found(self):
        from app.curriculum.loader import load_from_json
        from app.curriculum.exceptions import CurriculumLoadError

        with pytest.raises(CurriculumLoadError):
            load_from_json("/nonexistent/path/curriculum.json")

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
                load_from_json(tmp_path)
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
                load_from_json(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_accepts_path_or_string(self):
        from app.curriculum.loader import load_from_json

        data = _valid_curriculum_dict()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp_path = f.name

        try:
            c1 = load_from_json(Path(tmp_path))
            c2 = load_from_json(tmp_path)
            assert c1.paper == c2.paper
        finally:
            Path(tmp_path).unlink()


class TestLoadCurriculum:
    """Tests for load_curriculum() / load_curriculum_v2()."""

    def test_loads_bundled_cs1_2026(self):
        from app.curriculum.loader import load_curriculum_v2

        c = load_curriculum_v2("ifoa", "cs1", "2026")
        assert c.provider == "IFoA"
        assert c.exam_code == "CS1"
        assert c.version == "2026"
        assert len(c.sections) == 5
        assert sum(len(section.topics) for section in c.sections) == 14

    def test_case_insensitive_organisation(self):
        from app.curriculum.loader import load_curriculum_v2

        c = load_curriculum_v2("IFOA", "cs1", "2026")
        assert c.provider == "IFoA"

    def test_case_insensitive_paper(self):
        from app.curriculum.loader import load_curriculum_v2

        c = load_curriculum_v2("ifoa", "CS1", "2026")
        assert c.exam_code == "CS1"

    def test_unknown_curriculum_raises(self):
        from app.curriculum.loader import load_curriculum
        from app.curriculum.exceptions import CurriculumLoadError

        with pytest.raises(CurriculumLoadError):
            load_curriculum("unknown", "xyz", "2099")


class TestDiscoverCurricula:
    """Tests for discover_curricula()."""

    def test_finds_bundled_curricula(self):
        from app.curriculum.loader import discover_curricula

        result = discover_curricula()
        assert len(result) >= 1
        orgs = {org for org, _, _ in result}
        assert "IFOA" in orgs

    def test_each_entry_has_versions(self):
        from app.curriculum.loader import discover_curricula

        for org, paper, versions in discover_curricula():
            assert isinstance(org, str)
            assert isinstance(paper, str)
            assert isinstance(versions, list)
            assert len(versions) >= 1
            for v in versions:
                assert isinstance(v, str)


# ═══════════════════════════════════════════════════════════════════════════════
# Validator
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidateCurriculum:
    """Tests for validate_curriculum()."""

    def _curriculum(self, **overrides):
        from app.curriculum.models import Curriculum, LearningOutcome, Topic

        lo = LearningOutcome(id="lo1", code="LO-1", description="d", suggested_revision_days=7)
        t = Topic(
            id="t1", code="T1", title="Topic", description="d",
            weighting=100.0, estimated_hours=10.0, difficulty="foundational",
            learning_outcomes=[lo],
        )
        c = Curriculum(
            organisation="X", examination="Y", paper="Z",
            syllabus_version="2026", effective_from=date(2026, 1, 1),
            effective_to=None, total_weight=100.0, estimated_total_hours=10.0,
            topics=[t],
        )
        # Apply overrides via replace
        for k, v in overrides.items():
            object.__setattr__(c, k, v)
        return c

    def test_valid_passes(self):
        from app.curriculum.validator import validate_curriculum

        c = self._curriculum()
        validate_curriculum(c)  # should not raise

    def test_duplicate_topic_id_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t1 = Topic(id="dup", code="A", title="One", description="d", weighting=50.0, estimated_hours=5.0, difficulty="foundational", learning_outcomes=[lo])
        t2 = Topic(id="dup", code="B", title="Two", description="d", weighting=50.0, estimated_hours=5.0, difficulty="intermediate", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t1, t2])
        object.__setattr__(c, "total_weight", 100.0)
        object.__setattr__(c, "estimated_total_hours", 10.0)

        with pytest.raises(CurriculumValidationError, match="Duplicate topic id"):
            validate_curriculum(c)

    def test_duplicate_topic_code_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t1 = Topic(id="a", code="DUP", title="One", description="d", weighting=50.0, estimated_hours=5.0, difficulty="foundational", learning_outcomes=[lo])
        t2 = Topic(id="b", code="DUP", title="Two", description="d", weighting=50.0, estimated_hours=5.0, difficulty="intermediate", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t1, t2])
        object.__setattr__(c, "total_weight", 100.0)
        object.__setattr__(c, "estimated_total_hours", 10.0)

        with pytest.raises(CurriculumValidationError, match="Duplicate topic code"):
            validate_curriculum(c)

    def test_duplicate_lo_code_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo1 = LearningOutcome(id="a", code="DUP", description="d", suggested_revision_days=7)
        lo2 = LearningOutcome(id="b", code="DUP", description="d", suggested_revision_days=7)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=100.0, estimated_hours=5.0, difficulty="foundational", learning_outcomes=[lo1, lo2])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])
        object.__setattr__(c, "total_weight", 100.0)
        object.__setattr__(c, "estimated_total_hours", 5.0)

        with pytest.raises(CurriculumValidationError, match="Duplicate learning outcome code"):
            validate_curriculum(c)

    def test_weighting_out_of_range_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=50.0, estimated_hours=5.0, difficulty="foundational", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])
        object.__setattr__(c, "total_weight", 50.0)
        object.__setattr__(c, "estimated_total_hours", 5.0)

        with pytest.raises(CurriculumValidationError, match="weighting"):
            validate_curriculum(c)

    def test_non_positive_estimated_hours_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=100.0, estimated_hours=0.0, difficulty="foundational", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])

        with pytest.raises(CurriculumValidationError, match="estimated_hours"):
            validate_curriculum(c)

    def test_invalid_prerequisite_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=100.0, estimated_hours=5.0, difficulty="foundational", prerequisites=["nonexistent"], learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])

        with pytest.raises(CurriculumValidationError, match="prerequisite"):
            validate_curriculum(c)

    def test_invalid_difficulty_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=7)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=100.0, estimated_hours=5.0, difficulty="expert", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])

        with pytest.raises(CurriculumValidationError, match="difficulty"):
            validate_curriculum(c)

    def test_non_positive_revision_days_raises(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=0)
        t = Topic(id="t1", code="T1", title="T", description="d", weighting=100.0, estimated_hours=5.0, difficulty="foundational", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t])

        with pytest.raises(CurriculumValidationError, match="suggested_revision_days"):
            validate_curriculum(c)

    def test_aggregates_multiple_errors(self):
        from app.curriculum.validator import validate_curriculum
        from app.curriculum.exceptions import CurriculumValidationError
        from app.curriculum.models import Topic, LearningOutcome

        lo = LearningOutcome(id="x", code="LO", description="d", suggested_revision_days=0)
        t1 = Topic(id="dup", code="A", title="One", description="d", weighting=30.0, estimated_hours=0.0, difficulty="bad", learning_outcomes=[lo])
        t2 = Topic(id="dup", code="A", title="Two", description="d", weighting=30.0, estimated_hours=0.0, difficulty="bad", learning_outcomes=[lo])
        c = self._curriculum()
        object.__setattr__(c, "topics", [t1, t2])
        object.__setattr__(c, "total_weight", 60.0)
        object.__setattr__(c, "estimated_total_hours", 0.0)

        with pytest.raises(CurriculumValidationError) as exc_info:
            validate_curriculum(c)
        assert len(exc_info.value.messages) >= 3  # multiple issues found

    def test_bundled_cs1_passes_validation(self):
        from app.curriculum.loader import load_curriculum_v2
        from app.curriculum.validator import validate_curriculum_v2

        c = load_curriculum_v2("ifoa", "cs1", "2026")
        validate_curriculum_v2(c)  # should not raise


class TestIndividualValidators:
    """Tests for the specialised validator functions."""

    def _curriculum_with_topics(self, topics):
        from app.curriculum.models import Curriculum

        c = Curriculum(
            organisation="X", examination="Y", paper="Z",
            syllabus_version="2026", effective_from=date(2026, 1, 1),
            effective_to=None, total_weight=sum(t.weighting for t in topics),
            estimated_total_hours=sum(t.estimated_hours for t in topics),
            topics=topics,
        )
        return c

    def test_validate_duplicate_topic_codes_passes(self):
        from app.curriculum.validator import validate_duplicate_topic_codes
        from app.curriculum.models import Topic

        t1 = Topic(id="a", code="A", title="One", description="d")
        t2 = Topic(id="b", code="B", title="Two", description="d")
        c = self._curriculum_with_topics([t1, t2])
        validate_duplicate_topic_codes(c)  # should not raise

    def test_validate_duplicate_topic_codes_raises(self):
        from app.curriculum.validator import validate_duplicate_topic_codes
        from app.curriculum.exceptions import DuplicateTopicCodeError
        from app.curriculum.models import Topic

        t1 = Topic(id="a", code="X", title="One", description="d")
        t2 = Topic(id="b", code="X", title="Two", description="d")
        c = self._curriculum_with_topics([t1, t2])
        with pytest.raises(DuplicateTopicCodeError):
            validate_duplicate_topic_codes(c)

    def test_validate_duplicate_lo_codes_passes(self):
        from app.curriculum.validator import validate_duplicate_lo_codes
        from app.curriculum.models import LearningOutcome, Topic

        lo1 = LearningOutcome(id="a", code="A", description="d")
        lo2 = LearningOutcome(id="b", code="B", description="d")
        t = Topic(id="t", code="T", title="T", description="d", learning_outcomes=[lo1, lo2])
        c = self._curriculum_with_topics([t])
        validate_duplicate_lo_codes(c)  # should not raise

    def test_validate_duplicate_lo_codes_raises(self):
        from app.curriculum.validator import validate_duplicate_lo_codes
        from app.curriculum.exceptions import DuplicateLearningOutcomeCodeError
        from app.curriculum.models import LearningOutcome, Topic

        lo1 = LearningOutcome(id="a", code="X", description="d")
        lo2 = LearningOutcome(id="b", code="X", description="d")
        t = Topic(id="t", code="T", title="T", description="d", learning_outcomes=[lo1, lo2])
        c = self._curriculum_with_topics([t])
        with pytest.raises(DuplicateLearningOutcomeCodeError):
            validate_duplicate_lo_codes(c)

    def test_validate_weightings_passes(self):
        from app.curriculum.validator import validate_weightings
        from app.curriculum.models import Topic

        t = Topic(id="t", code="T", title="T", description="d", weighting=100.0)
        c = self._curriculum_with_topics([t])
        validate_weightings(c)  # should not raise

    def test_validate_weightings_raises(self):
        from app.curriculum.validator import validate_weightings
        from app.curriculum.exceptions import InvalidWeightingError
        from app.curriculum.models import Topic

        t = Topic(id="t", code="T", title="T", description="d", weighting=10.0)
        c = self._curriculum_with_topics([t])
        with pytest.raises(InvalidWeightingError):
            validate_weightings(c)

    def test_validate_weightings_within_tolerance(self):
        from app.curriculum.validator import validate_weightings
        from app.curriculum.models import Topic

        t1 = Topic(id="a", code="A", title="A", description="d", weighting=52.0)
        t2 = Topic(id="b", code="B", title="B", description="d", weighting=51.0)
        c = self._curriculum_with_topics([t1, t2])
        validate_weightings(c)  # 103 is within tolerance of 5

    def test_validate_prerequisites_passes(self):
        from app.curriculum.validator import validate_prerequisites
        from app.curriculum.models import Topic

        t1 = Topic(id="a", code="A", title="A", description="d")
        t2 = Topic(id="b", code="B", title="B", description="d", prerequisites=["a"])
        c = self._curriculum_with_topics([t1, t2])
        validate_prerequisites(c)  # should not raise

    def test_validate_prerequisites_raises(self):
        from app.curriculum.validator import validate_prerequisites
        from app.curriculum.exceptions import InvalidPrerequisiteError
        from app.curriculum.models import Topic

        t = Topic(id="a", code="A", title="A", description="d", prerequisites=["ghost"])
        c = self._curriculum_with_topics([t])
        with pytest.raises(InvalidPrerequisiteError):
            validate_prerequisites(c)


# ═══════════════════════════════════════════════════════════════════════════════
# Repository
# ═══════════════════════════════════════════════════════════════════════════════

class TestCurriculumRepository:
    """Tests for CurriculumRepository."""

    def test_init_empty(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        assert repo._cache == {}

    def test_cache_key(self):
        from app.curriculum.repository import CurriculumRepository

        key = CurriculumRepository._cache_key("IFoA", "CS1", "2026")
        assert key == "ifoa/cs1/2026"

    def test_load_caches(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        c = repo.load_auto("ifoa", "cs1", "2026")
        assert repo.is_loaded("ifoa", "cs1", "2026")
        # Second load returns cached
        c2 = repo.load_auto("ifoa", "cs1", "2026")
        assert c is c2

    def test_load_invalid_curriculum_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumLoadError

        repo = CurriculumRepository()
        with pytest.raises(CurriculumLoadError):
            repo.load_auto("no-such-org", "no-such-paper", "2099")

    def test_exists_true(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        assert repo.exists("ifoa", "cs1", "2026") is True

    def test_exists_false(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        assert repo.exists("nonexistent", "xyz", "2099") is False

    def test_get_curriculum_loaded(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        c = repo.get_curriculum_v2("ifoa", "cs1", "2026")
        assert c.exam_code == "CS1"

    def test_get_curriculum_not_loaded_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError

        repo = CurriculumRepository()
        with pytest.raises(CurriculumNotFoundError, match="not found"):
            repo.get_curriculum_v2("ifoa", "cs1", "2026")

    def test_get_topics(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        topics = repo.get_topics_v2("ifoa", "cs1", "2026", "CS1-A")
        assert len(topics) == 2
        assert topics[0].code == "1.1"

    def test_get_topic_found(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        t = repo.get_topic_v2("ifoa", "cs1", "2026", "CS1-B-T01")
        assert t.code == "2.1"
        assert "univariate distributions" in t.title.lower()

    def test_get_topic_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        with pytest.raises(CurriculumNotFoundError):
            repo.get_topic_v2("ifoa", "cs1", "2026", "nonexistent-topic")

    def test_get_learning_outcome_found(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        lo = repo.get_learning_objective("ifoa", "cs1", "2026", "CS1-A-T01-LO01")
        assert lo.code == "1.1.1"

    def test_get_learning_outcome_not_found_raises(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.exceptions import CurriculumNotFoundError

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        with pytest.raises(CurriculumNotFoundError):
            repo.get_learning_objective("ifoa", "cs1", "2026", "nonexistent-lo")

    def test_list_exams(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        exams = repo.list_exams()
        assert len(exams) >= 1
        # Check structure
        for org, paper, versions in exams:
            assert isinstance(org, str)
            assert isinstance(paper, str)
            assert isinstance(versions, list)
            assert len(versions) >= 1

    def test_list_versions_found(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        versions = repo.list_versions("ifoa", "cs1")
        assert "2026" in versions

    def test_list_versions_not_found(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        versions = repo.list_versions("unknown", "paper")
        assert versions == []

    def test_clear(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        assert repo.is_loaded("ifoa", "cs1", "2026")
        repo.clear()
        assert not repo.is_loaded("ifoa", "cs1", "2026")
        assert repo._cache == {}

    def test_is_loaded_false_initially(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        assert not repo.is_loaded("ifoa", "cs1", "2026")

    def test_is_loaded_true_after_load(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        assert repo.is_loaded("ifoa", "cs1", "2026")

    def test_case_insensitive_lookup(self):
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        repo.load_auto("ifoa", "cs1", "2026")
        # Look up with different case
        assert repo.is_loaded("IFOA", "CS1", "2026")
        c = repo.get_curriculum_v2("IfOa", "Cs1", "2026")
        assert c.exam_code == "CS1"


# ═══════════════════════════════════════════════════════════════════════════════
# Seed
# ═══════════════════════════════════════════════════════════════════════════════

class TestSeedCurricula:
    """Tests for seed_curricula()."""

    def test_seeds_into_new_repo_when_none_given(self):
        from app.curriculum.seed import seed_curricula

        repo = seed_curricula()
        assert repo.is_loaded("ifoa", "cs1", "2026")
        c = repo.get_curriculum_v2("ifoa", "cs1", "2026")
        assert c.exam_code == "CS1"

    def test_seeds_into_provided_repo(self):
        from app.curriculum.repository import CurriculumRepository
        from app.curriculum.seed import seed_curricula

        repo = CurriculumRepository()
        result = seed_curricula(repo)
        assert result is repo
        assert repo.is_loaded("ifoa", "cs1", "2026")

    def test_seed_is_idempotent(self):
        from app.curriculum.seed import seed_curricula

        repo = seed_curricula()
        c1 = repo.get_curriculum_v2("ifoa", "cs1", "2026")
        # Seed again into same repo
        seed_curricula(repo)
        c2 = repo.get_curriculum_v2("ifoa", "cs1", "2026")
        assert c1 is c2  # Same cached object
