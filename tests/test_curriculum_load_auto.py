"""Tests for the canonical curriculum loader (load_auto) and backfill command.

Covers:
    - CurriculumRepository.load_auto() — V1, V2, auto-detection, caching
    - CurriculumEngineService.load_auto() — public wrapper
    - CurriculumEngineService.get_topics_flat() — V1 and V2 flattening
    - CurriculumService._load_curriculum_auto() — thin delegate
    - StudyPlanService._load_engine_curriculum_auto() — tuple return
    - StudyPlanService._get_engine_topics_ordered() — delegate
    - flask backfill-sections command — idempotency, duplicate protection
    - Traversal consistency between engine and DB sides
"""

from __future__ import annotations

import json

import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers — minimal in-memory curriculum dicts
# ═══════════════════════════════════════════════════════════════════════════════

def _v1_dict() -> dict:
    return {
        "organisation": "TestOrg",
        "examination": "Test Exam",
        "paper": "TE1",
        "syllabus_version": "2026",
        "effective_from": "2026-01-01",
        "effective_to": None,
        "metadata": {},
        "topics": [
            {
                "id": "te1-2026-1",
                "code": "TE1-A",
                "title": "Topic Alpha",
                "description": "First topic.",
                "weighting": 60.0,
                "estimated_hours": 10.0,
                "difficulty": "foundational",
                "prerequisites": [],
                "learning_outcomes": [
                    {
                        "id": "te1-2026-1-1",
                        "code": "TE1-A-1",
                        "description": "Understand alpha.",
                        "suggested_revision_days": 7,
                    }
                ],
            },
            {
                "id": "te1-2026-2",
                "code": "TE1-B",
                "title": "Topic Beta",
                "description": "Second topic.",
                "weighting": 40.0,
                "estimated_hours": 8.0,
                "difficulty": "intermediate",
                "prerequisites": ["te1-2026-1"],
                "learning_outcomes": [
                    {
                        "id": "te1-2026-2-1",
                        "code": "TE1-B-1",
                        "description": "Understand beta.",
                        "suggested_revision_days": 7,
                    }
                ],
            },
        ],
    }


def _v2_dict() -> dict:
    return {
        "exam_code": "TE2",
        "exam_name": "Test Exam V2",
        "provider": "TestOrg",
        "version": "2026",
        "effective_date": "2026-01-01",
        "superseded_date": None,
        "total_estimated_hours": 20.0,
        "description": "A test V2 curriculum.",
        "sections": [
            {
                "id": "TE2-A",
                "code": "TE2-S1",
                "title": "Section One",
                "description": "First section.",
                "exam_weight": 60.0,
                "estimated_hours": 12.0,
                "difficulty": "foundational",
                "display_order": 1,
                "topics": [
                    {
                        "id": "TE2-A-T01",
                        "section_id": "TE2-A",
                        "code": "TE2-S1.1",
                        "title": "Topic One Alpha",
                        "description": "First topic of first section.",
                        "estimated_minutes": 120,
                        "difficulty": "foundational",
                        "display_order": 1,
                        "learning_objectives": [
                            {
                                "id": "TE2-A-T01-LO01",
                                "topic_id": "TE2-A-T01",
                                "code": "TE2-S1.1.a",
                                "description": "Understand alpha.",
                                "cognitive_level": "understand",
                                "estimated_minutes": 30,
                                "learning_type": "concept",
                                "display_order": 1,
                            }
                        ],
                    },
                    {
                        "id": "TE2-A-T02",
                        "section_id": "TE2-A",
                        "code": "TE2-S1.2",
                        "title": "Topic One Beta",
                        "description": "Second topic of first section.",
                        "estimated_minutes": 90,
                        "difficulty": "intermediate",
                        "display_order": 2,
                        "learning_objectives": [
                            {
                                "id": "TE2-A-T02-LO01",
                                "topic_id": "TE2-A-T02",
                                "code": "TE2-S1.2.a",
                                "description": "Understand beta.",
                                "cognitive_level": "understand",
                                "estimated_minutes": 20,
                                "learning_type": "concept",
                                "display_order": 1,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "TE2-B",
                "code": "TE2-S2",
                "title": "Section Two",
                "description": "Second section.",
                "exam_weight": 40.0,
                "estimated_hours": 8.0,
                "difficulty": "advanced",
                "display_order": 2,
                "topics": [
                    {
                        "id": "TE2-B-T01",
                        "section_id": "TE2-B",
                        "code": "TE2-S2.1",
                        "title": "Topic Two Alpha",
                        "description": "First topic of second section.",
                        "estimated_minutes": 60,
                        "difficulty": "advanced",
                        "display_order": 1,
                        "learning_objectives": [
                            {
                                "id": "TE2-B-T01-LO01",
                                "topic_id": "TE2-B-T01",
                                "code": "TE2-S2.1.a",
                                "description": "Apply gamma.",
                                "cognitive_level": "apply",
                                "estimated_minutes": 15,
                                "learning_type": "procedure",
                                "display_order": 1,
                            }
                        ],
                    }
                ],
            },
        ],
        "metadata": {},
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures — on-disk temp JSON files
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def tmp_v1_file(tmp_path):
    """Write a minimal V1 curriculum to a temp file and return the Path."""
    p = tmp_path / "te1" / "2026.json"
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(_v1_dict()), encoding="utf-8")
    return p


@pytest.fixture
def tmp_v2_file(tmp_path):
    """Write a minimal V2 curriculum to a temp file and return the Path."""
    p = tmp_path / "te2" / "2026.json"
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(_v2_dict()), encoding="utf-8")
    return p


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumRepository.load_auto — V1 loading
# ═══════════════════════════════════════════════════════════════════════════════

class TestRepositoryLoadAutoV1:
    def test_returns_curriculum_for_v1(self, tmp_v1_file):
        from app.curriculum.loader import load_from_json
        from app.curriculum.models import Curriculum
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        # Manually prime the cache via load_from_json
        v1 = load_from_json(tmp_v1_file)
        from app.curriculum.validator import validate_curriculum
        validate_curriculum(v1)
        repo._cache["testorg/te1/2026"] = v1

        result = repo.load_auto("testorg", "te1", "2026")
        assert isinstance(result, Curriculum)
        assert result.organisation == "TestOrg"
        assert len(result.topics) == 2

    def test_v1_is_not_curriculum_definition(self, tmp_v1_file):
        from app.curriculum.loader import load_from_json
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        v1 = load_from_json(tmp_v1_file)
        repo._cache["testorg/te1/2026"] = v1

        result = repo.load_auto("testorg", "te1", "2026")
        assert not isinstance(result, CurriculumDefinition)


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumRepository.load_auto — V2 loading
# ═══════════════════════════════════════════════════════════════════════════════

class TestRepositoryLoadAutoV2:
    def test_returns_curriculum_definition_for_v2(self, tmp_v2_file):
        from app.curriculum.loader import load_from_json
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        v2 = load_from_json(tmp_v2_file)
        from app.curriculum.validator import validate_curriculum_v2
        validate_curriculum_v2(v2)
        repo._cache["testorg/te2/2026"] = v2

        result = repo.load_auto("testorg", "te2", "2026")
        assert isinstance(result, CurriculumDefinition)
        assert result.exam_name == "Test Exam V2"
        assert len(result.sections) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumRepository.load_auto — auto-detection from dict
# ═══════════════════════════════════════════════════════════════════════════════

class TestLoadFromDictAutoDetect:
    def test_detects_v1_format(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import Curriculum

        result = load_from_dict(_v1_dict())
        assert isinstance(result, Curriculum)

    def test_detects_v2_format(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition

        result = load_from_dict(_v2_dict())
        assert isinstance(result, CurriculumDefinition)

    def test_v1_topic_count(self):
        from app.curriculum.loader import load_from_dict

        result = load_from_dict(_v1_dict())
        assert len(result.topics) == 2

    def test_v2_section_count(self):
        from app.curriculum.loader import load_from_dict

        result = load_from_dict(_v2_dict())
        assert len(result.sections) == 2

    def test_v2_topics_in_sections(self):
        from app.curriculum.loader import load_from_dict

        result = load_from_dict(_v2_dict())
        topic_count = sum(len(s.topics) for s in result.sections)
        assert topic_count == 3


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumEngineService.load_auto — public wrapper
# ═══════════════════════════════════════════════════════════════════════════════

class TestEngineServiceLoadAuto:
    def test_load_auto_returns_v1(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import Curriculum
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService

        repo = CurriculumRepository()
        repo._cache["testorg/te1/2026"] = load_from_dict(_v1_dict())

        engine = CurriculumEngineService(repository=repo)
        result = engine.load_auto("testorg", "te1", "2026")
        assert isinstance(result, Curriculum)

    def test_load_auto_returns_v2(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService

        repo = CurriculumRepository()
        repo._cache["testorg/te2/2026"] = load_from_dict(_v2_dict())

        engine = CurriculumEngineService(repository=repo)
        result = engine.load_auto("testorg", "te2", "2026")
        assert isinstance(result, CurriculumDefinition)

    def test_load_auto_caches_result(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService

        repo = CurriculumRepository()
        repo._cache["testorg/te1/2026"] = load_from_dict(_v1_dict())

        engine = CurriculumEngineService(repository=repo)
        r1 = engine.load_auto("testorg", "te1", "2026")
        r2 = engine.load_auto("testorg", "te1", "2026")
        assert r1 is r2  # Same cached object


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumEngineService.get_topics_flat — V1 and V2 flattening
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetTopicsFlat:
    def test_v1_returns_flat_list(self):
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        curriculum = load_from_dict(_v1_dict())
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        assert len(topics) == 2
        assert topics[0].code == "TE1-A"
        assert topics[1].code == "TE1-B"

    def test_v2_returns_flat_ordered_list(self):
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        curriculum = load_from_dict(_v2_dict())
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        assert len(topics) == 3
        # Section 1 topics come before Section 2 topics
        assert topics[0].code == "TE2-S1.1"
        assert topics[1].code == "TE2-S1.2"
        assert topics[2].code == "TE2-S2.1"

    def test_v2_respects_display_order(self):
        """Topics within each section follow display_order, not dict order."""
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        # Reverse display_order in one section
        data = _v2_dict()
        data["sections"][0]["topics"][0]["display_order"] = 2
        data["sections"][0]["topics"][1]["display_order"] = 1
        curriculum = load_from_dict(data)
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        # display_order=1 → TE2-S1.2 should come first within section 1
        assert topics[0].code == "TE2-S1.2"
        assert topics[1].code == "TE2-S1.1"

    def test_v2_respects_section_display_order(self):
        """Sections follow their own display_order."""
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        data = _v2_dict()
        # Swap section display_orders
        data["sections"][0]["display_order"] = 2
        data["sections"][1]["display_order"] = 1
        curriculum = load_from_dict(data)
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        # Section Two (originally display_order 2, now 1) should come first
        assert topics[0].code == "TE2-S2.1"
        assert topics[1].code == "TE2-S1.1"
        assert topics[2].code == "TE2-S1.2"

    def test_v1_preserves_original_order(self):
        """V1 topics preserve the original list order."""
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        curriculum = load_from_dict(_v1_dict())
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        codes = [t.code for t in topics]
        assert codes == ["TE1-A", "TE1-B"]

    def test_returns_list_not_generator(self):
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService

        for data in [_v1_dict(), _v2_dict()]:
            curriculum = load_from_dict(data)
            result = CurriculumEngineService.get_topics_flat(curriculum)
            assert isinstance(result, list)


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumService._load_curriculum_auto — thin delegate
# ═══════════════════════════════════════════════════════════════════════════════

class TestCurriculumServiceLoadAuto:
    def test_delegates_to_repo_load_auto(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import Curriculum
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_service import CurriculumService

        repo = CurriculumRepository()
        repo._cache["testorg/te1/2026"] = load_from_dict(_v1_dict())

        result = CurriculumService._load_curriculum_auto(repo, "testorg", "te1", "2026")
        assert isinstance(result, Curriculum)

    def test_v2_result(self):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_service import CurriculumService

        repo = CurriculumRepository()
        repo._cache["testorg/te2/2026"] = load_from_dict(_v2_dict())

        result = CurriculumService._load_curriculum_auto(repo, "testorg", "te2", "2026")
        assert isinstance(result, CurriculumDefinition)


# ═══════════════════════════════════════════════════════════════════════════════
# StudyPlanService._load_engine_curriculum_auto — tuple return
# ═══════════════════════════════════════════════════════════════════════════════

class TestStudyPlanServiceLoadAuto:
    def _make_repo_with(self, data: dict):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.repository import CurriculumRepository

        repo = CurriculumRepository()
        curriculum = load_from_dict(data)
        if data.get("organisation"):
            key = f"testorg/te1/2026"
        else:
            key = f"testorg/te2/2026"
        repo._cache[key] = curriculum
        return repo

    def test_returns_v1_tuple(self, monkeypatch):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import Curriculum
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        v1 = load_from_dict(_v1_dict())
        repo = CurriculumRepository()
        repo._cache["testorg/te1/2026"] = v1

        # Patch CurriculumEngineService to use our repo
        monkeypatch.setattr(
            CurriculumEngineService, "__init__",
            lambda self, repository=None: setattr(self, "_repo", repo) or None,
        )

        result = StudyPlanService._load_engine_curriculum_auto("testorg", "te1", "2026")
        assert result is not None
        curriculum, is_v2 = result
        assert isinstance(curriculum, Curriculum)
        assert is_v2 is False

    def test_returns_v2_tuple(self, monkeypatch):
        from app.curriculum.loader import load_from_dict
        from app.curriculum.models import CurriculumDefinition
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        v2 = load_from_dict(_v2_dict())
        repo = CurriculumRepository()
        repo._cache["testorg/te2/2026"] = v2

        monkeypatch.setattr(
            CurriculumEngineService, "__init__",
            lambda self, repository=None: setattr(self, "_repo", repo) or None,
        )

        result = StudyPlanService._load_engine_curriculum_auto("testorg", "te2", "2026")
        assert result is not None
        curriculum, is_v2 = result
        assert isinstance(curriculum, CurriculumDefinition)
        assert is_v2 is True

    def test_returns_none_on_missing(self, monkeypatch):
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        empty_repo = CurriculumRepository()

        monkeypatch.setattr(
            CurriculumEngineService, "__init__",
            lambda self, repository=None: setattr(self, "_repo", empty_repo) or None,
        )

        result = StudyPlanService._load_engine_curriculum_auto("ghost", "xx", "9999")
        assert result is None


# ═══════════════════════════════════════════════════════════════════════════════
# StudyPlanService._get_engine_topics_ordered — delegates to get_topics_flat
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetEngineTopicsOrdered:
    def test_v1_returns_flat_list(self):
        from app.curriculum.loader import load_from_dict
        from app.services.study_plan_service import StudyPlanService

        curriculum = load_from_dict(_v1_dict())
        topics = StudyPlanService._get_engine_topics_ordered(curriculum, is_v2=False)
        assert len(topics) == 2

    def test_v2_returns_flat_ordered_list(self):
        from app.curriculum.loader import load_from_dict
        from app.services.study_plan_service import StudyPlanService

        curriculum = load_from_dict(_v2_dict())
        topics = StudyPlanService._get_engine_topics_ordered(curriculum, is_v2=True)
        assert len(topics) == 3
        assert topics[0].code == "TE2-S1.1"

    def test_is_v2_flag_is_ignored_for_v2(self):
        """is_v2 param is now ignored; format is auto-detected from type."""
        from app.curriculum.loader import load_from_dict
        from app.services.study_plan_service import StudyPlanService

        curriculum = load_from_dict(_v2_dict())
        # Pass is_v2=False even though it's V2 — should still work correctly.
        topics = StudyPlanService._get_engine_topics_ordered(curriculum, is_v2=False)
        assert len(topics) == 3

    def test_consistent_with_get_topics_flat(self):
        """_get_engine_topics_ordered must produce same result as get_topics_flat."""
        from app.curriculum.loader import load_from_dict
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        for data in [_v1_dict(), _v2_dict()]:
            curriculum = load_from_dict(data)
            flat = CurriculumEngineService.get_topics_flat(curriculum)
            ordered = StudyPlanService._get_engine_topics_ordered(curriculum, is_v2=False)
            assert [t.code for t in flat] == [t.code for t in ordered]


# ═══════════════════════════════════════════════════════════════════════════════
# Traversal consistency — engine vs DB
# ═══════════════════════════════════════════════════════════════════════════════

class TestTraversalConsistency:
    def test_v2_engine_flat_order_matches_db_section_order(self, ctx):
        """Engine canonical order must match DB CurriculumService traversal."""
        from app.curriculum.loader import load_from_dict
        from app.extensions import db
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.curriculum_service import CurriculumService

        engine_curriculum = load_from_dict(_v2_dict())
        engine_topics = CurriculumEngineService.get_topics_flat(engine_curriculum)
        engine_codes = [t.code for t in engine_topics]

        # Build matching DB rows
        db_curriculum = Curriculum(
            exam_name="Test Exam V2", version="2026", active=True
        )
        db.session.add(db_curriculum)
        db.session.flush()

        global_order = 0
        db_sections = []
        for eng_section in sorted(
            engine_curriculum.sections, key=lambda s: s.display_order
        ):
            db_sec = Section(
                curriculum_id=db_curriculum.id,
                official_id=eng_section.id,
                code=eng_section.code,
                title=eng_section.title,
                display_order=eng_section.display_order,
            )
            db.session.add(db_sec)
            db.session.flush()
            db_sections.append(db_sec)

            for eng_topic in sorted(
                eng_section.topics, key=lambda t: t.display_order
            ):
                global_order += 1
                db_topic = Topic(
                    curriculum_id=db_curriculum.id,
                    name=eng_topic.title,
                    order=global_order,
                    recommended_minutes=eng_topic.estimated_minutes,
                    syllabus_weight=0.0,
                    active=True,
                    section_id=db_sec.id,
                )
                db.session.add(db_topic)

        db.session.flush()

        # DB canonical traversal
        db_topics = CurriculumService.get_all_topics_ordered(db_curriculum)
        db_names = [t.name for t in db_topics]

        # Engine canonical order
        engine_names = [t.title for t in engine_topics]

        assert db_names == engine_names


# ═══════════════════════════════════════════════════════════════════════════════
# flask backfill-sections — CLI command
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackfillSectionsCommand:
    """Tests for the flask backfill-sections CLI command."""

    def _setup_v2_curriculum_without_sections(self, db):
        """Create a V2-style Curriculum row with topics but no Section rows."""
        from app.extensions import db as _db
        from app.models.curriculum import Curriculum, Topic

        c = Curriculum(exam_name="Test Exam V2", version="2026", active=True)
        _db.session.add(c)
        _db.session.flush()

        t1 = Topic(
            curriculum_id=c.id,
            name="Topic One Alpha",
            order=1,
            recommended_minutes=120,
            syllabus_weight=0.0,
            active=True,
            section_id=None,
        )
        t2 = Topic(
            curriculum_id=c.id,
            name="Topic One Beta",
            order=2,
            recommended_minutes=90,
            syllabus_weight=0.0,
            active=True,
            section_id=None,
        )
        t3 = Topic(
            curriculum_id=c.id,
            name="Topic Two Alpha",
            order=3,
            recommended_minutes=60,
            syllabus_weight=0.0,
            active=True,
            section_id=None,
        )
        _db.session.add_all([t1, t2, t3])
        _db.session.commit()
        return c, [t1, t2, t3]

    def _patch_discovered(self, monkeypatch, data: dict):
        """Make the repository discover exactly one V2 curriculum (from a dict)."""
        from app.curriculum.exceptions import CurriculumLoadError
        from app.curriculum.loader import load_from_dict
        from app.curriculum.repository import CurriculumRepository

        engine_curriculum = load_from_dict(data)

        def fake_list_exams(_self):
            return [("TestOrg", "TE2", ["2026"])]

        def fake_load_auto(_self, org, paper, version):
            if org.lower() == "testorg" and paper.lower() == "te2":
                return engine_curriculum
            raise CurriculumLoadError(f"{org}/{paper}/{version}", "not found")

        monkeypatch.setattr(CurriculumRepository, "list_exams", fake_list_exams)
        monkeypatch.setattr(CurriculumRepository, "load_auto", fake_load_auto)
        return engine_curriculum

    def test_creates_sections_and_links_topics(self, ctx, runner, db, monkeypatch):
        """Backfill creates Section rows and sets Topic.section_id."""
        from app.models.curriculum import Section, Topic

        self._setup_v2_curriculum_without_sections(db)
        self._patch_discovered(monkeypatch, _v2_dict())

        result = runner.invoke(args=["backfill-sections"])
        assert result.exit_code == 0, result.output

        sections = Section.query.all()
        assert len(sections) == 2  # Two sections in V2 fixture

        linked = Topic.query.filter(Topic.section_id.isnot(None)).count()
        assert linked == 3  # All 3 topics linked

    def test_idempotent_on_second_run(self, ctx, runner, db, monkeypatch):
        """Running backfill twice does not create duplicate sections."""
        from app.models.curriculum import Section

        self._setup_v2_curriculum_without_sections(db)
        self._patch_discovered(monkeypatch, _v2_dict())

        runner.invoke(args=["backfill-sections"])
        runner.invoke(args=["backfill-sections"])

        # Should not have duplicate sections
        sections = Section.query.all()
        codes = [s.code for s in sections]
        assert len(codes) == len(set(codes))  # All unique

    def test_already_linked_topics_skipped(self, ctx, runner, db, monkeypatch):
        """Topics that already have section_id are not re-processed."""
        from app.extensions import db as _db
        from app.models.curriculum import Curriculum, Section, Topic

        # Create curriculum with sections already linked
        c = Curriculum(exam_name="Test Exam V2", version="2026", active=True)
        _db.session.add(c)
        _db.session.flush()

        sec = Section(
            curriculum_id=c.id,
            official_id="TE2-S1",
            code="TE2-S1",
            title="Section One",
            display_order=1,
        )
        _db.session.add(sec)
        _db.session.flush()

        t = Topic(
            curriculum_id=c.id,
            name="Topic One Alpha",
            order=1,
            recommended_minutes=120,
            syllabus_weight=0.0,
            active=True,
            section_id=sec.id,
        )
        _db.session.add(t)
        _db.session.commit()

        self._patch_discovered(monkeypatch, _v2_dict())

        result = runner.invoke(args=["backfill-sections"])
        assert result.exit_code == 0
        # No new sections should have been created beyond the one we started with
        assert Section.query.count() == 1

    def test_dry_run_makes_no_changes(self, ctx, runner, db, monkeypatch):
        """--dry-run reports what would happen but writes nothing."""
        from app.models.curriculum import Section

        self._setup_v2_curriculum_without_sections(db)
        self._patch_discovered(monkeypatch, _v2_dict())

        result = runner.invoke(args=["backfill-sections", "--dry-run"])
        assert result.exit_code == 0
        assert "Dry run" in result.output
        assert Section.query.count() == 0  # Nothing written

    def test_dry_run_reports_expected_counts(self, ctx, runner, db, monkeypatch):
        """--dry-run output mentions sections to create and topics to link."""
        self._setup_v2_curriculum_without_sections(db)
        self._patch_discovered(monkeypatch, _v2_dict())

        result = runner.invoke(args=["backfill-sections", "--dry-run"])
        assert "2 section(s)" in result.output
        assert "3 topic(s)" in result.output

    def test_no_changes_for_all_already_linked(self, ctx, runner, db, monkeypatch):
        """When all topics are already linked, the command reports OK."""
        from app.extensions import db as _db
        from app.models.curriculum import Curriculum, Section, Topic

        c = Curriculum(exam_name="Test Exam V2", version="2026", active=True)
        _db.session.add(c)
        _db.session.flush()

        for i, (sec_code, topic_names) in enumerate(
            [
                ("TE2-S1", ["Topic One Alpha", "Topic One Beta"]),
                ("TE2-S2", ["Topic Two Alpha"]),
            ],
            start=1,
        ):
            sec = Section(
                curriculum_id=c.id,
                official_id=sec_code,
                code=sec_code,
                title=f"Section {i}",
                display_order=i,
            )
            _db.session.add(sec)
            _db.session.flush()
            for j, name in enumerate(topic_names, start=1):
                _db.session.add(
                    Topic(
                        curriculum_id=c.id,
                        name=name,
                        order=j,
                        recommended_minutes=60,
                        syllabus_weight=0.0,
                        active=True,
                        section_id=sec.id,
                    )
                )
        _db.session.commit()

        self._patch_discovered(monkeypatch, _v2_dict())

        result = runner.invoke(args=["backfill-sections"])
        assert result.exit_code == 0
        assert "already linked" in result.output

    def test_v1_curriculum_skipped(self, ctx, runner, db, monkeypatch):
        """V1 curricula are silently skipped — no sections created."""
        from app.curriculum.loader import load_from_dict
        from app.curriculum.repository import CurriculumRepository
        from app.models.curriculum import Section

        v1 = load_from_dict(_v1_dict())

        def fake_list_exams(_self):
            return [("TestOrg", "TE1", ["2026"])]

        def fake_load_auto(_self, org, paper, version):
            return v1

        monkeypatch.setattr(CurriculumRepository, "list_exams", fake_list_exams)
        monkeypatch.setattr(CurriculumRepository, "load_auto", fake_load_auto)

        result = runner.invoke(args=["backfill-sections"])
        assert result.exit_code == 0
        assert Section.query.count() == 0  # Nothing created for V1


# ═══════════════════════════════════════════════════════════════════════════════
# No duplicate V1/V2 detection — smoke test
# ═══════════════════════════════════════════════════════════════════════════════

class TestNoDuplicateDetectionLogic:
    """Verify that only CurriculumRepository.load_auto contains the V1→V2
    fallback logic.  Other helpers must delegate, not reimplement it."""

    def test_curriculum_service_delegates_to_repo(self):
        """CurriculumService._load_curriculum_auto uses repo.load_auto."""
        import inspect

        from app.services.curriculum_service import CurriculumService

        source = inspect.getsource(CurriculumService._load_curriculum_auto)
        # Must call load_auto
        assert "load_auto" in source
        # Must NOT contain its own try/except V1/V2 branching
        assert "load_v2" not in source
        assert "repo.load(" not in source

    def test_study_plan_service_delegates_to_engine_service(self):
        """StudyPlanService._load_engine_curriculum_auto uses CurriculumEngineService."""
        import inspect

        from app.services.study_plan_service import StudyPlanService

        source = inspect.getsource(StudyPlanService._load_engine_curriculum_auto)
        assert "CurriculumEngineService" in source
        assert "load_auto" in source
        # Must NOT contain its own try/except V1/V2 branching
        assert "load_v2" not in source

    def test_engine_service_get_topics_flat_is_single_impl(self):
        """get_topics_flat contains the one canonical section→topic traversal."""
        import inspect

        from app.services.curriculum_engine_service import CurriculumEngineService

        source = inspect.getsource(CurriculumEngineService.get_topics_flat)
        # Contains the traversal
        assert "display_order" in source

    def test_study_plan_service_get_engine_topics_ordered_delegates(self):
        """_get_engine_topics_ordered delegates to get_topics_flat."""
        import inspect

        from app.services.study_plan_service import StudyPlanService

        source = inspect.getsource(StudyPlanService._get_engine_topics_ordered)
        assert "get_topics_flat" in source
        # Must NOT contain display_order traversal itself
        assert "display_order" not in source

    def test_build_student_curriculum_uses_get_topics_flat(self):
        """build_student_curriculum uses the shared get_topics_flat helper."""
        import inspect

        from app.services.curriculum_engine_service import CurriculumEngineService

        source = inspect.getsource(CurriculumEngineService.build_student_curriculum)
        assert "get_topics_flat" in source
        # The inline sorted(sections...) pattern must not be present here
        assert "curriculum.sections" not in source
