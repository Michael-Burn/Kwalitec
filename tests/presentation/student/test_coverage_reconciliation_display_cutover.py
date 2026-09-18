"""Live coverage display cutover to dual-source reconciliation.

Proves Study / Stats / Settings export reflect reconciled coverage
(CONFIRMED_COVERED + HISTORICALLY_COMPLETED), including legacy-only accepted
completions that verified-only F1 never counted. Preserves the original
engines in-code; does not touch Exam Readiness withhold.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.coverage_reconciliation import (
    CATEGORY_HISTORICALLY_COMPLETED,
    CoverageReconciliationService,
)
from app.application.curriculum_identity import CurriculumIdentityService
from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
)
from app.application.curriculum_identity.seed_cs1_active import load_cs1_active_seed
from app.application.study_curriculum.types import CurriculumLearningSnapshot
from app.extensions import db
from app.models.curriculum import Topic
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.presentation.student.coverage_honesty import (
    reconciled_coverage_for_learner,
    verified_coverage_from_progress,
)
from app.presentation.student.exam_readiness_withheld import (
    EXAM_READINESS_NOT_YET_ASSESSABLE,
    student_facing_exam_readiness_claim,
    student_facing_exam_readiness_percentage,
)
from app.presentation.student.services.honest_progress_service import (
    HonestProgressService,
)
from app.presentation.student.services.student_study_curriculum_service import (
    StudentStudyCurriculumPresentationService,
)
from tests.application.curriculum_identity.test_canonical_identity_layer import (
    _populate_stage_a_cs1,
)


@pytest.fixture
def cs1_identity_populated(app, db):
    with app.app_context():
        _populate_stage_a_cs1(include_orphans=True)
        counts = CurriculumIdentityService.ensure_active_cs1_populated(
            require_stage_a=True
        )
        assert counts["canonical_inserted"] == 14
    yield


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _stage_a_topic_for_code(syllabus_code: str) -> tuple[Topic, dict]:
    seed = load_cs1_active_seed()
    entry = next(t for t in seed["topics"] if t["syllabus_code"] == syllabus_code)
    chain = CurriculumIdentityService.chain_for_published(
        str(entry["published_source_id"])
    )
    topic = db.session.get(Topic, int(chain["stage_a_source_id"]))
    assert topic is not None
    return topic, entry


class _EmptyAssembler:
    def assemble(
        self, *, user_id: int, subject_code: str
    ) -> CurriculumLearningSnapshot:
        return CurriculumLearningSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=ACTIVE_CS1_CURRICULUM_VERSION,
            topics=(),
        )


class TestReconciledDisplayProjection:
    def test_display_counts_historically_completed(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = _make_user(f"cutover-legacy-{uuid4().hex[:8]}@example.com")
            topic, entry = _stage_a_topic_for_code("1.1")
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=topic.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                    revision_count=0,
                    last_reviewed=None,
                )
            )
            db.session.commit()

            result = CoverageReconciliationService.reconcile_learner(user.id)
            verdict = next(
                v
                for v in result.canonical_verdicts
                if v.canonical_id == entry["canonical_id"]
            )
            assert verdict.eligibility == CATEGORY_HISTORICALLY_COMPLETED

            display = CoverageReconciliationService.display_coverage(result)
            assert display.covered_count == 1
            assert display.historically_completed_count == 1
            assert display.confirmed_covered_count == 0
            assert display.topic_count == 14
            assert display.coverage_percent == int(round(100 / 14))
            assert display.coverage_label == "1 of 14 topics completed"

            via_helper = reconciled_coverage_for_learner(user.id)
            assert via_helper.covered_count == display.covered_count
            assert via_helper.coverage_percent == display.coverage_percent


class TestSwitchedSurfacesUseReconciliation:
    def test_study_and_stats_show_legacy_only_completion(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = _make_user(f"cutover-study-{uuid4().hex[:8]}@example.com")
            topic, _entry = _stage_a_topic_for_code("2.1")
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=topic.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                    revision_count=1,
                    last_reviewed=datetime.now(UTC).replace(tzinfo=None),
                )
            )
            db.session.commit()

            expected = CoverageReconciliationService.coverage_for_learner(user.id)
            assert expected.historically_completed_count == 1
            assert expected.covered_count == 1

            study = StudentStudyCurriculumPresentationService(
                assembler=_EmptyAssembler(),
                why_lookup=lambda _code: {},
            ).build(user_id=user.id, subject_code="CS1", subject_label="CS1")
            assert study.covered_count == expected.covered_count
            assert study.topic_count == expected.topic_count
            assert study.coverage_label == expected.coverage_label
            assert study.coverage_ratio == pytest.approx(expected.coverage_ratio)

            stats = HonestProgressService(
                assembler=_EmptyAssembler(),
            )
            stats._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
            with app.test_request_context("/student/progress"):
                page = stats.build_progress_page(user_id=user.id)
            assert page.covered_count == expected.covered_count
            assert page.topic_count == expected.topic_count
            assert page.syllabus_coverage_label == expected.coverage_label
            assert page.syllabus_coverage_percent == expected.coverage_percent

    def test_settings_export_uses_reconciled_percent(
        self, app, db, cs1_identity_populated, logged_in_client, user, monkeypatch
    ):
        monkeypatch.setattr(
            "app.services.twin_cutover_service.subject_code_for_user",
            lambda _uid: "CS1",
        )
        with app.app_context():
            topic, _entry = _stage_a_topic_for_code("3.1")
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=topic.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                    revision_count=0,
                    last_reviewed=None,
                )
            )
            db.session.commit()
            expected = CoverageReconciliationService.coverage_for_learner(user.id)
            assert expected.covered_count == 1

            response = logged_in_client.get("/settings/export/pdf")
            assert response.status_code == 200
            body = response.get_data(as_text=True)
            assert "reconciled dual-source Study Progress" in body
            assert f"{expected.coverage_percent}%" in body
            assert "not Exam Readiness" in body
            # Exam Readiness withhold must remain on the same export.
            assert EXAM_READINESS_NOT_YET_ASSESSABLE in body
            assert student_facing_exam_readiness_claim() in body


class TestExamReadinessWithheldUnaffected:
    def test_coverage_cutover_does_not_mint_exam_readiness_percent(self):
        """Regression: reconciled coverage never becomes Exam Readiness %."""
        assert student_facing_exam_readiness_percentage() is None
        claim = student_facing_exam_readiness_claim()
        assert claim == EXAM_READINESS_NOT_YET_ASSESSABLE
        assert "%" not in claim

    def test_verified_only_helper_still_exists_for_diagnostics(self):
        """Original verified-only presentation helper remains callable."""
        class _Snap:
            topic_ids = ("a", "b")
            verified_completed_topic_ids = ("a",)
            prior_knowledge_claimed_topic_ids = ()
            verified_coverage_ratio = 0.5
            completed_topic_ids = ("a",)
            coverage_ratio = 0.5

        parts = verified_coverage_from_progress(_Snap())
        assert parts.verified_count == 1
        assert parts.verified_percent == 50
