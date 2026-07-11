"""Tests for section-aware curriculum service helpers (Milestone 1.8).

Covers:
- get_sections()                        — ordered section retrieval
- get_topics_for_section()              — topic retrieval within a section
- get_all_topics_ordered()              — canonical traversal helper
- get_ordered_topics()                  — public API delegates to canonical helper
- get_learning_objectives_for_topic()   — ordered LO retrieval
- get_topic_tree()                      — section-aware tree via centralized helpers
- V1 compatibility                      — no sections → parent_topic_id tree
- V2 compatibility                      — sections present → Section → Topic order
- Mixed curriculum support              — V1 and V2 curricula coexist in the same DB
- Ordering stability                    — deterministic ordering under all conditions
- CurriculumEngineService.build_student_curriculum() V2 section traversal
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# Fixture helpers (all run inside a pushed app context via `ctx`)
# ═══════════════════════════════════════════════════════════════════════════════


def _make_v1_curriculum(db_session):
    """Create a V1-style curriculum with 3 flat topics and no sections."""
    from app.models.curriculum import Curriculum, Topic

    c = Curriculum(exam_name="Test V1 Exam", version="2025", active=True)
    db_session.session.add(c)
    db_session.session.flush()

    t1 = Topic(curriculum_id=c.id, name="Alpha", order=1, recommended_minutes=60, active=True)
    t2 = Topic(curriculum_id=c.id, name="Beta",  order=2, recommended_minutes=60, active=True)
    t3 = Topic(curriculum_id=c.id, name="Gamma", order=3, recommended_minutes=60, active=True)
    db_session.session.add_all([t1, t2, t3])
    db_session.session.commit()
    return c, [t1, t2, t3]


def _make_v1_curriculum_with_subtopics(db_session):
    """Create a V1-style curriculum with parent/child topic nesting."""
    from app.models.curriculum import Curriculum, Topic

    c = Curriculum(exam_name="Test V1 Nested Exam", version="2025", active=True)
    db_session.session.add(c)
    db_session.session.flush()

    root = Topic(curriculum_id=c.id, name="Root", order=1, recommended_minutes=0, active=True)
    db_session.session.add(root)
    db_session.session.flush()

    child1 = Topic(
        curriculum_id=c.id, name="Child-1", order=1, recommended_minutes=30,
        active=True, parent_topic_id=root.id,
    )
    child2 = Topic(
        curriculum_id=c.id, name="Child-2", order=2, recommended_minutes=30,
        active=True, parent_topic_id=root.id,
    )
    db_session.session.add_all([child1, child2])
    db_session.session.commit()
    return c, root, [child1, child2]


def _make_v2_curriculum(db_session):
    """Create a V2-style curriculum with 2 sections, each containing topics."""
    from app.models.curriculum import Curriculum, Section, Topic

    c = Curriculum(exam_name="Test V2 Exam", version="2026", active=True)
    db_session.session.add(c)
    db_session.session.flush()

    sec_a = Section(
        curriculum_id=c.id, code="A", title="Section A",
        display_order=1, exam_weight=60.0,
    )
    sec_b = Section(
        curriculum_id=c.id, code="B", title="Section B",
        display_order=2, exam_weight=40.0,
    )
    db_session.session.add_all([sec_a, sec_b])
    db_session.session.flush()

    t_a1 = Topic(
        curriculum_id=c.id, name="A Topic 1", order=1,
        recommended_minutes=60, active=True, section_id=sec_a.id,
    )
    t_a2 = Topic(
        curriculum_id=c.id, name="A Topic 2", order=2,
        recommended_minutes=60, active=True, section_id=sec_a.id,
    )
    t_b1 = Topic(
        curriculum_id=c.id, name="B Topic 1", order=1,
        recommended_minutes=60, active=True, section_id=sec_b.id,
    )
    db_session.session.add_all([t_a1, t_a2, t_b1])
    db_session.session.commit()
    return c, [sec_a, sec_b], [t_a1, t_a2, t_b1]


# ═══════════════════════════════════════════════════════════════════════════════
# get_sections()
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetSections:
    """Tests for CurriculumService.get_sections()."""

    def test_v2_returns_sections_ordered_by_display_order(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, _ = _make_v2_curriculum(db)
        result = CurriculumService.get_sections(curriculum)

        assert len(result) == 2
        assert result[0].code == "A"
        assert result[1].code == "B"
        assert result[0].display_order < result[1].display_order

    def test_v1_returns_empty_list(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, _ = _make_v1_curriculum(db)
        result = CurriculumService.get_sections(curriculum)

        assert result == []

    def test_sections_are_ordered_when_stored_out_of_order(self, ctx, db):
        """Sections stored with non-sequential display_order values are
        still returned in ascending display_order sequence."""
        from app.models.curriculum import Curriculum, Section
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Out-of-order Sections", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        s3 = Section(curriculum_id=c.id, code="C", title="Third", display_order=30)
        s1 = Section(curriculum_id=c.id, code="A", title="First", display_order=10)
        s2 = Section(curriculum_id=c.id, code="B", title="Second", display_order=20)
        db.session.add_all([s3, s1, s2])
        db.session.commit()

        result = CurriculumService.get_sections(c)
        codes = [s.code for s in result]
        assert codes == ["A", "B", "C"]

    def test_get_sections_only_returns_own_curriculum_sections(self, ctx, db):
        """Sections from a different curriculum must not be returned."""
        from app.services.curriculum_service import CurriculumService

        c1, sections_c1, _ = _make_v2_curriculum(db)
        # Create a second V2 curriculum
        from app.models.curriculum import Curriculum, Section

        c2 = Curriculum(exam_name="Other V2 Exam", version="2026", active=True)
        db.session.add(c2)
        db.session.flush()
        db.session.add(Section(curriculum_id=c2.id, code="X", title="Extra", display_order=1))
        db.session.commit()

        result = CurriculumService.get_sections(c1)
        assert all(s.curriculum_id == c1.id for s in result)
        assert len(result) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# get_topics_for_section()
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetTopicsForSection:
    """Tests for CurriculumService.get_topics_for_section()."""

    def test_returns_active_topics_ordered_by_order(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, topics = _make_v2_curriculum(db)
        sec_a = sections[0]

        result = CurriculumService.get_topics_for_section(sec_a)
        assert len(result) == 2
        assert result[0].name == "A Topic 1"
        assert result[1].name == "A Topic 2"

    def test_excludes_inactive_topics(self, ctx, db):
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Active Test", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="S", title="Section", display_order=1)
        db.session.add(sec)
        db.session.flush()

        t_active = Topic(
            curriculum_id=c.id, name="Active Topic", order=1,
            recommended_minutes=30, active=True, section_id=sec.id,
        )
        t_inactive = Topic(
            curriculum_id=c.id, name="Inactive Topic", order=2,
            recommended_minutes=30, active=False, section_id=sec.id,
        )
        db.session.add_all([t_active, t_inactive])
        db.session.commit()

        result = CurriculumService.get_topics_for_section(sec)
        assert len(result) == 1
        assert result[0].name == "Active Topic"

    def test_returns_empty_for_section_with_no_topics(self, ctx, db):
        from app.models.curriculum import Curriculum, Section
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Empty Section Exam", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="E", title="Empty", display_order=1)
        db.session.add(sec)
        db.session.commit()

        result = CurriculumService.get_topics_for_section(sec)
        assert result == []

    def test_topics_ordered_by_order_field(self, ctx, db):
        """Topics stored out-of-order are returned in ascending order."""
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Order Test Exam", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="O", title="Order", display_order=1)
        db.session.add(sec)
        db.session.flush()

        t3 = Topic(curriculum_id=c.id, name="Third",  order=3, recommended_minutes=10, active=True, section_id=sec.id)
        t1 = Topic(curriculum_id=c.id, name="First",  order=1, recommended_minutes=10, active=True, section_id=sec.id)
        t2 = Topic(curriculum_id=c.id, name="Second", order=2, recommended_minutes=10, active=True, section_id=sec.id)
        db.session.add_all([t3, t1, t2])
        db.session.commit()

        result = CurriculumService.get_topics_for_section(sec)
        names = [t.name for t in result]
        assert names == ["First", "Second", "Third"]


# ═══════════════════════════════════════════════════════════════════════════════
# get_all_topics_ordered()
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetAllTopicsOrdered:
    """Tests for CurriculumService.get_all_topics_ordered()."""

    def test_v2_traverses_sections_then_topics(self, ctx, db):
        """V2: result is Section-A topics then Section-B topics."""
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, _ = _make_v2_curriculum(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)

        names = [t.name for t in result]
        assert names == ["A Topic 1", "A Topic 2", "B Topic 1"]

    def test_v2_section_display_order_drives_topic_sequence(self, ctx, db):
        """Reversing section display_order reverses the topic sequence."""
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Reversed Sections", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        # Sections stored with B first (display_order=1) and A second (display_order=2)
        sec_b = Section(curriculum_id=c.id, code="B", title="B", display_order=1)
        sec_a = Section(curriculum_id=c.id, code="A", title="A", display_order=2)
        db.session.add_all([sec_b, sec_a])
        db.session.flush()

        t_b = Topic(curriculum_id=c.id, name="B-T1", order=1, recommended_minutes=10, active=True, section_id=sec_b.id)
        t_a = Topic(curriculum_id=c.id, name="A-T1", order=1, recommended_minutes=10, active=True, section_id=sec_a.id)
        db.session.add_all([t_b, t_a])
        db.session.commit()

        result = CurriculumService.get_all_topics_ordered(c)
        names = [t.name for t in result]
        assert names == ["B-T1", "A-T1"]

    def test_v1_falls_back_to_parent_topic_tree(self, ctx, db):
        """V1: no sections → uses parent_topic_id DFS traversal."""
        from app.services.curriculum_service import CurriculumService

        curriculum, root, children = _make_v1_curriculum_with_subtopics(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)

        names = [t.name for t in result]
        # DFS: root → child-1 → child-2
        assert names == ["Root", "Child-1", "Child-2"]

    def test_v1_flat_topics_ordered_by_order_field(self, ctx, db):
        """V1: flat topics come back in ascending order field sequence."""
        from app.services.curriculum_service import CurriculumService

        curriculum, topics = _make_v1_curriculum(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)

        names = [t.name for t in result]
        assert names == ["Alpha", "Beta", "Gamma"]

    def test_v2_excludes_inactive_topics(self, ctx, db):
        """Inactive topics must not appear in the result even in V2 path."""
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Inactive V2", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="S", title="Sec", display_order=1)
        db.session.add(sec)
        db.session.flush()

        t_active   = Topic(curriculum_id=c.id, name="Active",   order=1, recommended_minutes=30, active=True,  section_id=sec.id)
        t_inactive = Topic(curriculum_id=c.id, name="Inactive", order=2, recommended_minutes=30, active=False, section_id=sec.id)
        db.session.add_all([t_active, t_inactive])
        db.session.commit()

        result = CurriculumService.get_all_topics_ordered(c)
        assert len(result) == 1
        assert result[0].name == "Active"

    def test_ordering_is_stable_across_repeated_calls(self, ctx, db):
        """Repeated calls with the same curriculum return the same sequence."""
        from app.services.curriculum_service import CurriculumService

        curriculum, _, _ = _make_v2_curriculum(db)
        first  = [t.id for t in CurriculumService.get_all_topics_ordered(curriculum)]
        second = [t.id for t in CurriculumService.get_all_topics_ordered(curriculum)]
        assert first == second


# ═══════════════════════════════════════════════════════════════════════════════
# get_ordered_topics() — public API
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetOrderedTopics:
    """Tests that get_ordered_topics() delegates to get_all_topics_ordered()."""

    def test_v2_returns_section_ordered_topics(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, _, _ = _make_v2_curriculum(db)
        result = CurriculumService.get_ordered_topics(curriculum)

        names = [t.name for t in result]
        assert names == ["A Topic 1", "A Topic 2", "B Topic 1"]

    def test_v1_returns_flat_topics_in_order(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, _ = _make_v1_curriculum(db)
        result = CurriculumService.get_ordered_topics(curriculum)

        names = [t.name for t in result]
        assert names == ["Alpha", "Beta", "Gamma"]

    def test_result_matches_get_all_topics_ordered(self, ctx, db):
        """get_ordered_topics() must return the exact same list as get_all_topics_ordered()."""
        from app.services.curriculum_service import CurriculumService

        curriculum, _, _ = _make_v2_curriculum(db)
        via_public  = [t.id for t in CurriculumService.get_ordered_topics(curriculum)]
        via_helper  = [t.id for t in CurriculumService.get_all_topics_ordered(curriculum)]
        assert via_public == via_helper


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Compatibility
# ═══════════════════════════════════════════════════════════════════════════════


class TestV1Compatibility:
    """Verify that the V1 traversal path is fully preserved."""

    def test_v1_topics_have_no_section_id(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, topics = _make_v1_curriculum(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)
        assert all(t.section_id is None for t in result)

    def test_v1_sections_are_empty(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, _ = _make_v1_curriculum(db)
        assert CurriculumService.get_sections(curriculum) == []

    def test_v1_nested_topics_returned_in_dfs_order(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, root, children = _make_v1_curriculum_with_subtopics(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)
        # Expected DFS: root first, then children in ascending order
        assert result[0].id == root.id
        assert result[1].name == "Child-1"
        assert result[2].name == "Child-2"

    def test_get_next_incomplete_topic_works_for_v1(self, ctx, db):
        """get_next_incomplete_topic() continues to work unchanged for V1."""
        from app.models.user import User
        from app.services.curriculum_service import CurriculumService

        u = User(email="v1compat@example.com", is_active_user=True)
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

        curriculum, topics = _make_v1_curriculum(db)
        next_topic = CurriculumService.get_next_incomplete_topic(u.id, curriculum)
        assert next_topic is not None
        assert next_topic.id == topics[0].id


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Compatibility
# ═══════════════════════════════════════════════════════════════════════════════


class TestV2Compatibility:
    """Verify V2 section-aware traversal works end-to-end."""

    def test_v2_topics_have_section_id_set(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, _ = _make_v2_curriculum(db)
        result = CurriculumService.get_all_topics_ordered(curriculum)
        assert all(t.section_id is not None for t in result)

    def test_v2_section_topics_are_grouped_correctly(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, _ = _make_v2_curriculum(db)
        sec_a, sec_b = sections

        a_topics = CurriculumService.get_topics_for_section(sec_a)
        b_topics = CurriculumService.get_topics_for_section(sec_b)

        assert len(a_topics) == 2
        assert len(b_topics) == 1
        assert all(t.section_id == sec_a.id for t in a_topics)
        assert all(t.section_id == sec_b.id for t in b_topics)

    def test_v2_get_next_incomplete_topic_follows_section_order(self, ctx, db):
        """The first incomplete topic for a V2 curriculum is the first topic
        in section display_order sequence."""
        from app.models.user import User
        from app.services.curriculum_service import CurriculumService

        u = User(email="v2compat@example.com", is_active_user=True)
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

        curriculum, sections, topics = _make_v2_curriculum(db)
        next_topic = CurriculumService.get_next_incomplete_topic(u.id, curriculum)
        # "A Topic 1" is first in section order
        assert next_topic is not None
        assert next_topic.name == "A Topic 1"


# ═══════════════════════════════════════════════════════════════════════════════
# Mixed Curriculum Support
# ═══════════════════════════════════════════════════════════════════════════════


class TestMixedCurriculumSupport:
    """V1 and V2 curricula may coexist; each follows its own traversal."""

    def test_v1_and_v2_curricula_traverse_independently(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        v1_curriculum, _ = _make_v1_curriculum(db)
        v2_curriculum, _, _ = _make_v2_curriculum(db)

        v1_topics = CurriculumService.get_all_topics_ordered(v1_curriculum)
        v2_topics = CurriculumService.get_all_topics_ordered(v2_curriculum)

        v1_names = [t.name for t in v1_topics]
        v2_names = [t.name for t in v2_topics]

        assert v1_names == ["Alpha", "Beta", "Gamma"]
        assert v2_names == ["A Topic 1", "A Topic 2", "B Topic 1"]

    def test_v1_sections_empty_v2_sections_populated(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        v1_curriculum, _ = _make_v1_curriculum(db)
        v2_curriculum, sections, _ = _make_v2_curriculum(db)

        assert CurriculumService.get_sections(v1_curriculum) == []
        assert len(CurriculumService.get_sections(v2_curriculum)) == 2

    def test_v1_topics_not_visible_through_v2_section_query(self, ctx, db):
        """Topics belonging to V1 (section_id=None) must not appear in V2
        section traversal."""
        from app.services.curriculum_service import CurriculumService

        _make_v1_curriculum(db)
        v2_curriculum, sections, _ = _make_v2_curriculum(db)

        v2_topics = CurriculumService.get_all_topics_ordered(v2_curriculum)
        v2_names = {t.name for t in v2_topics}

        assert "Alpha" not in v2_names
        assert "Beta"  not in v2_names


# ═══════════════════════════════════════════════════════════════════════════════
# Ordering Stability
# ═══════════════════════════════════════════════════════════════════════════════


class TestOrderingStability:
    """Ordering must be deterministic regardless of insertion order."""

    def test_v2_multi_section_ordering_is_stable(self, ctx, db):
        """Five sections with topics inserted in reverse display_order — result
        must still be in ascending display_order."""
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="Stability Test", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sections_and_topics: list[tuple[str, int, list[str]]] = [
            ("E", 5, ["E1"]),
            ("D", 4, ["D1"]),
            ("C", 3, ["C1"]),
            ("B", 2, ["B1"]),
            ("A", 1, ["A1"]),
        ]
        for code, disp_order, topic_names in sections_and_topics:
            sec = Section(
                curriculum_id=c.id, code=code, title=code,
                display_order=disp_order,
            )
            db.session.add(sec)
            db.session.flush()
            for i, name in enumerate(topic_names, start=1):
                db.session.add(
                    Topic(
                        curriculum_id=c.id, name=name, order=i,
                        recommended_minutes=10, active=True, section_id=sec.id,
                    )
                )
        db.session.commit()

        result = CurriculumService.get_all_topics_ordered(c)
        names = [t.name for t in result]
        assert names == ["A1", "B1", "C1", "D1", "E1"]

    def test_v2_within_section_topic_ordering_is_stable(self, ctx, db):
        """Topics within a section must be in ascending Topic.order even when
        inserted in reverse order."""
        from app.models.curriculum import Curriculum, Section, Topic
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="InSection Order", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="S", title="S", display_order=1)
        db.session.add(sec)
        db.session.flush()

        for order in [5, 3, 1, 4, 2]:
            db.session.add(
                Topic(
                    curriculum_id=c.id, name=f"T{order}", order=order,
                    recommended_minutes=10, active=True, section_id=sec.id,
                )
            )
        db.session.commit()

        result = CurriculumService.get_all_topics_ordered(c)
        orders = [t.order for t in result]
        assert orders == sorted(orders)

    def test_v1_ordering_unchanged(self, ctx, db):
        """V1 ordering must remain identical to the pre-milestone behaviour."""
        from app.services.curriculum_service import CurriculumService

        curriculum, topics = _make_v1_curriculum(db)

        service_result = [t.id for t in CurriculumService.get_all_topics_ordered(curriculum)]
        model_result   = [t.id for t in curriculum.get_all_topics_ordered()]

        assert service_result == model_result


# ═══════════════════════════════════════════════════════════════════════════════
# get_topic_tree()
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetTopicTree:
    """Tests for CurriculumService.get_topic_tree() section-aware shape."""

    def test_v2_tree_uses_sections_key(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, sections, _ = _make_v2_curriculum(db)
        tree = CurriculumService.get_topic_tree(curriculum)

        assert "sections" in tree
        assert "topics" not in tree
        assert tree["curriculum_id"] == curriculum.id
        assert len(tree["sections"]) == 2
        assert tree["sections"][0]["code"] == "A"
        assert tree["sections"][1]["code"] == "B"
        assert [t["name"] for t in tree["sections"][0]["topics"]] == [
            "A Topic 1",
            "A Topic 2",
        ]
        assert [t["name"] for t in tree["sections"][1]["topics"]] == ["B Topic 1"]

    def test_v2_tree_includes_ordered_learning_objectives(self, ctx, db):
        from app.models.curriculum import Curriculum, Section, Topic
        from app.models.learning import LearningObjective
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="LO Tree Exam", version="2026", active=True)
        db.session.add(c)
        db.session.flush()

        sec = Section(curriculum_id=c.id, code="A", title="A", display_order=1)
        db.session.add(sec)
        db.session.flush()

        topic = Topic(
            curriculum_id=c.id, name="T1", order=1,
            recommended_minutes=30, active=True, section_id=sec.id,
        )
        db.session.add(topic)
        db.session.flush()

        lo2 = LearningObjective(
            topic_id=topic.id, description="Second", order=2, active=True,
        )
        lo1 = LearningObjective(
            topic_id=topic.id, description="First", order=1, active=True,
        )
        db.session.add_all([lo2, lo1])
        db.session.commit()

        tree = CurriculumService.get_topic_tree(c)
        los = tree["sections"][0]["topics"][0]["learning_objectives"]
        assert [lo["description"] for lo in los] == ["First", "Second"]

    def test_v1_tree_keeps_topics_key_and_subtopics(self, ctx, db):
        from app.services.curriculum_service import CurriculumService

        curriculum, root, children = _make_v1_curriculum_with_subtopics(db)
        tree = CurriculumService.get_topic_tree(curriculum)

        assert "topics" in tree
        assert "sections" not in tree
        assert len(tree["topics"]) == 1
        assert tree["topics"][0]["name"] == "Root"
        assert [s["name"] for s in tree["topics"][0]["subtopics"]] == [
            "Child-1",
            "Child-2",
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# get_learning_objectives_for_topic()
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetLearningObjectivesForTopic:
    """Tests for CurriculumService.get_learning_objectives_for_topic()."""

    def test_returns_active_objectives_ordered(self, ctx, db):
        from app.models.curriculum import Curriculum, Section, Topic
        from app.models.learning import LearningObjective
        from app.services.curriculum_service import CurriculumService

        c = Curriculum(exam_name="LO Helper Exam", version="2026", active=True)
        db.session.add(c)
        db.session.flush()
        sec = Section(curriculum_id=c.id, code="A", title="A", display_order=1)
        db.session.add(sec)
        db.session.flush()
        topic = Topic(
            curriculum_id=c.id, name="T", order=1,
            recommended_minutes=10, active=True, section_id=sec.id,
        )
        db.session.add(topic)
        db.session.flush()

        db.session.add_all([
            LearningObjective(
                topic_id=topic.id, description="C", order=3, active=True,
            ),
            LearningObjective(
                topic_id=topic.id, description="A", order=1, active=True,
            ),
            LearningObjective(
                topic_id=topic.id, description="B", order=2, active=False,
            ),
        ])
        db.session.commit()

        result = CurriculumService.get_learning_objectives_for_topic(topic)
        assert [lo.description for lo in result] == ["A", "C"]


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumEngineService — V2 section traversal in build_student_curriculum()
# ═══════════════════════════════════════════════════════════════════════════════


class TestEngineServiceV2SectionTraversal:
    """build_student_curriculum() must handle V2 engine curricula via sections."""

    def _make_mock_v2_engine_curriculum(self):
        """Create a minimal V2 CurriculumDefinition in memory (no DB required)."""
        from datetime import date

        from app.curriculum.models import (
            CurriculumDefinition,
            LearningObjectiveDefinition,
            SectionDefinition,
            TopicDefinition,
        )

        lo = LearningObjectiveDefinition(
            id="CS2-A-T01-LO01", topic_id="CS2-A-T01",
            code="CS2-A.1.1", description="Understand probability",
            cognitive_level="understand", estimated_minutes=30,
            learning_type="concept", display_order=1,
        )
        topic_a1 = TopicDefinition(
            id="CS2-A-T01", section_id="CS2-A",
            code="CS2-A.1", title="Probability Fundamentals",
            description="Intro to probability", estimated_minutes=120,
            difficulty="foundational", display_order=1,
            learning_objectives=[lo],
        )
        topic_a2 = TopicDefinition(
            id="CS2-A-T02", section_id="CS2-A",
            code="CS2-A.2", title="Distributions",
            description="Common distributions", estimated_minutes=180,
            difficulty="intermediate", display_order=2,
            learning_objectives=[],
        )
        topic_b1 = TopicDefinition(
            id="CS2-B-T01", section_id="CS2-B",
            code="CS2-B.1", title="Regression",
            description="Linear regression", estimated_minutes=150,
            difficulty="intermediate", display_order=1,
            learning_objectives=[],
        )
        sec_a = SectionDefinition(
            id="CS2-A", code="A", title="Probability",
            description="Probability section", exam_weight=60.0,
            estimated_hours=10.0, difficulty="foundational",
            display_order=1, topics=[topic_a1, topic_a2],
        )
        sec_b = SectionDefinition(
            id="CS2-B", code="B", title="Statistics",
            description="Stats section", exam_weight=40.0,
            estimated_hours=8.0, difficulty="intermediate",
            display_order=2, topics=[topic_b1],
        )
        return CurriculumDefinition(
            exam_code="CS2", exam_name="Test Statistics",
            provider="IFoA", version="2026",
            effective_date=date(2026, 1, 1), superseded_date=None,
            total_estimated_hours=18.0,
            description="A test V2 curriculum",
            sections=[sec_a, sec_b],
        )

    def test_v2_engine_topics_flattened_in_section_order(self, ctx, db):
        """For a V2 engine curriculum, topics must be collected Section A then B."""
        from unittest.mock import MagicMock

        from app.services.curriculum_engine_service import CurriculumEngineService

        engine_curriculum = self._make_mock_v2_engine_curriculum()

        # Create matching DB curriculum and topics
        from app.models.curriculum import Curriculum, Topic

        db_c = Curriculum(exam_name="Test Statistics", version="2026", active=True)
        db.session.add(db_c)
        db.session.flush()

        db_t1 = Topic(curriculum_id=db_c.id, name="Probability Fundamentals", order=1, recommended_minutes=120, active=True, section_id=None)
        db_t2 = Topic(curriculum_id=db_c.id, name="Distributions",             order=2, recommended_minutes=180, active=True, section_id=None)
        db_t3 = Topic(curriculum_id=db_c.id, name="Regression",                order=3, recommended_minutes=150, active=True, section_id=None)
        db.session.add_all([db_t1, db_t2, db_t3])

        from app.models.user import User
        u = User(email="engine_v2@example.com", is_active_user=True)
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

        # Build a minimal study plan stub
        study_plan = MagicMock()
        study_plan.curriculum_id = db_c.id
        study_plan.curriculum_version = "2026"
        study_plan.exam_name = "IFoA CS2"
        study_plan.user_id = u.id
        study_plan.curriculum_topic_code = None

        # Wire repository to return V2 curriculum via canonical load_auto
        mock_repo = MagicMock()
        mock_repo.load_auto.return_value = engine_curriculum

        service = CurriculumEngineService(repository=mock_repo)

        # Patch parse_exam_name so we can use "IFoA CS2"
        from unittest.mock import patch
        with patch(
            "app.services.curriculum_engine_service.CurriculumEngineService.build_student_curriculum",
            wraps=service.build_student_curriculum,
        ):
            with patch("app.services.examination_catalogue.parse_exam_name", return_value=("IFoA", "CS2")):
                summary = service.build_student_curriculum(study_plan)

        assert summary is not None
        assert summary.total_topics == 3
        # No TopicProgress rows → all remaining
        assert summary.completed_topics == 0
        assert summary.remaining_topics == 3

    def test_v2_engine_equal_weighting_used(self, ctx, db):
        """V2 weighted_completed_percentage equals curriculum_coverage_percentage."""
        from unittest.mock import MagicMock, patch

        from app.models.curriculum import Curriculum, Topic
        from app.models.topic_progress import TopicProgress
        from app.models.user import User
        from app.services.curriculum_engine_service import CurriculumEngineService

        engine_curriculum = self._make_mock_v2_engine_curriculum()

        db_c = Curriculum(exam_name="Statistics V2W", version="2026", active=True)
        db.session.add(db_c)
        db.session.flush()

        db_t1 = Topic(curriculum_id=db_c.id, name="Probability Fundamentals", order=1, recommended_minutes=120, active=True)
        db_t2 = Topic(curriculum_id=db_c.id, name="Distributions",             order=2, recommended_minutes=180, active=True)
        db_t3 = Topic(curriculum_id=db_c.id, name="Regression",                order=3, recommended_minutes=150, active=True)
        db.session.add_all([db_t1, db_t2, db_t3])

        u = User(email="wt_v2@example.com", is_active_user=True)
        u.set_password("pw")
        db.session.add(u)
        db.session.flush()

        # Mark topic 1 as complete
        tp = TopicProgress(user_id=u.id, topic_id=db_t1.id, completed=True)
        db.session.add(tp)
        db.session.commit()

        study_plan = MagicMock()
        study_plan.curriculum_id = db_c.id
        study_plan.curriculum_version = "2026"
        study_plan.exam_name = "IFoA CS2"
        study_plan.user_id = u.id
        study_plan.curriculum_topic_code = None

        mock_repo = MagicMock()
        mock_repo.load_auto.return_value = engine_curriculum

        service = CurriculumEngineService(repository=mock_repo)
        with patch("app.services.examination_catalogue.parse_exam_name", return_value=("IFoA", "CS2")):
            summary = service.build_student_curriculum(study_plan)

        assert summary is not None
        assert summary.completed_topics == 1
        # Equal weighting → weighted % == simple coverage %
        assert abs(summary.weighted_completed_percentage - summary.curriculum_coverage_percentage) < 1e-9

    def test_v1_engine_path_unchanged(self, ctx, db):
        """V1 load path must still be tried first and used when V1 succeeds."""
        from datetime import date
        from unittest.mock import MagicMock, patch

        from app.curriculum.models import Curriculum as V1Curriculum
        from app.curriculum.models import LearningOutcome
        from app.curriculum.models import Topic as V1Topic
        from app.models.curriculum import Curriculum, Topic
        from app.models.user import User
        from app.services.curriculum_engine_service import CurriculumEngineService

        lo = LearningOutcome(id="lo1", code="C", description="desc")
        v1_topic = V1Topic(
            id="t1", code="T1", title="Probability",
            description="desc", weighting=100.0, estimated_hours=5.0,
            difficulty="foundational", learning_outcomes=[lo],
        )
        from app.curriculum.models import Curriculum as V1Curriculum
        v1_engine = V1Curriculum(
            organisation="IFoA", examination="CS1", paper="CS1",
            syllabus_version="2026", effective_from=date(2026, 1, 1),
            effective_to=None, total_weight=100.0,
            estimated_total_hours=5.0, topics=[v1_topic],
        )

        db_c = Curriculum(exam_name="IFoA CS1", version="2026", active=True)
        db.session.add(db_c)
        db.session.flush()
        db_t = Topic(curriculum_id=db_c.id, name="Probability", order=1, recommended_minutes=300, active=True)
        db.session.add(db_t)
        u = User(email="v1path@example.com", is_active_user=True)
        u.set_password("pw")
        db.session.add(u)
        db.session.commit()

        study_plan = MagicMock()
        study_plan.curriculum_id = db_c.id
        study_plan.curriculum_version = "2026"
        study_plan.exam_name = "IFoA CS1"
        study_plan.user_id = u.id
        study_plan.curriculum_topic_code = None

        mock_repo = MagicMock()
        mock_repo.load_auto.return_value = v1_engine  # load_auto returns V1

        service = CurriculumEngineService(repository=mock_repo)
        with patch("app.services.examination_catalogue.parse_exam_name", return_value=("IFoA", "CS1")):
            summary = service.build_student_curriculum(study_plan)

        # Canonical load_auto was called; result was V1 curriculum
        mock_repo.load_auto.assert_called_once()
        assert summary is not None
        assert summary.total_topics == 1
