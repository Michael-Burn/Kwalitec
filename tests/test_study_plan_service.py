"""Tests for StudyPlanService section-aware plan generation (Milestone 1.9).

Coverage
--------
- _load_engine_curriculum_auto  — V1 fast path, V2 fallback, both-fail
- _get_engine_topics_ordered    — V1 flat list, V2 section-ordered flattening
- _initialize_topic_progress_from_curriculum
    - V1 regression (real on-disk curriculum)
    - V2 section-aware: TopicProgress rows created in Section→Topic order
    - V2 section_id populated on created DB Topic rows
    - V2 Topics ordered globally by Section.display_order then Topic.display_order
    - Completed topics initialised correctly for V2
    - Current topic promotion works for V2
    - Existing TopicProgress rows are never overwritten
    - Idempotency: second plan for same curriculum leaves row count unchanged
- _sync_completed_topics        — V2-aware completion sync
- _create_topic_progress_if_absent — skips existing records
- Ordering stability            — deterministic across repeated calls
- V1 compatibility              — existing flat-topic behaviour is unchanged
- V2 compatibility              — sections present → canonical section ordering
- Regression protection         — existing V1 study plan tests continue to pass
"""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock, patch

# ═══════════════════════════════════════════════════════════════════════════════
# Shared helpers
# ═══════════════════════════════════════════════════════════════════════════════


def _make_user(db):
    from app.models.user import User

    u = User(email="sp_test@example.com", is_active_user=True)
    u.set_password("pw")
    db.session.add(u)
    db.session.commit()
    return u


def _make_v2_engine_curriculum():
    """Build a minimal in-memory V2 CurriculumDefinition for testing."""
    from app.curriculum.models import (
        CurriculumDefinition,
        LearningObjectiveDefinition,
        SectionDefinition,
        TopicDefinition,
    )

    lo_a1 = LearningObjectiveDefinition(
        id="T2-A-T01-LO01", topic_id="T2-A-T01",
        code="T2-A.1.1", description="Understand alpha",
        cognitive_level="understand", estimated_minutes=20,
        learning_type="concept", display_order=1,
    )
    lo_a2 = LearningObjectiveDefinition(
        id="T2-A-T01-LO02", topic_id="T2-A-T01",
        code="T2-A.1.2", description="Apply alpha",
        cognitive_level="apply", estimated_minutes=20,
        learning_type="procedure", display_order=2,
    )
    topic_a1 = TopicDefinition(
        id="T2-A-T01", section_id="T2-A",
        code="T2-A.1", title="Alpha Topic",
        description="First topic in section A",
        estimated_minutes=60, difficulty="foundational", display_order=1,
        learning_objectives=[lo_a1, lo_a2],
    )
    topic_a2 = TopicDefinition(
        id="T2-A-T02", section_id="T2-A",
        code="T2-A.2", title="Beta Topic",
        description="Second topic in section A",
        estimated_minutes=90, difficulty="intermediate", display_order=2,
        learning_objectives=[],
    )
    topic_b1 = TopicDefinition(
        id="T2-B-T01", section_id="T2-B",
        code="T2-B.1", title="Gamma Topic",
        description="First topic in section B",
        estimated_minutes=120, difficulty="intermediate", display_order=1,
        learning_objectives=[],
    )
    sec_a = SectionDefinition(
        id="T2-A", code="SA", title="Section A",
        description="First section", exam_weight=60.0,
        estimated_hours=5.0, difficulty="foundational",
        display_order=1, topics=[topic_a1, topic_a2],
    )
    sec_b = SectionDefinition(
        id="T2-B", code="SB", title="Section B",
        description="Second section", exam_weight=40.0,
        estimated_hours=4.0, difficulty="intermediate",
        display_order=2, topics=[topic_b1],
    )
    return CurriculumDefinition(
        exam_code="T2", exam_name="Test V2 Exam",
        provider="TestOrg", version="2026",
        effective_date=date(2026, 1, 1), superseded_date=None,
        total_estimated_hours=9.0,
        description="A synthetic V2 curriculum for testing",
        sections=[sec_a, sec_b],
    )


def _patch_repo_for_v2(v2_curriculum):
    """Return a context-manager that patches CurriculumRepository so that
    load_auto() returns *v2_curriculum* (a CurriculumDefinition instance)."""
    mock_repo = MagicMock()
    mock_repo.load_auto.return_value = v2_curriculum
    return patch(
        "app.services.curriculum_engine_service.CurriculumRepository",
        return_value=mock_repo,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# _load_engine_curriculum_auto
# ═══════════════════════════════════════════════════════════════════════════════


class TestLoadEngineCurriculumAuto:
    """Unit tests for StudyPlanService._load_engine_curriculum_auto."""

    def test_real_cs1_returned_as_v2(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        # Real on-disk CS1 curriculum is the canonical V2 syllabus.
        result = StudyPlanService._load_engine_curriculum_auto("IFoA", "CS1", "2026")
        assert result is not None
        engine_curriculum, is_v2 = result
        assert is_v2 is True
        assert hasattr(engine_curriculum, "sections")
        assert len(engine_curriculum.sections) == 5

    def test_v2_fallback_returns_is_v2_true(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        v2_curriculum = _make_v2_engine_curriculum()
        with _patch_repo_for_v2(v2_curriculum):
            result = StudyPlanService._load_engine_curriculum_auto(
                "TestOrg", "T2", "2026"
            )
        assert result is not None
        engine_curriculum, is_v2 = result
        assert is_v2 is True
        assert engine_curriculum is v2_curriculum

    def test_both_formats_fail_returns_none(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        mock_repo = MagicMock()
        mock_repo.load_auto.side_effect = Exception("no curriculum found")

        _target = "app.services.curriculum_engine_service.CurriculumRepository"
        with patch(_target, return_value=mock_repo):
            result = StudyPlanService._load_engine_curriculum_auto(
                "Nonexistent", "XX", "9999"
            )
        assert result is None

    def test_v1_unexpected_error_returns_none(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        mock_repo = MagicMock()
        mock_repo.load_auto.side_effect = RuntimeError("unexpected")

        _target = "app.services.curriculum_engine_service.CurriculumRepository"
        with patch(_target, return_value=mock_repo):
            result = StudyPlanService._load_engine_curriculum_auto(
                "Any", "XX", "2026"
            )
        assert result is None


# ═══════════════════════════════════════════════════════════════════════════════
# _get_engine_topics_ordered
# ═══════════════════════════════════════════════════════════════════════════════


class TestGetEngineTopicsOrdered:
    """Unit tests for StudyPlanService._get_engine_topics_ordered."""

    def test_real_cs1_returns_flat_topics_from_sections(self, ctx, db):
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        result = StudyPlanService._load_engine_curriculum_auto("IFoA", "CS1", "2026")
        assert result is not None
        engine_curriculum, is_v2 = result
        assert is_v2 is True

        ordered = StudyPlanService._get_engine_topics_ordered(engine_curriculum, True)
        expected = CurriculumEngineService.get_topics_flat(engine_curriculum)
        assert ordered == expected
        assert len(ordered) == 14
        assert [t.code for t in ordered[:2]] == ["1.1", "1.2"]

    def test_v2_flattens_in_section_display_order(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        v2 = _make_v2_engine_curriculum()
        ordered = StudyPlanService._get_engine_topics_ordered(v2, True)

        titles = [t.title for t in ordered]
        # Section A (display_order=1) topics first, then Section B (display_order=2)
        assert titles == ["Alpha Topic", "Beta Topic", "Gamma Topic"]

    def test_v2_within_section_topic_display_order_respected(self, ctx, db):
        """Topics stored in reverse display_order within a section must still
        be returned in ascending display_order."""
        from app.curriculum.models import (
            CurriculumDefinition,
            SectionDefinition,
            TopicDefinition,
        )
        from app.services.study_plan_service import StudyPlanService

        t_late = TopicDefinition(
            id="late", section_id="S", code="X.2", title="Late",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=2,
        )
        t_early = TopicDefinition(
            id="early", section_id="S", code="X.1", title="Early",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=1,
        )
        sec = SectionDefinition(
            id="S", code="S", title="S", description="",
            exam_weight=100.0, estimated_hours=1.0, difficulty="foundational",
            display_order=1, topics=[t_late, t_early],  # stored out of order
        )
        v2 = CurriculumDefinition(
            exam_code="X", exam_name="X", provider="X", version="2026",
            effective_date=date(2026, 1, 1), superseded_date=None,
            total_estimated_hours=1.0, description="",
            sections=[sec],
        )

        ordered = StudyPlanService._get_engine_topics_ordered(v2, True)
        titles = [t.title for t in ordered]
        assert titles == ["Early", "Late"]

    def test_v2_section_display_order_drives_overall_sequence(self, ctx, db):
        """Sections stored in reverse display_order must yield topics in
        correct ascending section sequence."""
        from app.curriculum.models import (
            CurriculumDefinition,
            SectionDefinition,
            TopicDefinition,
        )
        from app.services.study_plan_service import StudyPlanService

        t_b = TopicDefinition(
            id="b", section_id="B", code="B.1", title="B Topic",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=1,
        )
        t_a = TopicDefinition(
            id="a", section_id="A", code="A.1", title="A Topic",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=1,
        )
        sec_b = SectionDefinition(
            id="B", code="B", title="B", description="",
            exam_weight=40.0, estimated_hours=1.0, difficulty="intermediate",
            display_order=2, topics=[t_b],
        )
        sec_a = SectionDefinition(
            id="A", code="A", title="A", description="",
            exam_weight=60.0, estimated_hours=1.0, difficulty="foundational",
            display_order=1, topics=[t_a],
        )
        v2 = CurriculumDefinition(
            exam_code="TS", exam_name="TS", provider="TS", version="2026",
            effective_date=date(2026, 1, 1), superseded_date=None,
            total_estimated_hours=2.0, description="",
            sections=[sec_b, sec_a],  # stored with B first
        )

        ordered = StudyPlanService._get_engine_topics_ordered(v2, True)
        titles = [t.title for t in ordered]
        assert titles == ["A Topic", "B Topic"]

    def test_ordering_is_deterministic_across_repeated_calls(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        v2 = _make_v2_engine_curriculum()
        first = [t.code for t in StudyPlanService._get_engine_topics_ordered(v2, True)]
        second = [t.code for t in StudyPlanService._get_engine_topics_ordered(v2, True)]
        assert first == second


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Regression — existing flat-topic behaviour must be unchanged
# ═══════════════════════════════════════════════════════════════════════════════


class TestCanonicalCS1Regression:
    """Regression tests for the real on-disk canonical CS1 V2 curriculum."""
    """Verify that the V1 path inside _initialize_topic_progress_from_curriculum
    is completely unchanged after the Milestone 1.9 refactoring."""

    def test_creates_topic_progress_rows(self, ctx, db):
        """Creating a plan against canonical CS1-2026 must produce one
        TopicProgress row per engine topic."""
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )

        progress_rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(progress_rows) == 14  # 14 subtopics in canonical CS1-2026

    def test_topics_have_section_id(self, ctx, db):
        """Canonical CS1 DB topics must link to their parent section."""
        from app.models.curriculum import Topic as DBTopic
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )

        topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        assert all(t.section_id is not None for t in topics)

    def test_current_topic_marked_learning(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )

        topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Describe the purpose and function of data analysis",
        ).first()
        assert topic is not None
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic.id,
        ).first()
        assert tp is not None
        assert tp.current_stage == TopicProgress.STAGE_LEARNING
        assert tp.completed is False

    def test_completed_topics_marked_correctly(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="1.2",
            completed_curriculum_topics=["1.1"],
        )

        topic_a = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Describe the purpose and function of data analysis",
        ).first()
        tp_a = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic_a.id,
        ).first()
        assert tp_a.completed is True
        assert tp_a.mastery_score == 100.0

    def test_v1_topic_ordering_uses_engine_order(self, ctx, db):
        """DB topics for V1 curriculum must have order values 1, 2, 3... matching
        the engine's flat topics list."""
        from app.models.curriculum import Topic as DBTopic
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
        )

        topics = (
            DBTopic.query.filter_by(curriculum_id=sp.curriculum_id)
            .order_by(DBTopic.order)
            .all()
        )
        orders = [t.order for t in topics]
        assert orders == list(range(1, len(orders) + 1))


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Compatibility — section-aware initialisation
# ═══════════════════════════════════════════════════════════════════════════════


class TestV2SectionAwareInitialisation:
    """Verify that the V2 path creates TopicProgress rows in canonical
    Section (display_order) → Topic (display_order) order."""

    def _create_v2_plan(self, db, user, v2_curriculum, **kwargs):
        """Create a study plan backed by the mock V2 curriculum."""
        from app.services.study_plan_service import StudyPlanService

        defaults = dict(
            user_id=user.id,
            exam_name="TestOrg T2",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
        )
        defaults.update(kwargs)

        with _patch_repo_for_v2(v2_curriculum):
            return StudyPlanService.create_study_plan(**defaults)

    def test_v2_creates_one_progress_row_per_topic(self, ctx, db):
        from app.models.topic_progress import TopicProgress

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        self._create_v2_plan(db, user, v2)

        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(rows) == 3  # Alpha, Beta, Gamma

    def test_v2_topics_created_with_section_id(self, ctx, db):
        """All DB topics created for a V2 curriculum must have section_id set."""
        from app.models.curriculum import Topic as DBTopic

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(db, user, v2)

        topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        assert len(topics) == 3
        assert all(t.section_id is not None for t in topics)

    def test_v2_db_sections_created(self, ctx, db):
        """Section rows must be created in the DB when a V2 plan is initialised."""
        from app.models.curriculum import Section

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(db, user, v2)

        sections = Section.query.filter_by(curriculum_id=sp.curriculum_id).all()
        assert len(sections) == 2
        codes = {s.code for s in sections}
        assert codes == {"SA", "SB"}

    def test_v2_topics_ordered_by_section_then_topic(self, ctx, db):
        """Topics must be assigned global order values following
        Section.display_order → Topic.display_order."""
        from app.models.curriculum import Curriculum
        from app.services.curriculum_service import CurriculumService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(db, user, v2)

        db_curriculum = Curriculum.query.get(sp.curriculum_id)
        ordered = CurriculumService.get_all_topics_ordered(db_curriculum)
        names = [t.name for t in ordered]
        # Section A (display_order=1): Alpha Topic, Beta Topic
        # Section B (display_order=2): Gamma Topic
        assert names == ["Alpha Topic", "Beta Topic", "Gamma Topic"]

    def test_v2_section_display_order_controls_global_order(self, ctx, db):
        """Reversing section display_order must reverse the topic sequence
        returned by CurriculumService.get_all_topics_ordered."""
        from app.curriculum.models import (
            CurriculumDefinition,
            SectionDefinition,
            TopicDefinition,
        )
        from app.models.curriculum import Curriculum
        from app.services.curriculum_service import CurriculumService
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)

        t_b = TopicDefinition(
            id="b1", section_id="B", code="B.1", title="B Topic",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=1,
        )
        t_a = TopicDefinition(
            id="a1", section_id="A", code="A.1", title="A Topic",
            description="", estimated_minutes=30, difficulty="foundational",
            display_order=1,
        )
        sec_b = SectionDefinition(
            id="B", code="SB", title="Section B", description="",
            exam_weight=40.0, estimated_hours=1.0, difficulty="intermediate",
            display_order=2, topics=[t_b],
        )
        sec_a = SectionDefinition(
            id="A", code="SA", title="Section A", description="",
            exam_weight=60.0, estimated_hours=1.0, difficulty="foundational",
            display_order=1, topics=[t_a],
        )
        # Sections stored with B before A in the engine list
        v2 = CurriculumDefinition(
            exam_code="RV", exam_name="TestOrg RV", provider="TestOrg",
            version="2026", effective_date=date(2026, 1, 1), superseded_date=None,
            total_estimated_hours=2.0, description="",
            sections=[sec_b, sec_a],
        )

        with _patch_repo_for_v2(v2):
            sp = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg RV",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
            )

        db_curriculum = Curriculum.query.get(sp.curriculum_id)
        ordered = CurriculumService.get_all_topics_ordered(db_curriculum)
        names = [t.name for t in ordered]
        # Section A (display_order=1) must come before Section B (display_order=2)
        assert names == ["A Topic", "B Topic"]

    def test_v2_current_topic_marked_learning(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(db, user, v2, curriculum_topic_code="T2-A.1")

        topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Alpha Topic",
        ).first()
        assert topic is not None

        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic.id,
        ).first()
        assert tp is not None
        assert tp.current_stage == TopicProgress.STAGE_LEARNING
        assert tp.completed is False

    def test_v2_completed_topics_initialised_correctly(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(
            db, user, v2,
            curriculum_topic_code="T2-A.2",
            completed_curriculum_topics=["T2-A.1"],
        )

        alpha_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha_topic.id,
        ).first()
        assert tp.completed is True
        assert tp.mastery_score == 100.0
        assert tp.confidence == "Mastered"

    def test_v2_current_topic_never_marked_completed_even_if_in_list(self, ctx, db):
        """The current topic must not be completed even if its code appears in
        completed_curriculum_topics."""
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(
            db, user, v2,
            curriculum_topic_code="T2-A.1",
            completed_curriculum_topics=["T2-A.1"],  # both current and completed
        )

        alpha_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha_topic.id,
        ).first()
        assert tp.completed is False
        assert tp.current_stage == TopicProgress.STAGE_LEARNING

    def test_v2_idempotency_no_duplicate_progress_rows(self, ctx, db):
        """Creating a second plan against the same V2 curriculum must not
        create duplicate TopicProgress rows."""
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.1",
            )
        first_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert first_count == 3

        with _patch_repo_for_v2(v2):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="October 2027",
                exam_date=date.today() + timedelta(days=365),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Revision",
                study_preference="Questions First",
                target_grade="A",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.2",
            )
        second_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert second_count == 3  # No duplicates

    def test_v2_existing_topic_progress_not_overwritten(self, ctx, db):
        """Pre-existing TopicProgress values must survive V2 plan re-creation."""
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            sp1 = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.1",
            )

        alpha_topic = DBTopic.query.filter_by(
            curriculum_id=sp1.curriculum_id, name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha_topic.id,
        ).first()
        tp.mastery_score = 90.0
        tp.completed = True
        tp.confidence = "High"
        db.session.commit()

        with _patch_repo_for_v2(v2):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="October 2027",
                exam_date=date.today() + timedelta(days=365),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Revision",
                study_preference="Mixed",
                target_grade="A",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.2",
            )

        tp_check = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha_topic.id,
        ).first()
        assert tp_check.mastery_score == 90.0
        assert tp_check.completed is True
        assert tp_check.confidence == "High"

    def test_v2_learning_objectives_created_in_display_order(self, ctx, db):
        """LOs for V2 topics must be created sorted by display_order."""
        from app.models.curriculum import Topic as DBTopic
        from app.models.learning import LearningObjective

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()
        sp = self._create_v2_plan(db, user, v2)

        alpha_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id, name="Alpha Topic",
        ).first()
        assert alpha_topic is not None

        los = (
            LearningObjective.query
            .filter_by(topic_id=alpha_topic.id, active=True)
            .order_by(LearningObjective.order)
            .all()
        )
        assert len(los) == 2
        assert los[0].order == 1
        assert los[1].order == 2
        assert "T2-A.1.1" in los[0].description
        assert "T2-A.1.2" in los[1].description


# ═══════════════════════════════════════════════════════════════════════════════
# V1 / V2 Coexistence
# ═══════════════════════════════════════════════════════════════════════════════


class TestV1V2Coexistence:
    """V1 and V2 curricula must be independently initialised without
    interfering with each other."""

    def test_v1_and_v2_plans_coexist_for_different_users(self, ctx, db):
        """A V1 plan for user A and a V2 plan for user B must not mix
        TopicProgress rows."""
        from app.models.topic_progress import TopicProgress
        from app.models.user import User
        from app.services.study_plan_service import StudyPlanService

        u1 = User(email="v1user@example.com", is_active_user=True)
        u1.set_password("pw")
        u2 = User(email="v2user@example.com", is_active_user=True)
        u2.set_password("pw")
        db.session.add_all([u1, u2])
        db.session.commit()

        # V1 plan for u1
        StudyPlanService.create_study_plan(
            user_id=u1.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )

        # V2 plan for u2
        v2 = _make_v2_engine_curriculum()
        with _patch_repo_for_v2(v2):
            StudyPlanService.create_study_plan(
                user_id=u2.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
            )

        u1_count = TopicProgress.query.filter_by(user_id=u1.id).count()
        u2_count = TopicProgress.query.filter_by(user_id=u2.id).count()
        assert u1_count == 14  # canonical CS1 V2
        assert u2_count == 3  # V2 mock (3 topics)


# ═══════════════════════════════════════════════════════════════════════════════
# Ordering Stability
# ═══════════════════════════════════════════════════════════════════════════════


class TestOrderingStability:
    """Canonical topic ordering must be deterministic."""

    def test_v1_topic_ordering_stable_across_calls(self, ctx, db):
        """_get_engine_topics_ordered on V1 must return the same sequence
        every time it is called."""
        from app.services.study_plan_service import StudyPlanService

        result = StudyPlanService._load_engine_curriculum_auto("IFoA", "CS1", "2026")
        assert result is not None
        ec, is_v2 = result
        first = [
            t.code for t in StudyPlanService._get_engine_topics_ordered(ec, is_v2)
        ]
        second = [
            t.code for t in StudyPlanService._get_engine_topics_ordered(ec, is_v2)
        ]
        assert first == second

    def test_v2_topic_ordering_stable_across_calls(self, ctx, db):
        from app.services.study_plan_service import StudyPlanService

        v2 = _make_v2_engine_curriculum()
        first = [t.code for t in StudyPlanService._get_engine_topics_ordered(v2, True)]
        second = [t.code for t in StudyPlanService._get_engine_topics_ordered(v2, True)]
        assert first == second

    def test_v2_db_canonical_order_matches_engine_order(self, ctx, db):
        """CurriculumService.get_all_topics_ordered on the DB side must return
        topics in the same order as _get_engine_topics_ordered on the engine side."""
        from app.models.curriculum import Curriculum
        from app.services.curriculum_service import CurriculumService
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            sp = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
            )

        engine_order = [
            t.title
            for t in StudyPlanService._get_engine_topics_ordered(v2, True)
        ]
        db_curriculum = Curriculum.query.get(sp.curriculum_id)
        db_order = [
            t.name
            for t in CurriculumService.get_all_topics_ordered(db_curriculum)
        ]
        assert engine_order == db_order


# ═══════════════════════════════════════════════════════════════════════════════
# _create_topic_progress_if_absent
# ═══════════════════════════════════════════════════════════════════════════════


class TestCreateTopicProgressIfAbsent:
    """Unit tests for the extracted helper."""

    def test_creates_row_when_absent(self, ctx, db):
        from app.models.curriculum import Curriculum
        from app.models.curriculum import Topic as DBTopic
        from app.models.study_plan import StudyPlan
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)

        c = Curriculum(exam_name="UnitTest C", version="2026", active=True)
        db.session.add(c)
        db.session.flush()
        t = DBTopic(
            curriculum_id=c.id, name="T1", order=1,
            recommended_minutes=30, active=True,
        )
        db.session.add(t)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="UnitTest C",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            active=True,
            curriculum_id=c.id,
        )
        db.session.add(sp)
        db.session.commit()

        StudyPlanService._create_topic_progress_if_absent(sp, t, "T1-CODE", [])
        db.session.commit()

        tp = TopicProgress.query.filter_by(user_id=user.id, topic_id=t.id).first()
        assert tp is not None
        assert tp.completed is False
        assert tp.current_stage == TopicProgress.STAGE_NOT_STARTED

    def test_skips_creation_when_row_exists(self, ctx, db):
        from app.models.curriculum import Curriculum
        from app.models.curriculum import Topic as DBTopic
        from app.models.study_plan import StudyPlan
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)

        c = Curriculum(exam_name="UnitTest D", version="2026", active=True)
        db.session.add(c)
        db.session.flush()
        t = DBTopic(
            curriculum_id=c.id, name="T2", order=1,
            recommended_minutes=30, active=True,
        )
        db.session.add(t)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="UnitTest D",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            active=True,
            curriculum_id=c.id,
        )
        db.session.add(sp)

        # Pre-existing row with custom mastery
        existing_tp = TopicProgress(
            user_id=user.id, topic_id=t.id,
            mastery_score=75.0, completed=False,
            confidence="High",
            current_stage=TopicProgress.STAGE_PRACTISING,
        )
        db.session.add(existing_tp)
        db.session.commit()

        StudyPlanService._create_topic_progress_if_absent(sp, t, "T2-CODE", [])
        db.session.commit()

        rows = TopicProgress.query.filter_by(user_id=user.id, topic_id=t.id).all()
        assert len(rows) == 1  # No new row
        assert rows[0].mastery_score == 75.0  # Untouched

    def test_creates_completed_row_for_completed_code(self, ctx, db):
        from app.models.curriculum import Curriculum
        from app.models.curriculum import Topic as DBTopic
        from app.models.study_plan import StudyPlan
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)

        c = Curriculum(exam_name="UnitTest E", version="2026", active=True)
        db.session.add(c)
        db.session.flush()
        t = DBTopic(
            curriculum_id=c.id, name="T3", order=1,
            recommended_minutes=30, active=True,
        )
        db.session.add(t)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="UnitTest E",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            active=True,
            curriculum_id=c.id,
        )
        db.session.add(sp)
        db.session.commit()

        StudyPlanService._create_topic_progress_if_absent(
            sp, t, "T3-CODE", ["T3-CODE"]
        )
        db.session.commit()

        tp = TopicProgress.query.filter_by(user_id=user.id, topic_id=t.id).first()
        assert tp is not None
        assert tp.completed is True
        assert tp.mastery_score == 100.0
        assert tp.confidence == "Mastered"
        assert tp.current_stage == TopicProgress.STAGE_COMPLETED


# ═══════════════════════════════════════════════════════════════════════════════
# _sync_completed_topics — V2 awareness
# ═══════════════════════════════════════════════════════════════════════════════


class TestSyncCompletedTopicsV2:
    """_sync_completed_topics must handle V2 curricula via the canonical
    engine loading helpers."""

    def test_v2_sync_marks_topic_completed(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            sp = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.2",
            )

        with _patch_repo_for_v2(v2):
            StudyPlanService._sync_completed_topics(
                sp,
                completed_codes=["T2-A.1"],
                curriculum_topic_code="T2-A.2",
            )
        db.session.commit()

        alpha = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id, name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha.id,
        ).first()
        assert tp.completed is True
        assert tp.mastery_score == 100.0

    def test_v2_sync_never_marks_current_topic_completed(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            sp = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.1",
            )

        with _patch_repo_for_v2(v2):
            StudyPlanService._sync_completed_topics(
                sp,
                completed_codes=["T2-A.1"],  # current topic in completed list
                curriculum_topic_code="T2-A.1",
            )
        db.session.commit()

        alpha = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id, name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha.id,
        ).first()
        # Must stay Learning, not Completed
        assert tp.current_stage == TopicProgress.STAGE_LEARNING
        assert tp.completed is False

    def test_v2_sync_resets_unchecked_previously_completed_topic(self, ctx, db):
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress
        from app.services.study_plan_service import StudyPlanService

        user = _make_user(db)
        v2 = _make_v2_engine_curriculum()

        with _patch_repo_for_v2(v2):
            sp = StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="TestOrg T2",
                exam_sitting="April 2027",
                exam_date=date.today() + timedelta(days=180),
                weekday_study_minutes=60,
                weekend_study_minutes=120,
                current_stage="Learning",
                study_preference="Mixed",
                target_grade="B",
                curriculum_version="2026",
                curriculum_topic_code="T2-A.2",
                completed_curriculum_topics=["T2-A.1"],
            )

        # Now user un-checks T2-A.1
        with _patch_repo_for_v2(v2):
            StudyPlanService._sync_completed_topics(
                sp,
                completed_codes=[],  # T2-A.1 removed
                curriculum_topic_code="T2-A.2",
            )
        db.session.commit()

        alpha = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id, name="Alpha Topic",
        ).first()
        tp = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=alpha.id,
        ).first()
        assert tp.completed is False
        assert tp.current_stage == TopicProgress.STAGE_NOT_STARTED
