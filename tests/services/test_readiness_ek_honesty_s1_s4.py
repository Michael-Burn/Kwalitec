"""Readiness / analytics EK honesty fixes (S1-S4 pre-deploy inventory).

Proves absence of Twin evidence is never represented as a measured low value.
"""

from __future__ import annotations

from datetime import date

import pytest

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE
from app.application.student_twin.query import TopicKnowledgeFact
from app.extensions import db
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from app.services.analytics_service import AnalyticsService
from app.services.curriculum_service import CurriculumService
from app.services.readiness_quality import (
    CONFIDENCE_CANNOT_ESTIMATE,
    apply_readiness_quality_contract,
)
from app.services.readiness_service import ReadinessService


def _ek_fact(
    topic_id: str,
    *,
    ek: float,
    evidence_count: int = POLICY_V1_MIN_EVIDENCE,
) -> TopicKnowledgeFact:
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=True,
        estimated_knowledge=ek,
        estimated_mastery=ek,
        evidence_count=evidence_count,
        last_practised_at=None,
    )


@pytest.mark.usefixtures("ctx")
class TestS1CompositeWithoutFabricatedZeroMastery:
    """Zero Twin EK topics must not drag composite via a fabricated 0.0."""

    def test_no_evidence_reweights_composite_and_signals_unavailable(
        self, user, subject, curriculum, study_plan, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )

        completed_topic = leaf_topics[0]
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=completed_topic.id,
                completed=True,
                revision_count=1,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.add(
            Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=study_plan.id,
                mission_date=date.today(),
                title="Review mission",
                status="Completed",
            )
        )
        db.session.commit()

        result = ReadinessService.get_overall_readiness(user.id)

        assert result["mastery_available"] is False
        assert result["avg_mastery"] is None
        assert result["topics_with_ek_evidence"] == 0
        # Re-weighted: coverage 50% + review 100% over 70% weight, not 0 mastery.
        assert result["score"] == pytest.approx(
            ((result["coverage_pct"] * 0.50) + (100.0 * 0.20)) / 0.70,
            abs=0.2,
        )
        fabricated_zero_score = (
            (result["coverage_pct"] * 0.50) + (0.0 * 0.30) + (100.0 * 0.20)
        )
        assert result["score"] != pytest.approx(fabricated_zero_score, abs=0.5)

    def test_with_evidence_uses_full_composite(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        topic = leaf_topics[0]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {topic.id: _ek_fact("CS1-A-T01", ek=0.8)},
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=True,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.commit()

        result = ReadinessService.get_overall_readiness(user.id)

        assert result["mastery_available"] is True
        assert result["avg_mastery"] == pytest.approx(80.0, abs=0.1)
        assert result["topics_with_ek_evidence"] == 1


@pytest.mark.usefixtures("ctx")
class TestS2TopicsWithEkEvidenceCount:
    """Twin-practised topic count must not alias Study Progress completion."""

    def test_completed_without_twin_does_not_inflate_ek_topic_count(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )
        completed = leaf_topics[0]
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=completed.id,
                completed=True,
                revision_count=4,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.commit()

        result = ReadinessService.get_overall_readiness(user.id)

        assert result["topics_completed"] == 1
        assert result["topics_started"] == 1
        assert result["topics_with_ek_evidence"] == 0

    def test_twin_evidence_without_completion_counts_for_ek_only(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        topic = leaf_topics[0]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {topic.id: _ek_fact("CS1-A-T01", ek=0.6)},
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=False,
                revision_count=2,
                current_stage=TopicProgress.STAGE_PRACTISING,
            )
        )
        db.session.commit()

        result = ReadinessService.get_overall_readiness(user.id)

        assert result["topics_completed"] == 0
        assert result["topics_with_ek_evidence"] == 1


@pytest.mark.usefixtures("ctx")
class TestS3MasteredFromTwinEkNotStaleStage:
    """STAGE_MASTERED label must not act as a live knowledge signal."""

    def test_stale_stage_mastered_without_ek_not_counted(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        topic = leaf_topics[0]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=True,
                current_stage=TopicProgress.STAGE_MASTERED,
            )
        )
        db.session.commit()

        metrics = ReadinessService._study_progress_metrics(user.id)
        assert metrics["topics_mastered"] == 0

    def test_ek_mastered_with_sufficient_evidence_is_counted(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        topic = leaf_topics[0]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {
                topic.id: _ek_fact("CS1-A-T01", ek=0.92, evidence_count=3),
            },
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=True,
                current_stage=TopicProgress.STAGE_PRACTISING,
            )
        )
        db.session.commit()

        metrics = ReadinessService._study_progress_metrics(user.id)
        assert metrics["topics_mastered"] == 1

    def test_review_backlog_excludes_ek_mastered_not_stale_stage(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        topic = topics[0]
        review_due = date.today()
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {
                topic.id: _ek_fact("CS1-A-T01", ek=0.95, evidence_count=3),
            },
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topic.id,
                completed=True,
                current_stage=TopicProgress.STAGE_PRACTISING,
                next_review_date=review_due,
            )
        )
        db.session.commit()

        backlog = ReadinessService.get_review_backlog(user.id)
        assert backlog["total_backlog"] == 0

    def test_insufficient_evidence_ek_does_not_count_as_mastered(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        topic = leaf_topics[0]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {
                topic.id: _ek_fact("CS1-A-T01", ek=0.95, evidence_count=2),
            },
        )
        db.session.commit()

        metrics = ReadinessService._study_progress_metrics(user.id)
        assert metrics["topics_mastered"] == 0


@pytest.mark.usefixtures("ctx")
class TestS4AnalyticsCoverageFromStudyProgress:
    """Analytics weekly trend coverage must follow Study Progress, not EK counts."""

    def test_coverage_uses_completed_not_ek_topic_count(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        if len(leaf_topics) < 2:
            pytest.skip("Need at least two leaf topics for coverage divergence test")

        completed_a, completed_b, ek_only = (
            leaf_topics[0],
            leaf_topics[1],
            leaf_topics[2] if len(leaf_topics) > 2 else leaf_topics[1],
        )
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {
                ek_only.id: _ek_fact("CS1-A-T99", ek=0.7),
            },
        )
        db.session.add_all(
            [
                TopicProgress(
                    user_id=user.id,
                    topic_id=completed_a.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                ),
                TopicProgress(
                    user_id=user.id,
                    topic_id=completed_b.id,
                    completed=True,
                    current_stage=TopicProgress.STAGE_COMPLETED,
                ),
            ]
        )
        db.session.commit()

        trend = AnalyticsService.get_readiness_over_time(user.id, weeks=1)
        study_progress_coverage = round((2 / len(leaf_topics)) * 100.0, 1)
        ek_driven_coverage = round((1 / len(leaf_topics)) * 100.0, 1)

        assert trend[0]["coverage_pct"] == pytest.approx(
            study_progress_coverage, abs=0.1
        )
        assert trend[0]["coverage_pct"] != pytest.approx(ek_driven_coverage, abs=0.1)

    def test_analytics_avg_mastery_none_without_evidence(
        self, user, curriculum, monkeypatch
    ) -> None:
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )

        trend = AnalyticsService.get_readiness_over_time(user.id, weeks=1)
        assert trend[0]["avg_mastery"] is None


@pytest.mark.usefixtures("ctx")
class TestLeftoverMissionsCannotMintReadiness:
    """Honest refusal when leftover missions exist without earned evidence.

    Closes the gap that displayed ~29% from orphaned mission completion
    with no study plan, 0% Study Progress, and no Twin Estimated Knowledge.
    """

    def test_orphaned_completed_mission_without_plan_is_honest_refusal(
        self, user, subject, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )
        db.session.add(
            Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=None,
                mission_date=date.today(),
                title="Orphaned leftover mission",
                status="Completed",
            )
        )
        db.session.commit()

        overall = ReadinessService.get_overall_readiness(user.id)
        assert overall["total_topics"] == 0
        assert overall["topics_started"] == 0
        assert overall["topics_with_ek_evidence"] == 0
        assert overall["avg_mastery"] is None
        assert overall["score"] == 0.0
        assert overall["review_discipline"] == 0.0

        surface = apply_readiness_quality_contract(
            user.id,
            {
                "readiness": dict(overall),
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "legacy",
                "confidence_level": "",
                "limitations_codes": [],
                "readiness_drivers": [],
                "recommended_next_actions": [],
                "explainability": {},
            },
        )
        assert surface["honest_refusal"] is True
        assert surface["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE
        assert surface["judgement"] == (
            "Estimated readiness: cannot yet be estimated"
        )
        displayed = surface.get("readiness") or {}
        assert float(displayed.get("score") or 0.0) == 0.0

    def test_plan_scoped_completed_mission_without_coverage_or_ek_is_refused(
        self, user, subject, curriculum, study_plan, monkeypatch
    ) -> None:
        """Even a current-plan completed mission cannot mint a percentage alone."""
        curr, topics = curriculum
        leaf_topics = [
            t for t in CurriculumService.get_ordered_topics(curr) if t.is_leaf_topic()
        ]
        monkeypatch.setattr(
            ReadinessService,
            "_leaf_topics_for_user",
            staticmethod(lambda _uid, read_only=False: leaf_topics),
        )
        monkeypatch.setattr(
            "app.services.twin_cutover_service.topic_ek_by_orm_id",
            lambda **kwargs: {},
        )
        db.session.add(
            Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=study_plan.id,
                mission_date=date.today(),
                title="Completed with no study evidence",
                status="Completed",
            )
        )
        db.session.commit()

        overall = ReadinessService.get_overall_readiness(user.id)
        assert overall["topics_started"] == 0
        assert overall["topics_with_ek_evidence"] == 0
        assert overall["avg_mastery"] is None
        assert overall["coverage_pct"] == 0.0
        assert overall["score"] == 0.0
        assert overall["review_discipline"] == 100.0

        score, _available = ReadinessService._composite_readiness_score(
            coverage_pct=0.0,
            avg_mastery=None,
            review_discipline=100.0,
        )
        assert score == 0.0

        surface = apply_readiness_quality_contract(
            user.id,
            {
                "readiness": dict(overall),
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "legacy",
                "confidence_level": "",
                "limitations_codes": [],
                "readiness_drivers": [],
                "recommended_next_actions": [],
                "explainability": {},
            },
        )
        assert surface["honest_refusal"] is True
        assert surface["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE

    def test_original_29_percent_surface_is_honest_refusal(self, user) -> None:
        """Exact leftover-mission card: 29% score, 0% started, no Twin EK."""
        surface = apply_readiness_quality_contract(
            user.id,
            {
                "readiness": {
                    "score": 28.6,
                    "coverage_pct": 0.0,
                    "avg_mastery": None,
                    "mastery_available": False,
                    "review_discipline": 100.0,
                    "total_topics": 59,
                    "topics_started": 0,
                    "topics_completed": 0,
                    "topics_mastered": 0,
                    "topics_with_ek_evidence": 0,
                },
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "legacy",
                "confidence_level": "",
                "limitations_codes": [],
                "readiness_drivers": [],
                "recommended_next_actions": [],
                "explainability": {},
            },
        )
        assert surface["honest_refusal"] is True
        assert surface["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE
        assert "29" not in (surface.get("judgement") or "")
        assert surface["judgement"] == (
            "Estimated readiness: cannot yet be estimated"
        )

    def test_brand_new_account_still_refuses(self, user) -> None:
        overall = ReadinessService.get_overall_readiness(user.id)
        assert overall["score"] == 0.0
        assert overall["total_topics"] == 0
        assert overall["topics_started"] == 0
        assert overall["topics_with_ek_evidence"] == 0

        surface = apply_readiness_quality_contract(
            user.id,
            {
                "readiness": dict(overall),
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "legacy",
                "confidence_level": "",
                "limitations_codes": [],
                "readiness_drivers": [],
                "recommended_next_actions": [],
                "explainability": {},
            },
        )
        assert surface["honest_refusal"] is True
        assert surface["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE

    def test_orphaned_missions_are_ignored_in_review_discipline(
        self, user, subject, study_plan
    ) -> None:
        db.session.add(
            Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=None,
                mission_date=date.today(),
                title="Orphan completed",
                status="Completed",
            )
        )
        db.session.add(
            Mission(
                user_id=user.id,
                subject_id=subject.id,
                study_plan_id=study_plan.id,
                mission_date=date.today(),
                title="Current pending",
                status="Pending",
            )
        )
        db.session.commit()

        rate = ReadinessService.get_review_completion_rate(user.id)
        assert rate["total_missions"] == 1
        assert rate["completed_missions"] == 0
        assert rate["pending"] == 1
        assert rate["completion_rate"] == 0.0

