"""Phase 3 — official topic-code → SQL Topic.id resolver + ensure wrapper."""

from __future__ import annotations

import logging

import pytest

from app.application.student_runtime.syllabus_engine_map import (
    VERSION_MISMATCH_FALLBACK_MARKER,
    map_runtime_syllabus_to_engine,
)
from app.models.curriculum import Curriculum, Topic
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
