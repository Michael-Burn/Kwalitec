"""Tests for canonical coverage reconciliation (shadow-safe)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.coverage_reconciliation import (
    CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
    CATEGORY_CONFIRMED_COVERED,
    CATEGORY_HISTORICALLY_COMPLETED,
    CATEGORY_NOT_COVERED,
    EVIDENCE_LEGACY_COMPLETION,
    EVIDENCE_VERIFIED_COMPLETION,
    CoverageReconciliationService,
    LegacyCompletionCandidate,
    accept_legacy_completion,
)
from app.application.curriculum_identity import CurriculumIdentityService
from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
)
from app.application.curriculum_identity.seed_cs1_active import load_cs1_active_seed
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from app.models.topic_progress import TopicProgress
from app.models.user import User
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


def _append_runtime_event(
    *,
    user_id: int,
    event_type: EducationalEventType,
    topic_id: str,
    curriculum_identity: str = ACTIVE_CS1_CURRICULUM_VERSION,
    payload: dict | None = None,
) -> RuntimeEducationalEvent:
    import json

    row = RuntimeEducationalEvent(
        event_id=f"evt-{uuid4().hex[:16]}",
        event_type=event_type.value,
        user_id=user_id,
        curriculum_identity=curriculum_identity,
        topic_id=topic_id,
        payload_json=json.dumps(payload or {"source": "mission_completion"}),
        occurred_at=datetime.now(UTC).replace(tzinfo=None),
    )
    db.session.add(row)
    db.session.commit()
    return row


class TestLegacyAcceptanceContract:
    def test_rejects_orphan_mapping(self):
        result = accept_legacy_completion(
            LegacyCompletionCandidate(
                user_id=1,
                learner_user_id=1,
                completed=True,
                last_reviewed=None,
                revision_count=0,
                mapping_status="obsolete_no_equivalent",
                canonical_id=None,
                prior_knowledge_claim_present=False,
            )
        )
        assert result.accepted is False
        assert "canonical" in result.reason or "mapping" in result.reason

    def test_rejects_prior_knowledge_declaration_only(self):
        result = accept_legacy_completion(
            LegacyCompletionCandidate(
                user_id=1,
                learner_user_id=1,
                completed=True,
                last_reviewed=None,
                revision_count=0,
                mapping_status="exact",
                canonical_id="canonical-1",
                prior_knowledge_claim_present=True,
            )
        )
        assert result.accepted is False
        assert result.reason == "prior_knowledge_declaration_only"

    def test_accepts_historical_study_progress_without_claim(self):
        result = accept_legacy_completion(
            LegacyCompletionCandidate(
                user_id=1,
                learner_user_id=1,
                completed=True,
                last_reviewed=None,
                revision_count=0,
                mapping_status="exact",
                canonical_id="canonical-1",
                prior_knowledge_claim_present=False,
            )
        )
        assert result.accepted is True
        assert result.reason == "stage_a_completed_historical_study_progress"


class TestCoverageReconciliationClassification:
    def test_both_signals_confirmed_covered(self, app, db, cs1_identity_populated):
        with app.app_context():
            user = _make_user("both-signals@example.com")
            topic, entry = _stage_a_topic_for_code("1.1")
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
            _append_runtime_event(
                user_id=user.id,
                event_type=EducationalEventType.TOPIC_COMPLETED,
                topic_id=str(entry["published_source_id"]),
            )

            result = CoverageReconciliationService.reconcile_learner(user.id)
            verdict = next(
                v
                for v in result.canonical_verdicts
                if v.canonical_id == entry["canonical_id"]
            )
            assert verdict.eligibility == CATEGORY_CONFIRMED_COVERED
            assert verdict.legacy_completion_accepted is True
            assert verdict.verified_completion_accepted is True
            assert EVIDENCE_LEGACY_COMPLETION in verdict.evidence_sources
            assert EVIDENCE_VERIFIED_COMPLETION in verdict.evidence_sources

    def test_legacy_only_historically_completed(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = _make_user("legacy-only@example.com")
            topic, entry = _stage_a_topic_for_code("2.1")
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
            assert verdict.legacy_completion_accepted is True
            assert verdict.verified_completion_present is False
            assert verdict.evidence_sources == (EVIDENCE_LEGACY_COMPLETION,)

    def test_verified_only_confirmed_covered(self, app, db, cs1_identity_populated):
        with app.app_context():
            user = _make_user("verified-only@example.com")
            _topic, entry = _stage_a_topic_for_code("3.1")
            _append_runtime_event(
                user_id=user.id,
                event_type=EducationalEventType.TOPIC_COMPLETED,
                topic_id=str(entry["published_source_id"]),
            )

            result = CoverageReconciliationService.reconcile_learner(user.id)
            verdict = next(
                v
                for v in result.canonical_verdicts
                if v.canonical_id == entry["canonical_id"]
            )
            assert verdict.eligibility == CATEGORY_CONFIRMED_COVERED
            assert verdict.legacy_completion_present is False
            assert verdict.verified_completion_accepted is True
            assert verdict.evidence_sources == (EVIDENCE_VERIFIED_COMPLETION,)

    def test_neither_signal_not_covered(self, app, db, cs1_identity_populated):
        with app.app_context():
            user = _make_user("neither@example.com")
            result = CoverageReconciliationService.reconcile_learner(user.id)
            assert len(result.canonical_verdicts) == 14
            assert all(
                v.eligibility == CATEGORY_NOT_COVERED for v in result.canonical_verdicts
            )
            assert result.summary[CATEGORY_NOT_COVERED] == 14
            assert result.unmapped_activity == ()

    def test_orphan_stage_a_completion_is_ambiguous_never_covered(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = _make_user("orphan-complete@example.com")
            curriculum = Curriculum.query.filter_by(
                exam_name="IFoA CS1", version="2026", active=True
            ).first()
            orphan = Topic.query.filter_by(
                curriculum_id=curriculum.id, name="T0"
            ).first()
            assert orphan is not None
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=orphan.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                )
            )
            db.session.commit()

            result = CoverageReconciliationService.reconcile_learner(user.id)
            assert result.unmapped_activity
            assert all(
                item.eligibility == CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY
                for item in result.unmapped_activity
            )
            assert all(
                v.eligibility == CATEGORY_NOT_COVERED for v in result.canonical_verdicts
            )
            # Never silently promote orphan activity onto a canonical topic.
            assert all(
                not v.legacy_completion_present for v in result.canonical_verdicts
            )

    def test_prior_knowledge_claim_with_stage_a_is_ambiguous(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = _make_user("claim-only@example.com")
            topic, entry = _stage_a_topic_for_code("4.1")
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
            _append_runtime_event(
                user_id=user.id,
                event_type=EducationalEventType.PRIOR_KNOWLEDGE_CLAIM,
                topic_id=str(entry["published_source_id"]),
                payload={
                    "source": "baseline_self_declared",
                    "warrant": "thin_self_declared",
                },
            )

            result = CoverageReconciliationService.reconcile_learner(user.id)
            verdict = next(
                v
                for v in result.canonical_verdicts
                if v.canonical_id == entry["canonical_id"]
            )
            assert verdict.eligibility == CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY
            assert verdict.legacy_completion_present is True
            assert verdict.legacy_completion_accepted is False
            assert verdict.evidence_sources == ()
