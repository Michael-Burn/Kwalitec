"""Phase 3 — official topic-code → SQL Topic.id resolver + ensure wrapper."""

from __future__ import annotations

import logging

import pytest

from app.application.student_runtime.syllabus_engine_map import (
    VERSION_MISMATCH_FALLBACK_MARKER,
    map_runtime_syllabus_to_engine,
)
from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import LearningObjective
from app.services.curriculum_service import CurriculumService


@pytest.mark.usefixtures("ctx")
class TestEnsureCurriculumRows:
    def test_missing_curriculum_triggers_import(self):
        assert (
            Curriculum.query.filter_by(
                exam_name="IFoA CS1", version="2026"
            ).first()
            is None
        )
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert curriculum is not None
        assert curriculum.exam_name == "IFoA CS1"
        assert curriculum.version == "2026"
        topics = Topic.query.filter_by(curriculum_id=curriculum.id).all()
        assert len(topics) > 0

    def test_second_call_is_idempotent(self, monkeypatch):
        first = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert first is not None
        topic_count = Topic.query.filter_by(curriculum_id=first.id).count()

        calls = {"n": 0}
        real_import = CurriculumService.import_curricula

        def _counting_import():
            calls["n"] += 1
            return real_import()

        monkeypatch.setattr(
            CurriculumService, "import_curricula", staticmethod(_counting_import)
        )
        second = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert second is not None
        assert second.id == first.id
        assert calls["n"] == 0  # already present — import not invoked
        assert Topic.query.filter_by(curriculum_id=first.id).count() == topic_count


@pytest.mark.usefixtures("ctx")
class TestResolveTopicIdForOfficialCode:
    def test_known_code_resolves_after_import(self):
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert curriculum is not None
        topic_id = CurriculumService.resolve_topic_id_for_official_code(
            curriculum, "1.1"
        )
        assert topic_id is not None
        topic = Topic.query.get(topic_id)
        assert topic is not None
        assert topic.curriculum_id == curriculum.id
        assert topic.name == "Describe the purpose and function of data analysis"

    def test_unknown_code_returns_none(self):
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert (
            CurriculumService.resolve_topic_id_for_official_code(
                curriculum, "99.99"
            )
            is None
        )

    def test_missing_curriculum_returns_none(self):
        assert (
            CurriculumService.resolve_topic_id_for_official_code(None, "1.1")
            is None
        )

    def test_empty_code_returns_none(self):
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert (
            CurriculumService.resolve_topic_id_for_official_code(curriculum, "  ")
            is None
        )

    def test_duplicate_title_does_not_conflate_when_lo_codes_differ(self):
        """Finding B: shared titles must not bind the wrong ORM id."""
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert curriculum is not None
        original_id = CurriculumService.resolve_topic_id_for_official_code(
            curriculum, "1.1"
        )
        assert original_id is not None
        original = Topic.query.get(original_id)
        assert original is not None

        impostor = Topic(
            curriculum_id=curriculum.id,
            name=original.name,
            order=9000,
            recommended_minutes=1,
            syllabus_weight=0.0,
            active=True,
        )
        db.session.add(impostor)
        db.session.flush()
        db.session.add(
            LearningObjective(
                topic_id=impostor.id,
                description="[9.9.1] decoy objective on a cloned title",
                order=1,
                active=True,
            )
        )
        db.session.commit()

        resolved = CurriculumService.resolve_topic_id_for_official_code(
            curriculum, "1.1"
        )
        assert resolved == original_id
        assert resolved != impostor.id

    def test_title_clone_without_los_still_binds_via_lo_code(self):
        curriculum = CurriculumService.ensure_curriculum_rows("IFoA CS1", "2026")
        assert curriculum is not None
        original_id = CurriculumService.resolve_topic_id_for_official_code(
            curriculum, "1.1"
        )
        assert original_id is not None
        original = Topic.query.get(original_id)
        db.session.add(
            Topic(
                curriculum_id=curriculum.id,
                name=original.name,
                order=9001,
                recommended_minutes=1,
                syllabus_weight=0.0,
                active=True,
            )
        )
        db.session.commit()
        assert (
            CurriculumService.resolve_topic_id_for_official_code(
                curriculum, "1.1"
            )
            == original_id
        )


class _FakeEngineRepo:
    """Minimal catalogue for version-selection tests (Finding C)."""

    def __init__(self, versions: tuple[str, ...]) -> None:
        self.versions = versions

    def list_exams(self):
        return [("ifoa", "CS1", list(self.versions))]

    def load_auto(self, organisation, paper, version):
        if version not in self.versions:
            raise FileNotFoundError(version)
        return type(
            "EngineCurriculum",
            (),
            {"organisation": "IFoA", "paper": "CS1"},
        )()


@pytest.mark.usefixtures("ctx")
class TestSyllabusEngineMap:
    def test_cs1_maps_with_version_mismatch_fallback(self, caplog):
        with caplog.at_level(logging.WARNING):
            mapped = map_runtime_syllabus_to_engine("CS1", "2027.1")
        assert mapped is not None
        assert mapped.exam_name == "IFoA CS1"
        assert mapped.version == "2026"
        assert mapped.version_mismatch_fallback is True
        assert VERSION_MISMATCH_FALLBACK_MARKER in caplog.text

    def test_exact_version_match_skips_fallback(self, caplog):
        with caplog.at_level(logging.WARNING):
            mapped = map_runtime_syllabus_to_engine("CS1", "2026")
        assert mapped is not None
        assert mapped.version == "2026"
        assert mapped.version_mismatch_fallback is False
        assert VERSION_MISMATCH_FALLBACK_MARKER not in caplog.text

    def test_unmappable_subject_returns_none(self):
        assert map_runtime_syllabus_to_engine("ECMP6", "2027.1") is None

    def test_year_stem_matches_without_fallback(self):
        repo = _FakeEngineRepo(versions=("2026", "2027"))
        mapped = map_runtime_syllabus_to_engine(
            "CS1", "2027.1", repo=repo
        )
        assert mapped is not None
        assert mapped.version == "2027"
        assert mapped.version_mismatch_fallback is False

    def test_unmatched_label_among_multiple_years_refuses(self, caplog):
        """Finding C: do not silently pick lexicographic latest."""
        repo = _FakeEngineRepo(versions=("2026", "2027"))
        with caplog.at_level(logging.WARNING):
            mapped = map_runtime_syllabus_to_engine(
                "CS1", "2099.9-nonexistent", repo=repo
            )
        assert mapped is None
        assert "unmatched version" in caplog.text
