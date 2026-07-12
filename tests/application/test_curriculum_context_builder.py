"""Tests for CurriculumContextBuilder (Capability 3.2.6).

Covers V1/V2 context emission, missing/invalid curricula, immutability,
canonical traversal order, and framework-independence of the builder module.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from app.application.curriculum import (
    CurriculumContextBuilder,
    InvalidCurriculumError,
    MissingCurriculumError,
)
from app.domain.readiness.curriculum_context import (
    CurriculumContext,
    CurriculumFormat,
)
from app.services.curriculum_service import CurriculumService

BUILDER_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "curriculum"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
    }
)

FORBIDDEN_PREFIXES = (
    "app.domain.readiness.aggregation",
    "app.domain.decision",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.domain.twin",
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════════


def _make_v1_curriculum(db_session):
    """V1 flat curriculum: three topics, no sections."""
    from app.models.curriculum import Curriculum, Topic

    curriculum = Curriculum(exam_name="Builder V1 Exam", version="2025", active=True)
    db_session.session.add(curriculum)
    db_session.session.flush()

    topics = [
        Topic(
            curriculum_id=curriculum.id,
            name="Alpha",
            order=1,
            recommended_minutes=60,
            syllabus_weight=0.5,
            active=True,
        ),
        Topic(
            curriculum_id=curriculum.id,
            name="Beta",
            order=2,
            recommended_minutes=60,
            syllabus_weight=0.3,
            active=True,
        ),
        Topic(
            curriculum_id=curriculum.id,
            name="Gamma",
            order=3,
            recommended_minutes=60,
            syllabus_weight=0.2,
            active=True,
        ),
    ]
    db_session.session.add_all(topics)
    db_session.session.commit()
    return curriculum, topics


def _make_v1_nested_curriculum(db_session):
    """V1 curriculum with parent/child nesting for traversal order checks."""
    from app.models.curriculum import Curriculum, Topic

    curriculum = Curriculum(
        exam_name="Builder V1 Nested Exam", version="2025", active=True
    )
    db_session.session.add(curriculum)
    db_session.session.flush()

    root = Topic(
        curriculum_id=curriculum.id,
        name="Root",
        order=1,
        recommended_minutes=0,
        syllabus_weight=1.0,
        active=True,
    )
    db_session.session.add(root)
    db_session.session.flush()

    child1 = Topic(
        curriculum_id=curriculum.id,
        name="Child-1",
        order=1,
        recommended_minutes=30,
        syllabus_weight=0.6,
        active=True,
        parent_topic_id=root.id,
    )
    child2 = Topic(
        curriculum_id=curriculum.id,
        name="Child-2",
        order=2,
        recommended_minutes=30,
        syllabus_weight=0.4,
        active=True,
        parent_topic_id=root.id,
    )
    db_session.session.add_all([child1, child2])
    db_session.session.commit()
    return curriculum, [root, child1, child2]


def _make_v2_curriculum(db_session):
    """V2 sectioned curriculum with ordered sections and topics."""
    from app.models.curriculum import Curriculum, Section, Topic

    curriculum = Curriculum(exam_name="Builder V2 Exam", version="2026", active=True)
    db_session.session.add(curriculum)
    db_session.session.flush()

    sec_a = Section(
        curriculum_id=curriculum.id,
        official_id="CS1-A",
        code="A",
        title="Section A",
        display_order=1,
        exam_weight=60.0,
    )
    sec_b = Section(
        curriculum_id=curriculum.id,
        official_id="CS1-B",
        code="B",
        title="Section B",
        display_order=2,
        exam_weight=40.0,
    )
    db_session.session.add_all([sec_a, sec_b])
    db_session.session.flush()

    topics = [
        Topic(
            curriculum_id=curriculum.id,
            name="A Topic 1",
            order=1,
            recommended_minutes=60,
            syllabus_weight=0.0,
            active=True,
            section_id=sec_a.id,
        ),
        Topic(
            curriculum_id=curriculum.id,
            name="A Topic 2",
            order=2,
            recommended_minutes=60,
            syllabus_weight=0.0,
            active=True,
            section_id=sec_a.id,
        ),
        Topic(
            curriculum_id=curriculum.id,
            name="B Topic 1",
            order=1,
            recommended_minutes=60,
            syllabus_weight=0.0,
            active=True,
            section_id=sec_b.id,
        ),
    ]
    db_session.session.add_all(topics)
    db_session.session.commit()
    return curriculum, [sec_a, sec_b], topics


def _make_empty_curriculum(db_session):
    """Curriculum row with no topics — invalid denominator."""
    from app.models.curriculum import Curriculum

    curriculum = Curriculum(exam_name="Empty Exam", version="2025", active=True)
    db_session.session.add(curriculum)
    db_session.session.commit()
    return curriculum


# ═══════════════════════════════════════════════════════════════════════════════
# V1 / V2 context
# ═══════════════════════════════════════════════════════════════════════════════


class TestV1Context:
    def test_build_emits_v1_context(self, ctx, db):
        curriculum, topics = _make_v1_curriculum(db)

        result = CurriculumContextBuilder.build(curriculum.id)

        assert isinstance(result, CurriculumContext)
        assert result.curriculum_id == str(curriculum.id)
        assert result.format is CurriculumFormat.V1
        assert result.section_ids == ()
        assert result.topic_ids == tuple(str(t.id) for t in topics)
        assert result.weight_for(str(topics[0].id)) == pytest.approx(0.5)
        assert result.topics[0].section_id is None

    def test_build_from_curriculum_matches_build(self, ctx, db):
        curriculum, _ = _make_v1_curriculum(db)

        via_id = CurriculumContextBuilder.build(curriculum.id)
        via_row = CurriculumContextBuilder.build_from_curriculum(curriculum)

        assert via_id == via_row


class TestV2Context:
    def test_build_emits_v2_context(self, ctx, db):
        curriculum, sections, topics = _make_v2_curriculum(db)

        result = CurriculumContextBuilder.build(curriculum.id)

        assert result.curriculum_id == str(curriculum.id)
        assert result.format is CurriculumFormat.V2
        assert result.section_ids == ("CS1-A", "CS1-B")
        assert result.topic_ids == tuple(str(t.id) for t in topics)
        assert result.topics[0].section_id == "CS1-A"
        assert result.topics[2].section_id == "CS1-B"
        # V2 topic weights reflect owning section exam_weight (not topic 0.0).
        assert result.weight_for(str(topics[0].id)) == pytest.approx(60.0)
        assert result.weight_for(str(topics[2].id)) == pytest.approx(40.0)
        assert sections[0].official_id == "CS1-A"


# ═══════════════════════════════════════════════════════════════════════════════
# Missing / invalid
# ═══════════════════════════════════════════════════════════════════════════════


class TestMissingCurriculum:
    def test_none_curriculum_id_raises(self, ctx, db):
        with pytest.raises(MissingCurriculumError):
            CurriculumContextBuilder.build(None)

    def test_unknown_curriculum_id_raises(self, ctx, db):
        with pytest.raises(MissingCurriculumError):
            CurriculumContextBuilder.build(999_999)

    def test_non_positive_curriculum_id_raises(self, ctx, db):
        with pytest.raises(MissingCurriculumError):
            CurriculumContextBuilder.build(0)

    def test_none_curriculum_row_raises(self, ctx, db):
        with pytest.raises(MissingCurriculumError):
            CurriculumContextBuilder.build_from_curriculum(None)  # type: ignore[arg-type]


class TestInvalidCurriculum:
    def test_empty_topic_list_raises(self, ctx, db):
        curriculum = _make_empty_curriculum(db)

        with pytest.raises(InvalidCurriculumError):
            CurriculumContextBuilder.build(curriculum.id)

    def test_v2_topic_missing_section_raises(self, ctx, db, monkeypatch):
        """Fail closed when traversal yields a V2 topic without section linkage."""
        curriculum, _, topics = _make_v2_curriculum(db)
        broken = topics[0]
        broken.section_id = None

        monkeypatch.setattr(
            CurriculumService,
            "get_all_topics_ordered",
            staticmethod(lambda _c: [broken]),
        )

        with pytest.raises(InvalidCurriculumError):
            CurriculumContextBuilder.build_from_curriculum(curriculum)

    def test_unpersisted_curriculum_raises_missing(self, ctx, db):
        from app.models.curriculum import Curriculum

        unpersisted = Curriculum(
            exam_name="Unsaved Exam", version="2025", active=True
        )
        with pytest.raises(MissingCurriculumError):
            CurriculumContextBuilder.build_from_curriculum(unpersisted)


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutability:
    def test_context_is_frozen(self, ctx, db):
        curriculum, _ = _make_v1_curriculum(db)
        result = CurriculumContextBuilder.build(curriculum.id)

        with pytest.raises(FrozenInstanceError):
            result.curriculum_id = "mutated"  # type: ignore[misc]

        with pytest.raises(FrozenInstanceError):
            result.topics[0].weight = 99.0  # type: ignore[misc]

        assert isinstance(result.topics, tuple)
        assert isinstance(result.section_ids, tuple)


# ═══════════════════════════════════════════════════════════════════════════════
# Canonical traversal
# ═══════════════════════════════════════════════════════════════════════════════


class TestCanonicalTraversal:
    def test_v1_order_matches_curriculum_service(self, ctx, db):
        curriculum, _ = _make_v1_nested_curriculum(db)
        expected = CurriculumService.get_all_topics_ordered(curriculum)

        result = CurriculumContextBuilder.build(curriculum.id)

        assert result.topic_ids == tuple(str(t.id) for t in expected)
        assert [t.name for t in expected] == ["Root", "Child-1", "Child-2"]

    def test_v2_order_matches_curriculum_service(self, ctx, db):
        curriculum, _, _ = _make_v2_curriculum(db)
        expected = CurriculumService.get_all_topics_ordered(curriculum)

        result = CurriculumContextBuilder.build(curriculum.id)

        assert result.topic_ids == tuple(str(t.id) for t in expected)
        assert [t.name for t in expected] == ["A Topic 1", "A Topic 2", "B Topic 1"]

    def test_builder_does_not_reorder_by_weight(self, ctx, db):
        """Syllabus order is not a study-priority ranking."""
        from app.models.curriculum import Curriculum, Topic

        curriculum = Curriculum(
            exam_name="Weight Order Exam", version="2025", active=True
        )
        db.session.add(curriculum)
        db.session.flush()
        # Higher weight last in syllabus order — builder must not promote it.
        low = Topic(
            curriculum_id=curriculum.id,
            name="Low-weight-first",
            order=1,
            recommended_minutes=30,
            syllabus_weight=0.1,
            active=True,
        )
        high = Topic(
            curriculum_id=curriculum.id,
            name="High-weight-second",
            order=2,
            recommended_minutes=30,
            syllabus_weight=0.9,
            active=True,
        )
        db.session.add_all([low, high])
        db.session.commit()

        result = CurriculumContextBuilder.build(curriculum.id)

        assert result.topic_ids == (str(low.id), str(high.id))


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / firewall
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_builder_module_has_no_flask_or_educational_engine_imports(self):
        violations: list[str] = []
        for path in sorted(BUILDER_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
        assert violations == []

    def test_builder_source_does_not_call_educational_domains(self):
        src = (
            BUILDER_ROOT / "curriculum_context_builder.py"
        ).read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "flask.request" not in src
        assert "flask.session" not in src

    def test_output_is_domain_curriculum_context(self, ctx, db):
        curriculum, _ = _make_v1_curriculum(db)
        result = CurriculumContextBuilder.build(curriculum.id)
        assert result.__class__.__module__ == (
            "app.domain.readiness.curriculum_context"
        )
